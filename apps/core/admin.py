from django.contrib import admin

from apps.core.models.system_settings import (
    SystemSettings,
)


@admin.register(SystemSettings)
class SystemSettingsAdmin(admin.ModelAdmin):

    list_display = (
        "enable_openai",
        "enable_gemini",
        "enable_ollama",
        "enable_memory",
        "provider_timeout",
        "max_retries",
        "updated_at",
    )