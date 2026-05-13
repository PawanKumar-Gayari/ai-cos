from django.contrib import admin

from apps.history.models import (
    GenerationHistory
)


@admin.register(
    GenerationHistory
)
class GenerationHistoryAdmin(
    admin.ModelAdmin
):

    list_display = (

        "task_type",

        "status",

        "provider",

        "created_at",
    )

    search_fields = (

        "query",

        "task_id",
    )

    list_filter = (

        "task_type",

        "status",
    )