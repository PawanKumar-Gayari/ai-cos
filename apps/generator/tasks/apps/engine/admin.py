from django.contrib import admin

from apps.engine.models import (
    Keyword,
    Article,
    GenerationLog,
)


@admin.register(Keyword)
class KeywordAdmin(admin.ModelAdmin):

    list_display = (

        "keyword",

        "intent",

        "difficulty",

        "volume",

        "created_at",
    )

    search_fields = (

        "keyword",
    )

    list_filter = (

        "intent",

        "difficulty",
    )


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):

    list_display = (

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
    )

    list_filter = (

        "ai_provider",

        "is_verified",

        "is_published",
    )

    readonly_fields = (

        "created_at",

        "updated_at",
    )


@admin.register(GenerationLog)
class GenerationLogAdmin(admin.ModelAdmin):

    list_display = (

        "article",

        "provider",

        "status",

        "response_time",

        "created_at",
    )

    list_filter = (

        "provider",

        "status",
    )

    readonly_fields = (

        "created_at",
    )