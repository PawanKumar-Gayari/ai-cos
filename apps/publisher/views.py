"""
Enterprise Publisher Views
--------------------------

Secure and optimized publisher system.

Features:
- protected dashboard
- admin-only APIs
- public health endpoint
- provider controls
- article generation
- publish workflow
- clean architecture
- production logging
"""

from __future__ import annotations

import logging

from django.shortcuts import (
    redirect,
    render,
)

from django.contrib.auth.decorators import (
    login_required,
)

from rest_framework import status

from rest_framework.authentication import (
    SessionAuthentication,
)

from rest_framework.permissions import (

    AllowAny,

    IsAdminUser,
)

from rest_framework.response import (
    Response,
)

from rest_framework.views import (
    APIView,
)

from apps.dashboard.services.feature_service import (
    FeatureService,
)

from apps.engine.models import (
    Article,
)

from apps.publisher.engine import (
    PublisherEngine,
)

from apps.publisher.serializers import (

    GenerateArticleRequestSerializer,

    PublishArticleRequestSerializer,
)


logger = logging.getLogger(
    __name__
)


# =========================================================
# HELPERS
# =========================================================

def calculate_word_count(
    content,
):

    return len(
        str(content or "").split()
    )


def active_provider():

    if FeatureService.is_enabled(
        "gemini_enabled",
        default=False,
    ):

        return "Gemini"

    if FeatureService.is_enabled(
        "openai_enabled",
        default=False,
    ):

        return "OpenAI"

    return "Ollama"


# =========================================================
# DASHBOARD VIEW
# =========================================================

@login_required(
    login_url="/login/"
)
def publisher_dashboard(
    request,
):

    if not request.user.is_staff:

        return redirect(
            "/login/"
        )

    logger.info(
        "Publisher dashboard opened."
    )

    # =====================================================
    # RECENT ARTICLES
    # =====================================================

    recent_articles = []

    try:

        articles = (

            Article.objects
            .only(

                "title",

                "content",

                "seo_score",

                "ai_provider",

                "is_published",
            )
            .order_by(
                "-created_at"
            )[:10]
        )

        for article in articles:

            recent_articles.append({

                "keyword": (

                    article.title
                    or
                    "Untitled"
                ),

                "provider": (

                    article.ai_provider
                    or
                    "Unknown"
                ),

                "word_count": (

                    calculate_word_count(
                        article.content
                    )
                ),

                "seo_score": (
                    article.seo_score
                    or
                    0
                ),

                "status": (

                    "Published"

                    if article.is_published

                    else

                    "Draft"
                ),
            })

    except Exception as error:

        logger.exception(

            f"Article load failed: "
            f"{str(error)}"
        )

    # =====================================================
    # STATS
    # =====================================================

    try:

        total_generated = (
            Article.objects.count()
        )

        total_published = (

            Article.objects.filter(
                is_published=True
            ).count()
        )

    except Exception as error:

        logger.warning(

            f"Stats failed: "
            f"{str(error)}"
        )

        total_generated = 0

        total_published = 0

    stats = {

        "total_generated":
            total_generated,

        "total_published":
            total_published,

        "active_provider":
            active_provider(),

        "queue_status":
            "Healthy",
    }

    # =====================================================
    # CONTEXT
    # =====================================================

    context = {

        "page_title":
            "Publisher",

        "stats":
            stats,

        "generate_url":
            "/api/publisher/generate/",

        "drafts_url":
            "/dashboard/",

        "articles_url":
            "/dashboard/",

        # ================================================
        # LANGUAGES
        # ================================================

        "supported_languages": [

            {
                "value": "english",
                "label": "English",
                "selected": True,
            },

            {
                "value": "hindi",
                "label": "Hindi",
                "selected": False,
            },

            {
                "value": "hinglish",
                "label": "Hinglish",
                "selected": False,
            },
        ],

        # ================================================
        # PROVIDERS
        # ================================================

        "providers": [

            {
                "value": "auto",
                "label": "Auto Routing",
                "selected": True,
            },

            {
                "value": "gemini",
                "label": "Gemini",
                "selected": False,
            },

            {
                "value": "openai",
                "label": "OpenAI",
                "selected": False,
            },

            {
                "value": "ollama",
                "label": "Ollama",
                "selected": False,
            },
        ],

        # ================================================
        # PROVIDER STATUS
        # ================================================

        "provider_status": [

            {
                "name": "Gemini",

                "description":
                    "Primary",

                "enabled": (

                    FeatureService.is_enabled(
                        "gemini_enabled",
                        default=False,
                    )
                ),
            },

            {
                "name": "OpenAI",

                "description":
                    "Secondary",

                "enabled": (

                    FeatureService.is_enabled(
                        "openai_enabled",
                        default=False,
                    )
                ),
            },

            {
                "name": "Ollama",

                "description":
                    "Fallback",

                "enabled": (

                    FeatureService.is_enabled(
                        "ollama_enabled",
                        default=True,
                    )
                ),
            },
        ],

        # ================================================
        # ARTICLES
        # ================================================

        "recent_articles":
            recent_articles,

        # ================================================
        # FORM
        # ================================================

        "form": {

            "keyword": "",

            "instructions": "",
        },
    }

    return render(

        request,

        "publisher/dashboard.html",

        context,
    )


