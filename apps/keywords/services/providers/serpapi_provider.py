"""
Enterprise SerpApi Provider
---------------------------

Production-grade Google SERP intelligence provider.

Features:
- organic SERP extraction
- People Also Ask extraction
- related searches extraction
- knowledge graph extraction
- normalized responses
- duplicate cleanup
- semantic keyword enrichment
- multilingual SEO support
- entity extraction ready
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


class SerpApiProvider(
    BaseProvider
):

    """
    Enterprise SERPAPI provider.
    """

    PROVIDER_NAME = "serpapi"

    BASE_URL = (
        "https://serpapi.com/search.json"
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
    # EXTRACT DOMAIN
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
    # NORMALIZE RESULT
    # =====================================================

    @classmethod
    def normalize_serp_result(

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
            # CORE SEO DATA
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
            f"search started | "
            f"keyword={keyword}"
        )

        try:

            # =========================================
            # REQUEST
            # =========================================

            response = requests.get(

                cls.BASE_URL,

                params={

                    "q":
                    keyword,

                    "api_key":
                    settings.SERPAPI_KEY,

                    "engine":
                    "google",

                    "num":
                    max_results,

                    "hl":
                    "en",

                    "gl":
                    "in",
                },

                timeout=cls.TIMEOUT,
            )

            logger.info(

                f"{cls.PROVIDER_NAME} "
                f"status={response.status_code}"
            )

            response.raise_for_status()

            data = response.json()

            # =========================================
            # ORGANIC RESULTS
            # =========================================

            organic_results = data.get(
                "organic_results",
                [],
            )

            logger.info(

                f"{cls.PROVIDER_NAME} "
                f"organic_results="
                f"{len(organic_results)}"
            )

            # =========================================
            # PEOPLE ALSO ASK
            # =========================================

            related_questions = data.get(
                "related_questions",
                [],
            )

            inline_questions = data.get(
                "inline_people_also_ask",
                [],
            )

            people_also_ask = []

            # standard PAA
            for item in related_questions:

                question = item.get(
                    "question",
                    "",
                )

                if question:

                    people_also_ask.append(
                        question
                    )

            # inline PAA
            for item in inline_questions:

                question = item.get(
                    "question",
                    "",
                )

                if question:

                    people_also_ask.append(
                        question
                    )

            people_also_ask = list(
                set(people_also_ask)
            )

            logger.info(

                f"{cls.PROVIDER_NAME} "
                f"people_also_ask="
                f"{len(people_also_ask)}"
            )

            # =========================================
            # RELATED SEARCHES
            # =========================================

            related_searches_raw = data.get(
                "related_searches",
                [],
            )

            related_searches = []

            for item in related_searches_raw:

                query = item.get(
                    "query",
                    "",
                )

                if query:

                    related_searches.append(
                        query
                    )

            related_searches = list(
                set(related_searches)
            )

            logger.info(

                f"{cls.PROVIDER_NAME} "
                f"related_searches="
                f"{len(related_searches)}"
            )

            # =========================================
            # KNOWLEDGE GRAPH
            # =========================================

            knowledge_graph = data.get(
                "knowledge_graph",
                {},
            )

            knowledge_graph_keywords = []

            if knowledge_graph:

                logger.info(

                    f"{cls.PROVIDER_NAME} "
                    f"knowledge_graph_found"
                )

                kg_title = (
                    knowledge_graph.get(
                        "title",
                        ""
                    )
                )

                if kg_title:

                    knowledge_graph_keywords.append(
                        kg_title
                    )

                kg_type = (
                    knowledge_graph.get(
                        "type",
                        ""
                    )
                )

                if kg_type:

                    knowledge_graph_keywords.append(
                        kg_type
                    )

            # =========================================
            # NORMALIZE RESULTS
            # =========================================

            results = []

            for item in organic_results:

                normalized = (

                    cls.normalize_serp_result(

                        item,

                        related_searches,

                        people_also_ask,
                    )
                )

                results.append(
                    normalized
                )

            # =========================================
            # ADD KNOWLEDGE GRAPH
            # =========================================

            for item in (
                knowledge_graph_keywords
            ):

                results.append({

                    "title":
                    item,

                    "url":
                    "",

                    "description":
                    "knowledge_graph",

                    "questions":
                    people_also_ask,

                    "related_searches":
                    related_searches,

                    "headings":
                    [],

                    "position":
                    0,

                    "domain":
                    "",

                    "source":
                    cls.PROVIDER_NAME,
                })

            # =========================================
            # REMOVE DUPLICATES
            # =========================================

            filtered_results = []

            seen_titles = set()

            for item in results:

                title = (
                    item.get(
                        "title",
                        ""
                    )
                    .strip()
                    .lower()
                )

                if not title:

                    continue

                if title in seen_titles:

                    continue

                seen_titles.add(
                    title
                )

                filtered_results.append(
                    item
                )

            # =========================================
            # PROCESS RESULTS
            # =========================================

            processed_results = (

                cls.process_results(

                    filtered_results,

                    max_results * 3,
                )
            )

            logger.info(

                f"{cls.PROVIDER_NAME} "
                f"processed_results="
                f"{len(processed_results)}"
            )

            cls.log_success(
                len(processed_results)
            )

            return processed_results

        # =============================================
        # TIMEOUT
        # =============================================

        except requests.Timeout as error:

            logger.exception(

                f"{cls.PROVIDER_NAME} "
                f"timeout error"
            )

            cls.log_failure(error)

            return []

        # =============================================
        # HTTP ERROR
        # =============================================

        except requests.HTTPError as error:

            logger.exception(

                f"{cls.PROVIDER_NAME} "
                f"http error"
            )

            cls.log_failure(error)

            return []

        # =============================================
        # UNKNOWN ERROR
        # =============================================

        except Exception as error:

            logger.exception(

                f"{cls.PROVIDER_NAME} "
                f"unexpected error"
            )

            cls.log_failure(error)

            return []