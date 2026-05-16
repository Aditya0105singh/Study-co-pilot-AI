"""
utils/session_export.py
=======================

Export the chat session in lightweight formats:
  * Markdown (.md)    - human-readable notes
  * JSON     (.json)  - re-importable session snapshot

Public API:
    export_chat_as_markdown(messages, title="Study Notes") -> str
    export_chat_as_json(messages, meta=None)               -> str
    add_markdown_download(messages, filename, key)         -> Streamlit button
    add_json_download(messages, filename, key)             -> Streamlit button
    import_chat_from_json(uploaded_file)                   -> list[dict]
"""

from __future__ import annotations

import json
from datetime import datetime
from typing import Iterable, List, Optional

import streamlit as st


# ---------------------------------------------------------------------------
# Markdown
# ---------------------------------------------------------------------------
def _role_label(role: str) -> str:
    role = (role or "").lower()
    if role == "user":
        return "🧑 You"
    if role in ("assistant", "ai", "bot"):
        return "🤖 Copilot"
    return role.capitalize() or "Note"


def export_chat_as_markdown(messages: Iterable[dict], title: str = "Study Notes") -> str:
    """Serialize chat messages to a clean Markdown document."""
    msgs = list(messages or [])
    stamp = datetime.now().strftime("%B %d, %Y at %H:%M")
    out: List[str] = [
        f"# {title}",
        "",
        f"_Exported from Study Copilot AI on {stamp}._",
        "",
        "---",
        "",
    ]
    if not msgs:
        out.append("> No messages to export yet.")
        return "\n".join(out)

    for m in msgs:
        label = _role_label(m.get("role", "user"))
        content = str(m.get("content", "")).strip()
        if not content:
            continue
        out.append(f"### {label}")
        out.append("")
        out.append(content)
        out.append("")
        out.append("---")
        out.append("")
    return "\n".join(out)


# ---------------------------------------------------------------------------
# JSON
# ---------------------------------------------------------------------------
def export_chat_as_json(messages: Iterable[dict], meta: Optional[dict] = None) -> str:
    """Serialize chat messages + optional meta to pretty JSON."""
    payload = {
        "app": "study-copilot-ai",
        "version": "2.0",
        "exported_at": datetime.utcnow().isoformat() + "Z",
        "meta": meta or {},
        "messages": list(messages or []),
    }
    return json.dumps(payload, indent=2, ensure_ascii=False)


def import_chat_from_json(uploaded_file) -> List[dict]:
    """Load a previously exported JSON session back into a messages list."""
    if uploaded_file is None:
        return []
    try:
        data = json.load(uploaded_file)
        if isinstance(data, dict) and "messages" in data:
            return list(data["messages"])
        if isinstance(data, list):
            return list(data)
    except Exception:
        return []
    return []


# ---------------------------------------------------------------------------
# Streamlit download buttons
# ---------------------------------------------------------------------------
def add_markdown_download(
    messages: Iterable[dict],
    filename: str = "study_notes.md",
    title: str = "Study Notes",
    label: str = "📝 Export as Markdown",
    key: Optional[str] = None,
) -> None:
    """Render a Streamlit download button for a Markdown chat export."""
    try:
        md = export_chat_as_markdown(messages, title=title)
    except Exception as e:
        st.warning(f"Could not build Markdown: {e}")
        return
    st.download_button(
        label=label,
        data=md.encode("utf-8"),
        file_name=filename,
        mime="text/markdown",
        key=key,
    )


def add_json_download(
    messages: Iterable[dict],
    filename: str = "study_session.json",
    meta: Optional[dict] = None,
    label: str = "💾 Save Session (JSON)",
    key: Optional[str] = None,
) -> None:
    """Render a Streamlit download button for a JSON chat export."""
    try:
        payload = export_chat_as_json(messages, meta=meta)
    except Exception as e:
        st.warning(f"Could not build JSON: {e}")
        return
    st.download_button(
        label=label,
        data=payload.encode("utf-8"),
        file_name=filename,
        mime="application/json",
        key=key,
    )
