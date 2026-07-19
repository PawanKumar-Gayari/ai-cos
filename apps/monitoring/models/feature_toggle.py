from django.db import models


class FeatureToggle(
    models.Model
):

    # ==========================================
    # FEATURE INFO
    # ==========================================

    name = models.CharField(
        max_length=255
    )

    slug = models.SlugField(
        unique=True
    )

    description = models.TextField(

        blank=True,

        null=True,
    )

    # ==========================================
    # STATUS
    # ==========================================

    is_enabled = models.BooleanField(
        default=True
    )

    environment = models.CharField(

        max_length=50,

        default="production",
    )

    # ==========================================
    # CONTROL
    # ==========================================

    updated_by = models.CharField(

        max_length=255,

        blank=True,

        null=True,
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

    class Meta:

        ordering = [
            "name"
        ]

        verbose_name = (
            "Feature Toggle"
        )

        verbose_name_plural = (
            "Feature Toggles"
        )

    def __str__(
        self
    ):

        return (

            f"{self.name} | "

            f"{'Enabled' if self.is_enabled else 'Disabled'}"
        )