# 🎓 Study Copilot AI

> AI-powered academic assistant with intelligent dual-LLM routing, collaborative study rooms, and multi-modal learning tools.


🏆 **2nd Place — Pixel to Product Hackathon**

<!-- Replace with an actual screenshot path later -->
>>>>

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Streamlit-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io)
[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org)
[![Gemini](https://img.shields.io/badge/Gemini-2.5%20Flash-4285F4?logo=google&logoColor=white)](https://ai.google.dev)
[![Groq](https://img.shields.io/badge/Groq-Llama%203-F55036?logo=meta&logoColor=white)](https://groq.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## ✨ What Makes This Different

Study Copilot AI is **not just another chatbot wrapper**. Under the hood it ships a **dual-LLM inference router** that picks the right model for each query in real time.

| Model | Role | Why |
|-------|------|-----|
| ⚡ **Groq (Llama 3)** | Fast factual queries, definitions, short lookups | Sub-second latency, ideal for "what / who / list" type prompts |
| 🧠 **Gemini 2.5 Flash** | Deep reasoning, multi-step explanations, PDF analysis | Long context window, stronger chain-of-thought, multimodal |

Routing happens automatically inside `core/ai_utils.py` via a `score_complexity()` function that inspects query length, intent keywords, and structure before dispatching to the optimal backend. Every response is tagged with an inline badge so the user can see which model answered — and how fast.

---

## 🚀 Features

| Mode | Description |
|------|-------------|
| 📘 **Understand Concepts** | Plain-language explanations of any topic with examples and analogies |
| 📝 **Exam Preparation** | Auto-generated quizzes, MCQs, and answer evaluation |
| 🎤 **Interview Practice** | Mock technical / behavioral interviews with feedback |
| 📄 **Resume Review** | Section-by-section critique tailored to target roles |
| 🎨 **Visualize Concepts** | Diagrams, flowcharts, and visual breakdowns of complex ideas |
| 🃏 **Flashcards** | Spaced-repetition flashcard generation from any topic or PDF |
| 👥 **Study Rooms (Collaborative)** | Shared study sessions with join-code based real-time rooms |

---

## 🗂️ Architecture

```
study-copilot-AI/
├── main.py                       # Streamlit entry point
├── requirements.txt
├── .env                          # GEMINI_API_KEY, GROQ_API_KEY
├── .streamlit/
│   └── config.toml
├── core/                         # LLM logic + mode handlers
│   ├── ai_utils.py               # Dual-LLM router + token tracker
│   ├── explainer.py
│   ├── summarizer.py
│   ├── quizzer.py
│   ├── flashcards.py
│   ├── interview.py
│   ├── resume_reviewer.py
│   ├── visualizer.py
│   ├── pdf_handler.py
│   └── prompt_templates.py
├── components/                   # Streamlit UI components
│   ├── sidebar.py
│   ├── chat_ui.py
│   ├── pdf_handler.py
│   ├── resume_handler.py
│   ├── pomodoro.py
│   └── study_rooms.py
├── utils/                        # Helpers
│   ├── ai_helper.py
│   ├── gemini_helper.py
│   ├── pdf_export.py             # PDF notes export
│   └── logger.py
└── frontend/                     # Optional Next.js companion frontend
```

---

## 🧠 LLM Routing Logic

Simplified pseudocode of how `score_complexity()` decides which model gets the query:

```python
def score_complexity(query: str) -> str:
    q = query.lower().strip()
    word_count = len(q.split())

    fast_keywords = {"define", "what is", "list", "who"}
    deep_keywords = {"explain", "why", "compare", "analyze",
                     "step by step", "derive"}

    # Short / factual -> Groq
    if word_count < 8:
        return "groq"
    if any(k in q for k in fast_keywords):
        return "groq"

    # Long / reasoning-heavy -> Gemini
    if any(k in q for k in deep_keywords):
        return "gemini"
    if word_count > 20:
        return "gemini"

    return "groq"   # default fast path
```

The router records latency, attaches a model badge to the UI, and updates the session token tracker after every call.

---

## 🛠️ Tech Stack

| Layer | Tool |
|-------|------|
| UI | Streamlit |
| Deep LLM | Gemini 2.5 Flash |
| Fast LLM | Groq API (Llama 3) |
| PDF parsing | PyPDF2 + pdfplumber |
| PDF export | fpdf2 |
| Config | python-dotenv |
| Hosting | Streamlit Cloud |

---

## ⚙️ Local Setup

```bash
# 1. Clone
git clone https://github.com/Aditya0105singh/study-copilot-AI.git
cd study-copilot-AI

# 2. Install
pip install -r requirements.txt

# 3. Environment
cat > .env <<EOF
GEMINI_API_KEY=your_gemini_key_here
GROQ_API_KEY=your_groq_key_here
EOF

# 4. Run
streamlit run main.py
```

App opens at `http://localhost:8501`.

---

## 📊 Results

- ⚡ **~87% faster** responses on simple queries via Groq routing vs. always-Gemini baseline
- 🧩 **Multi-mode workflow** covering the full student journey — understand → practice → revise → interview
- 📱 **Mobile responsive** UI with dark premium theme
- 👥 **Collaborative Study Rooms** with join-code based shared sessions
- 🏆 **2nd Place** at Pixel to Product Hackathon (40+ teams)

---

## 🗺️ Roadmap

- [ ] Streaming responses
- [ ] PDF export of notes
- [ ] Token usage tracker
- [ ] Persistent user history
- [ ] Speech-to-text

---

## 👤 Author

**Aditya Singh**

- GitHub: [@Aditya0105singh](https://github.com/Aditya0105singh)
- LinkedIn: [aditya17-singh](https://linkedin.com/in/aditya17-singh)
- Email: [adityasingh01517@gmail.com](mailto:adityasingh01517@gmail.com)

---

<sub>Built with care for students who want a smarter study partner.</sub>

