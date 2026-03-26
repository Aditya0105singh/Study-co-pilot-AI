import streamlit as st
from PyPDF2 import PdfReader

def handle_resume_upload():
    """
    Simple resume PDF upload handler.
    Returns tuple: (resume_text, should_process)
    """
    uploaded_file = st.file_uploader(
        "📄 Upload Resume (PDF)", 
        type=["pdf"],
        help="Upload your resume in PDF format for analysis"
    )
    
    if uploaded_file:
        with st.spinner("📖 Extracting text from resume PDF..."):
            try:
                reader = PdfReader(uploaded_file)
                resume_text = ""
                for page in reader.pages:
                    resume_text += page.extract_text() or ""
                    
                if len(resume_text.strip()) < 100:
                    st.warning("⚠️ Very little text extracted. This might be a scanned PDF or have formatting issues.")
                    st.info("💡 Try copying and pasting your resume content directly in the chat instead.")
                    return None, False
                
                st.success(f"✅ Resume processed! Extracted {len(resume_text)} characters")
                
                # Show preview
                with st.expander("📖 Resume Content Preview (first 500 chars)"):
                    st.text(resume_text[:500] + "..." if len(resume_text) > 500 else resume_text)
                
                return resume_text, True
                
            except Exception as e:
                st.error(f"❌ Error reading PDF: {str(e)}")
                st.info("💡 Try copying and pasting your resume content directly in the chat.")
                return None, False
    
    return None, False