# Contributing to Study Buddy

Thanks for your interest in contributing to **Study Buddy – AI-Powered Study Assistant**!  
This project is maintained by **Ammaar Ahmad Khan (GPA95)** and is open to improvements, bug fixes, and documentation updates.

Please read these guidelines before opening an issue or pull request.

---

## 💡 Types of contributions welcome

- 🐞 Bug fixes and robustness improvements  
- ✨ New features that improve the learning experience  
- 🧹 Code cleanup, refactoring, and performance improvements  
- 📚 Documentation updates (README, user guide, usage examples)

If you are not sure whether an idea fits, feel free to open a small issue first for discussion.

---

## 🪜 How to contribute (fork & PR workflow)

1. **Fork the repository**  
   Click the “Fork” button on GitHub to create your own copy under your account.

2. **Clone your fork locally**

    ```
    git clone https://github.com/<your-username>/AI_StudyBuddy.git
    cd AI_StudyBuddy
    ```

3. **Create a feature branch**

    ```
    git checkout -b feature/short-descriptive-name
    ```

4. **Set up the project**

- Create and activate a virtual environment (recommended).  
- Install dependencies:

  ```
  pip install -r requirements.txt
  ```

- Add your Gemini API key via `.env` / `st.secrets` as described in the README (do not commit secrets).

5. **Make your changes**

- Keep the code style consistent with the existing project.  
- Add/adjust comments and docstrings where useful.  
- Update or add documentation if behavior changes (README, user guide, etc.).

6. **Run and test locally**

    ```
    streamlit run main.py
    ```

    Make sure your changes work across all modes (Explainer, Summarizer, Quizzer) and do not break existing flows.

7. **Commit your changes**

    ```
    git add .
    git commit -m "feat: short description of change"
    ```

8. **Push your branch**

    ```
    git push origin feature/short-descriptive-name
    ```

9. **Open a Pull Request**

- Go to your fork on GitHub.  
- Click “Compare & pull request”.  
- Target: `GPA95/AI_StudyBuddy` → `main`.  
- Clearly describe:
  - What you changed.  
  - Why it improves the project.  
  - Any screenshots for UI changes.

---

## ✅ Pull request expectations

To keep the project maintainable:

- Keep PRs focused and small (one logical change per PR).  
- Make sure the app runs without errors on your branch.  
- Be responsive to review comments and open to changes.  
- Do not include:
- Secrets, API keys, or credentials  
- Large, unrelated refactors mixed with feature changes

PRs that do not meet these basics may be closed.

---

## 👤 Attribution and forks

- You are welcome to **fork** this project to learn or create your own version.  
- If you deploy or publish a derivative project publicly:
- Keep the license and attribution to **“Study Buddy by Ammaar Ahmad Khan (GPA95)”**.  
- Include a link back to the original repository:
 - https://github.com/GPA95/AI_StudyBuddy

---

## 🤝 Code of conduct

Please be respectful and constructive in all interactions (issues, PRs, discussions).  
Harassment, personal attacks, or spammy/self-promotional behavior is not acceptable.

By contributing to this repository, you agree to follow these guidelines.