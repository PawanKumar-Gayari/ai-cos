"""
Analytics admin configuration.
"""

from __future__ import annotations

from django.contrib import admin
from django.utils.html import format_html

from apps.analytics.models import (
    ArticleAnalytics,
    ProviderAnalytics,
)


# ==================================================
# ARTICLE ANALYTICS ADMIN
# ==================================================

@admin.register(
    ArticleAnalytics
)
class ArticleAnalyticsAdmin(
    admin.ModelAdmin
):

    # ==============================================
    # LIST DISPLAY
    # ==============================================

    list_display = (

        "article_title",

        "provider",

        "quality_badge",

        "seo_score",

        "rewrite_score",

        "verification_score",

        "word_count",

        "published",

        "created_at",
    )

    # ==============================================
    # FILTERS
    # ==============================================

    list_filter = (

        "quality_status",

        "provider",

        "published",

        "created_at",
    )

    # ==============================================
    # SEARCH
    # ==============================================

    search_fields = (

        "article__title",

        "provider",
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

        "provider",

        "generation_time",

        "used_fallback",

        "rewrite_score",

        "readability_score",

        "engagement_score",

        "ai_detection_score",

        "verification_score",

        "verified_claims",

        "flagged_claims",

        "seo_score",

        "keyword_density",

        "word_count",

        "published",

        "publish_url",

        "error_count",

        "warnings",

        "final_quality_score",

        "quality_status",

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

    @admin.display(
        description="Quality"
    )
    def quality_badge(
        self,
        obj,
    ):

        score = (
            obj.final_quality_score
        )

        color = "#dc3545"

        if score >= 85:

            color = "#198754"

        elif score >= 70:

            color = "#fd7e14"

        return format_html(

            '<strong style="color:{};">'
            '{} ({})'
            '</strong>',

            color,

            obj.quality_status.title(),

            score,
        )


# ==================================================
# PROVIDER ANALYTICS ADMIN
# ==================================================

@admin.register(
    ProviderAnalytics
)
class ProviderAnalyticsAdmin(
    admin.ModelAdmin
):

    # ==============================================
    # LIST DISPLAY
    # ==============================================

    list_display = (

        "provider_name",

        "success_rate",

        "formatted_response_time",

        "formatted_quality_score",

        "total_requests",

        "total_fallbacks",

        "updated_at",
    )

    # ==============================================
    # FILTERS
    # ==============================================

    list_filter = (

        "provider_name",

        "created_at",
    )

    # ==============================================
    # SEARCH
    # ==============================================

    search_fields = (

        "provider_name",
    )

    # ==============================================
    # ORDERING
    # ==============================================

    ordering = (

        "-updated_at",
    )

    # ==============================================
    # READONLY
    # ==============================================

    readonly_fields = (

        "provider_name",

        "total_requests",

        "successful_requests",

        "failed_requests",

        "average_response_time",

        "average_quality_score",

        "total_fallbacks",

        "last_error",

        "created_at",

        "updated_at",
    )

    # ==============================================
    # PAGINATION
    # ==============================================

    list_per_page = 25

    # ==================================================
    # SUCCESS RATE
    # ==================================================

    @admin.display(
        description="Success Rate"
    )
    def success_rate(
        self,
        obj,
    ):

        if obj.total_requests == 0:

            return "0%"

        rate = (

            obj.successful_requests

            / obj.total_requests

        ) * 100

        color = "#dc3545"

        if rate >= 85:

            color = "#198754"

        elif rate >= 70:

            color = "#fd7e14"

        return format_html(

            '<strong style="color:{};">'
            '{}%'
            '</strong>',

            color,

            round(rate, 1),
        )

    # ==================================================
    # RESPONSE TIME
    # ==================================================

    @admin.display(
        description="Avg Response"
    )
    def formatted_response_time(
        self,
        obj,
    ):

        return (
            f"{round(obj.average_response_time, 2)}s"
        )

    # ==================================================
    # QUALITY SCORE
    # ==================================================

    @admin.display(
        description="Avg Quality"
    )
    def formatted_quality_score(
        self,
        obj,
    ):

        score = (
            obj.average_quality_score
        )

        color = "#dc3545"

        if score >= 85:

            color = "#198754"

        elif score >= 70:

            color = "#fd7e14"

        return format_html(

            '<strong style="color:{};">'
            '{}'
            '</strong>',

            color,

            round(score, 1),
        )