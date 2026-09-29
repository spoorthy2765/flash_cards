"""
components/ui.py - Design system & UI sections for Smart Flashcards
Implements a modern 3D educational startup aesthetic with glassmorphism,
soft ambient lighting, 3D perspective transforms, and smooth micro-animations.
"""

import streamlit as st


def render_html(content: str):
    """Safely render raw HTML/CSS without Markdown parser interference."""
    if hasattr(st, "html"):
        st.html(content)
    else:
        st.markdown(content, unsafe_allow_html=True)


def inject_custom_styles():
    """Inject master CSS styles for a premium 3D startup look."""
    css_content = """<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Outfit:wght@400;600;700;800;900&display=swap');

:root {
    --primary: #4f46e5;
    --primary-light: #818cf8;
    --primary-glow: rgba(99, 102, 241, 0.25);
    --accent: #06b6d4;
    --success: #10b981;
    --warning: #f59e0b;
    --danger: #ef4444;
    --surface: rgba(255, 255, 255, 0.88);
    --surface-glass: rgba(255, 255, 255, 0.65);
    --border-glass: rgba(226, 232, 240, 0.85);
    --text-main: #0f172a;
    --text-muted: #64748b;
}

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    color: var(--text-main);
}

.stApp {
    background: radial-gradient(circle at 15% 15%, rgba(99, 102, 241, 0.08) 0%, transparent 40%),
                radial-gradient(circle at 85% 25%, rgba(6, 182, 212, 0.08) 0%, transparent 40%),
                radial-gradient(circle at 50% 85%, rgba(139, 92, 246, 0.06) 0%, transparent 50%),
                #f8fafc;
    min-height: 100vh;
}

header[data-testid="stHeader"] {
    background: transparent !important;
}
footer {
    visibility: hidden !important;
}

.block-container {
    max-width: 1020px !important;
    padding-top: 1.5rem !important;
    padding-bottom: 4rem !important;
}

/* Styled Streamlit Vertical Container */
[data-testid="stVerticalBlockBorderWrapper"] {
    border-radius: 22px !important;
    border: 1px solid var(--border-glass) !important;
    background: var(--surface) !important;
    box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.05) !important;
    backdrop-filter: blur(12px) !important;
}

.hero-container {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 2rem;
    padding: 2.5rem 1rem 3.5rem 1rem;
    flex-wrap: wrap;
}
.hero-content {
    flex: 1 1 460px;
}
.hero-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 6px 16px;
    background: linear-gradient(135deg, rgba(99, 102, 241, 0.1) 0%, rgba(6, 182, 212, 0.1) 100%);
    border: 1px solid rgba(99, 102, 241, 0.25);
    border-radius: 9999px;
    color: #4f46e5;
    font-size: 0.84rem;
    font-weight: 700;
    letter-spacing: 0.04em;
    margin-bottom: 1.2rem;
    box-shadow: 0 2px 10px rgba(99, 102, 241, 0.1);
}
.hero-title {
    font-family: 'Outfit', sans-serif;
    font-size: 3.3rem;
    font-weight: 900;
    line-height: 1.12;
    letter-spacing: -0.03em;
    margin-bottom: 1.2rem;
    background: linear-gradient(135deg, #0f172a 30%, #4338ca 70%, #06b6d4 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.hero-subtitle {
    font-size: 1.15rem;
    color: #475569;
    line-height: 1.6;
    margin-bottom: 2rem;
    max-width: 520px;
}

.hero-visual {
    flex: 1 1 360px;
    display: flex;
    justify-content: center;
    align-items: center;
    position: relative;
    perspective: 1200px;
    min-height: 360px;
}
.floating-card-3d {
    width: 310px;
    height: 210px;
    background: linear-gradient(135deg, #ffffff 0%, #f1f5f9 100%);
    border: 2px solid rgba(255, 255, 255, 0.9);
    border-radius: 24px;
    box-shadow: 0 30px 60px -12px rgba(79, 70, 229, 0.25), 0 18px 36px -18px rgba(0, 0, 0, 0.15);
    padding: 1.6rem;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    transform: rotateY(-14deg) rotateX(10deg);
    animation: floatCard 5s ease-in-out infinite;
    position: relative;
    z-index: 2;
}
@keyframes floatCard {
    0%, 100% { transform: rotateY(-14deg) rotateX(10deg) translateY(0px); }
    50% { transform: rotateY(-10deg) rotateX(6deg) translateY(-14px); }
}

.float-badge {
    position: absolute;
    padding: 7px 15px;
    border-radius: 9999px;
    font-weight: 700;
    font-size: 0.85rem;
    box-shadow: 0 10px 22px -4px rgba(0, 0, 0, 0.12);
    z-index: 3;
    backdrop-filter: blur(12px);
    animation: floatOrb 6s ease-in-out infinite;
}
.badge-ai {
    top: 15px;
    left: 15px;
    background: rgba(255, 255, 255, 0.92);
    border: 1px solid rgba(99, 102, 241, 0.3);
    color: #4f46e5;
    animation-delay: 0s;
}
.badge-py {
    bottom: 30px;
    left: 5px;
    background: rgba(255, 255, 255, 0.92);
    border: 1px solid rgba(16, 185, 129, 0.3);
    color: #059669;
    animation-delay: 1.5s;
}
.badge-ml {
    top: 30px;
    right: 10px;
    background: rgba(255, 255, 255, 0.92);
    border: 1px solid rgba(6, 182, 212, 0.3);
    color: #0891b2;
    animation-delay: 3s;
}
.badge-study {
    bottom: 20px;
    right: 20px;
    background: rgba(255, 255, 255, 0.92);
    border: 1px solid rgba(245, 158, 11, 0.3);
    color: #d97706;
    animation-delay: 4.5s;
}
@keyframes floatOrb {
    0%, 100% { transform: translateY(0px) scale(1); }
    50% { transform: translateY(-8px) scale(1.04); }
}

.section-title {
    font-family: 'Outfit', sans-serif;
    font-size: 2.1rem;
    font-weight: 800;
    text-align: center;
    margin-bottom: 0.5rem;
    color: #0f172a;
    letter-spacing: -0.02em;
}
.section-subtitle {
    text-align: center;
    color: #64748b;
    font-size: 1.05rem;
    margin-bottom: 2.2rem;
}

.stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(130px, 1fr));
    gap: 1rem;
    margin: 1.5rem 0;
}
.stat-box {
    background: rgba(255, 255, 255, 0.85);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(226, 232, 240, 0.85);
    border-radius: 16px;
    padding: 1.1rem;
    text-align: center;
    transition: transform 0.2s ease;
}
.stat-box:hover {
    transform: translateY(-2px);
}
.stat-val {
    font-family: 'Outfit', sans-serif;
    font-size: 1.8rem;
    font-weight: 800;
    color: #4f46e5;
}
.stat-lbl {
    font-size: 0.78rem;
    font-weight: 700;
    color: #64748b;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

.features-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 1.3rem;
    margin: 2rem 0;
}
.feature-card {
    padding: 1.8rem;
    border-radius: 20px;
    background: #ffffff;
    border: 1px solid rgba(226, 232, 240, 0.85);
    box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.04);
    transition: all 0.3s ease;
}
.feature-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 16px 30px -8px rgba(79, 70, 229, 0.12);
    border-color: rgba(99, 102, 241, 0.4);
}
.feature-icon {
    font-size: 2.1rem;
    margin-bottom: 0.7rem;
}
.feature-title {
    font-size: 1.18rem;
    font-weight: 700;
    color: #0f172a;
    margin-bottom: 0.4rem;
}
.feature-desc {
    font-size: 0.94rem;
    color: #64748b;
    line-height: 1.5;
}

.steps-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
    gap: 1.3rem;
    margin: 2rem 0;
}
.step-card {
    padding: 2rem 1.8rem;
    border-radius: 22px;
    background: #ffffff;
    border: 1px solid rgba(226, 232, 240, 0.85);
    box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.04);
}
.step-num {
    font-family: 'Outfit', sans-serif;
    font-size: 2.3rem;
    font-weight: 900;
    background: linear-gradient(135deg, #4f46e5 0%, #06b6d4 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.4rem;
}

.ai-loader-box {
    text-align: center;
    padding: 2.2rem;
    margin: 1.5rem 0;
    background: rgba(255, 255, 255, 0.88);
    border: 1px dashed rgba(99, 102, 241, 0.5);
    border-radius: 20px;
}
.pulse-glow {
    display: inline-block;
    font-size: 2.4rem;
    animation: pulseRing 1.6s ease-in-out infinite;
}
@keyframes pulseRing {
    0%, 100% { transform: scale(1); filter: drop-shadow(0 0 5px rgba(99, 102, 241, 0.4)); }
    50% { transform: scale(1.15); filter: drop-shadow(0 0 15px rgba(6, 182, 212, 0.7)); }
}

.summary-card {
    background: #ffffff;
    border: 1px solid rgba(226, 232, 240, 0.9);
    border-radius: 24px;
    padding: 2.5rem 2rem;
    text-align: center;
    box-shadow: 0 12px 30px -5px rgba(0, 0, 0, 0.05);
    margin: 1.5rem 0;
}
</style>"""
    render_html(css_content)


