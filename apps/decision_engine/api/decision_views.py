"""
Decision engine API views.
"""

import logging

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

from apps.decision_engine.api.serializers import (
    DecisionRequestSerializer,
)

from apps.decision_engine.decision import (
    DecisionEngine,
)


logger = logging.getLogger(
    __name__
)


class DecisionAPIView(
    APIView
):

    """
    Main decision engine API.
    """

    @extend_schema(

        tags=["Decision Engine"],

        request=(
            DecisionRequestSerializer
        ),
    )
    def post(
        self,
        request,
    ):

        serializer = (
            DecisionRequestSerializer(
                data=request.data
            )
        )

        serializer.is_valid(
            raise_exception=True
        )

        keyword = (
            serializer.validated_data[
                "keyword"
            ]
        )

        try:

            engine = (
                DecisionEngine()
            )

            result = (
                engine.execute(

                    {
                        "keyword": keyword
                    }
                )
            )

            return Response(

                {

                    "success": True,

                    "data": result,
                },

                status=(
                    status.HTTP_200_OK
                ),
            )

        except Exception as error:

            logger.exception(

                f"Decision API failed: "
                f"{str(error)}"
            )

            return Response(

                {

                    "success": False,

                    "error": str(error),
                },

                status=(

                    status.HTTP_500_INTERNAL_SERVER_ERROR
                ),
            )