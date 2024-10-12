import streamlit as st
import streamlit.components.v1 as components
import logging
import sys
from bedrock_a_bot.utils import load_sessions_from_file
from bedrock_a_bot.aws_bedrock import initialize_bedrock_client
from bedrock_a_bot.ui_components import display_chat_history, display_messages, get_user_input
from bedrock_a_bot.sidebar_components import configure_sidebar
from bedrock_a_bot.file_upload_handler import handle_file_upload
from bedrock_a_bot.session_management import initialize_session_state, save_current_session
from bedrock_a_bot.message_handling import handle_user_input
from bedrock_a_bot.logging_config import setup_logging

def initialize_app():
    st.set_page_config(layout="wide")
    st.title("🛏️      🪨      🤖")
    initialize_session_state()
    model, region, profile, temperature, top_p = configure_sidebar()
    st.session_state.file_contents = handle_file_upload()
    bedrock_runtime = initialize_bedrock_client(region, profile)
    return model, temperature, top_p, bedrock_runtime

def diya_chat_tab():
    with st.container():
        components.iframe("https://chat.com.amazon.dev/", height=600, scrolling=True)

def cedric_tab():
    with st.container():
        components.iframe("https://console.harmony.a2z.com/internal-ai-assistant/", height=600, scrolling=True)

def llm_play_tab():
    with st.container():
        components.iframe("https://llm-playground.pdebie.people.a2z.com/chat", height=600, scrolling=True)

def prompt_hub_tab():
    with st.container():
        components.iframe("https://console.harmony.a2z.com/prompt-generator/", height=600, scrolling=True)

def display_chatbot():
    display_chat_history()
    display_messages()

def main(port=8501):
    setup_logging()
    logger = logging.getLogger(__name__)
    model, temperature, top_p, bedrock_runtime = initialize_app()

    chatbot_tab, diya_tab, cedric_tab_content, llm_play_tab_content, prompt_hub_tab_content = st.tabs(["Local", "Diya", "Cedric", "LLM-Play", "Prompt-Hub"])

    with chatbot_tab:
        display_chatbot()

    with diya_tab:
        diya_chat_tab()

    with cedric_tab_content:
        cedric_tab()

    with llm_play_tab_content:
        llm_play_tab()

    with prompt_hub_tab_content:
        prompt_hub_tab()

    # Chat input outside of tabs
    if prompt := get_user_input():
        with chatbot_tab:
            response = handle_user_input(prompt, bedrock_runtime, model, temperature, top_p)
            save_current_session()
            st.rerun()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    else:
        port = 8501
    main(port=port)
