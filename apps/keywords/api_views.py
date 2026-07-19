"""
Production Keywords API Views
-----------------------------

Enterprise-grade SEO intelligence APIs.

Features:
- middleware-based API security
- stable API responses
- production-safe validation
- centralized error handling
- structured logging
- scalable architecture
- Swagger/OpenAPI support
- OCI optimized
"""

from __future__ import annotations

import logging

from drf_spectacular.utils import (

    OpenApiExample,

    OpenApiResponse,

    extend_schema,
)

from rest_framework import serializers
from rest_framework import status

from rest_framework.decorators import (

    api_view,

    permission_classes,

    authentication_classes,
)

from rest_framework.response import (
    Response,
)

from apps.keywords.services.pipeline_service import (
    KeywordPipelineService,
)


logger = logging.getLogger(__name__)


# =====================================================
# REQUEST SERIALIZER
# =====================================================

class KeywordAnalyzeSerializer(
    serializers.Serializer
):

    keyword = serializers.CharField(

        required=True,

        min_length=2,

        max_length=200,

        trim_whitespace=True,

        help_text="Keyword to analyze",
    )


# =====================================================
# SUCCESS RESPONSE
# =====================================================

def success_response(
    data: dict,
    status_code: int = 200,
) -> Response:

    return Response(

        {

            "success": True,

            "data": data,
        },

        status=status_code,
    )


# =====================================================
# ERROR RESPONSE
# =====================================================

def error_response(
    message: str,
    status_code: int = 400,
    errors: dict | None = None,
) -> Response:

    payload = {

        "success": False,

        "message": message,
    }

    if errors:

        payload["errors"] = errors

    return Response(

        payload,

        status=status_code,
    )


# =====================================================
# SAFE RESPONSE DATA
# =====================================================

def safe_response_data(
    data: dict | None,
) -> dict:

    if not isinstance(
        data,
        dict,
    ):

        return {}

    defaults = {

        "keyword": "",

        "keyword_id": None,

        "suggestions": [],

        "serp_results": [],

        "difficulty": {},

        "recommendations": {},

        "outline": {},

        "clusters": {},
    }

    for key, value in (
        defaults.items()
    ):

        data.setdefault(
            key,
            value,
        )

    return data


# =====================================================
# API DOCUMENTATION
# =====================================================

@extend_schema(

    tags=[
        "keywords",
    ],

    request=KeywordAnalyzeSerializer,

    responses={

        200: OpenApiResponse(
            description=(
                "Keyword analyzed successfully."
            )
        ),

        400: OpenApiResponse(
            description="Validation error."
        ),

        403: OpenApiResponse(
            description="Invalid API key."
        ),

        500: OpenApiResponse(
            description="Internal server error."
        ),
    },

    examples=[

        OpenApiExample(

            "SEO Keyword",

            value={

                "keyword":
                "best seo tools",
            },

            request_only=True,
        ),

        OpenApiExample(

            "Government Exam Keyword",

            value={

                "keyword":

                "Rajasthan Lab Assistant exam pyq",
            },

            request_only=True,
        ),
    ],
)

# =====================================================
# ANALYZE API
# =====================================================

@api_view([
    "POST",
])

@authentication_classes([])

@permission_classes([])

def analyze_keyword_api(
    request,
):

    """
    Run complete SEO intelligence pipeline.
    """

    try:

        # =========================================
        # VALIDATION
        # =========================================

        serializer = (

            KeywordAnalyzeSerializer(

                data=request.data
            )
        )

        if not serializer.is_valid():

            logger.warning(
                "Keyword validation failed."
            )

            return error_response(

                message=(
                    "Validation failed."
                ),

                errors=serializer.errors,

                status_code=(
                    status.HTTP_400_BAD_REQUEST
                ),
            )

        keyword = (

            serializer
            .validated_data[
                "keyword"
            ]
            .strip()
        )

        # =========================================
        # LOG START
        # =========================================

        logger.info(

            f"Keyword analysis started: "
            f"{keyword}"
        )

        # =========================================
        # PIPELINE
        # =========================================

        pipeline = (
            KeywordPipelineService()
        )

        result = pipeline.run(
            keyword
        )

        # =========================================
        # SAFE RESPONSE
        # =========================================

        result = safe_response_data(
            result
        )

        # =========================================
        # LOG SUCCESS
        # =========================================

        logger.info(

            f"Keyword analysis completed: "
            f"{keyword}"
        )

        logger.info(

            f"SERP results: "
            f"{len(result.get('serp_results', []))}"
        )

        # =========================================
        # SUCCESS
        # =========================================

        return success_response(

            data=result,

            status_code=(
                status.HTTP_200_OK
            ),
        )

    # =============================================
    # FAILURE
    # =============================================

    except Exception as error:

        logger.exception(
            "Keyword API failed."
        )

        return error_response(

            message=(
                "Internal server error."
            ),

            errors={

                "detail":
                str(error),
            },

            status_code=(
                status.HTTP_500_INTERNAL_SERVER_ERROR
            ),
        )