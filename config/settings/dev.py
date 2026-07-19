"""
Development Settings
--------------------

Production-grade development configuration.

Features:
- OCI optimized
- secure local development
- middleware-compatible API config
- DRF optimized
- async ready
- AI provider ready
- Redis optimized
- Celery production-safe configuration
"""

from __future__ import annotations

import os

from .base import *


# ==================================================
# DEBUG
# ==================================================

DEBUG = True


# ==================================================
# ALLOWED HOSTS
# ==================================================

ALLOWED_HOSTS = [

    "127.0.0.1",

    "localhost",

    "0.0.0.0",

    "ai.aspirantveda.in",
]


# ==================================================
# CSRF
# ==================================================

CSRF_TRUSTED_ORIGINS = [

    "https://ai.aspirantveda.in",
]


# ==================================================
# PROXY SSL
# ==================================================

SECURE_PROXY_SSL_HEADER = (

    "HTTP_X_FORWARDED_PROTO",

    "https",
)

USE_X_FORWARDED_HOST = True


# ==================================================
# DATABASE
# ==================================================

DATABASES = {

    "default": {

        "ENGINE": os.getenv(

            "DB_ENGINE",

            "django.db.backends.postgresql",
        ),

        "NAME": os.getenv(

            "DB_NAME",

            "ai_cos_db",
        ),

        "USER": os.getenv(

            "DB_USER",

            "ai_cos_user",
        ),

        "PASSWORD": os.getenv(

            "DB_PASSWORD",

            "",
        ),

        "HOST": os.getenv(

            "DB_HOST",

            "127.0.0.1",
        ),

        "PORT": os.getenv(

            "DB_PORT",

            "5432",
        ),
    }
}


# ==================================================
# REDIS
# ==================================================

REDIS_URL = os.getenv(

    "REDIS_URL",

    "redis://127.0.0.1:6379/1",
)


# ==================================================
# CELERY
# ==================================================

CELERY_BROKER_URL = os.getenv(

    "CELERY_BROKER_URL",

    "redis://127.0.0.1:6379/0",
)

CELERY_RESULT_BACKEND = os.getenv(

    "CELERY_RESULT_BACKEND",

    "redis://127.0.0.1:6379/0",
)

# ==================================================
# CELERY SERIALIZATION
# ==================================================

CELERY_TASK_SERIALIZER = "json"

CELERY_RESULT_SERIALIZER = "json"

CELERY_ACCEPT_CONTENT = [

    "json",
]

CELERY_RESULT_ACCEPT_CONTENT = [

    "json",
]

CELERY_TASK_IGNORE_RESULT = False

CELERY_RESULT_EXTENDED = True

CELERY_TASK_STORE_ERRORS_EVEN_IF_IGNORED = True

CELERY_WORKER_PREFETCH_MULTIPLIER = 1

CELERY_TASK_ACKS_LATE = True

CELERY_TASK_TRACK_STARTED = True

CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True

CELERY_TIMEZONE = "Asia/Kolkata"

CELERY_ENABLE_UTC = True


# ==================================================
# EMAIL
# ==================================================

EMAIL_BACKEND = (

    "django.core.mail.backends.console.EmailBackend"
)


# ==================================================
# SECURITY
# ==================================================

SESSION_COOKIE_SECURE = False

CSRF_COOKIE_SECURE = False

SECURE_SSL_REDIRECT = False


# ==================================================
# CORS
# ==================================================

CORS_ALLOW_ALL_ORIGINS = True

CORS_ALLOW_CREDENTIALS = True


# ==================================================
# API DOCS
# ==================================================

ENABLE_API_DOCS = True


# ==================================================
# FEATURES
# ==================================================

ENABLE_MEMORY = True

ENABLE_ASYNC_GENERATION = True

ENABLE_REDIS = True

ENABLE_CELERY = True


# ==================================================
# API AUTH
# ==================================================

AICOS_API_KEY = os.getenv(

    "AICOS_API_KEY",

    "",
)


# ==================================================
# AI PROVIDERS
# ==================================================

OPENAI_API_KEY = os.getenv(
    "OPENAI_API_KEY"
)

GEMINI_API_KEY = os.getenv(
    "GEMINI_API_KEY"
)

OLLAMA_BASE_URL = os.getenv(

    "OLLAMA_BASE_URL",

    "http://127.0.0.1:11434",
)

OLLAMA_MODEL = os.getenv(

    "OLLAMA_MODEL",

    "tinyllama",
)


# ==================================================
# SEARCH PROVIDERS
# ==================================================

SERPAPI_KEY = os.getenv(
    "SERPAPI_KEY"
)

SERPER_API_KEY = os.getenv(
    "SERPER_API_KEY"
)

TAVILY_API_KEY = os.getenv(
    "TAVILY_API_KEY"
)

GOOGLE_CSE_API_KEY = os.getenv(
    "GOOGLE_CSE_API_KEY"
)

GOOGLE_CSE_ID = os.getenv(
    "GOOGLE_CSE_ID"
)


# ==================================================
# TIMEOUTS
# ==================================================

AI_PROVIDER_TIMEOUT = 300

REQUEST_TIMEOUT = 120


# ==================================================
# GENERATION SETTINGS
# ==================================================

MAX_REWRITE_LOOPS = 3

TARGET_REWRITE_SCORE = 85


# ==================================================
# MEMORY SETTINGS
# ==================================================

MEMORY_TOP_K = 2

MEMORY_SIMILARITY_THRESHOLD = 0.75


# ==================================================
# DJANGO REST FRAMEWORK
# ==================================================

REST_FRAMEWORK = {

    # ==============================================
    # AUTH
    # ==============================================

    "DEFAULT_PERMISSION_CLASSES": [

        "rest_framework.permissions.AllowAny",
    ],

    # ==============================================
    # RENDERERS
    # ==============================================

    "DEFAULT_RENDERER_CLASSES": [

        "rest_framework.renderers.JSONRenderer",

        "rest_framework.renderers.BrowsableAPIRenderer",
    ],

    # ==============================================
    # PARSERS
    # ==============================================

    "DEFAULT_PARSER_CLASSES": [

        "rest_framework.parsers.JSONParser",

        "rest_framework.parsers.FormParser",

        "rest_framework.parsers.MultiPartParser",
    ],

    # ==============================================
    # THROTTLING
    # ==============================================

    "DEFAULT_THROTTLE_CLASSES": [

        "rest_framework.throttling.AnonRateThrottle",

        "rest_framework.throttling.UserRateThrottle",
    ],

    "DEFAULT_THROTTLE_RATES": {

        "anon": "20/min",

        "user": "300/min",
    },

    # ==============================================
    # PAGINATION
    # ==============================================

    "DEFAULT_PAGINATION_CLASS":

    "rest_framework.pagination.PageNumberPagination",

    "PAGE_SIZE": 10,

    # ==============================================
    # SCHEMA
    # ==============================================

    "DEFAULT_SCHEMA_CLASS":

    "drf_spectacular.openapi.AutoSchema",
}


# ==================================================
# LOGGING
# ==================================================

LOGGING["root"]["level"] = (
    "INFO"
)

LOGGING["loggers"] = {

    "django": {

        "handlers": [

            "console",

            "file",
        ],

        "level": "INFO",

        "propagate": True,
    },

    "apps": {

        "handlers": [

            "console",

            "file",
        ],

        "level": "INFO",

        "propagate": False,
    },

    "celery": {

        "handlers": [

            "console",

            "file",
        ],

        "level": "INFO",

        "propagate": False,
    },
}