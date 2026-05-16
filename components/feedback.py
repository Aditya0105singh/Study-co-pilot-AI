"""
components/feedback.py
======================

Per-message feedback (👍 / 👎) and chat-management helpers (clear, regenerate
hooks). Feedback is persisted to st.session_state.feedback_log so the user
can later review or export it.

Public API:
    feedback_row(message_index, on_copy=None, on_regen=None) -> None
    clear_chat_button(key="clear_chat") -> bool
    get_feedback_log() -> list[dict]
"""

from __future__ import annotations

from datetime import datetime
from typing import Callable, List, Optional

import streamlit as st


def _ensure_log() -> List[dict]:
    if "feedback_log" not in st.session_state:
        st.session_state.feedback_log = []
    return st.session_state.feedback_log


def get_feedback_log() -> List[dict]:
    return _ensure_log()


def _record(message_index: int, vote: str) -> None:
    log = _ensure_log()
    msgs = st.session_state.get("messages", [])
    snippet = ""
    if 0 <= message_index < len(msgs):
        snippet = str(msgs[message_index].get("content", ""))[:200]
    log.append({
        "ts": datetime.utcnow().isoformat() + "Z",
        "message_index": message_index,
        "vote": vote,
        "snippet": snippet,
    })
    st.session_state[f"_feedback_done_{message_index}"] = vote


def feedback_row(
    message_index: int,
    on_copy: Optional[Callable[[], None]] = None,
    on_regen: Optional[Callable[[], None]] = None,
) -> None:
    """Render a small action row under an assistant message."""
    already = st.session_state.get(f"_feedback_done_{message_index}")

    cols = st.columns([1, 1, 1, 1, 6])
    with cols[0]:
        if st.button("👍", key=f"fb_up_{message_index}",
                     help="Helpful", disabled=bool(already)):
            _record(message_index, "up")
            st.toast("Thanks for the feedback!", icon="✅")
    with cols[1]:
        if st.button("👎", key=f"fb_down_{message_index}",
                     help="Needs work", disabled=bool(already)):
            _record(message_index, "down")
            st.toast("Noted — we'll do better.", icon="📝")
    with cols[2]:
        if on_copy is not None and st.button("📋", key=f"fb_copy_{message_index}",
                                             help="Copy to clipboard hint"):
            on_copy()
    with cols[3]:
        if on_regen is not None and st.button("🔄", key=f"fb_regen_{message_index}",
                                              help="Regenerate"):
            on_regen()

    if already:
        with cols[4]:
            label = "👍 Helpful" if already == "up" else "👎 Needs work"
            st.caption(label)


def clear_chat_button(key: str = "clear_chat") -> bool:
    """
    Render a clear-chat button. Returns True if the chat was just cleared so
    the caller can also reset any mode-specific state.
    """
    if st.button("🧹 Clear chat", key=key, use_container_width=True):
        st.session_state.messages = []
        # Drop any pending streaming state too
        for k in list(st.session_state.keys()):
            if isinstance(k, str) and k.startswith(("_pending_", "_feedback_done_")):
                del st.session_state[k]
        st.toast("Chat cleared.", icon="🧼")
        return True
    return False
