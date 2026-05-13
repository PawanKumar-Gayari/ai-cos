"""
Celery task tracking API.
"""

from celery.result import (
    AsyncResult
)

from rest_framework.views import (
    APIView
)

from rest_framework.response import (
    Response
)

from rest_framework import status

from drf_spectacular.utils import (
    extend_schema,
)


class TaskStatusAPIView(
    APIView
):

    # ==========================================
    # SWAGGER FIX
    # ==========================================

    serializer_class = None

    @extend_schema(
        tags=["AI Tasks"]
    )
    def get(
        self,
        request,
        task_id,
    ):

        """
        Retrieve Celery task status.
        """

        task_result = (
            AsyncResult(task_id)
        )

        task_status = (
            task_result.status
        )

        response = {

            "task_id": task_id,

            "status": task_status,

            "successful": (
                task_result.successful()
            ),

            "failed": (
                task_result.failed()
            ),

            "ready": (
                task_result.ready()
            ),
        }

        # ==========================================
        # TASK STATES
        # ==========================================

        if task_status == "PENDING":

            response["message"] = (
                "Task is waiting "
                "in queue."
            )

        elif task_status == "STARTED":

            response["message"] = (
                "Task execution started."
            )

        elif task_status == "RETRY":

            response["message"] = (
                "Task retry in progress."
            )

        elif task_status == "SUCCESS":

            response["message"] = (
                "Task completed successfully."
            )

        elif task_status == "FAILURE":

            response["message"] = (
                "Task execution failed."
            )

        # ==========================================
        # RESULT
        # ==========================================

        if task_result.ready():

            try:

                result = (
                    task_result.result
                )

                # ----------------------------------
                # SAFE SERIALIZATION
                # ----------------------------------

                if isinstance(
                    result,
                    Exception,
                ):

                    response["result"] = str(
                        result
                    )

                else:

                    response["result"] = (
                        result
                    )

            except Exception as error:

                response["result_error"] = str(
                    error
                )

        return Response(

            response,

            status=status.HTTP_200_OK,
        )