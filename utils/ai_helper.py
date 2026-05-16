import os
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI
from google import genai
import warnings
import time
from pathlib import Path

# Suppress warnings
warnings.filterwarnings("ignore", category=FutureWarning)

# Load .env from the project root (works regardless of CWD)
_env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=_env_path)

def get_api_key(key_name):
    """Retrieve API key from env or st.secrets."""
    key = os.getenv(key_name)
    if not key and hasattr(st, 'secrets'):
        key = st.secrets.get(key_name)
    return key

# Individual model generators for fallback reuse
def _mark_gemini_down(reason: str = "quota"):
    """Disable Gemini for the rest of the session so Auto skips it."""
    try:
        st.session_state["gemini_disabled"] = True
        st.session_state["gemini_disabled_reason"] = reason
    except Exception:
        pass


def _is_gemini_down() -> bool:
    try:
        return bool(st.session_state.get("gemini_disabled"))
    except Exception:
        return False


_QUOTA_TOKENS = ("429", "resource_exhausted", "quota exceeded",
                 "exceeded your current quota", "rate limit")


def try_gemini(prompt: str):
    api_key = get_api_key("GEMINI_API_KEY")
    if not api_key: return None, "❌ Gemini API Key missing"
    # Session-level circuit breaker: skip Gemini if it already failed with quota
    if _is_gemini_down():
        return None, "⚠️ Gemini disabled for this session (quota previously hit)"
    try:
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
        )
        if response and response.text:
            return response.text.strip(), None
        return None, "⚠️ Gemini: Empty response"
    except Exception as e:
        err = str(e)
        lower = err.lower()
        if any(tok in lower for tok in _QUOTA_TOKENS):
            _mark_gemini_down("quota")
            return None, "⚠️ Gemini daily free quota exceeded — falling back (disabled for session)"
        return None, f"❌ Gemini Error: {err}"

def try_grok(prompt: str):
    api_key = get_api_key("XAI_API_KEY")
    if not api_key: return None, "❌ xAI API Key missing"
    try:
        client = OpenAI(api_key=api_key, base_url="https://api.x.ai/v1")
        response = client.chat.completions.create(
            model="grok-2-latest",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip(), None
    except Exception as e:
        return None, f"❌ Grok Error: {str(e)}"

def try_groq(prompt: str):
    api_key = get_api_key("GROQ_API_KEY")
    if not api_key: return None, "❌ Groq API Key missing"
    try:
        client = OpenAI(api_key=api_key, base_url="https://api.groq.com/openai/v1")
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip(), None
    except Exception as e:
        return None, f"❌ Groq Error: {str(e)}"

def generate_response(prompt: str) -> str:
    """Generate response with an intelligent fallback system for high availability."""
    # Map the session_state value to the generator function
    generators = {
        "Gemini":     try_gemini,
        "Grok (xAI)": try_grok,
        "Groq (Free)": try_groq,
        # aliases just in case
        "Groq":       try_groq,
        "Grok":       try_grok,
    }

    primary_choice = st.session_state.get("api_choice", "Groq (Free)")

    # Auto (Dual-LLM): pick Groq vs Gemini per query via complexity scoring.
    if primary_choice == "Auto (Dual-LLM)":
        try:
            from core.ai_utils import score_complexity
            picked = score_complexity(prompt)
        except Exception:
            picked = "groq"
        # Honour the circuit breaker — if Gemini already died this session,
        # silently route every Auto query to Groq instead of paying a wasted
        # round-trip per message.
        if picked == "gemini" and _is_gemini_down():
            picked = "groq"
        primary_choice = "Gemini" if picked == "gemini" else "Groq (Free)"

    # Try primary choice first
    gen_fn = generators.get(primary_choice, try_groq)
    res, err = gen_fn(prompt)
    if res:
        return res

    # If primary fails, log the error and try others as fallback
    st.toast(f"Fallback: {primary_choice} failed. Trying backup...", icon="⚠️")

    # Fallback order — Groq first (14,400 req/day free), then Gemini, then Grok
    fallback_order = ["Groq (Free)", "Gemini", "Grok (xAI)"]
    for model_name in fallback_order:
        if model_name == primary_choice:
            continue
        fn = generators.get(model_name)
        if not fn:
            continue
        res, err = fn(prompt)
        if res:
            st.toast(f"✅ Recovered using {model_name}!", icon="✨")
            return res

    # If everything fails
    return f"❌ All AI models failed. Please check your API keys and network connection. Last error: {err}"

