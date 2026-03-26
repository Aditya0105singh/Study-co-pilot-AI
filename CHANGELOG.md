# 🧾 CHANGELOG
**Project:** AI-Powered Study Buddy  
**Repository:** [GPA95/AI_StudyBuddy](https://github.com/GPA95/AI_StudyBuddy)  
**Last Updated:** 14 November 2025

### 🆕 Version 1.1.0 — Major Feature Update (November 2025)

#### ✨ New Features & Improvements

- **Quizzer Mode Expanded:**  
  - Added three sub-modes:
    - 📝 Generate Questions: MCQ, T/F, Fill in the Blanks, Descriptive — answers collected in answer key section
    - 📖 Solve Questions: Exam-style answers auto-adapted to marks/word limit
    - ✅ Evaluate Answers: Automated feedback, scoring, and tips for submitted answers
  - Answer key now shown at the end of quizzes for self-testing

- **Context-Aware Chat:**
  - Improved support for follow-up questions/responses using previous chat history in all modes

- **Dynamic Sidebar:**  
  - Nested radio buttons for Quizzer actions; emoji-powered UI  
  - Clickable badge links for **GitHub Repo** and **User Help** document

- **User Help Documentation:**  
  - Published quick-start guide covering sample inputs, usage tips, format instructions, troubleshooting, and UI walkthrough
  - Help doc directly accessible from sidebar

- **Refined Prompts & Outputs:**
  - Exam-optimized summaries and answer formatting
  - Markdown-friendly structure, answer keys, bullet points
  - Improved adaptive answer length based on marks/word limits

- **UI/UX Enhancements:**
  - Code block outputs with one-click copy capability
  - Info banners for mode guidance and instructions
  - Instant feedback buttons for user rating after responses

- **Performance / Stability:**
  - Improved error/timeout handling for API rate limits
  - Input text limits for large notes/PDFs for manageable processing
  - Auto-clearing new chat notifications for better UX

#### 🛠️ Other Updates

- Streamlined code structure and modularization for maintainability
- Optimized backend prompt logic for clarity, exam readiness, and user options
- Foundations laid for planned features (speech, flashcards, login, notes, multi-language, etc.)

---

### 🏁 Version 1.0.0 — Initial Release (October 2025)

#### ✅ Present Features
- AI Chat Modes: **Explainer**, **Summarizer**, **Quizzer**
- **PDF Upload & Summarization** (PyPDF2 + PDFPlumber)
- **Streamlit-based Chat UI** with sidebar & new chat
- **Gemini 2.5 Flash API** integration for AI responses
- **Secure API key handling** using `.env` and `st.secrets`
- **Deployed** on Streamlit Cloud
- **Clean modular structure** (core, components, utils, assets)

#### 🚀 Next Tasks (v1.1.0)
- Add **speech-to-text** and **text-to-speech** support
- Implement **multilingual explanations**
- Add **flashcard generation** with spaced repetition
- Enable **persistent chat memory**
- Integrate **user login + note storage**
- Enhance **UI/UX** and theme customization

---
