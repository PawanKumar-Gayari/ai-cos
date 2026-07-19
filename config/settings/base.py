"""
Base Django settings for ai_cos project.
Production-grade optimized configuration.
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
# AI COS API SECURITY
# ==================================================

AICOS_API_KEY = os.getenv(
    "AICOS_API_KEY",
    ""
)


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

    "rest_framework",

    "rest_framework.authtoken",

    "drf_spectacular",

    "corsheaders",
]


# ==================================================
# LOCAL APPS
# ==================================================

LOCAL_APPS = [

    "apps.core",

    "apps.api",

    "apps.memory",

    "apps.engine",

    "apps.generator",

    "apps.verifier",

    "apps.rewriter",

    "apps.discovery",

    "apps.decision_engine",

    "apps.keywords",

    "apps.competitor",

    "apps.publisher",

    "apps.analytics",

    "apps.monitoring",

    "apps.history",

    "apps.llm",

    "apps.dashboard",
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

    "django.middleware.security.SecurityMiddleware",

    "corsheaders.middleware.CorsMiddleware",

    "django.contrib.sessions.middleware.SessionMiddleware",

    "django.middleware.common.CommonMiddleware",

    "django.middleware.csrf.CsrfViewMiddleware",

    "django.contrib.auth.middleware.AuthenticationMiddleware",

    "django.contrib.messages.middleware.MessageMiddleware",

    "django.middleware.clickjacking.XFrameOptionsMiddleware",

    # ==============================================
    # DASHBOARD AUTH
    # ==============================================

    "apps.core.middleware.dashboard_auth.DashboardLoginRequiredMiddleware",

    # ==============================================
    # API SECURITY
    # ==============================================

    "apps.core.middleware.api_auth.APIKeyMiddleware",

    # ==============================================
    # MONITORING
    # ==============================================

    "apps.monitoring.middleware.request_logging.RequestLoggingMiddleware",

    "apps.monitoring.middleware.error_logging.ErrorLoggingMiddleware",
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
    # AUTHENTICATION
    # ==============================================

    "DEFAULT_AUTHENTICATION_CLASSES": [

        # TOKEN AUTH

        "rest_framework.authentication.TokenAuthentication",

        # SESSION AUTH

        "rest_framework.authentication.SessionAuthentication",

        # BASIC AUTH

        "rest_framework.authentication.BasicAuthentication",
    ],

    # ==============================================
    # PERMISSIONS
    # ==============================================

    "DEFAULT_PERMISSION_CLASSES": [

        "rest_framework.permissions.IsAuthenticated",
    ],

    # ==============================================
    # THROTTLING
    # ==============================================

    "DEFAULT_THROTTLE_CLASSES": [

        "rest_framework.throttling.AnonRateThrottle",

        "rest_framework.throttling.UserRateThrottle",
    ],

    # ==============================================
    # THROTTLE RATES
    # ==============================================

    "DEFAULT_THROTTLE_RATES": {

        "anon": "20/min",

        "user": "300/min",
    },

    # ==============================================
    # PAGINATION
    # ==============================================

    "DEFAULT_PAGINATION_CLASS": (
        "rest_framework.pagination.PageNumberPagination"
    ),

    "PAGE_SIZE": 10,

    # ==============================================
    # OPENAPI
    # ==============================================

    "DEFAULT_SCHEMA_CLASS": (
        "drf_spectacular.openapi.AutoSchema"
    ),
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
# SEARCH API KEYS
# ==================================================

SERPAPI_KEY = os.getenv(
    "SERPAPI_KEY",
    ""
)

GOOGLE_CSE_API_KEY = os.getenv(
    "GOOGLE_CSE_API_KEY",
    ""
)

GOOGLE_CSE_ID = os.getenv(
    "GOOGLE_CSE_ID",
    ""
)

BRAVE_API_KEY = os.getenv(
    "BRAVE_API_KEY",
    ""
)

SERPER_API_KEY = os.getenv(
    "SERPER_API_KEY",
    ""
)

TAVILY_API_KEY = os.getenv(
    "TAVILY_API_KEY",
    ""
)


# ==================================================
# DEFAULT PRIMARY KEY
# ==================================================

DEFAULT_AUTO_FIELD = (
    "django.db.models.BigAutoField"
)


# ==================================================
# AUTH REDIRECTS
# ==================================================

LOGIN_URL = "/login/"

LOGIN_REDIRECT_URL = "/dashboard/"

LOGOUT_REDIRECT_URL = "/login/"


# ==================================================
# EMAIL CONFIG
# ==================================================

EMAIL_BACKEND = (
    "django.core.mail.backends.smtp.EmailBackend"
)

EMAIL_HOST = "smtp.gmail.com"

EMAIL_PORT = 587

EMAIL_USE_TLS = True

EMAIL_HOST_USER = os.getenv(
    "EMAIL_HOST_USER"
)

EMAIL_HOST_PASSWORD = os.getenv(
    "EMAIL_HOST_PASSWORD"
)

DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

CONTACT_EMAIL = os.getenv(
    "CONTACT_EMAIL"
)