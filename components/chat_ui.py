import streamlit as st
from core.explainer import explain_concept
from core.summarizer import summarize_text
from core.quizzer import (
    generate_questions,
    solve_questions,
    evaluate_answers,
)
from core.interview import interview_prep
from core.visualizer import generate_visual
from core.flashcards import generate_flashcards_api
from core.resume_reviewer import review_resume
from utils.logger import log_usage
from utils.pdf_export import add_pdf_download_button
from utils.session_export import add_markdown_download, add_json_download
from utils.markdown_render import render_rich_markdown, has_math
from components.quick_actions import render_quick_actions
from components.feedback import feedback_row
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
                render_rich_markdown(content)

        show("Interview Questions", sections['interview_questions'])
        show("Ideal Answers", sections['ideal_answers'])
        show("Key Concepts", sections['key_concepts'])
        show("Analysis", sections['explanation'])
        show("Common Pitfalls", sections['common_mistakes'])
        show("Summary", sections['quick_summary'])

        if not any(sections[k] for k in ['key_concepts', 'explanation', 'common_mistakes', 'quick_summary', 'interview_questions']):
            render_rich_markdown(sections['main'])

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
        render_rich_markdown(response_text)
        return

    for i, card in enumerate(cards):
        with st.expander(f"Card {i+1} — {card['q'][:55]}…", expanded=False):
            st.markdown(f"**Q:** {card['q']}")
            st.markdown("---")
            st.markdown(f"**A:** {card['a']}")


def _render_assistant_message(content, mode, message_index=None):
    """Render an assistant message body using the right view for the mode."""
    if mode == "visualizer" and "[DIAGRAM_START]" in content:
        parts = content.split("[DIAGRAM_START]")
        render_rich_markdown(parts[0])
        render_mermaid(parts[1].split("[DIAGRAM_END]")[0].strip())
    elif mode == "flashcards" and "Q:" in content:
        render_flashcards(content)
    else:
        render_ai_response_card(content, mode)

    if message_index is not None:
        feedback_row(message_index)


def _run_mode(mode, final_prompt, previous_context):
    """Dispatch to the right mode helper. Returns the response string."""
    if mode == "explainer":
        return explain_concept(final_prompt, previous_context)
    if mode == "visualizer":
        return generate_visual(final_prompt)
    if mode == "flashcards":
        return generate_flashcards_api(final_prompt)
    if mode == "quizzer":
        return generate_questions(final_prompt, previous_context)
    if mode == "interview":
        return interview_prep(final_prompt, "Fresher")
    if mode == "resume":
        return review_resume(final_prompt, previous_context)
    return explain_concept(final_prompt, previous_context)


def _stream_via_router(final_prompt, history):
    """
    Stream a response through core.ai_utils.get_streamed_response which
    auto-routes between Groq and Gemini. Returns the final text.
    """
    try:
        from core.ai_utils import get_streamed_response
        return get_streamed_response(final_prompt, history=history)
    except Exception as e:
        st.warning(f"Streaming router failed, falling back to mode helper: {e}")
        return None


def chat_interface(mode):
    """Unified chat interface."""
    pdf_content = st.session_state.get("pdf_content")

    placeholders = {
        "explainer":  "What concept should we break down?",
        "visualizer": "Describe a system or concept to visualize…",
        "flashcards": "Paste text or a topic to generate flashcards…",
        "quizzer":    "What topic should we test your knowledge on?",
        "interview":  "What role are you interviewing for?",
        "resume":     "Paste your resume text or ask for feedback…",
    }
    placeholder = placeholders.get(mode, "Type your message here...")

    if not st.session_state.messages:
        # Empty State UI
        st.markdown(f"""
        <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; height: 28vh; opacity: 0.55; text-align: center;">
            <svg width="44" height="44" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" style="margin-bottom: 0.8rem;"><circle cx="12" cy="12" r="10"/><path d="M12 16v-4"/><path d="M12 8h.01"/></svg>
            <h3 style="margin: 0; font-weight: 500;">Ready when you are</h3>
            <p style="margin-top: 0.4rem; font-size: 0.9rem;">{placeholder}</p>
        </div>
        """, unsafe_allow_html=True)

        # Quick action chips
        picked = render_quick_actions(mode)
        if picked:
            st.session_state._chip_prompt = picked
            st.rerun()

    # Render history
    for idx, msg in enumerate(st.session_state.messages):
        with st.chat_message(msg["role"]):
            if msg["role"] == "assistant":
                _render_assistant_message(msg["content"], mode, message_index=idx)
            else:
                render_rich_markdown(msg["content"])

    # Export bar — only when there's something worth exporting
    try:
        if len(st.session_state.get("messages", [])) > 2:
            st.markdown(
                '<div style="opacity:0.75;font-size:0.72rem;letter-spacing:1px;'
                'text-transform:uppercase;margin:0.6rem 0 0.2rem;">Export</div>',
                unsafe_allow_html=True,
            )
            ec1, ec2, ec3 = st.columns(3)
            with ec1:
                add_pdf_download_button(
                    st.session_state.messages,
                    filename=f"study_notes_{mode}.pdf",
                    title=f"Study Copilot Notes — {mode.capitalize()}",
                    key=f"pdf_export_{mode}",
                )
            with ec2:
                add_markdown_download(
                    st.session_state.messages,
                    filename=f"study_notes_{mode}.md",
                    title=f"Study Copilot Notes — {mode.capitalize()}",
                    key=f"md_export_{mode}",
                )
            with ec3:
                add_json_download(
                    st.session_state.messages,
                    filename=f"study_session_{mode}.json",
                    meta={"mode": mode},
                    key=f"json_export_{mode}",
                )
    except Exception:
        pass

    # Pull voice / chip prompts (sidebar may have set these) and feed into the box
    pre_text = st.session_state.pop("voice_prompt", None) or st.session_state.pop("_chip_prompt", None)

    # Input
    prompt = st.chat_input(placeholder)

    # If voice/chip pushed text, treat it as a submitted prompt
    if not prompt and pre_text:
        prompt = pre_text

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
            res = None
            try:
                # Always run the mode helper so each mode keeps its specialized
                # prompt engineering (mermaid for visualizer, Q:/A: for
                # flashcards, structured MCQs for quizzer, etc.). The chosen
                # AI engine ("Auto (Dual-LLM)" / Groq / Gemini / Grok) is read
                # downstream by utils/ai_helper.generate_response.
                with st.spinner("Thinking…"):
                    res = _run_mode(mode, final_prompt, previous_context)

                st.session_state.messages.append({"role": "assistant", "content": res})
                log_usage(mode, st.session_state.get("answer_style", ""), bool(pdf_content),
                          final_prompt[:120], (res or "")[:120])

                _render_assistant_message(res, mode, message_index=len(st.session_state.messages) - 1)

            except Exception as e:
                err_msg = f"❌ Error: {str(e)}"
                st.session_state.messages.append({"role": "assistant", "content": err_msg})
                st.error(err_msg)
