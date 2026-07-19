"""
Production SEO Difficulty Engine
--------------------------------

Enterprise-grade SERP competition
analysis engine.

Features:
- shared SERP context
- competitor page analysis
- SEO competition scoring
- semantic-safe normalization
- scalable architecture
- OCI optimized
- production-safe
"""

from __future__ import annotations

import logging

from typing import (
    Any,
)

from apps.keywords.services.page_analyzer_service import (
    PageAnalyzerService,
)

from apps.keywords.services.serp_service import (
    SERPService,
)


logger = logging.getLogger(__name__)


class DifficultyService:

    """
    SEO competition difficulty engine.
    """

    MAX_ANALYZED_RESULTS = 3

    BLOCKED_DOMAINS = [

        "youtube.com",

        "translate.google",

        "google.com",

        "facebook.com",

        "instagram.com",

        "twitter.com",

        "x.com",
    ]

    NORMALIZATION_REPLACEMENTS = {

        "rajatan":
        "rajasthan",

        "vacany":
        "vacancy",

        "nokri":
        "naukri",
    }

    # =============================================
    # INIT
    # =============================================

    def __init__(
        self,
    ) -> None:

        self.serp_service = (
            SERPService()
        )

        self.page_service = (
            PageAnalyzerService()
        )

    # =============================================
    # SCORE WORD COUNT
    # =============================================

    @staticmethod
    def score_word_count(
        count: int,
    ) -> int:

        if count >= 5000:

            return 30

        if count >= 3000:

            return 20

        if count >= 1500:

            return 10

        return 5

    # =============================================
    # SCORE HEADINGS
    # =============================================

    @staticmethod
    def score_headings(
        headings_count: int,
    ) -> int:

        if headings_count >= 20:

            return 25

        if headings_count >= 10:

            return 15

        return 5

    # =============================================
    # SCORE FAQS
    # =============================================

    @staticmethod
    def score_faqs(
        faq_count: int,
    ) -> int:

        if faq_count >= 10:

            return 20

        if faq_count >= 5:

            return 10

        return 5

    # =============================================
    # VALID RESULT
    # =============================================

    def is_valid_result(
        self,
        url: str,
    ) -> bool:

        if not url:

            return False

        url = str(
            url
        ).lower()

        for domain in (
            self.BLOCKED_DOMAINS
        ):

            if domain in url:

                return False

        return True

    # =============================================
    # NORMALIZE KEYWORD
    # =============================================

    def normalize_keyword(
        self,
        keyword: str,
    ) -> str:

        keyword = (

            keyword
            .lower()
            .strip()
        )

        for wrong, correct in (

            self.NORMALIZATION_REPLACEMENTS
            .items()
        ):

            keyword = keyword.replace(

                wrong,

                correct,
            )

        return keyword

    # =============================================
    # EMPTY RESPONSE
    # =============================================

    @staticmethod
    def empty_response(
        keyword: str,
    ) -> dict[str, Any]:

        return {

            "keyword":
            keyword,

            "difficulty_score":
            0,

            "competition_level":
            "unknown",

            "analyzed_pages":
            [],
        }

    # =============================================
    # DETECT COMPETITION LEVEL
    # =============================================

    @staticmethod
    def detect_level(
        score: int,
    ) -> str:

        if score >= 60:

            return "very_high"

        if score >= 45:

            return "high"

        if score >= 30:

            return "medium"

        return "low"

    # =============================================
    # CALCULATE
    # =============================================

    def calculate(
        self,
        keyword: str,
        serp_results: list | None = None,
    ) -> dict[str, Any]:

        logger.info(
            "Difficulty analysis started."
        )

        # =========================================
        # NORMALIZATION
        # =========================================

        keyword = (
            self.normalize_keyword(
                keyword
            )
        )

        # =========================================
        # FETCH SERP RESULTS
        # =========================================

        if serp_results is None:

            serp_results = (

                self.serp_service.search(

                    keyword,

                    max_results=(
                        self.MAX_ANALYZED_RESULTS
                    ),
                )
            )

        # =========================================
        # FILTER RESULTS
        # =========================================

        serp_results = [

            result

            for result in serp_results

            if self.is_valid_result(

                result.get(
                    "url",
                    "",
                )
            )
        ]

        # =========================================
        # EMPTY RESULTS
        # =========================================

        if not serp_results:

            logger.warning(
                "No SERP results found."
            )

            return self.empty_response(
                keyword
            )

        total_score = 0

        analyzed_pages = []

        # =========================================
        # PAGE ANALYSIS
        # =========================================

        for result in serp_results[
            :self.MAX_ANALYZED_RESULTS
        ]:

            try:

                page_data = (

                    self.page_service
                    .analyze(

                        result["url"]
                    )
                )

                word_count = (

                    page_data.get(
                        "word_count",
                        0,
                    )
                )

                headings = (

                    page_data.get(
                        "headings",
                        [],
                    )
                )

                faqs = (

                    page_data.get(
                        "faq_questions",
                        [],
                    )
                )

                page_score = 0

                page_score += (

                    self.score_word_count(
                        word_count
                    )
                )

                page_score += (

                    self.score_headings(
                        len(headings)
                    )
                )

                page_score += (

                    self.score_faqs(
                        len(faqs)
                    )
                )

                total_score += (
                    page_score
                )

                analyzed_pages.append({

                    "url":
                    result["url"],

                    "title":
                    result.get(
                        "title",
                        "",
                    ),

                    "word_count":
                    word_count,

                    "headings_count":
                    len(headings),

                    "faq_count":
                    len(faqs),

                    "page_score":
                    page_score,
                })

            except Exception as error:

                logger.exception(

                    f"Page analysis failed: "
                    f"{str(error)}"
                )

        # =========================================
        # SAFE EMPTY ANALYSIS
        # =========================================

        if not analyzed_pages:

            return self.empty_response(
                keyword
            )

        # =========================================
        # FINAL SCORE
        # =========================================

        average_score = int(

            total_score /

            len(analyzed_pages)
        )

        level = self.detect_level(
            average_score
        )

        logger.info(
            "Difficulty analysis completed."
        )

        # =========================================
        # FINAL RESPONSE
        # =========================================

        return {

            "keyword":
            keyword,

            "difficulty_score":
            average_score,

            "competition_level":
            level,

            "analyzed_pages":
            analyzed_pages,
        }