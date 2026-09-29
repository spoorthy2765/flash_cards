"""
app.py - Smart Flashcards: AI-Powered Study & Revision Platform
A modern, polished 3D educational platform with interactive CSS 3D transforms,
dual Generative AI support (Gemini 3.8 Flash & OpenAI), and a robust offline Demo Mode.
"""

import streamlit as st
import time

from components.ui import (
    inject_custom_styles,
    render_hero_section,
    render_how_it_works,
    render_features_grid,
    render_about_section,
    render_stats_dashboard,
    render_html
)
from components.navbar import render_navbar
from components.flashcard import render_3d_flashcard, render_card_controls
from services.ai_service import (
    generate_deck,
    is_ai_connected,
    get_active_provider_and_key
)

# ---------------------------------------------------------
# PAGE SETUP
# ---------------------------------------------------------
st.set_page_config(
    page_title="Smart Flashcards – Learn Smarter. Remember Faster.",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Inject master 3D & glassmorphism CSS
inject_custom_styles()

# ---------------------------------------------------------
# SESSION STATE INITIALIZATION
# ---------------------------------------------------------
if "active_tab" not in st.session_state:
    st.session_state.active_tab = "Home"
if "deck" not in st.session_state:
    st.session_state.deck = []
if "current_index" not in st.session_state:
    st.session_state.current_index = 0
if "is_flipped" not in st.session_state:
    st.session_state.is_flipped = False
if "completed" not in st.session_state:
    st.session_state.completed = False
if "known_cards" not in st.session_state:
    st.session_state.known_cards = set()
if "revision_cards" not in st.session_state:
    st.session_state.revision_cards = set()
if "force_demo" not in st.session_state:
    st.session_state.force_demo = False
if "runtime_api_key" not in st.session_state:
    st.session_state.runtime_api_key = ""
if "generation_metadata" not in st.session_state:
    st.session_state.generation_metadata = {}
if "topic_input" not in st.session_state:
    st.session_state.topic_input = ""

# ---------------------------------------------------------
# SIDEBAR: API & DEMO CONFIGURATION
# ---------------------------------------------------------
with st.sidebar:
    st.markdown("### ⚙️ Engine Settings")
    
    st.session_state.runtime_api_key = st.text_input(
        "API Key (Gemini or OpenAI)",
        value=st.session_state.runtime_api_key,
        type="password",
        help="Optional: Paste a GEMINI_API_KEY or OPENAI_API_KEY for live AI synthesis."
    )
    
    provider_detected, _ = get_active_provider_and_key(st.session_state.runtime_api_key)
    
    st.session_state.force_demo = st.checkbox(
        "🧪 Force Demo Mode",
        value=st.session_state.force_demo,
        help="Enable offline mode to test with curated sample datasets without calling an AI API."
    )
    
    st.markdown("---")
    st.markdown("#### ⚡ Active Status")
    if st.session_state.force_demo:
        st.warning("🧪 Demo Mode Active (Offline sample dataset)")
    elif provider_detected:
        st.success(f"🟢 Connected to {provider_detected.title()} API")
    else:
        st.info("ℹ️ AI service not connected. Demo Mode will be used.")

    st.markdown("---")
    if st.button("🔄 Reset Entire Workspace", use_container_width=True):
        st.session_state.deck = []
        st.session_state.current_index = 0
        st.session_state.is_flipped = False
        st.session_state.completed = False
        st.session_state.known_cards = set()
        st.session_state.revision_cards = set()
        st.session_state.active_tab = "Home"
        st.rerun()

# ---------------------------------------------------------
# TOP NAVBAR
# ---------------------------------------------------------
render_navbar()

# ---------------------------------------------------------
# VIEW ROUTER
# ---------------------------------------------------------

# =========================================================
# ROUTE 1: HOME / LANDING PAGE
# =========================================================
if st.session_state.active_tab == "Home":
    render_hero_section()
    
    # Hero CTA Buttons
    col_cta1, col_cta2, col_cta3 = st.columns([1.2, 1.2, 2])
    with col_cta1:
        if st.button("✨ Create Flashcards", type="primary", use_container_width=True):
            st.session_state.active_tab = "Study"
            st.rerun()
    with col_cta2:
        if st.button("🧪 Explore Demo Mode", type="secondary", use_container_width=True):
            st.session_state.force_demo = True
            st.session_state.topic_input = "Machine Learning"
            st.session_state.active_tab = "Study"
            st.rerun()

    # How It Works
    render_how_it_works()
    
    # 6 Features
    render_features_grid()
    
    # About Section
    render_about_section()


# =========================================================
# ROUTE 2: STUDY WORKSPACE (MAIN APP)
# =========================================================
elif st.session_state.active_tab == "Study":
    
    # Case A: No deck active yet -> Deck Creation Form
    if not st.session_state.deck:
        render_html("""<div style="text-align: center; margin-bottom: 1.8rem;">
<div class="section-title">Create Your Flashcards</div>
<div class="section-subtitle">Enter any topic and let AI synthesize your high-retention revision deck.</div>
</div>""")

        # Connection & Mode Status Banner
        has_ai = is_ai_connected(st.session_state.runtime_api_key)
        if st.session_state.force_demo:
            render_html("""<div style="background: #fffbeb; border: 1.5px solid #fde68a; border-radius: 14px; padding: 12px 18px; margin-bottom: 1.6rem; display: flex; align-items: center; justify-content: space-between;">
<div>
<span style="font-weight: 700; color: #92400e;">🧪 Demo Mode Active</span>
<span style="color: #b45309; font-size: 0.9rem; margin-left: 8px;">— Using curated academic datasets for presentation.</span>
</div>
<span style="background: #fef3c7; color: #92400e; padding: 3px 10px; border-radius: 9999px; font-size: 0.76rem; font-weight: 800;">OFFLINE</span>
</div>""")
        elif has_ai:
            provider_name, _ = get_active_provider_and_key(st.session_state.runtime_api_key)
            render_html(f"""<div style="background: #ecfdf5; border: 1.5px solid #a7f3d0; border-radius: 14px; padding: 12px 18px; margin-bottom: 1.6rem; display: flex; align-items: center; justify-content: space-between;">
<div>
<span style="font-weight: 700; color: #065f46;">🟢 AI Service Connected</span>
<span style="color: #047857; font-size: 0.9rem; margin-left: 8px;">— Live generation powered by {provider_name.title()}.</span>
</div>
<span style="background: #d1fae5; color: #065f46; padding: 3px 10px; border-radius: 9999px; font-size: 0.76rem; font-weight: 800;">LIVE AI</span>
</div>""")
        else:
            render_html("""<div style="background: #eff6ff; border: 1.5px solid #bfdbfe; border-radius: 14px; padding: 12px 18px; margin-bottom: 1.6rem; display: flex; align-items: center; justify-content: space-between;">
<div>
<span style="font-weight: 700; color: #1e40af;">ℹ️ AI Service Not Connected</span>
<span style="color: #1d4ed8; font-size: 0.9rem; margin-left: 8px;">— Add API key in sidebar or use Demo Mode for instant presentation.</span>
</div>
<span style="background: #dbeafe; color: #1e40af; padding: 3px 10px; border-radius: 9999px; font-size: 0.76rem; font-weight: 800;">READY</span>
</div>""")

        # Input Form Container
        with st.container(border=True):
            # Topic Input
            st.markdown("##### 🎯 Topic")
            topic_val = st.text_input(
                "Topic",
                value=st.session_state.topic_input,
                placeholder="Example: Machine Learning, Python, DBMS, Computer Networks...",
                label_visibility="collapsed"
            )

            # Quick Example Chips
            render_html("<div style='margin-top: -6px; margin-bottom: 12px;'><span style='font-size: 0.8rem; color: #64748b; font-weight: 600;'>Popular Examples: </span></div>")
            col_chip1, col_chip2, col_chip3, col_chip4, col_chip5 = st.columns(5)
            with col_chip1:
                if st.button("Machine Learning", key="chip_ml", use_container_width=True):
                    st.session_state.topic_input = "Machine Learning"
                    st.rerun()
            with col_chip2:
                if st.button("Python", key="chip_py", use_container_width=True):
                    st.session_state.topic_input = "Python"
                    st.rerun()
            with col_chip3:
                if st.button("DBMS", key="chip_dbms", use_container_width=True):
                    st.session_state.topic_input = "DBMS"
                    st.rerun()
            with col_chip4:
                if st.button("Artificial Intelligence", key="chip_ai", use_container_width=True):
                    st.session_state.topic_input = "Artificial Intelligence"
                    st.rerun()
            with col_chip5:
                if st.button("Computer Networks", key="chip_cn", use_container_width=True):
                    st.session_state.topic_input = "Computer Networks"
                    st.rerun()

            st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)

            # Settings Row: Card Count, Difficulty, Learning Level
            col_c1, col_c2, col_c3 = st.columns(3)
            with col_c1:
                st.markdown("##### 🔢 Number of Cards")
                num_cards = st.radio(
                    "Cards",
                    [5, 10, 15],
                    index=0,
                    horizontal=True,
                    label_visibility="collapsed"
                )
            with col_c2:
                st.markdown("##### ⚡ Difficulty")
                difficulty = st.selectbox(
                    "Difficulty",
                    ["Medium", "Easy", "Hard"],
                    index=0,
                    label_visibility="collapsed"
                )
            with col_c3:
                st.markdown("##### 🎓 Learning Level")
                learning_level = st.selectbox(
                    "Level",
                    ["Intermediate", "Beginner", "Advanced"],
                    index=0,
                    label_visibility="collapsed"
                )

            st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

            # Mode Action Buttons
            col_btn_gen, col_btn_demo = st.columns([2.5, 1.2])
            with col_btn_gen:
                generate_clicked = st.button("✨ Generate Flashcards", type="primary", use_container_width=True)
            with col_btn_demo:
                toggle_demo_clicked = st.button("🧪 Quick Demo Mode", use_container_width=True)

            if toggle_demo_clicked:
                st.session_state.force_demo = True
                if not topic_val.strip():
                    topic_val = "Machine Learning"
                    st.session_state.topic_input = "Machine Learning"
                generate_clicked = True

            # Execution logic
            if generate_clicked:
                clean_topic = topic_val.strip()
                if not clean_topic:
                    st.error("⚠️ Please enter a study topic before generating flashcards.")
                else:
                    # AI Particle Loading Animation
                    with st.container():
                        render_html(f"""<div class="ai-loader-box">
<div class="pulse-glow">✨</div>
<div style="font-weight: 800; font-size: 1.25rem; color: #0f172a; margin-top: 0.8rem;">
Creating your personalized flashcards...
</div>
<div style="color: #64748b; font-size: 0.95rem; margin-top: 0.3rem;">
Synthesizing {num_cards} high-yield {difficulty.lower()} cards for '{clean_topic}'
</div>
</div>""")
                        time.sleep(0.6)

                    # Dispatch to AI service
                    response = generate_deck(
                        topic=clean_topic,
                        count=num_cards,
                        difficulty=difficulty,
                        level=learning_level,
                        runtime_key=st.session_state.runtime_api_key,
                        force_demo=st.session_state.force_demo
                    )

                    if response["cards"]:
                        st.session_state.deck = response["cards"]
                        st.session_state.current_index = 0
                        st.session_state.is_flipped = False
                        st.session_state.completed = False
                        st.session_state.known_cards = set()
                        st.session_state.revision_cards = set()
                        st.session_state.generation_metadata = response
                        st.rerun()
                    else:
                        st.error(f"❌ {response.get('message', 'Unable to generate flashcards.')}")
                        if response.get("error"):
                            st.caption(f"Details: {response['error']}")

    # Case B: Deck is active and not yet completed -> 3D Study Workspace
    elif not st.session_state.completed:
        total_cards = len(st.session_state.deck)
        current_idx = st.session_state.current_index
        card = st.session_state.deck[current_idx]
        meta = st.session_state.generation_metadata

        # Header Info Bar with Exit Deck option
        col_top_a, col_top_b = st.columns([3, 1])
        with col_top_a:
            mode_badge = ('<span style="background: #ecfdf5; color: #065f46; padding: 4px 12px; border-radius: 9999px; font-size: 0.78rem; font-weight: 700;">🟢 Live AI Generation</span>'
                          if meta.get("mode") == "live" else
                          '<span style="background: #fffbeb; color: #92400e; padding: 4px 12px; border-radius: 9999px; font-size: 0.78rem; font-weight: 700;">🧪 Demo Mode (Sample Data)</span>')
            render_html(f"<div style='padding-top:6px;'>{mode_badge} &nbsp;&nbsp; <b>{card.get('topic', 'Flashcards')}</b></div>")
        
        with col_top_b:
            if st.button("✕ Exit Deck", use_container_width=True):
                st.session_state.deck = []
                st.session_state.current_index = 0
                st.session_state.is_flipped = False
                st.rerun()

        # Render 3D Flashcard
        render_3d_flashcard(
            card_data=card,
            current_idx=current_idx,
            total_cards=total_cards,
            is_flipped=st.session_state.is_flipped
        )

        # Render Controls (Flip, I Know This, Need Revision, Navigation)
        render_card_controls(
            current_idx=current_idx,
            total_cards=total_cards
        )

        # Live Statistics Dashboard
        known_count = len(st.session_state.known_cards)
        rev_count = len(st.session_state.revision_cards)
        studied_count = current_idx + 1

        render_stats_dashboard(
            total=total_cards,
            current_studied=studied_count,
            known_count=known_count,
            revision_count=rev_count
        )

    # Case C: Deck is completed -> Completion Summary Screen
    else:
        total_cards = len(st.session_state.deck)
        known_count = len(st.session_state.known_cards)
        rev_count = len(st.session_state.revision_cards)

        st.balloons()

        render_html("""<div class="summary-card">
<div style="font-size: 3.5rem; margin-bottom: 0.5rem;">🎉</div>
<h1 style="font-family: 'Outfit', sans-serif; font-size: 2.5rem; font-weight: 900; color: #0f172a; margin-bottom: 0.3rem;">
Great Work!
</h1>
<p style="color: #64748b; font-size: 1.15rem; margin-bottom: 1.5rem;">
You completed your flashcard deck. Active recall session finished!
</p>
</div>""")

        # Big Stat Metrics
        col_res1, col_res2, col_res3 = st.columns(3)
        with col_res1:
            render_html(f"""<div class="stat-box" style="padding: 1.8rem;">
<div class="stat-val">{total_cards}</div>
<div class="stat-lbl">Total Cards</div>
</div>""")
        with col_res2:
            render_html(f"""<div class="stat-box" style="padding: 1.8rem;">
<div class="stat-val" style="color: #10b981;">{known_count}</div>
<div class="stat-lbl">Known & Mastered</div>
</div>""")
        with col_res3:
            render_html(f"""<div class="stat-box" style="padding: 1.8rem;">
<div class="stat-val" style="color: #f59e0b;">{rev_count}</div>
<div class="stat-lbl">Revision Needed</div>
</div>""")

        st.markdown("<div style='height: 25px;'></div>", unsafe_allow_html=True)

        # Action Buttons
        col_act1, col_act2, col_act3 = st.columns(3)
        
        with col_act1:
            has_difficult = len(st.session_state.revision_cards) > 0
            if st.button("🎯 Review Difficult Cards", disabled=not has_difficult, type="secondary", use_container_width=True):
                difficult_indices = sorted(list(st.session_state.revision_cards))
                st.session_state.deck = [st.session_state.deck[i] for i in difficult_indices]
                st.session_state.current_index = 0
                st.session_state.is_flipped = False
                st.session_state.completed = False
                st.session_state.known_cards = set()
                st.session_state.revision_cards = set()
                st.rerun()

        with col_act2:
            if st.button("🔄 Study Deck Again", type="secondary", use_container_width=True):
                st.session_state.current_index = 0
                st.session_state.is_flipped = False
                st.session_state.completed = False
                st.session_state.known_cards = set()
                st.session_state.revision_cards = set()
                st.rerun()

        with col_act3:
            if st.button("✨ Create New Deck", type="primary", use_container_width=True):
                st.session_state.deck = []
                st.session_state.current_index = 0
                st.session_state.is_flipped = False
                st.session_state.completed = False
                st.session_state.known_cards = set()
                st.session_state.revision_cards = set()
                st.rerun()


