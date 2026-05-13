"""
Content generation APIs.
"""

from rest_framework import status

from .base import (
    BaseAPIView,
    logger,
    AICOSException,
)

from apps.engine.schemas.request_schema import (
    GenerateContentRequestSerializer,
)

from apps.generator.tasks import (
    generate_article_task
)


class GenerateContentView(
    BaseAPIView
):

    # ==========================================
    # SWAGGER SUPPORT
    # ==========================================

    serializer_class = (
        GenerateContentRequestSerializer
    )

    def post(
        self,
        request,
    ):

        """
        Queue async AI content generation.
        """

        try:

            serializer = (
                self.serializer_class(
                    data=request.data
                )
            )

            # ==========================================
            # VALIDATION
            # ==========================================

            if not serializer.is_valid():

                logger.warning(

                    "Invalid content "
                    "generation request."
                )

                return self.validation_error_response(

                    serializer.errors
                )

            # ==========================================
            # SUPPORT BOTH query + keyword
            # ==========================================

            keyword = (
                serializer.validated_data.get(
                    "keyword"
                )
            )

            query = (
                serializer.validated_data.get(
                    "query"
                )
            )

            final_query = (
                query or keyword
            )

            if not final_query:

                return self.validation_error_response({

                    "query": [

                        "Query is required."
                    ]
                })

            logger.info(

                f"AI generation requested "
                f"for: {final_query}"
            )

            # ==========================================
            # CREATE TASK
            # ==========================================

            task = (
                generate_article_task.delay(

                    final_query
                )
            )

            # ==========================================
            # RESPONSE
            # ==========================================

            response_data = {

                "task_id": task.id,

                "status": "queued",

                "query": final_query,

                "task_status_url": (

                    f"/api/v1/generator/task/"
                    f"{task.id}/"
                ),
            }

            return self.success_response(

                data=response_data,

                message=(

                    "AI generation task "
                    "queued successfully."
                )
            )

        except AICOSException as error:

            logger.error(

                f"AI generation error: "
                f"{str(error)}"
            )

            return self.error_response(

                message=str(error),

                error_code=(
                    "GENERATION_ERROR"
                )
            )

        except Exception as error:

            logger.exception(

                "Unexpected generation "
                "API error."
            )

            return self.server_error_response(
                error
            )