import streamlit as st
import time
import streamlit.components.v1 as components

def pomodoro_timer():
    """Lag-free focus timer using epoch tracking and frontend JS rendering."""
    with st.sidebar:
        st.markdown("---")
        st.markdown("""
        <div style="font-size: 0.65rem; opacity: 0.7; font-weight: 600; text-transform: uppercase; letter-spacing: 1px;">
            Focus Timer
        </div>
        """, unsafe_allow_html=True)

        # Initialize core states without ticking loops
        if "timer_running" not in st.session_state:
            st.session_state.timer_running = False
            st.session_state.time_left = 25 * 60
            st.session_state.target_time = None

        duration_mode = st.radio("Duration", ["25m", "5m", "15m"], horizontal=True, label_visibility="collapsed")

        # Synchronize backend state based purely on epoch delta
        current_time_left = st.session_state.time_left
        if st.session_state.timer_running and st.session_state.target_time:
            current_time_left = int(st.session_state.target_time - time.time())
            if current_time_left <= 0:
                current_time_left = 0
                st.session_state.timer_running = False
                st.session_state.time_left = 0

        mins = current_time_left // 60
        secs = current_time_left % 60
        is_running = st.session_state.timer_running
        color = "#5E6AD2" if is_running else "#888888"
        status_text = '● Active' if is_running else 'Paused'

        # Use an isolated iframe so the visual countdown ticks continuously 
        # completely disconnected from the Python backend (zero server lag!)
        html_code = f"""
        <!DOCTYPE html>
        <html>
        <head>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@500;700&display=swap');
            html, body {{ margin: 0; padding: 0; font-family: 'Inter', sans-serif; background: transparent; overflow: hidden; }}
            .pbox {{ text-align:center; background:#0A0A0A; padding:12px; border-radius:10px; border:1px solid #222222; margin:4px 0; }}
            .ptime {{ font-size:2rem; font-weight:700; letter-spacing:-1px; color:#EEEEEE; }}
            .pstatus {{ font-size:0.65rem; color:{color}; margin-top:4px; font-weight:500; text-transform:uppercase; letter-spacing:1px; }}
        </style>
        </head>
        <body>
            <div class="pbox">
                <div class="ptime" id="ptime">{mins:02d}:{secs:02d}</div>
                <div class="pstatus" id="pstatus">{status_text}</div>
            </div>
            <script>
                let timeLeft = {current_time_left};
                let isRunning = {'true' if is_running else 'false'};
                if (isRunning && timeLeft > 0) {{
                    setInterval(() => {{
                        if (timeLeft <= 0) {{
                            document.getElementById('pstatus').innerText = 'COMPLETE';
                            document.getElementById('pstatus').style.color = '#10B981';
                            document.getElementById('ptime').innerText = '00:00';
                            return;
                        }}
                        timeLeft--;
                        let windowMins = Math.floor(timeLeft / 60).toString().padStart(2, '0');
                        let windowSecs = (timeLeft % 60).toString().padStart(2, '0');
                        document.getElementById('ptime').innerText = windowMins + ':' + windowSecs;
                    }}, 1000);
                }}
            </script>
        </body>
        </html>
        """
        # Embed the completely native JS timer. This stops Python from looping.
        components.html(html_code, height=92)

        # Control Panel Buttons
        col1, col2 = st.columns(2)
        with col1:
            def toggle_timer():
                ctl = st.session_state.time_left
                if st.session_state.timer_running and st.session_state.target_time:
                    ctl = max(0, int(st.session_state.target_time - time.time()))
                
                if st.session_state.timer_running:
                    # Execute Pause
                    st.session_state.timer_running = False
                    st.session_state.time_left = ctl
                else:
                    # Execute Start
                    if ctl <= 0:
                        ctl = int(duration_mode[:-1]) * 60
                    st.session_state.timer_running = True
                    st.session_state.target_time = time.time() + ctl
                
            st.button("Pause" if is_running else "Start", use_container_width=True, on_click=toggle_timer)
            
        with col2:
            def reset_timer():
                st.session_state.timer_running = False
                st.session_state.time_left = int(duration_mode[:-1]) * 60
                st.session_state.target_time = None
                
            st.button("Reset", use_container_width=True, on_click=reset_timer)
