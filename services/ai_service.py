"""
services/ai_service.py - AI Engine for Smart Flashcards
Handles real Generative AI synthesis via Google Gemini or OpenAI, Pydantic data validation,
and offline Demo Mode fallback using curated datasets.
"""

import os
import json
import re
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from pydantic import BaseModel, Field, ValidationError
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Path to demo dataset
DATA_DIR = Path(__file__).resolve().parent.parent / "data"
DEMO_CARDS_FILE = DATA_DIR / "demo_cards.json"


class FlashcardItem(BaseModel):
    question: str = Field(..., min_length=5, description="Clear, college-level conceptual question")
    answer: str = Field(..., min_length=5, description="Concise, 1-2 sentence accurate answer")
    difficulty: str = Field(default="Medium", description="Easy, Medium, or Hard")
    topic: str = Field(default="", description="Topic name")


class FlashcardDeck(BaseModel):
    cards: List[FlashcardItem]


def _get_secret(name: str) -> Optional[str]:
    """
    Read a configuration value from the first source that provides it:

    1. Streamlit secrets (`st.secrets` / `.streamlit/secrets.toml`) - this is
       how Streamlit Community Cloud, and any platform that mounts a
       secrets.toml, hands keys to the app.
    2. Environment variables (`os.getenv`) - covers a local `.env` file and
       hosts that inject real env vars (Render, Docker, Hugging Face, ...).

    Never raises: a missing/unreadable secrets file simply falls through.
    """
    try:
        import streamlit as st

        if name in st.secrets:
            value = st.secrets[name]
            if value and str(value).strip():
                return str(value).strip()
    except Exception:
        # No secrets.toml present, or no Streamlit runtime available.
        pass

    value = os.getenv(name)
    return value.strip() if value and value.strip() else None


def get_active_provider_and_key(runtime_key: Optional[str] = None) -> Tuple[Optional[str], Optional[str]]:
    """
    Detect active AI provider and key.

    Priority:
      1. Key typed into the sidebar at runtime.
      2. Streamlit secrets (hosted deployments).
      3. Environment variables / local `.env` file.

    Returns: (provider_name, api_key) or (None, None)
    """
    if runtime_key and runtime_key.strip():
        k = runtime_key.strip()
        if k.startswith("sk-"):
            return "openai", k
        return "gemini", k

    # Check Gemini
    gemini_key = _get_secret("GEMINI_API_KEY") or _get_secret("GOOGLE_API_KEY")
    if gemini_key and len(gemini_key) > 8:
        return "gemini", gemini_key

    # Check OpenAI
    openai_key = _get_secret("OPENAI_API_KEY")
    if openai_key and len(openai_key) > 8:
        return "openai", openai_key

    return None, None


def is_ai_connected(runtime_key: Optional[str] = None) -> bool:
    """Check if any valid API key is available."""
    provider, key = get_active_provider_and_key(runtime_key)
    return provider is not None and key is not None


def _clean_json_output(raw_text: str) -> str:
    """Extract clean JSON array/object from LLM markdown response."""
    text = raw_text.strip()
    match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", text)
    if match:
        return match.group(1).strip()
    return text


def load_demo_cards(topic: str, count: int = 5, difficulty: str = "Medium") -> List[Dict[str, str]]:
    """
    Load curated sample cards from data/demo_cards.json for demo mode.
    Guarantees reliable demonstration without an API key.
    """
    topic_lower = topic.strip().lower()
    demo_dict: Dict[str, List[Dict[str, str]]] = {}

    if DEMO_CARDS_FILE.exists():
        try:
            with open(DEMO_CARDS_FILE, "r", encoding="utf-8") as f:
                demo_dict = json.load(f)
        except Exception:
            demo_dict = {}

    # Find matched topic
    matched_key = None
    for key in demo_dict:
        if key in topic_lower or topic_lower in key:
            matched_key = key
            break

    cards_pool = []
    if matched_key and demo_dict.get(matched_key):
        cards_pool = demo_dict[matched_key]
    else:
        # Generic heuristic cards if topic is not in predefined bank
        title_topic = topic.strip().title() or "Core Computing"
        templates = [
            (f"What is the foundational definition of {title_topic}?",
             f"{title_topic} is a specialized technical discipline focused on the principles, design, and practical implementation of computational systems.",
             "Easy"),
            (f"What is the primary industrial or academic use-case of {title_topic}?",
             f"The primary use-case of {title_topic} is to optimize workflows, automate decision making, and engineer robust real-world architectures.",
             "Easy"),
            (f"What are the core structural components or layers in {title_topic}?",
             f"Key components include the data ingestion interface, algorithmic processing pipeline, state persistence store, and communication endpoints.",
             "Medium"),
            (f"What is a critical performance trade-off encountered in {title_topic}?",
             f"Practitioners balance computational latency and memory consumption against system reliability, security, and scalability.",
             "Medium"),
            (f"How do engineers formally evaluate and benchmark {title_topic}?",
             f"By measuring standardized throughput, convergence rates, error tolerances, and stress-testing under peak distribution loads.",
             "Hard"),
            (f"What security precautions are vital when implementing {title_topic}?",
             f"Input validation, end-to-end cryptographic protection, strict authorization controls, and deterministic audit trails.",
             "Hard"),
            (f"How does Generative AI integrate into modern {title_topic}?",
             f"Generative models synthesize synthetic training data, accelerate code development, and automate analytical summarization in {title_topic}.",
             "Medium")
        ]
        for q, a, diff in templates:
            cards_pool.append({
                "question": q,
                "answer": a,
                "difficulty": diff,
                "topic": title_topic
            })

    # Return requested count
    result = []
    for i in range(count):
        card = cards_pool[i % len(cards_pool)]
        result.append({
            "question": card["question"],
            "answer": card["answer"],
            "difficulty": card.get("difficulty", difficulty),
            "topic": card.get("topic", topic.strip().title())
        })
    return result


