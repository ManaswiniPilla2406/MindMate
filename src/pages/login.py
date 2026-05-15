import streamlit as st
import json
from pathlib import Path

# ---------------- USERS FILE ----------------
USERS_FILE = Path(__file__).resolve().parents[1] / "users.json"

# Create users.json automatically
if not USERS_FILE.exists():
    USERS_FILE.write_text("{}")

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Login - MindMate",
    page_icon="🌿",
    layout="centered"
)

# ---------------- HIDE SIDEBAR ----------------
st.markdown("""
<style>

/* Hide Sidebar */
[data-testid="stSidebar"] {
    display: none;
}

/* Hide Sidebar Navigation */
section[data-testid="stSidebarNav"] {
    display: none;
}

/* Hide Header */
[data-testid="stHeader"] {
    display: none;
}

/* Main Background */
.stApp {
    background-color: #f8f7f2;
}

/* Title */
.title {
    text-align: center;
    color: #2c3e2c;
    font-size: 3rem;
    margin-top: 50px;
    margin-bottom: 10px;
}

/* Subtitle */
.subtitle {
    text-align: center;
    color: #6b7a6b;
    margin-bottom: 40px;
    font-size: 1.1rem;
}

/* Buttons */
.stButton > button {
    width: 100%;
    border-radius: 12px;
    background-color: #7fb77e;
    color: white;
    border: none;
    padding: 0.7rem;
    font-size: 1rem;
}

.stButton > button:hover {
    background-color: #6ca56b;
    color: white;
}

/* Input Boxes */
div[data-baseweb="input"] {
    border-radius: 12px !important;
}

</style>
""", unsafe_allow_html=True)

# ---------------- UI ----------------
st.markdown(
    '<div class="title">🌿 MindMate</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Login to continue your wellness journey</div>',
    unsafe_allow_html=True
)

# ---------------- FORM ----------------
username = st.text_input("Username")
password = st.text_input("Password", type="password")

# ---------------- LOGIN ----------------
if st.button("Login"):

    with open(USERS_FILE, "r") as f:
        users = json.load(f)

    if username in users and users[username]["password"] == password:

        st.session_state.logged_in = True
        st.session_state.username = username

        st.success("Login successful!")

        st.switch_page("app.py")

    else:
        st.error("Invalid username or password")

# ---------------- SIGNUP ----------------
st.markdown("### Don't have an account?")

if st.button("Create New Account"):
    st.switch_page("pages/signup.py")