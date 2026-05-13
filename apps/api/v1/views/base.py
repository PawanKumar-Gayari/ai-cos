"""
Base API utilities and shared imports.
"""

from rest_framework import status

from rest_framework.response import (
    Response,
)

from rest_framework.views import (
    APIView,
)

from utils.response import (
    APIResponse,
)

from utils.logger import (
    logger,
)

from utils.exceptions import (
    AICOSException,
)


class BaseAPIView(APIView):

    def success_response(
        self,
        data=None,
        message="Success",
        status_code=status.HTTP_200_OK
    ):

        response = APIResponse.success(
            data=data,
            message=message
        )

        return Response(
            response,
            status=status_code
        )

    def validation_error_response(
        self,
        errors
    ):

        response = APIResponse.validation_error(
            errors=errors
        )

        return Response(
            response,
            status=status.HTTP_422_UNPROCESSABLE_ENTITY
        )

    def error_response(
        self,
        message,
        status_code=status.HTTP_400_BAD_REQUEST,
        error_code="ERROR"
    ):

        response = APIResponse.error(
            message=message,
            status_code=status_code,
            error_code=error_code
        )

        return Response(
            response,
            status=status_code
        )

    def server_error_response(
        self,
        error
    ):

        logger.error(str(error))

        response = APIResponse.server_error(
            str(error)
        )

        return Response(
            response,
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )