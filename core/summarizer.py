import streamlit as st
from utils.gemini_helper import generate_response
from core.prompt_templates import SYSTEM_PROMPT, get_style_prompt, build_final_prompt

def summarize_text(text: str, previous_context: str = "", user_focus: str = "", extra_instruction: str = "") -> str:
    """
    Summarize study materials using prompt engineering with style control.
    """
    # Short-text guard
    clean_text = (text or "").strip()
    if len(clean_text) < 100:
        return (
            "⚠️ The extracted text is very short. "
            "This often happens with scanned/image-based PDFs or empty pages. "
            "Please try another file or copy-paste the content directly."
        )

    # Get answer style from session state
    answer_style = st.session_state.get("answer_style", "Beginner Friendly")
    style_prompt = get_style_prompt(answer_style)
    
    # Prefer extra_instruction, fall back to user_focus (keeps compatibility)
    instruction = extra_instruction.strip() if extra_instruction else user_focus.strip()
    
    # Build user content with summarization instructions
    user_content = f"""
Please summarize this study material:

Content:
{text}

Additional Instructions:
- If text is VERY short (<50 words), say: "This text is too short to summarize. Please provide longer content."
- Otherwise, create a compact, exam-ready summary in clear, bullet-point sections:
  - Core definitions
  - Most important points (bullets)
  - Key formulas or diagrams (if present)
  - Application scenarios or examples
  - Add 2-3 practice/follow-up questions based on the content

If the user gives extra instructions (below), adapt output accordingly (e.g., "focus on applications"):
{instruction}

Reference prior chat context if relevant:
{previous_context}
"""
    
    # Build final prompt with system + style + user content
    final_prompt = build_final_prompt(SYSTEM_PROMPT, style_prompt, user_content, previous_context)
    
    return generate_response(final_prompt.strip())
# ...existing code...