"""
Publisher app configuration.
"""

from __future__ import annotations

from django.apps import (
    AppConfig,
)


class PublisherConfig(
    AppConfig
):

    default_auto_field = (
        "django.db.models.BigAutoField"
    )

    name = (
        "apps.publisher"
    )

    label = (
        "publisher"
    )

    verbose_name = (
        "AI COS Publisher"
    )

    def ready(
        self,
    ):

        # =================================================
        # IMPORT SIGNALS / STARTUP LOGIC
        # =================================================

        try:

            import apps.publisher.signals  # noqa

        except ImportError:

            # Signals optional for now
            pass