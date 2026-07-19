"""
Enterprise API Authentication Middleware
----------------------------------------

Production-grade API authentication layer.

Features:
- constant-time API key validation
- protected route groups
- public health endpoints
- Authorization Bearer support
- X-API-KEY fallback support
- secure request logging
- malformed key detection
- WordPress compatible
- OCI optimized
- production-safe security
"""

from __future__ import annotations

import hmac
import logging
import re
import time

from django.conf import settings

from django.http import JsonResponse


logger = logging.getLogger(
    __name__
)


class APIKeyMiddleware:

    """
    Enterprise API authentication middleware.
    """

    # =============================================
    # PROTECTED ROUTES
    # =============================================

    PROTECTED_PATHS = [

        "/api/v1/generator/",

        "/api/keywords/",

        "/dashboard/api/",
    ]

    # =============================================
    # PUBLIC ROUTES
    # =============================================

    PUBLIC_PATHS = [

        "/api/publisher/health/",
    ]

    # =============================================
    # ALLOWED KEY PATTERN
    # =============================================

    API_KEY_PATTERN = re.compile(
        r"^[A-Za-z0-9_\-]{12,200}$"
    )

    # =============================================
    # INIT
    # =============================================

    def __init__(
        self,
        get_response,
    ):

        self.get_response = (
            get_response
        )

    # =============================================
    # CHECK PUBLIC ROUTE
    # =============================================

    @classmethod
    def is_public_route(
        cls,
        path,
    ):

        return any(

            path.startswith(
                public
            )

            for public in (
                cls.PUBLIC_PATHS
            )
        )

    # =============================================
    # CHECK PROTECTED ROUTE
    # =============================================

    @classmethod
    def is_protected_route(
        cls,
        path,
    ):

        return any(

            path.startswith(
                protected
            )

            for protected in (
                cls.PROTECTED_PATHS
            )
        )

    # =============================================
    # CLIENT IP
    # =============================================

    @staticmethod
    def client_ip(
        request,
    ):

        forwarded = request.META.get(
            "HTTP_X_FORWARDED_FOR"
        )

        if forwarded:

            return forwarded.split(",")[
                0
            ].strip()

        return request.META.get(
            "REMOTE_ADDR",
            "unknown",
        )

    # =============================================
    # GET API KEY
    # =============================================

    @staticmethod
    def get_api_key(
        request,
    ):

        # =========================================
        # X-API-KEY SUPPORT
        # =========================================

        api_key = (

            request.META.get(
                "HTTP_X_API_KEY"
            )

            or

            request.headers.get(
                "X-API-KEY"
            )

            or

            request.META.get(
                "X-API-KEY"
            )
        )

        # =========================================
        # AUTHORIZATION HEADER SUPPORT
        # =========================================

        if not api_key:

            auth_header = (

                request.META.get(
                    "HTTP_AUTHORIZATION"
                )

                or

                request.headers.get(
                    "Authorization"
                )
            )

            if auth_header:

                auth_header = str(
                    auth_header
                ).strip()

                if auth_header.startswith(
                    "Bearer "
                ):

                    api_key = auth_header.replace(

                        "Bearer ",

                        ""
                    ).strip()

        if not api_key:

            return None

        return str(
            api_key
        ).strip()

    # =============================================
    # SAFE KEY PREVIEW
    # =============================================

    @staticmethod
    def safe_key_preview(
        api_key,
    ):

        if not api_key:

            return "missing"

        if len(api_key) < 8:

            return "invalid"

        return (
            f"{api_key[:4]}"
            f"..."
            f"{api_key[-4:]}"
        )

    # =============================================
    # MALFORMED KEY
    # =============================================

    @classmethod
    def malformed_key(
        cls,
        api_key,
    ):

        if not api_key:

            return True

        return not bool(

            cls.API_KEY_PATTERN.match(
                api_key
            )
        )

    # =============================================
    # UNAUTHORIZED RESPONSE
    # =============================================

    @staticmethod
    def unauthorized_response(
        message="Invalid API key.",
    ):

        return JsonResponse(

            {

                "success": False,

                "error": message,
            },

            status=403,
        )

    # =============================================
    # SECURITY HEADERS
    # =============================================

    @staticmethod
    def apply_security_headers(
        response,
        execution_time,
    ):

        response[
            "X-API-Auth"
        ] = "verified"

        response[
            "X-Response-Time"
        ] = str(
            execution_time
        )

        response[
            "X-Content-Type-Options"
        ] = "nosniff"

        response[
            "Referrer-Policy"
        ] = "same-origin"

        return response

    # =============================================
    # MAIN
    # =============================================

    def __call__(
        self,
        request,
    ):

        started = time.time()

        path = request.path

        ip_address = self.client_ip(
            request
        )

        # =========================================
        # PUBLIC ROUTES
        # =========================================

        if self.is_public_route(
            path
        ):

            logger.info(

                f"Public API access | "
                f"path={path} | "
                f"ip={ip_address}"
            )

            response = self.get_response(
                request
            )

            execution_time = round(

                time.time()
                - started,

                4,
            )

            return self.apply_security_headers(

                response,

                execution_time,
            )

        # =========================================
        # NON PROTECTED
        # =========================================

        if not self.is_protected_route(
            path
        ):

            return self.get_response(
                request
            )

        # =========================================
        # API KEY
        # =========================================

        api_key = self.get_api_key(
            request
        )

        expected_key = str(

            getattr(

                settings,

                "AICOS_API_KEY",

                "",
            )
        ).strip()

        # =========================================
        # LOG REQUEST
        # =========================================

        logger.info(

            f"Protected API request | "
            f"path={path} | "
            f"ip={ip_address} | "
            f"key={self.safe_key_preview(api_key)}"
        )

        # =========================================
        # MALFORMED
        # =========================================

        if self.malformed_key(
            api_key
        ):

            logger.warning(

                f"Malformed API key | "
                f"path={path} | "
                f"ip={ip_address}"
            )

            return self.unauthorized_response(

                "Malformed API key."
            )

        # =========================================
        # CONSTANT-TIME VALIDATION
        # =========================================

        is_valid = hmac.compare_digest(

            api_key,

            expected_key,
        )

        if not is_valid:

            logger.warning(

                f"Invalid API key attempt | "
                f"path={path} | "
                f"ip={ip_address}"
            )

            return self.unauthorized_response()

        # =========================================
        # SUCCESS
        # =========================================

        response = self.get_response(
            request
        )

        execution_time = round(

            time.time()
            - started,

            4,
        )

        response = self.apply_security_headers(

            response,

            execution_time,
        )

        logger.info(

            f"API authenticated | "
            f"path={path} | "
            f"time={execution_time}s"
        )

        return response