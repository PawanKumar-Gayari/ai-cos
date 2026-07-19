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

    INFORMATIONAL_PATTERNS = {

        "how": 25,

        "guide": 20,

        "tutorial": 20,

        "tips": 15,

        "learn": 20,

        "examples": 15,

        "what is": 25,

        "why": 25,

        "strategy": 15,

        "workflow": 15,

        "roadmap": 15,

        "implementation": 15,

        "best practices": 20,
    }

    COMMERCIAL_PATTERNS = {

        "best": 25,

        "top": 20,

        "review": 25,

        "comparison": 25,

        "vs": 20,

        "alternatives": 20,

        "features": 15,

        "pros and cons": 20,

        "comparison guide": 25,
    }

    TRANSACTIONAL_PATTERNS = {

        "buy": 30,

        "price": 25,

        "discount": 25,

        "deal": 25,

        "coupon": 25,

        "cheap": 20,

        "purchase": 30,

        "offer": 20,

        "pricing": 25,
    }

    NAVIGATIONAL_PATTERNS = {

        "login": 30,

        "official": 25,

        "website": 25,

        "app": 20,

        "download": 25,

        "dashboard": 25,

        "portal": 25,
    }

    def _apply_patterns(
        self,
        keyword,
        patterns
    ):

        score = 0

        for pattern, weight in (
            patterns.items()
        ):

            if pattern in keyword:

                score += weight

        return score

    def detect(
        self,
        keyword
    ):

        # =========================
        # VALIDATE INPUT
        # =========================

        if not keyword:

            return {

                "keyword": "",

                "intent": "general",

                "intent_score": 0,

                "confidence_level": "low",

                "all_scores": {},
            }

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
        # CALCULATE SCORES
        # =========================

        scores = {

            "informational": (
                self._apply_patterns(
                    keyword,
                    self.INFORMATIONAL_PATTERNS
                )
            ),

            "commercial": (
                self._apply_patterns(
                    keyword,
                    self.COMMERCIAL_PATTERNS
                )
            ),

            "transactional": (
                self._apply_patterns(
                    keyword,
                    self.TRANSACTIONAL_PATTERNS
                )
            ),

            "navigational": (
                self._apply_patterns(
                    keyword,
                    self.NAVIGATIONAL_PATTERNS
                )
            ),
        }

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

        if top_score <= 0:

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

            "keyword": (
                keyword
            ),

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