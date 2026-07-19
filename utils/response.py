"""
Central API response builder for AI COS.
"""

from utils.helpers import (
    Helpers,
)


class APIResponse:

    # ==================================================
    # SUCCESS RESPONSE
    # ==================================================

    @classmethod
    def success(
        cls,
        data=None,
        message="Request successful.",
        meta=None,
        status_code=200
    ):

        return {

            "success": True,

            "status_code": status_code,

            "message": message,

            "timestamp": (
                Helpers.current_timestamp()
            ),

            "data": data or {},

            "meta": meta or {},
        }

    # ==================================================
    # ERROR RESPONSE
    # ==================================================

    @classmethod
    def error(
        cls,
        message="Request failed.",
        errors=None,
        status_code=400,
        error_code="ERROR",
        meta=None
    ):

        return {

            "success": False,

            "status_code": status_code,

            "message": message,

            "timestamp": (
                Helpers.current_timestamp()
            ),

            "error_code": (
                error_code
            ),

            "errors": (
                errors or []
            ),

            "meta": meta or {},
        }

    # ==================================================
    # PAGINATION RESPONSE
    # ==================================================

    @classmethod
    def paginated(
        cls,
        data,
        total_items=0,
        page=1,
        page_size=10,
        message="Paginated data fetched successfully.",
        meta=None
    ):

        total_pages = 1

        if page_size > 0:

            total_pages = max(

                1,

                (
                    total_items
                    + page_size
                    - 1
                ) // page_size
            )

        return {

            "success": True,

            "status_code": 200,

            "message": message,

            "timestamp": (
                Helpers.current_timestamp()
            ),

            "data": data,

            "pagination": {

                "total_items": (
                    total_items
                ),

                "page": page,

                "page_size": (
                    page_size
                ),

                "total_pages": (
                    total_pages
                ),
            },

            "meta": meta or {},
        }

    # ==================================================
    # CREATED RESPONSE
    # ==================================================

    @classmethod
    def created(
        cls,
        data=None,
        message="Resource created successfully.",
        meta=None
    ):

        return cls.success(

            data=data,

            message=message,

            meta=meta,

            status_code=201
        )

    # ==================================================
    # VALIDATION ERROR
    # ==================================================

    @classmethod
    def validation_error(
        cls,
        errors=None,
        message="Validation failed.",
        meta=None
    ):

        return cls.error(

            message=message,

            errors=errors,

            status_code=422,

            error_code="VALIDATION_ERROR",

            meta=meta
        )

    # ==================================================
    # NOT FOUND RESPONSE
    # ==================================================

    @classmethod
    def not_found(
        cls,
        message="Resource not found.",
        meta=None
    ):

        return cls.error(

            message=message,

            status_code=404,

            error_code="NOT_FOUND",

            meta=meta
        )

    # ==================================================
    # SERVER ERROR RESPONSE
    # ==================================================

    @classmethod
    def server_error(
        cls,
        message="Internal server error.",
        meta=None
    ):

        return cls.error(

            message=message,

            status_code=500,

            error_code="SERVER_ERROR",

            meta=meta
        )

    # ==================================================
    # UNAUTHORIZED RESPONSE
    # ==================================================

    @classmethod
    def unauthorized(
        cls,
        message="Unauthorized access.",
        meta=None
    ):

        return cls.error(

            message=message,

            status_code=401,

            error_code="UNAUTHORIZED",

            meta=meta
        )

    # ==================================================
    # FORBIDDEN RESPONSE
    # ==================================================

    @classmethod
    def forbidden(
        cls,
        message="Access forbidden.",
        meta=None
    ):

        return cls.error(

            message=message,

            status_code=403,

            error_code="FORBIDDEN",

            meta=meta
        )

    # ==================================================
    # CUSTOM RESPONSE
    # ==================================================

    @classmethod
    def custom(
        cls,
        success=True,
        message="Custom response.",
        data=None,
        errors=None,
        status_code=200,
        error_code=None,
        meta=None
    ):

        return {

            "success": success,

            "status_code": status_code,

            "message": message,

            "timestamp": (
                Helpers.current_timestamp()
            ),

            "data": data or {},

            "errors": errors or [],

            "error_code": error_code,

            "meta": meta or {},
        }