# Bedrock-A-Bot

Bedrock-A-Bot is a chatbot tool using AWS Bedrock and Streamlit. It provides a user-friendly interface for interacting with various language models and includes features like file upload, session management, and customizable model parameters.

## Installation

You can install Bedrock-A-Bot using pip:

```
pip install bedrock-a-bot
```

## Usage

To run Bedrock-A-Bot, use the following command:

```
bedrock-a-bot [--port PORT]
```

The `--port` argument is optional and defaults to 8501 if not specified.

## Features

- Interactive chat interface
- Support for multiple language models
- File upload functionality
- Session management
- Customizable model parameters (temperature, top_p)
- Integration with AWS Bedrock

## Requirements

- Python 3.12 or higher
- AWS account with Bedrock access
- Required Python packages (automatically installed with pip)

## Development

To set up the development environment:

1. Clone the repository
2. Create a virtual environment:
   ```
   conda create -n BedRockABot python=3.12
   conda activate BedRockABot
   ```
3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## License

This project is licensed under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