def _call_gemini_api(api_key: str, topic: str, count: int, difficulty: str, level: str) -> List[Dict[str, str]]:
    """Generate structured flashcards using Google Gemini 3.8 Flash via official google-genai SDK."""
    from google import genai
    from google.genai import types

    client = genai.Client(api_key=api_key)

    prompt = f"""You are an elite professor and academic study tutor.
Generate exactly {count} high-yield, college-level revision flashcards for the topic: "{topic}".
Difficulty level: {difficulty}
Student learning level: {level}

Strict Rules:
1. Each card MUST have:
   - "question": A clear conceptual question testing active recall.
   - "answer": A concise (1-2 sentences, max 35 words), precise, and exam-ready answer.
   - "difficulty": "{difficulty}"
   - "topic": "{topic}"
2. Return ONLY a valid JSON array of objects conforming to the schema. No conversational filler.
"""

    config = types.GenerateContentConfig(
        response_mime_type="application/json",
        response_schema=list[FlashcardItem],
        temperature=0.3,
    )

    response = client.models.generate_content(
        model="gemini-3.8-flash",
        contents=prompt,
        config=config,
    )

    cleaned = _clean_json_output(response.text or "")
    data = json.loads(cleaned)

    # Validate with Pydantic
    cards = []
    if isinstance(data, list):
        for item in data:
            validated = FlashcardItem.model_validate(item)
            cards.append(validated.model_dump())
    elif isinstance(data, dict) and "cards" in data:
        for item in data["cards"]:
            validated = FlashcardItem.model_validate(item)
            cards.append(validated.model_dump())
    else:
        raise ValueError("Invalid JSON format received from Gemini.")

    if not cards:
        raise ValueError("No flashcards could be parsed from AI response.")

    return cards[:count]


def _call_openai_api(api_key: str, topic: str, count: int, difficulty: str, level: str) -> List[Dict[str, str]]:
    """Generate structured flashcards using OpenAI API (gpt-4o-mini)."""
    from openai import OpenAI

    client = OpenAI(api_key=api_key)

    prompt = f"""Generate exactly {count} high-yield study flashcards for college exams on: "{topic}".
Difficulty: {difficulty}, Target level: {level}.
Each card must have:
- "question": Conceptual question
- "answer": Concise 1-2 sentence answer (max 35 words)
- "difficulty": "{difficulty}"
- "topic": "{topic}"
Return a valid JSON array of objects.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an expert tutor. Output only valid JSON arrays."},
            {"role": "user", "content": prompt}
        ],
        response_format={"type": "json_object"}
    )

    content = response.choices[0].message.content or "{}"
    parsed = json.loads(content)
    
    items = parsed if isinstance(parsed, list) else parsed.get("cards", parsed.get("flashcards", []))
    if not items and isinstance(parsed, dict):
        for v in parsed.values():
            if isinstance(v, list):
                items = v
                break

    cards = []
    for item in items:
        validated = FlashcardItem.model_validate(item)
        cards.append(validated.model_dump())

    if not cards:
        raise ValueError("No flashcards found in OpenAI response.")

    return cards[:count]


def generate_deck(
    topic: str,
    count: int = 5,
    difficulty: str = "Medium",
    level: str = "Intermediate",
    runtime_key: Optional[str] = None,
    force_demo: bool = False
) -> Dict[str, Any]:
    """
    Main entry point for flashcard generation.

    Returns a dictionary:
    {
      "success": True/False,
      "cards": [...],
      "mode": "live" | "demo",
      "provider": "gemini" | "openai" | "demo",
      "message": "Status description",
      "error": "Error details if any"
    }
    """
    clean_topic = topic.strip()
    if not clean_topic:
        return {
            "success": False,
            "cards": [],
            "mode": "error",
            "provider": None,
            "message": "Please enter a study topic before generating.",
            "error": "Empty topic"
        }

    provider, api_key = get_active_provider_and_key(runtime_key)

    # 1. Handle Demo Mode
    if force_demo or not provider:
        cards = load_demo_cards(clean_topic, count=count, difficulty=difficulty)
        msg = ("Demo Mode active – using curated academic dataset." 
               if force_demo else 
               "AI service is not connected. Add your API key to enable AI generation. (Showing Demo Mode)")
        return {
            "success": True,
            "cards": cards,
            "mode": "demo",
            "provider": "demo",
            "message": msg,
            "error": None
        }

    # 2. Live Generation
    try:
        if provider == "gemini":
            cards = _call_gemini_api(api_key, clean_topic, count, difficulty, level)
            return {
                "success": True,
                "cards": cards,
                "mode": "live",
                "provider": "Google Gemini 3.8 Flash",
                "message": f"Successfully synthesized {len(cards)} flashcards using Google Gemini AI.",
                "error": None
            }
        elif provider == "openai":
            cards = _call_openai_api(api_key, clean_topic, count, difficulty, level)
            return {
                "success": True,
                "cards": cards,
                "mode": "live",
                "provider": "OpenAI (gpt-4o-mini)",
                "message": f"Successfully synthesized {len(cards)} flashcards using OpenAI.",
                "error": None
            }
        else:
            raise ValueError("Unsupported AI provider.")

    except Exception as e:
        # Fallback to Demo with clear error notification
        demo_cards = load_demo_cards(clean_topic, count=count, difficulty=difficulty)
        return {
            "success": False,
            "cards": demo_cards,
            "mode": "demo_fallback",
            "provider": provider,
            "message": "Unable to generate flashcards via AI service. Please check your API configuration or network.",
            "error": str(e)
        }
