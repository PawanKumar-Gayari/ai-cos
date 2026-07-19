from django.contrib import admin
from django.utils.html import format_html

from apps.monitoring.models import (
    APIRequestLog,
)


@admin.register(APIRequestLog)
class APIRequestLogAdmin(
    admin.ModelAdmin
):

    list_display = (

        "method_badge",

        "short_path",

        "status_badge",

        "formatted_execution_time",

        "request_id",

        "created_at",
    )

    search_fields = (

        "path",

        "request_id",
    )

    list_filter = (

        "method",

        "status_code",

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
    # METHOD BADGE
    # ==========================================

    def method_badge(
        self,
        obj,
    ):

        method = str(
            obj.method
        ).upper()

        color = "#6b7280"

        if method == "GET":

            color = "#2563eb"

        elif method == "POST":

            color = "#16a34a"

        elif method == "PUT":

            color = "#f59e0b"

        elif method == "DELETE":

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

            method,
        )

    method_badge.short_description = (
        "Method"
    )

    # ==========================================
    # STATUS BADGE
    # ==========================================

    def status_badge(
        self,
        obj,
    ):

        try:

            code = int(
                obj.status_code
            )

            color = "#6b7280"

            if 200 <= code < 300:

                color = "#16a34a"

            elif 300 <= code < 400:

                color = "#2563eb"

            elif 400 <= code < 500:

                color = "#f59e0b"

            elif code >= 500:

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

                code,
            )

        except Exception:

            return "-"

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

        if len(path) > 60:

            return (
                path[:60] + "..."
            )

        return path

    short_path.short_description = (
        "API Path"
    )