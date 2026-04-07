# ✦ Student Copilot AI
**An Intelligent, All-in-One Study Suite for Modern Learners**

🚀 **[Try the Live Application Here!](https://study-co-pilot-ai-9hqbmaev2ha7r3vqkmyvfv.streamlit.app/)**

![Student Copilot AI Hero](/public/hero.png) <!-- Replace with an actual screenshot path later -->

Student Copilot AI is a premium, AI-powered educational application built with **Streamlit** and heavily customized with modern CSS/SaaS-like aesthetics. It brings the power of state-of-the-art LLMs (Gemini, Groq, and Grok) into a single, cohesive interface designed to help students learn faster, prepare for exams, and ace their interviews.

---

## ✨ Features

- **🧠 Study & Understand**: Get deep, beginner-to-advanced explanations for any complex topic using customized pedagogical prompts.
- **📊 Visualize Concepts**: Automatically generate mermaid.js flowcharts, mind maps, and architectural diagrams.
- **📝 Exam Preparation**: Generate mock quizzes and have your descriptive answers evaluated for accuracy and scored instantly.
- **⚡ Flashcards**: Learn via spaced-repetition logic. Generate targeted Q&A pairs instantly.
- **💼 Interview Practice**: Role-play behavioral and technical interviews with AI, receiving actionable feedback.
- **📄 Resume Review**: Upload your background details and get ATS-style critique on your resume keywords.

### Platform Capabilities
- **📚 Universal Document Loader (PDF)**: Upload a syllabus, research paper, or textbook chapter once in the sidebar, and the AI will contextually reference it across *all tools* automatically.
- **👥 Live Study Rooms**: Create a 6-character room code. Join with friends to chat, collaborate, and study in sync.
- **⏱️ Focus Timer (Pomodoro)**: A built-in SVG ring timer with 25m, 15m, and 5m presets to keep studying sessions optimized.
- **🤖 High-Availability AI Routing**: Multi-model support. Defaults to **Groq (Free) / Llama-3** for lightning-fast speeds and high rate limits (14,400 req/day). Falls back intelligently to **Google Gemini 2.0 Flash** and **Grok** if quotas are exceeded.
- **🌙 Premium UI Design**: Fully responsive, lightweight mobile-first UI with glassmorphism cards, glowing borders, and a beautiful dark mode. 

---

## 🛠️ Tech Stack
- **Frontend / Framework:** Streamlit, Custom HTML/CSS
- **Backend Languages:** Python 3.12+
- **AI Models:** Groq (Llama-3.3-70b-versatile), Google AI (gemini-2.0-flash), xAI (grok-2-latest)
- **Utilities:** `PyPDF2` (Document Processing), `python-dotenv` (Secret management), `google-genai`, `openai` SDK

---

## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/your-username/study-copilot-AI.git
cd study-copilot-AI
```

### 2. Set up Virtual Environment
```bash
python -m venv .venv
# On Windows
.venv\Scripts\activate
# On Mac/Linux
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Variables
Create a `.env` file in the root directory and add your API keys. *Note: Only the Groq API key is strictly required to run the app as it is the default provider.*
```env
# Get from: https://console.groq.com/keys
GROQ_API_KEY=gsk_your_key_here

# Get from: https://aistudio.google.com/apikey
GEMINI_API_KEY=AIzaSy_your_key_here

# Get from: https://console.x.ai/
XAI_API_KEY=xai-your_key_here
```

### 5. Run the Application
```bash
streamlit run main.py
```
*The app will automatically open in your default browser at `http://localhost:8501`.*

---

## 📱 Mobile Friendly
Student Copilot AI includes custom `@media` queries in the underlying design system. It scales perfectly on mobile viewports, restructuring grid columns into a unified scrollable stack while increasing touch targets for a smooth mobile web experience.

## 🤝 Contributing
Contributions are always welcome! Feel free to open an issue or submit a Pull Request.

## 📝 License
This project is licensed under the MIT License.
