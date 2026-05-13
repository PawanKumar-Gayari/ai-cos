"""
Enterprise AI generation API views.
"""

from rest_framework.views import (
    APIView
)

from rest_framework.response import (
    Response
)

from rest_framework import status

from drf_spectacular.utils import (
    extend_schema,
)

from apps.api.v1.generator.serializers import (

    GenerateArticleSerializer,

    GenerateOutlineSerializer,

    GenerateKeywordsSerializer,

    TaskQueuedSerializer,

    ErrorSerializer,
)

from apps.generator.tasks import (

    generate_article_task,

    generate_outline_task,

    generate_keywords_task,
)


class GenerateArticleAPIView(
    APIView
):

    @extend_schema(

        request=GenerateArticleSerializer,

        responses={

            200: TaskQueuedSerializer,

            400: ErrorSerializer,
        },

        tags=["AI Generator"],
    )
    def post(
        self,
        request,
    ):

        serializer = (
            GenerateArticleSerializer(
                data=request.data
            )
        )

        if not serializer.is_valid():

            return Response(

                serializer.errors,

                status=status.HTTP_400_BAD_REQUEST,
            )

        query = serializer.validated_data[
            "query"
        ]

        session_id = (
            serializer.validated_data.get(
                "session_id"
            )
        )

        task = (
            generate_article_task.delay(

                query,

                session_id,
            )
        )

        return Response({

            "success": True,

            "task_id": task.id,

            "status": "queued",
        })


class GenerateOutlineAPIView(
    APIView
):

    @extend_schema(

        request=GenerateOutlineSerializer,

        responses={

            200: TaskQueuedSerializer,

            400: ErrorSerializer,
        },

        tags=["AI Generator"],
    )
    def post(
        self,
        request,
    ):

        serializer = (
            GenerateOutlineSerializer(
                data=request.data
            )
        )

        if not serializer.is_valid():

            return Response(

                serializer.errors,

                status=status.HTTP_400_BAD_REQUEST,
            )

        topic = serializer.validated_data[
            "topic"
        ]

        session_id = (
            serializer.validated_data.get(
                "session_id"
            )
        )

        task = (
            generate_outline_task.delay(

                topic,

                session_id,
            )
        )

        return Response({

            "success": True,

            "task_id": task.id,

            "status": "queued",
        })


class GenerateKeywordsAPIView(
    APIView
):

    @extend_schema(

        request=GenerateKeywordsSerializer,

        responses={

            200: TaskQueuedSerializer,

            400: ErrorSerializer,
        },

        tags=["AI Generator"],
    )
    def post(
        self,
        request,
    ):

        serializer = (
            GenerateKeywordsSerializer(
                data=request.data
            )
        )

        if not serializer.is_valid():

            return Response(

                serializer.errors,

                status=status.HTTP_400_BAD_REQUEST,
            )

        topic = serializer.validated_data[
            "topic"
        ]

        session_id = (
            serializer.validated_data.get(
                "session_id"
            )
        )

        task = (
            generate_keywords_task.delay(

                topic,

                session_id,
            )
        )

        return Response({

            "success": True,

            "task_id": task.id,

            "status": "queued",
        })