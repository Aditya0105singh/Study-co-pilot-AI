# 📒 CHANGELOG

**Project:** Study Copilot AI
**Author:** Aditya Singh

All notable changes to this project are documented in this file. Versioning follows [Semantic Versioning](https://semver.org/).

---

## [v2.0.0] — Major Architecture Overhaul · January 2026

A ground-up overhaul focused on speed, modularity, and collaborative learning.

### Core changes

- **Dual-LLM Routing System** — added Groq API alongside the existing Gemini backend and built a complexity-scoring router (`core/ai_utils.py::score_complexity`) that dispatches each query to the optimal model based on length, intent keywords, and structure.
- **Collaborative Study Rooms** — real-time shared study sessions using a simple join-code system; multiple users can study together in the same context.
- **Complete dark premium UI redesign** — refreshed visual language with CSS animations, smooth transitions, and a Midnight Aurora accent palette across all modes.
- **Full mobile responsive layout** — every panel, card, and modal now adapts cleanly down to small viewports.
- **Modular refactor** — code split into clear `core/`, `components/`, and `utils/` packages so each mode, UI block, and helper lives in its own module.

### New modes added

- **Interview Practice** — mock technical and behavioral interviews with structured feedback.
- **Resume Review** — section-by-section critique tailored to the target role.
- **Visualize Concepts** — Mermaid-powered diagrams and flowcharts generated from natural-language descriptions.
- **Flashcards** — spaced-repetition flashcard sets generated from any topic or uploaded PDF.

---

## [v1.1.0] — Quizzer Expansion · November 2025

- **Quizzer sub-modes** — split into three flows: **Generate** (build quizzes), **Solve** (take quizzes), and **Evaluate** (score and explain answers).
- **Context-aware follow-up chat** — assistant now carries previous turns into the next prompt so the conversation stays coherent.
- **Dynamic sidebar navigation** — sidebar reshapes itself based on the active mode, exposing only the controls relevant to the current task.

---

## [v1.0.0] — Initial Release · October 2025

- **Explainer**, **Summarizer**, and **Quizzer** modes.
- **PDF upload** for in-document Q&A.
- **Gemini integration** as the primary LLM backend.
- Deployed to **Streamlit Cloud**.

---
