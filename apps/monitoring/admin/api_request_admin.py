from django.contrib import admin

from apps.monitoring.models import (
    APIRequestLog,
)


@admin.register(APIRequestLog)
class APIRequestLogAdmin(admin.ModelAdmin):

    list_display = [
        "method",
        "path",
        "status_code",
        "execution_time",
        "created_at",
    ]

    search_fields = [
        "path",
        "request_id",
    ]

    list_filter = [
        "method",
        "status_code",
    ]