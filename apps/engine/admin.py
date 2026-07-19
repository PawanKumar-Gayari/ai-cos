"""
Admin configuration for AI COS engine.
"""

from django.contrib import admin

from apps.engine.models import (
    Article,
    GenerationLog,
    Keyword,
)


# ==================================================
# KEYWORD ADMIN
# ==================================================

@admin.register(Keyword)
class KeywordAdmin(admin.ModelAdmin):

    list_display = (

        "id",

        "keyword",

        "intent",

        "difficulty",

        "volume",

        "created_at",
    )

    search_fields = (

        "keyword",

        "intent",
    )

    list_filter = (

        "intent",

        "difficulty",
    )

    ordering = (
        "-created_at",
    )

    readonly_fields = (

        "created_at",

        "updated_at",
    )


# ==================================================
# ARTICLE ADMIN
# ==================================================

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):

    list_display = (

        "id",

        "title",

        "keyword",

        "seo_score",

        "ai_provider",

        "is_verified",

        "is_published",

        "created_at",
    )

    search_fields = (

        "title",

        "content",

        "meta_description",

        "slug",
    )

    list_filter = (

        "is_verified",

        "is_published",

        "ai_provider",
    )

    ordering = (
        "-created_at",
    )

    readonly_fields = (

        "created_at",

        "updated_at",
    )

    fieldsets = (

        (

            "SEO Information",

            {

                "fields": (

                    "keyword",

                    "title",

                    "slug",

                    "meta_description",

                    "seo_score",
                )
            },
        ),

        (

            "Content",

            {

                "fields": (

                    "content",

                    "faq",

                    "conclusion",
                )
            },
        ),

        (

            "AI Information",

            {

                "fields": (

                    "ai_provider",
                )
            },
        ),

        (

            "Publishing",

            {

                "fields": (

                    "is_verified",

                    "is_published",

                    "published_url",
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


# ==================================================
# GENERATION LOG ADMIN
# ==================================================

@admin.register(GenerationLog)
class GenerationLogAdmin(admin.ModelAdmin):

    list_display = (

        "id",

        "article",

        "provider",

        "status",

        "response_time",

        "created_at",
    )

    search_fields = (

        "provider",

        "status",
    )

    list_filter = (

        "provider",

        "status",
    )

    ordering = (
        "-created_at",
    )

    readonly_fields = (

        "created_at",
    )