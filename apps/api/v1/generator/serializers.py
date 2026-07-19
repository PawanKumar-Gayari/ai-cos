"""
Enterprise Generator API Serializers
------------------------------------

Production-grade API validation layer.

Features:
- secure validation
- keyword normalization
- prompt injection protection
- payload sanitization
- multilingual support
- SEO-safe limits
- production-safe architecture
"""

from __future__ import annotations

import re

from rest_framework import serializers


class BaseGeneratorSerializer(
    serializers.Serializer
):

    """
    Enterprise validation serializer.
    """

    BLOCKED_PATTERNS = [

        "ignore previous instructions",

        "system prompt",

        "developer instructions",

        "reveal prompt",

        "bypass security",

        "<script",

        "</script>",

        "drop table",

        "rm -rf",

        "sudo ",

        "wget ",

        "curl ",

        "exec(",

        "__import__",
    ]

    MULTI_SPACE_PATTERN = re.compile(
        r"\s+"
    )

    # =============================================
    # CLEAN TEXT
    # =============================================

    def clean_text(
        self,
        value,
    ):

        value = str(
            value
        ).strip()

        value = (

            self.MULTI_SPACE_PATTERN
            .sub(

                " ",

                value,
            )
        )

        return value

    # =============================================
    # SAFE TEXT
    # =============================================

    def validate_safe_text(
        self,
        value,
    ):

        lowered = value.lower()

        for pattern in (
            self.BLOCKED_PATTERNS
        ):

            if pattern in lowered:

                raise serializers.ValidationError(

                    "Unsafe content detected."
                )

        return value

    # =============================================
    # VALIDATE QUERY
    # =============================================

    def validate_query_like(
        self,
        value,
    ):

        value = self.clean_text(
            value
        )

        value = (
            self.validate_safe_text(
                value
            )
        )

        if len(value) < 3:

            raise serializers.ValidationError(

                "Query too short."
            )

        if len(value.split()) > 100:

            raise serializers.ValidationError(

                "Too many words."
            )

        return value


# =====================================================
# ARTICLE SERIALIZER
# =====================================================

class GenerateArticleSerializer(
    BaseGeneratorSerializer
):

    query = serializers.CharField(

        max_length=1000,

        trim_whitespace=True,
    )

    session_id = serializers.CharField(

        required=False,

        allow_blank=True,

        max_length=255,
    )

    # =============================================
    # VALIDATE QUERY
    # =============================================

    def validate_query(
        self,
        value,
    ):

        return self.validate_query_like(
            value
        )


# =====================================================
# OUTLINE SERIALIZER
# =====================================================

class GenerateOutlineSerializer(
    BaseGeneratorSerializer
):

    topic = serializers.CharField(

        max_length=1000,

        trim_whitespace=True,
    )

    session_id = serializers.CharField(

        required=False,

        allow_blank=True,

        max_length=255,
    )

    # =============================================
    # VALIDATE TOPIC
    # =============================================

    def validate_topic(
        self,
        value,
    ):

        return self.validate_query_like(
            value
        )


# =====================================================
# KEYWORD SERIALIZER
# =====================================================

class GenerateKeywordsSerializer(
    BaseGeneratorSerializer
):

    topic = serializers.CharField(

        max_length=1000,

        trim_whitespace=True,
    )

    session_id = serializers.CharField(

        required=False,

        allow_blank=True,

        max_length=255,
    )

    # =============================================
    # VALIDATE TOPIC
    # =============================================

    def validate_topic(
        self,
        value,
    ):

        return self.validate_query_like(
            value
        )


# =====================================================
# TASK RESPONSE
# =====================================================

class TaskQueuedSerializer(
    serializers.Serializer
):

    success = serializers.BooleanField()

    task_id = serializers.CharField()

    status = serializers.CharField()

    provider = serializers.CharField(
        required=False
    )

    seo_score = serializers.FloatField(
        required=False
    )


# =====================================================
# ERROR RESPONSE
# =====================================================

class ErrorSerializer(
    serializers.Serializer
):

    success = serializers.BooleanField(
        default=False
    )

    error = serializers.CharField()

    details = serializers.DictField(
        required=False
    )