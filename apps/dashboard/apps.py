from django.apps import AppConfig


class DashboardConfig(
    AppConfig
):

    default_auto_field = (
        "django.db.models.BigAutoField"
    )

    name = (
        "apps.dashboard"
    )

    verbose_name = (
        "AI Dashboard"
    )

    def ready(
        self
    ):

        try:

            from apps.dashboard.services.feature_service import (
                FeatureService
            )

            FeatureService.ensure_defaults()

        except Exception:

            # Prevent startup crash
            pass