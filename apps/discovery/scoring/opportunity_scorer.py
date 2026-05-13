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

    def score(
        self,
        keyword,
        intent="general",
        trend_score=50
    ):

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
        # KEYWORD LENGTH SCORE
        # =========================

        word_count = len(
            keyword.split()
        )

        if word_count >= 5:

            keyword_score = 90

        elif word_count >= 4:

            keyword_score = 75

        elif word_count >= 3:

            keyword_score = 60

        else:

            keyword_score = 40

        # =========================
        # INTENT SCORE
        # =========================

        intent_scores = {

            "transactional": 90,

            "commercial": 80,

            "informational": 70,

            "navigational": 50,

            "general": 40,
        }

        intent_score = (
            intent_scores.get(
                intent,
                40
            )
        )

        # =========================
        # TREND SCORE NORMALIZATION
        # =========================

        trend_score = (
            ScoringHelpers.normalize_score(
                trend_score
            )
        )

        # =========================
        # BONUS PATTERNS
        # =========================

        bonus_score = 0

        bonus_patterns = [

            "best",

            "top",

            "review",

            "guide",

            "how to",

            "tutorial",

            "comparison",

            "vs",

            "alternatives",
        ]

        for pattern in bonus_patterns:

            if pattern in keyword:

                bonus_score += 5

        bonus_score = min(
            bonus_score,
            20
        )

        # =========================
        # WEIGHTED OPPORTUNITY SCORE
        # =========================

        weighted_score = (
            ScoringHelpers.weighted_score([
                {
                    "score": keyword_score,
                    "weight": 0.3,
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
                    "weight": 0.1,
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

            "keyword": keyword,

            "intent": intent,

            "trend_score": trend_score,

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