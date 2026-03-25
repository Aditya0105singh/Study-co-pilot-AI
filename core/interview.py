import streamlit as st
from utils.gemini_helper import generate_response
from core.prompt_templates import SYSTEM_PROMPT, get_style_prompt, build_final_prompt

def interview_prep(role: str, level: str) -> str:
    """
    Generate interview questions, ideal answers, and tips using prompt engineering with style control.
    """
    # Get answer style from session state
    answer_style = st.session_state.get("answer_style", "Beginner Friendly")
    style_prompt = get_style_prompt(answer_style)
    
    # Build user content with interview preparation instructions
    user_content = f"""
I am preparing for a {role} interview.
Experience level: {level}.

Generate:
1. 5-7 interview questions
2. Short, ideal answers (clear, concise)
3. 3 practical tips to answer confidently

Format output as:
🎯 Interview Questions
Q1. ...
Q2. ...
...

💡 Ideal Answers
• ...
• ...
...

🧠 Interview Tips
✔ ...
✔ ...
✔ ...
"""
    
    # Build final prompt with system + style + user content
    final_prompt = build_final_prompt(SYSTEM_PROMPT, style_prompt, user_content)
    
    return generate_response(final_prompt.strip())
