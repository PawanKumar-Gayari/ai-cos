"""
Production SEO Intelligence Admin
---------------------------------

Enterprise-grade Django admin
configuration.

Features:
- optimized admin performance
- scalable admin filters
- organized SEO management
- production-safe admin
- OCI optimized
"""

from __future__ import annotations

from django.contrib import (
    admin,
)

from apps.keywords.models import (
    KeywordAnalysis,
)


@admin.register(
    KeywordAnalysis
)
class KeywordAnalysisAdmin(
    admin.ModelAdmin
):

    """
    SEO keyword intelligence admin.
    """

    # =====================================================
    # LIST VIEW
    # =====================================================

    list_display = (

        "keyword",

        "language",

        "search_intent",

        "seo_difficulty",

        "keyword_score",

        "search_volume",

        "competition_level",

        "is_trending",

        "is_verified",

        "is_active",

        "updated_at",
    )

    # =====================================================
    # FILTERS
    # =====================================================

    list_filter = (

        "language",

        "search_intent",

        "seo_difficulty",

        "competition_level",

        "is_trending",

        "is_verified",

        "is_active",

        "created_at",

        "updated_at",
    )

    # =====================================================
    # SEARCH
    # =====================================================

    search_fields = (

        "keyword",

        "normalized_keyword",

        "cache_key",
    )

    # =====================================================
    # ORDERING
    # =====================================================

    ordering = (
        "-updated_at",
    )

    # =====================================================
    # READONLY
    # =====================================================

    readonly_fields = (

        "normalized_keyword",

        "cache_key",

        "created_at",

        "updated_at",

        "last_analyzed_at",
    )

    # =====================================================
    # AUTOCOMPLETE
    # =====================================================

    autocomplete_fields = ()

    # =====================================================
    # PERFORMANCE
    # =====================================================

    list_select_related = False

    show_full_result_count = True

    list_per_page = 25

    list_max_show_all = 100

    save_on_top = True

    # =====================================================
    # FIELDSETS
    # =====================================================

    fieldsets = (

        (

            "Keyword Information",

            {

                "fields": (

                    "keyword",

                    "normalized_keyword",

                    "cache_key",

                    "language",

                    "search_intent",
                )
            },
        ),

        (

            "SEO Metrics",

            {

                "fields": (

                    "seo_difficulty",

                    "search_volume",

                    "keyword_score",

                    "trend_score",

                    "competition_score",

                    "competition_level",
                )
            },
        ),

        (

            "Semantic SEO Data",

            {

                "fields": (

                    "related_keywords",

                    "semantic_keywords",

                    "entities",

                    "tags",
                )
            },
        ),

        (

            "Content Strategy",

            {

                "fields": (

                    "recommended_content_type",

                    "target_audience",

                    "recommended_word_count",
                )
            },
        ),

        (

            "Analytics",

            {

                "fields": (

                    "total_analyses",

                    "last_analyzed_at",
                )
            },
        ),

        (

            "System Flags",

            {

                "fields": (

                    "is_trending",

                    "is_verified",

                    "is_active",
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
    # BULK ACTIONS
    # =====================================================

    actions = [

        "mark_trending",

        "mark_verified",

        "activate_keywords",

        "deactivate_keywords",
    ]

    # =====================================================
    # TRENDING
    # =====================================================

    @admin.action(
        description="Mark selected keywords as trending"
    )
    def mark_trending(
        self,
        request,
        queryset,
    ):

        queryset.update(
            is_trending=True
        )

    # =====================================================
    # VERIFIED
    # =====================================================

    @admin.action(
        description="Mark selected keywords as verified"
    )
    def mark_verified(
        self,
        request,
        queryset,
    ):

        queryset.update(
            is_verified=True
        )

    # =====================================================
    # ACTIVATE
    # =====================================================

    @admin.action(
        description="Activate selected keywords"
    )
    def activate_keywords(
        self,
        request,
        queryset,
    ):

        queryset.update(
            is_active=True
        )

    # =====================================================
    # DEACTIVATE
    # =====================================================

    @admin.action(
        description="Deactivate selected keywords"
    )
    def deactivate_keywords(
        self,
        request,
        queryset,
    ):

        queryset.update(
            is_active=False
        )