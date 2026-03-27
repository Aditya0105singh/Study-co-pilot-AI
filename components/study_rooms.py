import streamlit as st
import uuid
from datetime import datetime
from streamlit_webrtc import webrtc_streamer, WebRtcMode, RTCConfiguration


# TURN/STUN servers for WebRTC connectivity
RTC_CONFIGURATION = RTCConfiguration({
    "iceServers": [
        {"urls": ["stun:stun.l.google.com:19302"]},
        {"urls": ["stun:stun1.l.google.com:19302"]},
        {"urls": ["stun:stun2.l.google.com:19302"]},
        {"urls": ["stun:stun3.l.google.com:19302"]},
        {"urls": ["stun:stun4.l.google.com:19302"]},
    ]
})


def generate_room_code():
    """Generate a 6-character room code."""
    return str(uuid.uuid4())[:6].upper()


def create_room(room_name: str, creator_name: str) -> str:
    """Create a new study room and return the room code."""
    room_code = generate_room_code()
    
    if "rooms" not in st.session_state:
        st.session_state.rooms = {}
        
    st.session_state.rooms[room_code] = {
        "name": room_name,
        "creator": creator_name,
        "participants": [creator_name],
        "created_at": datetime.now().isoformat(),
        "messages": [],
        "is_active": True
    }
    
    return room_code


def join_room(room_code: str, participant_name: str) -> bool:
    """Join an existing room. Returns True if successful."""
    room_code = room_code.upper().strip()
    
    if "rooms" in st.session_state and room_code in st.session_state.rooms:
        room = st.session_state.rooms[room_code]
        if room["is_active"]:
            if participant_name not in room["participants"]:
                room["participants"].append(participant_name)
            st.session_state.current_room = room_code
            return True
    return False


def leave_room():
    """Leave the current room."""
    st.session_state.current_room = None
    st.session_state.room_messages = []


def send_message(room_code: str, sender: str, message: str):
    """Send a message in the room chat."""
    if "rooms" in st.session_state and room_code in st.session_state.rooms:
        msg = {
            "sender": sender,
            "message": message,
            "timestamp": datetime.now().strftime("%H:%M")
        }
        st.session_state.rooms[room_code]["messages"].append(msg)


