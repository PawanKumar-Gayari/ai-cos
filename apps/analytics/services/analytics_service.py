"""
Analytics service layer.
"""

from __future__ import annotations

from django.db.models import Avg
from django.db.models import Sum

from apps.analytics.models import (
    ArticleAnalytics,
)

from apps.analytics.models import (
    ProviderAnalytics,
)

from apps.analytics.scoring.performance_score import (
    PerformanceScorer,
)


class AnalyticsService:

    def __init__(
        self,
    ):

        # ======================================
        # SCORER
        # ======================================

        self.scorer = (
            PerformanceScorer()
        )

    # ==================================================
    # ARTICLE PERFORMANCE
    # ==================================================

    def article_performance(
        self,
        article_id: int,
    ) -> dict:

        analytics = (

            ArticleAnalytics.objects.select_related(
                "article"
            ).get(
                article_id=article_id
            )
        )

        score_result = (

            self.scorer.article_score(

                seo_score=(
                    analytics.seo_score
                ),

                rewrite_score=(
                    analytics.rewrite_score
                ),

                verification_score=(
                    analytics.verification_score
                ),

                readability_score=(
                    analytics.readability_score
                ),

                engagement_score=(
                    analytics.engagement_score
                ),
            )
        )

        return {

            "article_id": (
                analytics.article.id
            ),

            "title": (
                analytics.article.title
            ),

            "performance_score": (
                score_result["score"]
            ),

            "status": (
                score_result["status"]
            ),

            "seo_score": (
                analytics.seo_score
            ),

            "verification_score": (
                analytics.verification_score
            ),

            "rewrite_score": (
                analytics.rewrite_score
            ),

            "word_count": (
                analytics.word_count
            ),

            "published": (
                analytics.published
            ),
        }

    # ==================================================
    # PROVIDER PERFORMANCE
    # ==================================================

    def provider_performance(
        self,
        provider_name: str,
    ) -> dict:

        provider = (

            ProviderAnalytics.objects.get(
                provider_name=provider_name
            )
        )

        success_rate = 0

        if provider.total_requests > 0:

            success_rate = (

                provider.successful_requests

                / provider.total_requests

            ) * 100

        fallback_rate = 0

        if provider.total_requests > 0:

            fallback_rate = (

                provider.total_fallbacks

                / provider.total_requests

            ) * 100

        score_result = (

            self.scorer.provider_score(

                success_rate=(
                    success_rate
                ),

                avg_response_time=(
                    provider.average_response_time
                ),

                avg_quality_score=(
                    provider.average_quality_score
                ),

                fallback_rate=(
                    fallback_rate
                ),
            )
        )

        return {

            "provider": (
                provider.provider_name
            ),

            "performance_score": (
                score_result["score"]
            ),

            "status": (
                score_result["status"]
            ),

            "success_rate": round(
                success_rate,
                2,
            ),

            "fallback_rate": round(
                fallback_rate,
                2,
            ),

            "avg_response_time": round(
                provider.average_response_time,
                2,
            ),

            "avg_quality_score": round(
                provider.average_quality_score,
                2,
            ),
        }

    # ==================================================
    # SYSTEM PERFORMANCE
    # ==================================================

    def system_performance(
        self,
    ) -> dict:

        total_articles = (
            ArticleAnalytics.objects.count()
        )

        avg_quality = (

            ArticleAnalytics.objects.aggregate(

                avg=Avg(
                    "final_quality_score"
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

        providers = (
            ProviderAnalytics.objects.all()
        )

        total_success = 0
        total_failed = 0

        for provider in providers:

            total_success += (
                provider.successful_requests
            )

            total_failed += (
                provider.failed_requests
            )

        total_requests = (
            total_success
            + total_failed
        )

        success_rate = 0

        if total_requests > 0:

            success_rate = (

                total_success
                / total_requests

            ) * 100

        failure_rate = 100 - success_rate

        score_result = (

            self.scorer.system_health_score(

                success_rate=(
                    success_rate
                ),

                avg_quality=(
                    avg_quality
                ),

                verification_avg=(
                    avg_verification
                ),

                failure_rate=(
                    failure_rate
                ),
            )
        )

        return {

            "articles": (
                total_articles
            ),

            "success_rate": round(
                success_rate,
                2,
            ),

            "average_quality": round(
                avg_quality,
                2,
            ),

            "average_verification": round(
                avg_verification,
                2,
            ),

            "system_score": (
                score_result["score"]
            ),

            "system_status": (
                score_result["status"]
            ),
        }

    # ==================================================
    # BEST ARTICLES
    # ==================================================

    def best_articles(
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

        for analytics in articles:

            results.append({

                "article_id": (
                    analytics.article.id
                ),

                "title": (
                    analytics.article.title
                ),

                "quality_score": (
                    analytics.final_quality_score
                ),

                "seo_score": (
                    analytics.seo_score
                ),

                "verification_score": (
                    analytics.verification_score
                ),
            })

        return results

    # ==================================================
    # WARNING ARTICLES
    # ==================================================

    def warning_articles(
        self,
    ) -> list[dict]:

        articles = (

            ArticleAnalytics.objects.exclude(
                warnings=[]
            )
        )

        results = []

        for analytics in articles:

            results.append({

                "article_id": (
                    analytics.article.id
                ),

                "title": (
                    analytics.article.title
                ),

                "warnings": (
                    analytics.warnings
                ),
            })

        return results