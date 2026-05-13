"""
Health check APIs.
"""

from rest_framework import status

from rest_framework.response import (
    Response,
)

from .base import (
    BaseAPIView,
    logger,
)

from utils.response import (
    APIResponse,
)


class HealthCheckView(BaseAPIView):

    def get(
        self,
        request
    ):

        logger.info(
            "Health check requested"
        )

        response = APIResponse.success(

            data={

                "service": "AI COS API",

                "version": "2.0.0",

                "status": "healthy",
            },

            message=(
                "AI COS API is running"
            )
        )

        return Response(
            response,
            status=status.HTTP_200_OK
        )