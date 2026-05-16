"""
utils/pdf_export.py
===================

Export chat / study notes as a polished, downloadable PDF.

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
    fpdf2's core fonts cover Latin-1 only, so strip / replace characters that
    can't be encoded (emojis, smart quotes, em-dashes, etc.).
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
    return text.encode("latin-1", "replace").decode("latin-1")


def _role_label(role: str) -> str:
    role = (role or "").lower()
    if role == "user":
        return "You"
    if role in ("assistant", "ai", "bot"):
        return "Copilot"
    return role.capitalize() or "Note"


# ---------------------------------------------------------------------------
# Brand colors (kept dim so prints clean)
# ---------------------------------------------------------------------------
BRAND_PRIMARY = (94, 106, 210)      # #5E6AD2
BRAND_USER = (33, 102, 220)         # blue
BRAND_BOT = (0, 140, 110)           # teal-green
INK = (28, 28, 32)
INK_MUTED = (118, 118, 130)
RULE = (220, 220, 226)


# ---------------------------------------------------------------------------
# PDF builder
# ---------------------------------------------------------------------------
class _NotesPDF(FPDF):
    def __init__(self, title: str):
        super().__init__()
        self._doc_title = _sanitize(title)
        self.set_auto_page_break(auto=True, margin=18)
        self.set_margins(18, 18, 18)

    def header(self):  # noqa: D401 - fpdf API
        if self.page_no() == 1:
            return
        # Subtle running header on continuation pages
        self.set_font("Helvetica", "I", 9)
        self.set_text_color(*INK_MUTED)
        self.cell(0, 8, self._doc_title, ln=1, align="R")
        self.set_draw_color(*RULE)
        y = self.get_y()
        self.line(18, y, 192, y)
        self.ln(3)
        self.set_text_color(*INK)

    def footer(self):  # noqa: D401
        self.set_y(-14)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(*INK_MUTED)
        self.cell(0, 8, f"Study Copilot AI  ·  Page {self.page_no()}", align="C")
        self.set_text_color(*INK)


def _render_block(pdf: FPDF, content: str) -> None:
    """Render content respecting fenced code blocks (mono font, light bg)."""
    lines = content.splitlines() or [""]
    in_code = False
    code_buffer: List[str] = []

    usable_w = pdf.w - pdf.l_margin - pdf.r_margin

    def reset_x():
        pdf.set_x(pdf.l_margin)

    def flush_code():
        if not code_buffer:
            return
        pdf.set_fill_color(245, 245, 248)
        pdf.set_font("Courier", "", 9.5)
        pdf.set_text_color(50, 50, 70)
        for code_line in code_buffer:
            reset_x()
            pdf.multi_cell(usable_w, 5, _sanitize(code_line) or " ", fill=True)
        pdf.set_text_color(*INK)
        pdf.set_font("Helvetica", "", 11)
        pdf.ln(2)

    for raw in lines:
        line = raw.rstrip()
        if line.strip().startswith("```"):
            if in_code:
                flush_code()
                code_buffer = []
                in_code = False
            else:
                in_code = True
            continue
        if in_code:
            code_buffer.append(line)
            continue

        reset_x()
        if line.startswith(("- ", "* ")):
            indent = 4
            pdf.set_x(pdf.l_margin + indent)
            pdf.multi_cell(usable_w - indent, 6, _sanitize("- " + line[2:]))
        elif line.startswith("#"):
            level = min(line.count("#", 0, 6), 4)
            size = {1: 14, 2: 13, 3: 12, 4: 11}.get(level, 11)
            heading = line.lstrip("# ").strip()
            pdf.set_font("Helvetica", "B", size)
            pdf.multi_cell(usable_w, 6 + (4 - level), _sanitize(heading) or " ")
            pdf.set_font("Helvetica", "", 11)
        else:
            pdf.multi_cell(usable_w, 6, _sanitize(line) if line else " ")

    if in_code and code_buffer:
        flush_code()


def export_chat_as_pdf(messages: Iterable[dict], title: str = "Study Notes") -> bytes:
    """Build a polished PDF from a list of {"role", "content"} message dicts."""
    pdf = _NotesPDF(title)
    pdf.add_page()

    # Usable inner width
    usable_w = pdf.w - pdf.l_margin - pdf.r_margin

    # ── Brand strip ─────────────────────────────────────────
    pdf.set_fill_color(*BRAND_PRIMARY)
    pdf.rect(0, 0, pdf.w, 6, "F")
    pdf.set_xy(pdf.l_margin, 14)

    # ── Title ───────────────────────────────────────────────
    pdf.set_font("Helvetica", "B", 22)
    pdf.set_text_color(*INK)
    pdf.cell(usable_w, 10, _sanitize(title), ln=1)

    # ── Subtitle ────────────────────────────────────────────
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(*INK_MUTED)
    stamp = datetime.now().strftime("%B %d, %Y at %H:%M")
    pdf.cell(usable_w, 6, _sanitize(f"Generated by Study Copilot AI  -  {stamp}"), ln=1)

    # Separator
    pdf.ln(2)
    pdf.set_draw_color(*RULE)
    y = pdf.get_y()
    pdf.line(18, y, 192, y)
    pdf.ln(6)

    # ── Messages ────────────────────────────────────────────
    msg_list = list(messages or [])
    if not msg_list:
        pdf.set_font("Helvetica", "I", 11)
        pdf.set_text_color(*INK_MUTED)
        pdf.multi_cell(0, 7, "No messages to export yet.")
    else:
        for msg in msg_list:
            role = _role_label(msg.get("role", "user"))
            content = str(msg.get("content", "")).strip()
            if not content:
                continue

            # Role chip
            pdf.set_font("Helvetica", "B", 11)
            color = BRAND_USER if role == "You" else BRAND_BOT
            pdf.set_text_color(*color)
            pdf.cell(0, 7, _sanitize(role), ln=1)

            # Message body
            pdf.set_font("Helvetica", "", 11)
            pdf.set_text_color(*INK)
            _render_block(pdf, content)

            # Spacing
            pdf.ln(4)

    out = pdf.output(dest="S")
    if isinstance(out, (bytes, bytearray)):
        return bytes(out)
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
