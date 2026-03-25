import streamlit as st
from utils.gemini_helper import generate_response
from core.prompt_templates import SYSTEM_PROMPT, get_style_prompt, build_final_prompt

def generate_flashcards_api(topic: str, previous_context: str = "") -> str:
    """
    Generate AI Flashcards for a topic.
    """
    user_content = f"""
    Please generate 10-15 high-quality academic flashcards for the following topic: {topic}
    
    Context: {previous_context if previous_context else "No previous context"}
    
    Instructions:
    1. Create a question and a clear, concise answer for each card.
    2. Focus on key terms, definitions, and core concepts.
    3. Ensure the cards cover different aspects of the topic (e.g., definitions, processes, examples).
    
    Format your response EXACTLY like this (one per line):
    Q: Question here? | A: Answer here.
    Q: Question here? | A: Answer here.
    """
    
    final_prompt = build_final_prompt(SYSTEM_PROMPT, "Concise & Accurate", user_content, previous_context)
    return generate_response(final_prompt.strip())
