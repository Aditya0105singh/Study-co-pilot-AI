from utils.ai_helper import generate_response as unified_generate_response

def generate_response(prompt: str) -> str:
    """Unified response generator that selects between Gemini, Grok, or Groq."""
    return unified_generate_response(prompt)
