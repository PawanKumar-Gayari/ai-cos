from django.contrib.auth.decorators import (
    login_required,
)

from django.shortcuts import render

import markdown

from apps.dashboard.services.feature_service import (
    FeatureService,
)

from apps.history.models import (
    GenerationHistory,
)


@login_required
def article_view(request):

    # =====================================================
    # FEATURE CHECK
    # =====================================================

    features = (
        FeatureService.get_features_dict()
    )

    generator_enabled = (
        features.get(
            "generator_enabled",
            True,
        )
    )

    if not generator_enabled:

        return render(

            request,

            "articles/disabled.html",

            {
                "message": (
                    "Generator engine is disabled."
                )
            },
        )

    # =====================================================
    # FETCH LATEST ARTICLE
    # =====================================================

    latest_article = (

        GenerationHistory.objects

        .filter(
            status="completed"
        )

        .order_by(
            "-created_at"
        )

        .first()
    )

    # =====================================================
    # ARTICLE EXISTS
    # =====================================================

    if latest_article:

        markdown_content = (

            latest_article.generated_content
        )

        title = (

            latest_article.query[:80]
        )

        meta_description = (

            f"AI generated article about "
            f"{latest_article.query}"
        )

    # =====================================================
    # NO ARTICLE
    # =====================================================

    else:

        markdown_content = """

# No Article Found

No generated article available yet.
"""

        title = (

            "No Article"
        )

        meta_description = (

            "No generated article available."
        )

    # =====================================================
    # MARKDOWN RENDERING
    # =====================================================

    md = markdown.Markdown(

        extensions=[

            "toc",

            "tables",

            "fenced_code",
        ]
    )

    html_content = (

        md.convert(
            markdown_content
        )
    )

    toc = md.toc

    # =====================================================
    # RENDER TEMPLATE
    # =====================================================

    return render(

        request,

        "articles/view.html",

        {

            "title": title,

            "meta_description": (

                meta_description
            ),

            "content_html": (

                html_content
            ),

            "toc": toc,
        },
    )