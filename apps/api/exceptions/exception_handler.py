"""
Global exception handler for AI COS API.
"""

import traceback

from rest_framework.views import (
    exception_handler,
)

from rest_framework.response import (
    Response,
)

from rest_framework import (
    status,
)

from rest_framework.exceptions import (

    ValidationError,

    NotFound,

    PermissionDenied,
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

from utils.helpers import (
    Helpers,
)

from apps.monitoring.models import (
    ErrorLog,
)


def custom_exception_handler(
    exc,
    context
):

    # ==================================================
    # DEFAULT DRF HANDLER
    # ==================================================

    response = exception_handler(

        exc,

        context
    )

    # ==================================================
    # REQUEST INFO
    # ==================================================

    request = context.get(
        "request"
    )

    request_path = "unknown"

    request_method = "unknown"

    request_id = None

    if request:

        request_path = getattr(

            request,

            "path",

            "unknown"
        )

        request_method = getattr(

            request,

            "method",

            "unknown"
        )

        request_id = getattr(

            request,

            "request_id",

            None
        )

    # ==================================================
    # ERROR DETAILS
    # ==================================================

    error_type = (
        exc.__class__.__name__
    )

    error_message = str(
        exc
    )

    traceback_data = (
        traceback.format_exc()
    )

    # ==================================================
    # LOG ERROR
    # ==================================================

    logger.exception(

        f"[API ERROR] "
        f"TYPE={error_type} | "
        f"PATH={request_path} | "
        f"METHOD={request_method} | "
        f"ERROR={error_message}"
    )

    # ==================================================
    # SAVE ERROR LOG
    # ==================================================

    try:

        ErrorLog.objects.create(

            request_id=request_id,

            error_type=error_type,

            message=error_message,

            traceback=traceback_data,

            path=request_path,

            severity="error",
        )

    except Exception as error:

        logger.exception(

            f"[ERROR LOG SAVE FAILED] "
            f"{str(error)}"
        )

    # ==================================================
    # VALIDATION ERROR
    # ==================================================

    if isinstance(
        exc,
        ValidationError
    ):

        formatted_response = (
            APIResponse.validation_error(

                errors=response.data
                if response else [],

                message=(
                    "Validation failed."
                )
            )
        )

        return Response(

            formatted_response,

            status=status.HTTP_422_UNPROCESSABLE_ENTITY
        )

    # ==================================================
    # NOT FOUND
    # ==================================================

    if isinstance(
        exc,
        NotFound
    ):

        formatted_response = (
            APIResponse.not_found(

                message=str(exc)
            )
        )

        return Response(

            formatted_response,

            status=status.HTTP_404_NOT_FOUND
        )

    # ==================================================
    # PERMISSION DENIED
    # ==================================================

    if isinstance(
        exc,
        PermissionDenied
    ):

        formatted_response = (
            APIResponse.forbidden(

                message=str(exc)
            )
        )

        return Response(

            formatted_response,

            status=status.HTTP_403_FORBIDDEN
        )

    # ==================================================
    # CUSTOM AI COS EXCEPTION
    # ==================================================

    if isinstance(
        exc,
        AICOSException
    ):

        formatted_response = (
            APIResponse.error(

                message=str(exc),

                status_code=400,

                error_code=(
                    "AICOS_ERROR"
                ),

                meta={

                    "request_id": (
                        request_id
                    ),

                    "timestamp": (
                        Helpers.current_timestamp()
                    ),
                }
            )
        )

        return Response(

            formatted_response,

            status=status.HTTP_400_BAD_REQUEST
        )

    # ==================================================
    # DRF DEFAULT RESPONSE
    # ==================================================

    if response is not None:

        formatted_response = (
            APIResponse.error(

                message=(
                    "Request failed."
                ),

                errors=response.data,

                status_code=response.status_code,

                error_code=(
                    "API_ERROR"
                ),

                meta={

                    "request_id": (
                        request_id
                    ),

                    "timestamp": (
                        Helpers.current_timestamp()
                    ),
                }
            )
        )

        return Response(

            formatted_response,

            status=response.status_code
        )

    # ==================================================
    # UNKNOWN SERVER ERROR
    # ==================================================

    formatted_response = (
        APIResponse.server_error(

            message=(
                "An unexpected error occurred."
            ),

            meta={

                "request_id": (
                    request_id
                ),

                "timestamp": (
                    Helpers.current_timestamp()
                ),
            }
        )
    )

    return Response(

        formatted_response,

        status=status.HTTP_500_INTERNAL_SERVER_ERROR
    )