import streamlit as st
from utils.gemini_helper import generate_response
from core.prompt_templates import SYSTEM_PROMPT, get_style_prompt, build_final_prompt

def generate_visual(concept: str, previous_context: str = "") -> str:
    """
    Generate a Mermaid.js diagram code for a concept.
    """
    user_content = f"""
    Please create a comprehensive Mermaid.js Flowchart (graph TD) for the following concept: {concept}
    
    Context: {previous_context if previous_context else "No previous context"}
    
    CRITICAL SYNTAX RULES for Mermaid 10.9.5:
    1. Use 'graph TD' (Top Down) as the header.
    2. EVERY node ID must be alphanumeric (e.g., A1, B2).
    3. EVERY node label MUST be in double quotes (e.g., A["This is a label"]).
    4. NO special characters (like (), [], "", etc.) allowed inside the node ID.
    5. Ensure all arrows use --> syntax.
    6. Minimum 10 nodes for a deep explanation.

    Format your response EXACTLY like this:
    [DIAGRAM_START]
    graph TD
        A["Root Concept"] --> B["Sub-concept 1"]
        A --> C["Sub-concept 2"]
    [DIAGRAM_END]
    
    Brief explanation of the diagram here.
    """
    
    final_prompt = build_final_prompt(SYSTEM_PROMPT, "Technical & Visual", user_content, previous_context)
    return generate_response(final_prompt.strip())