def study_rooms_ui():
    """Main UI for study rooms feature with the new Crafted Indigo design."""
    
    # Custom CSS for study rooms (Restrained/Modern)
    st.markdown("""
    <style>
    .room-card {
        background: #0A0A0A;
        border: 1px solid #222222;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        text-align: center;
        transition: border-color 0.2s ease;
        box-shadow: 0 4px 10px rgba(0,0,0,0.5);
    }
    .room-card:hover {
        border-color: #5E6AD2;
        box-shadow: 0 8px 24px rgba(0,0,0,0.8);
    }
    .room-code {
        font-size: 2rem;
        font-weight: 700;
        color: #EEEEEE;
        letter-spacing: 0.2rem;
        font-family: monospace;
        background: #111111;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        display: inline-block;
        margin: 1rem 0;
        border: 1px solid #333333;
    }
    .room-code-small {
        font-size: 1rem;
        font-weight: 600;
        color: #5E6AD2;
        font-family: monospace;
        background: rgba(94, 106, 210, 0.1);
        padding: 0.2rem 0.5rem;
        border-radius: 6px;
        border: 1px solid rgba(94, 106, 210, 0.3);
    }
    .participant-badge {
        display: inline-block;
        background: rgba(94, 106, 210, 0.15);
        color: #5E6AD2;
        padding: 0.2rem 0.6rem;
        border-radius: 6px;
        margin: 0.2rem;
        font-weight: 500;
        font-size: 0.8rem;
        border: 1px solid rgba(94, 106, 210, 0.3);
    }
    .chat-message {
        background: #111111;
        padding: 0.8rem 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 3px solid #5E6AD2;
    }
    .chat-sender {
        color: #5E6AD2;
        font-weight: 600;
        font-size: 0.8rem;
    }
    .chat-time {
        opacity: 0.6;
        font-size: 0.7rem;
        float: right;
    }
    .video-container {
        background: #0A0A0A;
        border-radius: 12px;
        overflow: hidden;
        border: 1px solid #222222;
    }
    .status-dot {
        display: inline-block;
        width: 8px;
        height: 8px;
        border-radius: 50%;
        margin-right: 8px;
    }
    .status-live {
        background: #5E6AD2;
        box-shadow: 0 0 10px rgba(94, 106, 210, 0.5);
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Check if user is in a room
    if st.session_state.get('current_room'):
        render_room_interface()
    else:
        render_room_lobby()


def render_room_lobby():
    """Render the room creation/joining lobby."""
    
    st.markdown("""
    <div style="text-align: center; padding: 1rem 0 2rem;">
        <h2 style="margin-bottom: 0.5rem;">Study Rooms</h2>
        <p style="opacity: 0.7; font-size: 1rem;">
            Collaborative video spaces for focused group learning.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # User name input
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        user_name = st.text_input(
            "Display Name",
            value=st.session_state.get('user_name', ''),
            placeholder="Identity yourself...",
            label_visibility="collapsed"
        )
        st.session_state.user_name = user_name
    
    if not user_name:
        st.info("👋 Enter your name to enter the lobby.")
        return
    
    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
    
    # Two columns for Create and Join
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="room-card">
            <div style="font-size: 1.5rem; margin-bottom: 0.5rem; color: #5E6AD2;">✨</div>
            <div style="font-weight: 600; margin: 0.5rem 0; color: #EEEEEE;">Create Room</div>
            <div style="color: #888888; font-size: 0.85rem;">Start a new space</div>
        </div>
        """, unsafe_allow_html=True)
        
        room_name = st.text_input(
            "Room Name",
            placeholder="e.g., Physics Deep-Dive",
            key="create_room_name"
        )
        
        def create_space_action():
            if st.session_state.create_room_name:
                room_code = create_room(st.session_state.create_room_name, user_name)
                st.session_state.current_room = room_code

        st.button("Create Space", use_container_width=True, key="create_btn", on_click=create_space_action)
    
    with col2:
        st.markdown("""
        <div class="room-card">
            <div style="font-size: 1.5rem; margin-bottom: 0.5rem; color: #5E6AD2;">🔗</div>
            <div style="font-weight: 600; margin: 0.5rem 0; color: #EEEEEE;">Join Room</div>
            <div style="color: #888888; font-size: 0.85rem;">Enter a 6-character code</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Check if there's a code from home page
        default_code = st.session_state.get("join_code_from_home", "")
        
        join_code = st.text_input(
            "Code",
            value=default_code,
            placeholder="Room code...",
            max_chars=6,
            key="join_room_code"
        ).upper()
        
        def join_space_action():
            if st.session_state.join_room_code:
                if join_room(st.session_state.join_room_code.upper(), user_name):
                    st.session_state.join_code_from_home = ""
                else:
                    st.toast("Space not found")
        
        st.button("Join Space", use_container_width=True, key="join_btn", on_click=join_space_action)
    
    # Show active rooms
    if st.session_state.get('rooms'):
        st.markdown("<div style='height: 30px;'></div>", unsafe_allow_html=True)
        st.markdown("### 🏠 Active Spaces")
        
        for code, room in st.session_state.rooms.items():
            if room["is_active"]:
                with st.expander(f"🔹 {room['name']} • {len(room['participants'])} online"):
                    st.write(f"**Code:** `{code}`")
                    st.write(f"**Participants:** {', '.join(room['participants'])}")
                    if st.button(f"Enter {room['name']}", key=f"quick_join_{code}", use_container_width=True):
                        if join_room(code, user_name):
                            st.rerun()


def render_room_interface():
    """Render the active room interface with real WebRTC video/chat."""
    
    room_code = st.session_state.current_room
    room = st.session_state.rooms.get(room_code, {})
    
    if not room:
        st.error("Room missing")
        leave_room()
        return
    
    # Room header
    header_col1, header_col2 = st.columns([3, 1])
    
    with header_col1:
        st.markdown(f"""
        <div style="display: flex; align-items: center; gap: 10px;">
            <span class="status-dot status-live"></span>
            <h3 style="margin: 0;">{room['name']}</h3>
            <span class="room-code-small">{room_code}</span>
        </div>
        """, unsafe_allow_html=True)
    
    with header_col2:
        def leave_space_action():
            if st.session_state.user_name in room["participants"]:
                room["participants"].remove(st.session_state.user_name)
            leave_room()
            
        st.button("Leave space", use_container_width=True, on_click=leave_space_action)
    
    st.markdown("---")
    
    # Main content: Video + Chat
    video_col, chat_col = st.columns([2, 1])
    
    with video_col:
        st.markdown("#### 🎥 Video Conference")
        
        # WebRTC logic
        video_constraint = st.session_state.get("camera_enabled", True)
        audio_constraint = st.session_state.get("mic_enabled", True)
        
        webrtc_ctx = webrtc_streamer(
            key=f"room-{room_code}-{video_constraint}-{audio_constraint}",
            mode=WebRtcMode.SENDRECV,
            rtc_configuration=RTC_CONFIGURATION,
            media_stream_constraints={
                "video": video_constraint,
                "audio": audio_constraint
            },
            video_html_attrs={
                "style": {"width": "100%", "border-radius": "12px", "border": "1px solid #373A40"},
                "controls": False,
                "autoPlay": True,
            },
            async_processing=True,
        )
        
        # Media controls
        ctrl_col1, ctrl_col2 = st.columns(2)
        with ctrl_col1:
            if st.button("Toggle Video", use_container_width=True):
                st.session_state.camera_enabled = not video_constraint
                st.rerun()
        with ctrl_col2:
            if st.button("Toggle Audio", use_container_width=True):
                st.session_state.mic_enabled = not audio_constraint
                st.rerun()

        # Participants
        st.markdown("#### 👥 Participants")
        participant_html = ""
        for p in room["participants"]:
            participant_html += f'<span class="participant-badge">👤 {p}</span> '
        st.markdown(f'<div>{participant_html}</div>', unsafe_allow_html=True)
    
    with chat_col:
        st.markdown("#### 💬 Chat")
        
        chat_container = st.container(height=300)
        with chat_container:
            messages = room.get("messages", [])
            for msg in messages[-50:]:
                st.markdown(f"""
                <div class="chat-message">
                    <span class="chat-sender">{msg['sender']}</span>
                    <span class="chat-time">{msg['timestamp']}</span>
                    <p style="margin: 0.2rem 0 0 0; font-size: 0.9rem;">{msg['message']}</p>
                </div>
                """, unsafe_allow_html=True)
        
        # Chat input simplified
        with st.form(key="chat_entry", clear_on_submit=True):
            chat_input = st.text_input("Message", placeholder="Send a message...", label_visibility="collapsed")
            if st.form_submit_button("Send", use_container_width=True):
                if chat_input:
                    send_message(room_code, st.session_state.user_name, chat_input)
                    st.rerun()
