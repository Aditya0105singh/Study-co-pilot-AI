import streamlit as st
from core.explainer import explain_concept
from core.summarizer import summarize_text
from core.quizzer import (
    generate_questions,
    solve_questions,
    evaluate_answers
)
from core.interview import interview_prep
from core.visualizer import generate_visual
from core.flashcards import generate_flashcards_api
from components.pdf_handler import handle_pdf_upload
from components.resume_handler import handle_resume_upload
from utils.logger import log_usage
import re
import streamlit.components.v1 as components


def parse_ai_response(response_text):
    """Parse AI response into structured sections."""
    sections = {
        'main': '', 'key_concepts': '', 'explanation': '',
        'common_mistakes': '', 'quick_summary': '',
        'interview_questions': '', 'ideal_answers': '', 'interview_tips': ''
    }

    if '🎯 Interview Questions' in response_text:
        parts = re.split(r'🎯 Interview Questions|💡 Ideal Answers|🧠 Interview Tips', response_text)
        if len(parts) >= 3:
            sections['interview_questions'] = parts[1].strip()
            sections['ideal_answers'] = parts[2].strip()
            sections['interview_tips'] = parts[3].strip() if len(parts) > 3 else ''
            sections['main'] = response_text
            return sections

    lines = response_text.split('\n')
    current_section = 'main'
    for line in lines:
        line_stripped = line.strip()
        if not line_stripped:
            continue
        if any(h in line_stripped for h in ['Key Concepts', '📌 Key Concepts', '**Key Concepts**']):
            current_section = 'key_concepts'; continue
        elif any(h in line_stripped for h in ['Explanation', '🧠 Explanation', '**Explanation**']):
            current_section = 'explanation'; continue
        elif any(h in line_stripped for h in ['Common Mistakes', '⚠️ Common Mistakes', '**Common Mistakes**']):
            current_section = 'common_mistakes'; continue
        elif any(h in line_stripped for h in ['Quick Summary', '✅ Quick Summary', '**Quick Summary**']):
            current_section = 'quick_summary'; continue
        sections[current_section] += ('\n' + line) if sections[current_section] else line

    if all(not v for k, v in sections.items() if k != 'main'):
        sections['main'] = response_text
    return sections


def render_ai_response_card(response_text, selected_mode):
    """Render AI response in a styled card matching the Midnight Aurora palette."""
    sections = parse_ai_response(response_text)

    # Color per mode
    mode_colors = {
        "explainer": "#5B8DEF", "visualizer": "#A78BFA", "quizzer": "#F59E0B",
        "flashcards": "#2DD4BF", "interview": "#F472B6", "resume": "#FB923C"
    }
    accent = mode_colors.get(selected_mode, "#5B8DEF")

    st.markdown(f"""
    <style>
    .ai-card {{
        background: rgba(128,128,128,0.05);
        border: 1px solid rgba(128,128,128,0.2);
        border-left: 3px solid {accent};
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
    }}
    .ai-card-header {{
        font-size: 0.75rem;
        font-weight: 600;
        color: {accent};
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 1rem;
        padding-bottom: 0.6rem;
        border-bottom: 1px solid rgba(128,128,128,0.2);
    }}
    .ai-section-label {{
        color: {accent};
        font-weight: 600;
        font-size: 0.85rem;
        margin: 1rem 0 0.4rem;
    }}
    @media (max-width: 768px) {{
        .ai-card {{ padding: 1rem; margin: 0.5rem 0; border-radius: 8px; }}
        .ai-card-header {{ font-size: 0.68rem; margin-bottom: 0.6rem; padding-bottom: 0.4rem; }}
        .ai-section-label {{ font-size: 0.78rem; margin: 0.6rem 0 0.3rem; }}
    }}
    </style>
    """, unsafe_allow_html=True)

    mode_titles = {
        "explainer": "Explanation", "quizzer": "Quiz Session", "interview": "Interview Prep",
        "resume": "Resume Analysis", "visualizer": "Visual Concept", "flashcards": "Flash Review"
    }
    title = mode_titles.get(selected_mode, "AI Response")

    with st.container():
        st.markdown('<div class="ai-card">', unsafe_allow_html=True)
        st.markdown(f'<div class="ai-card-header">✦ {title}</div>', unsafe_allow_html=True)

        def show(label, content):
            if content:
                st.markdown(f'<div class="ai-section-label">{label}</div>', unsafe_allow_html=True)
                st.markdown(content)

        show("Interview Questions", sections['interview_questions'])
        show("Ideal Answers", sections['ideal_answers'])
        show("Key Concepts", sections['key_concepts'])
        show("Analysis", sections['explanation'])
        show("Common Pitfalls", sections['common_mistakes'])
        show("Summary", sections['quick_summary'])

        if not any(sections[k] for k in ['key_concepts', 'explanation', 'common_mistakes', 'quick_summary', 'interview_questions']):
            st.markdown(sections['main'])

        st.markdown('</div>', unsafe_allow_html=True)


def get_previous_messages_summary(messages, limit=3):
    return "\n".join(f"{m['role'].capitalize()}: {m['content']}" for m in messages[-2*limit:])


