import streamlit as st
from components.sidebar import sidebar_ui
from components.chat_ui import chat_interface
from components.study_rooms import study_rooms_ui

st.set_page_config(page_title="Student Copilot AI", page_icon="🎓", layout="wide")

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
    "camera_enabled": True, "mic_enabled": True
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

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
    --card-bg: #0A0A0A;
    --card-border: #222222;
    --card-hover-border: #444444;
    
    --text-muted: #888888;
    --primary: #5E6AD2;
    
    --c-blue:   #3B82F6;
    --c-purple: #8B5CF6;
    --c-amber:  #F59E0B;
    --c-teal:   #14B8A6;
    --c-rose:   #F43F5E;
    --c-orange: #F97316;
}

section.main > div.block-container {
    background: none;
}

.hero-wrap { text-align: center; padding: 3rem 1rem 2.5rem; position: relative; }

.hero-badge {
    display: inline-block;
    background: #111111;
    color: #DDDDDD;
    font-size: 0.75rem;
    font-weight: 600;
    padding: 5px 16px;
    border-radius: 20px;
    letter-spacing: 0.5px;
    margin-bottom: 1rem;
    border: 1px solid #222222;
    transition: all 0.3s ease;
    cursor: default;
}
.hero-badge:hover {
    border-color: var(--primary);
    box-shadow: 0 0 15px rgba(94, 106, 210, 0.25);
    color: #FFFFFF;
}

.hero-title {
    font-size: 2.8rem;
    font-weight: 800;
    letter-spacing: -1.5px;
    line-height: 1.15;
    background: linear-gradient(180deg, #FFFFFF 0%, #888888 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.8rem;
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
    transition: all 0.25s ease;
    box-shadow: 0 4px 10px rgba(0,0,0,0.5);
    position: relative;
    overflow: hidden;
    margin-bottom: 0.4rem;
}
.fcard::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    border-radius: 14px 14px 0 0;
    opacity: 0;
    transition: opacity 0.25s ease;
}
.fcard:hover { 
    transform: translateY(-4px); 
    box-shadow: 0 12px 30px rgba(0,0,0,0.8);
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

.fc-icon { font-size: 1.6rem; margin-bottom: 0.8rem; display: block; }
.fc-title { font-size: 1.05rem; font-weight: 600; margin-bottom: 0.4rem; color: #EEEEEE; }
.fc-desc { font-size: 0.85rem; color: var(--text-muted); line-height: 1.55; }

div.stButton > button {
    border-radius: 8px !important;
    font-weight: 500 !important;
    font-size: 0.85rem !important;
    padding: 0.55rem 1.2rem !important;
    transition: all 0.2s ease !important;
    width: 100%;
    background: #0A0A0A !important;
    border: 1px solid #222222 !important;
    color: #EEEEEE !important;
}
div.stButton > button:hover {
    background: #111111 !important;
    border-color: var(--primary) !important;
    color: #FFFFFF !important;
}

.collab-card {
    background: var(--card-bg);
    border: 1px solid var(--card-border);
    border-radius: 16px;
    padding: 2rem;
    transition: border-color 0.2s ease;
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
}
.bfeat:hover { border-color: var(--card-hover-border); transform: translateY(-3px); }
.bfeat-icon { font-size: 1.4rem; margin-bottom: 0.5rem; }
.bfeat-title { font-size: 0.9rem; font-weight: 600; margin-bottom: 0.25rem; color: #EEEEEE; }
.bfeat-desc { font-size: 0.8rem; color: var(--text-muted); line-height: 1.4; }

::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-thumb { background: #333333; border-radius: 10px; }
::-webkit-scrollbar-thumb:hover { background: #555555; }

section[data-testid="stSidebar"] {
    border-right: 1px solid #1A1A1A !important;
    background: #000000 !important;
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
        ("🧠", "Study & Understand",  "Deep explanations with structured breakdowns and examples.",    "explainer",  "fcard-blue"),
        ("📊", "Visualize Concepts",  "Auto-generate flowcharts, mind maps, and system diagrams.",     "visualizer",  "fcard-purple"),
        ("📝", "Exam Preparation",    "Practice questions, mock tests, and instant evaluation.",        "quizzer",    "fcard-amber"),
        ("⚡", "Flashcards",          "Spaced repetition cards generated from any topic or PDF.",       "flashcards", "fcard-teal"),
        ("💼", "Interview Practice",  "Role-specific behavioral and technical interview prep.",         "interview",  "fcard-rose"),
        ("📄", "Resume Review",       "AI critique of your resume with actionable improvements.",       "resume",     "fcard-orange"),
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

    with room_col1:
        st.markdown("""
        <div class="collab-card">
            <div style="font-size: 2rem; margin-bottom: 0.6rem;">👥</div>
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

    bcols = st.columns(3, gap="medium")
    bottom_features = [
        ("🤖", "Multi-Model AI",     "Gemini, Groq, and Grok — automatic fallback for reliability."),
        ("📎", "PDF Context",         "Upload documents once, reference them across every tool."),
        ("🌙", "Universal UI",        "Clean interface that auto-adapts to Light & Dark Modes."),
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
        "explainer":  "🧠 Study & Understand",
        "quizzer":    "📝 Exam Preparation",
        "interview":  "💼 Interview Practice",
        "resume":     "📄 Resume Review",
        "visualizer": "📊 Visualize Concepts",
        "flashcards": "⚡ Flashcards"
    }

    st.markdown(f"## {mode_titles.get(mode, 'Study Mode')}")

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
