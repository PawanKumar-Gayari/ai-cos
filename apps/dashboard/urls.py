"""
Dashboard URLs.
"""

from django.urls import path

from .api_views import (
    stats_api,
)

from .views import (

    generator,

    index,

    monitoring,

    toggle_feature,

    keywords_dashboard,

    keyword_results,
)


urlpatterns = [

    # =====================================================
    # DASHBOARD HOME
    # =====================================================

    path(
        "",
        index,
        name="dashboard-home",
    ),

    # =====================================================
    # MONITORING PAGE
    # =====================================================

    path(
        "monitoring/",
        monitoring,
        name="dashboard-monitoring",
    ),

    # =====================================================
    # GENERATOR PAGE
    # =====================================================

    path(
        "generator/",
        generator,
        name="dashboard-generator",
    ),

    # =====================================================
    # KEYWORDS DASHBOARD
    # =====================================================

    path(
        "keywords/",
        keywords_dashboard,
        name="dashboard-keywords",
    ),

    # =====================================================
    # KEYWORD RESULTS PAGE
    # =====================================================

    path(

        "results/<int:job_id>/",

        keyword_results,

        name="keyword-results",
    ),

    # =====================================================
    # FEATURE TOGGLE
    # =====================================================

    path(
        "toggle/<int:pk>/",
        toggle_feature,
        name="toggle-feature",
    ),

    # =====================================================
    # LIVE STATS API
    # =====================================================

    path(
        "api/stats/",
        stats_api,
        name="dashboard-stats",
    ),

]