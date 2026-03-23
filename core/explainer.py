import streamlit as st
from utils.gemini_helper import generate_response
from core.prompt_templates import SYSTEM_PROMPT, get_style_prompt, build_final_prompt

def explain_concept(concept: str, previous_context: str = "") -> str:
    """
    Explain a concept using prompt engineering with style control.
    """
    # Get answer style from session state
    answer_style = st.session_state.get("answer_style", "Beginner Friendly")
    style_prompt = get_style_prompt(answer_style)
    
    # Build user content with concept explanation instructions
    user_content = f"""
Please explain this concept: {concept}

Context: {previous_context if previous_context else "No previous context"}

Additional Instructions:
- If this is a topic (e.g., "Heap Sort", "Normalization in DBMS"):
    - Start with a simple definition or analogy/real-life example.
    - Follow with a step-by-step breakdown or main characteristics in bullet points.
    - Add common mistakes or misconceptions (if any).
    - End with 2-3 quick 'Key Takeaways' for revision.
- If the input sounds like an instruction ("make a quiz", "summarize this"):
    - Gently respond: "It looks like you might want to use the Quizzer or Summarizer mode instead."
- Use information from the previous chat for follow-up or clarifying answers.
- Use Markdown formatting for structure.
- Finally, wherever relevant, suggest a very simple diagram the student can draw 
(ASCII-style or described in words) to visualize the concept, with 4–8 labeled elements.
"""
    
    # Build final prompt with system + style + user content
    final_prompt = build_final_prompt(SYSTEM_PROMPT, style_prompt, user_content, previous_context)
    
    return generate_response(final_prompt.strip())
