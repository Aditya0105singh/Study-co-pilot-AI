import streamlit as st
from components.sidebar import sidebar_ui
from components.chat_ui import chat_interface
from components.study_rooms import study_rooms_ui

st.set_page_config(page_title="Student Copilot AI", page_icon="✦", layout="wide")

# Viewport meta for mobile
st.markdown('<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">', unsafe_allow_html=True)

# Debug: Check if API key is loaded
import os
from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY") or st.secrets.get("GEMINI_API_KEY", "NOT_FOUND")

# Initialize session state
defaults = {
    "current_mode": None, "messages": [], "api_choice": "Gemini",
    "answer_style": "Beginner Friendly", "in_study_room": False,
    "current_room": None, "user_name": "", "rooms": {},
    "room_messages": [], "join_code_from_home": "",
    "camera_enabled": True, "mic_enabled": True, "welcomed": False
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

if not st.session_state.welcomed:
    st.toast("Welcome back! AI engines are initialized & ready.", icon="🚀")
    st.session_state.welcomed = True

# ─────────────────────────────────────────────────────────────
# GLOBAL BRANDING & SVG RESOURCES
# ─────────────────────────────────────────────────────────────
GLOBAL_SVG_BRAIN = '<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9.5 2A2.5 2.5 0 0 1 12 4.5v15a2.5 2.5 0 0 1-4.96.44 2.5 2.5 0 0 1-2.96-3.08 3 3 0 0 1-.34-5.58 2.5 2.5 0 0 1 1.32-4.24 2.5 2.5 0 0 1 1.98-3A2.5 2.5 0 0 1 9.5 2Z"/><path d="M14.5 2A2.5 2.5 0 0 0 12 4.5v15a2.5 2.5 0 0 0 4.96.44 2.5 2.5 0 0 0 2.96-3.08 3 3 0 0 0 .34-5.58 2.5 2.5 0 0 0-1.32-4.24 2.5 2.5 0 0 0-1.98-3A2.5 2.5 0 0 0 14.5 2Z"/></svg>'
GLOBAL_SVG_NODES = '<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="7" height="7" x="14" y="3" rx="1"/><path d="M10 21V8a1 1 0 0 0-1-1H4a1 1 0 0 0-1 1v12a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1v-5a1 1 0 0 0-1-1H3"/></svg>'
GLOBAL_SVG_TARGET = '<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/></svg>'
GLOBAL_SVG_ZAP = '<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 14a1 1 0 0 1-.78-1.63l9.9-10.2a.5.5 0 0 1 .86.46l-1.92 6.02A1 1 0 0 0 13 10h7a1 1 0 0 1 .78 1.63l-9.9 10.2a.5.5 0 0 1-.86-.46l1.92-6.02A1 1 0 0 0 11 14z"/></svg>'
GLOBAL_SVG_BOT = '<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="18" height="14" x="3" y="7" rx="2" ry="2"/><path d="M12 7V3"/><path d="M15 3h-6"/><path d="M9 13h.01"/><path d="M15 13h.01"/><path d="M10 17h4"/></svg>'
GLOBAL_SVG_SPARKLE = '<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9.937 15.5A2 2 0 0 0 8.5 14.063l-6.135-1.582a.5.5 0 0 1 0-.962L8.5 9.936A2 2 0 0 0 9.937 8.5l1.582-6.135a.5.5 0 0 1 .963 0L14.063 8.5A2 2 0 0 0 15.5 9.937l6.135 1.581a.5.5 0 0 1 0 .964L15.5 14.063a2 2 0 0 0-1.437 1.437l-1.582 6.135a.5.5 0 0 1-.963 0z"/><path d="M20 3v4"/><path d="M22 5h-4"/><path d="M4 17v2"/><path d="M5 18H3"/></svg>'

# ─────────────────────────────────────────────────────────────
# DESIGN SYSTEM — "Premium Light"
# Inspired by Modern SaaS Tooling
# Clean white base · Soft Shadows · Green Accents
# ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

*, *::before, *::after { font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; }

:root {
    --card-bg: #0C0C0E;
    --card-border: #222225;
    --card-hover-border: #44444A;
    
    --text-muted: #888888;
    --primary: #5E6AD2;
    
    --c-blue:   #3B82F6;
    --c-purple: #8B5CF6;
    --c-amber:  #F59E0B;
    --c-teal:   #14B8A6;
    --c-rose:   #F43F5E;
    --c-orange: #F97316;
}

@keyframes shimmer {
    0% { background-position: 200% center; }
    100% { background-position: -200% center; }
}

@keyframes fadeUp {
    0% { opacity: 0; transform: translateY(20px); }
    100% { opacity: 1; transform: translateY(0); }
}

@keyframes float {
    0% { transform: translateY(0px); }
    50% { transform: translateY(-10px); }
    100% { transform: translateY(0px); }
}

/* Subtle architectural grid pattern to break up pure black */
.stApp {
    background-color: #050505;
    background-image: 
        radial-gradient(rgba(255, 255, 255, 0.04) 1px, transparent 1px);
    background-size: 24px 24px;
}

section.main > div.block-container {
    background: none;
}

.hero-wrap { text-align: center; padding: 3rem 1rem 2.5rem; position: relative; }

@keyframes pulseGlow {
    0% { box-shadow: 0 0 5px rgba(94, 106, 210, 0.2); border-color: rgba(94, 106, 210, 0.3); }
    50% { box-shadow: 0 0 20px rgba(94, 106, 210, 0.6); border-color: rgba(94, 106, 210, 0.8); }
    100% { box-shadow: 0 0 5px rgba(94, 106, 210, 0.2); border-color: rgba(94, 106, 210, 0.3); }
}

.hero-badge {
    display: inline-block;
    color: #EEEEEE;
    font-size: 0.75rem;
    font-weight: 600;
    padding: 5px 16px;
    border-radius: 20px;
    letter-spacing: 0.5px;
    margin-bottom: 1rem;
    border: 1px solid var(--primary);
    transition: all 0.3s ease;
    cursor: default;
    
    /* Shimmer & Continuous Glow Effect */
    background: linear-gradient(90deg, #111111 25%, #2a2a35 50%, #111111 75%);
    background-size: 200% auto;
    animation: shimmer 4s linear infinite, pulseGlow 3s ease-in-out infinite;
}
.hero-badge:hover {
    color: #FFFFFF;
    transform: translateY(-1px);
}

.hero-title {
    font-size: 2.8rem;
    font-weight: 800;
    letter-spacing: -1.5px;
    line-height: 1.15;
    background: linear-gradient(90deg, #888888 0%, #FFFFFF 50%, #888888 100%);
    background-size: 200% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.8rem;
    animation: fadeUp 0.8s cubic-bezier(0.16, 1, 0.3, 1) forwards, shimmer 5s ease-in-out infinite;
}

.hero-subtitle {
    font-size: 1.05rem;
    color: var(--text-muted);
    font-weight: 400;
    line-height: 1.6;
    max-width: 500px;
    margin: 0 auto;
}

.section-header {
    font-size: 0.8rem;
    font-weight: 600;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin: 2rem 0 1rem;
}

.fcard {
    background: var(--card-bg);
    border: 1px solid var(--card-border);
    border-radius: 14px;
    padding: 1.2rem 1.4rem;
    transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    box-shadow: 0 4px 10px rgba(0,0,0,0.5);
    position: relative;
    overflow: hidden;
    margin-bottom: 0.4rem;
    backdrop-filter: blur(10px);
    
    /* Entrance Animation */
    opacity: 0;
    animation: fadeUp 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}

/* Stagger entrance by element index roughly */
div[data-testid="column"]:nth-child(1) .fcard { animation-delay: 0.1s; }
div[data-testid="column"]:nth-child(2) .fcard { animation-delay: 0.2s; }
div[data-testid="column"]:nth-child(3) .fcard { animation-delay: 0.3s; }

.fcard::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    border-radius: 14px 14px 0 0;
    opacity: 0;
    transition: opacity 0.3s ease;
}
.fcard:hover { 
    transform: translateY(-8px) scale(1.02); 
    box-shadow: 0 20px 40px rgba(0,0,0,0.9);
    z-index: 10;
}
.fcard:hover::before { opacity: 1; }

.fcard-blue::before   { background: var(--c-blue); }
.fcard-purple::before { background: var(--c-purple); }
.fcard-amber::before  { background: var(--c-amber); }
.fcard-teal::before   { background: var(--c-teal); }
.fcard-rose::before   { background: var(--c-rose); }
.fcard-orange::before { background: var(--c-orange); }

.fcard-blue:hover   { border-color: var(--c-blue); box-shadow: 0 12px 30px rgba(0,0,0,0.8), 0 0 20px rgba(59, 130, 246, 0.15); }
.fcard-purple:hover { border-color: var(--c-purple); box-shadow: 0 12px 30px rgba(0,0,0,0.8), 0 0 20px rgba(139, 92, 246, 0.15); }
.fcard-amber:hover  { border-color: var(--c-amber); box-shadow: 0 12px 30px rgba(0,0,0,0.8), 0 0 20px rgba(245, 158, 11, 0.15); }
.fcard-teal:hover   { border-color: var(--c-teal); box-shadow: 0 12px 30px rgba(0,0,0,0.8), 0 0 20px rgba(20, 184, 166, 0.15); }
.fcard-rose:hover   { border-color: var(--c-rose); box-shadow: 0 12px 30px rgba(0,0,0,0.8), 0 0 20px rgba(244, 63, 94, 0.15); }
.fcard-orange:hover { border-color: var(--c-orange); box-shadow: 0 12px 30px rgba(0,0,0,0.8), 0 0 20px rgba(249, 115, 22, 0.15); }

.fcard-blue   .fc-icon { color: var(--c-blue); }
.fcard-purple .fc-icon { color: var(--c-purple); }
.fcard-amber  .fc-icon { color: var(--c-amber); }
.fcard-teal   .fc-icon { color: var(--c-teal); }
.fcard-rose   .fc-icon { color: var(--c-rose); }
.fcard-orange .fc-icon { color: var(--c-orange); }

.fc-icon { margin-bottom: 0.8rem; display: block; }
.fc-icon svg { width: 32px; height: 32px; stroke-width: 1.5; filter: drop-shadow(0 0 5px currentColor); }
.fc-title { font-size: 1.05rem; font-weight: 600; margin-bottom: 0.4rem; color: #EEEEEE; }
.fc-desc { font-size: 0.85rem; color: var(--text-muted); line-height: 1.55; }

div.stButton > button {
    border-radius: 8px !important;
    font-weight: 500 !important;
    font-size: 0.85rem !important;
    padding: 0.55rem 1.2rem !important;
    transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1) !important;
    width: 100%;
    background: #0A0A0B !important;
    border: 1px solid #222225 !important;
    color: #EEEEEE !important;
}
div.stButton > button:hover {
    background: #111113 !important;
    border-color: var(--primary) !important;
    color: #FFFFFF !important;
    box-shadow: 0 0 14px rgba(94, 106, 210, 0.3) !important;
    transform: translateY(-1px) !important;
}

.collab-card {
    background: var(--card-bg);
    border: 1px solid var(--card-border);
    border-radius: 16px;
    padding: 2rem;
    transition: border-color 0.2s ease;
    backdrop-filter: blur(10px);
}
.collab-card:hover { 
    border-color: var(--primary); 
    box-shadow: 0 8px 24px rgba(0,0,0,0.6), 0 0 20px rgba(94, 106, 210, 0.1);
}

.bfeat {
    background: var(--card-bg);
    border: 1px solid var(--card-border);
    border-radius: 12px;
    padding: 1.3rem;
    text-align: center;
    min-height: 120px;
    transition: all 0.2s ease;
    backdrop-filter: blur(10px);
}
.bfeat:hover { border-color: var(--card-hover-border); transform: translateY(-3px); box-shadow: 0 8px 16px rgba(0,0,0,0.5); }
.bfeat-icon { margin-bottom: 0.5rem; display: flex; justify-content: center; }
.bfeat-icon svg { width: 28px; height: 28px; stroke-width: 1.5; color: var(--text-muted); transition: color 0.3s, filter 0.3s; }
.bfeat:hover .bfeat-icon svg { color: var(--primary); filter: drop-shadow(0 0 4px var(--primary)); }
.bfeat-title { font-size: 0.9rem; font-weight: 600; margin-bottom: 0.25rem; color: #EEEEEE; transition: color 0.3s; }
.bfeat:hover .bfeat-title { color: #FFFFFF; }
.bfeat-desc { font-size: 0.8rem; color: var(--text-muted); line-height: 1.4; }

::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-thumb { background: #333333; border-radius: 10px; }
::-webkit-scrollbar-thumb:hover { background: #555555; }

section[data-testid="stSidebar"] {
    border-right: 1px solid #1A1A1C !important;
    background: #09090B !important;
}

.stTextInput > div > div > input,
.stSelectbox > div > div {
    border-radius: 8px !important;
    background: #0A0A0A !important;
    border: 1px solid #333333 !important;
    color: #EEEEEE !important;
}
.stTextInput > div > div > input:focus,
.stSelectbox > div > div:focus-within {
    border-color: var(--primary) !important;
    box-shadow: 0 0 0 2px rgba(94, 106, 210, 0.2) !important;
}

.stForm {
    border: 1px solid var(--card-border) !important;
    border-radius: 12px !important;
    background: var(--card-bg) !important;
}

@media (max-width: 768px) {
    /* ── Hero ── */
    .hero-wrap { padding: 1.5rem 0.5rem 1.2rem; }
    .hero-title { font-size: 1.6rem !important; letter-spacing: -0.5px; }
    .hero-subtitle { font-size: 0.88rem; padding: 0 0.5rem; }
    .hero-badge { font-size: 0.65rem; padding: 4px 12px; }

    /* ── Feature cards: stack single column ── */
    .fcard { padding: 1rem 1rem; margin-bottom: 0.3rem; }
    .fc-icon { font-size: 1.3rem; margin-bottom: 0.5rem; }
    .fc-title { font-size: 0.95rem; }
    .fc-desc { font-size: 0.8rem; }

    /* ── Streamlit columns → stack on mobile ── */
    [data-testid="column"] {
        width: 100% !important;
        flex: 1 1 100% !important;
        min-width: 100% !important;
    }
    .stHorizontalBlock {
        flex-wrap: wrap !important;
        gap: 0.3rem !important;
    }

    /* ── Buttons: bigger tap targets ── */
    div.stButton > button {
        font-size: 0.9rem !important;
        padding: 0.7rem 1rem !important;
        min-height: 44px !important;
    }

    /* ── Section headers ── */
    .section-header { font-size: 0.72rem; margin: 1.2rem 0 0.6rem; }

    /* ── Collab card ── */
    .collab-card { padding: 1.2rem; }

    /* ── Bottom features ── */
    .bfeat { padding: 1rem; min-height: auto; }
    .bfeat-icon { font-size: 1.2rem; }
    .bfeat-title { font-size: 0.85rem; }
    .bfeat-desc { font-size: 0.75rem; }

    /* ── Main container: reduce padding ── */
    section.main > div.block-container {
        padding-left: 0.5rem !important;
        padding-right: 0.5rem !important;
        padding-top: 1rem !important;
    }

    /* ── Sidebar mobile: slimmer ── */
    section[data-testid="stSidebar"] {
        min-width: 240px !important;
        max-width: 240px !important;
    }
    section[data-testid="stSidebar"] > div {
        padding: 0.8rem 0.6rem !important;
    }

    /* ── Chat input ── */
    [data-testid="stChatInput"] {
        padding: 0.3rem 0.5rem !important;
    }
    [data-testid="stChatInput"] textarea {
        font-size: 0.9rem !important;
    }

    /* ── Selectbox / Input ── */
    .stSelectbox, .stTextInput {
        font-size: 0.88rem !important;
    }

    /* ── Study Rooms: responsive cards ── */
    .room-card { padding: 1rem; }
    .room-code { font-size: 1.4rem; padding: 0.3rem 0.6rem; }

    /* ── Chat messages ── */
    .chat-message { padding: 0.6rem 0.8rem; }
    .chat-sender { font-size: 0.75rem; }

    /* ── AI response cards ── */
    .ai-card { padding: 1rem; margin: 0.5rem 0; }
    .ai-card-header { font-size: 0.7rem; }
    .ai-section-label { font-size: 0.8rem; }

    /* ── Video container ── */
    .video-container { border-radius: 8px; }

    /* ── Scrollbar: thinner on mobile ── */
    ::-webkit-scrollbar { width: 3px; }
}

/* ── Small phones (< 480px) ── */
@media (max-width: 480px) {
    .hero-title { font-size: 1.35rem !important; }
    .hero-subtitle { font-size: 0.82rem; }
    .fcard { padding: 0.8rem; border-radius: 10px; }
    .fc-icon { font-size: 1.1rem; margin-bottom: 0.3rem; }
    .fc-title { font-size: 0.88rem; }
    .fc-desc { font-size: 0.75rem; }

    div.stButton > button {
        font-size: 0.85rem !important;
        padding: 0.65rem 0.8rem !important;
    }

    section.main > div.block-container {
        padding-left: 0.3rem !important;
        padding-right: 0.3rem !important;
    }

    .collab-card { padding: 0.8rem; }
    .room-code { font-size: 1.2rem; }
}

/* ── Premium Streamlit Hiding ── */
#MainMenu {visibility: hidden;}
.stAppDeployButton {display: none;}
header {visibility: hidden;}
footer {visibility: hidden;}

/* ── Custom Chat Speech Bubbles ── */
[data-testid="stChatMessage"] {
    background-color: transparent !important;
    border: none !important;
    padding: 0.5rem 0 !important;
}

/* Assistant Messages */
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) .stMarkdown {
    background: linear-gradient(145deg, rgba(94, 106, 210, 0.08) 0%, rgba(30, 30, 40, 0) 100%) !important;
    border-left: 3px solid var(--primary);
    border-radius: 4px 16px 16px 16px;
    padding: 1.2rem 1.4rem;
    box-shadow: 0 4px 20px rgba(0,0,0,0.15);
}

/* User Messages */
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) {
    flex-direction: row-reverse;
}
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) .stMarkdown {
    background-color: #212124 !important;
    border: 1px solid #333333;
    border-radius: 16px 16px 4px 16px;
    padding: 0.8rem 1.2rem;
    display: inline-block;
}
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) [data-testid="chatAvatarIcon-user"] {
    margin-left: 1rem;
    margin-right: 0;
}

</style>
""", unsafe_allow_html=True)


# ─────────────── Sidebar ───────────────
sidebar_ui()


# ─────────────── Navigation ───────────────
def set_mode(mode):
    st.session_state.current_mode = mode
    st.session_state.messages = []
    st.session_state.in_study_room = False


def show_home():
    """Home dashboard with color-coded feature cards."""

    # Hero
    st.markdown("""
    <div class="hero-wrap">
        <div class="hero-badge">✦ AI-Powered Study Suite</div>
        <div class="hero-title">Student Copilot AI</div>
        <div class="hero-subtitle">
            Six intelligent tools — one calm interface.<br>
            Explain, visualize, quiz, revise, and prepare.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-header">Choose a Tool</div>', unsafe_allow_html=True)

    # Card data: (icon, title, desc, mode_key, color_class)
    cards = [
        (GLOBAL_SVG_BRAIN,   "Study & Understand",  "Deep explanations with structured breakdowns and examples.",    "explainer",  "fcard-blue"),
        (GLOBAL_SVG_NODES,   "Visualize Concepts",  "Auto-generate flowcharts, mind maps, and system diagrams.",     "visualizer",  "fcard-purple"),
        (GLOBAL_SVG_TARGET,  "Exam Preparation",    "Practice questions, mock tests, and instant evaluation.",        "quizzer",    "fcard-amber"),
        (GLOBAL_SVG_ZAP,     "Flashcards",          "Spaced repetition cards generated from any topic or PDF.",       "flashcards", "fcard-teal"),
        (GLOBAL_SVG_BOT,     "Interview Practice",  "Role-specific behavioral and technical interview prep.",         "interview",  "fcard-rose"),
        (GLOBAL_SVG_SPARKLE, "Resume Review",       "AI critique of your resume with actionable improvements.",       "resume",     "fcard-orange"),
    ]

    def handle_btn_click(mode):
        st.session_state.current_mode = mode
        st.session_state.messages = []
        st.session_state.in_study_room = False

    # Row 1
    cols = st.columns(3, gap="medium")
    for i, (icon, title, desc, mode_key, color) in enumerate(cards[:3]):
        with cols[i]:
            st.markdown(f"""
            <div class="fcard {color}">
                <span class="fc-icon">{icon}</span>
                <div class="fc-title">{title}</div>
                <div class="fc-desc">{desc}</div>
            </div>
            """, unsafe_allow_html=True)
            st.button(f"Open {title}", key=f"btn_{mode_key}", on_click=handle_btn_click, args=(mode_key,), use_container_width=True)

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    # Row 2
    cols2 = st.columns(3, gap="medium")
    for i, (icon, title, desc, mode_key, color) in enumerate(cards[3:]):
        with cols2[i]:
            st.markdown(f"""
            <div class="fcard {color}">
                <span class="fc-icon">{icon}</span>
                <div class="fc-title">{title}</div>
                <div class="fc-desc">{desc}</div>
            </div>
            """, unsafe_allow_html=True)
            st.button(f"Open {title}", key=f"btn_{mode_key}", on_click=handle_btn_click, args=(mode_key,), use_container_width=True)

    # ── Collab Section ──
    st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)
    st.markdown('<div class="section-header">Collaborate</div>', unsafe_allow_html=True)

    room_col1, room_col2 = st.columns([2, 1])

    # Interconnected users SVG for collab
    svg_collab = '<svg xmlns="http://www.w3.org/2000/svg" width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="#5E6AD2" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="filter: drop-shadow(0 0 6px rgba(94, 106, 210, 0.5)); margin-bottom: 0.6rem;"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>'

    with room_col1:
        st.markdown(f"""
        <div class="collab-card">
            {svg_collab}
            <div style="font-size: 1.1rem; font-weight: 600; margin-bottom: 0.4rem;">Study Rooms</div>
            <div style="opacity: 0.7; font-size: 0.9rem; line-height: 1.5;">
                Create or join a live study room with video, audio, and group chat.
                Share a 6-character code to invite classmates.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with room_col2:
        st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
        def enter_creating_room():
            st.session_state.in_study_room = True
        
        st.button("Create Room", key="btn_create_room", on_click=enter_creating_room, use_container_width=True)

        join_code = st.text_input("Join Code", placeholder="e.g. A1B2C3", max_chars=6,
                                  label_visibility="collapsed", key="quick_join_code_input")
        def enter_joining_room():
            if st.session_state.quick_join_code_input:
                st.session_state.in_study_room = True
                st.session_state.join_code_from_home = st.session_state.quick_join_code_input.upper()

        st.button("Join Room", key="btn_join_room", on_click=enter_joining_room, use_container_width=True)

    # ── Bottom capabilities ──
    st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)
    st.markdown('<div class="section-header">Platform Capabilities</div>', unsafe_allow_html=True)

    # SVGs for Bottom features
    svg_cpu = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor"><rect width="16" height="16" x="4" y="4" rx="2"/><rect width="6" height="6" x="9" y="9" rx="1"/><path d="M15 2v2"/><path d="M15 20v2"/><path d="M2 15h2"/><path d="M2 9h2"/><path d="M20 15h2"/><path d="M20 9h2"/><path d="M9 2v2"/><path d="M9 20v2"/></svg>'
    svg_doc = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor"><path d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5L14.5 2z"/><polyline points="14 2 14 8 20 8"/><path d="m9 15 2 2 4-4"/></svg>'
    svg_layers = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor"><polygon points="12 2 2 7 12 12 22 7 12 2"/><polyline points="2 17 12 22 22 17"/><polyline points="2 12 12 17 22 12"/></svg>'

    bcols = st.columns(3, gap="medium")
    bottom_features = [
        (svg_cpu,    "Multi-Model AI",     "Gemini, Groq, and Grok — automatic fallback for reliability."),
        (svg_doc,    "PDF Context",         "Upload documents once, reference them across every tool."),
        (svg_layers, "Universal UI",        "Clean interface that auto-adapts to Light & Dark Modes."),
    ]
    for i, (icon, title, desc) in enumerate(bottom_features):
        with bcols[i]:
            st.markdown(f"""
            <div class="bfeat">
                <div class="bfeat-icon">{icon}</div>
                <div class="bfeat-title">{title}</div>
                <div class="bfeat-desc">{desc}</div>
            </div>
            """, unsafe_allow_html=True)


def show_mode_interface():
    """Display the interface for the selected mode."""
    mode = st.session_state.current_mode

    # Back button
    col1, col2, col3 = st.columns([1, 6, 1])
    with col1:
        def go_back():
            st.session_state.current_mode = None
            st.session_state.messages = []
            
        st.button("← Back", use_container_width=True, on_click=go_back)

    mode_titles = {
        "explainer":  (GLOBAL_SVG_BRAIN, "Study & Understand", "var(--c-blue)"),
        "quizzer":    (GLOBAL_SVG_TARGET, "Exam Preparation", "var(--c-amber)"),
        "interview":  (GLOBAL_SVG_BOT, "Interview Practice", "var(--c-rose)"),
        "resume":     (GLOBAL_SVG_SPARKLE, "Resume Review", "var(--c-orange)"),
        "visualizer": (GLOBAL_SVG_NODES, "Visualize Concepts", "var(--c-purple)"),
        "flashcards": (GLOBAL_SVG_ZAP, "Flashcards", "var(--c-teal)")
    }

    mdata = mode_titles.get(mode, ('', 'Study Mode', 'var(--primary)'))
    
    st.markdown(f"""
    <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 1rem; padding-bottom: 0.5rem; border-bottom: 1px solid var(--border-color);">
        <div style="color: {mdata[2]}; display: flex; filter: drop-shadow(0 0 6px {mdata[2]}); opacity: 0.9;">
            {mdata[0]}
        </div>
        <h2 style="margin: 0; padding: 0; border: none; letter-spacing: -0.5px;">{mdata[1]}</h2>
    </div>
    """, unsafe_allow_html=True)

    st.session_state.answer_style = st.selectbox(
        "Answer Style",
        ["Beginner Friendly", "Intermediate", "Advanced/Technical"],
        index=0,
        help="Choose how detailed and technical you want the responses to be"
    )

    st.markdown("---")
    chat_interface(mode)


# ─────────────── Main Router ───────────────
if st.session_state.in_study_room:
    col1, col2, col3 = st.columns([1, 6, 1])
    with col1:
        if st.button("← Home", use_container_width=True):
            st.session_state.in_study_room = False
            st.session_state.current_room = None
            st.rerun()
    study_rooms_ui()
elif st.session_state.current_mode is None:
    show_home()
else:
    show_mode_interface()
