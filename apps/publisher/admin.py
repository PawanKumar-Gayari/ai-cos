"""
Publisher admin configuration.
"""

from __future__ import annotations

from django.contrib import admin
from django.utils.html import format_html

from apps.publisher.models import (
    PublishedPost,
)


# ==================================================
# PUBLISHED POST ADMIN
# ==================================================

@admin.register(
    PublishedPost
)
class PublishedPostAdmin(
    admin.ModelAdmin
):

    # ==============================================
    # LIST DISPLAY
    # ==============================================

    list_display = (

        "article_title",

        "status_badge",

        "wordpress_post_id",

        "publish_attempts",

        "short_url",

        "published_at",

        "created_at",
    )

    # ==============================================
    # FILTERS
    # ==============================================

    list_filter = (

        "status",

        "published_at",

        "created_at",
    )

    # ==============================================
    # SEARCH
    # ==============================================

    search_fields = (

        "article__title",

        "wordpress_post_id",

        "wordpress_url",
    )

    # ==============================================
    # ORDERING
    # ==============================================

    ordering = (

        "-created_at",
    )

    # ==============================================
    # READONLY
    # ==============================================

    readonly_fields = (

        "article",

        "wordpress_post_id",

        "wordpress_url",

        "status",

        "error_message",

        "publish_attempts",

        "response_data",

        "published_at",

        "created_at",

        "updated_at",
    )

    # ==============================================
    # PAGINATION
    # ==============================================

    list_per_page = 25

    # ==================================================
    # CUSTOM METHODS
    # ==================================================

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

    # ==================================================
    # STATUS BADGE
    # ==================================================

    @admin.display(
        description="Status"
    )
    def status_badge(
        self,
        obj,
    ):

        color = "#6c757d"

        if obj.status == "published":

            color = "#198754"

        elif obj.status == "draft":

            color = "#fd7e14"

        elif obj.status == "failed":

            color = "#dc3545"

        elif obj.status == "pending":

            color = "#0d6efd"

        return format_html(

            '<strong style="color:{};">'
            '{}'
            '</strong>',

            color,

            obj.status.upper(),
        )

    # ==================================================
    # SHORT URL
    # ==================================================

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