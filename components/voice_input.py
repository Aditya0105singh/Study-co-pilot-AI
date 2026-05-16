"""
components/voice_input.py
=========================

Speech-to-text via Groq's Whisper-large-v3 endpoint.

Uses Streamlit's built-in st.audio_input (Streamlit >= 1.31) so the user
can record from the browser without any extra package. Falls back
gracefully if the runtime / API key is missing.

Public API:
    voice_to_text(key="voice")  -> Optional[str]
        Returns the transcribed text, or None.
"""

from __future__ import annotations

import io
import os
from typing import Optional

import streamlit as st


def _transcribe_with_groq(audio_bytes: bytes) -> Optional[str]:
    """Send the recording to Groq's whisper-large-v3 and return the text."""
    key = os.getenv("GROQ_API_KEY")
    if not key:
        return None
    try:
        from groq import Groq  # type: ignore
    except Exception:
        return None

    try:
        client = Groq(api_key=key)
        buf = io.BytesIO(audio_bytes)
        buf.name = "input.wav"  # Groq client uses the filename suffix
        result = client.audio.transcriptions.create(
            file=("input.wav", buf, "audio/wav"),
            model=os.getenv("GROQ_WHISPER_MODEL", "whisper-large-v3"),
        )
        text = getattr(result, "text", None) or (
            result.get("text") if isinstance(result, dict) else None
        )
        return text.strip() if text else None
    except Exception as e:
        st.warning(f"Voice transcription failed: {e}")
        return None


def voice_to_text(key: str = "voice", label: str = "🎙️ Record your question") -> Optional[str]:
    """
    Render a voice-input widget. Returns transcribed text once recording is
    finished and Whisper completes, otherwise returns None.
    """
    recorder = getattr(st, "audio_input", None)
    if recorder is None:
        st.caption("Voice input needs Streamlit >= 1.31. Update Streamlit to enable.")
        return None

    audio = recorder(label, key=key)
    if audio is None:
        return None

    # Streamlit's audio_input returns an UploadedFile-like object
    try:
        data = audio.getvalue() if hasattr(audio, "getvalue") else audio.read()
    except Exception:
        return None
    if not data:
        return None

    with st.spinner("Transcribing…"):
        text = _transcribe_with_groq(data)
    if text:
        st.success(f"Heard: \"{text}\"")
    else:
        st.info("Couldn't transcribe — try again or check GROQ_API_KEY.")
    return text
