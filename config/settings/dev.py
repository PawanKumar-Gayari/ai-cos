"""
Development settings.
"""

from .base import *

import os


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
]


# ==================================================
# DEVELOPMENT DATABASE
# ==================================================

DATABASES = {

    "default": {

        "ENGINE": (
            "django.db.backends.sqlite3"
        ),

        "NAME": (
            BASE_DIR / "db.sqlite3"
        ),
    }
}


# ==================================================
# DEVELOPMENT CACHE
# ==================================================

REDIS_URL = (
    "redis://127.0.0.1:6379/1"
)


# ==================================================
# CELERY CONFIGURATION
# ==================================================

CELERY_BROKER_URL = (
    "redis://127.0.0.1:6379/0"
)

CELERY_RESULT_BACKEND = (
    "redis://127.0.0.1:6379/0"
)


# ==================================================
# EMAIL BACKEND
# ==================================================

EMAIL_BACKEND = (
    "django.core.mail.backends.console.EmailBackend"
)


# ==================================================
# LOGGING
# ==================================================

LOGGING["root"]["level"] = (
    "INFO"
)


# ==================================================
# DEVELOPMENT SECURITY
# ==================================================

SESSION_COOKIE_SECURE = False

CSRF_COOKIE_SECURE = False

SECURE_SSL_REDIRECT = False


# ==================================================
# DEVELOPMENT FEATURES
# ==================================================

ENABLE_API_DOCS = True

ENABLE_MEMORY = True

ENABLE_ASYNC_GENERATION = True


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
# DEVELOPMENT CORS
# ==================================================

CORS_ALLOW_ALL_ORIGINS = True


# ==================================================
# LOCAL AI
# ==================================================

OLLAMA_BASE_URL = (
    "http://localhost:11434"
)

OLLAMA_MODEL = (
    "tinyllama"
)