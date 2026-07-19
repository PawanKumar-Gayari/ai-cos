from django.contrib import admin
from django.utils.html import format_html

from apps.monitoring.models import (
    ErrorLog,
)


@admin.register(ErrorLog)
class ErrorLogAdmin(
    admin.ModelAdmin
):

    list_display = (

        "error_type",

        "severity_badge",

        "short_message",

        "short_path",

        "created_at",
    )

    search_fields = (

        "message",

        "path",

        "error_type",
    )

    list_filter = (

        "severity",

        "error_type",

        "created_at",
    )

    readonly_fields = (

        "created_at",
    )

    ordering = (
        "-created_at",
    )

    list_per_page = 25

    # ==========================================
    # SEVERITY BADGE
    # ==========================================

    def severity_badge(
        self,
        obj,
    ):

        severity = str(
            obj.severity
        ).lower()

        color = "#6b7280"

        if severity in [
            "low",
            "info",
        ]:

            color = "#16a34a"

        elif severity in [
            "medium",
            "warning",
        ]:

            color = "#f59e0b"

        elif severity in [
            "high",
            "critical",
            "error",
        ]:

            color = "#dc2626"

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

            obj.severity,
        )

    severity_badge.short_description = (
        "Severity"
    )

    # ==========================================
    # SHORT MESSAGE
    # ==========================================

    def short_message(
        self,
        obj,
    ):

        message = str(
            obj.message
        )

        if len(message) > 80:

            return (
                message[:80] + "..."
            )

        return message

    short_message.short_description = (
        "Message"
    )

    # ==========================================
    # SHORT PATH
    # ==========================================

    def short_path(
        self,
        obj,
    ):

        path = str(
            obj.path
        )

        if len(path) > 50:

            return (
                path[:50] + "..."
            )

        return path

    short_path.short_description = (
        "Path"
    )