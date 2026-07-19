"""
Competitor API serializers.
"""

from rest_framework import serializers


class CompetitorRequestSerializer(
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

    competitor_limit = (
        serializers.IntegerField(

            required=False,

            default=10,

            min_value=1,

            max_value=50
        )
    )

    include_serp = (
        serializers.BooleanField(

            required=False,

            default=True
        )
    )

    include_gaps = (
        serializers.BooleanField(

            required=False,

            default=True
        )
    )

    include_weaknesses = (
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

        value = (
            value
            .strip()
        )

        if len(value) < 3:

            raise serializers.ValidationError(

                "Keyword is too short."
            )

        return value