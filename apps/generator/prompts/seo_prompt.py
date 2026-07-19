"""
Enterprise SEO Prompt Module
----------------------------

Production-grade SEO prompt utilities.
"""

from __future__ import annotations

import logging


logger = logging.getLogger(
    __name__
)


class SEOPrompt:

    """
    Enterprise SEO prompt builder.
    """

    MAX_KEYWORDS = 15

    MAX_HEADINGS = 8

    MAX_FAQS = 10

    @classmethod
    def build(
        cls,
        seo_data,
        user_query,
    ):

        if not seo_data:

            return []

        lines = []

        primary_keyword = (
            seo_data.get(
                "keyword",
                user_query,
            )
        )

        suggestions = (
            seo_data.get(
                "suggestions",
                []
            )
        )

        recommendations = (
            seo_data.get(
                "recommendations",
                {}
            )
        )

        difficulty = (
            seo_data.get(
                "difficulty",
                {}
            )
        )

        headings = (
            recommendations.get(
                "recommended_headings",
                []
            )
        )

        faqs = (
            recommendations.get(
                "recommended_faqs",
                []
            )
        )

        word_count = (
            recommendations.get(
                "recommended_word_count",
                2000,
            )
        )

        # =========================================
        # SEO RULES
        # =========================================

        lines.extend([

            "CRITICAL SEO REQUIREMENTS:",

            "Use the primary keyword naturally in the title.",

            "Use the primary keyword in the introduction.",

            "Use the primary keyword in at least one H2 heading.",

            "Use semantic keyword variations naturally.",

            "Maintain strong topical relevance.",

            "Cover the complete search intent.",

            "Write for humans first and SEO second.",

            "Avoid keyword stuffing.",

            "Maintain natural readability.",

            "Create SEO-friendly headings.",

            "Use long-tail keyword variations naturally.",

            "Include semantic topical coverage.",

            "",
        ])

        # =========================================
        # PRIMARY KEYWORD
        # =========================================

        lines.extend([

            "PRIMARY SEO KEYWORD:",

            primary_keyword,

            "",
        ])

        # =========================================
        # SECONDARY KEYWORDS
        # =========================================

        if suggestions:

            lines.append(
                "IMPORTANT SECONDARY KEYWORDS:"
            )

            for keyword in suggestions[
                :cls.MAX_KEYWORDS
            ]:

                lines.append(
                    f"- {keyword}"
                )

            lines.append("")

        # =========================================
        # HEADINGS
        # =========================================

        if headings:

            lines.append(
                "SUGGESTED SEO HEADINGS:"
            )

            for heading in headings[
                :cls.MAX_HEADINGS
            ]:

                lines.append(
                    f"- {heading}"
                )

            lines.append("")

        # =========================================
        # FAQS
        # =========================================

        if faqs:

            lines.append(
                "TARGET SEO FAQS:"
            )

            for faq in faqs[
                :cls.MAX_FAQS
            ]:

                lines.append(
                    f"- {faq}"
                )

            lines.append("")

        # =========================================
        # SEO TARGETS
        # =========================================

        lines.extend([

            "SEO TARGETS:",

            f"Target Word Count: {word_count}",

            f"Competition Level: "
            f"{difficulty.get('competition_level', 'unknown')}",

            f"Difficulty Score: "
            f"{difficulty.get('difficulty_score', 0)}",

            "",
        ])

        logger.info(
            "SEO prompt built."
        )

        return lines