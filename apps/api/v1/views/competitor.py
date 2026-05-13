"""
Competitor APIs.
"""

from .base import (
    BaseAPIView,
    logger,
    AICOSException,
)

from apps.api.v1.serializers.competitor_serializer import (
    CompetitorRequestSerializer,
)

from apps.competitor.engine import (
    CompetitorEngine,
)


class CompetitorView(BaseAPIView):

    def post(
        self,
        request
    ):

        try:

            serializer = (
                CompetitorRequestSerializer(
                    data=request.data
                )
            )

            if not serializer.is_valid():

                return self.validation_error_response(
                    serializer.errors
                )

            keyword = (
                serializer.validated_data[
                    "keyword"
                ]
            )

            include_serp = (
                serializer.validated_data[
                    "include_serp"
                ]
            )

            include_gaps = (
                serializer.validated_data[
                    "include_gaps"
                ]
            )

            include_weaknesses = (
                serializer.validated_data[
                    "include_weaknesses"
                ]
            )

            logger.info(

                f"Competitor analysis "
                f"requested for: {keyword}"
            )

            competitor_engine = (
                CompetitorEngine()
            )

            result = (
                competitor_engine.analyze(

                    keyword=keyword,

                    include_serp=(
                        include_serp
                    ),

                    include_gaps=(
                        include_gaps
                    ),

                    include_weaknesses=(
                        include_weaknesses
                    )
                )
            )

            return self.success_response(

                data=result,

                message=(
                    "Competitor analysis "
                    "completed successfully."
                )
            )

        except AICOSException as error:

            return self.error_response(

                message=str(error),

                error_code=(
                    "COMPETITOR_ERROR"
                )
            )

        except Exception as error:

            return self.server_error_response(
                error
            )