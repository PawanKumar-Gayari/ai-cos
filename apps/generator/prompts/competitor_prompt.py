"""
Enterprise Competitor Prompt Module
-----------------------------------

Production-grade competitor prompt utilities.

Features:
- competitor heading extraction
- SEO opportunity enrichment
- safe competitor sanitization
- topical enrichment
- low-noise competitor guidance
- production-safe architecture
"""

from __future__ import annotations

import logging
import re


logger = logging.getLogger(
    __name__
)


# =========================================================
# COMPETITOR PROMPT
# =========================================================

class CompetitorPrompt:

    """
    Enterprise competitor context builder.
    """

    MAX_HEADINGS = 5

    # =====================================================
    # SANITIZE TEXT
    # =====================================================

    @classmethod
    def sanitize_text(
        cls,
        text,
    ):

        text = str(
            text
        ).strip()

        # =============================================
        # REMOVE EXCESSIVE SPACES
        # =============================================

        text = re.sub(

            r"\s+",

            " ",

            text,
        )

        # =============================================
        # REMOVE NOISE
        # =============================================

        noise_patterns = [

            r"jhbd\w*",

            r"kjhv\w*",

            r"asdf\w*",

            r"qwerty\w*",
        ]

        for pattern in noise_patterns:

            text = re.sub(

                pattern,

                "",

                text,

                flags=re.IGNORECASE,
            )

        return text.strip()

    # =====================================================
    # CLEAN HEADINGS
    # =====================================================

    @classmethod
    def clean_headings(
        cls,
        headings,
    ):

        cleaned = []

        for heading in headings:

            heading = cls.sanitize_text(
                heading
            )

            if (
                len(heading) < 5
            ):

                continue

            cleaned.append(
                heading
            )

        return list(
            dict.fromkeys(cleaned)
        )

    # =====================================================
    # BUILD SUMMARY SECTION
    # =====================================================

    @classmethod
    def build_summary_section(
        cls,
        summary,
    ):

        if not summary:

            return []

        lines = []

        competition_level = (
            summary.get(
                "competition_level"
            )
        )

        seo_opportunity = (
            summary.get(
                "seo_opportunity"
            )
        )

        content_gap = (
            summary.get(
                "content_gap"
            )
        )

        if competition_level:

            lines.append(

                f"Competition level: "
                f"{competition_level}"
            )

        if seo_opportunity:

            lines.append(

                f"SEO opportunity: "
                f"{seo_opportunity}"
            )

        if content_gap:

            lines.append(

                f"Content gap: "
                f"{content_gap}"
            )

        return lines

    # =====================================================
    # BUILD HEADINGS SECTION
    # =====================================================

    @classmethod
    def build_headings_section(
        cls,
        headings,
    ):

        if not headings:

            return []

        lines = [

            "Top competitor headings:",
        ]

        cleaned_headings = (
            cls.clean_headings(
                headings
            )
        )

        for heading in cleaned_headings[
            :cls.MAX_HEADINGS
        ]:

            lines.append(
                f"- {heading}"
            )

        return lines

    # =====================================================
    # BUILD SEO INSIGHTS
    # =====================================================

    @classmethod
    def build_seo_insights(
        cls,
        competitor_data,
    ):

        lines = []

        keywords = (
            competitor_data.get(
                "top_keywords",
                []
            )
        )

        keywords = (
            cls.clean_headings(
                keywords
            )
        )

        if keywords:

            lines.append(
                "Competitor semantic keywords:"
            )

            for keyword in keywords[:10]:

                lines.append(
                    f"- {keyword}"
                )

        return lines

    # =====================================================
    # BUILD FULL CONTEXT
    # =====================================================

    @classmethod
    def build(
        cls,
        competitor_data,
    ):

        if not competitor_data:

            return ""

        try:

            lines = []

            summary = (
                competitor_data.get(
                    "analysis_summary",
                    {}
                )
            )

            top_headings = (
                competitor_data.get(
                    "top_headings",
                    []
                )
            )

            # =========================================
            # SUMMARY
            # =========================================

            lines.extend(
                cls.build_summary_section(
                    summary
                )
            )

            # =========================================
            # HEADINGS
            # =========================================

            heading_lines = (
                cls.build_headings_section(
                    top_headings
                )
            )

            if heading_lines:

                lines.append("")

                lines.extend(
                    heading_lines
                )

            # =========================================
            # SEO INSIGHTS
            # =========================================

            seo_lines = (
                cls.build_seo_insights(
                    competitor_data
                )
            )

            if seo_lines:

                lines.append("")

                lines.extend(
                    seo_lines
                )

            context = "\n".join(
                lines
            )

            logger.info(
                "Competitor prompt built."
            )

            return context

        except Exception as error:

            logger.exception(

                f"Competitor prompt build failed: "
                f"{str(error)}"
            )

            return ""
