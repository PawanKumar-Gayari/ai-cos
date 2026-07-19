"""
Production AI Outline Engine
----------------------------

Enterprise-grade AI-powered
SEO article outline generator.

Features:
- semantic article structure
- shared recommendation context
- heading optimization
- FAQ integration
- reusable intelligence
- scalable architecture
- OCI optimized
- production-safe
"""

from __future__ import annotations

import logging

from typing import (
    Any,
)


logger = logging.getLogger(__name__)


class OutlineService:

    """
    AI-powered SEO outline engine.
    """

    MAX_HEADINGS = 10

    MAX_FAQS = 10

    BLOCKED_HEADINGS = [

        "blog",

        "author",

        "home",

        "menu",

        "contact",

        "privacy",

        "login",

        "register",

        "about us",
    ]

    # =============================================
    # GENERATE H1
    # =============================================

    @staticmethod
    def generate_h1(
        keyword: str,
    ) -> str:

        return keyword.title()

    # =============================================
    # GENERATE INTRO
    # =============================================

    @staticmethod
    def generate_intro(
        keyword: str,
    ) -> str:

        return (

            f"Complete guide about "
            f"{keyword}."
        )

    # =============================================
    # UNIQUE LIST
    # =============================================

    @staticmethod
    def unique_list(
        items: list[str],
    ) -> list[str]:

        seen = set()

        cleaned = []

        for item in items:

            item = str(
                item
            ).strip()

            if not item:

                continue

            if item in seen:

                continue

            seen.add(item)

            cleaned.append(item)

        return cleaned

    # =============================================
    # CLEAN HEADINGS
    # =============================================

    def clean_headings(
        self,
        headings: list[str],
    ) -> list[str]:

        cleaned = []

        headings = self.unique_list(
            headings
        )

        for heading in headings:

            lower = heading.lower()

            # =====================================
            # BLOCKED TERMS
            # =====================================

            if any(

                word in lower

                for word in
                self.BLOCKED_HEADINGS
            ):

                continue

            # =====================================
            # SHORT HEADING
            # =====================================

            if len(heading) < 5:

                continue

            cleaned.append(
                heading
            )

        return cleaned[
            :self.MAX_HEADINGS
        ]

    # =============================================
    # CLEAN FAQS
    # =============================================

    def clean_faqs(
        self,
        faqs: list[str],
    ) -> list[str]:

        cleaned = []

        faqs = self.unique_list(
            faqs
        )

        for faq in faqs:

            faq = str(
                faq
            ).strip()

            if len(faq) < 5:

                continue

            cleaned.append(faq)

        return cleaned[
            :self.MAX_FAQS
        ]

    # =============================================
    # EMPTY OUTLINE
    # =============================================

    @staticmethod
    def empty_outline(
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

            "article_structure": {

                "h1":
                keyword.title(),

                "intro":
                f"Guide about {keyword}.",

                "h2_sections":
                [],

                "faq_section":
                [],
            },
        }

    # =============================================
    # GENERATE OUTLINE
    # =============================================

    def generate(
        self,
        keyword: str,
        recommendation_data: dict | None = None,
    ) -> dict[str, Any]:

        logger.info(
            "Outline engine started."
        )

        keyword = str(
            keyword
        ).strip()

        if not keyword:

            logger.warning(
                "Empty keyword received."
            )

            return self.empty_outline(
                keyword=""
            )

        # =========================================
        # SAFE DEFAULT
        # =========================================

        if recommendation_data is None:

            recommendation_data = {}

        # =========================================
        # HEADINGS
        # =========================================

        headings = (

            recommendation_data.get(

                "recommended_headings",

                [],
            )
        )

        # =========================================
        # FAQS
        # =========================================

        faqs = (

            recommendation_data.get(

                "recommended_faqs",

                [],
            )
        )

        # =========================================
        # CLEAN DATA
        # =========================================

        headings = (
            self.clean_headings(
                headings
            )
        )

        faqs = (
            self.clean_faqs(
                faqs
            )
        )

        # =========================================
        # FINAL OUTLINE
        # =========================================

        outline = {

            "keyword":
            keyword,

            "difficulty_score":

            recommendation_data.get(
                "difficulty_score",
                0,
            ),

            "competition_level":

            recommendation_data.get(
                "competition_level",
                "unknown",
            ),

            "recommended_word_count":

            recommendation_data.get(
                "recommended_word_count",
                0,
            ),

            "article_structure": {

                "h1":

                self.generate_h1(
                    keyword
                ),

                "intro":

                self.generate_intro(
                    keyword
                ),

                "h2_sections":
                headings,

                "faq_section":
                faqs,
            },
        }

        logger.info(
            "Outline engine completed."
        )

        return outline