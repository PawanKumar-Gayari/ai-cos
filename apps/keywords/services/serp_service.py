"""
Enterprise SERP Intelligence Service
------------------------------------

Production-grade SEO SERP intelligence layer.

Features:
- SERPER integration
- SERPAPI integration
- provider fallback routing
- People Also Ask extraction
- related searches extraction
- organic result parsing
- competitor intelligence
- heading extraction ready
- multilingual SEO analysis
- semantic-ready architecture
- OCI optimized
- production-safe
"""

from __future__ import annotations

import logging

from typing import (
    Any,
)

from .providers.search_router import (
    SearchRouter,
)


logger = logging.getLogger(
    __name__
)


class SERPService:

    """
    Enterprise SERP intelligence service.
    """

    DEFAULT_MAX_RESULTS = 10

    # =====================================================
    # CLEAN TEXT
    # =====================================================

    @staticmethod
    def clean_text(
        value: Any,
    ) -> str:

        if not value:

            return ""

        return (
            str(value)
            .strip()
        )

    # =====================================================
    # ENSURE LIST
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
    # NORMALIZE ORGANIC RESULT
    # =====================================================

    @classmethod
    def normalize_result(
        cls,
        item: dict,
    ) -> dict:

        return {

            # =========================================
            # CORE SEO DATA
            # =========================================

            "title":

            cls.clean_text(

                item.get(
                    "title",
                    ""
                )
            ),

            "description":

            cls.clean_text(

                item.get(
                    "description",

                    item.get(
                        "snippet",
                        ""
                    )
                )
            ),

            "url":

            cls.clean_text(

                item.get(
                    "url",

                    item.get(
                        "link",
                        ""
                    )
                )
            ),

            # =========================================
            # SEO INTELLIGENCE
            # =========================================

            "questions":

            cls.ensure_list(

                item.get(
                    "questions",

                    item.get(
                        "peopleAlsoAsk",
                        []
                    )
                )
            ),

            "related_searches":

            cls.ensure_list(

                item.get(
                    "related_searches",

                    item.get(
                        "relatedSearches",
                        []
                    )
                )
            ),

            "headings":

            cls.ensure_list(

                item.get(
                    "headings",
                    []
                )
            ),

            # =========================================
            # EXTRA SEO SIGNALS
            # =========================================

            "position":

            item.get(
                "position",
                0
            ),

            "domain":

            cls.clean_text(

                item.get(
                    "domain",
                    ""
                )
            ),

            "source":

            cls.clean_text(

                item.get(
                    "source",
                    ""
                )
            ),
        }

    # =====================================================
    # NORMALIZE RESULTS
    # =====================================================

    @classmethod
    def normalize_results(
        cls,
        results: list[dict],
    ) -> list[dict]:

        cleaned_results = []

        for item in results:

            try:

                normalized = (
                    cls.normalize_result(
                        item
                    )
                )

                if not normalized.get(
                    "title"
                ):

                    continue

                cleaned_results.append(
                    normalized
                )

            except Exception:

                continue

        return cleaned_results

    # =====================================================
    # SEARCH
    # =====================================================

    @classmethod
    def search(

        cls,

        keyword: str,

        max_results: int = 10,
    ) -> list[dict[str, Any]]:

        # =============================================
        # SAFE KEYWORD
        # =============================================

        keyword = str(
            keyword
        ).strip()

        if not keyword:

            logger.warning(
                "Empty SERP keyword received."
            )

            return []

        # =============================================
        # SAFE MAX RESULTS
        # =============================================

        if max_results <= 0:

            max_results = (
                cls.DEFAULT_MAX_RESULTS
            )

        logger.info(

            f"SERP intelligence started "
            f"for keyword: "
            f"{keyword}"
        )

        try:

            # =========================================
            # PROVIDER SEARCH
            # =========================================

            raw_results = (

                SearchRouter.search(

                    keyword=keyword,

                    max_results=max_results,
                )
            )

            raw_results = (
                cls.ensure_list(
                    raw_results
                )
            )

            logger.info(

                f"Raw SERP results: "
                f"{len(raw_results)}"
            )

            # =========================================
            # NORMALIZE RESULTS
            # =========================================

            normalized_results = (

                cls.normalize_results(
                    raw_results
                )
            )

            logger.info(

                f"Normalized SERP results: "
                f"{len(normalized_results)}"
            )

            return normalized_results

        # =============================================
        # FAILURE
        # =============================================

        except Exception as error:

            logger.exception(

                f"SERP intelligence failed: "
                f"{str(error)}"
            )

            return []

    # =====================================================
    # GET PAA QUESTIONS
    # =====================================================

    @classmethod
    def extract_people_also_ask(
        cls,
        results: list[dict],
    ) -> list[str]:

        questions = []

        for item in results:

            paa = item.get(
                "questions",
                []
            )

            if not isinstance(
                paa,
                list,
            ):

                continue

            questions.extend(
                paa
            )

        return list(
            set(questions)
        )

    # =====================================================
    # GET RELATED SEARCHES
    # =====================================================

    @classmethod
    def extract_related_searches(
        cls,
        results: list[dict],
    ) -> list[str]:

        related = []

        for item in results:

            searches = item.get(
                "related_searches",
                []
            )

            if not isinstance(
                searches,
                list,
            ):

                continue

            related.extend(
                searches
            )

        return list(
            set(related)
        )

    # =====================================================
    # GET TITLES
    # =====================================================

    @classmethod
    def extract_titles(
        cls,
        results: list[dict],
    ) -> list[str]:

        titles = []

        for item in results:

            title = item.get(
                "title",
                ""
            )

            if title:

                titles.append(
                    title
                )

        return titles

    # =====================================================
    # GET DOMAINS
    # =====================================================

    @classmethod
    def extract_domains(
        cls,
        results: list[dict],
    ) -> list[str]:

        domains = []

        for item in results:

            domain = item.get(
                "domain",
                ""
            )

            if domain:

                domains.append(
                    domain
                )

        return list(
            set(domains)
        )

    # =====================================================
    # AVAILABLE PROVIDERS
    # =====================================================

    @staticmethod
    def available_providers(
    ) -> list[str]:

        return (
            SearchRouter
            .available_providers()
        )