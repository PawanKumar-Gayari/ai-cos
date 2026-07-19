"""
Publisher API URLs
------------------

Production-grade publisher routes.

Features:
- dynamic dashboard
- REST APIs
- publishing system
- AI generation
- health monitoring
"""

from __future__ import annotations

from django.urls import path


from apps.publisher.views import (

    publisher_dashboard,

    GenerateArticleAPIView,

    HealthAPIView,

    PublishArticleAPIView,

    ToggleFeatureAPIView,
)


urlpatterns = [

    # =====================================================
    # DASHBOARD
    # =====================================================

    path(

        "",

        publisher_dashboard,

        name="publisher-dashboard",
    ),

    # =====================================================
    # HEALTH CHECK
    # =====================================================

    path(

        "health/",

        HealthAPIView.as_view(),

        name="publisher-health",
    ),

    # =====================================================
    # GENERATE ARTICLE
    # =====================================================

    path(

        "generate/",

        GenerateArticleAPIView.as_view(),

        name="publisher-generate",
    ),

    # =====================================================
    # PUBLISH ARTICLE
    # =====================================================

    path(

        "publish/",

        PublishArticleAPIView.as_view(),

        name="publisher-publish",
    ),

    path(
        "toggle-feature/",
        ToggleFeatureAPIView.as_view(),
        name="publisher-toggle-feature",
    ),



]