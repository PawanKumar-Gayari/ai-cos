"""
Enterprise Ollama local LLM provider.
"""

import logging

import requests

from requests.exceptions import (
    RequestException,
    Timeout,
    ConnectionError,
)

from apps.llm.base_provider import (
    BaseProvider
)


logger = logging.getLogger(
    __name__
)


class OllamaProvider(
    BaseProvider
):

    provider_name = (
        "ollama"
    )

    DEFAULT_TEMPERATURE = 0.7

    DEFAULT_MAX_TOKENS = 512

    REQUEST_TIMEOUT = 60

    HEALTH_TIMEOUT = 5

    def __init__(
        self,
        base_url="http://localhost:11434",
        model="tinyllama",
    ):

        """
        Initialize Ollama provider.
        """

        self.base_url = (
            base_url.rstrip("/")
        )

        self.model = model

        # ==========================================
        # REQUEST SESSION
        # ==========================================

        self.session = (
            requests.Session()
        )

        logger.info(

            f"Ollama provider initialized "
            f"with model: {model}"
        )

    # ==================================================
    # ENDPOINT
    # ==================================================

    def endpoint(
        self
    ):

        """
        Ollama generate endpoint.
        """

        return (

            f"{self.base_url}"
            "/api/generate"
        )

    # ==================================================
    # CLEAN RESPONSE
    # ==================================================

    def clean_response(
        self,
        text,
    ):

        """
        Clean Ollama output.
        """

        if not text:

            return ""

        return str(
            text
        ).strip()

    # ==================================================
    # PAYLOAD
    # ==================================================

    def payload(
        self,
        prompt,
        **kwargs,
    ):

        """
        Build Ollama request payload.
        """

        return {

            "model": (
                self.model
            ),

            "prompt": prompt,

            "stream": False,

            "options": {

                "temperature": (

                    kwargs.get(
                        "temperature",
                        self.DEFAULT_TEMPERATURE,
                    )
                ),

                "num_predict": (

                    kwargs.get(
                        "max_tokens",
                        self.DEFAULT_MAX_TOKENS,
                    )
                ),
            },
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
        Generate Ollama response.
        """

        try:

            logger.info(

                f"Generating Ollama response "
                f"using model: {self.model}"
            )

            response = (
                self.session.post(

                    self.endpoint(),

                    json=self.payload(

                        prompt,

                        **kwargs,
                    ),

                    timeout=(
                        self.REQUEST_TIMEOUT
                    ),
                )
            )

            response.raise_for_status()

            data = response.json()

            response_text = (
                data.get(
                    "response",
                    ""
                )
            )

            response_text = (
                self.clean_response(
                    response_text
                )
            )

            if not response_text:

                logger.warning(

                    "Ollama returned "
                    "empty response."
                )

                return (

                    "Ollama returned "
                    "empty response."
                )

            logger.info(
                "Ollama generation successful."
            )

            return response_text

        except Timeout:

            logger.warning(
                "Ollama request timed out."
            )

            return (
                "Ollama generation failed: timeout"
            )

        except ConnectionError:

            logger.warning(
                "Ollama server unavailable."
            )

            return (
                "Ollama generation failed: "
                "server unavailable"
            )

        except RequestException as error:

            logger.exception(

                f"Ollama request failed: "
                f"{str(error)}"
            )

            return (

                f"Ollama generation failed: "
                f"{str(error)}"
            )

        except Exception as error:

            logger.exception(

                f"Ollama unexpected error: "
                f"{str(error)}"
            )

            return (

                f"Ollama generation failed: "
                f"{str(error)}"
            )

    # ==================================================
    # AVAILABLE MODELS
    # ==================================================

    def available_models(
        self
    ):

        """
        Return installed Ollama models.
        """

        try:

            response = (
                self.session.get(

                    f"{self.base_url}/api/tags",

                    timeout=(
                        self.HEALTH_TIMEOUT
                    ),
                )
            )

            response.raise_for_status()

            data = response.json()

            return data.get(
                "models",
                []
            )

        except Exception:

            return []

    # ==================================================
    # HEALTH CHECK
    # ==================================================

    def health_check(
        self
    ):

        """
        Check Ollama availability.
        """

        try:

            response = (
                self.session.get(

                    f"{self.base_url}/api/tags",

                    timeout=(
                        self.HEALTH_TIMEOUT
                    ),
                )
            )

            return (
                response.status_code == 200
            )

        except Exception:

            return False

    # ==================================================
    # PROVIDER INFO
    # ==================================================

    def provider_info(
        self
    ):

        """
        Return provider metadata.
        """

        return {

            "provider": (
                self.provider_name
            ),

            "model": (
                self.model
            ),

            "local": True,

            "healthy": (
                self.health_check()
            ),

            "base_url": (
                self.base_url
            ),
        }

    # ==================================================
    # SWITCH MODEL
    # ==================================================

    def switch_model(
        self,
        model,
    ):

        """
        Dynamically switch model.
        """

        self.model = model

        logger.info(

            f"Ollama model switched "
            f"to: {model}"
        )

        return {

            "status": "updated",

            "model": model,
        }