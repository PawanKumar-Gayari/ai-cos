from django.contrib import admin
from django.utils.html import format_html

from apps.decision_engine.models import (
    DecisionLog,
)


@admin.register(DecisionLog)
class DecisionLogAdmin(
    admin.ModelAdmin
):

    list_display = (

        "keyword",

        "provider",

        "seo_score",

        "publish_score",

        "status_badge",

        "created_at",
    )

    search_fields = (

        "keyword",

        "provider",
    )

    list_filter = (

        "provider",

        "status",

        "should_generate",

        "rewrite_required",
    )

    readonly_fields = (

        "created_at",

        "updated_at",
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

        success = (
            obj.status == "success"
        )

        color = "#dc2626"

        label = "Failed"

        if success:

            color = "#16a34a"

            label = "Success"

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