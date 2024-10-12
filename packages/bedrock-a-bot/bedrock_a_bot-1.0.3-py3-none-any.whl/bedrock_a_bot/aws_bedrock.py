import boto3
import json
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def initialize_bedrock_client(region, profile):
    os.environ['AWS_PROFILE'] = profile
    try:
        client = boto3.client(
            service_name='bedrock-runtime',
            region_name=region
        )
        logger.info(f"Successfully initialized Bedrock client for region: {region}")
        return client
    except Exception as e:
        logger.error(f"Error initializing Bedrock client: {str(e)}")
        raise

def get_claude_response(bedrock_runtime, model, messages, temperature=0.7, top_p=0.9):
    body = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 1000,
        "messages": messages,
        "temperature": temperature,
        "top_p": top_p,
    }

    logger.info(f"Sending request to Claude model: {model}")
    logger.debug(f"Request body: {json.dumps(body, indent=2)}")

    try:
        response = bedrock_runtime.invoke_model(
            modelId=model,
            body=json.dumps(body)
        )
        
        response_body = json.loads(response['body'].read())
        logger.info("Successfully received response from Claude")
        logger.debug(f"Response body: {json.dumps(response_body, indent=2)}")
        
        return response_body['content'][0]['text']
    except Exception as e:
        logger.error(f"Error invoking Claude model: {str(e)}")
        raise