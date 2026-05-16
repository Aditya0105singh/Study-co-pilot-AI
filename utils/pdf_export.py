"""
utils/pdf_export.py
===================

Export chat / study notes as a downloadable PDF.

Public API:
    export_chat_as_pdf(messages, title="Study Notes") -> bytes
    add_pdf_download_button(messages, filename="study_notes.pdf") -> None
"""

from __future__ import annotations

from datetime import datetime
from typing import Iterable, List, Optional

import streamlit as st
from fpdf import FPDF


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def _sanitize(text: str) -> str:
    """
    fpdf2's default core fonts only support a Latin-1 subset, so strip / replace
    characters that can't be encoded (emojis, smart quotes, em-dashes, etc.).
    """
    if text is None:
        return ""
    replacements = {
        "—": "-", "–": "-", "•": "*", "→": "->", "←": "<-",
        "“": '"', "”": '"', "’": "'", "‘": "'", "…": "...",
        "©": "(c)", "®": "(R)", "™": "(TM)",
    }
    for src, dst in replacements.items():
        text = text.replace(src, dst)
    # Drop anything still outside Latin-1
    return text.encode("latin-1", "replace").decode("latin-1")


def _role_label(role: str) -> str:
    role = (role or "").lower()
    if role == "user":
        return "You"
    if role in ("assistant", "ai", "bot"):
        return "Copilot"
    return role.capitalize() or "Note"


# ---------------------------------------------------------------------------
# PDF builder
# ---------------------------------------------------------------------------
class _NotesPDF(FPDF):
    def __init__(self, title: str):
        super().__init__()
        self._doc_title = _sanitize(title)
        self.set_auto_page_break(auto=True, margin=15)
        self.set_margins(15, 15, 15)

    def header(self):  # noqa: D401 - fpdf API
        # Only render header on pages 2+
        if self.page_no() == 1:
            return
        self.set_font("Helvetica", "I", 9)
        self.set_text_color(120, 120, 120)
        self.cell(0, 8, self._doc_title, ln=1, align="R")
        self.set_text_color(0, 0, 0)

    def footer(self):  # noqa: D401
        self.set_y(-12)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 8, f"Page {self.page_no()}", align="C")
        self.set_text_color(0, 0, 0)


def export_chat_as_pdf(messages: Iterable[dict], title: str = "Study Notes") -> bytes:
    """
    Build a PDF from a list of {"role", "content"} message dicts.

    Returns the PDF as raw bytes.
    """
    pdf = _NotesPDF(title)
    pdf.add_page()

    # ── Title ────────────────────────────────────────────────
    pdf.set_font("Helvetica", "B", 20)
    pdf.set_text_color(20, 20, 20)
    pdf.multi_cell(0, 10, _sanitize(title))
    pdf.ln(1)

    # ── Generated stamp ─────────────────────────────────────
    pdf.set_font("Helvetica", "I", 10)
    pdf.set_text_color(120, 120, 120)
    stamp = datetime.now().strftime("Generated on %B %d, %Y at %H:%M")
    pdf.cell(0, 6, _sanitize(stamp), ln=1)
    pdf.set_text_color(0, 0, 0)

    # Separator
    pdf.ln(3)
    pdf.set_draw_color(200, 200, 200)
    y = pdf.get_y()
    pdf.line(15, y, 195, y)
    pdf.ln(5)

    # ── Messages ────────────────────────────────────────────
    msg_list = list(messages or [])
    if not msg_list:
        pdf.set_font("Helvetica", "I", 11)
        pdf.set_text_color(120, 120, 120)
        pdf.multi_cell(0, 7, "No messages to export yet.")
    else:
        for msg in msg_list:
            role = _role_label(msg.get("role", "user"))
            content = _sanitize(str(msg.get("content", "")).strip())
            if not content:
                continue

            # Role label
            pdf.set_font("Helvetica", "B", 11)
            if role == "You":
                pdf.set_text_color(33, 102, 220)
            else:
                pdf.set_text_color(0, 140, 110)
            pdf.cell(0, 7, f"{role}:", ln=1)

            # Message body
            pdf.set_font("Helvetica", "", 11)
            pdf.set_text_color(40, 40, 40)
            pdf.multi_cell(0, 6, content)

            # Spacing between messages
            pdf.ln(3)

    # fpdf2 returns bytearray; cast to bytes for Streamlit
    out = pdf.output(dest="S")
    if isinstance(out, (bytes, bytearray)):
        return bytes(out)
    # Older fpdf versions return str
    return out.encode("latin-1", "replace")  # type: ignore[union-attr]


# ---------------------------------------------------------------------------
# Streamlit download button
# ---------------------------------------------------------------------------
def add_pdf_download_button(
    messages: Iterable[dict],
    filename: str = "study_notes.pdf",
    title: str = "Study Notes",
    label: str = "📥 Export Notes as PDF",
    key: Optional[str] = None,
) -> None:
    """Render a Streamlit download button that exports the messages as a PDF."""
    try:
        pdf_bytes = export_chat_as_pdf(messages, title=title)
    except Exception as e:
        st.warning(f"Could not build PDF: {e}")
        return

    st.download_button(
        label=label,
        data=pdf_bytes,
        file_name=filename,
        mime="application/pdf",
        key=key,
    )
