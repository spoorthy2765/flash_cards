"""
components/flashcard.py - 3D Interactive Flashcard Component
Renders genuine 3D perspective transforms with rotateY and backface-visibility
using native st.html to eliminate Markdown code block escaping bugs and iframe constraints.
"""

import html
import streamlit as st
import streamlit.components.v1 as components


def render_3d_flashcard(card_data: dict, current_idx: int, total_cards: int, is_flipped: bool = False):
    """
    Renders an interactive 3D Flip Flashcard with 60 FPS hardware acceleration.
    Uses st.html (or components.html fallback) with strict HTML escaping to ensure
    no Markdown parser code-block leakage.
    """
    raw_question = card_data.get("question", "")
    raw_answer = card_data.get("answer", "")
    raw_difficulty = card_data.get("difficulty", "Medium")
    raw_topic = card_data.get("topic", "Study Deck")

    # Safe HTML escaping to prevent syntax breakage
    question = html.escape(raw_question)
    answer = html.escape(raw_answer)
    difficulty = html.escape(raw_difficulty)
    topic = html.escape(raw_topic)

    # Difficulty color tokens
    diff_styles = {
        "Easy": ("#dcfce7", "#166534"),
        "Medium": ("#fef3c7", "#92400e"),
        "Hard": ("#fee2e2", "#991b1b")
    }
    diff_bg, diff_text = diff_styles.get(difficulty, ("#f1f5f9", "#475569"))
    flipped_class = "flipped" if is_flipped else ""

    # Self-contained 3D Card Markup (No indentation on lines to ensure zero Markdown code-block triggers)
    card_html = f"""<style>
.flashcard-stage {{
width: 100%;
max-width: 680px;
height: 330px;
margin: 1.2rem auto;
perspective: 1400px;
cursor: pointer;
}}
.card-flipper-3d {{
width: 100%;
height: 100%;
position: relative;
transform-style: preserve-3d;
transition: transform 0.65s cubic-bezier(0.2, 0.8, 0.2, 1);
border-radius: 24px;
box-shadow: 0 20px 40px -12px rgba(0, 0, 0, 0.09), 0 0 0 1px rgba(226, 232, 240, 0.9);
}}
.card-flipper-3d.flipped {{
transform: rotateY(180deg);
}}
.card-face-pane {{
position: absolute;
width: 100%;
height: 100%;
border-radius: 24px;
padding: 26px 30px;
backface-visibility: hidden;
-webkit-backface-visibility: hidden;
display: flex;
flex-direction: column;
justify-content: space-between;
box-sizing: border-box;
}}
.card-face-front {{
background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
border: 2px solid #e2e8f0;
}}
.card-face-back {{
background: linear-gradient(135deg, #f0fdf4 0%, #ffffff 100%);
border: 2px solid #86efac;
transform: rotateY(180deg);
}}
.card-badge-q {{
display: inline-block;
padding: 5px 14px;
background: #e0e7ff;
color: #3730a3;
border-radius: 9999px;
font-size: 11px;
font-weight: 800;
text-transform: uppercase;
letter-spacing: 0.05em;
}}
.card-badge-a {{
display: inline-block;
padding: 5px 14px;
background: #dcfce7;
color: #15803d;
border-radius: 9999px;
font-size: 11px;
font-weight: 800;
text-transform: uppercase;
letter-spacing: 0.05em;
}}
.card-badge-diff {{
padding: 4px 12px;
border-radius: 9999px;
font-size: 11px;
font-weight: 800;
text-transform: uppercase;
background: {diff_bg};
color: {diff_text};
}}
.card-body-question {{
font-size: 1.34rem;
font-weight: 700;
line-height: 1.48;
color: #0f172a;
margin: 12px 0;
}}
.card-body-answer {{
font-size: 1.15rem;
font-weight: 500;
line-height: 1.6;
color: #1e293b;
margin: 12px 0;
}}
.card-bottom-bar {{
display: flex;
justify-content: space-between;
align-items: center;
border-top: 1px solid rgba(226, 232, 240, 0.8);
padding-top: 12px;
font-size: 13px;
font-weight: 600;
}}
.card-flipper-3d:hover {{
box-shadow: 0 24px 45px -10px rgba(99, 102, 241, 0.16), 0 0 0 1.5px rgba(99, 102, 241, 0.35);
}}
</style>

<div class="flashcard-stage" onclick="this.querySelector('.card-flipper-3d').classList.toggle('flipped');">
<div class="card-flipper-3d {flipped_class}" id="card-flipper-main">
<!-- Front Face: Question -->
<div class="card-face-pane card-face-front">
<div style="display:flex; justify-content:space-between; align-items:center;">
<span class="card-badge-q">Question {current_idx + 1} of {total_cards}</span>
<span class="card-badge-diff">{difficulty}</span>
</div>
<div class="card-body-question">
{question}
</div>
<div class="card-bottom-bar">
<span style="color:#64748b;">📖 {topic}</span>
<span style="color:#4f46e5; font-weight:700;">🔄 Click anywhere to Flip ➔</span>
</div>
</div>

<!-- Back Face: Answer -->
<div class="card-face-pane card-face-back">
<div style="display:flex; justify-content:space-between; align-items:center;">
<span class="card-badge-a">Answer Reveal</span>
<span class="card-badge-diff">{difficulty}</span>
</div>
<div class="card-body-answer">
{answer}
</div>
<div class="card-bottom-bar">
<span style="color:#047857;">💡 Active Recall Verified</span>
<span style="color:#059669; font-weight:700;">🔄 Click to Flip Back ➔</span>
</div>
</div>
</div>
</div>
"""
    if hasattr(st, "html"):
        st.html(card_html)
    else:
        st.markdown(card_html, unsafe_allow_html=True)


