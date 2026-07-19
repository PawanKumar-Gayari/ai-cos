"""
Publisher models.
"""

from __future__ import annotations

from django.db import models

from apps.engine.models import (
    Article,
)


# =========================================================
# PUBLISHED POST
# =========================================================

class PublishedPost(
    models.Model
):

    # =====================================================
    # STATUS CONSTANTS
    # =====================================================

    STATUS_PENDING = "pending"

    STATUS_DRAFT = "draft"

    STATUS_PUBLISHED = "published"

    STATUS_FAILED = "failed"

    STATUS_CHOICES = [

        (
            STATUS_PENDING,
            "Pending",
        ),

        (
            STATUS_DRAFT,
            "Draft",
        ),

        (
            STATUS_PUBLISHED,
            "Published",
        ),

        (
            STATUS_FAILED,
            "Failed",
        ),
    ]

    # =====================================================
    # PROVIDER CONSTANTS
    # =====================================================

    PROVIDER_WORDPRESS = (
        "wordpress"
    )

    PROVIDER_CHOICES = [

        (
            PROVIDER_WORDPRESS,
            "WordPress",
        ),
    ]

    # =====================================================
    # ARTICLE RELATION
    # =====================================================

    article = models.ForeignKey(

        Article,

        on_delete=models.CASCADE,

        related_name=(
            "published_posts"
        ),
    )

    # =====================================================
    # PROVIDER DATA
    # =====================================================

    provider = models.CharField(

        max_length=50,

        choices=PROVIDER_CHOICES,

        default=(
            PROVIDER_WORDPRESS
        ),
    )

    publish_method = models.CharField(

        max_length=50,

        default="rest_api",
    )

    # =====================================================
    # WORDPRESS DATA
    # =====================================================

    wordpress_post_id = models.CharField(

        max_length=255,

        blank=True,

        null=True,
    )

    wordpress_url = models.URLField(

        blank=True,

        null=True,
    )

    # =====================================================
    # PUBLISH STATUS
    # =====================================================

    status = models.CharField(

        max_length=20,

        choices=STATUS_CHOICES,

        default=(
            STATUS_PENDING
        ),
    )

    # =====================================================
    # ERROR HANDLING
    # =====================================================

    error_message = models.TextField(

        blank=True,

        null=True,
    )

    error_code = models.CharField(

        max_length=100,

        blank=True,

        null=True,
    )

    last_error_at = (
        models.DateTimeField(

            blank=True,

            null=True,
        )
    )

    publish_attempts = (
        models.PositiveIntegerField(

            default=0
        )
    )

    # =====================================================
    # RESPONSE DATA
    # =====================================================

    response_data = models.JSONField(

        default=dict,

        blank=True,
    )

    # =====================================================
    # PERFORMANCE TRACKING
    # =====================================================

    publish_duration = (
        models.FloatField(

            blank=True,

            null=True,
        )
    )

    # =====================================================
    # TIMESTAMPS
    # =====================================================

    published_at = (
        models.DateTimeField(

            blank=True,

            null=True,
        )
    )

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

    # =====================================================
    # META
    # =====================================================

    class Meta:

        ordering = [
            "-created_at"
        ]

        verbose_name = (
            "Published Post"
        )

        verbose_name_plural = (
            "Published Posts"
        )

        indexes = [

            models.Index(
                fields=[
                    "status"
                ]
            ),

            models.Index(
                fields=[
                    "created_at"
                ]
            ),

            models.Index(
                fields=[
                    "published_at"
                ]
            ),
        ]

        constraints = [

            models.UniqueConstraint(

                fields=[
                    "article",
                    "wordpress_post_id",
                ],

                name=(
                    "unique_article_publish"
                ),
            ),
        ]

    # =====================================================
    # STRING REPRESENTATION
    # =====================================================

    def __str__(
        self,
    ):

        return (

            f"{self.article.title} "
            f"({self.status})"
        )