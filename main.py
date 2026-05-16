"""
main.py
========

Study Copilot AI — entry point.

This file owns:
  - page config + global design system (CSS injection)
  - SVG icon set
  - home / mode interface / study-room routing
"""

import os
import streamlit as st
from dotenv import load_dotenv

from components.sidebar import sidebar_ui
from components.chat_ui import chat_interface
from components.study_rooms import study_rooms_ui

# ─────────────────────────────────────────────────────────────
# Page config
# ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Study Copilot AI",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Viewport meta for mobile
st.markdown(
    '<meta name="viewport" content="width=device-width, initial-scale=1.0">',
    unsafe_allow_html=True,
)

load_dotenv()

# ─────────────────────────────────────────────────────────────
# Session state defaults
# ─────────────────────────────────────────────────────────────
_DEFAULTS = {
    "current_mode": None,
    "messages": [],
    "api_choice": "Groq (Free)",
    "answer_style": "Beginner Friendly",
    "in_study_room": False,
    "current_room": None,
    "user_name": "",
    "rooms": {},
    "room_messages": [],
    "join_code_from_home": "",
    "camera_enabled": True,
    "mic_enabled": True,
    "welcomed": False,
}
for _k, _v in _DEFAULTS.items():
    st.session_state.setdefault(_k, _v)

if not st.session_state.welcomed:
    st.toast("Welcome to Study Copilot — your AI study suite is ready.", icon="✨")
    st.session_state.welcomed = True

# ─────────────────────────────────────────────────────────────
# SVG icons
# ─────────────────────────────────────────────────────────────
SVG_BRAIN   = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M9.5 2A2.5 2.5 0 0 1 12 4.5v15a2.5 2.5 0 0 1-4.96.44 2.5 2.5 0 0 1-2.96-3.08 3 3 0 0 1-.34-5.58 2.5 2.5 0 0 1 1.32-4.24 2.5 2.5 0 0 1 1.98-3A2.5 2.5 0 0 1 9.5 2Z"/><path d="M14.5 2A2.5 2.5 0 0 0 12 4.5v15a2.5 2.5 0 0 0 4.96.44 2.5 2.5 0 0 0 2.96-3.08 3 3 0 0 0 .34-5.58 2.5 2.5 0 0 0-1.32-4.24 2.5 2.5 0 0 0-1.98-3A2.5 2.5 0 0 0 14.5 2Z"/></svg>'
SVG_NODES   = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="6" cy="6" r="3"/><circle cx="18" cy="6" r="3"/><circle cx="6" cy="18" r="3"/><circle cx="18" cy="18" r="3"/><line x1="9" y1="6" x2="15" y2="6"/><line x1="6" y1="9" x2="6" y2="15"/><line x1="18" y1="9" x2="18" y2="15"/><line x1="9" y1="18" x2="15" y2="18"/></svg>'
SVG_TARGET  = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/></svg>'
SVG_ZAP     = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M4 14a1 1 0 0 1-.78-1.63l9.9-10.2a.5.5 0 0 1 .86.46l-1.92 6.02A1 1 0 0 0 13 10h7a1 1 0 0 1 .78 1.63l-9.9 10.2a.5.5 0 0 1-.86-.46l1.92-6.02A1 1 0 0 0 11 14z"/></svg>'
SVG_BOT     = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect width="18" height="14" x="3" y="7" rx="3" ry="3"/><path d="M12 7V3"/><path d="M15 3h-6"/><circle cx="9" cy="13" r="0.8" fill="currentColor"/><circle cx="15" cy="13" r="0.8" fill="currentColor"/><path d="M10 17h4"/></svg>'
SVG_SPARKLE = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M9.937 15.5A2 2 0 0 0 8.5 14.063l-6.135-1.582a.5.5 0 0 1 0-.962L8.5 9.936A2 2 0 0 0 9.937 8.5l1.582-6.135a.5.5 0 0 1 .963 0L14.063 8.5A2 2 0 0 0 15.5 9.937l6.135 1.581a.5.5 0 0 1 0 .964L15.5 14.063a2 2 0 0 0-1.437 1.437l-1.582 6.135a.5.5 0 0 1-.963 0z"/><path d="M20 3v4"/><path d="M22 5h-4"/></svg>'
SVG_USERS   = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>'
SVG_ARROW   = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>'