def render_hero_section():
    """Render startup landing hero with 3D illustration and floating badges."""
    hero_html = """<div class="hero-container">
<div class="hero-content">
<div class="hero-badge">✨ AI-POWERED LEARNING</div>
<h1 class="hero-title">Turn Any Topic<br>Into Smart Flashcards.</h1>
<p class="hero-subtitle">
Learn difficult concepts faster with AI-generated flashcards designed for quick revision, active recall, and effortless exam mastery.
</p>
</div>
<div class="hero-visual">
<div class="float-badge badge-ai">✨ AI Synth</div>
<div class="float-badge badge-py">🐍 Python</div>
<div class="float-badge badge-ml">🧠 ML Deep</div>
<div class="float-badge badge-study">📚 Active Recall</div>
<div class="floating-card-3d">
<div>
<span style="display:inline-block; padding:4px 12px; background:#e0e7ff; color:#3730a3; border-radius:9999px; font-size:11px; font-weight:800;">Question Preview</span>
<div style="font-weight: 700; font-size: 1.15rem; color: #0f172a; margin-top: 0.8rem; line-height: 1.4;">
What is the core difference between Supervised and Unsupervised Learning?
</div>
</div>
<div style="display: flex; justify-content: space-between; align-items: center; border-top: 1px solid #e2e8f0; padding-top: 0.8rem;">
<span style="font-size: 0.8rem; font-weight: 600; color: #64748b;">3D Interactive Card</span>
<span style="font-size: 0.8rem; font-weight: 700; color: #4f46e5;">Tap to Flip ➔</span>
</div>
</div>
</div>
</div>"""
    render_html(hero_html)


