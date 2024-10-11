import json
import time
import streamlit as st
import tiktoken

def load_sessions_from_file():
    try:
        with open('saved_sessions.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_sessions_to_file(sessions):
    with open('saved_sessions.json', 'w') as f:
        json.dump(sessions, f)

def show_temporary_message(message, duration=3):
    placeholder = st.empty()
    placeholder.success(message)
    time.sleep(duration)
    placeholder.empty()

def count_tokens(messages):
    encoding = tiktoken.get_encoding("cl100k_base")  # Claude uses cl100k_base encoding
    token_count = 0
    for message in messages:
        if isinstance(message["content"], list):
            for content in message["content"]:
                if content["type"] == "text":
                    token_count += len(encoding.encode(content["text"]))
                # Note: We're not counting tokens for images here
        else:
            token_count += len(encoding.encode(message["content"]))
    return token_count

def infer_session_name(messages, max_length=30):
    if not messages:
        return "New Chat"
    
    first_message = messages[0]["content"]
    words = first_message.split()
    session_name = " ".join(words[:5])  # Take first 5 words
    
    if len(session_name) > max_length:
        session_name = session_name[:max_length-3] + "..."
    
    return session_name