"""
Generator system models.
"""

from django.db import models


class GeneratorConfig(
    models.Model
):

    # ==========================================
    # PROVIDERS
    # ==========================================

    PROVIDER_CHOICES = [

        ("openai", "OpenAI"),

        ("gemini", "Gemini"),

        ("ollama", "Ollama"),
    ]

    # ==========================================
    # CONTENT TYPES
    # ==========================================

    CONTENT_TYPE_CHOICES = [

        ("article", "Article"),

        ("blog", "Blog"),

        ("seo", "SEO Content"),

        ("rewrite", "Rewrite"),

        ("summary", "Summary"),

        ("social", "Social Post"),
    ]

    # ==========================================
    # WRITING TONES
    # ==========================================

    TONE_CHOICES = [

        ("professional", "Professional"),

        ("casual", "Casual"),

        ("humanized", "Humanized"),

        ("technical", "Technical"),

        ("marketing", "Marketing"),
    ]

    # ==========================================
    # BASIC CONFIG
    # ==========================================

    name = models.CharField(

        max_length=100,

        unique=True,
    )

    active_provider = models.CharField(

        max_length=50,

        choices=PROVIDER_CHOICES,

        default="gemini",
    )

    default_model = models.CharField(

        max_length=100,

        default="gemini-2.0-flash",
    )

    # ==========================================
    # GENERATION SETTINGS
    # ==========================================

    content_type = models.CharField(

        max_length=50,

        choices=CONTENT_TYPE_CHOICES,

        default="article",
    )

    tone = models.CharField(

        max_length=50,

        choices=TONE_CHOICES,

        default="humanized",
    )

    target_word_count = models.IntegerField(

        default=2000
    )

    temperature = models.FloatField(

        default=0.7
    )

    max_tokens = models.IntegerField(

        default=2000
    )

    max_rewrite_loops = models.IntegerField(

        default=3
    )

    minimum_quality_score = (

        models.IntegerField(

            default=80
        )
    )

    # ==========================================
    # AI FEATURES
    # ==========================================

    enable_memory = models.BooleanField(

        default=True
    )

    enable_scoring = models.BooleanField(

        default=True
    )

    enable_cleaning = models.BooleanField(

        default=True
    )

    enable_fallback = models.BooleanField(

        default=True
    )

    enable_seo = models.BooleanField(

        default=True
    )

    # ==========================================
    # PROMPTS
    # ==========================================

    system_prompt = models.TextField(

        blank=True,

        null=True,
    )

    prompt_template = models.TextField(

        blank=True,

        null=True,
    )

    # ==========================================
    # STATUS
    # ==========================================

    is_active = models.BooleanField(

        default=True
    )

    # ==========================================
    # TIMESTAMPS
    # ==========================================

    created_at = models.DateTimeField(

        auto_now_add=True
    )

    updated_at = models.DateTimeField(

        auto_now=True
    )

    # ==========================================
    # META
    # ==========================================

    class Meta:

        verbose_name = (
            "Generator Config"
        )

        verbose_name_plural = (
            "Generator Configs"
        )

        ordering = [
            "-updated_at"
        ]

    # ==========================================
    # STRING
    # ==========================================

    def __str__(self):

        return (

            f"{self.name} | "
            f"{self.active_provider}"
        )