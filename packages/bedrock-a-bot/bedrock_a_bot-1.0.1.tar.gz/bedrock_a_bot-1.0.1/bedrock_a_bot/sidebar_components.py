import streamlit as st

def create_collapsible_sidebar():
    st.markdown("""
    <style>
    .sidebar-content {
        transition: margin-left 0.3s ease-in-out;
    }
    .sidebar-collapse {
        margin-left: -350px;
    }
    .sidebar-toggle {
        position: fixed;
        top: 50%;
        left: 0;
        transform: translateY(-50%);
        z-index: 1000;
        background-color: #0E1117;
        color: white;
        border: none;
        padding: 10px;
        cursor: pointer;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <script>
    const sidebarContent = window.parent.document.querySelector('.sidebar-content');
    const sidebarToggle = window.parent.document.querySelector('.sidebar-toggle');
    
    function toggleSidebar() {
        sidebarContent.classList.toggle('sidebar-collapse');
        sidebarToggle.textContent = sidebarContent.classList.contains('sidebar-collapse') ? '>' : '<';
    }
    
    if (!sidebarToggle) {
        const toggle = window.parent.document.createElement('button');
        toggle.textContent = '<';
        toggle.className = 'sidebar-toggle';
        toggle.onclick = toggleSidebar;
        window.parent.document.body.appendChild(toggle);
    }
    </script>
    """, unsafe_allow_html=True)

def configure_sidebar():
    create_collapsible_sidebar()
    
    st.sidebar.title("Configuration")
    with st.sidebar.expander("LLM Settings", expanded=False):
        model = st.selectbox(
            "Select Model",
            ["anthropic.claude-3-5-sonnet-20240620-v1:0","anthropic.claude-3-sonnet-20240229-v1:0", "anthropic.claude-3-haiku-20240307-v1:0"],
            index=0
        )
        region = st.text_input("AWS Region", value="us-east-1")
        profile = st.text_input("AWS Profile", value="ziya")
        temperature = st.slider("Temperature", min_value=0.0, max_value=1.0, value=0.7, step=0.1)
        top_p = st.slider("Creativity (Top-p)", min_value=0.0, max_value=1.0, value=0.9, step=0.1)
    return model, region, profile, temperature, top_p
