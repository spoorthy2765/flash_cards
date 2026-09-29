# ⚡ Smart Flashcards – AI-Powered Study & Revision Platform

> **Modern 3D EdTech Product Prototype**  
> **Tagline:** Learn Smarter. Remember Faster.  
> **Technology:** Python, Streamlit, Generative AI (Google Gemini 3.8 Flash & OpenAI), CSS3 3D Hardware Transforms, Pydantic, Structured JSON.

---

## 🌟 What's New in this Upgrade?

The application has been completely redesigned from a basic page into a **polished, modern 3D educational platform**:

1. **Genuine 3D Interactive Flashcards:** Built with CSS 3D transforms (`perspective`, `rotateY`, `backface-visibility`, `preserve-3d`). Tap or click directly on the card to flip between Question and Answer smoothly with realistic depth and lighting.
2. **Dual Generative AI Engines:** Supports both **Google Gemini 3.8 Flash** (`google-genai` SDK) and **OpenAI** (`gpt-4o-mini`), with strict Pydantic JSON schema enforcement.
3. **Dedicated Offline Demo Mode:** A high-visibility **"Demo Mode"** button using rich, curated datasets (`data/demo_cards.json`) for *Machine Learning*, *Python*, *Artificial Intelligence*, and *DBMS*. Clearly labeled as "Demo Mode" so you can demonstrate the platform confidently without needing an active API key or internet connection.
4. **Active Recall Mastery Controls:**
   - **`✓ I Know This`**: Marks concepts as mastered and tracks accuracy.
   - **`✕ Need Revision`**: Flags challenging questions.
   - **`Review Difficult Cards`**: Automatically creates a targeted revision sub-deck containing only the cards you missed!
5. **Modern Startup Landing Page:**
   - Sleek glassmorphic navigation (`Home`, `Study`, `How It Works`, `About`).
   - Hero section with **3D floating flashcard illustration** and floating tech badges (`AI ✨`, `Python 🐍`, `ML 🧠`, `Study 📚`).
   - 3-step *How It Works* interactive workflow.
   - 6 modern feature cards with micro-animations.
   - Live study analytics dashboard (Cards Studied, Mastered, Need Revision, Progress %).

---

## 📁 Upgraded Project Directory Structure

```text
smart-flashcards/
│
├── app.py                      # Main application entry point & page routing (Home, Study, How It Works, About)
├── requirements.txt            # Project dependencies (streamlit, google-genai, openai, pydantic, python-dotenv)
├── .env.example                # API key template (OPENAI_API_KEY and GEMINI_API_KEY)
├── .streamlit/                 # Hosting & theme configuration
│   ├── config.toml             # Theme tokens + headless server mode for containers
│   └── secrets.toml.example    # Cloud secrets template (copy to secrets.toml)
├── .gitignore                  # Keeps API keys, venv/ and caches out of the repo
├── DEPLOYMENT.md               # ⭐ How to PUBLISH online (+ why Netlify cannot run this)
├── netlify.toml                # Tells Netlify to publish the static landing page below
├── index.html                  # Safety-net redirect -> ./netlify/index.html
├── netlify/                    # 📄 Static landing page deployed to Netlify
│   ├── index.html              # Hero, features, workflow + "Launch the App" button
│   ├── netlify.toml            # Publish config (no more 404 pages)
│   ├── _redirects              # Catch-all -> index.html
│   └── README.md               # 2-minute Netlify fix instructions
├── README.md                   # Comprehensive documentation & presentation guide
│
├── components/                 # Reusable frontend UI components
│   ├── __init__.py
│   ├── navbar.py               # Glassmorphic top navigation header
│   ├── flashcard.py            # Hardware-accelerated 3D flip card & study controls
│   └── ui.py                   # Master 3D CSS styling, hero section, features, & stats
│
├── services/                   # Business logic & AI orchestration
│   ├── __init__.py
│   └── ai_service.py           # Gemini & OpenAI client, Pydantic validation & demo fallback
│
├── data/                       # Local offline datasets
│   └── demo_cards.json         # Curated college exam questions for ML, Python, AI, DBMS, Networks
│
└── documentation/              # Academic viva & evaluation resources
    ├── architecture.md         # Architecture diagrams & component breakdown
    ├── faculty_demo_script.md  # Viva script & anticipated professor questions
    └── sample_test_topics.md   # Curated test topics with expected concepts
```

---

## 🚀 Quick Start & Installation

### 1. Prerequisites
- Python 3.10 or higher installed.

### 2. Virtual Environment Setup
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

