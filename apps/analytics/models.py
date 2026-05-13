"""
Analytics models.
"""

from django.db import models

from apps.engine.models import (
    Article,
)


# ==================================================
# ARTICLE ANALYTICS
# ==================================================

class ArticleAnalytics(
    models.Model
):

    # ==============================================
    # RELATIONS
    # ==============================================

    article = models.OneToOneField(

        Article,

        on_delete=models.CASCADE,

        related_name=(
            "analytics"
        ),
    )

    # ==============================================
    # GENERATION
    # ==============================================

    provider = models.CharField(

        max_length=100,

        blank=True,

        null=True,
    )

    generation_time = (
        models.FloatField(
            default=0
        )
    )

    used_fallback = (
        models.BooleanField(
            default=False
        )
    )

    # ==============================================
    # REWRITE METRICS
    # ==============================================

    rewrite_score = (
        models.IntegerField(
            default=0
        )
    )

    readability_score = (
        models.IntegerField(
            default=0
        )
    )

    engagement_score = (
        models.IntegerField(
            default=0
        )
    )

    ai_detection_score = (
        models.IntegerField(
            default=0
        )
    )

    # ==============================================
    # VERIFICATION
    # ==============================================

    verification_score = (
        models.IntegerField(
            default=0
        )
    )

    verified_claims = (
        models.IntegerField(
            default=0
        )
    )

    flagged_claims = (
        models.IntegerField(
            default=0
        )
    )

    # ==============================================
    # SEO
    # ==============================================

    seo_score = (
        models.IntegerField(
            default=0
        )
    )

    keyword_density = (
        models.FloatField(
            default=0
        )
    )

    word_count = (
        models.IntegerField(
            default=0
        )
    )

    # ==============================================
    # PUBLISHING
    # ==============================================

    published = (
        models.BooleanField(
            default=False
        )
    )

    publish_url = (
        models.URLField(
            blank=True,
            null=True,
        )
    )

    # ==============================================
    # SYSTEM HEALTH
    # ==============================================

    error_count = (
        models.IntegerField(
            default=0
        )
    )

    warnings = (
        models.JSONField(
            default=list,
            blank=True,
        )
    )

    # ==============================================
    # QUALITY
    # ==============================================

    final_quality_score = (
        models.IntegerField(
            default=0
        )
    )

    quality_status = (
        models.CharField(

            max_length=50,

            default="unknown",
        )
    )

    # ==============================================
    # TIMESTAMPS
    # ==============================================

    created_at = (
        models.DateTimeField(
            auto_now_add=True
        )
    )

    updated_at = (
        models.DateTimeField(
            auto_now=True
        )
    )

    # ==================================================
    # STRING
    # ==================================================

    def __str__(
        self,
    ):

        return (

            f"Analytics: "
            f"{self.article.title}"
        )


# ==================================================
# PROVIDER ANALYTICS
# ==================================================

class ProviderAnalytics(
    models.Model
):

    # ==============================================
    # PROVIDER
    # ==============================================

    provider_name = (
        models.CharField(
            max_length=100
        )
    )

    # ==============================================
    # REQUESTS
    # ==============================================

    total_requests = (
        models.IntegerField(
            default=0
        )
    )

    successful_requests = (
        models.IntegerField(
            default=0
        )
    )

    failed_requests = (
        models.IntegerField(
            default=0
        )
    )

    # ==============================================
    # PERFORMANCE
    # ==============================================

    average_response_time = (
        models.FloatField(
            default=0
        )
    )

    # ==============================================
    # QUALITY
    # ==============================================

    average_quality_score = (
        models.FloatField(
            default=0
        )
    )

    # ==============================================
    # SYSTEM
    # ==============================================

    total_fallbacks = (
        models.IntegerField(
            default=0
        )
    )

    last_error = (
        models.TextField(
            blank=True,
            null=True,
        )
    )

    # ==============================================
    # TIMESTAMPS
    # ==============================================

    created_at = (
        models.DateTimeField(
            auto_now_add=True
        )
    )

    updated_at = (
        models.DateTimeField(
            auto_now=True
        )
    )

    # ==================================================
    # STRING
    # ==================================================

    def __str__(
        self,
    ):

        return self.provider_name