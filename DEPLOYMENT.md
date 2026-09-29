# 🚀 Publishing Smart Flashcards — Deployment Guide

> **Short answer:** your Netlify upload is empty because Netlify **cannot run Python or
> Streamlit at all**. Publish the app on a Python-capable host instead — **Option A below
> takes about 5 minutes and is free.**

---

## ⚠️ 1. Why nothing opens on Netlify

Netlify is a **static site host**. It only serves pre-built `HTML` / `CSS` / `JS` files
from a CDN, plus short-lived serverless functions written in **Node.js or Go**.

Smart Flashcards is a **Streamlit application**:

| What Streamlit needs | Does Netlify provide it? |
|---|---|
| A long-running Python process | ❌ No Python runtime at all |
| Server-side rendering on every interaction | ❌ No, static files only |
| A persistent WebSocket connection (`/_stcore/stream`) | ❌ Serverless functions time out in seconds |
| An entry `.py` file to execute | ❌ It only looks for `index.html` |

This repo contains no `index.html`, so Netlify has literally nothing to render. The
upload "succeeds" and then shows a blank page / 404. **No `netlify.toml`, redirect or
build command can fix this** — it is a platform limitation, not a bug in your code.

👉 So: keep Netlify only if you want a static landing page (see **Option D** at the end of
this guide), and publish the actual app using one of the options below.

---

## ✅ Option A (recommended — free, ~5 min): Streamlit Community Cloud

Made by the Streamlit team for exactly this kind of app. Free forever for public apps,
gives you a `https://<name>.streamlit.app` link, and needs no server management.

### Step A1 — Put the project on GitHub

The project folder is already an initialised git repository with a first commit, so you
only need to create an empty repo and push.

1. Go to <https://github.com/new>
2. **Repository name:** `smart-flashcards` · **Visibility:** `Public` (easiest for
   sharing/submission) → click **Create repository** (do **not** add a README).
3. In a terminal, from the project folder:

```powershell
cd C:\Users\admin\Desktop\smart-flashcards
git remote add origin https://github.com/<YOUR-USERNAME>/smart-flashcards.git
git branch -M main
git push -u origin main
```

> If git asks who you are: `git config --global user.name "Your Name"` and
> `git config --global user.email "you@example.com"` first.

### Step A2 — Deploy it

1. Go to <https://share.streamlit.io> and sign in **with GitHub** (authorise it once).
2. Click **Create app** (top-right) → when asked *"Do you already have an app?"* choose
   **"Yup, I have an app"**.
3. Fill the form:

   | Field | Value |
   |---|---|
   | Repository | `<YOUR-USERNAME>/smart-flashcards` |
   | Branch | `main` |
   | **Main file path** | `app.py` |

4. *(Optional but recommended)* **App URL** → type a memorable subdomain, e.g.
   `smart-flashcards-ai` → your app will live at `https://smart-flashcards-ai.streamlit.app`.

5. Click **Advanced settings**:
   - **Python version** → choose **3.12** (Community Cloud's default and the safest
     choice; the code is version-agnostic and also runs on your local Python 3.14).
   - **Secrets** → leave empty for now (Demo Mode works without any key), or paste your
     key to enable live AI — see Step A4.

6. Click **Deploy** and watch the build log. First deploy takes roughly **2–5 minutes**.

### Step A3 — What already works with ZERO configuration

Everything, as soon as the build finishes:

- The 3D flip flashcards, all four routes (Home / Study / How It Works / About),
  the stats dashboard, *I Know This* / *Need Revision* tracking and the
  *🎯 Review Difficult Cards* sub-deck generator.
- Because no API key is configured, the app automatically runs in **🧪 Demo Mode**
  using the curated decks in `data/demo_cards.json`
  (`Machine Learning`, `Python`, `DBMS`, `Artificial Intelligence`, `Computer Networks`).

You can also let a visitor paste their own key into the **sidebar → API Key** field at
any time — that path needs no secrets configuration at all.

### Step A4 — (Optional) Enable live AI generation

**Important:** Community Cloud hands secrets to your app through `st.secrets`, *not*
through environment variables. `services/ai_service.py` now reads **both** sources
(`_get_secret()`), so this works:

1. Get a **free** Gemini API key: <https://aistudio.google.com/app/apikey>
2. In <https://share.streamlit.io> open your app → **⋮ / Settings → Secrets** (you can
   also paste this into the *Secrets* box of the Advanced-settings dialog at deploy time):
   ```toml
   GEMINI_API_KEY = "AIza...your_real_key_here"
   ```
   Using OpenAI instead? Paste `OPENAI_API_KEY = "sk-..."`.
3. Click **Save**. The app reboots and the sidebar status turns green
   (*🟢 Connected to Gemini API*).

> 🔒 `.streamlit/secrets.toml` and `.env` are already excluded by `.gitignore`, so your
> keys can never be pushed to GitHub by accident.

### ⚠️ Known issue you should fix before using Gemini

`services/ai_service.py` (line ~216) and the legacy `ai_generator.py` request:

