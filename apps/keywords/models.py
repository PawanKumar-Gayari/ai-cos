"""
Production SEO Intelligence Models v1.1
---------------------------------------

Enterprise-grade keyword intelligence models.

Version: 1.1

Features:
- async keyword jobs
- enterprise SEO storage
- semantic-ready architecture
- clustering-ready structure
- competitor intelligence storage
- scalable dashboard backend
- Celery-ready workflow
- audit-safe timestamps
- OCI optimized
- production-safe
"""

from __future__ import annotations

import hashlib
import logging
import re

from django.core.validators import (

    MaxValueValidator,

    MinLengthValidator,

    MinValueValidator,
)

from django.db import models

from django.utils import timezone

from apps.keywords.constants import (

    DIFFICULTY_HIGH,

    DIFFICULTY_LOW,

    DIFFICULTY_MEDIUM,

    DIFFICULTY_VERY_HIGH,

    INTENT_COMMERCIAL,

    INTENT_COMPARISON,

    INTENT_INFORMATIONAL,

    INTENT_LOCAL,

    INTENT_NAVIGATIONAL,

    INTENT_TRANSACTIONAL,

    MAX_KEYWORD_LENGTH,

    MIN_KEYWORD_LENGTH,
)


logger = logging.getLogger(
    __name__
)


# =========================================================
# QUERY MANAGER
# =========================================================


class KeywordAnalysisManager(
    models.Manager
):

    def active(
        self,
    ):

        return self.filter(
            is_active=True
        )

    def trending(
        self,
    ):

        return self.filter(
            is_trending=True
        )

    def verified(
        self,
    ):

        return self.filter(
            is_verified=True
        )

    def top_keywords(
        self,
    ):

        return self.order_by(
            "-keyword_score"
        )

    def informational(
        self,
    ):

        return self.filter(

            search_intent=
            INTENT_INFORMATIONAL
        )

    def commercial(
        self,
    ):

        return self.filter(

            search_intent=
            INTENT_COMMERCIAL
        )

    def transactional(
        self,
    ):

        return self.filter(

            search_intent=
            INTENT_TRANSACTIONAL
        )

    def local_keywords(
        self,
    ):

        return self.filter(

            search_intent=
            INTENT_LOCAL
        )


# =========================================================
# KEYWORD RESEARCH JOB
# =========================================================


class KeywordResearchJob(
    models.Model
):

    """
    Async SEO research job.
    """

    STATUS_PENDING = "pending"

    STATUS_RUNNING = "running"

    STATUS_COMPLETED = "completed"

    STATUS_FAILED = "failed"

    STATUS_CHOICES = [

        (
            STATUS_PENDING,
            "Pending",
        ),

        (
            STATUS_RUNNING,
            "Running",
        ),

        (
            STATUS_COMPLETED,
            "Completed",
        ),

        (
            STATUS_FAILED,
            "Failed",
        ),
    ]

    keyword = models.CharField(

        max_length=255,

        db_index=True,
    )

    normalized_keyword = models.CharField(

        max_length=255,

        blank=True,

        db_index=True,
    )

    status = models.CharField(

        max_length=50,

        choices=STATUS_CHOICES,

        default=STATUS_PENDING,

        db_index=True,
    )

    progress = models.PositiveIntegerField(

        default=0,

        validators=[

            MinValueValidator(0),

            MaxValueValidator(100),
        ],
    )

    result = models.JSONField(

        default=dict,

        blank=True,
    )

    error_message = models.TextField(

        blank=True,

        null=True,
    )

    celery_task_id = models.CharField(

        max_length=255,

        blank=True,

        null=True,
    )

    started_at = models.DateTimeField(

        blank=True,

        null=True,
    )

    completed_at = models.DateTimeField(

        blank=True,

        null=True,
    )

    created_at = models.DateTimeField(

        auto_now_add=True,

        db_index=True,
    )

    updated_at = models.DateTimeField(

        auto_now=True,
    )

    class Meta:

        ordering = [
            "-created_at"
        ]

        verbose_name = (
            "Keyword Research Job"
        )

        verbose_name_plural = (
            "Keyword Research Jobs"
        )

        indexes = [

            models.Index(
                fields=[
                    "status"
                ]
            ),

            models.Index(
                fields=[
                    "created_at"
                ]
            ),

            models.Index(
                fields=[
                    "normalized_keyword"
                ]
            ),
        ]

    # =====================================================
    # NORMALIZE
    # =====================================================

    @staticmethod
    def normalize_text(
        text: str,
    ) -> str:

        text = (
            text
            .strip()
            .lower()
        )

        text = re.sub(

            r"\s+",

            " ",

            text,
        )

        return text

    # =====================================================
    # SAVE
    # =====================================================

    def save(
        self,
        *args,
        **kwargs,
    ):

        if self.keyword:

            self.normalized_keyword = (

                self.normalize_text(
                    self.keyword
                )
            )

        super().save(
            *args,
            **kwargs,
        )

    # =====================================================
    # STRING
    # =====================================================

    def __str__(
        self,
    ):

        return (

            f"{self.keyword} | "
            f"{self.status}"
        )


# =========================================================
# MAIN MODEL
# =========================================================


class KeywordAnalysis(
    models.Model
):

    """
    Central SEO intelligence model.
    """

    objects = (
        KeywordAnalysisManager()
    )

    # =====================================================
    # SEARCH INTENTS
    # =====================================================

    INTENT_CHOICES = [

        (
            INTENT_INFORMATIONAL,
            "Informational",
        ),

        (
            INTENT_COMMERCIAL,
            "Commercial",
        ),

        (
            INTENT_TRANSACTIONAL,
            "Transactional",
        ),

        (
            INTENT_NAVIGATIONAL,
            "Navigational",
        ),

        (
            INTENT_COMPARISON,
            "Comparison",
        ),

        (
            INTENT_LOCAL,
            "Local",
        ),
    ]

    # =====================================================
    # DIFFICULTY LEVELS
    # =====================================================

    DIFFICULTY_CHOICES = [

        (
            DIFFICULTY_LOW,
            "Low",
        ),

        (
            DIFFICULTY_MEDIUM,
            "Medium",
        ),

        (
            DIFFICULTY_HIGH,
            "High",
        ),

        (
            DIFFICULTY_VERY_HIGH,
            "Very High",
        ),
    ]

    # =====================================================
    # BASIC DATA
    # =====================================================

    keyword = models.CharField(

        max_length=MAX_KEYWORD_LENGTH,

        unique=True,

        db_index=True,

        validators=[

            MinLengthValidator(
                MIN_KEYWORD_LENGTH
            ),
        ],
    )

    normalized_keyword = models.CharField(

        max_length=MAX_KEYWORD_LENGTH,

        editable=False,

        db_index=True,
    )

    cache_key = models.CharField(

        max_length=64,

        blank=True,

        db_index=True,
    )

    language = models.CharField(

        max_length=20,

        default="english",

        db_index=True,
    )

    search_intent = models.CharField(

        max_length=50,

        choices=INTENT_CHOICES,

        default=INTENT_INFORMATIONAL,

        db_index=True,
    )

    # =====================================================
    # SEO METRICS
    # =====================================================

    seo_difficulty = models.CharField(

        max_length=20,

        choices=DIFFICULTY_CHOICES,

        default=DIFFICULTY_MEDIUM,

        db_index=True,
    )

    search_volume = models.PositiveIntegerField(

        default=0,

        validators=[
            MinValueValidator(0),
        ],
    )

    keyword_score = models.FloatField(

        default=0.0,

        validators=[

            MinValueValidator(0),

            MaxValueValidator(100),
        ],

        db_index=True,
    )

    trend_score = models.FloatField(

        default=0.0,
    )

    competition_score = models.FloatField(

        default=0.0,
    )

    competition_level = models.CharField(

        max_length=50,

        blank=True,

        null=True,
    )

    # =====================================================
    # SEO INTELLIGENCE
    # =====================================================

    related_keywords = models.JSONField(

        default=list,

        blank=True,
    )

    semantic_keywords = models.JSONField(

        default=list,

        blank=True,
    )

    entities = models.JSONField(

        default=list,

        blank=True,
    )

    people_also_ask = models.JSONField(

        default=list,

        blank=True,
    )

    related_searches = models.JSONField(

        default=list,

        blank=True,
    )

    competitor_data = models.JSONField(

        default=list,

        blank=True,
    )

    recommendation_data = models.JSONField(

        default=dict,

        blank=True,
    )

    outline_data = models.JSONField(

        default=dict,

        blank=True,
    )

    cluster_data = models.JSONField(

        default=dict,

        blank=True,
    )

    tags = models.JSONField(

        default=list,

        blank=True,
    )

    # =====================================================
    # CONTENT STRATEGY
    # =====================================================

    recommended_content_type = (

        models.CharField(

            max_length=100,

            blank=True,

            null=True,
        )
    )

    target_audience = (

        models.CharField(

            max_length=255,

            blank=True,

            null=True,
        )
    )

    recommended_word_count = (

        models.PositiveIntegerField(
            default=1000
        )
    )

    # =====================================================
    # FLAGS
    # =====================================================

    is_trending = models.BooleanField(

        default=False,

        db_index=True,
    )

    is_active = models.BooleanField(

        default=True,

        db_index=True,
    )

    is_verified = models.BooleanField(

        default=False,

        db_index=True,
    )

    # =====================================================
    # ANALYTICS
    # =====================================================

    total_analyses = (

        models.PositiveIntegerField(
            default=0
        )
    )

    last_analyzed_at = (

        models.DateTimeField(

            blank=True,

            null=True,
        )
    )

    # =====================================================
    # TIMESTAMPS
    # =====================================================

    created_at = models.DateTimeField(

        auto_now_add=True,

        db_index=True,
    )

    updated_at = models.DateTimeField(

        auto_now=True,

        db_index=True,
    )

    # =====================================================
    # META
    # =====================================================

    class Meta:

        ordering = [
            "-updated_at"
        ]

        get_latest_by = (
            "updated_at"
        )

        verbose_name = (
            "Keyword Analysis"
        )

        verbose_name_plural = (
            "Keyword Analyses"
        )

    # =====================================================
    # NORMALIZE TEXT
    # =====================================================

    @staticmethod
    def normalize_text(
        text: str,
    ) -> str:

        text = (
            text
            .strip()
            .lower()
        )

        text = re.sub(

            r"\s+",

            " ",

            text,
        )

        return text

    # =====================================================
    # CACHE KEY
    # =====================================================

    @staticmethod
    def generate_cache_key(
        keyword: str,
    ) -> str:

        return hashlib.md5(

            keyword.encode()
        ).hexdigest()

    # =====================================================
    # SAVE
    # =====================================================

    def save(
        self,
        *args,
        **kwargs,
    ):

        if self.keyword:

            self.normalized_keyword = (

                self.normalize_text(
                    self.keyword
                )
            )

            self.cache_key = (

                self.generate_cache_key(

                    self.normalized_keyword
                )
            )

        self.total_analyses += 1

        self.last_analyzed_at = (
            timezone.now()
        )

        super().save(
            *args,
            **kwargs,
        )

    # =====================================================
    # STRING
    # =====================================================

    def __str__(
        self,
    ) -> str:

        return (

            f"{self.keyword} | "

            f"{self.search_intent} | "

            f"SEO {self.keyword_score}"
        )