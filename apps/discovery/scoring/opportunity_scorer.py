"""
Opportunity scoring engine for discovery system.
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

from utils.config import (
    Config,
)


class OpportunityScorer:

    # =========================
    # BONUS PATTERNS
    # =========================

    BONUS_PATTERNS = {

        "best": 5,

        "top": 5,

        "review": 6,

        "guide": 5,

        "how to": 8,

        "tutorial": 6,

        "comparison": 7,

        "vs": 7,

        "alternatives": 7,

        "strategy": 5,

        "roadmap": 6,

        "implementation": 6,
    }

    # =========================
    # INTENT SCORES
    # =========================

    INTENT_SCORES = {

        "transactional": 90,

        "commercial": 80,

        "informational": 70,

        "navigational": 50,

        "general": 40,
    }

    def _keyword_quality_score(
        self,
        keyword
    ):

        word_count = len(
            keyword.split()
        )

        if word_count >= 6:

            return 95

        if word_count >= 5:

            return 90

        if word_count >= 4:

            return 80

        if word_count >= 3:

            return 65

        if word_count >= 2:

            return 50

        return 35

    def _bonus_score(
        self,
        keyword
    ):

        score = 0

        keyword_lower = (
            keyword.lower()
        )

        for pattern, value in (
            self.BONUS_PATTERNS.items()
        ):

            if pattern in keyword_lower:

                score += value

        return min(
            score,
            25
        )

    def score(
        self,
        keyword,
        intent="general",
        trend_score=50
    ):

        # =========================
        # VALIDATE INPUT
        # =========================

        if not keyword:

            return {

                "keyword": "",

                "intent": "general",

                "trend_score": 0,

                "opportunity_score": 0,

                "opportunity_level": "low",

                "confidence": "low",

                "score_grade": "F",
            }

        logger.info(

            f"Scoring keyword opportunity: "
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
        # KEYWORD QUALITY SCORE
        # =========================

        keyword_score = (
            self._keyword_quality_score(
                keyword
            )
        )

        # =========================
        # INTENT SCORE
        # =========================

        intent_score = (
            self.INTENT_SCORES.get(
                intent,
                40
            )
        )

        # =========================
        # TREND SCORE
        # =========================

        trend_score = (
            ScoringHelpers.normalize_score(
                trend_score
            )
        )

        # =========================
        # BONUS SCORE
        # =========================

        bonus_score = (
            self._bonus_score(
                keyword
            )
        )

        # =========================
        # WEIGHTED SCORE
        # =========================

        weighted_score = (
            ScoringHelpers.weighted_score([
                {
                    "score": keyword_score,
                    "weight": 0.30,
                },
                {
                    "score": intent_score,
                    "weight": 0.35,
                },
                {
                    "score": trend_score,
                    "weight": 0.25,
                },
                {
                    "score": bonus_score,
                    "weight": 0.10,
                },
            ])
        )

        # =========================
        # FINAL SCORE
        # =========================

        final_score = (
            ScoringHelpers.normalize_score(
                weighted_score
            )
        )

        final_score = min(
            max(
                final_score,
                0
            ),
            100
        )

        # =========================
        # OPPORTUNITY LEVEL
        # =========================

        if final_score >= (
            Config.HIGH_SCORE_THRESHOLD
        ):

            level = "high"

        elif final_score >= (
            Config.MEDIUM_SCORE_THRESHOLD
        ):

            level = "medium"

        else:

            level = "low"

        # =========================
        # CONFIDENCE LEVEL
        # =========================

        confidence = (
            ScoringHelpers.confidence_level(
                final_score
            )
        )

        # =========================
        # SCORE GRADE
        # =========================

        score_grade = (
            ScoringHelpers.score_grade(
                final_score
            )
        )

        logger.info(

            f"Opportunity score calculated: "
            f"{final_score}"
        )

        # =========================
        # RETURN RESULT
        # =========================

        return {

            "keyword": (
                keyword
            ),

            "intent": (
                intent
            ),

            "trend_score": (
                trend_score
            ),

            "opportunity_score": (
                final_score
            ),

            "opportunity_level": (
                level
            ),

            "confidence": (
                confidence
            ),

            "score_grade": (
                score_grade
            ),
        }