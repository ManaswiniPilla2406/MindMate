from __future__ import annotations

import sys
from pathlib import Path
import streamlit as st

# ---------------- PATH CONFIG ----------------
ROOT_DIR = Path(__file__).resolve().parents[1]

if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from src.chatbot import EmotionAwareCompanion

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="MindMate",
    page_icon="🌿",
    layout="centered"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>

    /* Entire App */
    .stApp {
        background-color: #f8f7f2;
        color: #3e4a3e;
        font-family: 'Segoe UI', sans-serif;
    }

    /* Remove dark Streamlit top spacing */
    .block-container {
        padding-top: 2rem;
    }

    /* Header */
    .main-header {
        text-align: center;
        margin-top: 20px;
    }

    .main-header h1 {
        font-size: 3.2rem;
        color: #7fb77e;
        margin-bottom: 10px;
        font-weight: 700;
    }

    .main-header span {
        color: #5f7a5f;
    }

    .sub-header {
        text-align: center;
        color: #6b7a6b;
        font-size: 1.1rem;
        margin-bottom: 35px;
    }

    /* Bot Bubble */
    .bot-bubble {
        background-color: #ffffff;
        color: #3e4a3e;
        padding: 18px;
        border-radius: 18px 18px 18px 5px;
        margin-bottom: 12px;
        border: 1px solid #d7dfd3;
        box-shadow: 0px 2px 8px rgba(0,0,0,0.03);
    }

    /* User Bubble */
    .user-bubble {
        background-color: #7fb77e;
        color: white;
        padding: 15px;
        border-radius: 18px 18px 5px 18px;
        margin-left: auto;
        margin-bottom: 12px;
        width: fit-content;
        max-width: 80%;
    }

    /* Emotion Label */
    .emotion-label {
        font-size: 0.85rem;
        font-weight: 600;
        color: #5f7a5f;
        margin-bottom: 6px;
        display: block;
    }

    /* Suggestion Buttons */
    div.stButton > button {
        background-color: #f2eadf !important;
        color: #5f7a5f !important;
        border: 1px solid #d9d1c7 !important;
        border-radius: 20px !important;
        padding: 10px 16px !important;
        font-weight: 500 !important;
        transition: 0.3s ease;
    }

    div.stButton > button:hover {
        background-color: #e8dfd2 !important;
        color: #3e4a3e !important;
        border: 1px solid #c8beb0 !important;
    }

    /* Input Box */
    .stChatInputContainer {
        background-color: transparent !important;
        border-top: none !important;
    }

    .stChatInputContainer > div {
        background-color: #f2eadf !important;
        border: 1px solid #ddd4c8 !important;
        border-radius: 18px !important;
    }

    textarea {
        color: #3e4a3e !important;
    }

    textarea::placeholder {
        color: #7a8477 !important;
    }

    /* Footer */
    .footer {
        text-align: center;
        color: #8c9489;
        margin-top: 30px;
        font-size: 0.9rem;
    }

</style>
""", unsafe_allow_html=True)

# ---------------- MODEL ----------------
@st.cache_resource
def get_bot():
    return EmotionAwareCompanion()

bot = get_bot()

# ---------------- SESSION STATE ----------------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "bot",
            "content": (
                "Hi, I'm MindMate 🌿 — your emotion-aware study companion. "
                "Tell me how you're feeling or what's on your mind, "
                "and I'll meet you where you are."
            ),
            "emotion": "neutral"
        }
    ]

# To handle suggestion clicks
if "prefill" not in st.session_state:
    st.session_state.prefill = ""

# ---------------- HEADER ----------------
st.markdown("""
<div class="main-header">
    <h1>Hey, how are you <span>really</span> feeling?</h1>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="sub-header">
MindMate listens, senses your emotions, and gently supports your studies and wellbeing.
</div>
""", unsafe_allow_html=True)

# ---------------- CHAT DISPLAY ----------------
for msg in st.session_state.messages:

    if msg["role"] == "bot":

        emotion_html = (
            f"<span class='emotion-label'>Emotion: {msg.get('emotion', 'neutral')}</span>"
        )

        content = msg["content"].replace("\n", "<br>")

        st.markdown(f"""
        <div class="bot-bubble">
            {emotion_html}
            {content}
        </div>
        """, unsafe_allow_html=True)

    else:

        st.markdown(f"""
        <div class="user-bubble">
            {msg["content"]}
        </div>
        """, unsafe_allow_html=True)

# ---------------- SUGGESTIONS ----------------
if len(st.session_state.messages) == 1:

    st.write("🪄 Try one of these")

    suggestions = [
        "I'm stressed about exams",
        "I can't focus today",
        "I aced my test!"
    ]

    cols = st.columns(3)

    for i, suggestion in enumerate(suggestions):

        if cols[i].button(suggestion):

            st.session_state.prefill = suggestion

# ---------------- CHAT INPUT ----------------
query = st.chat_input(
    "Tell MindMate what's on your mind...",
    key="chat_input"
)

# Autofill suggestion into input
if st.session_state.prefill and not query:
    query = st.session_state.prefill
    st.session_state.prefill = ""

# ---------------- PROCESS INPUT ----------------
if query:

    # User message
    st.session_state.messages.append({
        "role": "user",
        "content": query
    })

    # Bot analysis
    result = bot.analyze(query)

    # Full response
    full_response = (
        f"{result.response}\n\n"
        f"🌿 Try this:\n"
        f"{result.wellness_tip}\n\n"
        f"📚 Study Tip:\n"
        f"{result.study_tip}"
    )

    # Bot message
    st.session_state.messages.append({
        "role": "bot",
        "content": full_response,
        "emotion": result.emotion
    })

    st.rerun()

# ---------------- FOOTER ----------------
st.markdown("""
<div class="footer">
MindMate offers supportive guidance — not a substitute for professional care.
</div>
""", unsafe_allow_html=True)