"""
Enterprise generator engine for AI COS.
"""

import logging
import time

from apps.engine.services.generation_service import (
    GenerationService,
)


logger = logging.getLogger(
    __name__
)


class GeneratorEngine:

    MAX_RETRIES = 3

    MIN_CONTENT_LENGTH = 300

    BLOCKED_PATTERNS = [

        "ignore previous instructions",

        "system prompt",

        "developer instructions",

        "reveal hidden prompt",
    ]

    def __init__(
        self
    ):

        # ==========================================
        # GENERATION SERVICE
        # ==========================================

        self.generation_service = (
            GenerationService()
        )

    # ==================================================
    # SAFE TEXT
    # ==================================================

    def safe_text(
        self,
        text,
    ):

        """
        Validate unsafe prompt patterns.
        """

        if not text:

            return False

        lowered = (
            str(text)
            .lower()
        )

        for pattern in (
            self.BLOCKED_PATTERNS
        ):

            if pattern in lowered:

                return False

        return True

    # ==================================================
    # NORMALIZE KEYWORD
    # ==================================================

    def normalize_keyword(
        self,
        keyword,
    ):

        """
        Normalize keyword input.
        """

        if not keyword:

            return ""

        keyword = str(
            keyword
        ).strip()

        return keyword[:300]

    # ==================================================
    # DEFAULT RESPONSE
    # ==================================================

    def default_response(
        self,
        keyword,
        content,
    ):

        """
        Default structured response.
        """

        return {

            "title": (
                f"Complete Guide About "
                f"{keyword}"
            ),

            "meta_description": (

                f"Learn everything about "
                f"{keyword} in this "
                f"detailed guide."
            ),

            "content": str(
                content
            ),

            "faq": "",

            "conclusion": (

                f"{keyword} is an "
                f"important topic."
            ),

            "seo_score": 80,

            "verified": True,
        }

    # ==================================================
    # VALIDATE RESPONSE
    # ==================================================

    def validate_response(
        self,
        response,
    ):

        """
        Validate generated response.
        """

        if not response:

            raise Exception(
                "Generated response empty"
            )

        if not isinstance(
            response,
            dict,
        ):

            raise Exception(
                "Invalid response format"
            )

        content = response.get(
            "content",
            ""
        )

        if not content:

            raise Exception(
                "Generated content missing"
            )

        if len(
            content.strip()
        ) < self.MIN_CONTENT_LENGTH:

            raise Exception(
                "Generated content too short"
            )

        return True

    # ==================================================
    # CLEAN RESPONSE
    # ==================================================

    def clean_response(
        self,
        keyword,
        response,
    ):

        """
        Normalize response payload.
        """

        response.setdefault(

            "title",

            f"Complete Guide About "
            f"{keyword}"
        )

        response.setdefault(

            "meta_description",

            f"Learn everything about "
            f"{keyword} in this guide."
        )

        response.setdefault(
            "faq",
            ""
        )

        response.setdefault(
            "conclusion",
            ""
        )

        response.setdefault(
            "seo_score",
            80
        )

        response.setdefault(
            "verified",
            True
        )

        response.setdefault(
            "generation_time",
            round(
                time.time(),
                2,
            )
        )

        return response

    # ==================================================
    # GENERATE
    # ==================================================

    def generate(
        self,
        keyword_data
    ):

        """
        Main generation pipeline.
        """

        start_time = time.time()

        # ==========================================
        # VALIDATE INPUT
        # ==========================================

        if not keyword_data:

            raise Exception(
                "Keyword data required"
            )

        keyword = (
            self.normalize_keyword(

                keyword_data.get(
                    "keyword"
                )
            )
        )

        if not keyword:

            raise Exception(
                "Keyword required"
            )

        if not self.safe_text(
            keyword
        ):

            raise Exception(
                "Unsafe keyword detected"
            )

        logger.info(

            f"Starting generation "
            f"for keyword: {keyword}"
        )

        generated_content = None

        last_error = None

        # ==========================================
        # RETRY PIPELINE
        # ==========================================

        for attempt in range(
            self.MAX_RETRIES
        ):

            try:

                logger.info(

                    f"Generation attempt "
                    f"{attempt + 1}"
                )

                result = (

                    self.generation_service.generate(
                        keyword_data
                    )
                )

                # ==================================
                # NORMALIZE RESPONSE
                # ==================================

                if not isinstance(
                    result,
                    dict,
                ):

                    result = (
                        self.default_response(

                            keyword,

                            result,
                        )
                    )

                # ==================================
                # VALIDATE RESPONSE
                # ==================================

                self.validate_response(
                    result
                )

                generated_content = (
                    self.clean_response(

                        keyword,

                        result,
                    )
                )

                break

            except Exception as error:

                last_error = error

                logger.warning(

                    f"Generation attempt "
                    f"failed: {str(error)}"
                )

                time.sleep(
                    1 + attempt
                )

        # ==========================================
        # FINAL FAILURE
        # ==========================================

        if not generated_content:

            logger.exception(

                f"Generation failed for "
                f"{keyword}"
            )

            raise Exception(

                f"Content generation failed: "
                f"{str(last_error)}"
            )

        # ==========================================
        # METADATA
        # ==========================================

        generated_content[
            "engine_metadata"
        ] = {

            "engine": (
                "generator_engine"
            ),

            "version": "2.0.0",

            "retries": (
                self.MAX_RETRIES
            ),

            "execution_time": round(

                time.time()
                - start_time,

                2,
            ),
        }

        logger.info(

            f"Generation completed "
            f"for keyword: {keyword}"
        )

        return generated_content