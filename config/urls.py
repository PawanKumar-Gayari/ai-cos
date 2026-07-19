"""
Main URL configuration for ai_cos project.
"""

from __future__ import annotations

from django.conf import settings

from django.conf.urls.static import static

from django.contrib import admin

from django.contrib.admin.views.decorators import (
    staff_member_required,
)

from django.contrib.auth import views as auth_views

from django.contrib.auth.decorators import (
    login_required,
)

from django.http import JsonResponse

from django.urls import (
    include,
    path,
)

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

# =========================================================
# SAFE IMPORTS
# =========================================================

from apps.core.model_manager import (
    ModelManager,
)

from apps.llm.router import (
    LLMRouter,
)

from apps.memory.embeddings.embedding_service import (
    EmbeddingService,
)

# =========================================================
# APP METADATA
# =========================================================

API_VERSION = "v1"

SYSTEM_NAME = "AI COS API"

# =========================================================
# SYSTEM STATUS
# =========================================================


@login_required(
    login_url="/login/"
)
def system_status(request):

    """
    Enterprise runtime status.
    """

    if not request.user.is_staff:

        return JsonResponse({

            "success": False,

            "message": (
                "Access denied."
            ),

        }, status=403)

    try:

        router = LLMRouter()

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


# =========================================================
# URL PATTERNS
# =========================================================

urlpatterns = [

    # =====================================================
    # FRONTEND
    # =====================================================

    path(
        "",
        include(
            "apps.frontend.urls"
        ),
    ),

    # =====================================================
    # AUTH
    # =====================================================

    path(

        "login/",

        auth_views.LoginView.as_view(

            template_name=(
                "auth/login.html"
            )
        ),

        name="login",
    ),

    path(

        "logout/",

        auth_views.LogoutView.as_view(),

        name="logout",
    ),

    # =====================================================
    # PASSWORD RESET
    # =====================================================

    path(

        "password-reset/",

        auth_views.PasswordResetView.as_view(

            template_name=(
                "auth/password_reset.html"
            )
        ),

        name="password_reset",
    ),

    path(

        "password-reset/done/",

        auth_views.PasswordResetDoneView.as_view(

            template_name=(
                "auth/password_reset_done.html"
            )
        ),

        name="password_reset_done",
    ),

    path(

        "reset/<uidb64>/<token>/",

        auth_views.PasswordResetConfirmView.as_view(

            template_name=(
                "auth/password_reset_confirm.html"
            )
        ),

        name="password_reset_confirm",
    ),

    path(

        "reset/done/",

        auth_views.PasswordResetCompleteView.as_view(

            template_name=(
                "auth/password_reset_complete.html"
            )
        ),

        name="password_reset_complete",
    ),

    # =====================================================
    # SYSTEM STATUS
    # =====================================================

    path(

        "system/status/",

        system_status,

        name="system-status",
    ),

    # =====================================================
    # ADMIN
    # =====================================================

    path(
        "admin/",
        admin.site.urls,
    ),

    # =====================================================
    # DASHBOARD
    # =====================================================

    path(
        "dashboard/",
        include(
            "apps.dashboard.urls"
        ),
    ),

    # =====================================================
    # API V1
    # =====================================================

    path(
        "api/v1/",
        include(
            "apps.api.v1.urls"
        ),
    ),

    # =====================================================
    # KEYWORDS API
    # =====================================================

    path(
        "api/keywords/",
        include(
            "apps.keywords.urls"
        ),
    ),

    # =====================================================
    # GENERATOR API
    # =====================================================

    path(
        "api/v1/generator/",
        include(
            "apps.generator.urls"
        ),
    ),

    # =====================================================
    # PUBLISHER API
    # =====================================================

    path(
        "api/publisher/",
        include(
            "apps.publisher.urls"
        ),
    ),

    # =====================================================
    # DECISION ENGINE API
    # =====================================================

    path(
        "api/decision/",
        include(
            "apps.decision_engine.api.urls"
        ),
    ),

    # =====================================================
    # MONITORING API
    # =====================================================

    path(
        "api/monitoring/",
        include(
            "apps.monitoring.urls"
        ),
    ),

    # =====================================================
    # OPENAPI SCHEMA
    # =====================================================

    path(

        "api/schema/",

        staff_member_required(

            SpectacularAPIView.as_view()
        ),

        name="schema",
    ),
]

# =========================================================
# OPTIONAL DOCS
# =========================================================

if getattr(
    settings,
    "ENABLE_API_DOCS",
    True,
):

    urlpatterns += [

        # =================================================
        # SWAGGER UI
        # =================================================

        path(

            "api/docs/",

            staff_member_required(

                SpectacularSwaggerView.as_view(
                    url_name="schema"
                )
            ),

            name="swagger-ui",
        ),

        # =================================================
        # REDOC
        # =================================================

        path(

            "api/redoc/",

            staff_member_required(

                SpectacularRedocView.as_view(
                    url_name="schema"
                )
            ),

            name="redoc",
        ),
    ]

# =========================================================
# STATIC / MEDIA
# =========================================================

if settings.DEBUG:

    urlpatterns += static(

        settings.MEDIA_URL,

        document_root=settings.MEDIA_ROOT,
    )

    urlpatterns += static(

        settings.STATIC_URL,

        document_root=settings.STATIC_ROOT,
    )