"""
Enterprise Search Router
------------------------

Production-grade SEO intelligence routing system.

Priority:
1. Serper
2. SerpAPI
3. Tavily
4. DuckDuckGo

Features:
- provider failover
- intelligent routing
- provider scoring
- SEO response normalization
- People Also Ask support
- related searches support
- semantic-safe routing
- multilingual SEO support
- provider timing analytics
- OCI optimized
- production-safe
"""

from __future__ import annotations

import logging
import time

from typing import (
    Any,
)

from .duckduckgo_provider import (
    DuckDuckGoProvider,
)

from .serpapi_provider import (
    SerpApiProvider,
)

from .serper_provider import (
    SerperProvider,
)

from .tavily_provider import (
    TavilyProvider,
)


logger = logging.getLogger(
    __name__
)


class SearchRouter:

    """
    Enterprise SEO intelligence router.
    """

    # =====================================================
    # PROVIDERS
    # =====================================================

    PROVIDERS = [

        # ===============================================
        # BEST FOR SEO
        # ===============================================

        SerperProvider,

        # ===============================================
        # STRONG FALLBACK
        # ===============================================

        SerpApiProvider,

        # ===============================================
        # AI SEARCH
        # ===============================================

        TavilyProvider,

        # ===============================================
        # LAST FALLBACK
        # ===============================================

        DuckDuckGoProvider,
    ]

    # =====================================================
    # SAFE LIST
    # =====================================================

    @staticmethod
    def ensure_list(
        value,
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

    @staticmethod
    def clean_text(
        value,
    ) -> str:

        if not value:

            return ""

        return (
            str(value)
            .strip()
        )

    # =====================================================
    # NORMALIZE RESULT
    # =====================================================

    @classmethod
    def normalize_result(
        cls,
        item,
        provider_name,
    ) -> dict[str, Any]:

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
            # METADATA
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
            provider_name,
        }

    # =====================================================
    # SAFE RESULTS
    # =====================================================

    @classmethod
    def safe_results(

        cls,

        results,

        provider_name,
    ) -> list[dict[str, Any]]:

        if not isinstance(
            results,
            list,
        ):

            return []

        cleaned = []

        seen_titles = set()

        for item in results:

            if not isinstance(
                item,
                dict,
            ):

                continue

            normalized = (
                cls.normalize_result(

                    item,

                    provider_name,
                )
            )

            title = (

                normalized[
                    "title"
                ]
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

            cleaned.append(
                normalized
            )

        return cleaned

    # =====================================================
    # SEO QUALITY CHECK
    # =====================================================

    @staticmethod
    def quality_score(
        results,
    ) -> int:

        score = 0

        for item in results:

            # title
            if item.get(
                "title"
            ):

                score += 2

            # description
            if item.get(
                "description"
            ):

                score += 2

            # url
            if item.get(
                "url"
            ):

                score += 1

            # PAA
            if item.get(
                "questions"
            ):

                score += 5

            # related
            if item.get(
                "related_searches"
            ):

                score += 4

        return score

    # =====================================================
    # SEARCH
    # =====================================================

    @classmethod
    def search(

        cls,

        keyword: str,

        max_results: int = 10,
    ) -> list[dict[str, Any]]:

        keyword = str(
            keyword
        ).strip()

        logger.info(

            f"SEO SEARCH ROUTER STARTED | "
            f"keyword={keyword}"
        )

        if not keyword:

            return []

        if max_results <= 0:

            max_results = 10

        last_error = None

        best_results = []

        best_score = 0

        provider_stats = []

        # =================================================
        # PROVIDER LOOP
        # =================================================

        for provider in cls.PROVIDERS:

            provider_name = (
                provider.__name__
            )

            try:

                logger.info(

                    f"TRYING PROVIDER | "
                    f"{provider_name}"
                )

                start_time = (
                    time.time()
                )

                # =========================================
                # PROVIDER SEARCH
                # =========================================

                results = (

                    provider.search(

                        keyword=keyword,

                        max_results=max_results,
                    )
                )

                elapsed = round(

                    time.time()
                    - start_time,

                    2,
                )

                # =========================================
                # NORMALIZE RESULTS
                # =========================================

                results = (
                    cls.safe_results(

                        results,

                        provider_name,
                    )
                )

                # =========================================
                # QUALITY CHECK
                # =========================================

                quality = (
                    cls.quality_score(
                        results
                    )
                )

                provider_stats.append({

                    "provider":
                    provider_name,

                    "results":
                    len(results),

                    "quality":
                    quality,

                    "time":
                    elapsed,
                })

                # =========================================
                # EMPTY RESULTS
                # =========================================

                if not results:

                    logger.warning(

                        f"EMPTY RESULTS | "
                        f"{provider_name}"
                    )

                    continue

                logger.info(

                    f"PROVIDER SUCCESS | "
                    f"{provider_name} | "
                    f"results={len(results)} | "
                    f"quality={quality} | "
                    f"time={elapsed}s"
                )

                # =========================================
                # STORE BEST RESULTS
                # =========================================

                if quality > best_score:

                    best_score = quality

                    best_results = results

                # =========================================
                # EARLY EXIT
                # =========================================

                if quality >= 25:

                    logger.info(

                        f"HIGH QUALITY RESULTS | "
                        f"{provider_name}"
                    )

                    return results

            # =============================================
            # PROVIDER FAILURE
            # =============================================

            except Exception as error:

                logger.exception(

                    f"PROVIDER FAILED | "
                    f"{provider_name} | "
                    f"error={str(error)}"
                )

                last_error = error

                continue

        # =================================================
        # RETURN BEST AVAILABLE
        # =================================================

        if best_results:

            logger.info(

                f"RETURNING BEST RESULTS | "
                f"quality={best_score}"
            )

            return best_results

        # =================================================
        # COMPLETE FAILURE
        # =================================================

        logger.error(

            "ALL SEARCH PROVIDERS FAILED | "
            f"keyword={keyword}"
        )

        logger.error(

            f"PROVIDER STATS | "
            f"{provider_stats}"
        )

        if last_error:

            raise last_error

        return []

    # =====================================================
    # AVAILABLE PROVIDERS
    # =====================================================

    @classmethod
    def available_providers(
        cls,
    ) -> list[str]:

        return [

            provider.__name__

            for provider in cls.PROVIDERS
        ]

    # =====================================================
    # PROVIDER PRIORITY
    # =====================================================

    @classmethod
    def provider_priority(
        cls,
    ) -> list[str]:

        return [

            provider.__name__

            for provider in cls.PROVIDERS
        ]