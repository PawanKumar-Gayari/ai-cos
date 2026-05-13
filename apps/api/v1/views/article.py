"""
Article APIs.
"""

from rest_framework import status

from .base import (
    BaseAPIView,
    logger,
)

from apps.api.v1.serializers import (
    ArticleSerializer,
)

from apps.engine.models import (
    Article,
)


class ArticleListView(BaseAPIView):

    def get(
        self,
        request
    ):

        try:

            logger.info(
                "Fetching article list"
            )

            articles = (

                Article.objects
                .all()
                .order_by("-created_at")
            )

            search = request.GET.get(
                "search"
            )

            if search:

                articles = (
                    articles.filter(
                        title__icontains=search
                    )
                )

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

            seo_score = request.GET.get(
                "seo_score"
            )

            if seo_score:

                articles = (
                    articles.filter(
                        seo_score__gte=seo_score
                    )
                )

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

            return self.success_response(

                data=response_data,

                message=(
                    "Articles fetched "
                    "successfully."
                )
            )

        except Exception as error:

            return self.server_error_response(
                error
            )


class ArticleDetailView(BaseAPIView):

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

            article = (
                Article.objects.get(
                    id=article_id
                )
            )

            serializer = (
                ArticleSerializer(
                    article
                )
            )

            return self.success_response(

                data=serializer.data,

                message=(
                    "Article fetched "
                    "successfully."
                )
            )

        except Article.DoesNotExist:

            return self.error_response(

                message=(
                    "Article not found."
                ),

                status_code=status.HTTP_404_NOT_FOUND,

                error_code="ARTICLE_NOT_FOUND"
            )

        except Exception as error:

            return self.server_error_response(
                error
            )