# ─────────────────────────────────────────────────────────────
# Global design system — "Aurora" refresh
# ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
    --bg-0: #07070A;
    --bg-1: #0C0C12;
    --bg-2: #11121A;
    --line: #1E1F2A;
    --line-soft: #15161F;
    --line-strong: #2A2C3A;

    --ink-100: #F4F5FA;
    --ink-70:  #B8BAC8;
    --ink-50:  #8A8C99;
    --ink-30:  #5B5D6A;

    --accent: #7C84E8;
    --accent-soft: rgba(124, 132, 232, 0.16);
    --accent-glow: rgba(124, 132, 232, 0.42);

    --c-blue:   #60A5FA;
    --c-purple: #A78BFA;
    --c-amber:  #FBBF24;
    --c-teal:   #2DD4BF;
    --c-rose:   #FB7185;
    --c-orange: #FB923C;

    --radius-card: 18px;
    --radius-btn:  10px;
    --shadow-sm: 0 1px 2px rgba(0,0,0,0.4);
    --shadow-md: 0 8px 24px rgba(0,0,0,0.45);
    --shadow-glow: 0 0 0 1px rgba(124,132,232,0.25), 0 12px 40px rgba(124,132,232,0.18);
}

*, *::before, *::after {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    -webkit-font-smoothing: antialiased;
}
code, pre, .stCode { font-family: 'JetBrains Mono', monospace !important; }

/* Global background — subtle aurora */
.stApp {
    background:
        radial-gradient(1200px 700px at 8% -10%, rgba(124,132,232,0.13), transparent 60%),
        radial-gradient(1100px 700px at 110% 110%, rgba(45, 212, 191, 0.10), transparent 60%),
        radial-gradient(900px 500px at 50% 120%, rgba(167,139,250,0.06), transparent 60%),
        var(--bg-0);
    color: var(--ink-100);
}

[data-testid="stHeader"] { background: transparent; }

/* Sidebar polish */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, var(--bg-1) 0%, var(--bg-0) 100%);
    border-right: 1px solid var(--line);
}
[data-testid="stSidebar"] hr {
    border-color: var(--line-soft) !important;
    margin: 0.7rem 0 !important;
}

/* Headings tighter */
h1, h2, h3 {
    letter-spacing: -0.6px;
    font-weight: 700;
    color: var(--ink-100);
}

