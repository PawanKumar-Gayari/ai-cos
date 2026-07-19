"""
Enterprise Ollama Local LLM Provider
------------------------------------

Production-grade Ollama provider.

Features:
- OCI optimized
- retry-safe requests
- streaming-ready architecture
- timeout protection
- markdown-safe cleanup
- local inference support
- model switching
- production-safe orchestration
"""

from __future__ import annotations

import logging
import re
import time

import requests

from requests.exceptions import (

    ConnectionError,

    RequestException,

    Timeout,
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

    DEFAULT_MAX_TOKENS = 2048

    REQUEST_TIMEOUT = 180

    HEALTH_TIMEOUT = 5

    MAX_RETRIES = 3

    RETRY_DELAY = 2

    # =============================================
    # INIT
    # =============================================

    def __init__(
        self,
        base_url="http://localhost:11434",
        model="tinyllama",
    ):

        self.base_url = (
            base_url.rstrip("/")
        )

        self.model = model

        self.session = (
            requests.Session()
        )

        logger.info(

            f"Ollama initialized | "
            f"model={model}"
        )

    # =============================================
    # ENDPOINT
    # =============================================

    def endpoint(
        self
    ):

        return (

            f"{self.base_url}"
            "/api/generate"
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
        # REMOVE EXCESSIVE NEWLINES
        # =========================================

        text = re.sub(

            r"\n{4,}",

            "\n\n",

            text,
        )

        return text.strip()

    # =============================================
    # PAYLOAD
    # =============================================

    def payload(
        self,
        prompt,
        **kwargs,
    ):

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

    # =============================================
    # SAFE RESPONSE
    # =============================================

    def safe_response_text(
        self,
        data,
    ):

        try:

            if not isinstance(
                data,
                dict,
            ):

                return ""

            return str(

                data.get(
                    "response",
                    ""
                )
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

        for attempt in range(

            1,

            self.MAX_RETRIES + 1,
        ):

            try:

                logger.info(

                    f"Ollama generate | "
                    f"attempt={attempt} | "
                    f"model={self.model}"
                )

                started = time.time()

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

                    self.clean_response(

                        self.safe_response_text(
                            data
                        )
                    )
                )

                if not response_text:

                    raise ValueError(
                        "Empty Ollama response."
                    )

                execution_time = round(

                    time.time()
                    - started,

                    2,
                )

                logger.info(

                    f"Ollama success | "
                    f"time={execution_time}s"
                )

                return response_text

            except Timeout:

                logger.warning(
                    "Ollama timeout."
                )

            except ConnectionError:

                logger.warning(
                    "Ollama unavailable."
                )

            except RequestException as error:

                logger.exception(

                    f"Ollama request failed: "
                    f"{str(error)}"
                )

            except Exception as error:

                logger.exception(

                    f"Ollama error: "
                    f"{str(error)}"
                )

            if attempt < (
                self.MAX_RETRIES
            ):

                time.sleep(
                    self.RETRY_DELAY
                )

        return (
            "Ollama generation failed."
        )

    # =============================================
    # STREAM GENERATE
    # =============================================

    def stream_generate(
        self,
        prompt,
        **kwargs,
    ):

        try:

            payload = self.payload(

                prompt,

                **kwargs,
            )

            payload["stream"] = True

            response = (
                self.session.post(

                    self.endpoint(),

                    json=payload,

                    timeout=(
                        self.REQUEST_TIMEOUT
                    ),

                    stream=True,
                )
            )

            response.raise_for_status()

            final_text = ""

            for line in (
                response.iter_lines()
            ):

                try:

                    if line:

                        decoded = (
                            line.decode(
                                "utf-8"
                            )
                        )

                        final_text += (
                            decoded
                        )

                except Exception:

                    continue

            return self.clean_response(
                final_text
            )

        except Exception as error:

            logger.exception(

                f"Ollama stream failed: "
                f"{str(error)}"
            )

            return (
                "Ollama stream failed."
            )

    # =============================================
    # AVAILABLE MODELS
    # =============================================

    def available_models(
        self
    ):

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

    # =============================================
    # HEALTH CHECK
    # =============================================

    def health_check(
        self
    ):

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

    # =============================================
    # PROVIDER INFO
    # =============================================

    def provider_info(
        self
    ):

        return {

            "provider":
            self.provider_name,

            "model":
            self.model,

            "local":
            True,

            "healthy":
            self.health_check(),

            "base_url":
            self.base_url,

            "max_retries":
            self.MAX_RETRIES,
        }

    # =============================================
    # SWITCH MODEL
    # =============================================

    def switch_model(
        self,
        model,
    ):

        self.model = str(
            model
        ).strip()

        logger.info(

            f"Ollama model switched "
            f"to: {model}"
        )

        return {

            "status": "updated",

            "model": model,
        }