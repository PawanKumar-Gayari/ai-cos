"""
Enterprise Celery Task Tracking API
-----------------------------------

Production-grade async task tracking API.

Features:
- live task tracking
- safe result serialization
- progress tracking
- execution metadata
- frontend-ready responses
- failure-safe formatting
- dashboard compatible
- production-safe logging
"""

from __future__ import annotations

import logging

from celery.result import (
    AsyncResult,
)

from rest_framework.views import (
    APIView,
)

from rest_framework.response import (
    Response,
)

from rest_framework import status

from drf_spectacular.utils import (
    extend_schema,
)


logger = logging.getLogger(
    __name__
)


# =========================================================
# TASK STATUS API
# =========================================================

class TaskStatusAPIView(
    APIView
):

    """
    Enterprise task tracking API.
    """

    serializer_class = None

    # =====================================================
    # SAFE RESULT
    # =====================================================

    @staticmethod
    def safe_result(
        result,
    ):

        """
        Safe JSON-compatible result serialization.
        """

        try:

            if result is None:

                return None

            if isinstance(
                result,
                BaseException,
            ):

                return {

                    "error": str(result),

                    "type": (
                        result.__class__.__name__
                    ),
                }

            if isinstance(
                result,
                (
                    str,
                    int,
                    float,
                    bool,
                    list,
                    dict,
                ),
            ):

                return result

            return str(result)

        except Exception as error:

            logger.exception(

                f"Result serialization failed: "
                f"{str(error)}"
            )

            return (
                "Result serialization failed."
            )

    # =====================================================
    # STATUS MESSAGE
    # =====================================================

    @staticmethod
    def status_message(
        task_status,
    ):

        """
        Human-readable task messages.
        """

        messages = {

            "PENDING":
            "Task is waiting in queue.",

            "RECEIVED":
            "Task received by worker.",

            "STARTED":
            "Task execution started.",

            "PROGRESS":
            "Content generation in progress.",

            "RETRY":
            "Task retry in progress.",

            "SUCCESS":
            "Task completed successfully.",

            "FAILURE":
            "Task execution failed.",

            "REVOKED":
            "Task was cancelled.",
        }

        return messages.get(

            task_status,

            "Unknown task state.",
        )

    # =====================================================
    # EXTRACT META
    # =====================================================

    @staticmethod
    def extract_meta(
        task_info,
    ):

        """
        Extract safe task metadata.
        """

        try:

            if isinstance(
                task_info,
                dict,
            ):

                safe_meta = {}

                for key, value in (
                    task_info.items()
                ):

                    try:

                        if isinstance(

                            value,

                            (
                                str,
                                int,
                                float,
                                bool,
                                list,
                                dict,
                            )
                        ):

                            safe_meta[key] = value

                        else:

                            safe_meta[key] = str(
                                value
                            )

                    except Exception:

                        safe_meta[key] = (
                            "Serialization failed"
                        )

                return safe_meta

            return {}

        except Exception as error:

            logger.exception(

                f"Meta extraction failed: "
                f"{str(error)}"
            )

            return {}

    # =====================================================
    # EXTRACT TRACEBACK
    # =====================================================

    @staticmethod
    def extract_traceback(
        task_result,
    ):

        """
        Safe traceback extraction.
        """

        try:

            traceback_data = getattr(

                task_result,

                "traceback",

                None,
            )

            if traceback_data:

                return str(
                    traceback_data
                )[:5000]

            return None

        except Exception as error:

            logger.exception(

                f"Traceback extraction failed: "
                f"{str(error)}"
            )

            return None

    # =====================================================
    # BUILD RESPONSE
    # =====================================================

    def build_response(
        self,
        task_result,
        task_id,
    ):

        """
        Build standardized API response.
        """

        task_status = (
            task_result.status
        )

        response = {

            "success": True,

            "task_id": task_id,

            "status": task_status,

            "message": (

                self.status_message(
                    task_status
                )
            ),

            "successful": False,

            "failed": False,

            "ready": False,

            "traceback": None,

            "result": None,

            "meta": {},
        }

        # =============================================
        # SAFE TASK FLAGS
        # =============================================

        try:

            response["successful"] = (
                task_result.successful()
            )

        except Exception:

            response["successful"] = False

        try:

            response["failed"] = (
                task_result.failed()
            )

        except Exception:

            response["failed"] = False

        try:

            response["ready"] = (
                task_result.ready()
            )

        except Exception:

            response["ready"] = False

        # =============================================
        # TASK META
        # =============================================

        try:

            response["meta"] = (

                self.extract_meta(
                    task_result.info
                )
            )

        except Exception:

            logger.exception(
                "Task meta extraction failed."
            )

        # =============================================
        # FAILURE HANDLING
        # =============================================

        if task_status == "FAILURE":

            response["success"] = False

            try:

                result_data = (
                    task_result.result
                )

                if isinstance(
                    result_data,
                    BaseException,
                ):

                    response["error"] = str(
                        result_data
                    )

                    response["exception_type"] = (
                        result_data.__class__.__name__
                    )

                else:

                    response["error"] = str(
                        result_data
                    )

            except Exception as error:

                response["error"] = str(
                    error
                )

            response["traceback"] = (

                self.extract_traceback(
                    task_result
                )
            )

        # =============================================
        # SUCCESS RESULT
        # =============================================

        elif task_result.ready():

            try:

                response["result"] = (

                    self.safe_result(
                        task_result.result
                    )
                )

            except Exception as error:

                logger.exception(

                    f"Task result extraction "
                    f"failed: {str(error)}"
                )

                response["result"] = str(
                    error
                )

        return response

    # =====================================================
    # GET
    # =====================================================

    @extend_schema(
        tags=["AI Tasks"]
    )
    def get(
        self,
        request,
        task_id,
    ):

        """
        Retrieve async task status.
        """

        logger.info(

            f"Task status requested | "
            f"task_id={task_id}"
        )

        try:

            task_result = (
                AsyncResult(task_id)
            )

            response = (
                self.build_response(
                    task_result=task_result,
                    task_id=task_id,
                )
            )

            return Response(

                response,

                status=status.HTTP_200_OK,
            )

        except Exception as error:

            logger.exception(

                f"Task status API failed | "
                f"task_id={task_id} | "
                f"error={str(error)}"
            )

            return Response(

                {

                    "success": False,

                    "task_id": task_id,

                    "status": "ERROR",

                    "message": (
                        "Task status retrieval "
                        "failed."
                    ),

                    "error": str(error),
                },

                status=(
                    status.HTTP_500_INTERNAL_SERVER_ERROR
                ),
            )