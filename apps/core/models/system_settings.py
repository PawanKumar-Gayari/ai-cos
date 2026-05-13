from django.db import models


class SystemSettings(models.Model):

    enable_openai = models.BooleanField(
        default=True
    )

    enable_gemini = models.BooleanField(
        default=True
    )

    enable_ollama = models.BooleanField(
        default=True
    )

    enable_memory = models.BooleanField(
        default=True
    )

    enable_hot_memory = models.BooleanField(
        default=True
    )

    enable_semantic_memory = models.BooleanField(
        default=True
    )

    debug_logging = models.BooleanField(
        default=False
    )

    provider_timeout = models.IntegerField(
        default=120
    )

    max_retries = models.IntegerField(
        default=2
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:

        verbose_name = "System Settings"

        verbose_name_plural = (
            "System Settings"
        )

    def __str__(self):

        return "AI COS System Settings"