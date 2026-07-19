"""
Unified enterprise LLM manager.
"""

import logging

from apps.llm.fallback_manager import (
    FallbackManager
)


logger = logging.getLogger(
    __name__
)


class LLMManager:

    def __init__(self):

        self.fallback_manager = (
            FallbackManager()
        )

    def generate(
        self,
        prompt,
        task_type="general",
        **kwargs,
    ):

        """
        Generate response using
        intelligent fallback providers.
        """

        try:

            result = (
                self.fallback_manager.generate(

                    prompt=prompt,

                    task_type=task_type,

                    **kwargs,
                )
            )

            if not isinstance(
                result,
                dict
            ):

                logger.warning(

                    "Invalid LLM response format."
                )

                return (

                    "Invalid AI response format."
                )

            success = result.get(
                "success",
                False,
            )

            content = result.get(
                "content",
                "",
            )

            provider = result.get(
                "provider",
                "unknown",
            )

            errors = result.get(
                "errors",
                [],
            )

            if success:

                logger.info(

                    f"Generation success "
                    f"via {provider}"
                )

                return content

            logger.warning(

                f"Generation failed. "
                f"Errors: {errors}"
            )

            if content:

                return content

            return (
                "AI generation failed."
            )

        except Exception as error:

            logger.exception(

                "LLM manager generation failed."
            )

            return (

                f"LLM system failure: "
                f"{str(error)}"
            )

    def generate_with_metadata(
        self,
        prompt,
        task_type="general",
        **kwargs,
    ):

        """
        Return full provider metadata.
        """

        try:

            result = (
                self.fallback_manager.generate(

                    prompt=prompt,

                    task_type=task_type,

                    **kwargs,
                )
            )

            return result

        except Exception as error:

            logger.exception(

                "Metadata generation failed."
            )

            return {

                "success": False,

                "provider": None,

                "content": (

                    "Generation failed."
                ),

                "errors": [
                    str(error)
                ],
            }

    def providers(self):

        """
        Return active providers.
        """

        try:

            return (
                self.fallback_manager
                .available_providers()
            )

        except Exception:

            return []

    def provider_count(self):

        """
        Return total providers.
        """

        return len(
            self.providers()
        )

    def has_active_provider(self):

        """
        Check if any provider active.
        """

        return (
            self.provider_count() > 0
        )

    def health_check(self):

        """
        Enterprise LLM health status.
        """

        providers = (
            self.providers()
        )

        return {

            "status": (

                "active"

                if providers

                else

                "inactive"
            ),

            "providers": providers,

            "provider_count": (
                len(providers)
            ),

            "fallback_enabled": True,

            "local_ai_enabled": (

                any(

                    provider.get(
                        "provider"
                    ) == "ollama"

                    for provider in providers
                )
            ),
        }