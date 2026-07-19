"""
Request middleware for AI COS platform.
"""

import time

import uuid

from django.conf import (
    settings,
)

from utils.logger import (
    logger,
)

from apps.monitoring.models import (
    APIRequestLog,
)


class RequestMiddleware:

    def __init__(
        self,
        get_response
    ):

        self.get_response = (
            get_response
        )

    # ==================================================
    # MAIN REQUEST HANDLER
    # ==================================================

    def __call__(
        self,
        request
    ):

        # ==============================================
        # START TIMER
        # ==============================================

        start_time = time.time()

        # ==============================================
        # GENERATE REQUEST ID
        # ==============================================

        request_id = str(
            uuid.uuid4()
        )

        # ==============================================
        # ATTACH REQUEST ID
        # ==============================================

        request.request_id = (
            request_id
        )

        # ==============================================
        # REQUEST INFO
        # ==============================================

        request_method = (
            request.method
        )

        request_path = (
            request.path
        )

        request_ip = (
            self.get_client_ip(
                request
            )
        )

        user_agent = request.META.get(

            "HTTP_USER_AGENT",

            "unknown"
        )

        # ==============================================
        # REQUEST START LOG
        # ==============================================

        logger.info(

            f"[REQUEST START] "
            f"ID={request_id} | "
            f"METHOD={request_method} | "
            f"PATH={request_path} | "
            f"IP={request_ip} | "
            f"AGENT={user_agent}"
        )

        # ==============================================
        # PROCESS REQUEST
        # ==============================================

        try:

            response = self.get_response(
                request
            )

        except Exception as error:

            logger.exception(

                f"[REQUEST ERROR] "
                f"ID={request_id} | "
                f"ERROR={str(error)}"
            )

            raise error

        # ==============================================
        # EXECUTION TIME
        # ==============================================

        execution_time = round(

            time.time() - start_time,

            4
        )

        # ==============================================
        # RESPONSE STATUS
        # ==============================================

        status_code = getattr(

            response,

            "status_code",

            500
        )

        # ==============================================
        # PERFORMANCE LEVEL
        # ==============================================

        performance_level = (
            self.get_performance_level(
                execution_time
            )
        )

        # ==============================================
        # ATTACH RESPONSE HEADERS
        # ==============================================

        response[
            "X-Request-ID"
        ] = request_id

        response[
            "X-Execution-Time"
        ] = str(
            execution_time
        )

        response[
            "X-Performance-Level"
        ] = performance_level

        response[
            "X-API-Version"
        ] = getattr(

            settings,

            "API_VERSION",

            "v1"
        )

        # ==============================================
        # SLOW REQUEST WARNING
        # ==============================================

        if execution_time > 3:

            logger.warning(

                f"[SLOW REQUEST] "
                f"ID={request_id} | "
                f"TIME={execution_time}s | "
                f"PATH={request_path}"
            )

        # ==============================================
        # SAVE REQUEST LOG
        # ==============================================

        try:

            APIRequestLog.objects.create(

                request_id=request_id,

                method=request_method,

                path=request_path,

                status_code=status_code,

                execution_time=execution_time,

                ip_address=request_ip,

                user_agent=user_agent,
            )

        except Exception as error:

            logger.exception(

                f"[REQUEST LOG ERROR] "
                f"ID={request_id} | "
                f"ERROR={str(error)}"
            )

        # ==============================================
        # REQUEST END LOG
        # ==============================================

        logger.info(

            f"[REQUEST END] "
            f"ID={request_id} | "
            f"STATUS={status_code} | "
            f"TIME={execution_time}s | "
            f"PERFORMANCE={performance_level}"
        )

        return response

    # ==================================================
    # GET CLIENT IP
    # ==================================================

    def get_client_ip(
        self,
        request
    ):

        forwarded_for = (
            request.META.get(
                "HTTP_X_FORWARDED_FOR"
            )
        )

        if forwarded_for:

            ip = (
                forwarded_for
                .split(",")[0]
                .strip()
            )

        else:

            ip = request.META.get(

                "REMOTE_ADDR",

                "unknown"
            )

        return ip

    # ==================================================
    # PERFORMANCE LEVEL
    # ==================================================

    def get_performance_level(
        self,
        execution_time
    ):

        if execution_time < 0.5:

            return "excellent"

        if execution_time < 1.5:

            return "good"

        if execution_time < 3:

            return "average"

        return "slow"