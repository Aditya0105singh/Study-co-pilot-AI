"""
components/quick_actions.py
===========================

Per-mode suggestion chips shown on the chat empty state.
Clicking a chip prefills the next user prompt and triggers a rerun.

Public API:
    render_quick_actions(mode) -> Optional[str]
        Returns the picked suggestion (or None). Caller appends it to messages.
"""

from __future__ import annotations

from typing import List, Optional

import streamlit as st


SUGGESTIONS = {
    "explainer": [
        "Explain backpropagation like I'm 12",
        "What is the CAP theorem?",
        "Compare TCP vs UDP with examples",
        "Why does recursion work on trees?",
    ],
    "visualizer": [
        "Flowchart the HTTPS handshake",
        "Visualize a REST API request lifecycle",
        "Diagram a React component lifecycle",
        "Draw the OSI 7-layer model",
    ],
    "flashcards": [
        "10 flashcards on Operating Systems",
        "Flashcards from my uploaded PDF",
        "Quick deck on SQL JOIN types",
        "Top 15 Python built-ins as flashcards",
    ],
    "quizzer": [
        "Quiz me on Data Structures basics",
        "5 MCQs on linear algebra",
        "Mixed quiz: networking + DBMS",
        "Warm-up quiz on Python syntax",
    ],
    "interview": [
        "Mock backend developer interview",
        "Behavioral questions for a PM role",
        "System design: URL shortener",
        "Frontend deep dive: React hooks",
    ],
    "resume": [
        "Review my resume for ML Engineer roles",
        "Strengthen my impact bullets",
        "Tailor this resume for FAANG",
        "Find weak verbs and suggest replacements",
    ],
}


def _chips_for(mode: str) -> List[str]:
    return SUGGESTIONS.get(mode, [
        "Summarize the uploaded PDF",
        "Explain a concept I'm stuck on",
        "Quiz me on a topic of your choice",
    ])


def render_quick_actions(mode: str, key_prefix: str = "qa") -> Optional[str]:
    """Render quick-start chips. Returns the chosen suggestion text, or None."""
    chips = _chips_for(mode)
    if not chips:
        return None

    st.markdown(
        '<div style="text-align:center;margin:0.3rem 0 0.7rem;'
        'font-size:0.72rem;letter-spacing:1.5px;text-transform:uppercase;'
        'opacity:0.55;font-weight:600;">'
        '✨  Try one of these to get started  ✨'
        '</div>',
        unsafe_allow_html=True,
    )

    picked: Optional[str] = None
    cols = st.columns(min(len(chips), 4))
    for i, chip in enumerate(chips):
        with cols[i % len(cols)]:
            if st.button(
                chip,
                key=f"{key_prefix}_{mode}_{i}",
                use_container_width=True,
                help="Click to use this prompt",
            ):
                picked = chip

    return picked
