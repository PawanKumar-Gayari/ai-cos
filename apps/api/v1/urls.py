from django.urls import (
    include,
    path,
)

from apps.api.v1.views import (

    HealthCheckView,

    GenerateContentView,

    DiscoveryView,

    CompetitorView,

    ArticleListView,

    ArticleDetailView,
)


urlpatterns = [

    # ==================================================
    # HEALTH CHECK
    # ==================================================

    path(
        "health/",
        HealthCheckView.as_view(),
        name="health-check",
    ),

    # ==================================================
    # AI HISTORY
    # ==================================================

    path(
        "history/",
        include(
            "apps.api.v1.history.urls"
        ),
    ),

    # ==================================================
    # AI GENERATOR API
    # ==================================================

    path(
        "generator/",
        include(
            "apps.api.v1.generator.urls"
        ),
    ),

    # ==================================================
    # GENERATE CONTENT
    # ==================================================

    path(
        "generate/",
        GenerateContentView.as_view(),
        name="generate-content",
    ),

    # ==================================================
    # DISCOVERY ENGINE
    # ==================================================

    path(
        "discovery/",
        DiscoveryView.as_view(),
        name="discovery-engine",
    ),

    # ==================================================
    # COMPETITOR ENGINE
    # ==================================================

    path(
        "competitor/",
        CompetitorView.as_view(),
        name="competitor-engine",
    ),

    # ==================================================
    # LIST ARTICLES
    # ==================================================

    path(
        "articles/",
        ArticleListView.as_view(),
        name="article-list",
    ),

    # ==================================================
    # ARTICLE DETAIL
    # ==================================================

    path(
        "articles/<int:article_id>/",
        ArticleDetailView.as_view(),
        name="article-detail",
    ),
]