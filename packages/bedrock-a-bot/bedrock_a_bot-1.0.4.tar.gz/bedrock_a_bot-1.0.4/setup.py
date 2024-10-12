from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read().splitlines()

setup(
    name="bedrock-a-bot",
    version="1.0.4",
    author="Manav Kundra",
    author_email="your.email@example.com",
    description="A chatbot tool using AWS Bedrock and Streamlit",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/manav148/Bedrock-A-Bot",
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.12",
    entry_points={
        "console_scripts": [
            "bedrock-a-bot=bedrock_a_bot.__main__:main",
            "upload-bedrock-a-bot=upload_to_pip:main",
        ],
    },
)
