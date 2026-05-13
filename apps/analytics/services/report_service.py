"""
Report service.
"""

from __future__ import annotations

from datetime import datetime

from apps.analytics.insights import (
    AnalyticsInsights,
)

from apps.analytics.services.analytics_service import (
    AnalyticsService,
)


class ReportService:

    def __init__(
        self,
    ):

        # ======================================
        # SERVICES
        # ======================================

        self.analytics_service = (
            AnalyticsService()
        )

        self.insights = (
            AnalyticsInsights()
        )

    # ==================================================
    # EXECUTIVE REPORT
    # ==================================================

    def executive_report(
        self,
    ) -> dict:

        overview = (
            self.insights.system_overview()
        )

        quality = (
            self.insights.quality_report()
        )

        health = (
            self.insights.system_health()
        )

        return {

            "generated_at": (
                datetime.utcnow().isoformat()
            ),

            "overview": (
                overview
            ),

            "quality": (
                quality
            ),

            "health": (
                health
            ),
        }

    # ==================================================
    # PROVIDER REPORT
    # ==================================================

    def provider_report(
        self,
    ) -> dict:

        providers = (
            self.insights.provider_performance()
        )

        ranked = sorted(

            providers,

            key=lambda item: (
                item[
                    "average_quality_score"
                ]
            ),

            reverse=True,
        )

        return {

            "generated_at": (
                datetime.utcnow().isoformat()
            ),

            "providers": (
                ranked
            ),
        }

    # ==================================================
    # VERIFICATION REPORT
    # ==================================================

    def verification_report(
        self,
    ) -> dict:

        verification = (

            self.insights.verification_report()
        )

        warnings = (
            self.insights.warning_report()
        )

        return {

            "generated_at": (
                datetime.utcnow().isoformat()
            ),

            "verification": (
                verification
            ),

            "warnings": (
                warnings
            ),
        }

    # ==================================================
    # CONTENT QUALITY REPORT
    # ==================================================

    def content_quality_report(
        self,
    ) -> dict:

        top_articles = (
            self.insights.top_articles()
        )

        quality = (
            self.insights.quality_report()
        )

        return {

            "generated_at": (
                datetime.utcnow().isoformat()
            ),

            "top_articles": (
                top_articles
            ),

            "quality_distribution": (
                quality
            ),
        }

    # ==================================================
    # SYSTEM OPTIMIZATION REPORT
    # ==================================================

    def optimization_report(
        self,
    ) -> dict:

        system = (
            self.analytics_service.system_performance()
        )

        providers = (
            self.insights.provider_performance()
        )

        recommendations = []

        # ==============================================
        # QUALITY
        # ==============================================

        if system[
            "average_quality"
        ] < 70:

            recommendations.append(

                "Improve rewrite quality "
                "pipeline."
            )

        # ==============================================
        # VERIFICATION
        # ==============================================

        if system[
            "average_verification"
        ] < 75:

            recommendations.append(

                "Improve verification "
                "accuracy and source "
                "coverage."
            )

        # ==============================================
        # PROVIDERS
        # ==============================================

        for provider in providers:

            if provider[
                "success_rate"
            ] < 70:

                recommendations.append(

                    f"Provider "
                    f"{provider['provider']} "
                    f"has low success rate."
                )

            if provider[
                "average_response_time"
            ] > 15:

                recommendations.append(

                    f"Provider "
                    f"{provider['provider']} "
                    f"is responding slowly."
                )

        # ==============================================
        # FALLBACK
        # ==============================================

        if not recommendations:

            recommendations.append(

                "System operating "
                "within healthy parameters."
            )

        return {

            "generated_at": (
                datetime.utcnow().isoformat()
            ),

            "system": (
                system
            ),

            "recommendations": (
                recommendations
            ),
        }

    # ==================================================
    # FULL REPORT
    # ==================================================

    def full_report(
        self,
    ) -> dict:

        return {

            "executive": (
                self.executive_report()
            ),

            "providers": (
                self.provider_report()
            ),

            "verification": (
                self.verification_report()
            ),

            "content_quality": (
                self.content_quality_report()
            ),

            "optimization": (
                self.optimization_report()
            ),
        }