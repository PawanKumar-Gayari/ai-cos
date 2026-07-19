"""
Enterprise Base Search Provider
-------------------------------

Production-grade provider foundation layer.

Features:
- provider standardization
- enterprise normalization
- SEO-safe validation
- duplicate cleanup
- spam filtering
- multilingual support
- semantic-safe extraction
- domain extraction
- quality scoring
- heading support
- People Also Ask support
- related searches support
- OCI optimized
- production-safe
- scalable architecture
"""

from __future__ import annotations

import logging
import re

from typing import (
    Any,
)


logger = logging.getLogger(
    __name__
)


class BaseProvider:

    """
    Enterprise provider foundation.
    """

    # =====================================================
    # PROVIDER CONFIG
    # =====================================================

    PROVIDER_NAME = "base"

    TIMEOUT = 20

    MAX_RESULTS = 10

    # =====================================================
    # BLOCKED TERMS
    # =====================================================

    BLOCKED_TERMS = {

        # spam
        "torrent",
        "crack",
        "hack",

        # adult
        "porn",
        "sex",

        # junk SEO
        "tutorial",
        "guide",
        "tips",
        "tools",
        "review",
        "reviews",
    }

    # =====================================================
    # SAFE STRING
    # =====================================================

    @staticmethod
    def safe_string(
        value: Any,
    ) -> str:

        if value is None:

            return ""

        return (
            str(value)
            .strip()
        )

    # =====================================================
    # SAFE LIST
    # =====================================================

    @staticmethod
    def ensure_list(
        value: Any,
    ) -> list:

        if isinstance(
            value,
            list,
        ):

            return value

        return []

    # =====================================================
    # CLEAN TEXT
    # =====================================================

    @classmethod
    def clean_text(
        cls,
        value: Any,
    ) -> str:

        value = cls.safe_string(
            value
        )

        if not value:

            return ""

        # preserve multilingual text
        value = re.sub(

            r"[^\w\s\u0900-\u097F]",

            " ",

            value,
        )

        value = re.sub(

            r"\s+",

            " ",

            value,
        )

        return value.strip()

    # =====================================================
    # EXTRACT DOMAIN
    # =====================================================

    @staticmethod
    def extract_domain(
        url: str,
    ) -> str:

        try:

            return (

                url.split("//")[-1]
                .split("/")[0]
                .replace("www.", "")
                .strip()
            )

        except Exception:

            return ""

    # =====================================================
    # NORMALIZE RESULT
    # =====================================================

    @classmethod
    def normalize_result(

        cls,

        title: str = "",

        url: str = "",

        description: str = "",

        questions: list | None = None,

        related_searches: list | None = None,

        headings: list | None = None,

        position: int = 0,

        source: str = "",
    ) -> dict[str, Any]:

        title = cls.clean_text(
            title
        )

        url = cls.safe_string(
            url
        )

        description = cls.clean_text(
            description
        )

        return {

            # =========================================
            # CORE SEO DATA
            # =========================================

            "title":
            title,

            "url":
            url,

            "description":
            description,

            # =========================================
            # SEO INTELLIGENCE
            # =========================================

            "questions":

            cls.ensure_list(
                questions
            ),

            "related_searches":

            cls.ensure_list(
                related_searches
            ),

            "headings":

            cls.ensure_list(
                headings
            ),

            # =========================================
            # SEO METADATA
            # =========================================

            "position":
            position,

            "domain":

            cls.extract_domain(
                url
            ),

            "source":

            source
            or cls.PROVIDER_NAME,
        }

    # =====================================================
    # SPAM CHECK
    # =====================================================

    @classmethod
    def is_spam(
        cls,
        text: str,
    ) -> bool:

        text = (
            cls.clean_text(
                text
            )
            .lower()
        )

        return any(

            bad in text

            for bad in (
                cls.BLOCKED_TERMS
            )
        )

    # =====================================================
    # VALIDATE RESULT
    # =====================================================

    @classmethod
    def is_valid_result(
        cls,
        result: dict[str, Any],
    ) -> bool:

        if not result:

            return False

        title = cls.clean_text(

            result.get(
                "title",
            )
        )

        url = cls.safe_string(

            result.get(
                "url",
            )
        )

        description = cls.clean_text(

            result.get(
                "description",
            )
        )

        # =========================================
        # REQUIRED TITLE
        # =========================================

        if not title:

            return False

        if len(title) < 3:

            return False

        # =========================================
        # SPAM FILTER
        # =========================================

        if cls.is_spam(
            title
        ):

            return False

        # =========================================
        # VALID URL
        # =========================================

        if url:

            if not url.startswith(
                (
                    "http://",
                    "https://",
                )
            ):

                return False

        # =========================================
        # DESCRIPTION QUALITY
        # =========================================

        if description:

            if len(description) < 10:

                return False

        return True

    # =====================================================
    # QUALITY SCORE
    # =====================================================

    @classmethod
    def quality_score(
        cls,
        result: dict[str, Any],
    ) -> int:

        score = 0

        # title
        if result.get(
            "title"
        ):

            score += 3

        # description
        if result.get(
            "description"
        ):

            score += 2

        # url
        if result.get(
            "url"
        ):

            score += 1

        # PAA
        if result.get(
            "questions"
        ):

            score += 5

        # related
        if result.get(
            "related_searches"
        ):

            score += 4

        # headings
        if result.get(
            "headings"
        ):

            score += 3

        return score

    # =====================================================
    # CLEAN RESULTS
    # =====================================================

    @classmethod
    def clean_results(
        cls,
        results: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:

        cleaned = []

        seen_urls = set()

        seen_titles = set()

        for result in results:

            # =========================================
            # VALIDATION
            # =========================================

            if not cls.is_valid_result(
                result
            ):

                continue

            url = cls.safe_string(

                result.get(
                    "url",
                )
            )

            title = (
                cls.clean_text(

                    result.get(
                        "title",
                        "",
                    )
                )
                .lower()
            )

            # =========================================
            # DUPLICATE URL
            # =========================================

            if url and (
                url in seen_urls
            ):

                continue

            # =========================================
            # DUPLICATE TITLE
            # =========================================

            if title in seen_titles:

                continue

            if url:

                seen_urls.add(
                    url
                )

            seen_titles.add(
                title
            )

            cleaned.append(
                result
            )

        logger.info(

            f"{cls.PROVIDER_NAME} "
            f"cleaned "
            f"{len(cleaned)} results."
        )

        return cleaned

    # =====================================================
    # LIMIT RESULTS
    # =====================================================

    @classmethod
    def limit_results(
        cls,
        results: list[dict[str, Any]],
        max_results: int,
    ) -> list[dict[str, Any]]:

        return results[
            :max_results
        ]

    # =====================================================
    # SORT RESULTS
    # =====================================================

    @classmethod
    def sort_results(
        cls,
        results: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:

        return sorted(

            results,

            key=lambda item:

            cls.quality_score(
                item
            ),

            reverse=True,
        )

    # =====================================================
    # PROCESS RESULTS
    # =====================================================

    @classmethod
    def process_results(

        cls,

        results: list[dict[str, Any]],

        max_results: int,
    ) -> list[dict[str, Any]]:

        # =============================================
        # CLEAN
        # =============================================

        cleaned = cls.clean_results(
            results
        )

        # =============================================
        # SORT
        # =============================================

        sorted_results = (
            cls.sort_results(
                cleaned
            )
        )

        # =============================================
        # LIMIT
        # =============================================

        limited = cls.limit_results(

            sorted_results,

            max_results,
        )

        logger.info(

            f"{cls.PROVIDER_NAME} "
            f"processed "
            f"{len(limited)} results."
        )

        return limited

    # =====================================================
    # LOG SUCCESS
    # =====================================================

    @classmethod
    def log_success(
        cls,
        total_results: int,
    ) -> None:

        logger.info(

            f"{cls.PROVIDER_NAME} "
            f"success with "
            f"{total_results} results."
        )

    # =====================================================
    # LOG FAILURE
    # =====================================================

    @classmethod
    def log_failure(
        cls,
        error: Exception,
    ) -> None:

        logger.exception(

            f"{cls.PROVIDER_NAME} "
            f"failed: "
            f"{str(error)}"
        )