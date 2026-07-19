"""
OpenAI client for AI COS.
"""

import os

from openai import OpenAI


class OpenAIClient:

    def __init__(self):

        api_key = os.getenv(
            "OPENAI_API_KEY"
        )

        if not api_key:

            raise ValueError(
                "OPENAI_API_KEY not found."
            )

        self.client = OpenAI(
            api_key=api_key
        )

    def generate_content(self, prompt):

        response = self.client.chat.completions.create(

            model="gpt-4.1-mini",

            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],

            temperature=0.7,
        )

        return response.choices[0].message.content