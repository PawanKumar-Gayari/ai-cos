"""
Enterprise AI generation history models.
"""

import uuid

from django.db import models


class GenerationHistory(
    models.Model
):

    STATUS_PENDING = "pending"

    STATUS_RUNNING = "running"

    STATUS_COMPLETED = "completed"

    STATUS_FAILED = "failed"

    STATUS_RETRYING = "retrying"

    STATUS_CHOICES = [

        (
            STATUS_PENDING,
            "Pending",
        ),

        (
            STATUS_RUNNING,
            "Running",
        ),

        (
            STATUS_COMPLETED,
            "Completed",
        ),

        (
            STATUS_FAILED,
            "Failed",
        ),

        (
            STATUS_RETRYING,
            "Retrying",
        ),
    ]

    # ==================================================
    # PRIMARY KEY
    # ==================================================

    id = models.UUIDField(

        primary_key=True,

        default=uuid.uuid4,

        editable=False,
    )

    # ==================================================
    # TASK INFO
    # ==================================================

    task_id = models.CharField(

        max_length=255,

        db_index=True,
    )

    task_type = models.CharField(

        max_length=100,

        db_index=True,
    )

    status = models.CharField(

        max_length=50,

        choices=STATUS_CHOICES,

        default=STATUS_PENDING,

        db_index=True,
    )

    # ==================================================
    # QUERY INPUT
    # ==================================================

    query = models.TextField()

    normalized_query = (
        models.TextField(

            blank=True,

            null=True,

            db_index=True,
        )
    )

    # ==================================================
    # GENERATED OUTPUT
    # ==================================================

    generated_content = (
        models.TextField()
    )

    content_length = (
        models.PositiveIntegerField(

            default=0
        )
    )

    # ==================================================
    # PROVIDER INFO
    # ==================================================

    provider = models.CharField(

        max_length=100,

        blank=True,

        null=True,

        db_index=True,
    )

    model_name = models.CharField(

        max_length=150,

        blank=True,

        null=True,
    )

    # ==================================================
    # EXECUTION METRICS
    # ==================================================

    execution_time = (
        models.FloatField(

            default=0.0
        )
    )

    retry_count = (
        models.PositiveIntegerField(

            default=0
        )
    )

    # ==================================================
    # TOKEN / COST TRACKING
    # ==================================================

    prompt_tokens = (
        models.PositiveIntegerField(

            default=0
        )
    )

    completion_tokens = (
        models.PositiveIntegerField(

            default=0
        )
    )

    total_tokens = (
        models.PositiveIntegerField(

            default=0
        )
    )

    estimated_cost = (
        models.FloatField(

            default=0.0
        )
    )

    # ==================================================
    # ERROR TRACKING
    # ==================================================

    error_message = models.TextField(

        blank=True,

        null=True,
    )

    traceback = models.TextField(

        blank=True,

        null=True,
    )

    # ==================================================
    # EXTRA METADATA
    # ==================================================

    metadata = models.JSONField(

        default=dict,

        blank=True,
    )

    # ==================================================
    # TIMESTAMPS
    # ==================================================

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

        indexes = [

            models.Index(
                fields=[
                    "task_id"
                ]
            ),

            models.Index(
                fields=[
                    "task_type"
                ]
            ),

            models.Index(
                fields=[
                    "provider"
                ]
            ),

            models.Index(
                fields=[
                    "status"
                ]
            ),

            models.Index(
                fields=[
                    "-created_at"
                ]
            ),
        ]

    # ==================================================
    # SAVE
    # ==================================================

    def save(
        self,
        *args,
        **kwargs,
    ):

        """
        Normalize analytics data.
        """

        if self.query:

            self.normalized_query = (
                self.query
                .strip()
                .lower()
            )

        if self.generated_content:

            self.content_length = len(
                self.generated_content
            )

        self.total_tokens = (

            self.prompt_tokens

            + self.completion_tokens
        )

        super().save(
            *args,
            **kwargs,
        )

    # ==================================================
    # SUCCESS
    # ==================================================

    @property
    def successful(
        self
    ):

        return (

            self.status
            == self.STATUS_COMPLETED
        )

    # ==================================================
    # FAILED
    # ==================================================

    @property
    def failed(
        self
    ):

        return (

            self.status
            == self.STATUS_FAILED
        )

    # ==================================================
    # STRING
    # ==================================================

    def __str__(
        self
    ):

        return (

            f"{self.task_type} | "

            f"{self.provider} | "

            f"{self.status}"
        )