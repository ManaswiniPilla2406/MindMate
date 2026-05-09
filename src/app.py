from __future__ import annotations

import sys
from pathlib import Path
import streamlit as st

# Path configuration
ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from src.chatbot import EmotionAwareCompanion

# ---------------- UI CONFIG ----------------
st.set_page_config(
    page_title="MindMate",
    page_icon="🌿",
    layout="centered"
)

# ---------------- THEME (Refined Cream + Sage Green) ----------------
st.markdown("""
<style>
    /* Background and global font */
    .stApp {
        background-color: #f8f7f2;
        color: #3e4a3e;
    }

    /* Header Styling */
    .main-header {
        text-align: center;
        padding: 20px 0;
    }
    .main-header h1 {
        font-size: 3rem;
        color: #2c3e2c;
        margin-bottom: 0;
    }
    .main-header span {
        color: #7fb77e;
    }
    .sub-header {
        text-align: center;
        color: #6b7a6b;
        font-size: 1.1rem;
        margin-bottom: 40px;
    }

    /* Chat Container Simulation */
    .chat-container {
        background-color: #f1f3ee;
        border-radius: 20px;
        padding: 20px;
        border: 1px solid #e0e4d9;
        margin-bottom: 20px;
    }

    /* Chat Bubbles */
    .bot-bubble {
        background-color: contrast-color: #3e4a3e;
        padding: 15px;
        border-radius: 15px 15px 15px 0px;
        margin-bottom: 10px;
        max-width: 85%;
        border: 1px solid #ccd5c9;
    }
    .user-bubble {
        background-color: #5f7a5f;
        color: white;
        padding: 15px;
        border-radius: 15px 15px 0px 15px;
        margin-left: auto;
        margin-bottom: 10px;
        max-width: 80%;
        text-align: left;
    }

    /* Small labels inside bubbles */
    .emotion-label {
        font-weight: bold;
        font-size: 0.8rem;
        margin-bottom: 5px;
        display: block;
    }

    /* Input Styling */
    div[data-baseweb="input"] {
        border-radius: 25px !important;
        background-color: white !important;
    }
</style>
""", unsafe_allow_html=True)

# ---------------- MODEL ----------------
@st.cache_resource
def get_bot():
    return EmotionAwareCompanion()

bot = get_bot()

# ---------------- SESSION ----------------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "bot", "content": "Hi, I'm MindMate 🌿 — your emotion-aware study companion. Tell me how you're feeling or what's on your mind, and I'll meet you where you are.", "emotion": "neutral"}
    ]

# ---------------- HEADER ----------------
st.markdown('<div class="main-header"><h1>Hey, how are you <span>really</span> feeling?</h1></div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">MindMate listens, senses your emotions, and gently supports your studies and wellbeing.</div>', unsafe_allow_html=True)

# ---------------- CHAT DISPLAY ----------------
for msg in st.session_state.messages:
    if msg["role"] == "bot":
        emotion_html = f"<span class='emotion-label'>Emotion: {msg.get('emotion', 'analyzing...')}</span>" if "emotion" in msg else ""
        content = msg["content"].replace("\n", "<br>")
        st.markdown(f"""
            <div class="bot-bubble">
                {emotion_html}
                {content}
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="user-bubble">{msg["content"]}</div>', unsafe_allow_html=True)

# ---------------- QUICK REPLIES (Suggestion Pills) ----------------
if len(st.session_state.messages) == 1:
    st.write("🪄 Try one of these")
    cols = st.columns([1, 1, 1])
    suggestions = ["I'm stressed about exams", "I can't focus today", "I aced my test!"]
    
    for i, suggestion in enumerate(suggestions):
        if cols[i % 3].button(suggestion, key=f"sug_{i}"):
            user_input = suggestion # Handled below

# ---------------- CHAT INPUT ----------------
with st.container():
    query = st.chat_input("Tell MindMate what's on your mind...")
    
    if query:
        # Add user message
        st.session_state.messages.append({"role": "user", "content": query})
        
        # Analyze
        result = bot.analyze(query)
        
        # Build composite response
        full_response = f"{result.response}\n\n**Try this:**\n{result.wellness_tip}\n{result.study_tip}"
        
        # Add bot message
        st.session_state.messages.append({
            "role": "bot", 
            "content": full_response, 
            "emotion": result.emotion
        })
        
        st.rerun()

# Footer
st.markdown("---")
st.caption("<center>MindMate offers supportive guidance — not a substitute for professional care.</center>", unsafe_allow_html=True)