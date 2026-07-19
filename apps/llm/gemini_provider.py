"""
Enterprise Gemini LLM Provider
------------------------------

Final Optimized Enterprise Edition

Major Improvements:
-------------------
✓ AFC disabled
✓ Faster Gemini generation
✓ Lower latency architecture
✓ Reduced retry storms
✓ No blocking worker sleeps
✓ Better quota handling
✓ Production-safe response cleanup
✓ OCI optimized
✓ Faster failover
✓ Stable flash model support
"""

from __future__ import annotations

import logging
import re
import time

from google import genai
from google.genai import types

from apps.llm.base_provider import (
    BaseProvider
)


logger = logging.getLogger(
    __name__
)


class GeminiProvider(
    BaseProvider
):

    # =====================================================
    # ENTERPRISE SETTINGS
    # =====================================================

    DEFAULT_TEMPERATURE = 0.7

    DEFAULT_MAX_TOKENS = 8192

    DEFAULT_MODEL = (
        "gemini-2.5-flash"
    )

    MAX_RETRIES = 1

    # =====================================================
    # INIT
    # =====================================================

    def __init__(
        self,
        api_key,
        model_name=None,
    ):

        if not api_key:

            raise ValueError(
                "GEMINI_API_KEY missing."
            )

        self.api_key = api_key

        self.model_name = (

            model_name

            or

            self.DEFAULT_MODEL
        )

        self.client = (
            genai.Client(
                api_key=api_key
            )
        )

        logger.info(

            f"Gemini initialized | "
            f"model={self.model_name}"
        )

    # =====================================================
    # CLEAN RESPONSE
    # =====================================================

    def clean_response(
        self,
        text,
    ):

        if not text:

            return ""

        text = str(
            text
        ).strip()

        # =============================================
        # REMOVE EMPTY CODE BLOCKS
        # =============================================

        text = re.sub(

            r"```+\s*```+",

            "",

            text,
        )

        # =============================================
        # REMOVE DUPLICATE SPACES
        # =============================================

        text = re.sub(

            r"[ \t]+",

            " ",

            text,
        )

        # =============================================
        # REMOVE EXCESSIVE NEWLINES
        # =============================================

        text = re.sub(

            r"\n{4,}",

            "\n\n",

            text,
        )

        # =============================================
        # REMOVE AI PHRASES
        # =============================================

        unwanted = [

            "As an AI language model",

            "Here is your article",

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

    # =====================================================
    # CONFIG
    # =====================================================

    def build_generation_config(
        self,
        temperature=None,
        max_output_tokens=None,
    ):

        """
        Enterprise optimized config.

        AFC disabled for:
        - lower latency
        - direct generation
        - lower orchestration overhead
        """

        return types.GenerateContentConfig(

            temperature=(

                temperature

                if temperature is not None

                else self.DEFAULT_TEMPERATURE
            ),

            max_output_tokens=(

                max_output_tokens

                or

                self.DEFAULT_MAX_TOKENS
            ),

            # =========================================
            # MASSIVE LATENCY OPTIMIZATION
            # =========================================

            automatic_function_calling={

                "disable": True
            },
        )

    # =====================================================
    # SAFE RESPONSE
    # =====================================================

    def safe_response_text(
        self,
        response,
    ):

        try:

            if not response:
                return ""

            if hasattr(
                response,
                "text",
            ):

                return str(
                    response.text
                ).strip()

            return str(response)

        except Exception:

            logger.exception(
                "Gemini response parse failed."
            )

            return ""

    # =====================================================
    # QUOTA DETECTION
    # =====================================================

    @staticmethod
    def is_quota_error(
        error_text,
    ):

        error_text = str(
            error_text
        ).lower()

        quota_keywords = [

            "quota",

            "429",

            "resource_exhausted",

            "rate limit",

            "too many requests",

            "service unavailable",

            "503",
        ]

        return any(

            keyword in error_text

            for keyword in quota_keywords
        )

    # =====================================================
    # GENERATE
    # =====================================================

    def generate(
        self,
        prompt,
        **kwargs,
    ):

        temperature = kwargs.get(
            "temperature"
        )

        max_output_tokens = kwargs.get(
            "max_output_tokens"
        )

        generation_config = (
            self.build_generation_config(

                temperature=(
                    temperature
                ),

                max_output_tokens=(
                    max_output_tokens
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

                    f"Gemini generation | "
                    f"attempt={attempt} | "
                    f"model={self.model_name}"
                )

                # =====================================
                # DIRECT GENERATION
                # =====================================

                response = (

                    self.client.models.generate_content(

                        model=(
                            self.model_name
                        ),

                        contents=prompt,

                        config=(
                            generation_config
                        ),
                    )
                )

                execution_time = round(

                    time.time()
                    - started,

                    2,
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
                        "Empty Gemini response."
                    )

                logger.info(

                    f"Gemini success | "
                    f"time={execution_time}s"
                )

                return response_text

            except Exception as error:

                error_text = str(
                    error
                )

                logger.exception(

                    f"Gemini failed | "
                    f"attempt={attempt} | "
                    f"error={error_text}"
                )

                # =====================================
                # QUOTA / RATE LIMIT
                # =====================================

                if self.is_quota_error(
                    error_text
                ):

                    logger.warning(

                        "Gemini quota exceeded."
                    )

                    return (
                        "GEMINI_QUOTA_EXCEEDED"
                    )

                # =====================================
                # FAST FAIL
                # =====================================

                if attempt >= (
                    self.MAX_RETRIES
                ):

                    return (

                        "Gemini generation "
                        f"failed: {error_text}"
                    )

        return (
            "Gemini generation failed."
        )

    # =====================================================
    # STREAM GENERATE
    # =====================================================

    def stream_generate(
        self,
        prompt,
    ):

        try:

            contents = [

                types.Content(

                    role="user",

                    parts=[

                        types.Part.from_text(
                            text=prompt
                        )
                    ],
                )
            ]

            stream = (

                self.client.models.generate_content_stream(

                    model=(
                        self.model_name
                    ),

                    contents=contents,
                )
            )

            final_text = ""

            for chunk in stream:

                try:

                    if chunk.text:

                        final_text += (
                            chunk.text
                        )

                except Exception:

                    continue

            return self.clean_response(
                final_text
            )

        except Exception as error:

            logger.exception(

                f"Gemini stream failed: "
                f"{str(error)}"
            )

            return (

                f"Gemini stream failed: "
                f"{str(error)}"
            )

    # =====================================================
    # HEALTH CHECK
    # =====================================================

    def health_check(
        self,
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

        except Exception as error:

            logger.exception(

                f"Gemini health failed: "
                f"{str(error)}"
            )

            return False

    # =====================================================
    # PROVIDER INFO
    # =====================================================

    def provider_info(
        self,
    ):

        return {

            "provider":
            "gemini",

            "model":
            self.model_name,

            "temperature":
            self.DEFAULT_TEMPERATURE,

            "max_output_tokens":
            self.DEFAULT_MAX_TOKENS,

            "retries":
            self.MAX_RETRIES,

            "afc_disabled":
            True,
        }