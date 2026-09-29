"""
ai_generator.py - Generative AI Flashcard Engine
Separated business logic for generating, validating, and managing flashcards.
Supports both Live Google Gemini API (gemini-3.8-flash) and an offline Demo/Mock mode.
"""

import os
import json
import re
from typing import List, Dict, Any, Optional, Tuple
from pydantic import BaseModel, Field, ValidationError
from dotenv import load_dotenv

# Load environment variables from .env file if available
load_dotenv()

# Pydantic Schema for strict validation of Flashcard structure
class Flashcard(BaseModel):
    question: str = Field(..., min_length=5, description="Clear, college-level conceptual question")
    answer: str = Field(..., min_length=5, description="Concise, 1-2 sentence accurate answer")

class FlashcardResponse(BaseModel):
    cards: List[Flashcard]


# ==========================================
# CURATED DEMO KNOWLEDGE BASE
# High-yield academic question banks for college topics
# ==========================================
CURATED_TOPICS: Dict[str, List[Dict[str, str]]] = {
    "machine learning": [
        {
            "question": "What is Machine Learning?",
            "answer": "Machine Learning is a branch of artificial intelligence where algorithms learn patterns from data to make decisions or predictions without explicit programming."
        },
        {
            "question": "What is Supervised Learning?",
            "answer": "Supervised learning trains algorithms on labeled datasets, mapping known inputs to correct outputs (e.g., classification and regression)."
        },
        {
            "question": "What is Unsupervised Learning?",
            "answer": "Unsupervised learning discovers hidden patterns, groupings, or clusters in unlabeled data without predefined output labels."
        },
        {
            "question": "What is the Overfitting problem in ML?",
            "answer": "Overfitting occurs when a model learns training data noise and details too closely, leading to poor generalization on unseen test data."
        },
        {
            "question": "What is the difference between Bias and Variance?",
            "answer": "Bias measures underfitting errors from oversimplified assumptions, while variance measures overfitting errors from extreme sensitivity to training data fluctuations."
        },
        {
            "question": "What is Cross-Validation?",
            "answer": "Cross-validation is a resampling technique that partitions data into multiple training and validation folds to evaluate model generalization."
        },
        {
            "question": "What is Gradient Descent?",
            "answer": "Gradient descent is an iterative optimization algorithm that minimizes a cost function by moving weights in the direction of steepest descent."
        },
        {
            "question": "What is the purpose of a Loss Function?",
            "answer": "A loss function quantifies the error between predicted outputs and actual target values during model training."
        },
        {
            "question": "What is Regularization (L1 vs L2)?",
            "answer": "Regularization penalizes large weights to prevent overfitting: L1 (Lasso) creates sparse features, while L2 (Ridge) shrinks weights toward zero."
        },
        {
            "question": "What is the ROC-AUC metric?",
            "answer": "ROC-AUC evaluates binary classifiers across varying thresholds by plotting True Positive Rate against False Positive Rate and computing area under the curve."
        },
        {
            "question": "What is Reinforcement Learning?",
            "answer": "Reinforcement learning is a paradigm where an autonomous agent learns optimal actions through trial-and-error by maximizing cumulative rewards."
        },
        {
            "question": "What is an Ensemble Method?",
            "answer": "Ensemble learning combines predictions from multiple individual models (e.g., Random Forests, Boosting) to achieve higher accuracy and robustness."
        },
        {
            "question": "What is Feature Scaling and why is it needed?",
            "answer": "Feature scaling normalizes numerical features to a uniform scale, preventing distance-based and gradient algorithms from being biased toward larger values."
        },
        {
            "question": "What is Precision vs Recall?",
            "answer": "Precision measures the proportion of true positives among all predicted positives, whereas recall measures the proportion of true positives captured among all actual positives."
        },
        {
            "question": "What is a Confusion Matrix?",
            "answer": "A confusion matrix is a tabular layout summarizing classification performance across True Positives, True Negatives, False Positives, and False Negatives."
        }
    ],
    "python": [
        {
            "question": "What are Python's core data types?",
            "answer": "Core built-in types include integers, floats, strings, booleans, lists, tuples, sets, and dictionaries."
        },
        {
            "question": "What is the difference between a List and a Tuple?",
            "answer": "Lists are mutable and defined using square brackets `[]`, whereas tuples are immutable and defined using parentheses `()`."
        },
        {
            "question": "What does the PEP 8 standard specify?",
            "answer": "PEP 8 is Python's official style guide that outlines readability conventions, naming rules, and indentation standards for clean Python code."
        },
        {
            "question": "What are Python Decorators?",
            "answer": "Decorators are callable functions that modify or extend the behavior of another function without altering its source code."
        },
        {
            "question": "What is the Global Interpreter Lock (GIL)?",
            "answer": "The GIL is a mutex in CPython that allows only one thread to execute Python bytecode at a time, limiting CPU-bound multithreading."
        },
        {
            "question": "What is a Python Generator and what does `yield` do?",
            "answer": "A generator produces a sequence of values lazily on-the-fly using `yield`, preserving function state between iterations with minimal memory."
        },
        {
            "question": "What is the difference between `is` and `==` in Python?",
            "answer": "`==` checks for equality of values, whereas `is` checks whether two variables reference the exact same object in memory."
        },
        {
            "question": "How does exception handling work in Python?",
            "answer": "Exceptions are captured using `try` blocks, handled in `except` blocks, cleaned up in `finally` blocks, and conditionally executed in `else` blocks."
        },
        {
            "question": "What is List Comprehension?",
            "answer": "List comprehension provides a concise, readable syntax for creating new lists by transforming or filtering elements from an existing iterable."
        },
        {
            "question": "What are `*args` and `**kwargs` in function definitions?",
            "answer": "`*args` allows passing a variable number of positional arguments as a tuple, while `**kwargs` passes keyword arguments as a dictionary."
        },
        {
            "question": "What are Lambda functions in Python?",
            "answer": "Lambda functions are small, anonymous single-line functions created using the `lambda` keyword for short inline operations."
        },
        {
            "question": "What is Duck Typing in Python?",
            "answer": "Duck typing is a dynamic typing concept where an object's suitability is determined by the presence of certain methods and properties, rather than its explicit class."
        },
        {
            "question": "What is the `__init__` method in Python classes?",
            "answer": "`__init__` is the constructor method in Python automatically invoked to initialize an object's attributes when an instance of a class is created."
        },
        {
            "question": "What is the difference between shallow copy and deep copy?",
            "answer": "A shallow copy creates a new object referencing original nested items, while a deep copy recursively duplicates all nested objects independently."
        },
        {
            "question": "How does memory management work in Python?",
            "answer": "Python manages memory through private heap allocation, reference counting, and a cyclical garbage collector to reclaim unreachable objects."
        }
    ],
    "dbms": [
        {
            "question": "What is a Database Management System (DBMS)?",
            "answer": "A DBMS is system software that enables users and applications to create, query, update, manage, and administer structured data efficiently."
        },
        {
            "question": "What are the ACID properties in database transactions?",
            "answer": "ACID stands for Atomicity (all-or-nothing), Consistency (preserves rules), Isolation (independent transactions), and Durability (permanent persistence)."
        },
        {
            "question": "What is Database Normalization?",
            "answer": "Normalization is the systematic process of organizing database tables to reduce data redundancy and eliminate update, insertion, and deletion anomalies."
        },
        {
            "question": "What is the difference between Primary Key and Foreign Key?",
            "answer": "A Primary Key uniquely identifies a record in a table, whereas a Foreign Key references the Primary Key of another table to maintain referential integrity."
        },
        {
            "question": "What is the difference between SQL and NoSQL databases?",
            "answer": "SQL databases are relational, schema-enforced, and vertically scalable, while NoSQL databases are non-relational, flexible-schema, and horizontally scalable."
        },
        {
            "question": "What is an Index in DBMS and how does it improve performance?",
            "answer": "An index is a data structure (such as a B-Tree) that speeds up data retrieval operations on a table at the expense of additional writes and storage."
        },
        {
            "question": "What is a Deadlock in database concurrency?",
            "answer": "A deadlock is a situation where two or more transactions are permanently blocked because each holds a lock that another transaction needs."
        },
        {
            "question": "What is the difference between DDL and DML in SQL?",
            "answer": "DDL (Data Definition Language) defines database schemas (CREATE, ALTER, DROP), while DML (Data Manipulation Language) handles data records (INSERT, UPDATE, DELETE)."
        },
        {
            "question": "What is a View in SQL?",
            "answer": "A view is a virtual table derived from the result of a stored SQL query, providing security and abstraction without storing physical data separately."
        },
        {
            "question": "What is Two-Phase Locking (2PL)?",
            "answer": "2PL is a concurrency control protocol with a growing phase (locks acquired) and shrinking phase (locks released) ensuring serializability of transactions."
        },
        {
            "question": "What is the difference between DELETE and TRUNCATE?",
            "answer": "DELETE is a logged DML operation that removes rows conditionally, while TRUNCATE is a fast DDL command that deallocates all table data pages without row logging."
        },
        {
            "question": "What are Database Joins (Inner, Left, Right, Full)?",
            "answer": "Joins combine rows from multiple tables: Inner returns matching rows, Left/Right retains all rows from one side, and Full retains all rows from both tables."
        },
        {
            "question": "What is Third Normal Form (3NF)?",
            "answer": "A table is in 3NF if it is in 2NF and has no transitive dependencies, meaning non-key attributes depend only on the primary key."
        },
        {
            "question": "What is Write-Ahead Logging (WAL)?",
            "answer": "WAL is a fault-tolerance technique where transaction changes are recorded in non-volatile logs before being committed to actual data files."
        },
        {
            "question": "What is the CAP Theorem?",
            "answer": "The CAP theorem states that a distributed data store can simultaneously guarantee at most two of three properties: Consistency, Availability, and Partition Tolerance."
        }
    ]
}