def render_how_it_works():
    """Render the 3-step 'How It Works' section."""
    steps_html = """<div style="margin-top: 3.5rem;">
<div class="section-title">How It Works</div>
<div class="section-subtitle">Effortless three-step mastery powered by Generative AI and cognitive science.</div>
<div class="steps-grid">
<div class="step-card">
<div class="step-num">01</div>
<div style="font-weight: 700; font-size: 1.18rem; color: #0f172a; margin-bottom: 0.4rem;">ENTER TOPIC</div>
<div style="color: #64748b; font-size: 0.95rem; line-height: 1.5;">
Choose any syllabus topic you want to learn—from Machine Learning to DBMS or Networks.
</div>
</div>
<div class="step-card">
<div class="step-num">02</div>
<div style="font-weight: 700; font-size: 1.18rem; color: #0f172a; margin-bottom: 0.4rem;">AI CREATES CARDS</div>
<div style="color: #64748b; font-size: 0.95rem; line-height: 1.5;">
Generative AI automatically distills high-yield questions and concise, exam-ready answers.
</div>
</div>
<div class="step-card">
<div class="step-num">03</div>
<div style="font-weight: 700; font-size: 1.18rem; color: #0f172a; margin-bottom: 0.4rem;">LEARN & REVIEW</div>
<div style="color: #64748b; font-size: 0.95rem; line-height: 1.5;">
Flip cards in real 3D, test your active recall, and track exactly which concepts need revision.
</div>
</div>
</div>
</div>"""
    render_html(steps_html)


