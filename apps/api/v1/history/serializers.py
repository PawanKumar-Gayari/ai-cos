from rest_framework import serializers

from apps.history.models import (
    GenerationHistory
)


class GenerationHistorySerializer(
    serializers.ModelSerializer
):

    class Meta:

        model = (
            GenerationHistory
        )

        fields = "__all__"