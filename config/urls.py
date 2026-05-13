"""
Main URL configuration for ai_cos project.
"""

from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin

from django.http import JsonResponse

from django.urls import (
    include,
    path,
)

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)


# ==================================================
# SAFE IMPORTS
# ==================================================

from apps.core.model_manager import (
    ModelManager
)

from apps.llm.router import (
    LLMRouter
)

from apps.memory.embeddings.embedding_service import (
    EmbeddingService
)


# ==================================================
# APP METADATA
# ==================================================

API_VERSION = "v1"

SYSTEM_NAME = "AI COS API"


# ==================================================
# HOME ENDPOINT
# ==================================================

def home(
    request
):

    """
    Root system health endpoint.
    """

    try:

        router = (
            LLMRouter()
        )

        embedding_service = (
            EmbeddingService()
        )

        return JsonResponse({

            "success": True,

            "message": (
                f"{SYSTEM_NAME} Running"
            ),

            "version": API_VERSION,

            "environment": (

                "development"

                if settings.DEBUG

                else "production"
            ),

            "ai_system": {

                "router": (
                    router.router_status()
                ),

                "embedding": (
                    embedding_service.health_check()
                ),

                "runtime": (
                    ModelManager.system_status()
                ),
            },
        })

    except Exception as error:

        return JsonResponse({

            "success": False,

            "message": (
                "System initialization failed."
            ),

            "error": str(error),
        }, status=500)


# ==================================================
# SYSTEM STATUS
# ==================================================

def system_status(
    request
):

    """
    Enterprise runtime status.
    """

    try:

        router = (
            LLMRouter()
        )

        embedding_service = (
            EmbeddingService()
        )

        return JsonResponse({

            "success": True,

            "system": "active",

            "debug": settings.DEBUG,

            "llm_router": (
                router.router_status()
            ),

            "embedding_service": (
                embedding_service.health_check()
            ),

            "runtime": (
                ModelManager.system_status()
            ),
        })

    except Exception as error:

        return JsonResponse({

            "success": False,

            "system": "error",

            "error": str(error),
        }, status=500)


# ==================================================
# URL PATTERNS
# ==================================================

urlpatterns = [

    # ==============================================
    # ROOT
    # ==============================================

    path(
        "",
        home,
        name="home",
    ),

    # ==============================================
    # SYSTEM STATUS
    # ==============================================

    path(
        "system/status/",
        system_status,
        name="system-status",
    ),

    # ==============================================
    # ADMIN
    # ==============================================

    path(
        "admin/",
        admin.site.urls,
    ),

    # ==============================================
    # API V1
    # ==============================================

    path(
        "api/v1/",
        include(
            "apps.api.v1.urls"
        ),
    ),

    # ==============================================
    # GENERATOR API
    # ==============================================

    path(
        "api/v1/generator/",
        include(
            "apps.api.v1.generator.urls"
        ),
    ),

    # ==============================================
    # MONITORING API
    # ==============================================

    path(
        "api/monitoring/",
        include(
            "apps.monitoring.urls"
        ),
    ),

    # ==============================================
    # OPENAPI SCHEMA
    # ==============================================

    path(
        "api/schema/",
        SpectacularAPIView.as_view(),
        name="schema",
    ),
]


# ==================================================
# OPTIONAL DOCS
# ==================================================

if getattr(
    settings,
    "ENABLE_API_DOCS",
    True,
):

    urlpatterns += [

        # ==========================================
        # SWAGGER
        # ==========================================

        path(

            "api/docs/",

            SpectacularSwaggerView.as_view(
                url_name="schema"
            ),

            name="swagger-ui",
        ),

        # ==========================================
        # REDOC
        # ==========================================

        path(

            "api/redoc/",

            SpectacularRedocView.as_view(
                url_name="schema"
            ),

            name="redoc",
        ),
    ]


# ==================================================
# STATIC / MEDIA
# ==================================================

if settings.DEBUG:

    urlpatterns += static(

        settings.MEDIA_URL,

        document_root=settings.MEDIA_ROOT,
    )

    urlpatterns += static(

        settings.STATIC_URL,

        document_root=settings.STATIC_ROOT,
    )