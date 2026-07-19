"""
Enterprise Dashboard API
------------------------

Production-grade dashboard monitoring API.

Features:
- live system monitoring
- provider analytics
- queue monitoring
- feature controls
- authenticated dashboard access
- frontend-ready responses
- production-safe serialization
- monitoring-safe architecture
"""

from __future__ import annotations

import logging
import traceback

from django.contrib.auth.decorators import (
    login_required,
)

from django.http import JsonResponse

from django.views.decorators.http import (
    require_GET,
)

from apps.monitoring.services.system_monitor import (
    SystemMonitor,
)

from apps.dashboard.services.feature_service import (
    FeatureService,
)

from apps.llm.router import (
    LLMRouter,
)


logger = logging.getLogger(
    __name__
)


# =========================================================
# SAFE SERIALIZER
# =========================================================

def safe_data(
    value,
):

    try:

        if value is None:

            return None

        if isinstance(
            value,
            (
                dict,
                list,
                str,
                int,
                float,
                bool,
            ),
        ):

            return value

        if hasattr(
            value,
            "values",
        ):

            return list(
                value.values()
            )

        return str(value)

    except Exception:

        return None


# =========================================================
# STATS API
# =========================================================

@login_required
@require_GET
def stats_api(
    request,
):

    """
    Live enterprise dashboard stats API.
    """

    try:

        logger.info(

            "Dashboard stats requested "
            "| user=%s",

            request.user.username,
        )

        # =========================================
        # SYSTEM STATS
        # =========================================

        stats = (

            SystemMonitor
            .get_system_stats()
        )

        # =========================================
        # FEATURES
        # =========================================

        features = (

            FeatureService
            .get_features()
        )

        # =========================================
        # LLM ROUTER
        # =========================================

        router = (
            LLMRouter()
        )

        router_status = (
            router.router_status()
        )

        # =========================================
        # RESPONSE
        # =========================================

        response = {

            "success": True,

            "user": (
                request.user.username
            ),

            "authenticated": (
                request.user.is_authenticated
            ),

            "stats": (
                safe_data(stats)
            ),

            "features": (
                safe_data(features)
            ),

            "router": (
                safe_data(
                    router_status
                )
            ),

            "system": {

                "monitoring":
                True,

                "dashboard":
                "active",

                "ai_providers": (

                    router.provider_count()
                ),
            },
        }

        logger.info(
            "Dashboard stats success."
        )

        return JsonResponse(
            response
        )

    except Exception as error:

        logger.exception(

            "Dashboard API failed "
            "| error=%s",

            error,
        )

        traceback.print_exc()

        return JsonResponse(

            {

                "success": False,

                "error": str(error),

                "traceback": (

                    traceback
                    .format_exc()
                )[:3000],
            },

            status=500,
        )