def get_api_key(override_key: Optional[str] = None) -> Optional[str]:
    """
    Retrieve Gemini API key with priority:
    1. Runtime user-provided key (from UI sidebar)
    2. GEMINI_API_KEY environment variable
    3. GOOGLE_API_KEY environment variable
    """
    if override_key and override_key.strip():
        return override_key.strip()
    return os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")


def is_live_api_ready(override_key: Optional[str] = None) -> bool:
    """Check if a valid API key string is present."""
    key = get_api_key(override_key)
    return bool(key and len(key.strip()) > 8)


def _generate_mock_flashcards(topic: str, count: int) -> List[Dict[str, str]]:
    """
    Produce high-quality mock flashcards:
    1. Checks if topic matches a curated college syllabus topic.
    2. If custom topic, generates academic template flashcards.
    All cards are returned as clean dictionaries with 'question' and 'answer'.
    """
    topic_clean = topic.strip().lower()

    # Search for curated match
    matched_cards = None
    for key, cards in CURATED_TOPICS.items():
        if key in topic_clean or topic_clean in key:
            matched_cards = cards
            break

    if matched_cards:
        # Return requested count from curated list, looping if needed
        result = []
        for i in range(count):
            card = matched_cards[i % len(matched_cards)]
            result.append({
                "question": card["question"],
                "answer": card["answer"]
            })
        return result

    # Smart academic template generation for arbitrary custom topics in demo mode
    templates = [
        ("What is the fundamental definition of {topic}?",
         "{topic} is a foundational domain focused on study, analysis, and implementation of core principles in modern computing and technology."),
        ("What is the primary objective or real-world use case of {topic}?",
         "The primary objective of {topic} is to solve complex engineering challenges, optimize workflows, and build scalable practical systems."),
        ("What are the key architectural components or layers in {topic}?",
         "Key components include the input/interface layer, processing logic, persistent state management, and communication protocols."),
        ("What is a major advantage of applying {topic} in practice?",
         "It increases efficiency, promotes systematic problem solving, and enables automated and modular solutions."),
        ("What is a common trade-off or challenge encountered in {topic}?",
         "Common challenges include balancing computational complexity with resource consumption, maintainability, and scalability."),
        ("What standard methodology or best practice is followed in {topic}?",
         "Engineers follow iterative testing, modular abstraction, formal validation, and benchmark metrics to ensure correctness."),
        ("How does {topic} integrate with modern distributed systems?",
         "It interfaces via standardized APIs, decoupled microservices, and asynchronous event streams for high availability."),
        ("What performance metric is most critical when evaluating {topic}?",
         "Throughput, latency, accuracy, and fault tolerance serve as the primary benchmarks for assessing real-world performance."),
        ("How has Generative AI influenced development in {topic}?",
         "Gen AI accelerates prototyping, automates routine analysis, and provides intelligent decision support for practitioners."),
        ("What prerequisite subject is most crucial before mastering {topic}?",
         "A solid foundation in discrete mathematics, data structures, and computer organization provides the necessary grounding."),
        ("What security considerations must be addressed when deploying {topic}?",
         "Access controls, data encryption, input sanitization, and compliance auditing are mandatory to mitigate threats."),
        ("How do engineers debug and troubleshoot issues in {topic}?",
         "By inspecting structured logs, running deterministic regression tests, and analyzing execution profiling telemetry."),
        ("What is the difference between theoretical models and practical implementations of {topic}?",
         "Theoretical models emphasize mathematical proofs and bounds, whereas practical implementations manage hardware constraints and latency."),
        ("What future trends or innovations are emerging within {topic}?",
         "Edge computing integration, autonomous optimization, and federated systems represent leading research frontiers."),
        ("Why is continuous revision and conceptual mastery essential in {topic}?",
         "Mastery of foundational concepts enables rapid problem decomposition and adaptation to evolving industrial standards.")
    ]

    title_topic = topic.strip().title()
    result = []
    for i in range(min(count, len(templates))):
        q_tpl, a_tpl = templates[i]
        result.append({
            "question": q_tpl.format(topic=title_topic),
            "answer": a_tpl.format(topic=title_topic)
        })
    return result