def sanitize_mermaid(code):
    return code.replace("```mermaid", "").replace("```", "").strip()


def render_mermaid(code):
    code = sanitize_mermaid(code)
    html_code = f"""
    <div style="background:rgba(128,128,128,0.05); padding:20px; border-radius:12px; border:1px solid rgba(128,128,128,0.2); margin:1rem 0;">
        <pre class="mermaid" style="text-align:center;">{code}</pre>
    </div>
    <script type="module">
        import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
        const isDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
        mermaid.initialize({{ startOnLoad: true, theme: isDark ? 'dark' : 'default', securityLevel: 'loose' }});
    </script>
    """
    components.html(html_code, height=600, scrolling=True)


def render_flashcards(response_text):
    """Parse and display flashcards."""
    cards = []
    for line in response_text.strip().split('\n'):
        if '|' in line and ': ' in line:
            parts = line.split('|')
            if len(parts) >= 2:
                q = parts[0].split(': ', 1)[-1].strip()
                a = parts[1].split(': ', 1)[-1].strip()
                cards.append({"q": q, "a": a})

    if not cards:
        st.markdown(response_text)
        return

    for i, card in enumerate(cards):
        with st.expander(f"Card {i+1} — {card['q'][:55]}…", expanded=False):
            st.markdown(f"**Q:** {card['q']}")
            st.markdown("---")
            st.markdown(f"**A:** {card['a']}")


def chat_interface(mode):
    """Unified chat interface."""
    pdf_content = handle_pdf_upload()
    st.markdown("---")

    placeholders = {
        "explainer":  "What concept should we break down?",
        "visualizer": "Describe a system or concept to visualize…",
        "flashcards": "Topic or chapter to create flashcards for…",
        "quizzer":    "Subject or topic for practice questions…",
        "interview":  "Role and company you're preparing for…",
        "resume":     "Paste your resume or describe your experience…"
    }
    placeholder = placeholders.get(mode, "Ask anything…")

    # Render history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            if msg["role"] == "assistant":
                if mode == "visualizer" and "[DIAGRAM_START]" in msg["content"]:
                    parts = msg["content"].split("[DIAGRAM_START]")
                    st.markdown(parts[0])
                    render_mermaid(parts[1].split("[DIAGRAM_END]")[0].strip())
                elif mode == "flashcards" and "Q:" in msg["content"]:
                    render_flashcards(msg["content"])
                else:
                    render_ai_response_card(msg["content"], mode)
            else:
                st.markdown(msg["content"])

    # Input
    prompt = st.chat_input(placeholder)
    if prompt:
        # Build context BEFORE appending new user msg
        previous_context = get_previous_messages_summary(st.session_state.messages, limit=4)

        # Build final prompt with PDF context
        if pdf_content:
            final_prompt = f"PDF Context:\n{pdf_content[:8000]}\n\nConversation so far:\n{previous_context}\n\nUser: {prompt}"
        else:
            final_prompt = f"Conversation so far:\n{previous_context}\n\nUser: {prompt}" if previous_context else prompt

        # Store user message + pending AI call, then rerun to render user msg cleanly
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.session_state._pending_prompt = final_prompt
        st.session_state._pending_prev   = previous_context
        st.session_state._pending_mode   = mode
        st.rerun()

    # Second pass: execute AI call after user message is already displayed
    if (st.session_state.get("_pending_prompt")
            and st.session_state.get("_pending_mode") == mode):

        final_prompt     = st.session_state.pop("_pending_prompt")
        previous_context = st.session_state.pop("_pending_prev", "")
        st.session_state.pop("_pending_mode", None)

        with st.chat_message("assistant"):
            with st.spinner("Thinking…"):
                try:
                    if mode == "explainer":    res = explain_concept(final_prompt, previous_context)
                    elif mode == "visualizer": res = generate_visual(final_prompt)
                    elif mode == "flashcards": res = generate_flashcards_api(final_prompt)
                    elif mode == "quizzer":    res = generate_questions(final_prompt, previous_context)
                    elif mode == "interview":  res = interview_prep(final_prompt, "Fresher")
                    elif mode == "resume":     res = explain_concept(final_prompt, previous_context)
                    else:                      res = explain_concept(final_prompt, previous_context)

                    st.session_state.messages.append({"role": "assistant", "content": res})
                    log_usage(mode, st.session_state.get("answer_style",""), bool(pdf_content), final_prompt[:120], res[:120])

                    # Render inline
                    if mode == "visualizer" and "[DIAGRAM_START]" in res:
                        parts = res.split("[DIAGRAM_START]")
                        st.markdown(parts[0])
                        render_mermaid(parts[1].split("[DIAGRAM_END]")[0].strip())
                    elif mode == "flashcards" and "Q:" in res:
                        render_flashcards(res)
                    else:
                        render_ai_response_card(res, mode)

                except Exception as e:
                    err_msg = f"❌ Error: {str(e)}"
                    st.session_state.messages.append({"role": "assistant", "content": err_msg})
                    st.error(err_msg)

