from django.db import models


class SystemFeature(models.Model):

    """
    Enterprise feature toggle model.
    """

    # =====================================================
    # FEATURE CATEGORIES
    # =====================================================

    CATEGORY_CHOICES = [

        ("ai", "AI Engine"),

        ("seo", "SEO System"),

        ("performance", "Performance"),

        ("monitoring", "Monitoring"),

        ("experimental", "Experimental"),
    ]

    # =====================================================
    # CORE FIELDS
    # =====================================================

    key = models.CharField(

        max_length=100,

        unique=True,
    )

    name = models.CharField(

        max_length=150,

        default="Feature",
    )

    description = models.TextField(

        blank=True,

        default="",
    )

    category = models.CharField(

        max_length=50,

        choices=CATEGORY_CHOICES,

        default="ai",
    )

    enabled = models.BooleanField(

        default=True,
    )

    # =====================================================
    # PERFORMANCE SETTINGS
    # =====================================================

    cpu_intensive = models.BooleanField(

        default=False,
    )

    experimental = models.BooleanField(

        default=False,
    )

    # =====================================================
    # METADATA
    # =====================================================

    created_at = models.DateTimeField(

        auto_now_add=True,
    )

    updated_at = models.DateTimeField(

        auto_now=True,
    )

    # =====================================================
    # MODEL META
    # =====================================================

    class Meta:

        ordering = [

            "category",

            "key",
        ]

        verbose_name = (
            "System Feature"
        )

        verbose_name_plural = (
            "System Features"
        )

    # =====================================================
    # STRING REPRESENTATION
    # =====================================================

    def __str__(self):

        status = (

            "ON"

            if self.enabled

            else "OFF"
        )

        return (
            f"{self.name} "
            f"[{self.key}] "
            f"({status})"
        )