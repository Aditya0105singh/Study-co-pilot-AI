# Student Copilot AI

An AI-powered assistant designed to help students 
understand concepts, summarize notes, prepare for exams, 
and get interview-ready using generative AI.

## Problem
Students waste hours searching, summarizing, and revising content.

## Solution
Student Copilot AI provides goal-based AI assistance 
for learning, exam prep, and career readiness.

## Key Features
- Concept explanation
- Notes & PDF summarization
- Quiz & practice questions
- AI-powered interview preparation

## Tech Stack
- Python
- Streamlit
- Gemini API

---

## 🧠 **Project Overview**

Students often struggle to grasp difficult topics or summarize lengthy notes.  
**Student Copilot AI** is an AI-powered web app that acts as a **personal academic assistant**, capable of:

- 🧩 Explaining complex concepts in simple terms  
- 📄 Summarizing notes or uploaded PDFs  
- ❓ Generating quizzes, solving exam questions, and evaluating answers

Combines **Streamlit** for UI and **Gemini 2.5 Flash API** for fast, intelligent AI responses — all in a clean chat-based interface.

---

## ⚙️ **System Design**

### 🏗️ **Architecture**
A lightweight **Streamlit frontend** interacts with **Google Gemini 2.5 Flash** backend via secure API calls.  
All secrets managed safely via `.env` and `st.secrets`.

### 🧩 **Core Features**

| Mode        | Function                                                           | Example                       |
|-------------|--------------------------------------------------------------------|-------------------------------|
| 🧠 **Understand Concepts**      | Simplifies academic concepts                                   | "Explain Deadlock in OS"      |
| 📚 **Revise Notes Quickly**     | Condenses notes or PDFs                                       | Upload 20-page PDF → summary  |
| 📝 **Practice Questions**        | Quiz generator, solver, evaluator (multi-mode workflow)       | MCQs, solve/evaluate Q&As     |

Other Features:
- 📂 PDF upload (PyPDF2 extraction)
- 💬 Real-time chat interface
- 🔄 New chat/reset option
- ☁️ Deployed on Streamlit Cloud

---

## 🧙‍♂️ **Practice Questions Mode — Three Powerful Sub-modes**

1. **📝 Generate Questions**  
   Enter a topic/chapter/passage. Get a variety of questions (MCQ, T/F, fill-in, descriptive) — answers listed together as an answer key for self-testing.
2. **📖 Solve Questions**  
   Paste your exam questions (optionally add word limits or marks). Get concise, exam-ready answers formatted per input.
3. **✅ Evaluate Answers**  
   Submit questions and your answers (with '---' separator, or sequential prompts). Get detailed feedback, correction, and scoring.

---

## 🧱 **Project Structure**

```
Student Copilot AI/
├── main.py
├── requirements.txt
├── assets/
│ └── PROBLEM STATEMENTS.pdf
├── components/
│ ├── chat_ui.py
│ ├── pdf_handler.py
│ └── sidebar.py
├── core/
│ ├── ai_utils.py
│ ├── explainer.py
│ ├── pdf_handler.py
│ ├── quizzer.py
│ └── summarizer.py
└── utils/
└── gemini_helper.py
```

---

## 🪜 **Workflow**
![Student Copilot AI Workflow](https://github.com/user-attachments/assets/2cdac27e-2ae1-4dcf-b339-3a63efcebbb3)
![Student Copilot AI System Architecture](https://github.com/user-attachments/assets/ae8f9a61-c84b-4ebf-9081-f139b98cf443)
©️🖼️ Diagram Credits: [https://gitdiagram.com/](https://gitdiagram.com/)

---

## 📚 **Installation & Setup**

### Prerequisites
- **Python 3.10+ recommended**
- Google Gemini API key

### Local Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/GPA95/SGPA.git
   cd SGPA
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   ```bash
   # Create .env file
   echo "GEMINI_API_KEY=your_api_key_here" > .env
   ```

4. Run the application:
   ```bash
   streamlit run main.py
   ```

---

## 📚 **In-Repo User Guide (Quick Start)**

### 1️⃣ Getting Started

- Open the deployed app: `https://sgpai-study-buddy.streamlit.app/`
- Select a mode from the sidebar: **Understand Concepts**, **Revise Notes Quickly**, or **Practice Questions**
- Provide input (topic, notes, PDF, or questions) in the main chat area

### 2️⃣ Mode Usage

- **Understand Concepts**:  
  Type your concept or question (e.g., "Explain paging in OS for exams").  
  Student Copilot AI returns a simple, exam-oriented explanation.

- **Revise Notes Quickly**:  
  Upload a PDF or paste notes.  
  Choose the summary style (concise / detailed / bullet points) if enabled and generate a summary.

- **Practice Questions**:  
  - Use "Generate Questions" for practice questions with an answer key.  
  - Use "Solve Questions" to get answers to your questions.  
  - Use "Evaluate Answers" to paste both question and your answer to receive feedback and scoring.

### 3️⃣ Tips for Best Results

- Mention exam context (e.g., "for B.Tech 3rd sem OS viva") for sharper responses.  
- Use follow-up prompts in the same chat to refine or extend answers.  
- Reset the chat using the "New Chat" / reset option before switching topics heavily.

---

## 💡 **Tech Stack**

| Category            | Technologies                             |
|---------------------|------------------------------------------|
| **Frontend**        | Streamlit                                |
| **Backend / AI**    | Google Gemini 2.5 Flash API              |
| **Language**        | Python                                   |
| **Libraries**       | PyPDF2, google-generativeai, streamlit, dotenv |
| **Deployment**      | Streamlit Community Cloud                |
| **Security**        | `.env` + `st.secrets` key handling       |

---

## 🧾 **Results**

- 🎯 Simple, modern, and interactive chat-based UI  
- 📑 Smart summarization, quiz generation, and answer evaluation  
- ⚡ Fast, context-aware AI with Gemini 2.5 Flash  
- 🧩 Smooth multi-mode workflow for study and revision

---

## 🚀 **Future Scope**

- 🗣️ Speech-to-text / text-to-speech interaction  
- 🌐 Multi-language explanations  
- 🧠 Flashcard & spaced-repetition support  
- 👤 Memory-based user personalization  
- ☁️ Drive/Notion integration for notes & sessions  

---

> 🧩 *"Integrating AI with Education — Making Learning Simpler, Smarter, and Accessible for All."*

---

## 📜 Usage & Attribution

- You are welcome to **fork** this repository to learn from it or build your own version of Student Copilot AI.  
- If you deploy this project publicly or create a derivative version:
  - Keep the existing license file.  
  - Credit **"Student Copilot AI by Ammaar Ahmad Khan (GPA95)"**.  
  - Include a link back to the original repo:
    - https://github.com/GPA95/SGPA

For contributions, please see [CONTRIBUTING.md](./CONTRIBUTING.md) for guidelines on forking, branching, and opening pull requests.

---

## 👨‍💻 Author

**Ammaar Ahmad Khan**  
- GitHub: [@GPA95](https://github.com/GPA95)

🌟 If you find this repository useful, please give it a star! 🌟

---
