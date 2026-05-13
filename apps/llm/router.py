"""
Enterprise hybrid LLM routing system.
"""

import os
import time
import logging
import asyncio

from apps.core.services.system_settings_service import (
    SystemSettingsService
)

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


class LLMRouter:

    PROVIDER_COOLDOWN = 60

    def __init__(self):

        self.settings = (
            SystemSettingsService.get_settings()
        )

        self.gemini_provider = None

        self.openai_provider = None

        self.ollama_provider = None

        # ==========================================
        # PROVIDER HEALTH
        # ==========================================

        self.provider_health = {}

        self.load_providers()

    # ==================================================
    # LOAD PROVIDERS
    # ==================================================

    def load_providers(
        self
    ):

        """
        Load enabled providers.
        """

        gemini_api_key = os.getenv(
            "GEMINI_API_KEY"
        )

        openai_api_key = os.getenv(
            "OPENAI_API_KEY"
        )

        ollama_url = os.getenv(

            "OLLAMA_BASE_URL",

            "http://localhost:11434",
        )

        ollama_model = os.getenv(

            "OLLAMA_MODEL",

            "tinyllama",
        )

        # ==========================================
        # OPENAI
        # ==========================================

        if (

            self.settings.enable_openai

            and openai_api_key
        ):

            try:

                self.openai_provider = (
                    OpenAIProvider(
                        api_key=openai_api_key
                    )
                )

                self.provider_health[
                    "openai"
                ] = {

                    "failures": 0,

                    "last_failure": None,
                }

                logger.info(
                    "OpenAI provider loaded."
                )

            except Exception as error:

                logger.exception(

                    f"OpenAI load failed: "
                    f"{str(error)}"
                )

        # ==========================================
        # GEMINI
        # ==========================================

        if (

            self.settings.enable_gemini

            and gemini_api_key
        ):

            try:

                self.gemini_provider = (
                    GeminiProvider(
                        api_key=gemini_api_key
                    )
                )

                self.provider_health[
                    "gemini"
                ] = {

                    "failures": 0,

                    "last_failure": None,
                }

                logger.info(
                    "Gemini provider loaded."
                )

            except Exception as error:

                logger.exception(

                    f"Gemini load failed: "
                    f"{str(error)}"
                )

        # ==========================================
        # OLLAMA
        # ==========================================

        if self.settings.enable_ollama:

            try:

                self.ollama_provider = (
                    OllamaProvider(

                        base_url=ollama_url,

                        model=ollama_model,
                    )
                )

                self.provider_health[
                    "ollama"
                ] = {

                    "failures": 0,

                    "last_failure": None,
                }

                logger.info(
                    "Ollama provider loaded."
                )

            except Exception as error:

                logger.exception(

                    f"Ollama load failed: "
                    f"{str(error)}"
                )

    # ==================================================
    # PROVIDER PRIORITY
    # ==================================================

    def provider_priority(
        self
    ):

        """
        Provider priority chain.

        Gemini
        ↓
        OpenAI
        ↓
        Ollama
        """

        return [

            (
                "gemini",
                self.gemini_provider,
            ),

            (
                "openai",
                self.openai_provider,
            ),

            (
                "ollama",
                self.ollama_provider,
            ),
        ]

    # ==================================================
    # HEALTH CHECK
    # ==================================================

    def provider_available(
        self,
        provider_name,
    ):

        """
        Check cooldown status.
        """

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

    # ==================================================
    # MARK FAILURE
    # ==================================================

    def mark_failure(
        self,
        provider_name,
    ):

        """
        Record provider failure.
        """

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

    # ==================================================
    # MARK SUCCESS
    # ==================================================

    def mark_success(
        self,
        provider_name,
    ):

        """
        Reset provider health.
        """

        if provider_name not in (
            self.provider_health
        ):

            return

        self.provider_health[
            provider_name
        ]["failures"] = 0

        self.provider_health[
            provider_name
        ]["last_failure"] = None

    # ==================================================
    # FAILED RESPONSE DETECTION
    # ==================================================

    def is_failed_response(
        self,
        response,
    ):

        """
        Detect provider failure.
        """

        if not response:

            return True

        response_lower = (
            str(response).lower()
        )

        failed_patterns = [

            "failed",

            "error",

            "429",

            "quota",

            "rate limit",

            "api key",

            "unauthorized",

            "timed out",

            "service unavailable",

            "connection refused",
        ]

        for pattern in (
            failed_patterns
        ):

            if pattern in (
                response_lower
            ):

                return True

        return False

    # ==================================================
    # SAFE GENERATION
    # ==================================================

    async def safe_generate(
        self,
        provider,
        prompt,
    ):

        """
        Timeout-safe provider call.
        """

        timeout = (
            self.settings.provider_timeout
        )

        return await asyncio.wait_for(

            asyncio.to_thread(

                provider.generate,

                prompt,
            ),

            timeout=timeout,
        )

    # ==================================================
    # MAIN GENERATION
    # ==================================================

    async def generate(
        self,
        prompt,
        task_type="general",
    ):

        """
        Intelligent generation
        with automatic failover.
        """

        errors = []

        for (
            provider_name,
            provider,
        ) in self.provider_priority():

            if not provider:

                continue

            if not self.provider_available(
                provider_name
            ):

                logger.warning(

                    f"{provider_name} "
                    f"in cooldown state."
                )

                continue

            try:

                logger.info(

                    f"Trying provider: "
                    f"{provider_name}"
                )

                response = await self.safe_generate(

                    provider,

                    prompt,
                )

                if self.is_failed_response(
                    response
                ):

                    logger.warning(

                        f"{provider_name} "
                        f"returned invalid response."
                    )

                    self.mark_failure(
                        provider_name
                    )

                    errors.append(

                        f"{provider_name}: "
                        f"invalid response"
                    )

                    continue

                self.mark_success(
                    provider_name
                )

                logger.info(

                    f"{provider_name} "
                    f"succeeded."
                )

                return {

                    "success": True,

                    "provider": (
                        provider_name
                    ),

                    "task_type": (
                        task_type
                    ),

                    "content": (
                        str(response)
                    ),

                    "fallback_used": (
                        len(errors) > 0
                    ),
                }

            except Exception as error:

                logger.exception(

                    f"{provider_name} error: "
                    f"{str(error)}"
                )

                self.mark_failure(
                    provider_name
                )

                errors.append(

                    f"{provider_name}: "
                    f"{str(error)}"
                )

        logger.error(
            "All providers failed."
        )

        return {

            "success": False,

            "provider": None,

            "task_type": (
                task_type
            ),

            "errors": errors,

            "content": (
                "All providers failed."
            ),
        }

    # ==================================================
    # ACTIVE PROVIDERS
    # ==================================================

    def active_providers(
        self
    ):

        """
        Return active providers.
        """

        providers = []

        if self.gemini_provider:

            providers.append({

                "provider": "gemini",

                "active": True,
            })

        if self.openai_provider:

            providers.append({

                "provider": "openai",

                "active": True,
            })

        if self.ollama_provider:

            providers.append({

                "provider": "ollama",

                "active": True,
            })

        return providers

    # ==================================================
    # PROVIDER COUNT
    # ==================================================

    def provider_count(
        self
    ):

        return len(
            self.active_providers()
        )

    # ==================================================
    # ROUTER STATUS
    # ==================================================

    def router_status(
        self
    ):

        """
        Router health status.
        """

        return {

            "router": "active",

            "provider_count": (
                self.provider_count()
            ),

            "providers": (
                self.active_providers()
            ),

            "provider_health": (
                self.provider_health
            ),

            "cloud_ai": (

                self.gemini_provider
                is not None

                or

                self.openai_provider
                is not None
            ),

            "local_ai": (
                self.ollama_provider
                is not None
            ),
        }