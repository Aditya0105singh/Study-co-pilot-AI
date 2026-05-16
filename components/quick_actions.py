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
        "Explain backpropagation in plain English",
        "What is the CAP theorem?",
        "Compare TCP and UDP step by step",
        "Why is recursion useful in tree traversal?",
    ],
    "visualizer": [
        "Draw a flowchart of HTTPS handshake",
        "Visualize the data flow in a REST API",
        "Show the lifecycle of a React component",
        "Diagram the OSI 7-layer model",
    ],
    "flashcards": [
        "Generate 10 flashcards on Operating Systems",
        "Make flashcards from the uploaded PDF",
        "Quick flashcards on SQL JOIN types",
        "Flashcards: top 15 Python built-ins",
    ],
    "quizzer": [
        "Quiz me on Data Structures basics",
        "5 MCQs on linear algebra",
        "Mixed quiz on networking + DBMS",
        "Easy warm-up quiz on Python syntax",
    ],
    "interview": [
        "Mock interview for backend developer role",
        "Ask me behavioral questions for a PM role",
        "System design: design a URL shortener",
        "Frontend interview: React hooks deep dive",
    ],
    "resume": [
        "Review my resume for an ML engineer role",
        "Strengthen the impact bullets in my experience",
        "How can I tailor this resume for FAANG?",
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
    """
    Render quick-start chips. Returns the chosen suggestion text, or None.
    Caller is responsible for pushing it through the chat pipeline.
    """
    chips = _chips_for(mode)
    if not chips:
        return None

    st.markdown(
        '<div style="text-align:center;opacity:0.7;font-size:0.78rem;'
        'letter-spacing:1px;text-transform:uppercase;margin:0.4rem 0 0.6rem;">'
        'Try one of these to get started'
        '</div>',
        unsafe_allow_html=True,
    )

    picked: Optional[str] = None
    cols = st.columns(min(len(chips), 4))
    for i, chip in enumerate(chips):
        with cols[i % len(cols)]:
            if st.button(chip, key=f"{key_prefix}_{mode}_{i}", use_container_width=True):
                picked = chip

    return picked
