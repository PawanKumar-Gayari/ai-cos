from rest_framework.generics import (

    ListAPIView,

    RetrieveAPIView,
)

from drf_spectacular.utils import (
    extend_schema,
)

from apps.history.models import (
    GenerationHistory
)

from apps.api.v1.history.serializers import (
    GenerationHistorySerializer
)


@extend_schema(
    tags=["AI History"]
)
class GenerationHistoryListAPIView(
    ListAPIView
):

    serializer_class = (
        GenerationHistorySerializer
    )

    queryset = (
        GenerationHistory.objects.all()
    )


@extend_schema(
    tags=["AI History"]
)
class GenerationHistoryDetailAPIView(
    RetrieveAPIView
):

    serializer_class = (
        GenerationHistorySerializer
    )

    queryset = (
        GenerationHistory.objects.all()
    )

    lookup_field = "id"