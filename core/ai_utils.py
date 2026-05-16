"""
core/ai_utils.py
================

Dual-LLM inference router for Study Copilot AI.

Backends:
  * Groq  (Llama 3)    - fast factual queries, low latency
  * Gemini (2.0 Flash) - deep reasoning, long-form, PDF analysis

Uses the new `google-genai` SDK (`from google import genai`) so it shares
the same Gemini client family as utils/ai_helper.py.

Public API:
    score_complexity(query)            -> "groq" | "gemini"
    show_model_badge(model, latency)   -> renders inline HTML badge
    update_token_tracker(...)          -> updates st.session_state.usage_stats
    stream_groq(prompt, history)       -> generator of text chunks
    stream_gemini(prompt, history)     -> generator of text chunks
    get_streamed_response(prompt, ...) -> full response string
"""

from __future__ import annotations

import os
import time
from typing import Generator, Iterable, List, Optional

import streamlit as st
from dotenv import load_dotenv

# ---------------------------------------------------------------------------
# Environment / API setup
# ---------------------------------------------------------------------------
load_dotenv()


def _get_key(name: str) -> Optional[str]:
    """Try env vars first, then st.secrets — matches utils/ai_helper.py behaviour."""
    val = os.getenv(name)
    if not val:
        try:
            if hasattr(st, "secrets") and name in st.secrets:
                val = st.secrets[name]
        except Exception:
            pass
    return val


GEMINI_API_KEY = _get_key("GEMINI_API_KEY")
GROQ_API_KEY = _get_key("GROQ_API_KEY")

# Gemini client (new google-genai SDK)
try:
    from google import genai  # type: ignore
    gemini_client = genai.Client(api_key=GEMINI_API_KEY) if GEMINI_API_KEY else None
except Exception:
    genai = None  # type: ignore
    gemini_client = None

# Groq client
try:
    from groq import Groq  # type: ignore
    groq_client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None
except Exception:
    Groq = None  # type: ignore
    groq_client = None

GEMINI_MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")
GROQ_MODEL_NAME = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")


# ---------------------------------------------------------------------------
# Complexity scoring
# ---------------------------------------------------------------------------
_FAST_KEYWORDS = ("define", "what is", "list", "who")
_DEEP_KEYWORDS = ("explain", "why", "compare", "analyze", "step by step", "derive")


def _extract_user_text(query: str) -> str:
    """If the prompt is wrapped with PDF/conversation context, score only the
    real user line. chat_ui formats prompts as `... \nUser: <real prompt>`."""
    if not query:
        return ""
    if "\nUser:" in query:
        return query.rsplit("\nUser:", 1)[-1].strip()
    return query.strip()


def score_complexity(query: str) -> str:
    """Pick which LLM should answer this query."""
    real = _extract_user_text(query)
    if not real:
        return "groq"

    q = real.lower()
    word_count = len(q.split())

    if word_count < 8:
        return "groq"
    if any(kw in q for kw in _FAST_KEYWORDS):
        return "groq"
    if any(kw in q for kw in _DEEP_KEYWORDS):
        return "gemini"
    if word_count > 20:
        return "gemini"
    return "groq"


