"""
Production Content Quality Scoring Engine
-----------------------------------------

Enterprise-grade AI content scoring system.

Features:
- SEO quality scoring
- readability analysis
- heading structure analysis
- semantic SEO scoring
- AI detection heuristics
- markdown quality analysis
- topical depth analysis
- content structure scoring
- production-safe architecture
"""

from __future__ import annotations

import re


class ContentScorer:

    """
    Enterprise content scoring engine.
    """

    H1_PATTERN = re.compile(
        r"^#\s.+",
        re.MULTILINE,
    )

    H2_PATTERN = re.compile(
        r"^##\s.+",
        re.MULTILINE,
    )

    H3_PATTERN = re.compile(
        r"^###\s.+",
        re.MULTILINE,
    )

    LIST_PATTERN = re.compile(
        r"^[-*]\s",
        re.MULTILINE,
    )

    TABLE_PATTERN = re.compile(
        r"\|.+\|"
    )

    FAQ_PATTERN = re.compile(
        r"(faq|frequently asked)",
        re.IGNORECASE,
    )

    # =============================================
    # WORD COUNT
    # =============================================

    @staticmethod
    def word_count(
        content,
    ):

        return len(
            content.split()
        )

    # =============================================
    # HEADING SCORE
    # =============================================

    @classmethod
    def heading_score(
        cls,
        content,
    ):

        h1_count = len(

            cls.H1_PATTERN.findall(
                content
            )
        )

        h2_count = len(

            cls.H2_PATTERN.findall(
                content
            )
        )

        h3_count = len(

            cls.H3_PATTERN.findall(
                content
            )
        )

        score = 0

        # =========================================
        # H1 RULE
        # =========================================

        if h1_count == 1:

            score += 30

        elif h1_count > 1:

            score -= 10

        # =========================================
        # H2 STRUCTURE
        # =========================================

        if h2_count >= 5:

            score += 40

        elif h2_count >= 3:

            score += 25

        elif h2_count >= 1:

            score += 10

        # =========================================
        # H3 STRUCTURE
        # =========================================

        if h3_count >= 3:

            score += 30

        elif h3_count >= 1:

            score += 15

        return max(
            min(score, 100),
            0,
        )

    # =============================================
    # READABILITY SCORE
    # =============================================

    @staticmethod
    def readability_score(
        content,
    ):

        sentences = re.split(

            r"[.!?]",

            content,
        )

        sentence_count = max(

            len(sentences),

            1,
        )

        words = content.split()

        word_count = max(

            len(words),

            1,
        )

        avg_sentence_length = (

            word_count / sentence_count
        )

        if avg_sentence_length <= 14:

            return 95

        if avg_sentence_length <= 20:

            return 85

        if avg_sentence_length <= 30:

            return 65

        return 40

    # =============================================
    # SEO SCORE
    # =============================================

    @classmethod
    def seo_score(
        cls,
        content,
    ):

        score = 0

        word_count = (
            cls.word_count(
                content
            )
        )

        # =========================================
        # HEADINGS
        # =========================================

        if cls.H1_PATTERN.search(
            content
        ):

            score += 10

        if cls.H2_PATTERN.search(
            content
        ):

            score += 15

        if cls.H3_PATTERN.search(
            content
        ):

            score += 10

        # =========================================
        # WORD COUNT
        # =========================================

        if word_count >= 2000:

            score += 30

        elif word_count >= 1200:

            score += 20

        elif word_count >= 600:

            score += 10

        # =========================================
        # STRUCTURE
        # =========================================

        if cls.LIST_PATTERN.search(
            content
        ):

            score += 10

        if cls.TABLE_PATTERN.search(
            content
        ):

            score += 10

        if cls.FAQ_PATTERN.search(
            content
        ):

            score += 15

        return min(
            score,
            100,
        )

    # =============================================
    # AI RISK SCORE
    # =============================================

    @staticmethod
    def ai_risk_score(
        content,
    ):

        robotic_phrases = [

            "in conclusion",

            "as an ai",

            "overall",

            "furthermore",

            "moreover",

            "it is important to note",

            "delve into",

            "landscape of",

            "unlock the power",
        ]

        repeated_phrases = [

            "additionally",

            "however",

            "therefore",
        ]

        risk = 0

        content_lower = (
            content.lower()
        )

        # =========================================
        # ROBOTIC PHRASES
        # =========================================

        for phrase in robotic_phrases:

            if phrase in content_lower:

                risk += 10

        # =========================================
        # REPETITION
        # =========================================

        for phrase in repeated_phrases:

            count = (
                content_lower.count(
                    phrase
                )
            )

            if count > 5:

                risk += 10

        return min(
            risk,
            100,
        )

    # =============================================
    # TOPICAL DEPTH SCORE
    # =============================================

    @classmethod
    def topical_depth_score(
        cls,
        content,
    ):

        h2_count = len(

            cls.H2_PATTERN.findall(
                content
            )
        )

        h3_count = len(

            cls.H3_PATTERN.findall(
                content
            )
        )

        paragraphs = len([

            p.strip()

            for p in content.split("\n\n")

            if p.strip()
        ])

        score = 0

        if h2_count >= 6:

            score += 40

        elif h2_count >= 4:

            score += 25

        if h3_count >= 5:

            score += 30

        elif h3_count >= 2:

            score += 15

        if paragraphs >= 15:

            score += 30

        elif paragraphs >= 8:

            score += 15

        return min(
            score,
            100,
        )

    # =============================================
    # CONTENT STRUCTURE SCORE
    # =============================================

    @classmethod
    def structure_score(
        cls,
        content,
    ):

        score = 0

        if cls.H1_PATTERN.search(
            content
        ):

            score += 20

        if cls.H2_PATTERN.search(
            content
        ):

            score += 25

        if cls.H3_PATTERN.search(
            content
        ):

            score += 20

        if cls.LIST_PATTERN.search(
            content
        ):

            score += 15

        if cls.TABLE_PATTERN.search(
            content
        ):

            score += 20

        return min(
            score,
            100,
        )

    # =============================================
    # FINAL SCORE
    # =============================================

    @classmethod
    def overall_score(
        cls,
        scores,
    ):

        overall = (

            (
                scores[
                    "seo_score"
                ] * 0.35
            )

            +

            (
                scores[
                    "readability_score"
                ] * 0.20
            )

            +

            (
                scores[
                    "heading_score"
                ] * 0.20
            )

            +

            (
                scores[
                    "topical_depth_score"
                ] * 0.15
            )

            +

            (
                scores[
                    "structure_score"
                ] * 0.10
            )

            -

            (
                scores[
                    "ai_risk_score"
                ] * 0.10
            )
        )

        return max(
            min(
                round(overall),
                100,
            ),
            0,
        )

    # =============================================
    # SCORE
    # =============================================

    @classmethod
    def score(
        cls,
        content,
    ):

        scores = {

            "word_count": (
                cls.word_count(
                    content
                )
            ),

            "heading_score": (
                cls.heading_score(
                    content
                )
            ),

            "readability_score": (
                cls.readability_score(
                    content
                )
            ),

            "seo_score": (
                cls.seo_score(
                    content
                )
            ),

            "ai_risk_score": (
                cls.ai_risk_score(
                    content
                )
            ),

            "topical_depth_score": (
                cls.topical_depth_score(
                    content
                )
            ),

            "structure_score": (
                cls.structure_score(
                    content
                )
            ),
        }

        scores[
            "overall_score"
        ] = cls.overall_score(
            scores
        )

        return scores