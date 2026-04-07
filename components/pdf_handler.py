import streamlit as st
from PyPDF2 import PdfReader

def extract_pdf_text(uploaded_file):
    """Extract full text from a PDF file."""
    text = ""
    try:
        reader = PdfReader(uploaded_file)
        for page in reader.pages:
            text += page.extract_text() or ""
        return text.strip()
    except Exception as e:
        st.error(f"❌ Error reading PDF: {e}")
        return ""

def handle_pdf_upload():
    """Universal PDF upload handler that renders in the sidebar."""
    with st.sidebar.expander("📚 Upload Study Material (PDF)", expanded=False):
        uploaded_file = st.file_uploader("Upload notes or chapters", type=["pdf"], key="universal_pdf_uploader")
        
        if uploaded_file:
            if st.session_state.get("last_pdf_name") != uploaded_file.name:
                with st.spinner("Extracting text..."):
                    text = extract_pdf_text(uploaded_file)
                    st.session_state["pdf_content"] = text
                    st.session_state["last_pdf_name"] = uploaded_file.name
                st.success(f"✅ Loaded: {uploaded_file.name}")
            
            if st.button("🗑️ Clear PDF", use_container_width=True):
                st.session_state["pdf_content"] = None
                st.session_state["last_pdf_name"] = None
                st.rerun()
            
            return st.session_state.get("pdf_content")
    return st.session_state.get("pdf_content")