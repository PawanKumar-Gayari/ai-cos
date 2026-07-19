from django.contrib import (
    admin
)

from apps.generator.models import (
    GeneratorConfig
)


@admin.register(
    GeneratorConfig
)
class GeneratorConfigAdmin(
    admin.ModelAdmin
):

    # ==========================================
    # LIST PAGE
    # ==========================================

    list_display = (

        "name",

        "active_provider",

        "default_model",

        "content_type",

        "tone",

        "target_word_count",

        "minimum_quality_score",

        "is_active",

        "updated_at",
    )

    # ==========================================
    # FILTERS
    # ==========================================

    list_filter = (

        "active_provider",

        "content_type",

        "tone",

        "enable_memory",

        "enable_seo",

        "enable_fallback",

        "is_active",
    )

    # ==========================================
    # SEARCH
    # ==========================================

    search_fields = (

        "name",

        "default_model",

        "system_prompt",
    )

    # ==========================================
    # READONLY
    # ==========================================

    readonly_fields = (

        "created_at",

        "updated_at",
    )

    # ==========================================
    # ORGANIZED FORM
    # ==========================================

    fieldsets = (

        (

            "Basic Configuration",

            {

                "fields": (

                    "name",

                    "active_provider",

                    "default_model",

                    "is_active",
                )
            },
        ),

        (

            "Generation Settings",

            {

                "fields": (

                    "content_type",

                    "tone",

                    "target_word_count",

                    "temperature",

                    "max_tokens",
                )
            },
        ),

        (

            "Quality Control",

            {

                "fields": (

                    "minimum_quality_score",

                    "max_rewrite_loops",
                )
            },
        ),

        (

            "AI Features",

            {

                "fields": (

                    "enable_memory",

                    "enable_scoring",

                    "enable_cleaning",

                    "enable_fallback",

                    "enable_seo",
                )
            },
        ),

        (

            "Prompt Engineering",

            {

                "fields": (

                    "system_prompt",

                    "prompt_template",
                )
            },
        ),

        (

            "Timestamps",

            {

                "fields": (

                    "created_at",

                    "updated_at",
                )
            },
        ),
    )

    # ==========================================
    # PAGINATION
    # ==========================================

    list_per_page = 20