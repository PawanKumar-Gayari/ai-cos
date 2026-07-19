"""
Enterprise API Rate Limiter
---------------------------

Production-grade API protection middleware.

Features:
- IP-based rate limiting
- API-key rate limiting
- burst protection
- AI abuse prevention
- Redis-backed counters
- OCI optimized
- production-safe architecture
"""

from __future__ import annotations

import logging
import time

from django.http import JsonResponse

from django.core.cache import cache


logger = logging.getLogger(
    __name__
)


class RateLimitMiddleware:

    """
    Enterprise rate limiter middleware.
    """

    # =============================================
    # LIMITS
    # =============================================

    REQUEST_LIMIT = 60

    WINDOW_SECONDS = 60

    BURST_LIMIT = 15

    BURST_WINDOW = 10

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
    # CLIENT IP
    # =============================================

    def get_client_ip(
        self,
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
    # CACHE KEY
    # =============================================

    def build_cache_key(
        self,
        prefix,
        identifier,
    ):

        return (
            f"rate_limit:"
            f"{prefix}:"
            f"{identifier}"
        )

    # =============================================
    # CHECK LIMIT
    # =============================================

    def exceeded(
        self,
        key,
        limit,
        window,
    ):

        current = cache.get(key)

        if current is None:

            cache.set(

                key,

                1,

                timeout=window,
            )

            return False

        if current >= limit:

            return True

        try:

            cache.incr(key)

        except Exception:

            cache.set(

                key,

                current + 1,

                timeout=window,
            )

        return False

    # =============================================
    # MAIN MIDDLEWARE
    # =============================================

    def __call__(
        self,
        request,
    ):

        protected_paths = [

            "/api/",

            "/dashboard/api/",
        ]

        if not any(

            request.path.startswith(
                path
            )

            for path in protected_paths
        ):

            return self.get_response(
                request
            )

        # =========================================
        # IDENTIFIERS
        # =========================================

        ip_address = (
            self.get_client_ip(
                request
            )
        )

        api_key = request.headers.get(
            "X-API-KEY",
            "anonymous",
        )

        # =========================================
        # KEYS
        # =========================================

        ip_key = self.build_cache_key(

            "ip",

            ip_address,
        )

        burst_key = self.build_cache_key(

            "burst",

            ip_address,
        )

        api_key_cache = (
            self.build_cache_key(

                "api",

                api_key,
            )
        )

        # =========================================
        # BURST PROTECTION
        # =========================================

        if self.exceeded(

            burst_key,

            self.BURST_LIMIT,

            self.BURST_WINDOW,
        ):

            logger.warning(

                f"Burst limit exceeded: "
                f"{ip_address}"
            )

            return JsonResponse(

                {

                    "success": False,

                    "error": (
                        "Too many rapid requests."
                    ),
                },

                status=429,
            )

        # =========================================
        # IP LIMIT
        # =========================================

        if self.exceeded(

            ip_key,

            self.REQUEST_LIMIT,

            self.WINDOW_SECONDS,
        ):

            logger.warning(

                f"IP rate limit exceeded: "
                f"{ip_address}"
            )

            return JsonResponse(

                {

                    "success": False,

                    "error": (
                        "Rate limit exceeded."
                    ),
                },

                status=429,
            )

        # =========================================
        # API KEY LIMIT
        # =========================================

        if api_key != "anonymous":

            if self.exceeded(

                api_key_cache,

                self.REQUEST_LIMIT,

                self.WINDOW_SECONDS,
            ):

                logger.warning(

                    f"API limit exceeded: "
                    f"{api_key[:10]}"
                )

                return JsonResponse(

                    {

                        "success": False,

                        "error": (
                            "API quota exceeded."
                        ),
                    },

                    status=429,
                )

        response = self.get_response(
            request
        )

        # =========================================
        # RESPONSE HEADERS
        # =========================================

        response[
            "X-RateLimit-Limit"
        ] = str(
            self.REQUEST_LIMIT
        )

        response[
            "X-RateLimit-Window"
        ] = str(
            self.WINDOW_SECONDS
        )

        response[
            "X-Powered-By"
        ] = "AI-COS"

        return response"""
Enterprise API Rate Limiter
---------------------------

Production-grade API protection middleware.

Features:
- IP-based rate limiting
- API-key rate limiting
- burst protection
- AI abuse prevention
- Redis-backed counters
- OCI optimized
- production-safe architecture
"""

from __future__ import annotations

import logging
import time

from django.http import JsonResponse

from django.core.cache import cache


logger = logging.getLogger(
    __name__
)


class RateLimitMiddleware:

    """
    Enterprise rate limiter middleware.
    """

    # =============================================
    # LIMITS
    # =============================================

    REQUEST_LIMIT = 60

    WINDOW_SECONDS = 60

    BURST_LIMIT = 15

    BURST_WINDOW = 10

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
    # CLIENT IP
    # =============================================

    def get_client_ip(
        self,
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
    # CACHE KEY
    # =============================================

    def build_cache_key(
        self,
        prefix,
        identifier,
    ):

        return (
            f"rate_limit:"
            f"{prefix}:"
            f"{identifier}"
        )

    # =============================================
    # CHECK LIMIT
    # =============================================

    def exceeded(
        self,
        key,
        limit,
        window,
    ):

        current = cache.get(key)

        if current is None:

            cache.set(

                key,

                1,

                timeout=window,
            )

            return False

        if current >= limit:

            return True

        try:

            cache.incr(key)

        except Exception:

            cache.set(

                key,

                current + 1,

                timeout=window,
            )

        return False

    # =============================================
    # MAIN MIDDLEWARE
    # =============================================

    def __call__(
        self,
        request,
    ):

        protected_paths = [

            "/api/",

            "/dashboard/api/",
        ]

        if not any(

            request.path.startswith(
                path
            )

            for path in protected_paths
        ):

            return self.get_response(
                request
            )

        # =========================================
        # IDENTIFIERS
        # =========================================

        ip_address = (
            self.get_client_ip(
                request
            )
        )

        api_key = request.headers.get(
            "X-API-KEY",
            "anonymous",
        )

        # =========================================
        # KEYS
        # =========================================

        ip_key = self.build_cache_key(

            "ip",

            ip_address,
        )

        burst_key = self.build_cache_key(

            "burst",

            ip_address,
        )

        api_key_cache = (
            self.build_cache_key(

                "api",

                api_key,
            )
        )

        # =========================================
        # BURST PROTECTION
        # =========================================

        if self.exceeded(

            burst_key,

            self.BURST_LIMIT,

            self.BURST_WINDOW,
        ):

            logger.warning(

                f"Burst limit exceeded: "
                f"{ip_address}"
            )

            return JsonResponse(

                {

                    "success": False,

                    "error": (
                        "Too many rapid requests."
                    ),
                },

                status=429,
            )

        # =========================================
        # IP LIMIT
        # =========================================

        if self.exceeded(

            ip_key,

            self.REQUEST_LIMIT,

            self.WINDOW_SECONDS,
        ):

            logger.warning(

                f"IP rate limit exceeded: "
                f"{ip_address}"
            )

            return JsonResponse(

                {

                    "success": False,

                    "error": (
                        "Rate limit exceeded."
                    ),
                },

                status=429,
            )

        # =========================================
        # API KEY LIMIT
        # =========================================

        if api_key != "anonymous":

            if self.exceeded(

                api_key_cache,

                self.REQUEST_LIMIT,

                self.WINDOW_SECONDS,
            ):

                logger.warning(

                    f"API limit exceeded: "
                    f"{api_key[:10]}"
                )

                return JsonResponse(

                    {

                        "success": False,

                        "error": (
                            "API quota exceeded."
                        ),
                    },

                    status=429,
                )

        response = self.get_response(
            request
        )

        # =========================================
        # RESPONSE HEADERS
        # =========================================

        response[
            "X-RateLimit-Limit"
        ] = str(
            self.REQUEST_LIMIT
        )

        response[
            "X-RateLimit-Window"
        ] = str(
            self.WINDOW_SECONDS
        )

        response[
            "X-Powered-By"
        ] = "AI-COS"

        return response