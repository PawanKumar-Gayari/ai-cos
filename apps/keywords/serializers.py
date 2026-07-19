"""
Enterprise SEO Intelligence Serializers
---------------------------------------

Production-grade serializers for
SEO intelligence APIs.

Features:
- enterprise validation
- multilingual normalization
- semantic-safe keyword validation
- anti-spam filtering
- production-safe serializers
- scalable SEO architecture
"""

from __future__ import annotations

import re

from rest_framework import serializers

from apps.keywords.models import (
    KeywordAnalysis,
)


# =====================================================
# BASE VALIDATOR
# =====================================================

class BaseKeywordValidator:

    """
    Enterprise keyword validation mixin.
    """

    BLOCKED_PATTERNS = [

        "ignore previous instructions",

        "system prompt",

        "developer instructions",

        "<script",

        "</script>",

        "drop table",

        "rm -rf",

        "wget ",

        "curl ",

        "__import__",

        "exec(",
    ]

    MULTI_SPACE_PATTERN = re.compile(
        r"\s+"
    )

    SPECIAL_CHAR_PATTERN = re.compile(
        r"[^\w\s\u0900-\u097F\-]"
    )

    # =============================================
    # NORMALIZE TEXT
    # =============================================

    def normalize_text(
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

                    "Unsafe keyword detected."
                )

        return value

    # =============================================
    # VALIDATE KEYWORD
    # =============================================

    def validate_keyword_input(
        self,
        value,
    ):

        value = self.normalize_text(
            value
        )

        value = (
            self.validate_safe_text(
                value
            )
        )

        if len(value) < 2:

            raise serializers.ValidationError(

                "Keyword too short."
            )

        if len(value) > 255:

            raise serializers.ValidationError(

                "Keyword too long."
            )

        if len(value.split()) > 30:

            raise serializers.ValidationError(

                "Too many words."
            )

        special_chars = (

            self.SPECIAL_CHAR_PATTERN
            .findall(value)
        )

        if len(special_chars) > 20:

            raise serializers.ValidationError(

                "Too many invalid characters."
            )

        return value


# =====================================================
# SERP RESULT SERIALIZER
# =====================================================

class SERPResultSerializer(
    serializers.Serializer
):

    """
    SERP result serializer.
    """

    title = serializers.CharField()

    url = serializers.URLField()

    description = serializers.CharField()


# =====================================================
# ANALYZED PAGE SERIALIZER
# =====================================================

class AnalyzedPageSerializer(
    serializers.Serializer
):

    url = serializers.URLField()

    title = serializers.CharField()

    word_count = (
        serializers.IntegerField()
    )

    headings_count = (
        serializers.IntegerField()
    )

    faq_count = (
        serializers.IntegerField()
    )

    page_score = (
        serializers.IntegerField()
    )


# =====================================================
# DIFFICULTY SERIALIZER
# =====================================================

class DifficultySerializer(
    serializers.Serializer
):

    keyword = serializers.CharField()

    difficulty_score = (
        serializers.IntegerField()
    )

    competition_level = (
        serializers.CharField()
    )

    analyzed_pages = (
        AnalyzedPageSerializer(
            many=True
        )
    )


# =====================================================
# RECOMMENDATION SERIALIZER
# =====================================================

class RecommendationSerializer(
    serializers.Serializer
):

    keyword = serializers.CharField()

    difficulty_score = (
        serializers.IntegerField()
    )

    competition_level = (
        serializers.CharField()
    )

    recommended_word_count = (
        serializers.IntegerField()
    )

    recommended_headings = (
        serializers.ListField(
            child=serializers.CharField()
        )
    )

    recommended_faqs = (
        serializers.ListField(
            child=serializers.CharField()
        )
    )

    recommendations = (
        serializers.ListField(
            child=serializers.CharField()
        )
    )


# =====================================================
# ARTICLE STRUCTURE SERIALIZER
# =====================================================

class ArticleStructureSerializer(
    serializers.Serializer
):

    h1 = serializers.CharField()

    intro = serializers.CharField()

    h2_sections = (
        serializers.ListField(
            child=serializers.CharField()
        )
    )

    faq_section = (
        serializers.ListField(
            child=serializers.CharField()
        )
    )


