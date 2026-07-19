"""
Enterprise AI SEO Recommendation Engine
---------------------------------------
"""

from __future__ import annotations

import logging

from collections import Counter

from typing import Any

from apps.keywords.services.page_analyzer_service import (
    PageAnalyzerService,
)

from apps.keywords.services.scoring_service import (
    AdvancedScoringService,
)

logger = logging.getLogger(__name__)


class RecommendationService:

    MAX_ANALYZED_PAGES = 5
    MAX_HEADINGS = 20
    MAX_FAQS = 20
    MAX_RECOMMENDATIONS = 15

    def __init__(self) -> None:

        self.page_service = (
            PageAnalyzerService()
        )

        self.scoring_service = (
            AdvancedScoringService()
        )

    # =====================================================
    # HELPERS
    # =====================================================

    @staticmethod
    def ensure_list(
        value: Any,
    ) -> list:

        if isinstance(value, list):
            return value

        return []

    @staticmethod
    def clean_text(
        value,
    ) -> str:

        if not value:
            return ""

        return str(value).strip()

    # =====================================================
    # HEADINGS
    # =====================================================

    @classmethod
    def extract_common_headings(
        cls,
        pages_data: list[dict],
    ) -> list[str]:

        heading_counter = Counter()

        for page in pages_data:

            headings = cls.ensure_list(
                page.get("headings", [])
            )

            for heading in headings:

                heading = cls.clean_text(
                    heading
                )

                if len(heading) < 5:
                    continue

                heading_counter[
                    heading
                ] += 1

        return [
            heading
            for heading, _ in
            heading_counter.most_common(
                cls.MAX_HEADINGS
            )
        ]

    # =====================================================
    # FAQS
    # =====================================================

    @classmethod
    def extract_common_faqs(
        cls,
        pages_data: list[dict],
    ) -> list[str]:

        faq_counter = Counter()

        for page in pages_data:

            faqs = cls.ensure_list(
                page.get(
                    "faq_questions",
                    [],
                )
            )

            for faq in faqs:

                faq = cls.clean_text(
                    faq
                )

                if len(faq) < 5:
                    continue

                faq_counter[
                    faq
                ] += 1

        return [
            faq
            for faq, _ in
            faq_counter.most_common(
                cls.MAX_FAQS
            )
        ]

    # =====================================================
    # TOPICAL GAPS
    # =====================================================

    @classmethod
    def topic_gaps(
        cls,
        headings,
    ):

        recommendations = []

        joined = " ".join(
            headings
        ).lower()

        important_topics = {

            "eligibility":
            "Add eligibility section.",

            "syllabus":
            "Add detailed syllabus coverage.",

            "exam pattern":
            "Add exam pattern section.",

            "selection process":
            "Explain selection process clearly.",

            "salary":
            "Add salary breakdown.",

            "cut off":
            "Add expected cut off analysis.",

            "admit card":
            "Explain admit card process.",

            "result":
            "Add result checking process.",

            "faq":
            "Add FAQ schema section.",
        }

        for topic, message in (
            important_topics.items()
        ):

            if topic not in joined:

                recommendations.append(
                    message
                )

        return recommendations

    # =====================================================
    # WORD COUNT
    # =====================================================

    @staticmethod
    def recommended_depth(
        avg_word_count,
    ):

        if avg_word_count < 1200:
            return 2500

        if avg_word_count < 2500:
            return 4000

        return avg_word_count + 1000

    # =====================================================
    # EMPTY RESPONSE
    # =====================================================

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

            "recommended_word_count":
            0,

            "recommended_headings":
            [],

            "recommended_faqs":
            [],

            "topical_gaps":
            [],

            "seo_recommendations":
            [],
        }

    # =====================================================
    # SEO RECOMMENDATIONS
    # =====================================================

    def seo_recommendations(
        self,
        keyword,
        score_data,
    ):

        recommendations = []

        score = getattr(
            score_data,
            "seo_score",
            0,
        )

        difficulty = getattr(
            score_data,
            "difficulty",
            "medium",
        )

        if score >= 80:

            recommendations.append(
                "High SEO opportunity keyword."
            )

        elif score >= 60:

            recommendations.append(
                "Moderate SEO opportunity keyword."
            )

        else:

            recommendations.append(
                "Competitive keyword detected."
            )

        if difficulty == "low":

            recommendations.append(
                "Target long-tail search intent."
            )

        if difficulty == "very_high":

            recommendations.append(
                "Build topical authority before targeting."
            )

        recommendations.extend([

            "Use semantic SEO headings.",

            "Optimize title for CTR.",

            "Add FAQ schema markup.",

            "Improve internal linking.",

            "Add entity-rich content.",

            "Cover related search queries.",

            "Use topical clusters.",

            "Optimize for featured snippets.",

            "Add search intent sections.",

            "Use competitor-inspired structure.",
        ])

        return recommendations[
            :self.MAX_RECOMMENDATIONS
        ]

    # =====================================================
    # GENERATE
    # =====================================================

    def generate(
        self,
        keyword: str,
        difficulty_data: dict | None = None,
    ) -> dict[str, Any]:

        logger.info(
            "SEO recommendation engine started."
        )

        keyword = str(
            keyword
        ).strip()

        if not keyword:

            return self.empty_response(
                keyword=""
            )

        if difficulty_data is None:
            difficulty_data = {}

        analyzed_pages = (
            self.ensure_list(
                difficulty_data.get(
                    "analyzed_pages",
                    [],
                )
            )
        )

        score_data = (
            self.scoring_service
            .calculate_advanced_score(
                keyword
            )
        )

        if not analyzed_pages:

            logger.warning(
                "No analyzed pages found."
            )

            return {

                "keyword":
                keyword,

                "difficulty_score":
                getattr(
                    score_data,
                    "seo_score",
                    0,
                ),

                "competition_level":
                getattr(
                    score_data,
                    "difficulty",
                    "medium",
                ),

                "recommended_word_count":
                2500,

                "recommended_headings":
                [],

                "recommended_faqs":
                [],

                "topical_gaps":
                [],

                "seo_recommendations":
                self.seo_recommendations(
                    keyword,
                    score_data,
                ),
            }

        full_pages_data = []

        total_words = 0

        for page in analyzed_pages[
            :self.MAX_ANALYZED_PAGES
        ]:

            try:

                url = page.get(
                    "url"
                )

                if not url:
                    continue

                page_data = (
                    self.page_service
                    .analyze(url)
                )

                full_pages_data.append(
                    page_data
                )

                total_words += (
                    page_data.get(
                        "word_count",
                        0,
                    )
                )

            except Exception as error:

                logger.exception(
                    f"Page analysis failed: {str(error)}"
                )

        avg_word_count = 0

        if full_pages_data:

            avg_word_count = int(
                total_words /
                len(full_pages_data)
            )

        recommended_word_count = (
            self.recommended_depth(
                avg_word_count
            )
        )

        common_headings = (
            self.extract_common_headings(
                full_pages_data
            )
        )

        common_faqs = (
            self.extract_common_faqs(
                full_pages_data
            )
        )

        topical_gaps = (
            self.topic_gaps(
                common_headings
            )
        )

        seo_recommendations = (
            self.seo_recommendations(
                keyword,
                score_data,
            )
        )

        logger.info(
            "SEO recommendation engine completed."
        )

        return {

            "keyword":
            keyword,

            "difficulty_score":
            getattr(
                score_data,
                "seo_score",
                0,
            ),

            "competition_level":
            getattr(
                score_data,
                "difficulty",
                "medium",
            ),

            "recommended_word_count":
            recommended_word_count,

            "recommended_headings":
            common_headings,

            "recommended_faqs":
            common_faqs,

            "topical_gaps":
            topical_gaps,

            "seo_recommendations":
            seo_recommendations,
        }