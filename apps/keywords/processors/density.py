"""
Production Keyword Density Processor
------------------------------------

Enterprise-grade SEO keyword density analyzer.

Features:
- semantic keyword density
- keyword stuffing detection
- heading keyword analysis
- intro/conclusion optimization
- multilingual safe normalization
- semantic keyword variations
- placement analysis
- production-safe architecture
"""

from __future__ import annotations

import logging
import re


logger = logging.getLogger(
    __name__
)


class KeywordDensityProcessor:

    """
    Enterprise SEO keyword density analyzer.
    """

    HEADING_PATTERN = re.compile(
        r"^#{1,3}\s(.+)$",
        re.MULTILINE,
    )

    # =============================================
    # CLEAN TEXT
    # =============================================

    def clean_text(
        self,
        text,
    ):

        text = str(
            text
        ).lower()

        text = re.sub(

            r"[^\w\s\u0900-\u097F]",

            " ",

            text,
        )

        text = re.sub(

            r"\s+",

            " ",

            text,
        )

        return text.strip()

    # =============================================
    # WORD COUNT
    # =============================================

    def word_count(
        self,
        content,
    ):

        content = (
            self.clean_text(
                content
            )
        )

        if not content:

            return 0

        return len(
            content.split()
        )

    # =============================================
    # KEYWORD COUNT
    # =============================================

    def keyword_count(
        self,
        content,
        keyword,
    ):

        content = (
            self.clean_text(
                content
            )
        )

        keyword = (
            self.clean_text(
                keyword
            )
        )

        if not keyword:

            return 0

        pattern = (
            rf"\b{re.escape(keyword)}\b"
        )

        matches = re.findall(
            pattern,
            content,
        )

        return len(matches)

    # =============================================
    # DENSITY SCORE
    # =============================================

    def density_score(
        self,
        content,
        keyword,
    ):

        total_words = (
            self.word_count(
                content
            )
        )

        keyword_occurrences = (
            self.keyword_count(

                content,

                keyword,
            )
        )

        if total_words == 0:

            return 0

        density = (

            keyword_occurrences
            / total_words

        ) * 100

        return round(
            density,
            2,
        )

    # =============================================
    # SEO STATUS
    # =============================================

    def seo_status(
        self,
        density,
    ):

        if density < 0.5:

            return "low"

        if density <= 1.5:

            return "optimal"

        if density <= 3:

            return "high"

        return "keyword_stuffing"

    # =============================================
    # HEADING ANALYSIS
    # =============================================

    def heading_analysis(
        self,
        content,
        keyword,
    ):

        keyword = (
            self.clean_text(
                keyword
            )
        )

        headings = (

            self.HEADING_PATTERN
            .findall(content)
        )

        total_headings = len(
            headings
        )

        keyword_headings = 0

        for heading in headings:

            cleaned_heading = (
                self.clean_text(
                    heading
                )
            )

            if keyword in cleaned_heading:

                keyword_headings += 1

        if total_headings == 0:

            return {

                "total_headings": 0,

                "keyword_headings": 0,

                "heading_ratio": 0,
            }

        ratio = (

            keyword_headings
            / total_headings

        ) * 100

        return {

            "total_headings":
            total_headings,

            "keyword_headings":
            keyword_headings,

            "heading_ratio":
            round(ratio, 2),
        }

    # =============================================
    # INTRO ANALYSIS
    # =============================================

    def intro_analysis(
        self,
        content,
        keyword,
    ):

        keyword = (
            self.clean_text(
                keyword
            )
        )

        intro = content[:800]

        intro_clean = (
            self.clean_text(
                intro
            )
        )

        return {

            "keyword_in_intro":
            keyword in intro_clean,

            "intro_keyword_count":
            self.keyword_count(

                intro_clean,

                keyword,
            ),
        }

    # =============================================
    # CONCLUSION ANALYSIS
    # =============================================

    def conclusion_analysis(
        self,
        content,
        keyword,
    ):

        keyword = (
            self.clean_text(
                keyword
            )
        )

        conclusion = content[-800:]

        conclusion_clean = (
            self.clean_text(
                conclusion
            )
        )

        return {

            "keyword_in_conclusion":
            keyword in conclusion_clean,

            "conclusion_keyword_count":
            self.keyword_count(

                conclusion_clean,

                keyword,
            ),
        }

    # =============================================
    # SEMANTIC VARIATIONS
    # =============================================

    def semantic_variations(
        self,
        keyword,
    ):

        keyword = (
            self.clean_text(
                keyword
            )
        )

        words = keyword.split()

        variations = set()

        if len(words) >= 2:

            variations.add(
                " ".join(words[:-1])
            )

            variations.add(
                " ".join(words[1:])
            )

        for word in words:

            if len(word) > 3:

                variations.add(word)

        return list(
            variations
        )

    # =============================================
    # SEMANTIC COVERAGE
    # =============================================

    def semantic_coverage(
        self,
        content,
        keyword,
    ):

        content = (
            self.clean_text(
                content
            )
        )

        variations = (
            self.semantic_variations(
                keyword
            )
        )

        matches = []

        for variation in variations:

            if variation in content:

                matches.append(
                    variation
                )

        coverage = 0

        if variations:

            coverage = (

                len(matches)
                / len(variations)

            ) * 100

        return {

            "semantic_matches":
            matches,

            "semantic_coverage":
            round(coverage, 2),
        }

    # =============================================
    # STUFFING DETECTION
    # =============================================

    def stuffing_detection(
        self,
        content,
        keyword,
    ):

        keyword = (
            self.clean_text(
                keyword
            )
        )

        content = (
            self.clean_text(
                content
            )
        )

        repeated_pattern = (
            rf"({re.escape(keyword)})(\s+\1)+"
        )

        repeated_matches = re.findall(

            repeated_pattern,

            content,
        )

        return {

            "stuffing_detected":
            len(repeated_matches) > 0,

            "repeated_patterns":
            len(repeated_matches),
        }

    # =============================================
    # ANALYZE
    # =============================================

    def analyze(
        self,
        content,
        keyword,
    ):

        total_words = (
            self.word_count(
                content
            )
        )

        keyword_occurrences = (
            self.keyword_count(

                content,

                keyword,
            )
        )

        density = (
            self.density_score(

                content,

                keyword,
            )
        )

        status = (
            self.seo_status(
                density
            )
        )

        heading_analysis = (
            self.heading_analysis(

                content,

                keyword,
            )
        )

        intro_analysis = (
            self.intro_analysis(

                content,

                keyword,
            )
        )

        conclusion_analysis = (
            self.conclusion_analysis(

                content,

                keyword,
            )
        )

        semantic_analysis = (
            self.semantic_coverage(

                content,

                keyword,
            )
        )

        stuffing_analysis = (
            self.stuffing_detection(

                content,

                keyword,
            )
        )

        result = {

            "keyword":
            keyword,

            "total_words":
            total_words,

            "keyword_count":
            keyword_occurrences,

            "density":
            density,

            "seo_status":
            status,

            "heading_analysis":
            heading_analysis,

            "intro_analysis":
            intro_analysis,

            "conclusion_analysis":
            conclusion_analysis,

            "semantic_analysis":
            semantic_analysis,

            "stuffing_analysis":
            stuffing_analysis,
        }

        logger.info(

            f"DENSITY RESULT: "
            f"{result}"
        )

        return result