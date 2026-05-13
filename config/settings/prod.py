"""
Production settings.
"""

from .base import *

import os


# ==================================================
# DEBUG
# ==================================================

DEBUG = False


# ==================================================
# ALLOWED HOSTS
# ==================================================

ALLOWED_HOSTS = os.getenv(

    "ALLOWED_HOSTS",

    "*",
).split(",")


# ==================================================
# DATABASE
# ==================================================

DATABASES = {

    "default": {

        "ENGINE": os.getenv(
            "DB_ENGINE"
        ),

        "NAME": os.getenv(
            "DB_NAME"
        ),

        "USER": os.getenv(
            "DB_USER"
        ),

        "PASSWORD": os.getenv(
            "DB_PASSWORD"
        ),

        "HOST": os.getenv(
            "DB_HOST"
        ),

        "PORT": os.getenv(
            "DB_PORT"
        ),
    }
}


# ==================================================
# REDIS
# ==================================================

REDIS_URL = os.getenv(
    "REDIS_URL"
)


# ==================================================
# CELERY
# ==================================================

CELERY_BROKER_URL = os.getenv(
    "CELERY_BROKER_URL",
    REDIS_URL,
)

CELERY_RESULT_BACKEND = os.getenv(
    "CELERY_RESULT_BACKEND",
    REDIS_URL,
)


# ==================================================
# SECURITY
# ==================================================

SESSION_COOKIE_SECURE = True

CSRF_COOKIE_SECURE = True

SECURE_SSL_REDIRECT = True

SECURE_BROWSER_XSS_FILTER = True

SECURE_CONTENT_TYPE_NOSNIFF = True

X_FRAME_OPTIONS = "DENY"


# ==================================================
# HSTS
# ==================================================

SECURE_HSTS_SECONDS = 31536000

SECURE_HSTS_INCLUDE_SUBDOMAINS = True

SECURE_HSTS_PRELOAD = True


# ==================================================
# STATIC FILES
# ==================================================

STATIC_ROOT = (
    BASE_DIR / "staticfiles"
)

MEDIA_ROOT = (
    BASE_DIR / "media"
)


# ==================================================
# LOGGING
# ==================================================

LOGGING["root"]["level"] = (
    "WARNING"
)


# ==================================================
# API DOCS
# ==================================================

ENABLE_API_DOCS = False


# ==================================================
# AI PROVIDERS
# ==================================================

OPENAI_API_KEY = os.getenv(
    "OPENAI_API_KEY"
)

GEMINI_API_KEY = os.getenv(
    "GEMINI_API_KEY"
)


# ==================================================
# LOCAL AI
# ==================================================

OLLAMA_BASE_URL = os.getenv(

    "OLLAMA_BASE_URL",

    "http://localhost:11434",
)

OLLAMA_MODEL = os.getenv(

    "OLLAMA_MODEL",

    "tinyllama",
)


# ==================================================
# PERFORMANCE
# ==================================================

CONN_MAX_AGE = 60

DATA_UPLOAD_MAX_MEMORY_SIZE = (
    10 * 1024 * 1024
)


# ==================================================
# CACHING
# ==================================================

CACHE_TTL = 60 * 15


# ==================================================
# ASYNC FEATURES
# ==================================================

ENABLE_ASYNC_GENERATION = True

ENABLE_MEMORY = True