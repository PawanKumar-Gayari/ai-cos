from django.urls import path

from apps.api.v1.generator.views import (

    GenerateArticleAPIView,

    GenerateOutlineAPIView,

    GenerateKeywordsAPIView,
)

from apps.api.v1.generator.task_views import (
    TaskStatusAPIView
)


urlpatterns = [

    path(

        "article/",

        GenerateArticleAPIView.as_view(),
    ),

    path(

        "outline/",

        GenerateOutlineAPIView.as_view(),
    ),

    path(

        "keywords/",

        GenerateKeywordsAPIView.as_view(),
    ),

    path(

        "task/<str:task_id>/",

        TaskStatusAPIView.as_view(),
    ),
]