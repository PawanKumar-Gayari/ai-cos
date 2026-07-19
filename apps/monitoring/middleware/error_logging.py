"""
Automatic error logging middleware.
"""

import traceback
import logging

from django.utils.deprecation import (
    MiddlewareMixin,
)

from apps.monitoring.models import (
    ErrorLog,
)


logger = logging.getLogger(
    __name__
)


class ErrorLoggingMiddleware(
    MiddlewareMixin
):

    def process_exception(

        self,

        request,

        exception,
    ):

        try:

            ErrorLog.objects.create(

                request_id=getattr(

                    request,

                    "request_id",

                    None,
                ),

                error_type=(
                    type(exception).__name__
                ),

                message=str(exception),

                traceback=(
                    traceback.format_exc()
                ),

                path=request.path,

                method=request.method,

                severity="error",

                source="django",

                ip_address=(
                    self.get_client_ip(
                        request
                    )
                ),

                user_agent=request.META.get(
                    "HTTP_USER_AGENT",
                    "",
                ),
            )

        except Exception as error:

            logger.exception(

                f"Error logging failed: "
                f"{str(error)}"
            )

        return None

    def get_client_ip(
        self,
        request,
    ):

        forwarded = request.META.get(
            "HTTP_X_FORWARDED_FOR"
        )

        if forwarded:

            return (
                forwarded.split(",")[0]
            )

        return request.META.get(
            "REMOTE_ADDR"
        )