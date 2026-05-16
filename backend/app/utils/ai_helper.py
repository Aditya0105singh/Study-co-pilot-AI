import os
from dotenv import load_dotenv
from openai import OpenAI
import google.generativeai as genai
import warnings
import time
from pathlib import Path

# Suppress warnings
warnings.filterwarnings("ignore", category=FutureWarning)

# Load .env from the project root
_env_path = Path(__file__).resolve().parent.parent.parent.parent / ".env"
load_dotenv(dotenv_path=_env_path)

def get_api_key(key_name):
    """Retrieve API key from env."""
    return os.getenv(key_name)

# Individual model generators for fallback reuse
def try_gemini(prompt: str):
    api_key = get_api_key("GEMINI_API_KEY")
    if not api_key: return None, "❌ Gemini API Key missing"
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-2.0-flash")
        response = model.generate_content(
            prompt,
            request_options={"timeout": 30}
        )
        if response and hasattr(response, "text"):
            return response.text.strip(), None
        return None, "⚠️ Gemini: Empty response"
    except Exception as e:
        err = str(e)
        if "429" in err:
            return None, "⚠️ Gemini daily free quota exceeded — falling back"
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

def generate_response(prompt: str, primary_choice: str = "Gemini") -> str:
    """Generate response with an intelligent fallback system for high availability."""
    generators = {
        "Gemini":     try_gemini,
        "Grok (xAI)": try_grok,
        "Groq (Free)": try_groq,
        "Groq":       try_groq,
        "Grok":       try_grok,
    }

    # Try primary choice first
    gen_fn = generators.get(primary_choice, try_gemini)
    res, err = gen_fn(prompt)
    if res:
        return res

    # Fallback order
    fallback_order = ["Gemini", "Groq (Free)", "Grok (xAI)"]
    for model_name in fallback_order:
        if model_name == primary_choice:
            continue
        fn = generators.get(model_name)
        if not fn:
            continue
        res, err = fn(prompt)
        if res:
            return res

    # If everything fails
    return f"❌ All AI models failed. Please check your API keys and network connection. Last error: {err}"