---

## 🔑 API Configuration & Dual-Engine Setup

### Option 1: Using `.env` File (Recommended)
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```
Open `.env` and add either (or both) API keys:
```env
# OpenAI (gpt-4o-mini)
OPENAI_API_KEY=sk-...

# OR Google Gemini (gemini-3.8-flash)
GEMINI_API_KEY=AIzaSy...
```

### Option 2: Runtime Entry via Sidebar
Launch the application and paste your API key directly into the **"API Key (Gemini or OpenAI)"** field in the left sidebar. The key remains securely stored in your ephemeral session state.

### Option 3: Offline Demo Mode (Zero Configuration)
If no API key is detected, or if you click **"🧪 Quick Demo Mode"**, the application instantly uses the high-yield curated datasets in `data/demo_cards.json`.

---

## 🏃 Run the Application

```bash
streamlit run app.py
```

The application will launch in your default web browser at:
👉 **`http://localhost:8501`**

---

## 🌍 Publish / Deploy (make it live on the internet)

> **Heads-up — this is why a Netlify upload shows a blank page:** Netlify (like GitHub
> Pages or a static Vercel deploy) only serves pre-built HTML/CSS/JS files and has **no
> Python runtime**, so it cannot execute `app.py`. Streamlit needs a long-running Python
> server plus a WebSocket connection, which static hosts do not provide.

Use a Python-capable host instead. Full walkthrough + troubleshooting:
👉 **[DEPLOYMENT.md](DEPLOYMENT.md)**

**Fastest path (free, ~5 minutes):** push this folder to GitHub →
<https://share.streamlit.io> → **Create app** → *"Yup, I have an app"* → repository
`<you>/smart-flashcards`, main file path `app.py` → **Deploy**.

Deployment-ready files already included:

| File | Purpose |
|---|---|
| `.streamlit/config.toml` | App theme + `headless = true` so it boots inside containers |
| `.streamlit/secrets.toml.example` | Template for API keys on the host's Secrets UI |
| `.gitignore` | Ensures `.env` / `secrets.toml` / `venv/` are never committed |
| `requirements.txt` | Installed automatically by every host listed in `DEPLOYMENT.md` |

---

## 🕹️ Step-by-Step Demonstration Guide

1. **Landing Page:**
   - App opens on a modern SaaS-style hero with a floating 3D card illustration and floating badges (`AI ✨`, `Python 🐍`, `ML 🧠`, `Study 📚`).
   - Click **"✨ Create Flashcards"** or select **"Study"** in the top navigation.
2. **Study Workspace:**
   - Type in a topic like `Machine Learning` or click one of the quick chips (`Python`, `DBMS`, `Artificial Intelligence`).
   - Choose card count (`5`, `10`, `15`) and difficulty (`Easy`, `Medium`, `Hard`).
   - Click **"✨ Generate Flashcards"** (or **"🧪 Quick Demo Mode"**).
   - Watch the animated AI particle shimmer while cards are generated.
3. **Interactive 3D Study Session:**
   - Click directly on the card or click **"✨ Reveal Answer (3D Flip)"** to see the 3D flip animation.
   - Click **`✓ I Know This`** to increment your mastered score.
   - Click **`✕ Need Revision`** on difficult cards.
   - Use **`← Previous`** and **`Next →`** to navigate.
   - Check the real-time glassmorphism stats dashboard below the card.
4. **Completion & Targeted Revision:**
   - At the end of the deck, balloons celebrate your session with complete metrics.
   - Click **`🎯 Review Difficult Cards`** to immediately spin up a targeted revision deck with only the questions you flagged as needing revision!

---

## 🎓 Faculty Viva & Defense Pitch

> *"Respected professors, **Smart Flashcards** is a modern EdTech product prototype that bridges Generative AI with the cognitive psychology of **Active Recall** and **Spaced Repetition**. 
>
> When a student submits a syllabus subject, our backend leverages modern Large Language Models (Gemini 3.8 Flash or OpenAI gpt-4o-mini) with strict Pydantic JSON validation to synthesize concise, college-level question-and-answer flashcards. 
>
> On the frontend, we implemented hardware-accelerated CSS 3D perspective transforms to create an interactive 3D flip card. Students can self-assess their recall (`I Know This` vs `Need Revision`), view real-time mastery analytics, and generate targeted revision sub-decks for difficult concepts. 
>
> To guarantee flawless demonstration during exams, the platform includes a decoupled, curated offline Demo Mode that never crashes even without internet or API keys."*
