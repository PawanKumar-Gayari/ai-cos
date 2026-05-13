"""
Base Django settings for ai_cos project.
"""

from pathlib import Path

from dotenv import load_dotenv

import os


from apps.core.constants.features import (
    ENABLE_REDIS,
    ENABLE_CELERY,
    ENABLE_ASYNC_GENERATION,
)


# ==================================================
# BASE DIRECTORY
# ==================================================

BASE_DIR = (
    Path(__file__)
    .resolve()
    .parent
    .parent
    .parent
)


# ==================================================
# LOAD ENV VARIABLES
# ==================================================

load_dotenv(
    BASE_DIR / ".env"
)


# ==================================================
# ENV HELPERS
# ==================================================

def env_bool(
    key,
    default=False,
):

    return (
        os.getenv(
            key,
            str(default),
        ).lower()
        == "true"
    )


# ==================================================
# SECURITY
# ==================================================

DEBUG = env_bool(
    "DEBUG",
    True,
)

SECRET_KEY = os.getenv(
    "SECRET_KEY"
)

if not SECRET_KEY and not DEBUG:

    raise ValueError(
        "SECRET_KEY missing in production."
    )

if not SECRET_KEY:

    SECRET_KEY = (
        "unsafe-dev-secret-key"
    )

ALLOWED_HOSTS = os.getenv(

    "ALLOWED_HOSTS",

    "127.0.0.1,localhost",
).split(",")


# ==================================================
# FEATURE FLAGS
# ==================================================

ENABLE_API_DOCS = env_bool(
    "ENABLE_API_DOCS",
    True,
)


# ==================================================
# DJANGO APPS
# ==================================================

DJANGO_APPS = [

    "django.contrib.admin",

    "django.contrib.auth",

    "django.contrib.contenttypes",

    "django.contrib.sessions",

    "django.contrib.messages",

    "django.contrib.staticfiles",
]


# ==================================================
# THIRD PARTY APPS
# ==================================================

THIRD_PARTY_APPS = [

    # ==========================================
    # REST API
    # ==========================================

    "rest_framework",

    "rest_framework.authtoken",

    # ==========================================
    # OPENAPI / DOCS
    # ==========================================

    "drf_spectacular",

    # ==========================================
    # CORS
    # ==========================================

    "corsheaders",
]


# ==================================================
# LOCAL APPS
# ==================================================

LOCAL_APPS = [

    # ==========================================
    # CORE
    # ==========================================

    "apps.core",

    # ==========================================
    # API
    # ==========================================

    "apps.api",

    # ==========================================
    # MEMORY
    # ==========================================

    "apps.memory",

    # ==========================================
    # ENGINE
    # ==========================================

    "apps.engine",

    "apps.generator",

    "apps.verifier",

    "apps.rewriter",

    "apps.discovery",

    "apps.decision_engine",

    # ==========================================
    # SEO SYSTEMS
    # ==========================================

    "apps.keywords",

    "apps.competitor",

    "apps.publisher",

    # ==========================================
    # ANALYTICS
    # ==========================================

    "apps.analytics",

    "apps.monitoring",

    "apps.history",

    "apps.llm",
]


# ==================================================
# INSTALLED APPS
# ==================================================

INSTALLED_APPS = (

    DJANGO_APPS

    + THIRD_PARTY_APPS

    + LOCAL_APPS
)


# ==================================================
# MIDDLEWARE
# ==================================================