# =========================================================
# ROUTE 3: HOW IT WORKS
# =========================================================
elif st.session_state.active_tab == "How It Works":
    render_how_it_works()
    st.markdown("<div style='height: 30px;'></div>", unsafe_allow_html=True)
    render_features_grid()
    st.markdown("<div style='height: 25px;'></div>", unsafe_allow_html=True)
    if st.button("🚀 Start Studying Now", type="primary", use_container_width=True):
        st.session_state.active_tab = "Study"
        st.rerun()


# =========================================================
# ROUTE 4: ABOUT
# =========================================================
elif st.session_state.active_tab == "About":
    render_about_section()
    render_html("""<div style="margin-top: 2rem; background: #ffffff; padding: 2rem; border-radius: 20px; border: 1px solid #e2e8f0;">
<h4 style="font-weight: 800; color: #0f172a; margin-bottom: 0.8rem;">🎓 College Faculty Demonstration Guide</h4>
<p style="color: #475569; font-size: 0.95rem; line-height: 1.6;">
<b>Project Identity:</b> Smart Flashcards is an AI-powered study and revision assistant.<br>
<b>Core Architecture:</b> Python handles business logic & data modeling (Pydantic), Streamlit orchestrates the web presentation, and Generative AI (Gemini 3.8 Flash or OpenAI) distills textbook topics into concise question-and-answer pairs.<br>
<b>Offline Resilience:</b> If an API key is not connected, the application gracefully activates Demo Mode using curated academic datasets.
</p>
</div>""")
