import streamlit as st
from components.pdf_handler import handle_pdf_upload
from components.pomodoro import pomodoro_timer

def sidebar_ui():
    """Sidebar with model selector and tools — Premium Universal theme."""

    st.sidebar.markdown("""
    <div style="padding: 0.5rem 0 1rem;">
        <div style="font-size: 1.1rem; font-weight: 700; letter-spacing: -0.5px;">🎓 Copilot AI</div>
        <div style="font-size: 0.7rem; opacity: 0.7; margin-top: 2px;">Study Intelligence Suite</div>
    </div>
    """, unsafe_allow_html=True)

    st.session_state.api_choice = st.sidebar.selectbox(
        "AI Engine",
        ["Gemini", "Groq (Free)", "Grok (xAI)"],
        index=0,
        help="Select the AI model to use"
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

    # PDF Context indicator
    if st.session_state.get("pdf_content"):
        pdf_name = st.session_state.get('last_pdf_name', 'Document')
        st.sidebar.markdown(f"""
        <div style="background: rgba(33, 136, 255, 0.05); border: 1px solid rgba(33, 136, 255, 0.2); border-radius: 8px; padding: 8px 12px; margin: 8px 0;">
            <div style="font-size: 0.65rem; color: rgba(33, 136, 255, 0.9); text-transform: uppercase; letter-spacing: 1px; font-weight: 600;">📎 Document Loaded</div>
            <div style="font-size: 0.8rem; opacity: 0.7; margin-top: 2px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">{pdf_name}</div>
        </div>
        """, unsafe_allow_html=True)

    # Focus Tool
    pomodoro_timer()
