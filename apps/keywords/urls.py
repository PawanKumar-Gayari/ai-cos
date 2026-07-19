"""
Production Keywords URLs
------------------------

Enterprise-grade SEO intelligence routes.

Features:
- API versioning ready
- clean endpoint structure
- scalable routing
- OCI optimized
- production-safe
"""

from __future__ import annotations

from django.urls import path

from apps.keywords.api_views import (

    analyze_keyword_api,
)


# =========================================================
# APP NAME
# =========================================================

app_name = "keywords"


# =========================================================
# URL PATTERNS
# =========================================================

urlpatterns = [

    # =====================================================
    # SEO PIPELINE ANALYSIS
    # =====================================================

    path(

        "analyze/",

        analyze_keyword_api,

        name="analyze-keyword",
    ),

    # =====================================================
    # COMPATIBILITY ROUTE
    # =====================================================

    path(

        "analyze",

        analyze_keyword_api,

        name="analyze-keyword-no-slash",
    ),
]