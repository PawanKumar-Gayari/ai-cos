from django.contrib import admin

from apps.monitoring.models import (
    ErrorLog,
)


@admin.register(ErrorLog)
class ErrorLogAdmin(admin.ModelAdmin):

    list_display = [
        "error_type",
        "severity",
        "created_at",
    ]

    search_fields = [
        "message",
        "path",
    ]