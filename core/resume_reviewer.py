import streamlit as st
from utils.ai_helper import generate_response
from core.prompt_templates import SYSTEM_PROMPT

def review_resume(prompt: str, previous_context: str = "") -> str:
    """
    Resume critique logic.
    """
    system_part = """You are an expert Tech Recruiter and Resume Writer. 
Your goal is to help candidates improve their resumes for ATS systems and hiring managers.
"""

    user_content = f"""
User Input / Resume Data:
{prompt}

Previous Context:
{previous_context if previous_context else "No previous context"}

INSTRUCTIONS:
1. If the user provided a resume/CV text, provide a structured critique:
   - 🌟 Overall Impression: A brief 2-sentence summary of the resume's strength.
   - ❌ Weaknesses: 2-3 areas that lack metrics, impact, or clarity.
   - ✅ Suggestions: 3 actionable ways to improve the resume (e.g., rewrite bullet point X to Y).
   - 🤖 ATS Score Estimation: A rough score out of 100 with a quick reason.

2. If the user asks a follow-up question (e.g., "how can I improve the education section?"), answer it directly based on the context.

Use clean Markdown formatting. Do not use the generic concept explainer format.
"""
    
    final_prompt = f"{SYSTEM_PROMPT}\n\n{system_part}\n\n{user_content}"
    return generate_response(final_prompt.strip())
