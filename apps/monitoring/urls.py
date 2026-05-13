"""
Monitoring URLs.
"""

from django.urls import path

from apps.monitoring.api.monitoring_views import (

    MonitoringAPIView,

    HealthCheckAPIView,

    MetricsAPIView,
)


urlpatterns = [

    # ==========================================
    # FULL SYSTEM REPORT
    # ==========================================

    path(

        "report/",

        MonitoringAPIView.as_view(),

        name="monitoring-report",
    ),

    # ==========================================
    # HEALTH CHECK
    # ==========================================

    path(

        "health/",

        HealthCheckAPIView.as_view(),

        name="health-check",
    ),

    # ==========================================
    # METRICS
    # ==========================================

    path(

        "metrics/",

        MetricsAPIView.as_view(),

        name="monitoring-metrics",
    ),
]