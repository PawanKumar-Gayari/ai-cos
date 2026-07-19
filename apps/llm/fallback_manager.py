"""
Enterprise Multi-Provider Fallback Manager
------------------------------------------

Production-grade AI fallback orchestration.

Features:
- smart provider fallback
- provider health tracking
- cooldown protection
- emergency local fallback
- retry-safe orchestration
- provider analytics
- failure recovery
- production-safe architecture
"""

from __future__ import annotations

import logging
import os
import time

from apps.llm.gemini_provider import (
    GeminiProvider
)

from apps.llm.openai_provider import (
    OpenAIProvider
)

from apps.llm.ollama_provider import (
    OllamaProvider
)


logger = logging.getLogger(
    __name__
)


class FallbackManager:

    """
    Enterprise fallback orchestration.
    """

    PROVIDER_COOLDOWN = 60

    INVALID_PATTERNS = [

        "generation failed",

        "all providers failed",

        "quota exceeded",

        "rate limit",

        "invalid api key",

        "timeout",

        "service unavailable",

        "server unavailable",

        "connection refused",
    ]

    # =============================================
    # INIT
    # =============================================

    def __init__(
        self
    ):

        self.providers = []

        self.provider_health = {}

        self.load_providers()

    # =============================================
    # LOAD PROVIDERS
    # =============================================

    def load_providers(
        self
    ):

        gemini_api_key = os.getenv(
            "GEMINI_API_KEY"
        )

        openai_api_key = os.getenv(
            "OPENAI_API_KEY"
        )

        # =========================================
        # GEMINI
        # =========================================

        if gemini_api_key:

            try:

                provider = (
                    GeminiProvider(
                        api_key=gemini_api_key
                    )
                )

                self.providers.append(
                    provider
                )

                self.provider_health[
                    "gemini"
                ] = {

                    "failures": 0,

                    "successes": 0,

                    "last_failure": None,
                }

                logger.info(
                    "Gemini fallback loaded."
                )

            except Exception as error:

                logger.exception(

                    f"Gemini fallback "
                    f"load failed: "
                    f"{str(error)}"
                )

        # =========================================
        # OPENAI
        # =========================================

        if openai_api_key:

            try:

                provider = (
                    OpenAIProvider(
                        api_key=openai_api_key
                    )
                )

                self.providers.append(
                    provider
                )

                self.provider_health[
                    "openai"
                ] = {

                    "failures": 0,

                    "successes": 0,

                    "last_failure": None,
                }

                logger.info(
                    "OpenAI fallback loaded."
                )

            except Exception as error:

                logger.exception(

                    f"OpenAI fallback "
                    f"load failed: "
                    f"{str(error)}"
                )

        # =========================================
        # OLLAMA
        # =========================================

        try:

            provider = (
                OllamaProvider(
                    model="tinyllama"
                )
            )

            self.providers.append(
                provider
            )

            self.provider_health[
                "ollama"
            ] = {

                "failures": 0,

                "successes": 0,

                "last_failure": None,
            }

            logger.info(
                "Ollama fallback loaded."
            )

        except Exception as error:

            logger.exception(

                f"Ollama fallback "
                f"load failed: "
                f"{str(error)}"
            )

    # =============================================
    # PROVIDER AVAILABLE
    # =============================================

    def provider_available(
        self,
        provider_name,
    ):

        health = (
            self.provider_health.get(
                provider_name,
                {}
            )
        )

        last_failure = (
            health.get(
                "last_failure"
            )
        )

        if not last_failure:

            return True

        elapsed = (
            time.time()
            - last_failure
        )

        return (
            elapsed >
            self.PROVIDER_COOLDOWN
        )

    # =============================================
    # MARK FAILURE
    # =============================================

    def mark_failure(
        self,
        provider_name,
    ):

        if provider_name not in (
            self.provider_health
        ):

            return

        self.provider_health[
            provider_name
        ]["failures"] += 1

        self.provider_health[
            provider_name
        ]["last_failure"] = (
            time.time()
        )

    # =============================================
    # MARK SUCCESS
    # =============================================

    def mark_success(
        self,
        provider_name,
    ):

        if provider_name not in (
            self.provider_health
        ):

            return

        self.provider_health[
            provider_name
        ]["successes"] += 1

        self.provider_health[
            provider_name
        ]["last_failure"] = None

    # =============================================
    # CLEAN RESPONSE
    # =============================================

    def clean_response(
        self,
        response,
    ):

        if not response:

            return ""

        return str(
            response
        ).strip()

    # =============================================
    # VALID RESPONSE
    # =============================================

    def valid_response(
        self,
        response,
    ):

        response = (
            self.clean_response(
                response
            )
        )

        if not response:

            return False

        response_lower = (
            response.lower()
        )

        for pattern in (
            self.INVALID_PATTERNS
        ):

            if pattern in (
                response_lower
            ):

                return False

        return True

    # =============================================
    # GENERATE
    # =============================================

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

            provider_name = (
                provider_info.get(
                    "provider",
                    "unknown",
                )
            )

            if not self.provider_available(
                provider_name
            ):

                logger.warning(

                    f"{provider_name} "
                    f"in cooldown."
                )

                continue

            try:

                logger.info(

                    f"Fallback trying: "
                    f"{provider_name}"
                )

                response = (
                    provider.generate(

                        prompt,

                        **kwargs,
                    )
                )

                response = (
                    self.clean_response(
                        response
                    )
                )

                if self.valid_response(
                    response
                ):

                    self.mark_success(
                        provider_name
                    )

                    logger.info(

                        f"{provider_name} "
                        f"fallback success."
                    )

                    return {

                        "success": True,

                        "provider": (
                            provider_info
                        ),

                        "content": response,

                        "fallback_used": (
                            len(errors) > 0
                        ),

                        "errors": errors,
                    }

                self.mark_failure(
                    provider_name
                )

                errors.append({

                    "provider": (
                        provider_info
                    ),

                    "error": response,
                })

            except Exception as error:

                self.mark_failure(
                    provider_name
                )

                logger.exception(

                    f"{provider_name} "
                    f"fallback failed: "
                    f"{str(error)}"
                )

                errors.append({

                    "provider": (
                        provider_info
                    ),

                    "error": str(error),
                })

        logger.error(
            "All fallback providers failed."
        )

        return {

            "success": False,

            "errors": errors,

            "content": (
                "All providers failed."
            ),
        }

    # =============================================
    # AVAILABLE PROVIDERS
    # =============================================

    def available_providers(
        self
    ):

        providers = []

        for provider in self.providers:

            providers.append(
                provider.provider_info()
            )

        return providers

    # =============================================
    # PROVIDER COUNT
    # =============================================

    def provider_count(
        self
    ):

        return len(
            self.providers
        )

    # =============================================
    # HAS PROVIDERS
    # =============================================

    def has_providers(
        self
    ):

        return (
            self.provider_count() > 0
        )

    # =============================================
    # HEALTH STATUS
    # =============================================

    def health_status(
        self
    ):

        return {

            "status": "active",

            "provider_count": (
                self.provider_count()
            ),

            "providers": (
                self.available_providers()
            ),

            "provider_health": (
                self.provider_health
            ),
        }

    # =============================================
    # PRIMARY PROVIDER
    # =============================================

    def primary_provider(
        self
    ):

        if not self.providers:

            return None

        return self.providers[0]

    # =============================================
    # PROVIDER NAMES
    # =============================================

    def provider_names(
        self
    ):

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