"""
Automatic API request monitoring middleware.
"""

import time
import uuid
import logging

from django.utils.deprecation import (
    MiddlewareMixin,
)

from apps.monitoring.models import (
    APIRequestLog,
)


logger = logging.getLogger(
    __name__
)


class RequestLoggingMiddleware(
    MiddlewareMixin
):

    def process_request(
        self,
        request,
    ):

        request.start_time = (
            time.time()
        )

        request.request_id = str(
            uuid.uuid4()
        )

    def process_response(

        self,

        request,

        response,
    ):

        try:

            execution_time = 0

            if hasattr(
                request,
                "start_time",
            ):

                execution_time = round(

                    time.time()
                    - request.start_time,

                    4,
                )

            APIRequestLog.objects.create(

                request_id=getattr(

                    request,

                    "request_id",

                    str(uuid.uuid4()),
                ),

                method=request.method,

                path=request.path,

                query_params=str(
                    request.GET.dict()
                ),

                status_code=(
                    response.status_code
                ),

                execution_time=(
                    execution_time
                ),

                response_size_kb=round(

                    len(response.content)
                    / 1024,

                    2,
                )

                if hasattr(
                    response,
                    "content",
                )

                else 0,

                ip_address=(
                    self.get_client_ip(
                        request
                    )
                ),

                user_agent=request.META.get(
                    "HTTP_USER_AGENT",
                    "",
                ),

                successful=(

                    response.status_code
                    < 400
                ),
            )

        except Exception as error:

            logger.exception(

                f"Request logging failed: "
                f"{str(error)}"
            )

        return response

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