# =====================================================
# OUTLINE SERIALIZER
# =====================================================

class OutlineSerializer(
    serializers.Serializer
):

    keyword = serializers.CharField()

    difficulty_score = (
        serializers.IntegerField()
    )

    competition_level = (
        serializers.CharField()
    )

    recommended_word_count = (
        serializers.IntegerField()
    )

    article_structure = (
        ArticleStructureSerializer()
    )


# =====================================================
# CLUSTER SERIALIZER
# =====================================================

class ClusterSerializer(
    serializers.Serializer
):

    total_keywords = (
        serializers.IntegerField()
    )

    total_clusters = (
        serializers.IntegerField()
    )

    clusters = (
        serializers.DictField(
            child=serializers.ListField(
                child=serializers.CharField()
            )
        )
    )


# =====================================================
# ANALYZE KEYWORD REQUEST
# =====================================================

class AnalyzeKeywordSerializer(

    BaseKeywordValidator,

    serializers.Serializer,
):

    """
    Enterprise keyword request validator.
    """

    keyword = serializers.CharField(

        max_length=255,

        required=True,

        allow_blank=False,

        trim_whitespace=True,
    )

    max_results = (
        serializers.IntegerField(

            required=False,

            default=10,

            min_value=1,

            max_value=50,
        )
    )

    # =============================================
    # VALIDATE KEYWORD
    # =============================================

    def validate_keyword(
        self,
        value,
    ):

        return self.validate_keyword_input(
            value
        )


# =====================================================
# EXPAND KEYWORD REQUEST
# =====================================================

class KeywordExpandSerializer(

    BaseKeywordValidator,

    serializers.Serializer,
):

    topic = serializers.CharField(

        max_length=255,

        required=True,

        allow_blank=False,

        trim_whitespace=True,
    )

    limit = serializers.IntegerField(

        required=False,

        default=10,

        min_value=1,

        max_value=100,
    )

    # =============================================
    # VALIDATE TOPIC
    # =============================================

    def validate_topic(
        self,
        value,
    ):

        return self.validate_keyword_input(
            value
        )


# =====================================================
# KEYWORD ANALYSIS SERIALIZER
# =====================================================

class KeywordAnalysisSerializer(
    serializers.ModelSerializer
):

    """
    Enterprise keyword analysis serializer.
    """

    class Meta:

        model = KeywordAnalysis

        fields = [

            "id",

            "keyword",

            "normalized_keyword",

            "language",

            "search_intent",

            "seo_difficulty",

            "search_volume",

            "keyword_score",

            "trend_score",

            "competition_score",

            "competition_level",

            "related_keywords",

            "semantic_keywords",

            "entities",

            "tags",

            "recommended_content_type",

            "target_audience",

            "recommended_word_count",

            "total_analyses",

            "is_trending",

            "is_active",

            "is_verified",

            "cache_key",

            "created_at",

            "updated_at",

            "last_analyzed_at",
        ]

        read_only_fields = [

            "id",

            "normalized_keyword",

            "cache_key",

            "created_at",

            "updated_at",

            "last_analyzed_at",
        ]


# =====================================================
# FULL PIPELINE RESPONSE SERIALIZER
# =====================================================

class KeywordPipelineResponseSerializer(
    serializers.Serializer
):

    """
    Enterprise SEO pipeline response serializer.
    """

    keyword = serializers.CharField()

    keyword_id = (
        serializers.IntegerField()
    )

    suggestions = (
        serializers.ListField(
            child=serializers.CharField()
        )
    )

    serp_results = (
        SERPResultSerializer(
            many=True
        )
    )

    difficulty = (
        DifficultySerializer()
    )

    recommendations = (
        RecommendationSerializer()
    )

    outline = (
        OutlineSerializer()
    )

    clusters = (
        ClusterSerializer()
    )

    semantic_keywords = (
        serializers.ListField(

            child=serializers.CharField(),

            required=False,
        )
    )

    search_intent = (
        serializers.CharField(
            required=False
        )
    )

    seo_score = (
        serializers.FloatField(
            required=False
        )
    )

    competition_level = (
        serializers.CharField(
            required=False
        )
    )