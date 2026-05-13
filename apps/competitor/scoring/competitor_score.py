"""
Competitor scoring engine.
"""

from utils.scoring_helpers import (
    ScoringHelpers,
)

from utils.logger import (
    competitor_logger,
)

from utils.config import (
    Config,
)


class CompetitorScore:

    def calculate_content_score(
        self,
        average_word_count,
    ):

        """
        Score competitor content depth.
        """

        if average_word_count >= 5000:

            return 95

        if average_word_count >= 4000:

            return 85

        if average_word_count >= 3000:

            return 75

        if average_word_count >= 2000:

            return 60

        return 40

    def calculate_structure_score(
        self,
        average_sections,
    ):

        """
        Score competitor structure depth.
        """

        if average_sections >= 12:

            return 95

        if average_sections >= 9:

            return 85

        if average_sections >= 7:

            return 75

        if average_sections >= 5:

            return 60

        return 40

    def determine_competition_level(
        self,
        final_score,
    ):

        """
        Determine competition level.
        """

        if final_score >= (
            Config.HIGH_SCORE_THRESHOLD
        ):

            return "high"

        if final_score >= (
            Config.MEDIUM_SCORE_THRESHOLD
        ):

            return "medium"

        return "low"

    def determine_seo_opportunity(
        self,
        competition_level,
    ):

        """
        Determine SEO opportunity.
        """

        if competition_level == "low":

            return "excellent"

        if competition_level == "medium":

            return "good"

        return "difficult"

    def determine_confidence(
        self,
        final_score,
    ):

        """
        Determine strategic confidence.
        """

        if final_score >= 80:

            return "high"

        if final_score >= 60:

            return "medium"

        return "low"

    def determine_grade(
        self,
        final_score,
    ):

        """
        Convert numeric score to grade.
        """

        if final_score >= 85:

            return "A"

        if final_score >= 70:

            return "B"

        if final_score >= 55:

            return "C"

        if final_score >= 40:

            return "D"

        return "F"

    def calculate(
        self,
        content_analysis,
        structure_analysis,
        gap_analysis,
        weakness_analysis,
    ):

        """
        Calculate final competitor score.
        """

        competitor_logger.info(
            "Starting competitor scoring"
        )

        # ==========================================
        # EXTRACT DATA
        # ==========================================

        average_word_count = (
            content_analysis.get(
                "average_word_count",
                0
            )
        )

        average_sections = (
            structure_analysis.get(
                "average_sections",
                0
            )
        )

        gap_score = (
            gap_analysis.get(
                "gap_score",
                0
            )
        )

        weakness_score = (
            weakness_analysis.get(
                "weakness_score",
                0
            )
        )

        # ==========================================
        # BASE SCORES
        # ==========================================

        content_score = (
            self.calculate_content_score(
                average_word_count
            )
        )

        structure_score = (
            self.calculate_structure_score(
                average_sections
            )
        )

        gap_opportunity_score = (
            max(0, 100 - gap_score)
        )

        weakness_resistance_score = (
            max(0, 100 - weakness_score)
        )

        # ==========================================
        # WEIGHTED SCORE
        # ==========================================

        weighted_score = (
            ScoringHelpers.weighted_score([

                {
                    "score": (
                        content_score
                    ),
                    "weight": 0.40,
                },

                {
                    "score": (
                        structure_score
                    ),
                    "weight": 0.30,
                },

                {
                    "score": (
                        gap_opportunity_score
                    ),
                    "weight": 0.15,
                },

                {
                    "score": (
                        weakness_resistance_score
                    ),
                    "weight": 0.15,
                },
            ])
        )

        # ==========================================
        # NORMALIZE SCORE
        # ==========================================

        final_score = (
            ScoringHelpers.normalize_score(
                weighted_score
            )
        )

        # ==========================================
        # CLASSIFICATIONS
        # ==========================================

        competition_level = (
            self.determine_competition_level(
                final_score
            )
        )

        seo_opportunity = (
            self.determine_seo_opportunity(
                competition_level
            )
        )

        strategic_confidence = (
            self.determine_confidence(
                final_score
            )
        )

        score_grade = (
            self.determine_grade(
                final_score
            )
        )

        # ==========================================
        # SCORE BREAKDOWN
        # ==========================================

        score_breakdown = {

            "content_score": (
                content_score
            ),

            "structure_score": (
                structure_score
            ),

            "gap_opportunity_score": (
                gap_opportunity_score
            ),

            "weakness_resistance_score": (
                weakness_resistance_score
            ),
        }

        competitor_logger.info(

            f"Competitor scoring completed | "
            f"FINAL_SCORE={final_score} | "
            f"GRADE={score_grade}"
        )

        # ==========================================
        # RETURN RESULT
        # ==========================================

        return {

            "competition_score": (
                final_score
            ),

            "competition_level": (
                competition_level
            ),

            "seo_opportunity": (
                seo_opportunity
            ),

            "strategic_confidence": (
                strategic_confidence
            ),

            "score_grade": (
                score_grade
            ),

            "score_breakdown": (
                score_breakdown
            ),
        }