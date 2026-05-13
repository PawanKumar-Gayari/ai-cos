"""
Performance scoring engine.
"""

from __future__ import annotations


class PerformanceScorer:

    # ==================================================
    # ARTICLE PERFORMANCE SCORE
    # ==================================================

    def article_score(
        self,
        seo_score: int = 0,
        rewrite_score: int = 0,
        verification_score: int = 0,
        readability_score: int = 0,
        engagement_score: int = 0,
    ) -> dict:

        # ==============================================
        # NORMALIZE
        # ==============================================

        seo_score = max(
            0,
            min(seo_score, 100),
        )

        rewrite_score = max(
            0,
            min(rewrite_score, 100),
        )

        verification_score = max(
            0,
            min(verification_score, 100),
        )

        readability_score = max(
            0,
            min(readability_score, 100),
        )

        engagement_score = max(
            0,
            min(engagement_score, 100),
        )

        # ==============================================
        # WEIGHTED SCORE
        # ==============================================

        final_score = int(

            (
                seo_score * 0.20
            )

            +

            (
                rewrite_score * 0.25
            )

            +

            (
                verification_score * 0.30
            )

            +

            (
                readability_score * 0.15
            )

            +

            (
                engagement_score * 0.10
            )
        )

        # ==============================================
        # QUALITY STATUS
        # ==============================================

        status = (
            "poor"
        )

        if final_score >= 90:

            status = (
                "excellent"
            )

        elif final_score >= 75:

            status = (
                "good"
            )

        elif final_score >= 55:

            status = (
                "average"
            )

        # ==============================================
        # RETURN
        # ==============================================

        return {

            "score": (
                final_score
            ),

            "status": (
                status
            ),
        }

    # ==================================================
    # PROVIDER SCORE
    # ==================================================

    def provider_score(
        self,
        success_rate: float = 0,
        avg_response_time: float = 0,
        avg_quality_score: float = 0,
        fallback_rate: float = 0,
    ) -> dict:

        # ==============================================
        # RESPONSE TIME SCORE
        # ==============================================

        response_score = 100

        if avg_response_time > 20:

            response_score = 40

        elif avg_response_time > 10:

            response_score = 60

        elif avg_response_time > 5:

            response_score = 80

        # ==============================================
        # FALLBACK SCORE
        # ==============================================

        fallback_score = max(

            0,

            100 - int(
                fallback_rate
            )
        )

        # ==============================================
        # FINAL SCORE
        # ==============================================

        final_score = int(

            (
                success_rate * 0.40
            )

            +

            (
                avg_quality_score * 0.30
            )

            +

            (
                response_score * 0.20
            )

            +

            (
                fallback_score * 0.10
            )
        )

        # ==============================================
        # STATUS
        # ==============================================

        status = (
            "unstable"
        )

        if final_score >= 90:

            status = (
                "elite"
            )

        elif final_score >= 75:

            status = (
                "strong"
            )

        elif final_score >= 55:

            status = (
                "usable"
            )

        # ==============================================
        # RETURN
        # ==============================================

        return {

            "score": (
                final_score
            ),

            "status": (
                status
            ),

            "response_score": (
                response_score
            ),

            "fallback_score": (
                fallback_score
            ),
        }

    # ==================================================
    # SYSTEM HEALTH SCORE
    # ==================================================

    def system_health_score(
        self,
        success_rate: float = 0,
        avg_quality: float = 0,
        verification_avg: float = 0,
        failure_rate: float = 0,
    ) -> dict:

        # ==============================================
        # FAILURE PENALTY
        # ==============================================

        stability_score = max(

            0,

            100 - int(
                failure_rate
            )
        )

        # ==============================================
        # FINAL
        # ==============================================

        final_score = int(

            (
                success_rate * 0.35
            )

            +

            (
                avg_quality * 0.30
            )

            +

            (
                verification_avg * 0.25
            )

            +

            (
                stability_score * 0.10
            )
        )

        # ==============================================
        # STATUS
        # ==============================================

        status = (
            "critical"
        )

        if final_score >= 90:

            status = (
                "excellent"
            )

        elif final_score >= 75:

            status = (
                "healthy"
            )

        elif final_score >= 55:

            status = (
                "stable"
            )

        # ==============================================
        # RETURN
        # ==============================================

        return {

            "score": (
                final_score
            ),

            "status": (
                status
            ),
        }