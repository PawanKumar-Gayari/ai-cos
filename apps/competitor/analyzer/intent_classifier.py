"""
Search intent classifier.
"""

from utils.logger import (
    competitor_logger,
)

from utils.text_cleaner import (
    TextCleaner,
)


class IntentClassifier:

    COMMERCIAL_PATTERNS = [

        "best",

        "top",

        "review",

        "reviews",

        "comparison",

        "vs",

        "pricing",

        "buy",

        "cheap",

        "discount",
    ]

    INFORMATIONAL_PATTERNS = [

        "what is",

        "how to",

        "guide",

        "tutorial",

        "learn",

        "tips",

        "examples",
    ]

    TRANSACTIONAL_PATTERNS = [

        "buy now",

        "coupon",

        "deal",

        "offers",

        "subscription",
    ]

    NEWS_PATTERNS = [

        "news",

        "latest",

        "update",

        "2026",

        "release date",
    ]

    # ==================================================
    # SAFE CLEAN
    # ==================================================

    def clean_keyword(
        self,
        keyword,
    ):

        return TextCleaner.clean(
            keyword.lower()
        )

    # ==================================================
    # MATCH SCORE
    # ==================================================

    def calculate_match_score(
        self,
        keyword,
        patterns,
    ):

        score = 0

        for pattern in patterns:

            if pattern in keyword:

                score += 1

        return score

    # ==================================================
    # CLASSIFY INTENT
    # ==================================================

    def classify(
        self,
        keyword,
    ):

        """
        Detect search intent.
        """

        cleaned_keyword = (
            self.clean_keyword(
                keyword
            )
        )

        commercial_score = (
            self.calculate_match_score(

                cleaned_keyword,

                self.COMMERCIAL_PATTERNS,
            )
        )

        informational_score = (
            self.calculate_match_score(

                cleaned_keyword,

                self.INFORMATIONAL_PATTERNS,
            )
        )

        transactional_score = (
            self.calculate_match_score(

                cleaned_keyword,

                self.TRANSACTIONAL_PATTERNS,
            )
        )

        news_score = (
            self.calculate_match_score(

                cleaned_keyword,

                self.NEWS_PATTERNS,
            )
        )

        scores = {

            "commercial": (
                commercial_score
            ),

            "informational": (
                informational_score
            ),

            "transactional": (
                transactional_score
            ),

            "news": (
                news_score
            ),
        }

        primary_intent = max(

            scores,

            key=scores.get,
        )

        competitor_logger.info(

            f"[INTENT CLASSIFIED] "
            f"KEYWORD={keyword} "
            f"INTENT={primary_intent}"
        )

        return {

            "primary_intent": (
                primary_intent
            ),

            "scores": scores,
        }