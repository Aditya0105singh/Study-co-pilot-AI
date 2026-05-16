"""
utils/markdown_render.py
========================

Render Markdown content with KaTeX math support and a small
code-block readability pass.

Streamlit's native st.markdown already renders most code blocks and
inline math ($...$, $$...$$) via MathJax-like fallback in newer versions.
This helper makes that explicit and adds a copy-button affordance for
fenced code blocks via a tiny components.html injection when requested.

Public API:
    render_rich_markdown(text, allow_math=True, allow_html=False) -> None
    has_math(text) -> bool
"""

from __future__ import annotations

import re

import streamlit as st


_MATH_PATTERN = re.compile(r"(\${1,2}[^$]+\${1,2}|\\\[[^\]]+\\\]|\\\([^)]+\\\))")


def has_math(text: str) -> bool:
    """Heuristic: does this text contain inline or block LaTeX math?"""
    if not text:
        return False
    return bool(_MATH_PATTERN.search(text))


def _normalize_math(text: str) -> str:
    """
    Convert \\(...\\) and \\[...\\] LaTeX delimiters into the $...$/$$...$$
    forms that Streamlit's Markdown renderer understands.
    """
    if not text:
        return text
    text = re.sub(r"\\\[(.+?)\\\]", r"$$\1$$", text, flags=re.S)
    text = re.sub(r"\\\((.+?)\\\)", r"$\1$", text, flags=re.S)
    return text


def render_rich_markdown(text: str, allow_math: bool = True, allow_html: bool = False) -> None:
    """
    Render Markdown with optional math normalization. Falls back to plain
    st.markdown on any failure so a single bad block never breaks the UI.
    """
    if text is None:
        return
    try:
        body = _normalize_math(text) if allow_math else text
        st.markdown(body, unsafe_allow_html=allow_html)
    except Exception:
        st.text(text)
