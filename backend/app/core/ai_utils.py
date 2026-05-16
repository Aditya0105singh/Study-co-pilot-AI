# core/ai_utils.py
#Handles API selection, loading keys, and LLM initialization.
import os
from dotenv import load_dotenv
from openai import OpenAI
import google.generativeai as genai

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def get_llm_client(api_choice="OpenAI"):
    """Initialize and return LLM client based on user choice."""
    if api_choice == "OpenAI":
        if not OPENAI_API_KEY:
            raise ValueError("❌ Missing OpenAI API Key in .env")
        client = OpenAI(api_key=OPENAI_API_KEY)
        return client, "OpenAI"
    elif api_choice == "Gemini":
        if not GEMINI_API_KEY:
            raise ValueError("❌ Missing Gemini API Key in .env")
        genai.configure(api_key=GEMINI_API_KEY)
        return genai, "Gemini"
    elif api_choice == "Grok":
        xai_api_key = os.getenv("XAI_API_KEY")
        if not xai_api_key:
            raise ValueError("❌ Missing XAI API Key in .env")
        client = OpenAI(api_key=xai_api_key, base_url="https://api.x.ai/v1")
        return client, "Grok"
    elif api_choice == "Groq":
        groq_api_key = os.getenv("GROQ_API_KEY")
        if not groq_api_key:
            raise ValueError("❌ Missing GROQ API Key in .env")
        client = OpenAI(api_key=groq_api_key, base_url="https://api.groq.com/openai/v1")
        return client, "Groq"
    else:
        raise ValueError("Invalid API choice. Use 'OpenAI', 'Gemini', 'Grok', or 'Groq'.")

print("🔑 OpenAI key loaded:", bool(os.getenv("OPENAI_API_KEY")))
print(os.getenv("OPENAI_API_KEY"))
print("🔑 Gemini key loaded:", bool(os.getenv("GEMINI_API_KEY")))
print(os.getenv("GEMINI_API_KEY"))