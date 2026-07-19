"""
Production Keyword Intelligence Service
---------------------------------------

Enterprise-grade keyword intelligence
orchestration layer.

Features:
- centralized SEO intelligence
- keyword analysis
- semantic keyword expansion
- trend analysis
- SEO scoring
- production-safe architecture
- OCI optimized
- scalable orchestration
"""

from __future__ import annotations

import logging

from typing import (
    Any,
)

from apps.keywords.engine import (
    KeywordEngine,
)

from apps.keywords.exceptions import (
    KeywordEngineException,
)

from apps.keywords.services.scoring_service import (
    ScoringService,
)

from apps.keywords.services.trend_service import (
    TrendService,
)

from apps.keywords.services.serp_service import (
    SERPService,
)


logger = logging.getLogger(__name__)


class KeywordService:
    """
    Central SEO intelligence service.
    """

    DEFAULT_LIMIT = 10

    # =============================================
    # INIT
    # =============================================

    def __init__(
        self,
    ) -> None:

        self.engine = (
            KeywordEngine()
        )

        self.scoring_service = (
            ScoringService()
        )

        self.trend_service = (
            TrendService()
        )

        self.serp_service = (
            SERPService()
        )

    # =============================================
    # ANALYZE KEYWORD
    # =============================================

    def analyze_keyword(
        self,
        keyword: str,
    ) -> dict[str, Any]:

        logger.info(
            "Keyword analysis started."
        )

        keyword = str(
            keyword
        ).strip()

        if not keyword:

            raise KeywordEngineException(
                message=(
                    "Keyword is required."
                )
            )

        try:

            # =====================================
            # ENGINE ANALYSIS
            # =====================================

            engine_result = (

                self.engine.analyze(
                    keyword
                )
            )

            # =====================================
            # SEO SCORING
            # =====================================

            scoring_result = (

                self.scoring_service
                .calculate_score(
                    keyword
                )
            )

            # =====================================
            # TREND ANALYSIS
            # =====================================

            trend_result = (

                self.trend_service
                .analyze(
                    keyword
                )
            )

            # =====================================
            # SERP RESULTS
            # =====================================

            serp_results = (

                self.serp_service.search(

                    keyword=keyword,

                    max_results=5,
                )
            )

            # =====================================
            # FINAL RESPONSE
            # =====================================

            result = {

                "keyword":
                keyword,

                "language":
                engine_result.get(
                    "language"
                ),

                "intent":
                engine_result.get(
                    "intent"
                ),

                "seo": {

                    "difficulty":
                    scoring_result.get(
                        "difficulty"
                    ),

                    "score":
                    scoring_result.get(
                        "score"
                    ),

                    "search_volume":
                    scoring_result.get(
                        "volume"
                    ),
                },

                "trend": {

                    "trend_score":
                    trend_result.get(
                        "trend_score"
                    ),

                    "momentum":
                    trend_result.get(
                        "momentum"
                    ),

                    "growth_potential":
                    trend_result.get(
                        "growth_potential"
                    ),
                },

                "serp": {

                    "results":
                    serp_results,

                    "total_results":
                    len(serp_results),
                },
            }

            logger.info(
                "Keyword analysis completed."
            )

            return result

        # =========================================
        # KNOWN ENGINE ERROR
        # =========================================

        except KeywordEngineException:

            logger.exception(
                "Keyword engine exception."
            )

            raise

        # =========================================
        # UNKNOWN FAILURE
        # =========================================

        except Exception as exc:

            logger.exception(
                "Keyword analysis failed."
            )

            raise KeywordEngineException(

                message=(
                    "Keyword analysis failed."
                ),

                details={

                    "reason":
                    str(exc),
                },

            ) from exc

    # =============================================
    # EXPAND KEYWORDS
    # =============================================

    def expand_keywords(
        self,
        topic: str,
        limit: int = 10,
    ) -> list[dict[str, Any]]:

        logger.info(
            "Keyword expansion started."
        )

        topic = str(
            topic
        ).strip()

        if not topic:

            return []

        try:

            keywords = (

                self.engine
                .expand_keywords(
                    topic
                )
            )

            # =====================================
            # SORT BY SCORE
            # =====================================

            sorted_keywords = sorted(

                keywords,

                key=lambda item:

                item.get(
                    "score",
                    0,
                ),

                reverse=True,
            )

            logger.info(

                f"Expanded "
                f"{len(sorted_keywords)} "
                f"keywords."
            )

            return sorted_keywords[:limit]

        except Exception as exc:

            logger.exception(
                "Keyword expansion failed."
            )

            raise KeywordEngineException(

                message=(
                    "Keyword expansion failed."
                ),

                details={

                    "reason":
                    str(exc),
                },

            ) from exc

    # =============================================
    # BEST KEYWORDS
    # =============================================

    def best_keywords(
        self,
        topic: str,
        limit: int = 5,
    ) -> list[dict[str, Any]]:

        logger.info(
            "Best keyword selection started."
        )

        keywords = (

            self.expand_keywords(

                topic=topic,

                limit=limit * 2,
            )
        )

        return keywords[:limit]

    # =============================================
    # TREND ANALYSIS
    # =============================================

    def trend_analysis(
        self,
        keyword: str,
    ) -> dict[str, Any]:

        logger.info(
            "Trend analysis started."
        )

        return (

            self.trend_service
            .analyze(
                keyword
            )
        )

    # =============================================
    # SERP ANALYSIS
    # =============================================

    def serp_analysis(
        self,
        keyword: str,
        max_results: int = 10,
    ) -> list[dict[str, Any]]:

        logger.info(
            "SERP analysis started."
        )

        return (

            self.serp_service.search(

                keyword=keyword,

                max_results=max_results,
            )
        )

    # =============================================
    # HEALTH CHECK
    # =============================================

    def health_check(
        self,
    ) -> dict[str, Any]:

        return {

            "service":
            "SEO Intelligence Engine",

            "status":
            "healthy",

            "version":
            "3.0.0",

            "components": {

                "engine":
                "ok",

                "scoring_service":
                "ok",

                "trend_service":
                "ok",

                "serp_service":
                "ok",
            },

            "providers":

            self.serp_service
            .available_providers(),
        }