def render_features_grid():
    """Render the 6 feature cards."""
    features_html = """<div style="margin-top: 3.5rem;">
<div class="section-title">Engineered for Academic Excellence</div>
<div class="section-subtitle">Everything you need to turn dense textbooks into high-retention study sessions.</div>
<div class="features-grid">
<div class="feature-card">
<div class="feature-icon">✨</div>
<div class="feature-title">AI Generated</div>
<div class="feature-desc">Dynamically crafts questions and answers tailored to college curricula using modern LLMs.</div>
</div>
<div class="feature-card">
<div class="feature-icon">📚</div>
<div class="feature-title">Smart Revision</div>
<div class="feature-desc">Flags challenging questions so you can target revision on concepts you haven't mastered yet.</div>
</div>
<div class="feature-card">
<div class="feature-icon">🎴</div>
<div class="feature-title">3D Flashcards</div>
<div class="feature-desc">Real CSS 3D hardware-accelerated flip animations make studying engaging and tactile.</div>
</div>
<div class="feature-card">
<div class="feature-icon">📊</div>
<div class="feature-title">Progress Tracking</div>
<div class="feature-desc">Live metrics monitor cards studied, recall accuracy, and deck completion percentages.</div>
</div>
<div class="feature-card">
<div class="feature-icon">🧠</div>
<div class="feature-title">Active Recall</div>
<div class="feature-desc">Enforces question retrieval before answer revelation, proven to double memory retention.</div>
</div>
<div class="feature-card">
<div class="feature-icon">⚡</div>
<div class="feature-title">Fast Learning</div>
<div class="feature-desc">Get exam-ready in minutes with bite-sized, 35-word concise conceptual answers.</div>
</div>
</div>
</div>"""
    render_html(features_html)


def render_about_section():
    """Render the About section detailing project purpose and tech stack."""
    about_html = """<div style="margin-top: 3.5rem; padding: 2.8rem 2rem; background: #ffffff; border-radius: 24px; border: 1px solid #e2e8f0; text-align: center;">
<div class="section-title">Built for Smarter Learning</div>
<p style="max-width: 680px; margin: 0 auto 1.8rem auto; color: #475569; font-size: 1.1rem; line-height: 1.6;">
Smart Flashcards combines Generative AI with active recall to make revision faster, simpler and more engaging.
Built as an advanced educational technology prototype designed for engineering college students.
</p>
<div style="display: flex; justify-content: center; gap: 12px; flex-wrap: wrap;">
<span style="background: #eef2ff; color: #4338ca; padding: 6px 16px; border-radius: 9999px; font-weight: 700; font-size: 0.88rem;">🐍 Python</span>
<span style="background: #ecfdf5; color: #065f46; padding: 6px 16px; border-radius: 9999px; font-weight: 700; font-size: 0.88rem;">⚡ Streamlit</span>
<span style="background: #eff6ff; color: #1e40af; padding: 6px 16px; border-radius: 9999px; font-weight: 700; font-size: 0.88rem;">🧠 Generative AI</span>
<span style="background: #fef3c7; color: #92400e; padding: 6px 16px; border-radius: 9999px; font-weight: 700; font-size: 0.88rem;">📦 Structured JSON & Pydantic</span>
</div>
</div>"""
    render_html(about_html)


def render_stats_dashboard(total: int, current_studied: int, known_count: int, revision_count: int):
    """Render the glassmorphism study statistics bar."""
    progress_pct = int((current_studied / total) * 100) if total > 0 else 0
    stats_html = f"""<div class="stats-grid">
<div class="stat-box">
<div class="stat-val">{current_studied} / {total}</div>
<div class="stat-lbl">Cards Studied</div>
</div>
<div class="stat-box">
<div class="stat-val" style="color: #10b981;">{known_count}</div>
<div class="stat-lbl">Mastered ✓</div>
</div>
<div class="stat-box">
<div class="stat-val" style="color: #f59e0b;">{revision_count}</div>
<div class="stat-lbl">Need Revision ✕</div>
</div>
<div class="stat-box">
<div class="stat-val" style="color: #06b6d4;">{progress_pct}%</div>
<div class="stat-lbl">Progress</div>
</div>
</div>"""
    render_html(stats_html)
