import json
import boto3

class ClaudeClient:

    def __init__(self):
        self.client = boto3.client(
            "bedrock-runtime",
            region_name="us-east-1"
        )

    def generate_content(self, prompt):

        response = self.client.invoke_model(
            modelId="anthropic.claude-sonnet-4",
            body=json.dumps({
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 8000,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            })
        )

        result = json.loads(
            response["body"].read()
        )

        return result["content"][0]["text"]