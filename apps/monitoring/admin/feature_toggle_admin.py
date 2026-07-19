from django.contrib import admin
from django.utils.html import format_html

from apps.monitoring.models import (
    FeatureToggle,
)


@admin.register(FeatureToggle)
class FeatureToggleAdmin(
    admin.ModelAdmin
):

    list_display = (

        "name",

        "slug",

        "status_badge",

        "updated_at",
    )

    list_editable = ()

    search_fields = (

        "name",

        "slug",
    )

    list_filter = (

        "is_enabled",

        "updated_at",
    )

    # ==========================================
    # FIXED
    # ==========================================

    readonly_fields = ()

    ordering = (
        "name",
    )

    list_per_page = 25

    actions = [

        "enable_features",

        "disable_features",
    ]

    # ==========================================
    # STATUS BADGE
    # ==========================================

    def status_badge(
        self,
        obj,
    ):

        enabled = bool(
            obj.is_enabled
        )

        color = "#dc2626"

        label = "Disabled"

        if enabled:

            color = "#16a34a"

            label = "Enabled"

        return format_html(

            '<span style="'
            'background:{};'
            'color:white;'
            'padding:4px 10px;'
            'border-radius:12px;'
            'font-weight:600;'
            'font-size:12px;'
            '">'
            '{}'
            '</span>',

            color,

            label,
        )

    status_badge.short_description = (
        "Status"
    )

    # ==========================================
    # ENABLE ACTION
    # ==========================================

    def enable_features(
        self,
        request,
        queryset,
    ):

        updated = queryset.update(
            is_enabled=True
        )

        self.message_user(

            request,

            f"{updated} feature(s) enabled."
        )

    enable_features.short_description = (
        "Enable selected features"
    )

    # ==========================================
    # DISABLE ACTION
    # ==========================================

    def disable_features(
        self,
        request,
        queryset,
    ):

        updated = queryset.update(
            is_enabled=False
        )

        self.message_user(

            request,

            f"{updated} feature(s) disabled."
        )

    disable_features.short_description = (
        "Disable selected features"
    )