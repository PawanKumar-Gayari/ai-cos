"""
Multi-provider fallback manager.
"""

import os

from apps.llm.gemini_provider import (
    GeminiProvider
)

from apps.llm.openai_provider import (
    OpenAIProvider
)

from apps.llm.ollama_provider import (
    OllamaProvider
)


class FallbackManager:

    def __init__(self):

        self.providers = []

        self.load_providers()

    def load_providers(self):

        """
        Load all available providers.
        """

        gemini_api_key = os.getenv(
            "GEMINI_API_KEY"
        )

        openai_api_key = os.getenv(
            "OPENAI_API_KEY"
        )

        if gemini_api_key:

            self.providers.append(

                GeminiProvider(
                    api_key=gemini_api_key
                )
            )

        if openai_api_key:

            self.providers.append(

                OpenAIProvider(
                    api_key=openai_api_key
                )
            )

        self.providers.append(

            OllamaProvider(
                model_name="tinyllama"
            )
        )

    def generate(
        self,
        prompt,
        **kwargs,
    ):

        """
        Sequential provider fallback.
        """

        errors = []

        for provider in self.providers:

            provider_info = (
                provider.provider_info()
            )

            try:

                response = (
                    provider.generate(
                        prompt,
                        **kwargs,
                    )
                )

                if (
                    response
                    and "failed"
                    not in response.lower()
                ):

                    return {

                        "success": True,

                        "provider": (
                            provider_info
                        ),

                        "content": response,
                    }

                errors.append({

                    "provider": (
                        provider_info
                    ),

                    "error": response,
                })

            except Exception as error:

                errors.append({

                    "provider": (
                        provider_info
                    ),

                    "error": str(error),
                })

        return {

            "success": False,

            "errors": errors,

            "content": (
                "All providers failed."
            ),
        }

    def available_providers(self):

        """
        Return active providers.
        """

        providers = []

        for provider in self.providers:

            providers.append(
                provider.provider_info()
            )

        return providers

    def provider_count(self):

        """
        Return total providers.
        """

        return len(
            self.providers
        )

    def has_providers(self):

        """
        Check providers exist.
        """

        return (
            self.provider_count() > 0
        )

    def health_status(self):

        """
        Return fallback system status.
        """

        return {

            "status": "active",

            "provider_count": (
                self.provider_count()
            ),

            "providers": (
                self.available_providers()
            ),
        }

    def primary_provider(self):

        """
        Return first provider.
        """

        if not self.providers:

            return None

        return self.providers[0]

    def provider_names(self):

        """
        Return provider names only.
        """

        names = []

        for provider in self.providers:

            info = (
                provider.provider_info()
            )

            names.append(
                info.get(
                    "provider"
                )
            )

        return names