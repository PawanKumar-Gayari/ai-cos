"""
Verifier dashboard service.
"""

from apps.verifier.services.verification_metrics_service import (
    VerificationMetricsService,
)


class VerifierDashboardService:

    def __init__(self):

        # =========================
        # METRICS SERVICE
        # =========================

        self.metrics_service = (
            VerificationMetricsService()
        )

    def build_dashboard(
        self,
        verification_results
    ):

        # =========================
        # BASE METRICS
        # =========================

        metrics = (

            self.metrics_service.build_metrics(
                verification_results
            )
        )

        # =========================
        # HIGH RISK CONTENT
        # =========================

        high_risk_results = [

            result

            for result in verification_results

            if result.get(
                "final_score",
                0
            ) < 50
        ]

        # =========================
        # HALLUCINATION ALERTS
        # =========================

        hallucination_alerts = [

            result

            for result in verification_results

            if result.get(
                "hallucination_score",
                100
            ) < 50
        ]

        # =========================
        # SPAM ALERTS
        # =========================

        spam_alerts = [

            result

            for result in verification_results

            if result.get(
                "spam_score",
                100
            ) < 50
        ]

        # =========================
        # SOURCE TRUST ALERTS
        # =========================

        source_alerts = [

            result

            for result in verification_results

            if result.get(
                "source_score",
                100
            ) < 50
        ]

        # =========================
        # BUILD DASHBOARD DATA
        # =========================

        return {

            "metrics": metrics,

            "high_risk_count": len(
                high_risk_results
            ),

            "hallucination_alert_count": len(
                hallucination_alerts
            ),

            "spam_alert_count": len(
                spam_alerts
            ),

            "source_alert_count": len(
                source_alerts
            ),

            "recent_high_risk_results": (
                high_risk_results[:10]
            ),
        }