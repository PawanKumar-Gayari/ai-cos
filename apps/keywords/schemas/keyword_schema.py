"""
SEO Intelligence Engine Schemas
-------------------------------

Production-ready request/response schemas.

Features:
- strict validation
- payload protection
- keyword sanitization
- secure defaults
- type safety
"""

from __future__ import annotations

import re

from rest_framework import serializers

from apps.keywords.constants import (
    BLOCKED_KEYWORDS,
    MAX_INPUT_PAYLOAD_SIZE,
    MAX_KEYWORD_LENGTH,
    MAX_KEYWORD_WORDS,
    MIN_KEYWORD_LENGTH,
)


# =========================================================
# BASE VALIDATION MIXIN
# =========================================================


class KeywordValidationMixin:
    """
    Shared secure keyword validation logic.
    """

    SUSPICIOUS_PATTERN = re.compile(
        r"[<>;$`{}[\]\\]"
    )

    MULTI_SPACE_PATTERN = re.compile(
        r"\s+"
    )

    def validate_keyword_text(
        self,
        value: str,
    ) -> str:

        """
        Validate and sanitize keyword/topic safely.
        """

        if not isinstance(
            value,
            str,
        ):
            raise serializers.ValidationError(
                "Input must be string."
            )

        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "Input cannot be empty."
            )

        if (
            len(value)
            > MAX_INPUT_PAYLOAD_SIZE
        ):
            raise serializers.ValidationError(
                "Input payload too large."
            )

        value = (
            self.MULTI_SPACE_PATTERN.sub(
                " ",
                value,
            )
        )

        normalized = value.lower()

        if normalized in BLOCKED_KEYWORDS:
            raise serializers.ValidationError(
                "Blocked keyword detected."
            )

        if (
            len(value)
            < MIN_KEYWORD_LENGTH
        ):
            raise serializers.ValidationError(
                "Keyword too short."
            )

        if (
            len(value)
            > MAX_KEYWORD_LENGTH
        ):
            raise serializers.ValidationError(
                "Keyword too long."
            )

        if (
            len(value.split())
            > MAX_KEYWORD_WORDS
        ):
            raise serializers.ValidationError(
                "Too many keyword words."
            )

        if self.SUSPICIOUS_PATTERN.search(
            value
        ):
            raise serializers.ValidationError(
                "Suspicious input detected."
            )

        return value


# =========================================================
# ANALYZE KEYWORD SCHEMA
# =========================================================


class KeywordAnalyzeSerializer(
    serializers.Serializer,
    KeywordValidationMixin,
):
    """
    Keyword analysis request schema.
    """

    keyword = serializers.CharField(
        required=True,
        trim_whitespace=True,
        max_length=MAX_KEYWORD_LENGTH,
    )

    def validate_keyword(
        self,
        value: str,
    ) -> str:

        return self.validate_keyword_text(
            value
        )


# =========================================================
# EXPAND KEYWORD SCHEMA
# =========================================================


class KeywordExpandSerializer(
    serializers.Serializer,
    KeywordValidationMixin,
):
    """
    Keyword expansion request schema.
    """

    topic = serializers.CharField(
        required=True,
        trim_whitespace=True,
        max_length=MAX_KEYWORD_LENGTH,
    )

    limit = serializers.IntegerField(
        required=False,
        default=10,
        min_value=1,
        max_value=50,
    )

    def validate_topic(
        self,
        value: str,
    ) -> str:

        return self.validate_keyword_text(
            value
        )


# =========================================================
# SEO ANALYSIS RESPONSE SCHEMA
# =========================================================


class KeywordResultSerializer(
    serializers.Serializer,
):
    """
    Standard keyword analysis response schema.
    """

    keyword = serializers.CharField()

    language = serializers.CharField()

    intent = serializers.CharField()

    difficulty = serializers.CharField()

    volume = serializers.IntegerField()

    score = serializers.FloatField()


# =========================================================
# HEALTH RESPONSE SCHEMA
# =========================================================


class KeywordHealthSerializer(
    serializers.Serializer,
):
    """
    Health check response schema.
    """

    success = serializers.BooleanField()

    service = serializers.CharField()

    status = serializers.CharField()

    version = serializers.CharField()