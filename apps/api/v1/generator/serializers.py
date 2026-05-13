"""
Generator API serializers.
"""

from rest_framework import serializers


class GenerateArticleSerializer(
    serializers.Serializer
):

    query = serializers.CharField(

        max_length=5000,
    )

    session_id = serializers.CharField(

        required=False,

        allow_blank=True,
    )


class GenerateOutlineSerializer(
    serializers.Serializer
):

    topic = serializers.CharField(

        max_length=3000,
    )

    session_id = serializers.CharField(

        required=False,

        allow_blank=True,
    )


class GenerateKeywordsSerializer(
    serializers.Serializer
):

    topic = serializers.CharField(

        max_length=3000,
    )

    session_id = serializers.CharField(

        required=False,

        allow_blank=True,
    )


class TaskQueuedSerializer(
    serializers.Serializer
):

    success = serializers.BooleanField()

    task_id = serializers.CharField()

    status = serializers.CharField()


class ErrorSerializer(
    serializers.Serializer
):

    error = serializers.CharField()