"""
Enterprise SEO Intelligence Views
---------------------------------

Production-grade SEO keyword APIs.

Features:
- enterprise validation
- SEO intelligence orchestration
- semantic keyword analytics
- structured keyword responses
- secure API architecture
- async-safe responses
- production-safe logging
"""

from __future__ import annotations

import logging
import time

from rest_framework import status

from rest_framework.permissions import (
    AllowAny,
)

from rest_framework.response import (
    Response,
)

from rest_framework.views import (
    APIView,
)

from apps.keywords.engine import (
    KeywordEngine,
)

from apps.keywords.exceptions import (
    KeywordEngineException,
)

from apps.keywords.serializers import (

    KeywordAnalyzeSerializer,

    KeywordExpandSerializer,
)


logger = logging.getLogger(
    __name__
)


# =========================================================
# BASE VIEW
# =========================================================

class BaseKeywordAPIView(
    APIView
):

    """
    Enterprise keyword API base view.
    """

    authentication_classes = []

    permission_classes = [
        AllowAny,
    ]

    engine = KeywordEngine()

    # =====================================================
    # SUCCESS RESPONSE
    # =====================================================

    def success_response(

        self,

        *,

        message,

        data,

        status_code=200,
    ):

        return Response(

            {

                "success": True,

                "message": message,

                "data": data,
            },

            status=status_code,
        )

    # =====================================================
    # ERROR RESPONSE
    # =====================================================

    def error_response(

        self,

        *,

        message,

        error_code,

        status_code,

        details=None,
    ):

        return Response(

            {

                "success": False,

                "error": {

                    "message":
                    message,

                    "error_code":
                    error_code,

                    "details":
                    details or {},
                },
            },

            status=status_code,
        )

    # =====================================================
    # SAFE LOG
    # =====================================================

    def safe_log(
        self,
        message,
    ):

        logger.info(
            str(message)[:1000]
        )


# =========================================================
# KEYWORD ANALYZE API
# =========================================================

class KeywordAnalyzeAPIView(
    BaseKeywordAPIView
):

    """
    Enterprise keyword SEO analysis.
    """

    def post(
        self,
        request,
    ):

        started = time.time()

        serializer = (
            KeywordAnalyzeSerializer(
                data=request.data
            )
        )

        # =================================================
        # VALIDATION
        # =================================================

        if not serializer.is_valid():

            return self.error_response(

                message=(
                    "Validation failed."
                ),

                error_code=(
                    "VALIDATION_ERROR"
                ),

                status_code=(
                    status.HTTP_400_BAD_REQUEST
                ),

                details=serializer.errors,
            )

        try:

            keyword = (
                serializer.validated_data[
                    "keyword"
                ]
            )

            self.safe_log(

                f"KEYWORD ANALYZE: "
                f"{keyword}"
            )

            # =============================================
            # FULL ANALYSIS
            # =============================================

            analysis = (

                self.engine.analyze_keyword(
                    keyword
                )
            )

            execution_time = round(

                time.time()
                - started,

                3,
            )

            response_data = {

                "keyword":
                keyword,

                "execution_time":
                execution_time,

                "analysis":
                analysis,

                "semantic_keywords": (

                    analysis.get(
                        "suggestions",
                        []
                    )
                ),

                "best_keywords": (

                    analysis.get(
                        "best_keywords",
                        []
                    )
                ),

                "total_keywords": (

                    analysis.get(
                        "total_keywords",
                        0,
                    )
                ),
            }

            return self.success_response(

                message=(
                    "Keyword analyzed successfully."
                ),

                data=response_data,
            )

        except KeywordEngineException as exc:

            logger.warning(
                "Keyword engine failure."
            )

            return Response(

                exc.to_dict(),

                status=exc.status_code,
            )

        except Exception as error:

            logger.exception(
                "Keyword analysis failed."
            )

            return self.error_response(

                message=(
                    "Internal server error."
                ),

                error_code=(
                    "INTERNAL_SERVER_ERROR"
                ),

                status_code=500,

                details={

                    "reason":
                    str(error)
                },
            )


# =========================================================
# KEYWORD EXPANSION API
# =========================================================

