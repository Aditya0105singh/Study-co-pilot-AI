import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai
from openai import OpenAI
import warnings
import time

# Suppress warnings
warnings.filterwarnings("ignore", category=FutureWarning)

load_dotenv()

def get_api_key(key_name):
    """Retrieve API key from env or st.secrets."""
    key = os.getenv(key_name)
    if not key and hasattr(st, 'secrets'):
        key = st.secrets.get(key_name)
    return key

# Individual model generators for fallback reuse
def try_gemini(prompt: str):
    api_key = get_api_key("GEMINI_API_KEY")
    if not api_key: return None, "❌ Gemini API Key missing"
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-2.0-flash")
        response = model.generate_content(prompt)
        if response and hasattr(response, "text"):
            return response.text.strip(), None
        return None, "⚠️ Gemini: Empty response"
    except Exception as e:
        return None, f"❌ Gemini Error: {str(e)}"

def try_grok(prompt: str):
    api_key = get_api_key("XAI_API_KEY")
    if not api_key: return None, "❌ xAI API Key missing"
    try:
        client = OpenAI(api_key=api_key, base_url="https://api.x.ai/v1")
        response = client.chat.completions.create(
            model="grok-2-latest",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip(), None
    except Exception as e:
        return None, f"❌ Grok Error: {str(e)}"

def try_groq(prompt: str):
    api_key = get_api_key("GROQ_API_KEY")
    if not api_key: return None, "❌ Groq API Key missing"
    try:
        client = OpenAI(api_key=api_key, base_url="https://api.groq.com/openai/v1")
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip(), None
    except Exception as e:
        return None, f"❌ Groq Error: {str(e)}"

def generate_response(prompt: str) -> str:
    """Generate response with an intelligent fallback system for high availability."""
    # Mapping of choice to generator function
    generators = {
        "Gemini": try_gemini,
        "Grok (xAI)": try_grok,
        "Groq": try_groq
    }
    
    primary_choice = st.session_state.get("api_choice", "Gemini")
    
    # Try primary choice first
    res, err = generators[primary_choice](prompt)
    if res:
        return res
    
    # If primary fails, log the error and try others as fallback
    st.toast(f"Fallback: {primary_choice} failed. Trying backup...", icon="⚠️")
    
    # Fallback order: If primary fails, try Gemini (if not primary), then Groq, then Grok
    fallback_order = ["Gemini", "Groq", "Grok (xAI)"]
    for model_name in fallback_order:
        if model_name == primary_choice:
            continue
            
        res, err = generators[model_name](prompt)
        if res:
            st.toast(f"✅ Recovered using {model_name}!", icon="✨")
            return res
            
    # If everything fails
    return f"❌ All AI models failed. Please check your API keys and network. Last error: {err}"
