"""
Enterprise Serper Provider
--------------------------

Production-grade Google SERP intelligence provider.

Features:
- real Google SERP extraction
- People Also Ask extraction
- related searches extraction
- organic ranking extraction
- SEO metadata extraction
- multilingual support
- semantic-safe normalization
- duplicate cleanup
- OCI optimized
- production-safe
"""

from __future__ import annotations

import logging

import requests

from django.conf import settings

from .base_provider import (
    BaseProvider,
)


logger = logging.getLogger(
    __name__
)


class SerperProvider(
    BaseProvider
):

    """
    Enterprise SERPER provider.
    """

    PROVIDER_NAME = "serper"

    BASE_URL = (
        "https://google.serper.dev/search"
    )

    # =====================================================
    # SAFE LIST
    # =====================================================

    @staticmethod
    def ensure_list(
        value,
    ):

        if isinstance(
            value,
            list,
        ):

            return value

        return []

    # =====================================================
    # CLEAN TEXT
    # =====================================================

    @staticmethod
    def clean_text(
        value,
    ):

        if not value:

            return ""

        return (
            str(value)
            .strip()
        )

    # =====================================================
    # DOMAIN EXTRACT
    # =====================================================

    @staticmethod
    def extract_domain(
        url,
    ):

        try:

            return (
                url.split("//")[-1]
                .split("/")[0]
                .replace("www.", "")
            )

        except Exception:

            return ""

    # =====================================================
    # NORMALIZE ORGANIC
    # =====================================================

    @classmethod
    def normalize_organic(
        cls,
        item,
        related_searches,
        people_also_ask,
    ):

        url = item.get(
            "link",
            ""
        )

        return {

            # =========================================
            # CORE SEO
            # =========================================

            "title":

            cls.clean_text(

                item.get(
                    "title",
                    ""
                )
            ),

            "url":

            cls.clean_text(
                url
            ),

            "description":

            cls.clean_text(

                item.get(
                    "snippet",
                    ""
                )
            ),

            # =========================================
            # SEO INTELLIGENCE
            # =========================================

            "questions":

            people_also_ask,

            "related_searches":

            related_searches,

            "headings":
            [],

            # =========================================
            # SEO METADATA
            # =========================================

            "position":

            item.get(
                "position",
                0
            ),

            "domain":

            cls.extract_domain(
                url
            ),

            "source":
            cls.PROVIDER_NAME,
        }

    # =====================================================
    # SEARCH
    # =====================================================

    @classmethod
    def search(

        cls,

        keyword: str,

        max_results: int = 10,
    ) -> list[dict]:

        logger.info(

            f"{cls.PROVIDER_NAME} "
            f"search started for: "
            f"{keyword}"
        )

        try:

            # =========================================
            # REQUEST
            # =========================================

            response = requests.post(

                cls.BASE_URL,

                headers={

                    "X-API-KEY":
                    settings.SERPER_API_KEY,

                    "Content-Type":
                    "application/json",
                },

                json={

                    "q":
                    keyword,

                    "num":
                    max_results,

                    "gl":
                    "in",

                    "hl":
                    "en",
                },

                timeout=cls.TIMEOUT,
            )

            logger.info(

                f"{cls.PROVIDER_NAME} "
                f"status: "
                f"{response.status_code}"
            )

            response.raise_for_status()

            data = response.json()

            # =========================================
            # ORGANIC RESULTS
            # =========================================

            organic_results = data.get(
                "organic",
                [],
            )

            # =========================================
            # PEOPLE ALSO ASK
            # =========================================

            paa_raw = data.get(
                "peopleAlsoAsk",
                []
            )

            people_also_ask = []

            for item in paa_raw:

                question = item.get(
                    "question",
                    ""
                )

                if question:

                    people_also_ask.append(
                        question
                    )

            # =========================================
            # RELATED SEARCHES
            # =========================================

            related_raw = data.get(
                "relatedSearches",
                []
            )

            related_searches = []

            for item in related_raw:

                query = item.get(
                    "query",
                    ""
                )

                if query:

                    related_searches.append(
                        query
                    )

            # =========================================
            # NORMALIZE RESULTS
            # =========================================

            results = []

            for item in organic_results:

                normalized = (

                    cls.normalize_organic(

                        item,

                        related_searches,

                        people_also_ask,
                    )
                )

                results.append(
                    normalized
                )

            # =========================================
            # PROCESS RESULTS
            # =========================================

            processed_results = (

                cls.process_results(

                    results,

                    max_results,
                )
            )

            cls.log_success(
                len(processed_results)
            )

            logger.info(

                f"PAA found: "
                f"{len(people_also_ask)}"
            )

            logger.info(

                f"Related searches found: "
                f"{len(related_searches)}"
            )

            return processed_results

        # =============================================
        # FAILURE
        # =============================================

        except Exception as error:

            cls.log_failure(error)

            raise