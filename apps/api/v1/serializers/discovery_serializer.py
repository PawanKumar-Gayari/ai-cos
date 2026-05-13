"""
Discovery API serializers.
"""

from rest_framework import serializers


class DiscoveryRequestSerializer(
    serializers.Serializer
):

    # =========================
    # REQUIRED INPUT
    # =========================

    keyword = serializers.CharField(

        max_length=255,

        required=True
    )

    # =========================
    # OPTIONAL SETTINGS
    # =========================

    limit = serializers.IntegerField(

        required=False,

        default=10,

        min_value=1,

        max_value=100
    )

    include_trends = (
        serializers.BooleanField(

            required=False,

            default=True
        )
    )

    include_clusters = (
        serializers.BooleanField(

            required=False,

            default=True
        )
    )

    # =========================
    # VALIDATE KEYWORD
    # =========================

    def validate_keyword(
        self,
        value
    ):

        value = value.strip()

        if len(value) < 3:

            raise serializers.ValidationError(

                "Keyword is too short."
            )

        return value