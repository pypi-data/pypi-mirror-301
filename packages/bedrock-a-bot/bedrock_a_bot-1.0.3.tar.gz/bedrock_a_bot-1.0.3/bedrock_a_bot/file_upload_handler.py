import streamlit as st
import base64
from .utils import show_temporary_message

def handle_file_upload():
    with st.sidebar.expander("Upload Files", expanded=False):
        uploaded_files = st.file_uploader("", accept_multiple_files=True)

        if uploaded_files:
            file_contents = []
            for file in uploaded_files:
                file_content = file.read()
                file_type = file.type
                
                if file_type.startswith('image'):
                    if file_type == 'image/svg+xml':
                        st.warning(f"SVG file '{file.name}' is not supported and will be skipped.")
                        continue
                    
                    image_base64 = base64.b64encode(file_content).decode('utf-8')
                    file_contents.append({
                        "type": "image",
                        "name": file.name,
                        "content": {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": file_type,
                                "data": image_base64
                            }
                        }
                    })
                else:
                    # For non-image files, use base64 encoding
                    file_base64 = base64.b64encode(file_content).decode('utf-8')
                    file_contents.append({
                        "type": "file",
                        "name": file.name,
                        "content": {
                            "type": "file",
                            "source": {
                                "type": "base64",
                                "media_type": file_type,
                                "data": file_base64
                            }
                        }
                    })
            
            show_temporary_message(f"{len(file_contents)} file(s) uploaded successfully!")
            return file_contents
    return []
