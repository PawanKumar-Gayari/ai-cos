"""
Publisher models.
"""

from __future__ import annotations

from django.db import models

from apps.engine.models import (
    Article,
)


# ==================================================
# PUBLISHED POST
# ==================================================

class PublishedPost(
    models.Model
):

    # ==============================================
    # STATUS CHOICES
    # ==============================================

    STATUS_DRAFT = "draft"

    STATUS_PUBLISHED = "published"

    STATUS_FAILED = "failed"

    STATUS_PENDING = "pending"

    STATUS_CHOICES = [

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

        (
            STATUS_PENDING,
            "Pending",
        ),
    ]

    # ==============================================
    # ARTICLE
    # ==============================================

    article = models.ForeignKey(

        Article,

        on_delete=models.CASCADE,

        related_name=(
            "published_posts"
        ),
    )

    # ==============================================
    # WORDPRESS DATA
    # ==============================================

    wordpress_post_id = models.CharField(

        max_length=255,

        blank=True,

        null=True,
    )

    wordpress_url = models.URLField(

        blank=True,

        null=True,
    )

    # ==============================================
    # PUBLISH STATUS
    # ==============================================

    status = models.CharField(

        max_length=20,

        choices=STATUS_CHOICES,

        default=STATUS_PENDING,
    )

    # ==============================================
    # ERROR HANDLING
    # ==============================================

    error_message = models.TextField(

        blank=True,

        null=True,
    )

    publish_attempts = models.PositiveIntegerField(

        default=0
    )

    # ==============================================
    # RESPONSE DATA
    # ==============================================

    response_data = models.JSONField(

        default=dict,

        blank=True,
    )

    # ==============================================
    # TIMESTAMPS
    # ==============================================

    published_at = models.DateTimeField(

        blank=True,

        null=True,
    )

    created_at = models.DateTimeField(

        auto_now_add=True
    )

    updated_at = models.DateTimeField(

        auto_now=True
    )

    # ==================================================
    # META
    # ==================================================

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

    # ==================================================
    # STRING
    # ==================================================

    def __str__(
        self,
    ):

        return (

            f"{self.article.title} "
            f"({self.status})"
        )