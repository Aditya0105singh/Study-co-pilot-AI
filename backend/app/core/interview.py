from backend.app.utils.ai_helper import generate_response
from backend.app.core.prompt_templates import SYSTEM_PROMPT, get_style_prompt, build_final_prompt

def interview_prep(user_input: str, level: str = "Beginner Friendly", api_choice: str = "Gemini") -> str:
    """
    Generate interview questions, ideal answers, and tips.
    user_input can be: role name, role + company, or any follow-up question.
    """
    style_prompt = get_style_prompt(level)

    user_content = f"""
The user wants to prepare for an interview. Their input:
"{user_input}"

If this is a role/company or first request:
1. Generate 5-7 role-specific interview questions (mix of behavioral and technical)
2. Provide short, ideal answers for each
3. Share 3 practical delivery tips

If this is a follow-up message (e.g., "give me harder questions", "explain Q3 more"), 
answer it directly based on the previous context.

Format:
🎯 Interview Questions
Q1. ...
Q2. ...
...

💡 Ideal Answers
A1. ...
A2. ...
...

🧠 Interview Tips
✔ ...
✔ ...
✔ ...
"""

    final_prompt = build_final_prompt(SYSTEM_PROMPT, style_prompt, user_content)
    return generate_response(final_prompt.strip(), primary_choice=api_choice)
