# PHASE 0: BASELINE DOCUMENTATION
## Current Features (Pre-Hackathon)

### Core Functionality
- **AI-powered study assistant** with three main modes:
  - **Explainer**: Simplifies academic concepts in simple terms
  - **Summarizer**: Condenses notes or uploaded PDFs
  - **Quizzer**: Three sub-modes (Generate Questions, Solve Questions, Evaluate Answers)

### Technical Stack
- **AI Model**: Google Gemini 2.5 Flash (`models/gemini-2.5-flash`)
- **Frontend**: Streamlit-based web UI
- **Backend**: Python with Google Generative AI SDK
- **PDF Processing**: PyPDF2 for text extraction
- **Environment**: Uses .env files for API key management

### Current Workflow
1. PDF → text extraction (PyPDF2)
2. Text + user prompt → Gemini API
3. Gemini response → formatted UI display

### Current Features
- Chat-based interface with real-time responses
- PDF upload and processing
- Multi-mode sidebar navigation
- Session state management for chat history
- Responsive design with custom branding

### Known Limitations
- No user authentication system
- No conversation history persistence
- Limited to single PDF processing at a time
- No offline mode
- No multi-language support
- Basic error handling
- No rate limiting or usage tracking

### What NOT to Touch (Stable Components)
- Core Gemini API integration (`utils/gemini_helper.py`)
- Streamlit page configuration and basic layout
- PDF processing pipeline
- Session state initialization
- .gitignore configuration (already properly set up)

### Files to Consider for Cleanup
- `rough.py` - Contains test code with hardcoded API key (REMOVE)
- Check for commented code in components
- Ensure all environment variables are properly handled

### Environment Requirements
- Python 3.10+ recommended
- Dependencies: streamlit, google-generativeai, python-dotenv, PyPDF2
- API key: GEMINI_API_KEY required in .env or Streamlit secrets

### Current Status
- ✅ Deployed and functional on Streamlit Cloud
- ✅ All three modes working
- ✅ PDF upload functional
- ✅ Basic error handling in place
- ⚠️ Needs cleanup before hackathon development

---
*This document serves as the baseline before hackathon modifications begin*
