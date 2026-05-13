from django.contrib import admin

from apps.monitoring.models import (
    FeatureToggle,
)


@admin.register(FeatureToggle)
class FeatureToggleAdmin(admin.ModelAdmin):

    list_display = [
        "name",
        "slug",
        "is_enabled",
        "updated_at",
    ]

    list_editable = [
        "is_enabled",
    ]