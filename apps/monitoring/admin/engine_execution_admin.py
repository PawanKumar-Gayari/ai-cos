from django.contrib import admin
from django.utils.html import format_html

from apps.monitoring.models import (
    EngineExecution,
)


@admin.register(EngineExecution)
class EngineExecutionAdmin(
    admin.ModelAdmin
):

    list_display = (

        "engine_name",

        "keyword",

        "status_badge",

        "formatted_execution_time",

        "created_at",
    )

    list_filter = (

        "status",

        "engine_name",

        "created_at",
    )

    search_fields = (

        "engine_name",

        "keyword",
    )

    readonly_fields = (

        "created_at",
    )

    ordering = (
        "-created_at",
    )

    list_per_page = 25

    # ==========================================
    # STATUS BADGE
    # ==========================================

    def status_badge(
        self,
        obj,
    ):

        status = (
            str(obj.status)
            .lower()
        )

        color = "#6b7280"

        if status in [
            "success",
            "completed",
            "healthy",
        ]:

            color = "#16a34a"

        elif status in [
            "failed",
            "error",
        ]:

            color = "#dc2626"

        elif status in [
            "processing",
            "running",
            "pending",
        ]:

            color = "#f59e0b"

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

            obj.status,
        )

    status_badge.short_description = (
        "Status"
    )

    # ==========================================
    # EXECUTION TIME
    # ==========================================

    def formatted_execution_time(
        self,
        obj,
    ):

        try:

            execution_time = float(
                obj.execution_time
            )

            color = "#16a34a"

            if execution_time > 5:

                color = "#dc2626"

            elif execution_time > 2:

                color = "#f59e0b"

            return format_html(

                '<span style="'
                'color:{};'
                'font-weight:600;'
                '">'
                '{} sec'
                '</span>',

                color,

                round(
                    execution_time,
                    2,
                ),
            )

        except Exception:

            return "-"

    formatted_execution_time.short_description = (
        "Execution Time"
    )