# =========================================================
# BASE API VIEW
# =========================================================

class BaseAPIView(
    APIView
):

    permission_classes = [
        IsAdminUser
    ]

    authentication_classes = [
        SessionAuthentication
    ]

    def success_response(
        self,
        data=None,
        message="Success",
        status_code=(
            status.HTTP_200_OK
        ),
    ):

        return Response(

            {
                "success": True,

                "message": message,

                "data": data,
            },

            status=status_code,
        )

    def error_response(
        self,
        error,
        status_code=(
            status.HTTP_400_BAD_REQUEST
        ),
    ):

        logger.warning(
            f"API Error: {str(error)}"
        )

        return Response(

            {
                "success": False,

                "error": str(error),
            },

            status=status_code,
        )


# =========================================================
# PUBLIC HEALTH API
# =========================================================

class HealthAPIView(
    APIView
):

    permission_classes = [
        AllowAny
    ]

    authentication_classes = []

    def success_response(
        self,
        data=None,
        message="Success",
        status_code=(
            status.HTTP_200_OK
        ),
    ):

        return Response(

            {
                "success": True,

                "message": message,

                "data": data,
            },

            status=status_code,
        )

    def error_response(
        self,
        error,
        status_code=(
            status.HTTP_400_BAD_REQUEST
        ),
    ):

        logger.warning(
            f"Health API Error: {str(error)}"
        )

        return Response(

            {
                "success": False,

                "error": str(error),
            },

            status=status_code,
        )

    def get(
        self,
        request,
    ):

        try:

            logger.info(
                "Public health check requested."
            )

            engine = (
                PublisherEngine()
            )

            result = (
                engine.health_check()
            )

            return self.success_response(

                data=result,

                message=(
                    "Healthy"
                ),
            )

        except Exception as error:

            logger.exception(

                f"Health failed: "
                f"{str(error)}"
            )

            return self.error_response(

                error,

                status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


# =========================================================
# GENERATE ARTICLE
# =========================================================

class GenerateArticleAPIView(
    BaseAPIView
):

    def post(
        self,
        request,
    ):

        serializer = (

            GenerateArticleRequestSerializer(
                data=request.data
            )
        )

        if not serializer.is_valid():

            return self.error_response(

                serializer.errors,

                status.HTTP_400_BAD_REQUEST,
            )

        try:

            topic = serializer.validated_data.get(
                "topic"
            )

            logger.info(

                f"Generate request: "
                f"{topic}"
            )

            engine = (
                PublisherEngine()
            )

            result = (

                engine.generate_and_publish(
                    topic=topic
                )
            )

            return self.success_response(

                data=result,

                message=(
                    "Article generated."
                ),
            )

        except Exception as error:

            logger.exception(

                f"Generation failed: "
                f"{str(error)}"
            )

            return self.error_response(

                error,

                status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


# =========================================================
# PUBLISH ARTICLE
# =========================================================

class PublishArticleAPIView(
    BaseAPIView
):

    def post(
        self,
        request,
    ):

        serializer = (

            PublishArticleRequestSerializer(
                data=request.data
            )
        )

        if not serializer.is_valid():

            return self.error_response(

                serializer.errors,

                status.HTTP_400_BAD_REQUEST,
            )

        try:

            article_id = (

                serializer.validated_data.get(
                    "article_id"
                )
            )

            logger.info(

                f"Publish request: "
                f"{article_id}"
            )

            article = (
                Article.objects.get(
                    id=article_id
                )
            )

            engine = (
                PublisherEngine()
            )

            result = (

                engine.publish_article(
                    article_id=article.id
                )
            )

            return self.success_response(

                data=result,

                message=(
                    "Article published."
                ),
            )

        except Article.DoesNotExist:

            return self.error_response(

                "Article not found.",

                status.HTTP_404_NOT_FOUND,
            )

        except Exception as error:

            logger.exception(

                f"Publish failed: "
                f"{str(error)}"
            )

            return self.error_response(

                error,

                status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


# =========================================================
# TOGGLE FEATURE
# =========================================================

class ToggleFeatureAPIView(
    BaseAPIView
):

    def post(
        self,
        request,
    ):

        try:

            feature = request.data.get(
                "feature"
            )

            enabled = request.data.get(
                "enabled"
            )

            if not feature:

                return self.error_response(
                    "Feature required."
                )

            FeatureService.set_feature(

                feature,

                bool(enabled),
            )

            logger.info(

                f"Feature updated | "
                f"{feature}={enabled}"
            )

            return self.success_response(

                data={

                    "feature": feature,

                    "enabled": enabled,
                },

                message=(
                    "Feature updated."
                ),
            )

        except Exception as error:

            logger.exception(

                f"Toggle failed: "
                f"{str(error)}"
            )

            return self.error_response(

                error,

                status.HTTP_500_INTERNAL_SERVER_ERROR,
            )