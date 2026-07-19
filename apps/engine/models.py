"""
Database models for AI COS engine.
"""

from django.db import models


class Keyword(models.Model):

    # =========================
    # BASIC INFO
    # =========================

    keyword = models.CharField(
        max_length=255,
        unique=True
    )

    intent = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    difficulty = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )

    volume = models.IntegerField(
        default=0
    )

    # =========================
    # TIMESTAMPS
    # =========================

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):

        return self.keyword


class Article(models.Model):

    # =========================
    # RELATIONS
    # =========================

    keyword = models.ForeignKey(
        Keyword,
        on_delete=models.CASCADE,
        related_name="articles"
    )

    # =========================
    # SEO DATA
    # =========================

    title = models.CharField(
        max_length=500
    )

    slug = models.SlugField(
        max_length=500,
        blank=True,
        null=True
    )

    meta_description = models.TextField(
        blank=True,
        null=True
    )

    # =========================
    # CONTENT
    # =========================

    content = models.TextField()

    faq = models.TextField(
        blank=True,
        null=True
    )

    conclusion = models.TextField(
        blank=True,
        null=True
    )

    # =========================
    # AI + SEO
    # =========================

    seo_score = models.IntegerField(
        default=0
    )

    ai_provider = models.CharField(
        max_length=100,
        default="AI Router"
    )

    # =========================
    # REWRITE SYSTEM
    # =========================

    rewrite_score = models.IntegerField(
        default=0
    )

    rewrite_quality_status = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )

    rewritten = models.BooleanField(
        default=False
    )

    # =========================
    # STATUS
    # =========================

    is_verified = models.BooleanField(
        default=False
    )

    is_published = models.BooleanField(
        default=False
    )

    published_url = models.URLField(
        blank=True,
        null=True
    )

    # =========================
    # TIMESTAMPS
    # =========================

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):

        return self.title


class GenerationLog(models.Model):

    # =========================
    # RELATIONS
    # =========================

    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name="logs"
    )

    # =========================
    # LOG DATA
    # =========================

    provider = models.CharField(
        max_length=100
    )

    status = models.CharField(
        max_length=100
    )

    response_time = models.FloatField(
        default=0
    )

    error_message = models.TextField(
        blank=True,
        null=True
    )

    # =========================
    # TIMESTAMP
    # =========================

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return (
            f"{self.provider} - {self.status}"
        )