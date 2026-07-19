from django.contrib import admin

from apps.dashboard.models import (
    SystemFeature,
)


# =========================================================
# SYSTEM FEATURE ADMIN
# =========================================================

@admin.register(SystemFeature)
class SystemFeatureAdmin(
    admin.ModelAdmin
):

    list_display = (

        "id",

        "name",

        "key",

        "category",

        "enabled",

        "cpu_intensive",

        "experimental",

        "updated_at",
    )

    list_editable = (

        "enabled",
    )

    list_filter = (

        "enabled",

        "category",

        "cpu_intensive",

        "experimental",
    )

    search_fields = (

        "name",

        "key",

        "description",
    )

    ordering = (

        "category",

        "key",
    )

    readonly_fields = (

        "created_at",

        "updated_at",
    )

    fieldsets = (

        (

            "Core Information",

            {

                "fields": (

                    "name",

                    "key",

                    "description",

                    "category",
                )
            },
        ),

        (

            "Feature Controls",

            {

                "fields": (

                    "enabled",

                    "cpu_intensive",

                    "experimental",
                )
            },
        ),

        (

            "Metadata",

            {

                "fields": (

                    "created_at",

                    "updated_at",
                )
            },
        ),
    )