def render_card_controls(current_idx: int, total_cards: int):
    """
    Render controls below the 3D card:
    - Flip / Reveal Answer toggle button
    - Mastery buttons: '✓ I Know This' & '✕ Need Revision'
    - Navigation: '← Previous' and 'Next →'
    - Real-time Progress Bar
    """
    is_flipped = st.session_state.get("is_flipped", False)
    btn_flip_label = "🔄 Flip to Question" if is_flipped else "✨ Reveal Answer (3D Flip)"
    
    col_flip_a, col_flip_b, col_flip_c = st.columns([1, 2, 1])
    with col_flip_b:
        if st.button(btn_flip_label, key=f"flip_btn_{current_idx}", use_container_width=True):
            st.session_state.is_flipped = not is_flipped
            st.rerun()

    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

    # Mastery Feedback: Known vs Need Revision
    col_know, col_rev = st.columns(2)
    with col_know:
        if st.button("✓ I Know This", key=f"know_btn_{current_idx}", use_container_width=True):
            st.session_state.known_cards.add(current_idx)
            st.session_state.revision_cards.discard(current_idx)
            st.session_state.is_flipped = False
            if current_idx < total_cards - 1:
                st.session_state.current_index += 1
            else:
                st.session_state.completed = True
            st.rerun()

    with col_rev:
        if st.button("✕ Need Revision", key=f"rev_btn_{current_idx}", use_container_width=True):
            st.session_state.revision_cards.add(current_idx)
            st.session_state.known_cards.discard(current_idx)
            st.session_state.is_flipped = False
            if current_idx < total_cards - 1:
                st.session_state.current_index += 1
            else:
                st.session_state.completed = True
            st.rerun()

    st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)

    # Traversal Navigation: Previous / Next
    col_prev, col_status, col_next = st.columns([1.2, 1.6, 1.2])
    with col_prev:
        prev_disabled = (current_idx == 0)
        if st.button("← Previous", disabled=prev_disabled, key=f"prev_btn_{current_idx}", use_container_width=True):
            st.session_state.current_index -= 1
            st.session_state.is_flipped = False
            st.rerun()

    with col_status:
        st.markdown(
            f"<div style='text-align:center; padding-top:6px; font-weight:700; color:#475569; font-size:0.95rem;'>"
            f"Card {current_idx + 1} / {total_cards}"
            f"</div>",
            unsafe_allow_html=True
        )

    with col_next:
        if current_idx < total_cards - 1:
            if st.button("Next →", type="primary", key=f"next_btn_{current_idx}", use_container_width=True):
                st.session_state.current_index += 1
                st.session_state.is_flipped = False
                st.rerun()
        else:
            if st.button("Finish Deck 🎉", type="primary", key="finish_deck_btn", use_container_width=True):
                st.session_state.completed = True
                st.rerun()

    # Visual Progress Bar
    progress_val = (current_idx + 1) / total_cards
    pct = int(progress_val * 100)
    st.markdown(
        f"<div style='display:flex; justify-content:space-between; font-size:0.8rem; font-weight:700; color:#64748b; margin-top:14px; margin-bottom:4px;'>"
        f"<span>Study Progress</span><span>{pct}%</span></div>",
        unsafe_allow_html=True
    )
    st.progress(progress_val)
