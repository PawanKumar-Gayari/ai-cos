"""
Publisher API serializers.
"""

from __future__ import annotations

from rest_framework import serializers


# =========================================================
# HEALTH SERIALIZER
# =========================================================

class HealthSerializer(
    serializers.Serializer
):

    success = serializers.BooleanField()

    status = serializers.CharField()

    service = serializers.CharField()

    message = serializers.CharField()


# =========================================================
# GENERATE ARTICLE REQUEST
# =========================================================

class GenerateArticleRequestSerializer(
    serializers.Serializer
):

    topic = serializers.CharField(

        max_length=500
    )

    language = serializers.CharField(

        required=False,

        default="en",
    )

    tone = serializers.CharField(

        required=False,

        default="seo",
    )

    keywords = serializers.ListField(

        child=serializers.CharField(),

        required=False,

        default=list,
    )

    publish = serializers.BooleanField(

        required=False,

        default=False,
    )


# =========================================================
# GENERATE ARTICLE RESPONSE
# =========================================================

class GenerateArticleResponseSerializer(
    serializers.Serializer
):

    success = serializers.BooleanField()

    title = serializers.CharField()

    content = serializers.CharField()

    meta_description = (
        serializers.CharField()
    )

    tags = serializers.ListField(

        child=serializers.CharField()
    )

    categories = serializers.ListField(

        child=serializers.CharField()
    )


# =========================================================
# PUBLISH ARTICLE REQUEST
# =========================================================

class PublishArticleRequestSerializer(
    serializers.Serializer
):

    article_id = serializers.IntegerField()

    publish = serializers.BooleanField(

        required=False,

        default=False,
    )


# =========================================================
# PUBLISH ARTICLE RESPONSE
# =========================================================

class PublishArticleResponseSerializer(
    serializers.Serializer
):

    success = serializers.BooleanField()

    tracker_id = serializers.IntegerField()

    article_id = serializers.IntegerField()

    wordpress_post_id = (
        serializers.CharField()
    )

    status = serializers.CharField()

    url = serializers.URLField()

    duration = serializers.FloatField()

    response = serializers.JSONField()


# =========================================================
# ERROR RESPONSE
# =========================================================

class ErrorResponseSerializer(
    serializers.Serializer
):

    success = serializers.BooleanField(
        default=False
    )

    error = serializers.CharField()

    details = serializers.JSONField(
        required=False
    )