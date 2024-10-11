import streamlit as st
import base64
import logging
import json
from .utils import count_tokens
from .aws_bedrock import get_claude_response
from .pdf_processing import extract_text_from_pdf

logger = logging.getLogger(__name__)

def prepare_conversation_history(messages):
    full_conversation = []
    for i, msg in enumerate(reversed(messages[:-1])):  # Exclude the last message (current user input) and reverse the order
        if msg["role"] == "user":
            full_conversation.append({"role": "user", "content": [{"type": "text", "text": f"Human Question: {msg['content']}"}]})
        elif msg["role"] == "assistant":
            full_conversation.append({"role": "assistant", "content": [{"type": "text", "text": msg['content']}]})
    return list(reversed(full_conversation))

def process_file_contents(file_contents):
    message_content = []
    for file in file_contents:
        if file["type"] == "image":
            message_content.append(file["content"])
        elif file["type"] == "file":
            try:
                file_content = base64.b64decode(file["content"]["source"]["data"])
                if file["content"]["source"]["media_type"] == "application/pdf":
                    extracted_text = extract_text_from_pdf(file_content)
                    if extracted_text:
                        message_content.append({
                            "type": "text",
                            "text": f"Additional Context: File contents of {file['name']} (PDF):\n\n{extracted_text}"
                        })
                    else:
                        message_content.append({
                            "type": "text",
                            "text": f"Additional Context: Unable to extract text from PDF file: {file['name']}"
                        })
                else:
                    text_content = file_content.decode('utf-8', errors='ignore')
                    message_content.append({
                        "type": "text",
                        "text": f"Additional Context: File contents of {file['name']} (type: {file['content']['source']['media_type']}):\n\n{text_content}"
                    })
                logger.info(f"Successfully processed file: {file['name']}")
            except Exception as e:
                logger.error(f"Error processing file {file['name']}: {str(e)}")
    return message_content

def handle_user_input(prompt, bedrock_runtime, model, temperature, top_p):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    full_conversation = prepare_conversation_history(st.session_state.messages)
    
    message_content = [{"type": "text", "text": f"Human Question: {prompt}"}]
    if st.session_state.file_contents:
        message_content.extend(process_file_contents(st.session_state.file_contents))
    
    full_conversation.append({"role": "user", "content": message_content})
    
    logger.info(f"Full conversation being sent to LLM: {json.dumps(full_conversation, indent=2)}")
    
    token_count = count_tokens(full_conversation)
    st.sidebar.write(f"Tokens submitted to LLM: {token_count}")
    
    with st.chat_message("assistant"):
        try:
            response = get_claude_response(bedrock_runtime, model, full_conversation, temperature, top_p)
            st.markdown(response)
            logger.info(f"Received response from LLM: {response}")
        except Exception as e:
            error_message = f"Error getting response from LLM: {str(e)}"
            logger.error(error_message)
            st.error(error_message)
    
    st.session_state.messages.append({"role": "assistant", "content": response})
    return response
