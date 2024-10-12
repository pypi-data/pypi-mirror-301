import argparse
import os
import sys
import subprocess

def main():
    print("Starting Bedrock-A-Bot...")
    parser = argparse.ArgumentParser(description="Run the Bedrock-A-Bot chatbot")
    parser.add_argument("--port", type=int, default=8501, help="Port to run the Streamlit app on")
    args = parser.parse_args()

    print(f"Attempting to run Streamlit app on port {args.port}")
    
    # Get the directory of the current script
    current_dir = os.path.dirname(os.path.abspath(__file__))
    streamlit_script = os.path.join(current_dir, "streamlit_chatbot.py")
    
    # Construct the Streamlit command
    command = f"streamlit run {streamlit_script} --server.port {args.port}"
    
    try:
        # Run the Streamlit command
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running Streamlit: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
