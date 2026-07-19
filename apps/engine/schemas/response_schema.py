"""
Response schemas for AI COS engine.
"""

from rest_framework import serializers


class GenerateContentResponseSerializer(
    serializers.Serializer
):

    status = serializers.CharField()

    current_step = serializers.CharField()

    data = serializers.DictField()

    errors = serializers.ListField()