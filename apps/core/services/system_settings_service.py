from django.core.cache import cache

from apps.core.models import (
    SystemSettings,
)

from apps.dashboard.services.feature_service import (
    FeatureService,
)


class SystemSettingsService:

    CACHE_KEY = (
        "system_settings_cache"
    )

    CACHE_TIMEOUT = 60

    @classmethod
    def get_settings(
        cls
    ):

        cached = cache.get(
            cls.CACHE_KEY
        )

        if cached:

            return cached

        settings = (
            SystemSettings.objects.first()
        )

        if not settings:

            settings = (
                SystemSettings.objects.create()
            )

        # ==========================================
        # FEATURE FLAG OVERRIDES
        # ==========================================

        settings.enable_gemini = (
            FeatureService.is_enabled(
                "gemini_enabled",
                default=False,
            )
        )

        settings.enable_ollama = (
            FeatureService.is_enabled(
                "ollama_enabled",
                default=True,
            )
        )

        settings.enable_openai = (
            FeatureService.is_enabled(
                "openai_enabled",
                default=False,
            )
        )

        cache.set(

            cls.CACHE_KEY,

            settings,

            timeout=(
                cls.CACHE_TIMEOUT
            ),
        )

        return settings

    @classmethod
    def clear_cache(
        cls
    ):

        cache.delete(
            cls.CACHE_KEY
        )