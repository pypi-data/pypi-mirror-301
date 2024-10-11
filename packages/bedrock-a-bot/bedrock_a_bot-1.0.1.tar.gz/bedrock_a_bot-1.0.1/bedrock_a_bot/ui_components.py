import streamlit as st
import uuid
from .utils import save_sessions_to_file, show_temporary_message

def delete_conversation(session_id):
    if session_id in st.session_state.saved_sessions:
        del st.session_state.saved_sessions[session_id]
        save_sessions_to_file(st.session_state.saved_sessions)
        show_temporary_message("Conversation deleted!")
        if session_id == st.session_state.current_session_id:
            st.session_state.messages = []
            st.session_state.file_contents = []
            st.session_state.current_session_id = str(uuid.uuid4())

def delete_all_capabilities():
    st.session_state.saved_sessions = {}
    save_sessions_to_file(st.session_state.saved_sessions)
    st.session_state.messages = []
    st.session_state.file_contents = []
    st.session_state.current_session_id = str(uuid.uuid4())
    show_temporary_message("All conversations deleted!")

def display_chat_history():
    with st.sidebar.expander("Chat History", expanded=True):
        if st.button("Create Chat", type="primary", use_container_width=True):
            st.session_state.messages = []
            st.session_state.file_contents = []
            st.session_state.current_session_id = str(uuid.uuid4())
            st.rerun()

        for session_id, session in st.session_state.saved_sessions.items():
            col1, col2 = st.columns([3, 1])
            with col1:
                if st.button(f"{session['name']}", key=f"load_{session_id}", use_container_width=True):
                    st.session_state.messages = session["messages"]
                    st.session_state.file_contents = session["file_contents"]
                    st.session_state.current_session_id = session_id
                    st.rerun()
            with col2:
                if st.button("🗑️", key=f"delete_{session_id}", use_container_width=True):
                    delete_conversation(session_id)
                    st.rerun()

        if st.button("Delete All Conversations", type="secondary", use_container_width=True):
            delete_all_capabilities()
            st.rerun()

def display_messages():
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

def get_user_input():
    return st.chat_input("What is your question?")
