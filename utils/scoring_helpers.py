"""
Central scoring helper utilities.
"""


class ScoringHelpers:

    # =========================
    # NORMALIZE SCORE
    # =========================

    @classmethod
    def normalize_score(
        cls,
        score,
        min_score=0,
        max_score=100
    ):

        # =========================
        # HANDLE INVALID VALUES
        # =========================

        if score is None:

            return 0

        # =========================
        # CLAMP SCORE
        # =========================

        score = max(
            min_score,
            min(score, max_score)
        )

        return round(
            score,
            2
        )

    # =========================
    # CALCULATE PERCENTAGE
    # =========================

    @classmethod
    def percentage(
        cls,
        value,
        total
    ):

        if total == 0:

            return 0

        return round(

            (value / total) * 100,

            2
        )

    # =========================
    # WEIGHTED SCORE
    # =========================

    @classmethod
    def weighted_score(
        cls,
        values
    ):

        """
        Example:

        values = [
            {"score": 80, "weight": 0.4},
            {"score": 70, "weight": 0.3},
            {"score": 90, "weight": 0.3},
        ]
        """

        total_score = 0

        total_weight = 0

        for item in values:

            score = item.get(
                "score",
                0
            )

            weight = item.get(
                "weight",
                0
            )

            total_score += (
                score * weight
            )

            total_weight += weight

        if total_weight == 0:

            return 0

        final_score = (

            total_score / total_weight
        )

        return round(
            final_score,
            2
        )

    # =========================
    # SCORE GRADE
    # =========================

    @classmethod
    def score_grade(
        cls,
        score
    ):

        score = cls.normalize_score(
            score
        )

        if score >= 90:

            return "A+"

        elif score >= 80:

            return "A"

        elif score >= 70:

            return "B"

        elif score >= 60:

            return "C"

        elif score >= 50:

            return "D"

        return "F"

    # =========================
    # CONFIDENCE LEVEL
    # =========================

    @classmethod
    def confidence_level(
        cls,
        score
    ):

        score = cls.normalize_score(
            score
        )

        if score >= 85:

            return "very_high"

        elif score >= 70:

            return "high"

        elif score >= 50:

            return "medium"

        elif score >= 30:

            return "low"

        return "very_low"

    # =========================
    # AVERAGE SCORE
    # =========================

    @classmethod
    def average_score(
        cls,
        scores
    ):

        if not scores:

            return 0

        return round(

            sum(scores) / len(scores),

            2
        )

    # =========================
    # COMBINE SCORES
    # =========================

    @classmethod
    def combine_scores(
        cls,
        *scores
    ):

        valid_scores = [

            score for score in scores

            if isinstance(
                score,
                (int, float)
            )
        ]

        if not valid_scores:

            return 0

        return cls.average_score(
            valid_scores
        )