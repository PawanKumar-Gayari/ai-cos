from django.urls import path

from apps.api.v1.history.views import (

    GenerationHistoryListAPIView,

    GenerationHistoryDetailAPIView,
)


urlpatterns = [

    path(
        "",
        GenerationHistoryListAPIView.as_view(),
    ),

    path(
        "<uuid:id>/",
        GenerationHistoryDetailAPIView.as_view(),
    ),
]