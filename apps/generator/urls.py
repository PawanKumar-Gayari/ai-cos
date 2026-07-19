from django.urls import path

from apps.generator.views import (
    article_view,
)

from apps.api.v1.generator.views import (

    GenerateArticleAPIView,

    GenerateOutlineAPIView,

    GenerateKeywordsAPIView,
)


urlpatterns = [

    # ==========================================
    # ARTICLE GENERATION
    # ==========================================

    path(

        "article/",

        GenerateArticleAPIView.as_view(),

        name="generate-article",
    ),

    # ==========================================
    # OUTLINE
    # ==========================================

    path(

        "outline/",

        GenerateOutlineAPIView.as_view(),

        name="generate-outline",
    ),

    # ==========================================
    # KEYWORDS
    # ==========================================

    path(

        "keywords/",

        GenerateKeywordsAPIView.as_view(),

        name="generate-keywords",
    ),

    # ==========================================
    # ARTICLE RENDERER DEMO
    # ==========================================

    path(

        "view/",

        article_view,

        name="article-view",
    ),
]