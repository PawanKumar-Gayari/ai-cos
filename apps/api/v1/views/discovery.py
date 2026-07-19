"""
Discovery APIs.
"""

from .base import (
    BaseAPIView,
    logger,
    AICOSException,
)

from apps.api.v1.serializers.discovery_serializer import (
    DiscoveryRequestSerializer,
)

from apps.discovery.engine import (
    DiscoveryEngine,
)


class DiscoveryView(BaseAPIView):

    def post(
        self,
        request
    ):

        try:

            serializer = (
                DiscoveryRequestSerializer(
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

            limit = (
                serializer.validated_data[
                    "limit"
                ]
            )

            include_trends = (
                serializer.validated_data[
                    "include_trends"
                ]
            )

            include_clusters = (
                serializer.validated_data[
                    "include_clusters"
                ]
            )

            logger.info(

                f"Discovery requested "
                f"for keyword: {keyword}"
            )

            discovery_engine = (
                DiscoveryEngine()
            )

            result = (
                discovery_engine.discover(
                    keyword
                )
            )

            if not include_trends:

                result.pop(
                    "trends",
                    None
                )

            if not include_clusters:

                result.pop(
                    "clusters",
                    None
                )

            result[
                "top_opportunities"
            ] = result[
                "top_opportunities"
            ][:limit]

            return self.success_response(

                data=result,

                message=(
                    "Keyword opportunities "
                    "generated successfully."
                )
            )

        except AICOSException as error:

            return self.error_response(

                message=str(error),

                error_code=(
                    "DISCOVERY_ERROR"
                )
            )

        except Exception as error:

            return self.server_error_response(
                error
            )