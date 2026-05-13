"""
OpenAI LLM provider.
"""

import logging

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

    def __init__(
        self,
        api_key,
        model_name="gpt-4o-mini",
    ):

        """
        Initialize OpenAI provider.
        """

        if not api_key:

            raise ValueError(
                "OPENAI_API_KEY missing."
            )

        self.client = OpenAI(
            api_key=api_key
        )

        self.model_name = (
            model_name
        )

        logger.info(

            f"OpenAI provider initialized "
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
        Clean OpenAI output.
        """

        if not text:

            return ""

        return str(
            text
        ).strip()

    # ==================================================
    # GENERATION CONFIG
    # ==================================================

    def build_generation_config(
        self,
        temperature=None,
        max_tokens=None,
    ):

        """
        Build OpenAI generation config.
        """

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

    # ==================================================
    # MAIN GENERATION
    # ==================================================

    def generate(
        self,
        prompt,
        **kwargs,
    ):

        """
        Generate OpenAI response.
        """

        try:

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

            logger.info(

                f"Generating OpenAI response "
                f"using model: "
                f"{self.model_name}"
            )

            response = (
                self.client.chat.completions.create(

                    model=self.model_name,

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

            response_text = ""

            if (

                response
                and response.choices
            ):

                response_text = (

                    response
                    .choices[0]
                    .message.content
                )

            response_text = (
                self.clean_response(
                    response_text
                )
            )

            if not response_text:

                logger.warning(

                    "OpenAI returned "
                    "empty response."
                )

                return (

                    "OpenAI returned "
                    "empty response."
                )

            logger.info(
                "OpenAI generation successful."
            )

            return response_text

        except Exception as error:

            logger.exception(

                f"OpenAI generation failed: "
                f"{str(error)}"
            )

            return (

                f"OpenAI generation failed: "
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

            "provider": "openai",

            "model": (
                self.model_name
            ),

            "temperature": (
                self.DEFAULT_TEMPERATURE
            ),

            "max_tokens": (
                self.DEFAULT_MAX_TOKENS
            ),
        }