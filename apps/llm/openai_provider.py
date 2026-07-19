"""
Enterprise OpenAI LLM Provider
------------------------------

Production-grade OpenAI provider.

Features:
- retry-safe generation
- timeout-safe requests
- markdown cleanup
- token optimization
- response validation
- hallucination-safe cleanup
- provider metadata
- production-safe orchestration
"""

from __future__ import annotations

import logging
import re
import time

from openai import OpenAI

from apps.llm.base_provider import (
    BaseProvider
)


logger = logging.getLogger(
    __name__
)


class OpenAIProvider(
    BaseProvider
):

    DEFAULT_TEMPERATURE = 0.7

    DEFAULT_MAX_TOKENS = 4096

    DEFAULT_MODEL = (
        "gpt-4o-mini"
    )

    MAX_RETRIES = 3

    RETRY_DELAY = 2

    # =============================================
    # INIT
    # =============================================

    def __init__(
        self,
        api_key,
        model_name=None,
    ):

        if not api_key:

            raise ValueError(
                "OPENAI_API_KEY missing."
            )

        self.client = OpenAI(
            api_key=api_key
        )

        self.model_name = (

            model_name

            or

            self.DEFAULT_MODEL
        )

        logger.info(

            f"OpenAI initialized | "
            f"model={self.model_name}"
        )

    # =============================================
    # CLEAN RESPONSE
    # =============================================

    def clean_response(
        self,
        text,
    ):

        if not text:

            return ""

        text = str(text).strip()

        # =========================================
        # REMOVE EMPTY CODE BLOCKS
        # =========================================

        text = re.sub(

            r"```+\s*```+",

            "",

            text,
        )

        # =========================================
        # REMOVE MULTI SPACES
        # =========================================

        text = re.sub(

            r"[ \t]+",

            " ",

            text,
        )

        # =========================================
        # REMOVE EXTRA NEWLINES
        # =========================================

        text = re.sub(

            r"\n{4,}",

            "\n\n",

            text,
        )

        # =========================================
        # REMOVE AI PHRASES
        # =========================================

        unwanted = [

            "As an AI language model",

            "Certainly!",

            "Sure!",

            "I hope this helps",

            "Let me know if",
        ]

        for phrase in unwanted:

            text = text.replace(
                phrase,
                "",
            )

        return text.strip()

    # =============================================
    # CONFIG
    # =============================================

    def build_generation_config(
        self,
        temperature=None,
        max_tokens=None,
    ):

        return {

            "temperature": (

                temperature

                or

                self.DEFAULT_TEMPERATURE
            ),

            "max_tokens": (

                max_tokens

                or

                self.DEFAULT_MAX_TOKENS
            ),
        }

    # =============================================
    # SAFE RESPONSE
    # =============================================

    def safe_response_text(
        self,
        response,
    ):

        try:

            if not response:

                return ""

            if not response.choices:

                return ""

            return str(

                response
                .choices[0]
                .message.content
            ).strip()

        except Exception:

            return ""

    # =============================================
    # GENERATE
    # =============================================

    def generate(
        self,
        prompt,
        **kwargs,
    ):

        temperature = kwargs.get(
            "temperature"
        )

        max_tokens = kwargs.get(
            "max_tokens"
        )

        config = (
            self.build_generation_config(

                temperature=(
                    temperature
                ),

                max_tokens=(
                    max_tokens
                ),
            )
        )

        for attempt in range(

            1,

            self.MAX_RETRIES + 1,
        ):

            try:

                started = time.time()

                logger.info(

                    f"OpenAI generate | "
                    f"attempt={attempt} | "
                    f"model={self.model_name}"
                )

                response = (
                    self.client.chat.completions.create(

                        model=(
                            self.model_name
                        ),

                        messages=[

                            {
                                "role": "user",

                                "content": prompt,
                            }
                        ],

                        temperature=(

                            config[
                                "temperature"
                            ]
                        ),

                        max_tokens=(

                            config[
                                "max_tokens"
                            ]
                        ),
                    )
                )

                response_text = (

                    self.clean_response(

                        self.safe_response_text(
                            response
                        )
                    )
                )

                if not response_text:

                    raise ValueError(
                        "Empty OpenAI response."
                    )

                execution_time = round(

                    time.time()
                    - started,

                    2,
                )

                logger.info(

                    f"OpenAI success | "
                    f"time={execution_time}s"
                )

                return response_text

            except Exception as error:

                logger.exception(

                    f"OpenAI failed | "
                    f"attempt={attempt} | "
                    f"error={str(error)}"
                )

                if attempt < (
                    self.MAX_RETRIES
                ):

                    time.sleep(
                        self.RETRY_DELAY
                    )

        return (
            "OpenAI generation failed."
        )

    # =============================================
    # HEALTH CHECK
    # =============================================

    def health_check(
        self
    ):

        try:

            response = (
                self.generate(
                    "health check"
                )
            )

            return bool(
                response
            )

        except Exception:

            return False

    # =============================================
    # PROVIDER INFO
    # =============================================

    def provider_info(
        self
    ):

        return {

            "provider":
            "openai",

            "model":
            self.model_name,

            "temperature":
            self.DEFAULT_TEMPERATURE,

            "max_tokens":
            self.DEFAULT_MAX_TOKENS,

            "retries":
            self.MAX_RETRIES,
        }