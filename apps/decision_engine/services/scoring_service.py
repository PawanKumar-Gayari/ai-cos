"""
Central scoring engine service.
"""

import logging

from apps.decision_engine.scoring.seo_score import (
    SEOScore,
)

from apps.decision_engine.scoring.keyword_score import (
    KeywordScore,
)

from apps.decision_engine.scoring.competition_score import (
    CompetitionScore,
)

from apps.decision_engine.scoring.quality_score import (
    QualityScore,
)

from apps.decision_engine.scoring.publish_score import (
    PublishScore,
)


logger = logging.getLogger(
    __name__
)


class ScoringService:

    """
    Central AI scoring orchestration.
    """

    def __init__(
        self
    ):

        self.seo_engine = (
            SEOScore()
        )

        self.keyword_engine = (
            KeywordScore()
        )

        self.competition_engine = (
            CompetitionScore()
        )

        self.quality_engine = (
            QualityScore()
        )

        self.publish_engine = (
            PublishScore()
        )

    # ==================================================
    # MAIN SCORING PIPELINE
    # ==================================================

    def calculate_scores(
        self,
        payload,
    ):

        """
        Calculate all scores.
        """

        keyword = str(

            payload.get(
                "keyword",
                ""
            )
        )

        keyword_length = len(
            keyword.split()
        )

        # ==========================================
        # SCORE ENGINES
        # ==========================================

        seo_score = (

            self.seo_engine.calculate(
                keyword
            )
        )

        keyword_score = (

            self.keyword_engine.calculate(
                keyword
            )
        )

        competition_score = (

            self.competition_engine.calculate(
                keyword_length
            )
        )

        quality_score = (

            self.quality_engine.calculate(
                keyword_length
            )
        )

        publish_score = (

            self.publish_engine.calculate(

                seo_score,

                quality_score,
            )
        )

        # ==========================================
        # FINAL SCORES
        # ==========================================

        scores = {

            "seo_score": (
                seo_score
            ),

            "keyword_score": (
                keyword_score
            ),

            "competition_score": (
                competition_score
            ),

            "quality_score": (
                quality_score
            ),

            "publish_score": (
                publish_score
            ),
        }

        logger.info(

            f"Scoring completed "
            f"for keyword: {keyword}"
        )

        return scores