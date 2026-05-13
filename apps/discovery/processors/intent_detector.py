"""
Intent detector for discovery engine.
"""

from utils.keyword_normalizer import (
    KeywordNormalizer,
)

from utils.scoring_helpers import (
    ScoringHelpers,
)

from utils.logger import (
    logger,
)


class IntentDetector:

    # =========================
    # INTENT PATTERNS
    # =========================

    INFORMATIONAL_PATTERNS = [

        "how",

        "guide",

        "tutorial",

        "tips",

        "learn",

        "examples",

        "what is",

        "why",

        "strategy",

        "workflow",
    ]

    COMMERCIAL_PATTERNS = [

        "best",

        "top",

        "review",

        "comparison",

        "vs",

        "alternatives",

        "features",

        "pros and cons",
    ]

    TRANSACTIONAL_PATTERNS = [

        "buy",

        "price",

        "discount",

        "deal",

        "coupon",

        "cheap",

        "purchase",

        "offer",
    ]

    NAVIGATIONAL_PATTERNS = [

        "login",

        "official",

        "website",

        "app",

        "download",

        "dashboard",
    ]

    def detect(
        self,
        keyword
    ):

        logger.info(

            f"Detecting intent for: "
            f"{keyword}"
        )

        # =========================
        # NORMALIZE KEYWORD
        # =========================

        keyword = (
            KeywordNormalizer.normalize(
                keyword
            )
        )

        # =========================
        # INTENT SCORES
        # =========================

        scores = {

            "informational": 0,

            "commercial": 0,

            "transactional": 0,

            "navigational": 0,
        }

        # =========================
        # INFORMATIONAL MATCH
        # =========================

        for pattern in (
            self.INFORMATIONAL_PATTERNS
        ):

            if pattern in keyword:

                scores[
                    "informational"
                ] += 20

        # =========================
        # COMMERCIAL MATCH
        # =========================

        for pattern in (
            self.COMMERCIAL_PATTERNS
        ):

            if pattern in keyword:

                scores[
                    "commercial"
                ] += 20

        # =========================
        # TRANSACTIONAL MATCH
        # =========================

        for pattern in (
            self.TRANSACTIONAL_PATTERNS
        ):

            if pattern in keyword:

                scores[
                    "transactional"
                ] += 20

        # =========================
        # NAVIGATIONAL MATCH
        # =========================

        for pattern in (
            self.NAVIGATIONAL_PATTERNS
        ):

            if pattern in keyword:

                scores[
                    "navigational"
                ] += 20

        # =========================
        # DETERMINE TOP INTENT
        # =========================

        top_intent = max(

            scores,

            key=scores.get
        )

        top_score = scores.get(
            top_intent,
            0
        )

        # =========================
        # DEFAULT GENERAL
        # =========================

        if top_score == 0:

            top_intent = "general"

            top_score = 20

        # =========================
        # NORMALIZE SCORE
        # =========================

        confidence_score = (
            ScoringHelpers.normalize_score(
                top_score
            )
        )

        # =========================
        # CONFIDENCE LEVEL
        # =========================

        confidence_level = (
            ScoringHelpers.confidence_level(
                confidence_score
            )
        )

        logger.info(

            f"Intent detected: "
            f"{top_intent}"
        )

        # =========================
        # RETURN RESULT
        # =========================

        return {

            "keyword": keyword,

            "intent": (
                top_intent
            ),

            "intent_score": (
                confidence_score
            ),

            "confidence_level": (
                confidence_level
            ),

            "all_scores": (
                scores
            ),
        }