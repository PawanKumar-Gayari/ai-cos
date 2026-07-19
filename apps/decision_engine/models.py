from django.db import models


class DecisionLog(
    models.Model
):

    STATUS_CHOICES = [

        ("success", "Success"),

        ("failed", "Failed"),

        ("processing", "Processing"),
    ]

    # ==========================================
    # QUERY
    # ==========================================

    keyword = models.CharField(
        max_length=255
    )

    intent = models.CharField(

        max_length=100,

        blank=True,

        null=True,
    )

    # ==========================================
    # PROVIDER
    # ==========================================

    provider = models.CharField(

        max_length=100,

        blank=True,

        null=True,
    )

    model_name = models.CharField(

        max_length=255,

        blank=True,

        null=True,
    )

    # ==========================================
    # SCORES
    # ==========================================

    seo_score = models.FloatField(
        default=0
    )

    competition_score = models.FloatField(
        default=0
    )

    quality_score = models.FloatField(
        default=0
    )

    publish_score = models.FloatField(
        default=0
    )

    ai_quality_score = models.FloatField(
        default=0
    )

    # ==========================================
    # DECISION FLAGS
    # ==========================================

    should_generate = models.BooleanField(
        default=True
    )

    rewrite_required = models.BooleanField(
        default=False
    )

    generation_success = models.BooleanField(
        default=True
    )

    # ==========================================
    # PERFORMANCE
    # ==========================================

    execution_time = models.FloatField(
        default=0
    )

    response_time = models.FloatField(
        default=0
    )

    provider_latency = models.FloatField(
        default=0
    )

    token_usage = models.IntegerField(
        default=0
    )

    estimated_cost = models.FloatField(
        default=0
    )

    # ==========================================
    # EXECUTION STATUS
    # ==========================================

    status = models.CharField(

        max_length=50,

        choices=STATUS_CHOICES,

        default="success",
    )

    error_message = models.TextField(

        blank=True,

        null=True,
    )

    # ==========================================
    # EXTRA METADATA
    # ==========================================

    metadata = models.JSONField(
        default=dict,
        blank=True,
    )

    # ==========================================
    # TIMESTAMPS
    # ==========================================

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:

        ordering = [
            "-created_at"
        ]

        verbose_name = (
            "Decision Log"
        )

        verbose_name_plural = (
            "Decision Logs"
        )

        indexes = [

            models.Index(
                fields=["provider"]
            ),

            models.Index(
                fields=["status"]
            ),

            models.Index(
                fields=["created_at"]
            ),

            models.Index(
                fields=["publish_score"]
            ),
        ]

    def __str__(
        self
    ):

        return (

            f"{self.keyword} | "

            f"{self.provider} | "

            f"{self.status}"
        )