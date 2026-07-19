"""
Analytics tracker.
"""

from __future__ import annotations

import logging

from apps.analytics.models import (
    ArticleAnalytics,
)

from apps.analytics.models import (
    ProviderAnalytics,
)

from apps.engine.models import (
    Article,
)


logger = logging.getLogger(
    __name__
)


class AnalyticsTracker:

    # ==================================================
    # TRACK ARTICLE
    # ==================================================

    def track_article(
        self,
        article: Article,
        provider: str = "unknown",
        generation_time: float = 0,
        rewrite_score: int = 0,
        readability_score: int = 0,
        engagement_score: int = 0,
        ai_detection_score: int = 0,
        verification_score: int = 0,
        verified_claims: int = 0,
        flagged_claims: int = 0,
        seo_score: int = 0,
        keyword_density: float = 0,
        used_fallback: bool = False,
        final_quality_score: int = 0,
        quality_status: str = "unknown",
        warnings: list | None = None,
    ) -> ArticleAnalytics:

        # ==============================================
        # WARNINGS
        # ==============================================

        if warnings is None:

            warnings = []

        # ==============================================
        # WORD COUNT
        # ==============================================

        word_count = len(

            article.content.split()
        )

        # ==============================================
        # CREATE / UPDATE
        # ==============================================

        analytics, created = (

            ArticleAnalytics.objects.update_or_create(

                article=article,

                defaults={

                    "provider": (
                        provider
                    ),

                    "generation_time": (
                        generation_time
                    ),

                    "used_fallback": (
                        used_fallback
                    ),

                    "rewrite_score": (
                        rewrite_score
                    ),

                    "readability_score": (
                        readability_score
                    ),

                    "engagement_score": (
                        engagement_score
                    ),

                    "ai_detection_score": (
                        ai_detection_score
                    ),

                    "verification_score": (
                        verification_score
                    ),

                    "verified_claims": (
                        verified_claims
                    ),

                    "flagged_claims": (
                        flagged_claims
                    ),

                    "seo_score": (
                        seo_score
                    ),

                    "keyword_density": (
                        keyword_density
                    ),

                    "word_count": (
                        word_count
                    ),

                    "published": (
                        article.is_published
                    ),

                    "publish_url": (
                        article.published_url
                    ),

                    "final_quality_score": (
                        final_quality_score
                    ),

                    "quality_status": (
                        quality_status
                    ),

                    "warnings": (
                        warnings
                    ),
                },
            )
        )

        logger.info(

            "Analytics tracked "
            "for article_id=%s",

            article.id,
        )

        return analytics

    # ==================================================
    # TRACK PROVIDER
    # ==================================================

    def track_provider(
        self,
        provider_name: str,
        success: bool = True,
        response_time: float = 0,
        quality_score: float = 0,
        fallback_used: bool = False,
        error_message: str | None = None,
    ) -> ProviderAnalytics:

        # ==============================================
        # GET OR CREATE
        # ==============================================

        provider, _ = (

            ProviderAnalytics.objects.get_or_create(

                provider_name=(
                    provider_name
                )
            )
        )

        # ==============================================
        # REQUESTS
        # ==============================================

        provider.total_requests += 1

        if success:

            provider.successful_requests += 1

        else:

            provider.failed_requests += 1

        # ==============================================
        # AVERAGE RESPONSE TIME
        # ==============================================

        current_total = (
            provider.total_requests
        )

        previous_average = (
            provider.average_response_time
        )

        provider.average_response_time = (

            (
                previous_average
                *
                (current_total - 1)
            )

            + response_time

        ) / current_total

        # ==============================================
        # QUALITY SCORE
        # ==============================================

        previous_quality = (
            provider.average_quality_score
        )

        provider.average_quality_score = (

            (
                previous_quality
                *
                (current_total - 1)
            )

            + quality_score

        ) / current_total

        # ==============================================
        # FALLBACKS
        # ==============================================

        if fallback_used:

            provider.total_fallbacks += 1

        # ==============================================
        # ERROR
        # ==============================================

        if error_message:

            provider.last_error = (
                error_message
            )

        provider.save()

        logger.info(

            "Provider analytics updated "
            "provider=%s",

            provider_name,
        )

        return provider