def _clean_json_text(raw_text: str) -> str:
    """Extract and sanitize JSON from model output that might include markdown fences."""
    text = raw_text.strip()
    # Match markdown code block ```json ... ``` or ``` ... ```
    match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", text)
    if match:
        return match.group(1).strip()
    return text


def generate_flashcards(
    topic: str,
    count: int = 5,
    api_key_override: Optional[str] = None,
    force_mock: bool = False
) -> Tuple[List[Dict[str, str]], str, Optional[str]]:
    """
    Main Flashcard Generation Function.

    Parameters:
    - topic: The study subject entered by user.
    - count: Number of cards (5, 10, or 15).
    - api_key_override: Optional key supplied by user in session.
    - force_mock: If True, bypasses API call and uses mock generator.

    Returns:
    - cards: List of validated dicts [{"question": "...", "answer": "..."}]
    - mode: "live" or "demo"
    - error_note: Any warning or fallback explanation, if applicable.
    """
    # 1. Input validation
    clean_topic = topic.strip()
    if not clean_topic:
        raise ValueError("Please provide a valid study topic.")

    if count not in [5, 10, 15]:
        count = 5

    api_key = get_api_key(api_key_override)

    # 2. Check if Mock Mode is forced or if API key is missing
    if force_mock or not api_key:
        cards = _generate_mock_flashcards(clean_topic, count)
        note = "API key not detected. Generated using offline Demo Mode." if not api_key else "Offline Demo Mode selected."
        return cards, "demo", note

    # 3. Call Live Generative AI API (Google Gemini 3.8 Flash via official google-genai SDK)
    try:
        from google import genai
        from google.genai import types

        client = genai.Client(api_key=api_key)

        prompt = f"""You are an expert college professor and academic tutor.
Generate exactly {count} high-yield, college-level revision flashcards for the topic: "{clean_topic}".

Strict Guidelines:
1. Each flashcard MUST have a clear conceptual "question" and a concise "answer".
2. The question must focus on definitions, key mechanisms, algorithms, comparisons, or core principles.
3. The answer MUST be concise (1-2 sentences, maximum 35 words), precise, and easy to memorize for exams.
4. Use professional yet simple English. Do not add conversational fluff or introductory notes.
5. Return ONLY a valid JSON array of objects with keys "question" and "answer".
"""

        # Use structured output schema to enforce clean JSON
        config = types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=list[Flashcard],
            temperature=0.3,
        )

        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=prompt,
            config=config,
        )

        raw_output = response.text or ""
        cleaned_json = _clean_json_text(raw_output)
        parsed_data = json.loads(cleaned_json)

        # Validate structured JSON using Pydantic
        validated_cards: List[Dict[str, str]] = []
        if isinstance(parsed_data, list):
            for item in parsed_data:
                card = Flashcard.model_validate(item)
                validated_cards.append({
                    "question": card.question.strip(),
                    "answer": card.answer.strip()
                })
        elif isinstance(parsed_data, dict) and "cards" in parsed_data:
            for item in parsed_data["cards"]:
                card = Flashcard.model_validate(item)
                validated_cards.append({
                    "question": card.question.strip(),
                    "answer": card.answer.strip()
                })
        else:
            raise ValueError("Unexpected JSON format from AI response.")

        if not validated_cards:
            raise ValueError("AI generated empty flashcard set.")

        # Ensure exact count
        final_cards = validated_cards[:count]
        return final_cards, "live", None

    except Exception as e:
        # Graceful fallback: If live API fails (network, quota, invalid key), fallback to Demo mode
        error_msg = str(e)
        cards = _generate_mock_flashcards(clean_topic, count)
        warning_note = f"Live AI generation encountered an issue ({error_msg[:120]}). Gracefully transitioned to Demo Mode."
        return cards, "demo", warning_note
