from django.db import models


class EngineExecution(
    models.Model
):

    STATUS_CHOICES = [

        ("success", "Success"),

        ("failed", "Failed"),

        ("processing", "Processing"),

        ("pending", "Pending"),
    ]

    # ==========================================
    # ENGINE INFO
    # ==========================================

    engine_name = models.CharField(
        max_length=255
    )

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
    # QUERY DATA
    # ==========================================

    keyword = models.CharField(
        max_length=255
    )

    task_type = models.CharField(
        max_length=100,

        default="article",
    )

    # ==========================================
    # PERFORMANCE
    # ==========================================

    execution_time = models.FloatField(
        default=0
    )

    memory_usage_mb = models.FloatField(
        default=0
    )

    cpu_usage_percent = models.FloatField(
        default=0
    )

    score = models.FloatField(
        default=0
    )

    # ==========================================
    # STATUS
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
            "Engine Execution"
        )

        verbose_name_plural = (
            "Engine Executions"
        )

    def __str__(
        self
    ):

        return (

            f"{self.engine_name} | "

            f"{self.keyword}"
        )