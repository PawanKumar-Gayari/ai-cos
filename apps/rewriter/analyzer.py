"""
Rewrite quality analyzer.
"""

from apps.rewriter.scorer.readability import (
    ReadabilityScorer,
)

from apps.rewriter.scorer.ai_detection import (
    AIDetectionScorer,
)

from apps.rewriter.scorer.engagement import (
    EngagementScorer,
)


class RewriteAnalyzer:

    def __init__(self):

        # =========================
        # SCORERS
        # =========================

        self.readability_scorer = (
            ReadabilityScorer()
        )

        self.ai_detection_scorer = (
            AIDetectionScorer()
        )

        self.engagement_scorer = (
            EngagementScorer()
        )

    def analyze(
        self,
        content,
    ):

        # =========================
        # VALIDATE CONTENT
        # =========================

        if not content:

            return {

                "final_score": 0,
            }

        # =========================
        # READABILITY
        # =========================

        readability_result = (

            self.readability_scorer.calculate(
                content
            )
        )

        # =========================
        # AI DETECTION
        # =========================

        ai_result = (

            self.ai_detection_scorer.calculate(
                content
            )
        )

        # =========================
        # ENGAGEMENT
        # =========================

        engagement_result = (

            self.engagement_scorer.calculate(
                content
            )
        )

        # =========================
        # FINAL SCORE
        # =========================

        final_score = int(

            (
                readability_result[
                    "score"
                ]

                +

                ai_result[
                    "score"
                ]

                +

                engagement_result[
                    "score"
                ]

            ) / 3
        )

        # =========================
        # QUALITY STATUS
        # =========================

        quality_status = (
            "poor"
        )

        if final_score >= 85:

            quality_status = (
                "excellent"
            )

        elif final_score >= 70:

            quality_status = (
                "good"
            )

        elif final_score >= 50:

            quality_status = (
                "average"
            )

        # =========================
        # RETURN RESULT
        # =========================

        return {

            "final_score": (
                final_score
            ),

            "quality_status": (
                quality_status
            ),

            "readability": (
                readability_result
            ),

            "ai_detection": (
                ai_result
            ),

            "engagement": (
                engagement_result
            ),
        }