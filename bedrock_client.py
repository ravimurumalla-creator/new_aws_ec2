import os
import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv

load_dotenv()

AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
BEDROCK_MODEL_ID = os.getenv("BEDROCK_MODEL_ID", "amazon.nova-micro-v1:0")

client = boto3.client("bedrock-runtime", region_name=AWS_REGION)

def ask_bedrock(user_text, history=None):
    if history is None:
        history = []

    messages = history + [
        {
            "role": "user",
            "content": [{"text": user_text}]
        }
    ]

    try:
        response = client.converse(
            modelId=BEDROCK_MODEL_ID,
            messages=messages,
            inferenceConfig={
                "maxTokens": 512,
                "temperature": 0.5,
                "topP": 0.9,
            },
        )
        assistant_msg = response["output"]["message"]
        assistant_text = assistant_msg["content"][0]["text"]
        return assistant_text, assistant_msg
    except ClientError as e:
        return f"AWS error: {e.response['Error']['Message']}", None
    except Exception as e:
        return f"Unexpected error: {e}", None