```python
model="gemini-3.8-flash"
```

There is **no such model** in the Gemini API, so a live Gemini call fails with a
*model not found* error. The OpenAI path (`gpt-4o-mini`) is valid and unaffected, and
Demo Mode is unaffected. If you want live Gemini, change that one string to a real
model ID, e.g.:

```python
model="gemini-2.5-flash"
```

(Ask your assistant to apply it together with the README/`documentation/` wording if
you want the "Gemini 3.8 Flash" branding in your report replaced too.)

---

## 🅱️ Option B: Render (free web-service tier, real environment variables)

Useful if you prefer env vars over `st.secrets`, or want a non-Streamlit-Cloud host.

1. Push to GitHub exactly as in Step A1.
2. <https://render.com> → **New +** → **Web Service** → connect your repo.
3. Settings:

   | Field | Value |
   |---|---|
   | Runtime | `Python 3` |
   | Build Command | `pip install -r requirements.txt` |
   | **Start Command** | `streamlit run app.py --server.port $PORT --server.address 0.0.0.0 --server.headless true` |

4. **Environment → Add Environment Variable** → `GEMINI_API_KEY` (or `OPENAI_API_KEY`).
   Also add `PYTHON_VERSION = 3.12`.
5. **Create Web Service**. Free instances sleep after ~15 min of inactivity and take
   ~50 s to wake up on the first request.

---

## 🤗 Option C: Hugging Face Spaces (free, permanent, popular for demos)

1. <https://huggingface.co/new-space> → **SDK: Streamlit** → *Public* → Create.
2. Upload this project's files (or connect the GitHub repo in the Space settings).
3. Make sure the entry file is `app.py` (the Space README front-matter needs
   `sdk: streamlit` and `app_file: app.py`).
4. **Settings → Variables and secrets → New secret** → `GEMINI_API_KEY`.
5. The Space builds automatically and gets a permanent `*.hf.space` URL.

---

## 🌐 Option D: "I still want to use my Netlify URL"

**This is already built for you** — see the [`netlify/`](netlify/) folder. It is a
self-contained static landing page (hero, 3D card illustration, 6 feature tiles,
3-step workflow, tech badges) plus a **"🚀 Launch the App"** button.

Your Netlify site currently shows Netlify's own **"Page not found" (404)** screen, which
proves the deploy is live but contained no `index.html`. Fix it in 2 minutes:

1. <https://app.netlify.com> → select your site (`dynamic-caramel-7a41c2`).
2. Open the **Deploys** tab and scroll to the bottom.
3. Drag the **`netlify` folder** onto the *"Drag and drop your site output folder here"*
   drop zone.
4. Reload `https://dynamic-caramel-7a41c2.netlify.app` → the landing page appears.

> ⚠️ Drag the **`netlify` folder itself**, not the whole project folder. (A root-level
> `index.html` is also included as a safety net, so even publishing the project root now
> shows the landing page instead of a 404.)

Now connect the button to the real app:

5. Deploy the app first (Option A) to get a URL like
   `https://smart-flashcards-ai.streamlit.app`.
6. In `netlify/index.html`, find `const HOSTED_URL = "https://YOUR-APP-NAME.streamlit.app";`
   near the bottom and paste your real URL.
7. Re-deploy (repeat step 3).

> 💡 While previewing `netlify/index.html` on your own machine (opening the file directly
> or via `localhost`), the buttons automatically open the local app at
> `http://localhost:8501`, so nothing looks broken during development. The yellow notice
> only appears on the *public* site while `HOSTED_URL` is still the placeholder.



---

## 🧯 Troubleshooting

| Symptom | Cause / fix |
|---|---|
| Netlify site is blank or 404 | Expected — Netlify cannot run Streamlit. Use Option A/B/C. |
| Cloud build fails on Python version | Set **Python version = 3.12** in *Advanced settings*. |
| `ModuleNotFoundError` in Cloud logs | A dependency is missing from `requirements.txt`. |
| Sidebar says *"AI service not connected"* | No key found → the app stays in Demo Mode (fully functional). Add the secret from Step A4. |
| Gemini returns *model not found* | See the "Known issue" box in Step A4. |
| Live AI worked, then stopped | Rotate/verify the key; check the app's log in the Cloud workspace. |
| Code pushed but the app looks stale | Workspace → **Reboot app** (or **Clear cache**). |

---

## ✅ Pre-flight checklist (already done in this repo)

- [x] `requirements.txt` in the repository root
- [x] Entry point `app.py`
- [x] `data/demo_cards.json` committed (Demo Mode needs it)
- [x] `.gitignore` excludes `venv/`, `__pycache__/`, `.env`, `.streamlit/secrets.toml`
- [x] `.streamlit/config.toml` with the app's theme + `headless = true` for containers
- [x] `services/ai_service.py` reads keys from `st.secrets` **and** `os.getenv`
- [x] `.streamlit/secrets.toml.example` template for hosted secrets
- [ ] (You) push to GitHub → deploy on <https://share.streamlit.io>

