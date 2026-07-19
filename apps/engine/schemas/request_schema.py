"""
Request schemas for AI COS engine.
"""

from rest_framework import serializers


class GenerateContentRequestSerializer(
    serializers.Serializer
):

    keyword = serializers.CharField(
        max_length=255
    )