from django.contrib import admin

from apps.monitoring.models import (
    EngineExecution,
)


@admin.register(EngineExecution)
class EngineExecutionAdmin(admin.ModelAdmin):

    list_display = [
        "engine_name",
        "keyword",
        "execution_time",
        "status",
        "created_at",
    ]

    search_fields = [
        "engine_name",
        "keyword",
    ]