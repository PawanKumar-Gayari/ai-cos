"""
Enterprise monitoring API views.
"""

import logging

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers

from drf_spectacular.utils import (
    extend_schema,
)

from apps.monitoring.services.system_monitor import (
    SystemMonitor
)


logger = logging.getLogger(
    __name__
)


# =====================================================
# SERIALIZERS
# =====================================================

class EmptySerializer(
    serializers.Serializer
):
    pass


# =====================================================
# FULL MONITORING API
# =====================================================

class MonitoringAPIView(
    APIView
):

    """
    Full monitoring endpoint.
    """

    authentication_classes = []

    permission_classes = []

    @extend_schema(

        tags=["Monitoring"],

        request=EmptySerializer,

        responses={
            200: EmptySerializer
        },
    )
    def get(
        self,
        request,
    ):

        try:

            monitor = (
                SystemMonitor()
            )

            report = (
                monitor.full_report()
            )

            return Response(

                {

                    "success": True,

                    "message": (
                        "Monitoring report generated."
                    ),

                    "data": report,
                },

                status=status.HTTP_200_OK,
            )

        except Exception as error:

            logger.exception(

                f"Monitoring API failed: "
                f"{str(error)}"
            )

            return Response(

                {

                    "success": False,

                    "message": (
                        "Monitoring system failure."
                    ),

                    "error": str(error),
                },

                status=(
                    status.HTTP_500_INTERNAL_SERVER_ERROR
                ),
            )


# =====================================================
# HEALTH CHECK API
# =====================================================

class HealthCheckAPIView(
    APIView
):

    """
    Lightweight health endpoint.
    """

    authentication_classes = []

    permission_classes = []

    @extend_schema(

        tags=["Monitoring"],

        request=EmptySerializer,

        responses={
            200: EmptySerializer
        },
    )
    def get(
        self,
        request,
    ):

        try:

            monitor = (
                SystemMonitor()
            )

            cache_status = (

                monitor.cache_metrics()
            )

            provider_status = (

                monitor.provider_health()
            )

            resource_status = (

                monitor.resource_metrics()
            )

            healthy = (

                cache_status.get(
                    "cache_working",
                    False,
                )

                and

                provider_status.get(
                    "healthy",
                    False,
                )
            )

            return Response(

                {

                    "healthy": healthy,

                    "cache": (
                        cache_status
                    ),

                    "providers": (
                        provider_status
                    ),

                    "resources": (
                        resource_status
                    ),
                },

                status=(
                    status.HTTP_200_OK
                ),
            )

        except Exception as error:

            logger.exception(

                f"Health check failed: "
                f"{str(error)}"
            )

            return Response(

                {

                    "healthy": False,

                    "error": str(error),
                },

                status=(
                    status.HTTP_500_INTERNAL_SERVER_ERROR
                ),
            )


# =====================================================
# METRICS API
# =====================================================

class MetricsAPIView(
    APIView
):

    """
    Lightweight metrics endpoint.
    """

    authentication_classes = []

    permission_classes = []

    @extend_schema(

        tags=["Monitoring"],

        request=EmptySerializer,

        responses={
            200: EmptySerializer
        },
    )
    def get(
        self,
        request,
    ):

        try:

            monitor = (
                SystemMonitor()
            )

            metrics = {

                "resources": (

                    monitor.resource_metrics()
                ),

                "generation": (

                    monitor.generation_metrics()
                ),

                "memory": (

                    monitor.memory_metrics()
                ),

                "providers": (

                    monitor.provider_health()
                ),

                "cache": (

                    monitor.cache_metrics()
                ),
            }

            return Response(

                {

                    "success": True,

                    "metrics": metrics,
                },

                status=status.HTTP_200_OK,
            )

        except Exception as error:

            logger.exception(

                f"Metrics API failed: "
                f"{str(error)}"
            )

            return Response(

                {

                    "success": False,

                    "error": str(error),
                },

                status=(
                    status.HTTP_500_INTERNAL_SERVER_ERROR
                ),
            )