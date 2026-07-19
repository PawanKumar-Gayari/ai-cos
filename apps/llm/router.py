"""
Enterprise Hybrid LLM Routing System
-----------------------------------

Final Optimized Production Edition

Major Improvements:
-------------------
✓ Fast provider fallback
✓ Reduced retry storms
✓ Lower latency routing
✓ Smarter provider prioritization
✓ Better Gemini failure handling
✓ OCI optimized
✓ No worker blocking
✓ Production-safe cooldown logic
✓ Faster AI failover
✓ Lower generation latency
"""

from __future__ import annotations

import logging
import os
import time

from apps.core.services.system_settings_service import (
    SystemSettingsService,
)

from apps.llm.gemini_provider import (
    GeminiProvider,
)

from apps.llm.openai_provider import (
    OpenAIProvider,
)

from apps.llm.ollama_provider import (
    OllamaProvider,
)


logger = logging.getLogger(
    __name__
)


class LLMRouter:

    """
    Enterprise AI routing engine.
    """

    # =====================================================
    # ENTERPRISE SETTINGS
    # =====================================================

    PROVIDER_COOLDOWN = 180

    MAX_RETRIES = 1

    MIN_RESPONSE_LENGTH = 40

    INVALID_PATTERNS = [

        "all providers failed",

        "generation failed",

        "quota exceeded",

        "insufficient_quota",

        "rate limit",

        "api key",

        "unauthorized",

        "429",

        "timed out",

        "connection refused",

        "service unavailable",

        "invalid api key",

        "error occurred",

        "request failed",
    ]

    # =====================================================
    # INIT
    # =====================================================

    def __init__(
        self,
    ):

        self.settings = (
            SystemSettingsService
            .get_settings()
        )

        self.gemini_provider = None

        self.openai_provider = None

        self.ollama_provider = None

        self.provider_health_data = {}

        self.load_providers()

    # =====================================================
    # PROVIDER HEALTH
    # =====================================================

    def provider_health(
        self,
    ):

        return self.provider_health_data

    # =====================================================
    # DEFAULT HEALTH
    # =====================================================

    def default_health(
        self,
    ):

        return {

            "failures": 0,

            "successes": 0,

            "last_failure": None,

            "avg_latency": 0,
        }

    # =====================================================
    # LOAD PROVIDERS
    # =====================================================

    def load_providers(
        self,
    ):

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

        # =================================================
        # GEMINI
        # =================================================

        if (

            self.settings.enable_gemini

            and gemini_api_key

            and "your_" not in (
                gemini_api_key.lower()
            )
        ):

            try:

                self.gemini_provider = (
                    GeminiProvider(
                        api_key=gemini_api_key
                    )
                )

                self.provider_health_data[
                    "gemini"
                ] = self.default_health()

                logger.info(
                    "Gemini provider loaded."
                )

            except Exception as error:

                logger.exception(

                    f"Gemini load failed: "
                    f"{error}"
                )

        # =================================================
        # OPENAI
        # =================================================

        if (

            self.settings.enable_openai

            and openai_api_key

            and "your_" not in (
                openai_api_key.lower()
            )
        ):

            try:

                self.openai_provider = (
                    OpenAIProvider(
                        api_key=openai_api_key
                    )
                )

                self.provider_health_data[
                    "openai"
                ] = self.default_health()

                logger.info(
                    "OpenAI provider loaded."
                )

            except Exception as error:

                logger.exception(

                    f"OpenAI load failed: "
                    f"{error}"
                )

        else:

            logger.warning(
                "OpenAI skipped."
            )

        # =================================================
        # OLLAMA DISABLED
        # =================================================

        if False:

            try:

                self.ollama_provider = (
                    OllamaProvider(

                        base_url=ollama_url,

                        model=ollama_model,
                    )
                )

                self.provider_health_data[
                    "ollama"
                ] = self.default_health()

                logger.info(
                    "Ollama provider loaded."
                )

            except Exception as error:

                logger.exception(

                    f"Ollama load failed: "
                    f"{error}"
                )

    # =====================================================
    # PROVIDER MAP
    # =====================================================

    def provider_map(
        self,
    ):

        return {

            "gemini": (
                "gemini",
                self.gemini_provider,
            ),

            "openai": (
                "openai",
                self.openai_provider,
            ),

            "ollama": (
                "ollama",
                self.ollama_provider,
            ),
        }

    # =====================================================
    # PROVIDER PRIORITY
    # =====================================================

    def provider_priority(
        self,
        forced_provider=None,
    ):

        providers = (
            self.provider_map()
        )

        # =================================================
        # FORCED PROVIDER
        # =================================================

        if forced_provider:

            forced_provider = (
                str(forced_provider)
                .lower()
                .strip()
            )

            if forced_provider in providers:

                logger.info(

                    f"Forced provider "
                    f"with fallback chain: "
                    f"{forced_provider}"
                )

                ordered = []

                forced_data = (
                    providers[
                        forced_provider
                    ]
                )

                if forced_data[1]:

                    ordered.append(
                        forced_data
                    )

                for name, data in (
                    providers.items()
                ):

                    if (
                        name != forced_provider
                        and data[1]
                    ):

                        ordered.append(
                            data
                        )

                return ordered

        # =================================================
        # SMART PRIORITY
        # =================================================

        priority = []

        for provider_name in [

            "gemini",

            "openai",

            "ollama",
        ]:

            provider_data = (
                providers[
                    provider_name
                ]
            )

            if provider_data[1]:

                priority.append(
                    provider_data
                )

        # =================================================
        # ENTERPRISE SORTING
        # =================================================

        priority.sort(

            key=lambda item:

            (

                self.provider_health_data
                .get(item[0], {})
                .get("failures", 0),

                self.provider_health_data
                .get(item[0], {})
                .get("avg_latency", 999),
            )
        )

        return priority

    # =====================================================
    # PROVIDER AVAILABLE
    # =====================================================

    def provider_available(
        self,
        provider_name,
    ):

        health = (
            self.provider_health_data.get(
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

        if (
            elapsed >
            self.PROVIDER_COOLDOWN
        ):

            return True

        logger.warning(

            f"{provider_name} "
            f"in cooldown for "
            f"{round(elapsed, 2)}s"
        )

        return False

    # =====================================================
    # MARK FAILURE
    # =====================================================

    def mark_failure(
        self,
        provider_name,
    ):

        if provider_name not in (
            self.provider_health_data
        ):

            return

        self.provider_health_data[
            provider_name
        ]["failures"] += 1

        self.provider_health_data[
            provider_name
        ]["last_failure"] = (
            time.time()
        )

    # =====================================================
    # MARK SUCCESS
    # =====================================================

    def mark_success(
        self,
        provider_name,
        latency=0,
    ):

        if provider_name not in (
            self.provider_health_data
        ):

            return

        health = (
            self.provider_health_data[
                provider_name
            ]
        )

        health["successes"] += 1

        health["last_failure"] = None

        previous_latency = (
            health.get(
                "avg_latency",
                0,
            )
        )

        if previous_latency == 0:

            health["avg_latency"] = latency

        else:

            health["avg_latency"] = round(

                (
                    previous_latency
                    + latency
                ) / 2,

                2,
            )

    # =====================================================
    # CLEAN RESPONSE
    # =====================================================

    def clean_response(
        self,
        response,
    ):

        if response is None:
            return ""

        try:

            response = str(response)

        except Exception:

            return ""

        return response.strip()

    # =====================================================
    # VALID RESPONSE
    # =====================================================

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

            if pattern in response_lower:

                return False

        if (
            len(response)
            < self.MIN_RESPONSE_LENGTH
        ):

            return False

        return True

    # =====================================================
    # SAFE GENERATE
    # =====================================================

    def safe_generate(
        self,
        provider,
        prompt,
    ):

        return provider.generate(
            prompt
        )

    # =====================================================
    # TRY PROVIDER
    # =====================================================

    def try_provider(
        self,
        provider_name,
        provider_instance,
        prompt,
        task_type,
    ):

        for attempt in range(
            self.MAX_RETRIES
        ):

            try:

                logger.info(

                    f"Trying provider: "
                    f"{provider_name} | "
                    f"Attempt: {attempt + 1}"
                )

                start_time = time.time()

                response = (
                    self.safe_generate(

                        provider_instance,

                        prompt,
                    )
                )

                latency = round(

                    time.time()
                    - start_time,

                    2,
                )

                response = (
                    self.clean_response(
                        response
                    )
                )

                if not self.valid_response(
                    response
                ):

                    logger.warning(

                        f"{provider_name} "
                        f"returned invalid response."
                    )

                    break

                self.mark_success(

                    provider_name,

                    latency,
                )

                logger.info(
                    f"{provider_name} succeeded."
                )

                return {

                    "success": True,

                    "provider": (
                        provider_name
                    ),

                    "task_type": (
                        task_type
                    ),

                    "content": response,

                    "latency": latency,
                }

            except Exception as error:

                logger.exception(

                    f"{provider_name} error: "
                    f"{error}"
                )

                error_text = str(
                    error
                ).lower()

                # =====================================
                # QUOTA / RATE LIMIT
                # =====================================

                if (

                    "quota" in error_text

                    or

                    "429" in error_text

                    or

                    "rate limit" in error_text

                    or

                    "resource_exhausted"
                    in error_text

                    or

                    "503" in error_text

                    or

                    "service unavailable"
                    in error_text
                ):

                    logger.warning(

                        f"{provider_name} "
                        f"cooldown triggered."
                    )

                    self.mark_failure(
                        provider_name
                    )

                    break

                # =====================================
                # FAST FAILOVER
                # =====================================

                break

        self.mark_failure(
            provider_name
        )

        return None

    # =====================================================
    # MAIN GENERATE
    # =====================================================

    def generate(
        self,
        prompt,
        task_type="general",
        provider=None,
    ):

        errors = []

        start_time = time.time()

        providers = self.provider_priority(
            forced_provider=provider
        )

        if not providers:

            return {

                "success": False,

                "provider": None,

                "task_type": task_type,

                "content": (
                    "No active providers."
                ),

                "errors": [
                    "No active providers."
                ],
            }

        for (
            provider_name,
            provider_instance,
        ) in providers:

            if not provider_instance:
                continue

            if not self.provider_available(
                provider_name
            ):

                errors.append(
                    f"{provider_name} cooldown"
                )

                continue

            result = self.try_provider(

                provider_name,

                provider_instance,

                prompt,

                task_type,
            )

            if result:

                result[
                    "fallback_used"
                ] = (
                    len(errors) > 0
                )

                result[
                    "errors"
                ] = errors

                result[
                    "total_execution_time"
                ] = round(

                    time.time()
                    - start_time,

                    2,
                )

                return result

            errors.append(
                f"{provider_name} failed"
            )

        logger.error(
            "All providers failed."
        )

        return {

            "success": False,

            "provider": None,

            "task_type": task_type,

            "content": (
                "All providers failed."
            ),

            "errors": errors,
        }

    # =====================================================
    # ACTIVE PROVIDERS
    # =====================================================

    def active_providers(
        self,
    ):

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

    # =====================================================
    # PROVIDER COUNT
    # =====================================================

    def provider_count(
        self,
    ):

        return len(
            self.active_providers()
        )

    # =====================================================
    # ROUTER STATUS
    # =====================================================

    def router_status(
        self,
    ):

        return {

            "router": "active",

            "provider_count": (
                self.provider_count()
            ),

            "providers": (
                self.active_providers()
            ),

            "provider_health": (
                self.provider_health_data
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