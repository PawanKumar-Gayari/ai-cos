"""
Analytics models.
"""

from django.db import models

from apps.engine.models import (
    Article,
)

from apps.generator.models import (
    GeneratorConfig,
)

from apps.keywords.models import (
    KeywordAnalysis,
)


# ==================================================
# ARTICLE ANALYTICS
# ==================================================

class ArticleAnalytics(
    models.Model
):

    QUALITY_CHOICES = [

        ("excellent", "Excellent"),

        ("good", "Good"),

        ("average", "Average"),

        ("poor", "Poor"),
    ]

    # ==============================================
    # RELATIONS
    # ==============================================

    article = models.OneToOneField(

        Article,

        on_delete=models.CASCADE,

        related_name="analytics",
    )

    keyword_analysis = (
        models.ForeignKey(

            KeywordAnalysis,

            on_delete=models.SET_NULL,

            blank=True,

            null=True,

            related_name=(
                "article_analytics"
            ),
        )
    )

    generator_config = (
        models.ForeignKey(

            GeneratorConfig,

            on_delete=models.SET_NULL,

            blank=True,

            null=True,
        )
    )

    # ==============================================
    # GENERATION
    # ==============================================

    provider = models.CharField(

        max_length=100,

        blank=True,

        null=True,
    )

    model_name = models.CharField(

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

    retry_count = (
        models.IntegerField(
            default=0
        )
    )

    # ==============================================
    # CONTENT QUALITY
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

    final_quality_score = (
        models.IntegerField(
            default=0
        )
    )

    quality_status = (
        models.CharField(

            max_length=50,

            choices=QUALITY_CHOICES,

            default="average",
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

    heading_score = (
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
    # PERFORMANCE
    # ==============================================

    token_usage = (
        models.IntegerField(
            default=0
        )
    )

    estimated_cost = (
        models.FloatField(
            default=0
        )
    )

    response_latency = (
        models.FloatField(
            default=0
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

    raw_metadata = (
        models.JSONField(
            default=dict,
            blank=True,
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

    published_at = (
        models.DateTimeField(
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
    # META
    # ==================================================

    class Meta:

        ordering = [
            "-created_at"
        ]

        verbose_name = (
            "Article Analytics"
        )

        verbose_name_plural = (
            "Article Analytics"
        )

    # ==================================================
    # STRING
    # ==================================================

    def __str__(
        self,
    ):

        return (

            f"Analytics | "
            f"{self.article.title}"
        )


# ==================================================
# PROVIDER ANALYTICS
# ==================================================

class ProviderAnalytics(
    models.Model
):

    PROVIDER_CHOICES = [

        ("openai", "OpenAI"),

        ("gemini", "Gemini"),

        ("ollama", "Ollama"),
    ]

    # ==============================================
    # PROVIDER
    # ==============================================

    provider_name = (
        models.CharField(

            max_length=100,

            choices=PROVIDER_CHOICES,

            unique=True,
        )
    )

    model_name = models.CharField(

        max_length=100,

        blank=True,

        null=True,
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

    total_fallbacks = (
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

    average_quality_score = (
        models.FloatField(
            default=0
        )
    )

    uptime_percentage = (
        models.FloatField(
            default=100
        )
    )

    # ==============================================
    # SYSTEM
    # ==============================================

    last_error = (
        models.TextField(
            blank=True,
            null=True,
        )
    )

    last_success = (
        models.DateTimeField(
            blank=True,
            null=True,
        )
    )

    last_failure = (
        models.DateTimeField(
            blank=True,
            null=True,
        )
    )

    healthy = (
        models.BooleanField(
            default=True
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
    # META
    # ==================================================

    class Meta:

        ordering = [
            "provider_name"
        ]

        verbose_name = (
            "Provider Analytics"
        )

        verbose_name_plural = (
            "Provider Analytics"
        )

    # ==================================================
    # STRING
    # ==================================================

    def __str__(
        self,
    ):

        return (

            f"{self.provider_name} "
            f"Analytics"
        )