# ---------------------------------------------------------------------------
# Model badge
# ---------------------------------------------------------------------------
def show_model_badge(model: str, latency_ms: float) -> None:
    """Render a small inline HTML badge showing which model answered."""
    latency = int(round(latency_ms))

    if model == "groq":
        bg = "linear-gradient(135deg, #F55036 0%, #FF7A45 100%)"
        text = f"⚡ Groq · Fast inference · {latency}ms"
    else:
        bg = "linear-gradient(135deg, #2563EB 0%, #4285F4 100%)"
        text = f"\U0001F9E0 Gemini · Deep reasoning · {latency}ms"

    html = (
        '<div style="display:inline-block;background:' + bg + ';color:#ffffff;'
        'padding:4px 10px;border-radius:999px;font-size:0.72rem;font-weight:600;'
        'letter-spacing:0.3px;margin:6px 0;box-shadow:0 2px 8px rgba(0,0,0,0.25);">'
        + text + '</div>'
    )
    st.markdown(html, unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Token / usage tracker
# ---------------------------------------------------------------------------
def _ensure_usage_stats() -> dict:
    if "usage_stats" not in st.session_state:
        st.session_state.usage_stats = {
            "total_queries": 0,
            "groq_calls": 0,
            "gemini_calls": 0,
            "total_input_tokens": 0,
            "total_output_tokens": 0,
            "avg_latency_ms": 0.0,
            "_latency_sum_ms": 0.0,
        }
    return st.session_state.usage_stats


def update_token_tracker(model: str, input_tokens: int, output_tokens: int, latency_ms: float) -> None:
    """Update the rolling session usage stats."""
    stats = _ensure_usage_stats()
    stats["total_queries"] += 1
    if model == "groq":
        stats["groq_calls"] += 1
    elif model == "gemini":
        stats["gemini_calls"] += 1
    stats["total_input_tokens"] += int(input_tokens or 0)
    stats["total_output_tokens"] += int(output_tokens or 0)
    stats["_latency_sum_ms"] = stats.get("_latency_sum_ms", 0.0) + float(latency_ms or 0)
    stats["avg_latency_ms"] = stats["_latency_sum_ms"] / stats["total_queries"]


# ---------------------------------------------------------------------------
# History helpers
# ---------------------------------------------------------------------------
def _tail_history(history: Optional[Iterable[dict]], n: int = 6) -> List[dict]:
    if not history:
        return []
    try:
        return list(history)[-n:]
    except TypeError:
        return []


def _history_to_groq_messages(history: Optional[Iterable[dict]]) -> List[dict]:
    out: List[dict] = []
    for m in _tail_history(history, 6):
        role = m.get("role", "user")
        if role not in ("user", "assistant", "system"):
            role = "user"
        out.append({"role": role, "content": str(m.get("content", ""))})
    return out


def _history_to_gemini_text(history: Optional[Iterable[dict]]) -> str:
    lines: List[str] = []
    for m in _tail_history(history, 6):
        role = m.get("role", "user").capitalize()
        lines.append(f"{role}: {m.get('content', '')}")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Streaming backends
# ---------------------------------------------------------------------------
def stream_gemini(prompt: str, history: Optional[Iterable[dict]] = None) -> Generator[str, None, None]:
    """Yield text chunks from Gemini using google-genai's streaming API."""
    if gemini_client is None or not GEMINI_API_KEY:
        yield "Gemini is not configured. Set GEMINI_API_KEY in your .env."
        return

    context = _history_to_gemini_text(history)
    full_prompt = f"{context}\n\nUser: {prompt}" if context else prompt

    try:
        # New google-genai SDK streaming
        stream = gemini_client.models.generate_content_stream(
            model=GEMINI_MODEL_NAME,
            contents=full_prompt,
        )
        for chunk in stream:
            text = getattr(chunk, "text", None)
            if text:
                yield text
    except Exception as e:
        # Fallback: non-streaming single shot
        try:
            response = gemini_client.models.generate_content(
                model=GEMINI_MODEL_NAME,
                contents=full_prompt,
            )
            text = getattr(response, "text", None)
            if text:
                yield text
                return
        except Exception:
            pass
        yield f"\n\nGemini error: {e}"


def stream_groq(prompt: str, history: Optional[Iterable[dict]] = None) -> Generator[str, None, None]:
    """Yield text chunks from Groq using its streaming API."""
    if groq_client is None or not GROQ_API_KEY:
        yield "Groq is not configured. Set GROQ_API_KEY in your .env."
        return

    messages = _history_to_groq_messages(history)
    messages.append({"role": "user", "content": prompt})

    try:
        completion = groq_client.chat.completions.create(
            model=GROQ_MODEL_NAME,
            messages=messages,
            stream=True,
        )
        for chunk in completion:
            try:
                delta = chunk.choices[0].delta.content
            except (AttributeError, IndexError):
                delta = None
            if delta:
                yield delta
    except Exception as e:
        yield f"\n\nGroq error: {e}"


# ---------------------------------------------------------------------------
# Main router
# ---------------------------------------------------------------------------
_QUOTA_PATTERNS = (
    "RESOURCE_EXHAUSTED",
    "quota exceeded",
    "exceeded your current quota",
    "429",
    "rate limit",
    "Please retry in",
)


def _looks_like_quota_error(text: str) -> bool:
    if not text:
        return False
    lower = text.lower()
    return any(p.lower() in lower for p in _QUOTA_PATTERNS)


def _drain(stream_fn, prompt, history, placeholder) -> List[str]:
    out: List[str] = []
    try:
        for piece in stream_fn(prompt, history=history):
            out.append(piece)
            placeholder.markdown("".join(out))
    except Exception as e:
        out.append(f"\n\nStreaming error: {e}")
        placeholder.markdown("".join(out))
    return out


def get_streamed_response(
    prompt: str,
    history: Optional[Iterable[dict]] = None,
    force_model: Optional[str] = None,
) -> str:
    """Pick a model, stream the response, render a badge, update token stats.

    Falls back from Gemini -> Groq automatically on quota / 429 errors, so a
    dead free-tier Gemini key never strands the user."""
    model = force_model if force_model in ("groq", "gemini") else score_complexity(prompt)

    placeholder = st.empty()
    start = time.time()

    stream_fn = stream_groq if model == "groq" else stream_gemini
    chunks = _drain(stream_fn, prompt, history, placeholder)
    response_text = "".join(chunks)

    # Auto-fallback: Gemini quota hit -> retry on Groq
    if model == "gemini" and _looks_like_quota_error(response_text) and groq_client is not None:
        try:
            st.toast("Gemini quota hit — falling back to Groq", icon="⚡")
        except Exception:
            pass
        placeholder.markdown("")
        chunks = _drain(stream_groq, prompt, history, placeholder)
        response_text = "".join(chunks)
        model = "groq"

    latency_ms = (time.time() - start) * 1000.0
    show_model_badge(model, latency_ms)

    input_tokens = len(prompt.split()) if prompt else 0
    output_tokens = len(response_text.split()) if response_text else 0
    update_token_tracker(model, input_tokens, output_tokens, latency_ms)

    return response_text


# ---------------------------------------------------------------------------
# Back-compat shim
# ---------------------------------------------------------------------------
def get_llm_client(api_choice: str = "Groq"):
    """Legacy helper for older modules. Returns (client, label)."""
    choice = (api_choice or "").lower()
    if choice in ("gemini", "google"):
        if gemini_client is None:
            raise ValueError("Missing GEMINI_API_KEY in .env")
        return gemini_client, "Gemini"
    if choice in ("groq", "groq (free)", "llama", "llama3"):
        if groq_client is None:
            raise ValueError("Missing GROQ_API_KEY in .env")
        return groq_client, "Groq"
    raise ValueError("Invalid api_choice. Use 'Gemini' or 'Groq'.")
