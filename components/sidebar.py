import streamlit as st
import os
import json
from dotenv import load_dotenv
from pathlib import Path
from components.pomodoro import pomodoro_timer

# Load .env so we can check which keys exist
_env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=_env_path)


def sidebar_ui():
    """Sidebar with model selector and tools - Premium Dark theme."""

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
    # Auto-routing pseudo-engine that uses both Groq + Gemini via core.ai_utils
    available_models.insert(0, "Auto (Dual-LLM)")

    if not available_models:
        available_models = ["Gemini"]  # fallback label

    st.session_state.api_choice = st.sidebar.selectbox(
        "AI Engine",
        available_models,
        index=0,
        help="Auto routes each query to Groq or Gemini based on complexity. Choose a single engine to force it.",
    )

    # Mode helpers always run with their specialised prompts; streaming
    # is wired through individual mode pipelines so no global toggle here.
    st.session_state.streaming_enabled = False

    # Model badge
    model_map = {
        "Gemini": ("Gemini 2.0 Flash", "rgba(33, 136, 255, 0.9)"),
        "Groq (Free)": ("Llama-3.3", "rgba(0, 176, 155, 0.9)"),
        "Grok (xAI)": ("Grok-2", "rgba(129, 98, 250, 0.9)"),
        "Auto (Dual-LLM)": ("Groq + Gemini", "rgba(245, 80, 54, 0.9)"),
    }
    model_name, model_color = model_map.get(
        st.session_state.api_choice, ("Unknown", "rgba(128,128,128,0.8)")
    )
    st.sidebar.markdown(f"""
    <div style="background: #0A0A0A; border: 1px solid #222222; border-radius: 8px; padding: 8px 12px; margin: 8px 0;">
        <div style="font-size: 0.65rem; color: #888; text-transform: uppercase; letter-spacing: 1px; font-weight: 600;">Active Model</div>
        <div style="font-size: 0.85rem; color: {model_color}; font-weight: 500; margin-top: 2px;">+ {model_name}</div>
    </div>
    """, unsafe_allow_html=True)

    from components.pdf_handler import handle_pdf_upload

    st.sidebar.markdown("---")

    # Universal PDF Uploader
    handle_pdf_upload()

    # Voice input (Groq Whisper)
    if os.getenv("GROQ_API_KEY"):
        with st.sidebar.expander("🎙️ Voice input", expanded=False):
            try:
                from components.voice_input import voice_to_text
                spoken = voice_to_text(key="sidebar_voice")
                if spoken:
                    st.session_state.voice_prompt = spoken
                    st.toast("Voice captured — sent to chat input.", icon="🎤")
            except Exception as e:
                st.caption(f"Voice unavailable: {e}")

    # Session import
    with st.sidebar.expander("💾 Sessions", expanded=False):
        uploaded = st.file_uploader("Load saved session (.json)", type=["json"], key="session_loader")
        if uploaded is not None:
            try:
                from utils.session_export import import_chat_from_json
                msgs = import_chat_from_json(uploaded)
                if msgs:
                    st.session_state.messages = msgs
                    st.success(f"Loaded {len(msgs)} messages.")
                else:
                    st.warning("File did not contain a valid session.")
            except Exception as e:
                st.warning(f"Could not load session: {e}")

        if st.button("🧹 Clear current chat", key="sidebar_clear_chat", use_container_width=True):
            st.session_state.messages = []
            for k in list(st.session_state.keys()):
                if isinstance(k, str) and k.startswith(("_pending_", "_feedback_done_")):
                    del st.session_state[k]
            st.toast("Chat cleared.", icon="🧼")
            st.rerun()

    st.sidebar.markdown("---")

    # Focus Tool
    pomodoro_timer()

    # Gemini circuit-breaker status ----------------------------------------
    if st.session_state.get("gemini_disabled"):
        st.sidebar.markdown("---")
        st.sidebar.warning(
            "🧠 Gemini disabled this session (quota hit). All Auto queries route to Groq.",
            icon="⚠️",
        )
        if st.sidebar.button("🔁 Retry Gemini", key="reset_gemini_breaker", use_container_width=True):
            st.session_state.pop("gemini_disabled", None)
            st.session_state.pop("gemini_disabled_reason", None)
            st.toast("Gemini re-enabled. Next deep query will retry.", icon="✅")
            st.rerun()

    # Session Stats ---------------------------------------------------------
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📊 Session Stats")
    try:
        stats = st.session_state.get("usage_stats")
        if not stats:
            st.sidebar.caption("No queries yet this session.")
        else:
            total_tokens = int(stats.get("total_input_tokens", 0)) + int(stats.get("total_output_tokens", 0))
            avg_latency = int(round(stats.get("avg_latency_ms", 0) or 0))

            col1, col2 = st.sidebar.columns(2)
            with col1:
                st.metric("Total Queries", stats.get("total_queries", 0))
                st.metric("Groq Calls (fast)", stats.get("groq_calls", 0))
                st.metric("Avg Latency (ms)", avg_latency)
            with col2:
                st.metric("Gemini Calls (deep)", stats.get("gemini_calls", 0))
                st.metric("Total Tokens Used", total_tokens)
    except Exception:
        st.sidebar.caption("Session stats unavailable.")
