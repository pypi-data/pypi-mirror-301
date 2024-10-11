import streamlit as st
import uuid
from .utils import load_sessions_from_file, save_sessions_to_file, infer_session_name, show_temporary_message

def initialize_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "file_contents" not in st.session_state:
        st.session_state.file_contents = []
    if "saved_sessions" not in st.session_state:
        st.session_state.saved_sessions = load_sessions_from_file()
    if "current_session_id" not in st.session_state:
        st.session_state.current_session_id = str(uuid.uuid4())

def save_current_session():
    if st.session_state.messages:
        session_name = infer_session_name(st.session_state.messages)
        st.session_state.saved_sessions[st.session_state.current_session_id] = {
            "name": session_name,
            "messages": st.session_state.messages,
            "file_contents": st.session_state.file_contents
        }
        save_sessions_to_file(st.session_state.saved_sessions)
        show_temporary_message(f"Chat '{session_name}' saved!", duration=3)

def display_messages():
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
