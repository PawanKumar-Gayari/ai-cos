"""
API v1 views for AI COS platform.
"""

from rest_framework import status

from rest_framework.response import (
    Response,
)

from rest_framework.views import (
    APIView,
)

from apps.api.v1.serializers import (
    ArticleSerializer,
)

from apps.api.v1.serializers.discovery_serializer import (
    DiscoveryRequestSerializer,
)

from apps.api.v1.serializers.competitor_serializer import (
    CompetitorRequestSerializer,
)

from apps.engine.models import (
    Article,
)

from apps.engine.orchestrator import (
    Orchestrator,
)

from apps.engine.schemas.request_schema import (
    GenerateContentRequestSerializer,
)

from apps.discovery.engine import (
    DiscoveryEngine,
)

from apps.competitor.engine import (
    CompetitorEngine,
)

from utils.response import (
    APIResponse,
)

from utils.logger import (
    logger,
)

from utils.exceptions import (
    AICOSException,
)


# ==================================================
# HEALTH CHECK API
# ==================================================

class HealthCheckView(APIView):

    def get(
        self,
        request
    ):

        logger.info(
            "Health check requested"
        )

        response = (
            APIResponse.success(

                data={

                    "service": "AI COS API",

                    "version": "2.0.0",

                    "status": "healthy",
                },

                message=(
                    "AI COS API is running"
                )
            )
        )

        return Response(
            response,
            status=status.HTTP_200_OK
        )


# ==================================================
# GENERATE CONTENT API
# ==================================================

