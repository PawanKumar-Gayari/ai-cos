"""
Keyword scoring service.
"""

from apps.keywords.constants import (

    DIFFICULTY_HIGH,

    DIFFICULTY_LOW,

    DIFFICULTY_MEDIUM,
)


class ScoringService:

    def calculate_score(
        self,
        keyword,
    ):

        """
        Calculate keyword opportunity score.
        """

        keyword_lower = (
            keyword.lower()
        )

        word_count = len(
            keyword_lower.split()
        )

        character_count = len(
            keyword_lower
        )

        # ==========================================
        # LONG-TAIL ADVANTAGE
        # ==========================================

        if word_count >= 5:

            difficulty = (
                DIFFICULTY_LOW
            )

            volume = 800

            score = 90

        elif word_count == 4:

            difficulty = (
                DIFFICULTY_LOW
            )

            volume = 1500

            score = 80

        elif word_count == 3:

            difficulty = (
                DIFFICULTY_MEDIUM
            )

            volume = 4000

            score = 65

        elif word_count == 2:

            difficulty = (
                DIFFICULTY_HIGH
            )

            volume = 10000

            score = 45

        else:

            difficulty = (
                DIFFICULTY_HIGH
            )

            volume = 25000

            score = 25

        # ==========================================
        # SEO BOOST TERMS
        # ==========================================

        boost_terms = [

            "best",

            "guide",

            "tutorial",

            "tips",

            "review",

            "how to",
        ]

        if any(
            term in keyword_lower
            for term in boost_terms
        ):

            score += 10

        # ==========================================
        # VERY SHORT KEYWORD PENALTY
        # ==========================================

        if character_count <= 8:

            score -= 10

        # ==========================================
        # FINAL CLAMP
        # ==========================================

        score = max(
            min(score, 100),
            0,
        )

        return {

            "difficulty": difficulty,

            "volume": volume,

            "score": score,
        }