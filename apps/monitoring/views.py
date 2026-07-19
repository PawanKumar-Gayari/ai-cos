"""
Enterprise Monitoring Dashboard Views
-------------------------------------

Production-grade monitoring dashboard.

Features:
- authenticated monitoring
- realtime infrastructure stats
- provider analytics
- monitoring reports
- dashboard-safe rendering
- production-safe observability
"""

from __future__ import annotations

import logging

from django.contrib.auth.decorators import (
    login_required,
)

from django.shortcuts import render

from django.views.decorators.http import (
    require_GET,
)

from apps.monitoring.services.system_monitor import (
    SystemMonitor,
)

from apps.dashboard.services.feature_service import (
    FeatureService,
)


logger = logging.getLogger(
    __name__
)


# =========================================================
# MONITORING DASHBOARD
# =========================================================

@login_required
@require_GET
def monitoring_dashboard(
    request,
):

    """
    Enterprise monitoring dashboard.
    """

    logger.info(

        "Monitoring dashboard opened "
        "| user=%s",

        request.user.username,
    )

    try:

        # =============================================
        # FEATURE CHECK
        # =============================================

        if not (
            FeatureService.is_enabled(
                "monitoring_enabled"
            )
        ):

            return render(

                request,

                "dashboard/disabled.html",

                {

                    "title": (
                        "Monitoring Disabled"
                    ),

                    "message": (
                        "Monitoring system "
                        "is disabled."
                    ),
                },
            )

        # =============================================
        # MONITOR
        # =============================================

        monitor = (
            SystemMonitor()
        )

        # =============================================
        # STATS
        # =============================================

        stats = (
            SystemMonitor
            .get_system_stats()
        )

        # =============================================
        # FULL REPORT
        # =============================================

        report = (
            monitor.full_report()
        )

        # =============================================
        # FEATURE STATUS
        # =============================================

        features = (
            FeatureService
            .system_status()
        )

        # =============================================
        # RESPONSE
        # =============================================

        context = {

            "stats": stats,

            "report": report,

            "features": features,

            "page_title": (
                "AI Infrastructure "
                "Monitoring"
            ),

            "dashboard_status": (
                "active"
            ),
        }

        logger.info(
            "Monitoring dashboard loaded."
        )

        return render(

            request,

            "dashboard/monitoring.html",

            context,
        )

    except Exception as error:

        logger.exception(

            "Monitoring dashboard failed "
            "| error=%s",

            error,
        )

        return render(

            request,

            "dashboard/error.html",

            {

                "title": (
                    "Monitoring Error"
                ),

                "error": str(error),
            },
        )