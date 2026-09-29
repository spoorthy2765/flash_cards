"""
components/navbar.py - Top Navigation Header for Smart Flashcards
Provides seamless navigation between Home, Study Workspace, How It Works, and About.
"""

import streamlit as st
from services.ai_service import is_ai_connected, get_active_provider_and_key


def render_navbar():
    """Render top navigation bar with active route highlighting and live AI indicator."""
    if "active_tab" not in st.session_state:
        st.session_state.active_tab = "Home"

    is_connected = is_ai_connected()
    demo_active = st.session_state.get("force_demo", False) or not is_connected

    # Top Brand Bar
    st.markdown("""
<style>
    .nav-bar-container {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0.8rem 1.5rem;
        background: rgba(255, 255, 255, 0.85);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(226, 232, 240, 0.8);
        border-radius: 18px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 20px -2px rgba(0, 0, 0, 0.04);
    }
    .brand-logo {
        font-family: 'Outfit', sans-serif;
        font-size: 1.35rem;
        font-weight: 900;
        letter-spacing: -0.02em;
        background: linear-gradient(135deg, #1e1b4b 0%, #4f46e5 50%, #06b6d4 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        display: flex;
        align-items: center;
        gap: 8px;
    }
</style>
""", unsafe_allow_html=True)

    col1, col2 = st.columns([1.2, 2])
    with col1:
        st.markdown("""
        <div style="padding-top: 6px;">
            <span class="brand-logo">⚡ SMART FLASHCARDS</span>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        # Navigation tabs as styled horizontal buttons
        nav_cols = st.columns(4)
        tabs = ["Home", "Study", "How It Works", "About"]
        for idx, tab_name in enumerate(tabs):
            with nav_cols[idx]:
                is_selected = (st.session_state.active_tab == tab_name)
                btn_type = "primary" if is_selected else "secondary"
                if st.button(tab_name, key=f"nav_{tab_name}", type=btn_type, use_container_width=True):
                    st.session_state.active_tab = tab_name
                    st.rerun()

    st.markdown("<hr style='margin: 0.5rem 0 1.5rem 0; border: none; border-bottom: 1px solid #e2e8f0;'>", unsafe_allow_html=True)