/* Hero */
.hero-wrap {
    position: relative;
    text-align: center;
    padding: 2.4rem 1rem 2rem;
    margin-bottom: 1.4rem;
}
.hero-eyebrow {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 6px 14px;
    background: var(--accent-soft);
    border: 1px solid rgba(124,132,232,0.32);
    border-radius: 999px;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 1.2px;
    text-transform: uppercase;
    color: var(--accent);
    box-shadow: var(--shadow-sm);
    margin-bottom: 1rem;
}
.hero-eyebrow .dot {
    width: 6px; height: 6px; border-radius: 50%;
    background: #2DD4BF;
    box-shadow: 0 0 8px rgba(45,212,191,0.8);
    animation: pulse 2.4s ease-in-out infinite;
}
@keyframes pulse {
    0%, 100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.55; transform: scale(0.85); }
}
.hero-title {
    font-size: clamp(2.2rem, 5vw, 3.4rem);
    font-weight: 800;
    letter-spacing: -1.8px;
    line-height: 1.05;
    margin: 0 0 0.7rem;
    background: linear-gradient(135deg, #FFFFFF 0%, #B8BAC8 60%, #7C84E8 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.hero-subtitle {
    color: var(--ink-50);
    font-size: 1rem;
    max-width: 580px;
    margin: 0 auto 1.4rem;
    line-height: 1.55;
}
.hero-stats {
    display: inline-flex;
    gap: 22px;
    padding: 8px 18px;
    background: var(--bg-2);
    border: 1px solid var(--line);
    border-radius: 999px;
    font-size: 0.78rem;
    color: var(--ink-70);
    box-shadow: var(--shadow-sm);
}
.hero-stats span { display: inline-flex; align-items: center; gap: 6px; }
.hero-stats b { color: var(--ink-100); font-weight: 600; }
.hero-stats em { color: var(--ink-30); font-style: normal; }

/* Section headers */
.section-h {
    display: flex; align-items: baseline; gap: 12px;
    margin: 1.4rem 0 0.9rem;
}
.section-h h3 {
    font-size: 0.78rem;
    text-transform: uppercase;
    letter-spacing: 2px;
    color: var(--ink-50);
    font-weight: 600;
    margin: 0;
}
.section-h .line {
    flex: 1;
    height: 1px;
    background: linear-gradient(90deg, var(--line) 0%, transparent 100%);
}

/* Feature cards */
.fcard {
    position: relative;
    background: linear-gradient(180deg, var(--bg-2) 0%, var(--bg-1) 100%);
    border: 1px solid var(--line);
    border-radius: var(--radius-card);
    padding: 22px 22px 18px;
    height: 100%;
    transition: transform 200ms ease, border-color 200ms ease, box-shadow 200ms ease;
    overflow: hidden;
}
.fcard::before {
    content: "";
    position: absolute;
    inset: 0;
    border-radius: var(--radius-card);
    padding: 1px;
    background: linear-gradient(135deg, transparent, var(--accent-glow));
    -webkit-mask: linear-gradient(#000 0 0) content-box, linear-gradient(#000 0 0);
    -webkit-mask-composite: xor;
            mask-composite: exclude;
    opacity: 0;
    transition: opacity 200ms ease;
    pointer-events: none;
}
.fcard:hover {
    transform: translateY(-2px);
    border-color: var(--line-strong);
    box-shadow: var(--shadow-md);
}
.fcard:hover::before { opacity: 1; }
.fc-icon {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 44px; height: 44px;
    border-radius: 12px;
    background: rgba(255,255,255,0.04);
    border: 1px solid var(--line);
    margin-bottom: 14px;
}
.fc-icon svg { width: 22px; height: 22px; }
.fc-title {
    font-size: 1.04rem;
    font-weight: 600;
    color: var(--ink-100);
    margin-bottom: 4px;
    letter-spacing: -0.3px;
}
.fc-desc {
    color: var(--ink-50);
    font-size: 0.86rem;
    line-height: 1.5;
    margin-bottom: 12px;
}
.fc-chip {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    font-size: 0.7rem;
    font-weight: 600;
    color: var(--ink-30);
    text-transform: uppercase;
    letter-spacing: 1.5px;
}
.fc-chip svg { width: 12px; height: 12px; }

/* Per-accent tint for icons */
.fc-blue   .fc-icon { color: var(--c-blue);   background: rgba(96,165,250,0.10); border-color: rgba(96,165,250,0.25); }
.fc-purple .fc-icon { color: var(--c-purple); background: rgba(167,139,250,0.10); border-color: rgba(167,139,250,0.25); }
.fc-amber  .fc-icon { color: var(--c-amber);  background: rgba(251,191,36,0.10);  border-color: rgba(251,191,36,0.25); }
.fc-teal   .fc-icon { color: var(--c-teal);   background: rgba(45,212,191,0.10);  border-color: rgba(45,212,191,0.25); }
.fc-rose   .fc-icon { color: var(--c-rose);   background: rgba(251,113,133,0.10); border-color: rgba(251,113,133,0.25); }
.fc-orange .fc-icon { color: var(--c-orange); background: rgba(251,146,60,0.10);  border-color: rgba(251,146,60,0.25); }

/* Primary Streamlit buttons under cards */
[data-testid="stBaseButton-secondary"], .stButton > button {
    background: rgba(124, 132, 232, 0.10) !important;
    color: var(--ink-100) !important;
    border: 1px solid rgba(124, 132, 232, 0.28) !important;
    border-radius: var(--radius-btn) !important;
    padding: 9px 14px !important;
    font-weight: 500 !important;
    font-size: 0.86rem !important;
    transition: all 180ms ease !important;
}
.stButton > button:hover {
    background: rgba(124, 132, 232, 0.18) !important;
    border-color: rgba(124, 132, 232, 0.55) !important;
    transform: translateY(-1px) !important;
}
.stButton > button:active { transform: translateY(0) !important; }

/* Collab card */
.collab-card {
    background: linear-gradient(135deg, rgba(124,132,232,0.10) 0%, rgba(45,212,191,0.06) 100%);
    border: 1px solid rgba(124,132,232,0.22);
    border-radius: var(--radius-card);
    padding: 26px 28px;
    position: relative;
    overflow: hidden;
}
.collab-card::after {
    content: "";
    position: absolute;
    top: -50%; right: -10%;
    width: 280px; height: 280px;
    background: radial-gradient(circle, rgba(124,132,232,0.16) 0%, transparent 70%);
    pointer-events: none;
}
.collab-icon {
    display: inline-flex;
    align-items: center; justify-content: center;
    width: 48px; height: 48px;
    border-radius: 14px;
    background: rgba(124,132,232,0.18);
    border: 1px solid rgba(124,132,232,0.30);
    color: var(--accent);
    margin-bottom: 12px;
}
.collab-icon svg { width: 24px; height: 24px; }
.collab-title { font-size: 1.16rem; font-weight: 700; margin-bottom: 6px; letter-spacing: -0.3px; }
.collab-desc { color: var(--ink-70); font-size: 0.9rem; line-height: 1.55; max-width: 420px; }

/* Status pills */
.engine-pills { display: flex; gap: 8px; flex-wrap: wrap; }
.epill {
    display: inline-flex;
    align-items: center; gap: 6px;
    padding: 4px 10px;
    background: var(--bg-2);
    border: 1px solid var(--line);
    border-radius: 999px;
    font-size: 0.72rem;
    color: var(--ink-70);
    font-weight: 500;
}
.epill .ok { width: 6px; height: 6px; border-radius: 50%; background: #2DD4BF; box-shadow: 0 0 6px rgba(45,212,191,0.8); }
.epill .no { width: 6px; height: 6px; border-radius: 50%; background: #FB7185; }

/* Mode header */
.mode-head {
    display: flex; align-items: center; gap: 14px;
    padding: 8px 0 6px;
    margin-bottom: 6px;
}
.mode-head .mh-icon {
    display: inline-flex;
    align-items: center; justify-content: center;
    width: 42px; height: 42px;
    border-radius: 12px;
    background: rgba(255,255,255,0.04);
    border: 1px solid var(--line);
}
.mode-head .mh-icon svg { width: 22px; height: 22px; }
.mode-head h2 {
    margin: 0; padding: 0; border: none;
    font-size: 1.6rem; line-height: 1.1;
}
.mode-head .mh-sub {
    color: var(--ink-50);
    font-size: 0.82rem;
    margin-top: 2px;
}

/* Subtle hr */
hr { border-color: var(--line) !important; }

/* Chat input refinement */
[data-testid="stChatInput"] textarea {
    background: var(--bg-2) !important;
    border-radius: 12px !important;
    border: 1px solid var(--line) !important;
}

/* Mobile */
@media (max-width: 768px) {
    .hero-title { font-size: 2rem; letter-spacing: -1px; }
    .hero-subtitle { font-size: 0.92rem; }
    .hero-stats { gap: 12px; font-size: 0.72rem; padding: 6px 12px; }
    .fcard { padding: 18px 16px 14px; }
    .fc-title { font-size: 0.98rem; }
    .fc-desc { font-size: 0.82rem; }
    .collab-card { padding: 20px; }
    .mode-head h2 { font-size: 1.3rem; }
}

/* — Card depth polish — */
.fcard {
    background:
        radial-gradient(120% 80% at 0% 0%, rgba(124,132,232,0.10) 0%, transparent 55%),
        linear-gradient(180deg, var(--bg-2) 0%, var(--bg-1) 100%) !important;
    box-shadow:
        inset 0 1px 0 rgba(255,255,255,0.03),
        0 8px 24px rgba(0,0,0,0.35) !important;
}
.fcard:hover {
    box-shadow:
        inset 0 1px 0 rgba(255,255,255,0.04),
        0 14px 40px rgba(0,0,0,0.5),
        0 0 0 1px rgba(124,132,232,0.22) !important;
}
.fc-icon {
    box-shadow:
        inset 0 0 0 1px rgba(255,255,255,0.03),
        0 6px 18px rgba(0,0,0,0.35);
}
.fc-blue   .fc-icon { box-shadow: inset 0 0 0 1px rgba(255,255,255,0.03), 0 6px 18px rgba(96,165,250,0.20); }
.fc-purple .fc-icon { box-shadow: inset 0 0 0 1px rgba(255,255,255,0.03), 0 6px 18px rgba(167,139,250,0.20); }
.fc-amber  .fc-icon { box-shadow: inset 0 0 0 1px rgba(255,255,255,0.03), 0 6px 18px rgba(251,191,36,0.18); }
.fc-teal   .fc-icon { box-shadow: inset 0 0 0 1px rgba(255,255,255,0.03), 0 6px 18px rgba(45,212,191,0.20); }
.fc-rose   .fc-icon { box-shadow: inset 0 0 0 1px rgba(255,255,255,0.03), 0 6px 18px rgba(251,113,133,0.20); }
.fc-orange .fc-icon { box-shadow: inset 0 0 0 1px rgba(255,255,255,0.03), 0 6px 18px rgba(251,146,60,0.20); }

/* Tighter CTA buttons under cards */
.stButton > button {
    font-size: 0.82rem !important;
    padding: 8px 14px !important;
    letter-spacing: 0.3px !important;
}
.stButton > button:hover {
    background: rgba(124,132,232,0.22) !important;
    box-shadow: 0 6px 18px rgba(124,132,232,0.20) !important;
}

/* Section header — slightly bigger label */
.section-h h3 { font-size: 0.74rem; letter-spacing: 2.4px; }
.section-h .line { background: linear-gradient(90deg, rgba(124,132,232,0.20) 0%, transparent 80%); }

/* Engine pills — a bit larger and slightly stronger contrast */
.epill { padding: 5px 11px; font-size: 0.74rem; }

/* Hero subtitle line-height */
.hero-subtitle { line-height: 1.6; }

</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# Sidebar
# ─────────────────────────────────────────────────────────────
sidebar_ui()


# ─────────────────────────────────────────────────────────────
# Navigation helpers
# ─────────────────────────────────────────────────────────────
def _go_mode(mode: str):
    st.session_state.current_mode = mode
    st.session_state.messages = []
    st.session_state.in_study_room = False


def _go_home():
    st.session_state.current_mode = None
    st.session_state.messages = []


def _safe_secret(name: str) -> str:
    """Read a secret without crashing when no secrets.toml is configured."""
    try:
        return st.secrets.get(name, "") if hasattr(st, "secrets") else ""
    except Exception:
        return ""


def _key_present(name: str) -> bool:
    return bool(os.getenv(name) or _safe_secret(name))


def _engine_pills_html() -> str:
    groq_ok = _key_present("GROQ_API_KEY")
    gemini_dead = bool(st.session_state.get("gemini_disabled"))
    gemini_ok = _key_present("GEMINI_API_KEY") and not gemini_dead
    pills = []
    pills.append(f'<span class="epill"><span class="{ "ok" if groq_ok else "no" }"></span>Groq</span>')
    pills.append(f'<span class="epill"><span class="{ "ok" if gemini_ok else "no" }"></span>Gemini</span>')
    return f'<div class="engine-pills">{"".join(pills)}</div>'


# ─────────────────────────────────────────────────────────────
# Home
# ─────────────────────────────────────────────────────────────
def show_home():
    """Polished landing dashboard."""

    # Hero
    st.markdown(f"""
    <div class="hero-wrap">
        <span class="hero-eyebrow"><span class="dot"></span>AI Study Suite · v2.0</span>
        <h1 class="hero-title">Learn faster.<br>Reason deeper.</h1>
        <div class="hero-subtitle">
            Six AI-powered tools — explain, visualize, quiz, revise, interview, refine.
            Routed across <b>Groq</b> and <b>Gemini</b> for the best of speed and reasoning.
        </div>
        <div class="hero-stats">
            <span><b>2</b><em>engines</em></span>
            <span><b>6</b><em>modes</em></span>
            <span><b>1</b><em>workspace</em></span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Status pills row
    pcol1, pcol2 = st.columns([3, 2])
    with pcol2:
        st.markdown(
            '<div style="display:flex;justify-content:flex-end;margin-bottom:0.4rem;">'
            + _engine_pills_html()
            + '</div>',
            unsafe_allow_html=True,
        )

    # Mode cards section
    st.markdown(
        '<div class="section-h"><h3>Choose a tool</h3><span class="line"></span></div>',
        unsafe_allow_html=True,
    )

    cards = [
        (SVG_BRAIN,   "Study & Understand",  "Deep explanations with structured breakdowns and worked examples.", "explainer",  "fc-blue"),
        (SVG_NODES,   "Visualize Concepts",  "Auto-generate flowcharts, mind maps, and system diagrams.",         "visualizer", "fc-purple"),
        (SVG_TARGET,  "Exam Preparation",    "Practice questions, mock tests, and instant evaluation.",            "quizzer",    "fc-amber"),
        (SVG_ZAP,     "Flashcards",          "Spaced-repetition decks generated from any topic or PDF.",           "flashcards", "fc-teal"),
        (SVG_BOT,     "Interview Practice",  "Role-specific behavioral and technical interview prep.",             "interview",  "fc-rose"),
        (SVG_SPARKLE, "Resume Review",       "AI critique of your resume with actionable improvements.",           "resume",     "fc-orange"),
    ]

    # Two rows of three
    for row_start in (0, 3):
        cols = st.columns(3, gap="medium")
        for i, (icon, title, desc, mode_key, klass) in enumerate(cards[row_start:row_start + 3]):
            with cols[i]:
                st.markdown(f"""
                <div class="fcard {klass}">
                    <span class="fc-icon">{icon}</span>
                    <div class="fc-title">{title}</div>
                    <div class="fc-desc">{desc}</div>
                </div>
                """, unsafe_allow_html=True)
                st.button(
                    f"Open  →",
                    key=f"open_{mode_key}",
                    on_click=_go_mode,
                    args=(mode_key,),
                    use_container_width=True,
                )

    # Collaborate section
    st.markdown("<div style='height:18px'></div>", unsafe_allow_html=True)
    st.markdown(
        '<div class="section-h"><h3>Study together</h3><span class="line"></span></div>',
        unsafe_allow_html=True,
    )

    rc1, rc2 = st.columns([3, 2], gap="medium")

    with rc1:
        st.markdown(f"""
        <div class="collab-card">
            <span class="collab-icon">{SVG_USERS}</span>
            <div class="collab-title">Live Study Rooms</div>
            <div class="collab-desc">
                Create or join a room with video, audio, and group chat. Share a 6-character code
                to invite classmates and tackle a topic together — with the same AI on standby.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with rc2:
        def _enter_creating_room():
            st.session_state.in_study_room = True

        st.button(
            "✨ Create new room",
            key="btn_create_room",
            on_click=_enter_creating_room,
            use_container_width=True,
        )

        join_code = st.text_input(
            "Join code",
            placeholder="6-char code · e.g. A1B2C3",
            max_chars=6,
            label_visibility="collapsed",
            key="quick_join_code_input",
        )

        def _enter_joining_room():
            if st.session_state.quick_join_code_input:
                st.session_state.in_study_room = True
                st.session_state.join_code_from_home = (
                    st.session_state.quick_join_code_input.upper()
                )

        st.button(
            "→ Join existing room",
            key="btn_join_room",
            on_click=_enter_joining_room,
            use_container_width=True,
        )

    # Tiny footer
    st.markdown(
        '<div style="text-align:center;margin-top:36px;padding:14px;'
        'font-size:0.72rem;color:var(--ink-30);">'
        '✦ Built with care · Streamlit · Groq · Gemini · '
        '<a href="https://github.com/Aditya0105singh" target="_blank" '
        'style="color:var(--ink-50);text-decoration:none;">@Aditya0105singh</a>'
        '</div>',
        unsafe_allow_html=True,
    )


# ─────────────────────────────────────────────────────────────
# Mode interface
# ─────────────────────────────────────────────────────────────
def show_mode_interface():
    mode = st.session_state.current_mode

    mode_meta = {
        "explainer":  (SVG_BRAIN,   "Study & Understand", "Plain-language explanations with structured breakdowns.", "var(--c-blue)"),
        "visualizer": (SVG_NODES,   "Visualize Concepts", "Auto-generate diagrams and flowcharts from any concept.", "var(--c-purple)"),
        "quizzer":    (SVG_TARGET,  "Exam Preparation",   "Generate, solve, and evaluate practice questions.",       "var(--c-amber)"),
        "flashcards": (SVG_ZAP,     "Flashcards",         "Spaced-repetition decks from any topic.",                 "var(--c-teal)"),
        "interview":  (SVG_BOT,     "Interview Practice", "Role-specific mock interviews with feedback.",            "var(--c-rose)"),
        "resume":     (SVG_SPARKLE, "Resume Review",      "Section-by-section critique tailored to your target.",    "var(--c-orange)"),
    }
    icon, title, sub, accent = mode_meta.get(
        mode, ("", "Study Mode", "Pick a tool from the dashboard.", "var(--accent)")
    )

    # Top bar: back button + title + engine pills
    top1, top2, top3 = st.columns([2, 14, 5], vertical_alignment="center")
    with top1:
        st.button("← Home", on_click=_go_home, use_container_width=True, key="mode_back")
    with top2:
        st.markdown(f"""
        <div class="mode-head">
            <span class="mh-icon" style="color:{accent}">{icon}</span>
            <div>
                <h2>{title}</h2>
                <div class="mh-sub">{sub}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    with top3:
        st.markdown(
            '<div style="display:flex;justify-content:flex-end;">'
            + _engine_pills_html()
            + '</div>',
            unsafe_allow_html=True,
        )

    # Response-depth selector
    st.session_state.answer_style = st.radio(
        "Response depth",
        ["Beginner Friendly", "Intermediate", "Advanced/Technical"],
        index=["Beginner Friendly", "Intermediate", "Advanced/Technical"].index(
            st.session_state.get("answer_style", "Beginner Friendly")
        ),
        horizontal=True,
        help="Adjust the depth and tone of the AI's response.",
    )

    st.markdown("<hr style='margin:0.6rem 0 0.8rem;'>", unsafe_allow_html=True)
    chat_interface(mode)


# ─────────────────────────────────────────────────────────────
# Router
# ─────────────────────────────────────────────────────────────
if st.session_state.in_study_room:
    tcol1, tcol2 = st.columns([1, 11], vertical_alignment="center")
    with tcol1:
        if st.button("← Home", use_container_width=True, key="room_back"):
            st.session_state.in_study_room = False
            st.session_state.current_room = None
            st.rerun()
    with tcol2:
        st.markdown(
            '<div style="font-size:0.86rem;color:var(--ink-50);">'
            'Live Study Rooms · share a code to collaborate'
            '</div>',
            unsafe_allow_html=True,
        )
    study_rooms_ui()
elif st.session_state.current_mode is None:
    show_home()
else:
    show_mode_interface()