class KeywordExpandAPIView(
    BaseKeywordAPIView
):

    """
    Enterprise semantic expansion API.
    """

    def post(
        self,
        request,
    ):

        started = time.time()

        serializer = (
            KeywordExpandSerializer(
                data=request.data
            )
        )

        # =================================================
        # VALIDATION
        # =================================================

        if not serializer.is_valid():

            return self.error_response(

                message=(
                    "Validation failed."
                ),

                error_code=(
                    "VALIDATION_ERROR"
                ),

                status_code=(
                    status.HTTP_400_BAD_REQUEST
                ),

                details=serializer.errors,
            )

        try:

            topic = (
                serializer.validated_data[
                    "topic"
                ]
            )

            limit = (
                serializer.validated_data.get(
                    "limit",
                    10,
                )
            )

            self.safe_log(

                f"KEYWORD EXPANSION: "
                f"{topic}"
            )

            keywords = (

                self.engine.expand_keywords(
                    topic
                )
            )

            keywords = keywords[:limit]

            execution_time = round(

                time.time()
                - started,

                3,
            )

            return self.success_response(

                message=(
                    "Keywords expanded successfully."
                ),

                data={

                    "topic":
                    topic,

                    "count":
                    len(keywords),

                    "execution_time":
                    execution_time,

                    "results":
                    keywords,
                },
            )

        except KeywordEngineException as exc:

            logger.warning(
                "Keyword expansion failure."
            )

            return Response(

                exc.to_dict(),

                status=exc.status_code,
            )

        except Exception as error:

            logger.exception(
                "Expansion failed."
            )

            return self.error_response(

                message=(
                    "Internal server error."
                ),

                error_code=(
                    "INTERNAL_SERVER_ERROR"
                ),

                status_code=500,

                details={

                    "reason":
                    str(error)
                },
            )


# =========================================================
# BEST KEYWORDS API
# =========================================================

class BestKeywordsAPIView(
    BaseKeywordAPIView
):

    """
    Enterprise best keyword selector.
    """

    def post(
        self,
        request,
    ):

        started = time.time()

        serializer = (
            KeywordExpandSerializer(
                data=request.data
            )
        )

        # =================================================
        # VALIDATION
        # =================================================

        if not serializer.is_valid():

            return self.error_response(

                message=(
                    "Validation failed."
                ),

                error_code=(
                    "VALIDATION_ERROR"
                ),

                status_code=(
                    status.HTTP_400_BAD_REQUEST
                ),

                details=serializer.errors,
            )

        try:

            topic = (
                serializer.validated_data[
                    "topic"
                ]
            )

            limit = (
                serializer.validated_data.get(
                    "limit",
                    10,
                )
            )

            self.safe_log(

                f"BEST KEYWORDS: "
                f"{topic}"
            )

            keywords = (

                self.engine.best_keywords(

                    topic=topic,

                    limit=limit,
                )
            )

            execution_time = round(

                time.time()
                - started,

                3,
            )

            response_data = {

                "topic":
                topic,

                "count":
                len(keywords),

                "execution_time":
                execution_time,

                "results":
                keywords,

                "top_keyword": (

                    keywords[0]

                    if keywords

                    else {}
                ),
            }

            return self.success_response(

                message=(
                    "Best keywords generated successfully."
                ),

                data=response_data,
            )

        except KeywordEngineException as exc:

            logger.warning(
                "Best keyword failure."
            )

            return Response(

                exc.to_dict(),

                status=exc.status_code,
            )

        except Exception as error:

            logger.exception(
                "Best keyword generation failed."
            )

            return self.error_response(

                message=(
                    "Internal server error."
                ),

                error_code=(
                    "INTERNAL_SERVER_ERROR"
                ),

                status_code=500,

                details={

                    "reason":
                    str(error)
                },
            )


# =========================================================
# HEALTH CHECK API
# =========================================================

class KeywordHealthAPIView(
    APIView
):

    """
    Enterprise keyword engine health API.
    """

    authentication_classes = []

    permission_classes = []

    def get(
        self,
        request,
    ):

        return Response(

            {

                "success": True,

                "service": (
                    "SEO Intelligence Engine"
                ),

                "status": "healthy",

                "version": "6.0.0",

                "features": [

                    "semantic_keywords",

                    "intent_detection",

                    "seo_scoring",

                    "keyword_clustering",

                    "content_optimization",

                    "density_analysis",
                ],
            },

            status=status.HTTP_200_OK,
        )