class GenerateContentView(APIView):

    def post(
        self,
        request
    ):

        try:

            # =====================
            # VALIDATE REQUEST
            # =====================

            serializer = (
                GenerateContentRequestSerializer(
                    data=request.data
                )
            )

            if not serializer.is_valid():

                response = (
                    APIResponse.validation_error(

                        errors=serializer.errors
                    )
                )

                return Response(
                    response,
                    status=status.HTTP_422_UNPROCESSABLE_ENTITY
                )

            # =====================
            # EXTRACT KEYWORD
            # =====================

            keyword = (
                serializer.validated_data[
                    "keyword"
                ]
            )

            logger.info(

                f"Content generation "
                f"requested for: {keyword}"
            )

            # =====================
            # RUN ORCHESTRATOR
            # =====================

            orchestrator = (
                Orchestrator()
            )

            result = (
                orchestrator.run(
                    keyword
                )
            )

            # =====================
            # GET ARTICLE
            # =====================

            article_id = result[
                "data"
            ].get(
                "article_id"
            )

            article = (
                Article.objects.get(
                    id=article_id
                )
            )

            # =====================
            # SERIALIZE ARTICLE
            # =====================

            article_serializer = (
                ArticleSerializer(
                    article
                )
            )

            # =====================
            # BUILD RESPONSE DATA
            # =====================

            response_data = {

                "article": (
                    article_serializer.data
                ),

                "pipeline": {

                    "status": result.get(
                        "status"
                    ),

                    "current_step": result.get(
                        "current_step"
                    ),

                    "started_at": result.get(
                        "started_at"
                    ),

                    "completed_at": result.get(
                        "completed_at"
                    ),
                },

                "errors": result.get(
                    "errors",
                    []
                ),
            }

            response = (
                APIResponse.success(

                    data=response_data,

                    message=(
                        "Article generated "
                        "successfully."
                    )
                )
            )

            return Response(
                response,
                status=status.HTTP_200_OK
            )

        except Article.DoesNotExist:

            logger.error(
                "Generated article not found"
            )

            response = (
                APIResponse.not_found(

                    message=(
                        "Generated article "
                        "not found."
                    )
                )
            )

            return Response(
                response,
                status=status.HTTP_404_NOT_FOUND
            )

        except AICOSException as error:

            logger.error(str(error))

            response = (
                APIResponse.error(

                    message=str(error),

                    status_code=400,

                    error_code=(
                        "GENERATION_ERROR"
                    )
                )
            )

            return Response(
                response,
                status=status.HTTP_400_BAD_REQUEST
            )

        except Exception as error:

            logger.error(str(error))

            response = (
                APIResponse.server_error(
                    str(error)
                )
            )

            return Response(
                response,
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# ==================================================
# ARTICLE LIST API
# ==================================================

class ArticleListView(APIView):

    def get(
        self,
        request
    ):

        try:

            logger.info(
                "Fetching article list"
            )

            # =====================
            # BASE QUERYSET
            # =====================

            articles = (

                Article.objects
                .all()
                .order_by("-created_at")
            )

            # =====================
            # SEARCH FILTER
            # =====================

            search = request.GET.get(
                "search"
            )

            if search:

                articles = (
                    articles.filter(
                        title__icontains=search
                    )
                )

            # =====================
            # VERIFIED FILTER
            # =====================

            verified = request.GET.get(
                "verified"
            )

            if verified == "true":

                articles = (
                    articles.filter(
                        is_verified=True
                    )
                )

            elif verified == "false":

                articles = (
                    articles.filter(
                        is_verified=False
                    )
                )

            # =====================
            # PUBLISHED FILTER
            # =====================

            published = request.GET.get(
                "published"
            )

            if published == "true":

                articles = (
                    articles.filter(
                        is_published=True
                    )
                )

            elif published == "false":

                articles = (
                    articles.filter(
                        is_published=False
                    )
                )

            # =====================
            # SEO SCORE FILTER
            # =====================

            seo_score = request.GET.get(
                "seo_score"
            )

            if seo_score:

                articles = (
                    articles.filter(
                        seo_score__gte=seo_score
                    )
                )

            # =====================
            # SERIALIZE ARTICLES
            # =====================

            serializer = (
                ArticleSerializer(
                    articles,
                    many=True
                )
            )

            response_data = {

                "count": (
                    articles.count()
                ),

                "filters": {

                    "search": search,

                    "verified": verified,

                    "published": published,

                    "seo_score": seo_score,
                },

                "results": (
                    serializer.data
                ),
            }

            response = (
                APIResponse.success(

                    data=response_data,

                    message=(
                        "Articles fetched "
                        "successfully."
                    )
                )
            )

            return Response(
                response,
                status=status.HTTP_200_OK
            )

        except Exception as error:

            logger.error(str(error))

            response = (
                APIResponse.server_error(
                    str(error)
                )
            )

            return Response(
                response,
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# ==================================================
# ARTICLE DETAIL API
# ==================================================

class ArticleDetailView(APIView):

    def get(
        self,
        request,
        article_id
    ):

        try:

            logger.info(

                f"Fetching article: "
                f"{article_id}"
            )

            # =====================
            # FETCH ARTICLE
            # =====================

            article = (
                Article.objects.get(
                    id=article_id
                )
            )

            # =====================
            # SERIALIZE ARTICLE
            # =====================

            serializer = (
                ArticleSerializer(
                    article
                )
            )

            response = (
                APIResponse.success(

                    data=serializer.data,

                    message=(
                        "Article fetched "
                        "successfully."
                    )
                )
            )

            return Response(
                response,
                status=status.HTTP_200_OK
            )

        except Article.DoesNotExist:

            logger.error(
                "Article not found"
            )

            response = (
                APIResponse.not_found(

                    message=(
                        "Article not found."
                    )
                )
            )

            return Response(
                response,
                status=status.HTTP_404_NOT_FOUND
            )

        except Exception as error:

            logger.error(str(error))

            response = (
                APIResponse.server_error(
                    str(error)
                )
            )

            return Response(
                response,
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# ==================================================
# DISCOVERY API
# ==================================================

class DiscoveryView(APIView):

    def post(
        self,
        request
    ):

        try:

            # =====================
            # VALIDATE REQUEST
            # =====================

            serializer = (
                DiscoveryRequestSerializer(
                    data=request.data
                )
            )

            if not serializer.is_valid():

                response = (
                    APIResponse.validation_error(

                        errors=serializer.errors
                    )
                )

                return Response(
                    response,
                    status=status.HTTP_422_UNPROCESSABLE_ENTITY
                )

            # =====================
            # EXTRACT DATA
            # =====================

            keyword = (
                serializer.validated_data[
                    "keyword"
                ]
            )

            limit = (
                serializer.validated_data[
                    "limit"
                ]
            )

            include_trends = (
                serializer.validated_data[
                    "include_trends"
                ]
            )

            include_clusters = (
                serializer.validated_data[
                    "include_clusters"
                ]
            )

            logger.info(

                f"Discovery requested "
                f"for keyword: {keyword}"
            )

            # =====================
            # RUN DISCOVERY ENGINE
            # =====================

            discovery_engine = (
                DiscoveryEngine()
            )

            result = (
                discovery_engine.discover(
                    keyword
                )
            )

            # =====================
            # OPTIONAL FILTERS
            # =====================

            if not include_trends:

                result.pop(
                    "trends",
                    None
                )

            if not include_clusters:

                result.pop(
                    "clusters",
                    None
                )

            # =====================
            # LIMIT RESULTS
            # =====================

            result[
                "top_opportunities"
            ] = result[
                "top_opportunities"
            ][:limit]

            response = (
                APIResponse.success(

                    data=result,

                    message=(
                        "Keyword opportunities "
                        "generated successfully."
                    )
                )
            )

            return Response(
                response,
                status=status.HTTP_200_OK
            )

        except AICOSException as error:

            logger.error(str(error))

            response = (
                APIResponse.error(

                    message=str(error),

                    status_code=400,

                    error_code=(
                        "DISCOVERY_ERROR"
                    )
                )
            )

            return Response(
                response,
                status=status.HTTP_400_BAD_REQUEST
            )

        except Exception as error:

            logger.error(str(error))

            response = (
                APIResponse.server_error(
                    str(error)
                )
            )

            return Response(
                response,
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# ==================================================
# COMPETITOR API
# ==================================================

class CompetitorView(APIView):

    def post(
        self,
        request
    ):

        try:

            # =====================
            # VALIDATE REQUEST
            # =====================

            serializer = (
                CompetitorRequestSerializer(
                    data=request.data
                )
            )

            if not serializer.is_valid():

                response = (
                    APIResponse.validation_error(

                        errors=serializer.errors
                    )
                )

                return Response(
                    response,
                    status=status.HTTP_422_UNPROCESSABLE_ENTITY
                )

            # =====================
            # EXTRACT DATA
            # =====================

            keyword = (
                serializer.validated_data[
                    "keyword"
                ]
            )

            include_serp = (
                serializer.validated_data[
                    "include_serp"
                ]
            )

            include_gaps = (
                serializer.validated_data[
                    "include_gaps"
                ]
            )

            include_weaknesses = (
                serializer.validated_data[
                    "include_weaknesses"
                ]
            )

            logger.info(

                f"Competitor analysis "
                f"requested for: {keyword}"
            )

            # =====================
            # RUN COMPETITOR ENGINE
            # =====================

            competitor_engine = (
                CompetitorEngine()
            )

            result = (
                competitor_engine.analyze(

                    keyword=keyword,

                    include_serp=(
                        include_serp
                    ),

                    include_gaps=(
                        include_gaps
                    ),

                    include_weaknesses=(
                        include_weaknesses
                    )
                )
            )

            response = (
                APIResponse.success(

                    data=result,

                    message=(
                        "Competitor analysis "
                        "completed successfully."
                    )
                )
            )

            return Response(
                response,
                status=status.HTTP_200_OK
            )

        except AICOSException as error:

            logger.error(str(error))

            response = (
                APIResponse.error(

                    message=str(error),

                    status_code=400,

                    error_code=(
                        "COMPETITOR_ERROR"
                    )
                )
            )

            return Response(
                response,
                status=status.HTTP_400_BAD_REQUEST
            )

        except Exception as error:

            logger.error(str(error))

            response = (
                APIResponse.server_error(
                    str(error)
                )
            )

            return Response(
                response,
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )