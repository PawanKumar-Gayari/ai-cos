"""
Gemini LLM provider.
"""

import logging

import google.generativeai as genai

from apps.llm.base_provider import (
    BaseProvider
)


logger = logging.getLogger(
    __name__
)


class GeminiProvider(
    BaseProvider
):

    DEFAULT_TEMPERATURE = 0.7

    DEFAULT_MAX_TOKENS = 4096

    def __init__(
        self,
        api_key,
        model_name="gemini-2.0-flash",
    ):

        """
        Initialize Gemini provider.
        """

        if not api_key:

            raise ValueError(
                "GEMINI_API_KEY is missing."
            )

        self.api_key = api_key

        self.model_name = (
            model_name
        )

        # ==========================================
        # CONFIGURE GEMINI
        # ==========================================

        genai.configure(
            api_key=api_key
        )

        # ==========================================
        # LOAD MODEL
        # ==========================================

        self.model = (
            genai.GenerativeModel(
                model_name
            )
        )

        logger.info(

            f"Gemini provider initialized "
            f"with model: {model_name}"
        )

    # ==================================================
    # CLEAN RESPONSE
    # ==================================================

    def clean_response(
        self,
        text,
    ):

        """
        Clean Gemini output.
        """

        if not text:

            return ""

        text = str(
            text
        ).strip()

        return text

    # ==================================================
    # GENERATION CONFIG
    # ==================================================

    def build_generation_config(
        self,
        temperature=None,
        max_output_tokens=None,
    ):

        """
        Build Gemini generation config.
        """

        return {

            "temperature": (

                temperature

                or

                self.DEFAULT_TEMPERATURE
            ),

            "max_output_tokens": (

                max_output_tokens

                or

                self.DEFAULT_MAX_TOKENS
            ),
        }

    # ==================================================
    # MAIN GENERATION
    # ==================================================

    def generate(
        self,
        prompt,
        **kwargs,
    ):

        """
        Generate Gemini response.
        """

        try:

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

            logger.info(

                f"Generating Gemini response "
                f"using model: "
                f"{self.model_name}"
            )

            response = (
                self.model.generate_content(

                    prompt,

                    generation_config=(
                        generation_config
                    ),
                )
            )

            response_text = ""

            if hasattr(
                response,
                "text"
            ):

                response_text = (
                    response.text
                )

            elif hasattr(
                response,
                "candidates"
            ):

                try:

                    response_text = (

                        response.candidates[0]
                        .content.parts[0]
                        .text
                    )

                except Exception:

                    response_text = ""

            response_text = (
                self.clean_response(
                    response_text
                )
            )

            if not response_text:

                logger.warning(

                    "Gemini returned "
                    "empty response."
                )

                return (
                    "Gemini returned "
                    "empty response."
                )

            logger.info(
                "Gemini generation successful."
            )

            return response_text

        except Exception as error:

            logger.exception(

                f"Gemini generation failed: "
                f"{str(error)}"
            )

            return (

                f"Gemini generation failed: "
                f"{str(error)}"
            )

    # ==================================================
    # PROVIDER INFO
    # ==================================================

    def provider_info(
        self
    ):

        """
        Return provider information.
        """

        return {

            "provider": "gemini",

            "model": (
                self.model_name
            ),

            "temperature": (
                self.DEFAULT_TEMPERATURE
            ),

            "max_output_tokens": (
                self.DEFAULT_MAX_TOKENS
            ),
        }