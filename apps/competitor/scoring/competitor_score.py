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

    # ==================================================
    # CONTENT SCORE
    # ==================================================

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

    # ==================================================
    # STRUCTURE SCORE
    # ==================================================

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

    # ==================================================
    # INTENT SCORE
    # ==================================================

    def calculate_intent_score(
        self,
        intent_analysis,
    ):

        """
        Score keyword intent competitiveness.
        """

        primary_intent = (
            intent_analysis.get(
                "primary_intent",
                "informational"
            )
        )

        if primary_intent == "transactional":

            return 90

        if primary_intent == "commercial":

            return 80

        if primary_intent == "news":

            return 75

        return 65

    # ==================================================
    # FREQUENCY SCORE
    # ==================================================

    def calculate_frequency_score(
        self,
        heading_frequency,
    ):

        """
        Score SERP heading competition.
        """

        total_frequency = sum(
            heading_frequency.values()
        )

        if total_frequency >= 50:

            return 95

        if total_frequency >= 35:

            return 85

        if total_frequency >= 20:

            return 70

        if total_frequency >= 10:

            return 55

        return 40

    # ==================================================
    # GAP PRIORITY SCORE
    # ==================================================

    def calculate_gap_priority_score(
        self,
        content_gaps,
    ):

        """
        Score SEO opportunity gaps.
        """

        critical = 0

        high = 0

        medium = 0

        low = 0

        for gap in content_gaps:

            priority = gap.get(
                "priority",
                "low"
            )

            if priority == "critical":

                critical += 1

            elif priority == "high":

                high += 1

            elif priority == "medium":

                medium += 1

            else:

                low += 1

        score = (

            critical * 25
            + high * 15
            + medium * 8
            + low * 3
        )

        return ScoringHelpers.normalize_score(
            score
        )

    # ==================================================
    # WEAKNESS SEVERITY SCORE
    # ==================================================

    def calculate_weakness_severity_score(
        self,
        weaknesses,
    ):

        """
        Score competitor weaknesses.
        """

        total_severity = 0

        for weakness in weaknesses:

            total_severity += (
                weakness.get(
                    "severity",
                    0
                )
            )

        return ScoringHelpers.normalize_score(
            total_severity * 5
        )

    # ==================================================
    # COMPETITION LEVEL
    # ==================================================

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

    # ==================================================
    # SEO OPPORTUNITY
    # ==================================================

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

    # ==================================================
    # CONFIDENCE
    # ==================================================

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

    # ==================================================
    # SCORE GRADE
    # ==================================================

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

    # ==================================================
    # MAIN SCORE CALCULATION
    # ==================================================

    def calculate(
        self,
        content_analysis,
        structure_analysis,
        gap_analysis,
        weakness_analysis,
        intent_analysis=None,
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

        heading_frequency = (
            content_analysis.get(
                "heading_frequency",
                {}
            )
        )

        average_sections = (
            structure_analysis.get(
                "average_sections",
                0
            )
        )

        content_gaps = (
            gap_analysis.get(
                "content_gaps",
                []
            )
        )

        weaknesses = (
            weakness_analysis.get(
                "weaknesses",
                []
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

        frequency_score = (
            self.calculate_frequency_score(
                heading_frequency
            )
        )

        gap_priority_score = (
            self.calculate_gap_priority_score(
                content_gaps
            )
        )

        weakness_severity_score = (
            self.calculate_weakness_severity_score(
                weaknesses
            )
        )

        intent_score = 70

        if intent_analysis:

            intent_score = (
                self.calculate_intent_score(
                    intent_analysis
                )
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
                    "weight": 0.25,
                },

                {
                    "score": (
                        structure_score
                    ),
                    "weight": 0.20,
                },

                {
                    "score": (
                        frequency_score
                    ),
                    "weight": 0.15,
                },

                {
                    "score": (
                        gap_priority_score
                    ),
                    "weight": 0.15,
                },

                {
                    "score": (
                        weakness_severity_score
                    ),
                    "weight": 0.15,
                },

                {
                    "score": (
                        intent_score
                    ),
                    "weight": 0.10,
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

            "frequency_score": (
                frequency_score
            ),

            "gap_priority_score": (
                gap_priority_score
            ),

            "weakness_severity_score": (
                weakness_severity_score
            ),

            "intent_score": (
                intent_score
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