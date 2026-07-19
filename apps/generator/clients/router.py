"""
Enterprise AI provider router.
"""

from __future__ import annotations

import logging
import time

from dataclasses import (
    dataclass,
    field,
)

from typing import (
    Any,
    Protocol,
    runtime_checkable,
)

from apps.generator.clients.gemini_client import (
    GeminiClient,
)

from apps.generator.clients.openai_client import (
    OpenAIClient,
)

from apps.generator.clients.ollama_client import (
    OllamaClient,
)

from apps.generator.models import (
    GeneratorConfig,
)


# ==========================================
# LOGGER
# ==========================================

logger = logging.getLogger(
    __name__
)


# ==========================================
# CONSTANTS
# ==========================================

MAX_PROVIDER_RETRIES = 3

RETRY_BASE_DELAY = 0.5

CIRCUIT_BREAKER_THRESH = 5

KEYWORD_SECTION_MARKER = (
    "KEYWORD:"
)


# ==========================================
# CLIENT PROTOCOL
# ==========================================

@runtime_checkable
class AIClient(Protocol):

    def generate_content(
        self,
        prompt: str,
    ) -> str | dict | None:
        ...


# ==========================================
# PROVIDER HEALTH
# ==========================================

@dataclass
class ProviderHealth:

    name: str

    client: AIClient

    consecutive_failures: int = (
        field(
            default=0,
            repr=False,
        )
    )

    @property
    def is_open(
        self
    ) -> bool:

        return (

            self.consecutive_failures
            >= CIRCUIT_BREAKER_THRESH
        )

    def record_success(
        self
    ):

        self.consecutive_failures = 0

    def record_failure(
        self
    ):

        self.consecutive_failures += 1


# ==========================================
# AI ROUTER
# ==========================================

class AIRouter:

    # ======================================
    # INIT
    # ======================================

    def __init__(
        self
    ):

        config = (

            GeneratorConfig.objects
            .filter(
                is_active=True
            )
            .first()
        )

        preferred_provider = (

            config.active_provider
            if config
            else "ollama"
        )

        logger.info(

            f"Preferred provider: "
            f"{preferred_provider}"
        )

        self._providers = (
            self._build_provider_priority(
                preferred_provider
            )
        )

    # ======================================
    # BUILD PROVIDER PRIORITY
    # ======================================

    def _build_provider_priority(
        self,
        preferred_provider,
    ):

        provider_map = {

            "ollama": [

                ProviderHealth(

                    name="Ollama",

                    client=OllamaClient(),
                ),

                ProviderHealth(

                    name="OpenAI",

                    client=OpenAIClient(),
                ),

                ProviderHealth(

                    name="Gemini",

                    client=GeminiClient(),
                ),
            ],

            "openai": [

                ProviderHealth(

                    name="OpenAI",

                    client=OpenAIClient(),
                ),

                ProviderHealth(

                    name="Gemini",

                    client=GeminiClient(),
                ),

                ProviderHealth(

                    name="Ollama",

                    client=OllamaClient(),
                ),
            ],

            "gemini": [

                ProviderHealth(

                    name="Gemini",

                    client=GeminiClient(),
                ),

                ProviderHealth(

                    name="OpenAI",

                    client=OpenAIClient(),
                ),

                ProviderHealth(

                    name="Ollama",

                    client=OllamaClient(),
                ),
            ],
        }

        return provider_map.get(

            preferred_provider,

            provider_map["ollama"],
        )

    # ======================================
    # GENERATE CONTENT
    # ======================================

    def generate_content(
        self,
        prompt,
    ):

        if not (

            prompt
            and
            prompt.strip()
        ):

            raise ValueError(
                "Prompt cannot be blank."
            )

        provider_errors = []

        for provider in (
            self._providers
        ):

            if provider.is_open:

                logger.warning(

                    f"Skipping provider "
                    f"{provider.name} "
                    f"(circuit open)"
                )

                continue

            result, error = (
                self._try_provider(

                    provider,

                    prompt,
                )
            )

            if result is not None:

                return result

            provider_errors.append(

                f"{provider.name}: "
                f"{error}"
            )

        logger.error(

            "All providers failed. "
            f"Errors: "
            f"{' | '.join(provider_errors)}"
        )

        return self._local_fallback(
            prompt
        )

    # ======================================
    # TRY PROVIDER
    # ======================================

    def _try_provider(
        self,
        provider,
        prompt,
    ):

        logger.info(

            f"Trying provider "
            f"'{provider.name}'."
        )

        last_error = (
            "unknown error"
        )

        for attempt in range(

            1,

            MAX_PROVIDER_RETRIES + 1,
        ):

            try:

                response = (

                    provider.client.generate_content(
                        prompt
                    )
                )

                if response:

                    logger.info(

                        f"Provider "
                        f"'{provider.name}' "
                        f"succeeded on "
                        f"attempt {attempt}."
                    )

                    provider.record_success()

                    return response, None

                last_error = (
                    "empty response"
                )

            except Exception as exc:

                last_error = str(exc)

                logger.warning(

                    f"Provider "
                    f"'{provider.name}' "
                    f"attempt {attempt} "
                    f"raised: {exc}"
                )

            if attempt < (
                MAX_PROVIDER_RETRIES
            ):

                delay = (

                    RETRY_BASE_DELAY
                    * (
                        2 ** (
                            attempt - 1
                        )
                    )
                )

                time.sleep(delay)

        provider.record_failure()

        logger.error(

            f"Provider "
            f"'{provider.name}' "
            f"exhausted all retries."
        )

        return None, last_error

    # ======================================
    # LOCAL FALLBACK
    # ======================================

    def _local_fallback(
        self,
        prompt,
    ):

        keyword = (
            self._extract_keyword(
                prompt
            )
        )

        logger.warning(

            f"Serving local fallback "
            f"for keyword={keyword}"
        )

        return {

            "title": (
                f"Complete Guide "
                f"to {keyword}"
            ),

            "meta_description": (

                f"Everything you need "
                f"to know about "
                f"{keyword}."
            ),

            "content": (

                f"# {keyword}\n\n"
                f"This is fallback "
                f"content generated "
                f"because all AI "
                f"providers failed."
            ),

            "faq": (

                f"### What is "
                f"{keyword}?\n"
                f"{keyword} is a "
                f"popular topic."
            ),

            "conclusion": (

                f"{keyword} is worth "
                f"learning more about."
            ),
        }

    # ======================================
    # EXTRACT KEYWORD
    # ======================================

    @staticmethod
    def _extract_keyword(
        prompt,
    ):

        try:

            if (
                KEYWORD_SECTION_MARKER
                in prompt
            ):

                raw = (

                    prompt
                    .split(

                        KEYWORD_SECTION_MARKER,
                        1,
                    )[-1]
                    .strip()
                    .splitlines()[0]
                )

                if raw:

                    return raw.strip()

        except Exception:

            pass

        return "SEO Topic"

    # ======================================
    # PROVIDER STATUS
    # ======================================

    def provider_status(
        self,
    ):

        return [

            {

                "name": (
                    p.name
                ),

                "consecutive_failures": (

                    p.consecutive_failures
                ),

                "circuit_open": (
                    p.is_open
                ),
            }

            for p in self._providers
        ]

    # ======================================
    # RESET CIRCUITS
    # ======================================

    def reset_circuit_breakers(
        self
    ):

        for provider in (
            self._providers
        ):

            provider.consecutive_failures = 0

        logger.info(
            "All provider "
            "circuits reset."
        )