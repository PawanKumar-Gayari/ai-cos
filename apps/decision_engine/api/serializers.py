from rest_framework import serializers


class DecisionRequestSerializer(
    serializers.Serializer
):

    keyword = serializers.CharField(
        max_length=255
    )


class DecisionResponseSerializer(
    serializers.Serializer
):

    success = serializers.BooleanField()

    keyword = serializers.CharField()

    decision = serializers.DictField()

    planning = serializers.DictField()