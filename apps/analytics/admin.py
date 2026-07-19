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

@admin.register(ArticleAnalytics)
class ArticleAnalyticsAdmin(admin.ModelAdmin):

    list_display = (

        "article_title",

        "provider",

        "model_name",

        "quality_badge",

        "seo_score",

        "rewrite_score",

        "verification_score",

        "word_count",

        "generation_time",

        "published",

        "created_at",
    )

    list_filter = (

        "quality_status",

        "provider",

        "published",

        "used_fallback",

        "created_at",
    )

    search_fields = (

        "article__title",

        "provider",

        "model_name",
    )

    ordering = ("-created_at",)

    readonly_fields = (

        "article",

        "keyword_analysis",

        "generator_config",

        "provider",

        "model_name",

        "generation_time",

        "used_fallback",

        "retry_count",

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

        "heading_score",

        "token_usage",

        "estimated_cost",

        "response_latency",

        "error_count",

        "warnings",

        "raw_metadata",

        "final_quality_score",

        "quality_status",

        "published",

        "publish_url",

        "published_at",

        "created_at",

        "updated_at",
    )

    list_per_page = 25

    @admin.display(description="Article")
    def article_title(self, obj):

        return obj.article.title

    @admin.display(description="Quality")
    def quality_badge(self, obj):

        score = obj.final_quality_score

        color = "#dc3545"

        if score >= 85:

            color = "#198754"

        elif score >= 70:

            color = "#fd7e14"

        return format_html(

            '<strong style="color:{};">{} ({})</strong>',

            color,

            obj.quality_status.title(),

            score,
        )


# ==================================================
# PROVIDER ANALYTICS ADMIN
# ==================================================

@admin.register(ProviderAnalytics)
class ProviderAnalyticsAdmin(admin.ModelAdmin):

    list_display = (

        "provider_name",

        "model_name",

        "health_badge",

        "success_rate",

        "formatted_response_time",

        "formatted_quality_score",

        "total_requests",

        "failed_requests",

        "total_fallbacks",

        "updated_at",
    )

    list_filter = (

        "provider_name",

        "healthy",

        "created_at",
    )

    search_fields = (

        "provider_name",

        "model_name",
    )

    ordering = ("-updated_at",)

    readonly_fields = (

        "provider_name",

        "model_name",

        "total_requests",

        "successful_requests",

        "failed_requests",

        "average_response_time",

        "average_quality_score",

        "uptime_percentage",

        "total_fallbacks",

        "last_error",

        "last_success",

        "last_failure",

        "healthy",

        "created_at",

        "updated_at",
    )

    list_per_page = 25

    # ==========================================
    # SUCCESS RATE
    # ==========================================

    @admin.display(description="Success Rate")
    def success_rate(self, obj):

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

            '<strong style="color:{};">{}%</strong>',

            color,

            round(rate, 1),
        )

    # ==========================================
    # HEALTH BADGE
    # ==========================================

    @admin.display(description="Health")
    def health_badge(self, obj):

        if obj.healthy:

            return format_html(

                '<strong style="color:{};">Healthy</strong>',

                "#198754",
            )

        return format_html(

            '<strong style="color:{};">Unhealthy</strong>',

            "#dc3545",
        )

    # ==========================================
    # RESPONSE TIME
    # ==========================================

    @admin.display(description="Avg Response")
    def formatted_response_time(self, obj):

        return f"{round(obj.average_response_time, 2)}s"

    # ==========================================
    # QUALITY SCORE
    # ==========================================

    @admin.display(description="Avg Quality")
    def formatted_quality_score(self, obj):

        score = obj.average_quality_score

        color = "#dc3545"

        if score >= 85:

            color = "#198754"

        elif score >= 70:

            color = "#fd7e14"

        return format_html(

            '<strong style="color:{};">{}</strong>',

            color,

            round(score, 1),
        )