MIDDLEWARE = [

    # ==========================================
    # SECURITY
    # ==========================================

    "django.middleware.security.SecurityMiddleware",

    # ==========================================
    # CORS
    # ==========================================

    "corsheaders.middleware.CorsMiddleware",

    # ==========================================
    # SESSIONS
    # ==========================================

    "django.contrib.sessions.middleware.SessionMiddleware",

    # ==========================================
    # COMMON
    # ==========================================

    "django.middleware.common.CommonMiddleware",

    # ==========================================
    # CSRF
    # ==========================================

    "django.middleware.csrf.CsrfViewMiddleware",

    # ==========================================
    # AUTH
    # ==========================================

    "django.contrib.auth.middleware.AuthenticationMiddleware",

    # ==========================================
    # MESSAGES
    # ==========================================

    "django.contrib.messages.middleware.MessageMiddleware",

    # ==========================================
    # CLICKJACKING
    # ==========================================

    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


# ==================================================
# ROOT CONFIG
# ==================================================

ROOT_URLCONF = "config.urls"


# ==================================================
# TEMPLATES
# ==================================================

TEMPLATES = [

    {

        "BACKEND": (
            "django.template.backends.django.DjangoTemplates"
        ),

        "DIRS": [
            BASE_DIR / "templates",
        ],

        "APP_DIRS": True,

        "OPTIONS": {

            "context_processors": [

                "django.template.context_processors.request",

                "django.contrib.auth.context_processors.auth",

                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


# ==================================================
# WSGI / ASGI
# ==================================================

WSGI_APPLICATION = (
    "config.wsgi.application"
)

ASGI_APPLICATION = (
    "config.asgi.application"
)


# ==================================================
# DATABASE
# ==================================================

DATABASES = {

    "default": {

        "ENGINE": os.getenv(

            "DB_ENGINE",

            "django.db.backends.sqlite3",
        ),

        "NAME": os.getenv(

            "DB_NAME",

            BASE_DIR / "db.sqlite3",
        ),

        "USER": os.getenv(
            "DB_USER",
            "",
        ),

        "PASSWORD": os.getenv(
            "DB_PASSWORD",
            "",
        ),

        "HOST": os.getenv(
            "DB_HOST",
            "",
        ),

        "PORT": os.getenv(
            "DB_PORT",
            "",
        ),
    }
}


# ==================================================
# CACHE
# ==================================================

REDIS_URL = os.getenv(

    "REDIS_URL",

    "redis://127.0.0.1:6379/1",
)

if ENABLE_REDIS:

    CACHES = {

        "default": {

            "BACKEND": (
                "django_redis.cache.RedisCache"
            ),

            "LOCATION": REDIS_URL,

            "OPTIONS": {

                "CLIENT_CLASS": (
                    "django_redis.client.DefaultClient"
                ),
            },

            "KEY_PREFIX": "ai_cos",
        }
    }

else:

    CACHES = {

        "default": {

            "BACKEND": (
                "django.core.cache.backends.locmem.LocMemCache"
            ),

            "LOCATION": "ai-cos-cache",
        }
    }


# ==================================================
# PASSWORD VALIDATION
# ==================================================

AUTH_PASSWORD_VALIDATORS = [

    {

        "NAME": (
            "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
        ),
    },

    {

        "NAME": (
            "django.contrib.auth.password_validation.MinimumLengthValidator"
        ),
    },

    {

        "NAME": (
            "django.contrib.auth.password_validation.CommonPasswordValidator"
        ),
    },

    {

        "NAME": (
            "django.contrib.auth.password_validation.NumericPasswordValidator"
        ),
    },
]


# ==================================================
# INTERNATIONALIZATION
# ==================================================

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Kolkata"

USE_I18N = True

USE_TZ = True


# ==================================================
# STATIC FILES
# ==================================================

STATIC_URL = "/static/"

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

STATIC_ROOT = (
    BASE_DIR / "staticfiles"
)


# ==================================================
# MEDIA FILES
# ==================================================

MEDIA_URL = "/media/"

MEDIA_ROOT = (
    BASE_DIR / "media"
)


# ==================================================
# REQUEST LIMITS
# ==================================================

DATA_UPLOAD_MAX_MEMORY_SIZE = (
    5 * 1024 * 1024
)

FILE_UPLOAD_MAX_MEMORY_SIZE = (
    5 * 1024 * 1024
)


# ==================================================
# REST FRAMEWORK
# ==================================================

REST_FRAMEWORK = {

    # ==========================================
    # RENDERERS
    # ==========================================

    "DEFAULT_RENDERER_CLASSES": [

        "rest_framework.renderers.JSONRenderer",

        "rest_framework.renderers.BrowsableAPIRenderer",
    ],

    # ==========================================
    # PARSERS
    # ==========================================

    "DEFAULT_PARSER_CLASSES": [

        "rest_framework.parsers.JSONParser",

        "rest_framework.parsers.FormParser",

        "rest_framework.parsers.MultiPartParser",
    ],

    # ==========================================
    # AUTH
    # ==========================================

    "DEFAULT_AUTHENTICATION_CLASSES": [],

    # ==========================================
    # PERMISSIONS
    # ==========================================

    "DEFAULT_PERMISSION_CLASSES": [

        "rest_framework.permissions.AllowAny",
    ],

    # ==========================================
    # THROTTLING
    # ==========================================

    "DEFAULT_THROTTLE_CLASSES": [

        "rest_framework.throttling.AnonRateThrottle",

        "rest_framework.throttling.UserRateThrottle",
    ],

    "DEFAULT_THROTTLE_RATES": {

        "anon": "30/min",

        "user": "200/min",
    },

    # ==========================================
    # PAGINATION
    # ==========================================

    "DEFAULT_PAGINATION_CLASS": (
        "rest_framework.pagination.PageNumberPagination"
    ),

    "PAGE_SIZE": 10,

    # ==========================================
    # SCHEMA
    # ==========================================

    "DEFAULT_SCHEMA_CLASS": (
        "drf_spectacular.openapi.AutoSchema"
    ),
}


# ==================================================
# OPENAPI
# ==================================================

SPECTACULAR_SETTINGS = {

    "TITLE": "AI COS API",

    "DESCRIPTION": (
        "AI Content Operating System"
    ),

    "VERSION": "2.0.0",

    "SERVE_INCLUDE_SCHEMA": False,
}


# ==================================================
# LOGGING
# ==================================================

LOGS_DIR = BASE_DIR / "logs"

LOGS_DIR.mkdir(
    exist_ok=True
)

LOGGING = {

    "version": 1,

    "disable_existing_loggers": False,

    "formatters": {

        "standard": {

            "format": (
                "[{asctime}] "
                "{levelname} "
                "{name} "
                "{message}"
            ),

            "style": "{",
        },
    },

    "handlers": {

        "console": {

            "class": (
                "logging.StreamHandler"
            ),

            "formatter": (
                "standard"
            ),
        },

        "file": {

            "class": (
                "logging.FileHandler"
            ),

            "filename": (
                LOGS_DIR / "app.log"
            ),

            "formatter": (
                "standard"
            ),
        },
    },

    "loggers": {

        "django.request": {

            "handlers": [
                "console",
                "file",
            ],

            "level": "WARNING",

            "propagate": False,
        },
    },

    "root": {

        "handlers": [

            "console",

            "file",
        ],

        "level": "INFO",
    },
}


# ==================================================
# CELERY
# ==================================================

if ENABLE_CELERY:

    CELERY_BROKER_URL = os.getenv(

        "CELERY_BROKER_URL",

        REDIS_URL,
    )

    CELERY_RESULT_BACKEND = os.getenv(

        "CELERY_RESULT_BACKEND",

        REDIS_URL,
    )

    CELERY_ACCEPT_CONTENT = [
        "json",
    ]

    CELERY_TASK_SERIALIZER = (
        "json"
    )

    CELERY_RESULT_SERIALIZER = (
        "json"
    )

    CELERY_TIMEZONE = TIME_ZONE

    CELERY_ENABLE_UTC = True

    CELERY_TASK_TRACK_STARTED = True

    CELERY_TASK_TIME_LIMIT = (
        30 * 60
    )

    CELERY_TASK_SOFT_TIME_LIMIT = (
        25 * 60
    )

    CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True

    CELERY_WORKER_PREFETCH_MULTIPLIER = 1

    CELERY_TASK_ACKS_LATE = True

    CELERY_WORKER_CONCURRENCY = int(

        os.getenv(
            "CELERY_WORKER_CONCURRENCY",
            2,
        )
    )

    CELERY_TASK_DEFAULT_QUEUE = (
        "default"
    )

    CELERY_TASK_ROUTES = {

        "apps.generator.tasks.*": {

            "queue": "generation",
        },

        "apps.memory.tasks.*": {

            "queue": "memory",
        },
    }

    CELERY_BEAT_SCHEDULE = {

        "memory-health-check": {

            "task": (
                "apps.memory.tasks.health_check"
            ),

            "schedule": 300.0,
        },
    }


# ==================================================
# AI PROVIDERS
# ==================================================

AI_PROVIDERS = {

    "openai": {

        "api_key": os.getenv(
            "OPENAI_API_KEY"
        ),
    },

    "gemini": {

        "api_key": os.getenv(
            "GEMINI_API_KEY"
        ),
    },
}


# ==================================================
# AI CONFIG
# ==================================================

MAX_REWRITE_LOOPS = int(
    os.getenv(
        "MAX_REWRITE_LOOPS",
        3,
    )
)

TARGET_REWRITE_SCORE = int(
    os.getenv(
        "TARGET_REWRITE_SCORE",
        85,
    )
)

REQUEST_TIMEOUT = 60

AI_PROVIDER_TIMEOUT = 120


# ==================================================
# MEMORY CONFIG
# ==================================================

MEMORY_TOP_K = 5

MEMORY_SIMILARITY_THRESHOLD = 0.75

ENABLE_MEMORY = True


# ==================================================
# CORS
# ==================================================

CORS_ALLOW_ALL_ORIGINS = DEBUG


# ==================================================
# SECURITY HEADERS
# ==================================================

SESSION_COOKIE_HTTPONLY = True

CSRF_COOKIE_HTTPONLY = True

SESSION_COOKIE_SAMESITE = "Lax"

CSRF_COOKIE_SAMESITE = "Lax"

X_FRAME_OPTIONS = "DENY"

SECURE_CONTENT_TYPE_NOSNIFF = True

SECURE_BROWSER_XSS_FILTER = True

SECURE_REFERRER_POLICY = (
    "strict-origin"
)


# ==================================================
# API CONFIG
# ==================================================

API_VERSION = "v1"

API_NAME = "AI COS API"

API_TIMEOUT = 60


# ==================================================
# DEFAULT PRIMARY KEY
# ==================================================

DEFAULT_AUTO_FIELD = (
    "django.db.models.BigAutoField"
)