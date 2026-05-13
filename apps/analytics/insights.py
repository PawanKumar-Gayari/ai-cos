"""
Analytics insights engine.
"""

from __future__ import annotations

from django.db.models import Avg
from django.db.models import Count
from django.db.models import Sum

from apps.analytics.models import (
    ArticleAnalytics,
)

from apps.analytics.models import (
    ProviderAnalytics,
)


class AnalyticsInsights:

    # ==================================================
    # SYSTEM OVERVIEW
    # ==================================================

    def system_overview(
        self,
    ) -> dict:

        total_articles = (
            ArticleAnalytics.objects.count()
        )

        total_providers = (
            ProviderAnalytics.objects.count()
        )

        published_articles = (

            ArticleAnalytics.objects.filter(
                published=True
            ).count()
        )

        avg_quality = (

            ArticleAnalytics.objects.aggregate(

                avg=Avg(
                    "final_quality_score"
                )

            )["avg"]

            or 0
        )

        avg_seo = (

            ArticleAnalytics.objects.aggregate(

                avg=Avg(
                    "seo_score"
                )

            )["avg"]

            or 0
        )

        avg_verification = (

            ArticleAnalytics.objects.aggregate(

                avg=Avg(
                    "verification_score"
                )

            )["avg"]

            or 0
        )

        avg_generation_time = (

            ArticleAnalytics.objects.aggregate(

                avg=Avg(
                    "generation_time"
                )

            )["avg"]

            or 0
        )

        return {

            "total_articles": (
                total_articles
            ),

            "total_providers": (
                total_providers
            ),

            "published_articles": (
                published_articles
            ),

            "average_quality_score": round(
                avg_quality,
                2,
            ),

            "average_seo_score": round(
                avg_seo,
                2,
            ),

            "average_verification_score": round(
                avg_verification,
                2,
            ),

            "average_generation_time": round(
                avg_generation_time,
                2,
            ),
        }

    # ==================================================
    # PROVIDER PERFORMANCE
    # ==================================================

    def provider_performance(
        self,
    ) -> list[dict]:

        providers = (

            ProviderAnalytics.objects.all()
        )

        results = []

        for provider in providers:

            success_rate = 0

            if provider.total_requests > 0:

                success_rate = (

                    provider.successful_requests

                    / provider.total_requests

                ) * 100

            results.append({

                "provider": (
                    provider.provider_name
                ),

                "total_requests": (
                    provider.total_requests
                ),

                "successful_requests": (
                    provider.successful_requests
                ),

                "failed_requests": (
                    provider.failed_requests
                ),

                "success_rate": round(
                    success_rate,
                    2,
                ),

                "average_response_time": round(
                    provider.average_response_time,
                    2,
                ),

                "average_quality_score": round(
                    provider.average_quality_score,
                    2,
                ),

                "fallbacks": (
                    provider.total_fallbacks
                ),

                "last_error": (
                    provider.last_error
                ),
            })

        return results

    # ==================================================
    # QUALITY REPORT
    # ==================================================

    def quality_report(
        self,
    ) -> dict:

        excellent = (

            ArticleAnalytics.objects.filter(
                quality_status="excellent"
            ).count()
        )

        good = (

            ArticleAnalytics.objects.filter(
                quality_status="good"
            ).count()
        )

        average = (

            ArticleAnalytics.objects.filter(
                quality_status="average"
            ).count()
        )

        poor = (

            ArticleAnalytics.objects.filter(
                quality_status="poor"
            ).count()
        )

        return {

            "excellent": (
                excellent
            ),

            "good": (
                good
            ),

            "average": (
                average
            ),

            "poor": (
                poor
            ),
        }

    # ==================================================
    # VERIFICATION REPORT
    # ==================================================

    def verification_report(
        self,
    ) -> dict:

        verified_claims = (

            ArticleAnalytics.objects.aggregate(

                total=Sum(
                    "verified_claims"
                )

            )["total"]

            or 0
        )

        flagged_claims = (

            ArticleAnalytics.objects.aggregate(

                total=Sum(
                    "flagged_claims"
                )

            )["total"]

            or 0
        )

        avg_verification = (

            ArticleAnalytics.objects.aggregate(

                avg=Avg(
                    "verification_score"
                )

            )["avg"]

            or 0
        )

        return {

            "verified_claims": (
                verified_claims
            ),

            "flagged_claims": (
                flagged_claims
            ),

            "average_verification_score": round(
                avg_verification,
                2,
            ),
        }

    # ==================================================
    # TOP ARTICLES
    # ==================================================

    def top_articles(
        self,
        limit: int = 10,
    ) -> list[dict]:

        articles = (

            ArticleAnalytics.objects.select_related(
                "article"
            )
            .order_by(
                "-final_quality_score"
            )[:limit]
        )

        results = []

        for item in articles:

            results.append({

                "article_id": (
                    item.article.id
                ),

                "title": (
                    item.article.title
                ),

                "quality_score": (
                    item.final_quality_score
                ),

                "seo_score": (
                    item.seo_score
                ),

                "verification_score": (
                    item.verification_score
                ),

                "published": (
                    item.published
                ),
            })

        return results

    # ==================================================
    # WARNING REPORT
    # ==================================================

    def warning_report(
        self,
    ) -> list[dict]:

        articles = (

            ArticleAnalytics.objects.exclude(
                warnings=[]
            )
        )

        results = []

        for item in articles:

            results.append({

                "article_id": (
                    item.article.id
                ),

                "title": (
                    item.article.title
                ),

                "warnings": (
                    item.warnings
                ),
            })

        return results

    # ==================================================
    # SYSTEM HEALTH
    # ==================================================

    def system_health(
        self,
    ) -> dict:

        provider_count = (
            ProviderAnalytics.objects.count()
        )

        failed_requests = (

            ProviderAnalytics.objects.aggregate(

                total=Sum(
                    "failed_requests"
                )

            )["total"]

            or 0
        )

        successful_requests = (

            ProviderAnalytics.objects.aggregate(

                total=Sum(
                    "successful_requests"
                )

            )["total"]

            or 0
        )

        total_requests = (
            failed_requests
            + successful_requests
        )

        success_rate = 0

        if total_requests > 0:

            success_rate = (

                successful_requests
                / total_requests

            ) * 100

        return {

            "providers": (
                provider_count
            ),

            "total_requests": (
                total_requests
            ),

            "successful_requests": (
                successful_requests
            ),

            "failed_requests": (
                failed_requests
            ),

            "system_success_rate": round(
                success_rate,
                2,
            ),
        }

    # ==================================================
    # FULL REPORT
    # ==================================================

    def full_report(
        self,
    ) -> dict:

        return {

            "overview": (
                self.system_overview()
            ),

            "providers": (
                self.provider_performance()
            ),

            "quality": (
                self.quality_report()
            ),

            "verification": (
                self.verification_report()
            ),

            "top_articles": (
                self.top_articles()
            ),

            "warnings": (
                self.warning_report()
            ),

            "health": (
                self.system_health()
            ),
        }