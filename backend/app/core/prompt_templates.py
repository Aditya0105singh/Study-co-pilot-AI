# core/prompt_templates.py
# Prompt engineering templates for different answer styles

SYSTEM_PROMPT = """
You are Student Copilot AI.
Your job is to help students learn efficiently.
Always be clear, structured, and practical.
"""

STYLE_PROMPTS = {
    "Beginner Friendly": """
Use simple language with real-life examples.
Avoid technical jargon unless explained.
Include step-by-step explanations.
Format with clear headings and bullet points.
Focus on building understanding from basics.
""",

    "Exam-Oriented": """
Structure answers for exam preparation.
Include definitions, key concepts, and formulas.
Use bullet points for quick review.
Highlight common mistakes and important points.
Focus on what's likely to appear in exams.
""",

    "Quick Revision": """
Keep responses concise and to the point.
Use short bullets and key facts.
Include essential formulas and definitions.
Skip detailed explanations unless critical.
Focus on rapid recall and memorization.
""",

    "Interview Ready": """
Format answers as if responding to interview questions.
Include talking points and practical examples.
Focus on demonstrating knowledge and experience.
Use professional but conversational tone.
Include tips for confident delivery.
"""
}

def get_style_prompt(style_name):
    """Get the prompt template for a specific answer style."""
    return STYLE_PROMPTS.get(style_name, STYLE_PROMPTS["Beginner Friendly"])

def build_final_prompt(system_prompt, style_prompt, user_content, context=""):
    """Combine system, style, and user input into final prompt."""
    prompt_parts = [system_prompt.strip()]
    
    if style_prompt:
        prompt_parts.append(f"Response Style Instructions:\n{style_prompt.strip()}")
    
    if context:
        prompt_parts.append(f"Previous Context:\n{context.strip()}")
    
    prompt_parts.append(f"User Request:\n{user_content.strip()}")
    
    return "\n\n".join(prompt_parts)
