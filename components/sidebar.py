import streamlit as st
import os
from dotenv import load_dotenv
from pathlib import Path
from components.pomodoro import pomodoro_timer

# Load .env so we can check which keys exist
_env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=_env_path)

def sidebar_ui():
    """Sidebar with model selector and tools — Premium Dark theme."""

    st.sidebar.markdown("""
    <div style="padding: 0.5rem 0 1rem;">
        <div style="display: flex; align-items: center; gap: 8px; font-size: 1.1rem; font-weight: 700; letter-spacing: -0.5px;">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#5E6AD2" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" style="filter: drop-shadow(0 0 6px rgba(94, 106, 210, 0.6));">
                <path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/>
                <polyline points="3.27 6.96 12 12.01 20.73 6.96"/>
                <line x1="12" y1="22.08" x2="12" y2="12"/>
            </svg>
            Copilot AI
        </div>
        <div style="font-size: 0.7rem; opacity: 0.7; margin-top: 2px;">Study Intelligence Suite</div>
    </div>
    """, unsafe_allow_html=True)

    # Only show models that have a valid API key in .env
    # We put Groq first so it's the default, since it has much higher free limits (14,400 req/day)
    available_models = []
    if os.getenv("GROQ_API_KEY"):
        available_models.append("Groq (Free)")
    if os.getenv("GEMINI_API_KEY"):
        available_models.append("Gemini")
    if os.getenv("XAI_API_KEY"):
        available_models.append("Grok (xAI)")

    if not available_models:
        available_models = ["Gemini"]  # fallback label

    st.session_state.api_choice = st.sidebar.selectbox(
        "AI Engine",
        available_models,
        index=0,
        help="Only models with valid API keys are shown"
    )

    # Model badge
    model_map = {"Gemini": ("Gemini 2.0 Flash", "rgba(33, 136, 255, 0.9)"), "Groq (Free)": ("Llama-3.3", "rgba(0, 176, 155, 0.9)"), "Grok (xAI)": ("Grok-2", "rgba(129, 98, 250, 0.9)")}
    model_name, model_color = model_map.get(st.session_state.api_choice, ("Unknown", "rgba(128,128,128,0.8)"))
    st.sidebar.markdown(f"""
    <div style="background: #0A0A0A; border: 1px solid #222222; border-radius: 8px; padding: 8px 12px; margin: 8px 0;">
        <div style="font-size: 0.65rem; color: #888; text-transform: uppercase; letter-spacing: 1px; font-weight: 600;">Active Model</div>
        <div style="font-size: 0.85rem; color: {model_color}; font-weight: 500; margin-top: 2px;">✦ {model_name}</div>
    </div>
    """, unsafe_allow_html=True)

    from components.pdf_handler import handle_pdf_upload
    
    st.sidebar.markdown("---")
    
    # Universal PDF Uploader
    handle_pdf_upload()
    
    st.sidebar.markdown("---")

    # Focus Tool
    pomodoro_timer()
