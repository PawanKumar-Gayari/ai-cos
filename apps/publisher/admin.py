"""
Publisher admin configuration.
"""

from __future__ import annotations

from django.contrib import admin
from django.utils.html import (
    format_html,
)

from apps.publisher.models import (
    PublishedPost,
)


# =========================================================
# PUBLISHED POST ADMIN
# =========================================================

@admin.register(
    PublishedPost
)
class PublishedPostAdmin(
    admin.ModelAdmin
):

    # =====================================================
    # LIST DISPLAY
    # =====================================================

    list_display = (

        "id",

        "article_title",

        "provider",

        "status_badge",

        "wordpress_post_id",

        "publish_attempts",

        "publish_duration",

        "short_url",

        "published_at",

        "created_at",
    )

    # =====================================================
    # FILTERS
    # =====================================================

    list_filter = (

        "provider",

        "status",

        "published_at",

        "created_at",
    )

    # =====================================================
    # SEARCH
    # =====================================================

    search_fields = (

        "article__title",

        "wordpress_post_id",

        "wordpress_url",

        "error_message",
    )

    # =====================================================
    # ORDERING
    # =====================================================

    ordering = (

        "-created_at",
    )

    # =====================================================
    # READONLY
    # =====================================================

    readonly_fields = (

        "article",

        "provider",

        "publish_method",

        "wordpress_post_id",

        "wordpress_url",

        "status",

        "error_message",

        "error_code",

        "last_error_at",

        "publish_attempts",

        "publish_duration",

        "response_data",

        "published_at",

        "created_at",

        "updated_at",
    )

    # =====================================================
    # PAGINATION
    # =====================================================

    list_per_page = 25

    # =====================================================
    # DATE HIERARCHY
    # =====================================================

    date_hierarchy = (
        "created_at"
    )

    # =====================================================
    # FIELDSETS
    # =====================================================

    fieldsets = (

        (

            "Article Information",

            {

                "fields": (

                    "article",

                    "provider",

                    "publish_method",
                )
            },
        ),

        (

            "Publishing Data",

            {

                "fields": (

                    "status",

                    "wordpress_post_id",

                    "wordpress_url",

                    "publish_duration",

                    "published_at",
                )
            },
        ),

        (

            "Error Tracking",

            {

                "fields": (

                    "error_message",

                    "error_code",

                    "last_error_at",

                    "publish_attempts",
                )
            },
        ),

        (

            "Response Data",

            {

                "fields": (

                    "response_data",
                )
            },
        ),

        (

            "Timestamps",

            {

                "fields": (

                    "created_at",

                    "updated_at",
                )
            },
        ),
    )

    # =====================================================
    # CUSTOM METHODS
    # =====================================================

    @admin.display(
        description="Article"
    )
    def article_title(
        self,
        obj,
    ):

        return (
            obj.article.title
        )

    # =====================================================
    # STATUS BADGE
    # =====================================================

    @admin.display(
        description="Status"
    )
    def status_badge(
        self,
        obj,
    ):

        color = "#6c757d"

        if (
            obj.status
            == PublishedPost.STATUS_PUBLISHED
        ):

            color = "#198754"

        elif (
            obj.status
            == PublishedPost.STATUS_DRAFT
        ):

            color = "#fd7e14"

        elif (
            obj.status
            == PublishedPost.STATUS_FAILED
        ):

            color = "#dc3545"

        elif (
            obj.status
            == PublishedPost.STATUS_PENDING
        ):

            color = "#0d6efd"

        return format_html(

            '<strong style="color:{};">'
            '{}'
            '</strong>',

            color,

            obj.status.upper(),
        )

    # =====================================================
    # SHORT URL
    # =====================================================

    @admin.display(
        description="WordPress URL"
    )
    def short_url(
        self,
        obj,
    ):

        if not obj.wordpress_url:

            return "-"

        return format_html(

            '<a href="{}" '
            'target="_blank">'
            'Open Post'
            '</a>',

            obj.wordpress_url,
        )