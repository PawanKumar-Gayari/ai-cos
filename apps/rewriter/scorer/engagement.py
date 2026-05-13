"""
Engagement scorer.
"""

import re


class EngagementScorer:

    def calculate(
        self,
        content,
    ):

        # =========================
        # VALIDATE CONTENT
        # =========================

        if not content:

            return {

                "score": 0,
            }

        # =========================
        # LOWERCASE CONTENT
        # =========================

        lower_content = (
            content.lower()
        )

        # =========================
        # ENGAGEMENT WORDS
        # =========================

        engagement_words = [

            "you",

            "your",

            "discover",

            "learn",

            "improve",

            "best",

            "important",

            "easy",

            "powerful",

            "essential",

            "secret",

            "ultimate",

            "simple",

            "quick",

            "effective",

            "help",

            "boost",

            "increase",

            "why",

            "how",
        ]

        # =========================
        # COUNT ENGAGEMENT WORDS
        # =========================

        engagement_matches = 0

        for word in engagement_words:

            engagement_matches += len(

                re.findall(

                    rf"\b{re.escape(word)}\b",

                    lower_content
                )
            )

        # =========================
        # QUESTION COUNT
        # =========================

        question_count = len(

            re.findall(
                r"\?",
                content
            )
        )

        # =========================
        # EXCLAMATION COUNT
        # =========================

        exclamation_count = len(

            re.findall(
                r"!",
                content
            )
        )

        # =========================
        # INITIAL SCORE
        # =========================

        score = 50

        # =========================
        # ENGAGEMENT BONUS
        # =========================

        score += min(
            engagement_matches,
            30
        )

        # =========================
        # QUESTION BONUS
        # =========================

        score += min(
            question_count * 2,
            10
        )

        # =========================
        # EXCLAMATION BONUS
        # =========================

        score += min(
            exclamation_count,
            10
        )

        # =========================
        # LIMIT SCORE
        # =========================

        score = max(
            0,
            min(score, 100)
        )

        # =========================
        # RETURN RESULT
        # =========================

        return {

            "score": score,

            "engagement_matches": (
                engagement_matches
            ),

            "question_count": (
                question_count
            ),

            "exclamation_count": (
                exclamation_count
            ),
        }