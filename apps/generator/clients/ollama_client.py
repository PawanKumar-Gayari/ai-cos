"""
Ollama local AI client.
"""

import requests

from django.conf import settings


class OllamaClient:

    def __init__(
        self
    ):

        self.base_url = getattr(

            settings,

            "OLLAMA_BASE_URL",

            "http://localhost:11434",
        )

        self.model = getattr(

            settings,

            "OLLAMA_MODEL",

            "tinyllama",
        )

    # ======================================
    # GENERATE CONTENT
    # ======================================

    def generate_content(
        self,
        prompt,
    ):

        response = requests.post(

            f"{self.base_url}/api/generate",

            json={

                "model": self.model,

                "prompt": prompt,

                "stream": False,
            },

            timeout=300,
        )

        response.raise_for_status()

        data = response.json()

        return data.get(
            "response",
            ""
        )