"""
Article serializers for API responses.
"""

from rest_framework import serializers

from apps.engine.models import (
    Article,
    GenerationLog,
    Keyword,
)


# ==================================================
# KEYWORD SERIALIZER
# ==================================================

class KeywordSerializer(
    serializers.ModelSerializer
):

    class Meta:

        model = Keyword

        fields = [

            "id",

            "keyword",

            "intent",

            "difficulty",

            "volume",

            "created_at",
        ]


# ==================================================
# ARTICLE SERIALIZER
# ==================================================

class ArticleSerializer(
    serializers.ModelSerializer
):

    keyword = KeywordSerializer(
        read_only=True
    )

    class Meta:

        model = Article

        fields = [

            "id",

            "keyword",

            "title",

            "slug",

            "meta_description",

            "content",

            "faq",

            "conclusion",

            "seo_score",

            "ai_provider",

            "is_verified",

            "is_published",

            "published_url",

            "created_at",

            "updated_at",
        ]


# ==================================================
# GENERATION LOG SERIALIZER
# ==================================================

class GenerationLogSerializer(
    serializers.ModelSerializer
):

    article = ArticleSerializer(
        read_only=True
    )

    class Meta:

        model = GenerationLog

        fields = [

            "id",

            "article",

            "provider",

            "status",

            "response_time",

            "error_message",

            "created_at",
        ]