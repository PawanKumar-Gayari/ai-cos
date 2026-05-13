"""
Central configuration system for AI COS.
"""

import os

from dotenv import load_dotenv


# ==================================================
# LOAD ENV
# ==================================================

load_dotenv()


class Config:

    # ==================================================
    # PROJECT
    # ==================================================

    PROJECT_NAME = "AI COS"

    PROJECT_VERSION = "1.0.0"

    ENVIRONMENT = os.getenv(

        "ENVIRONMENT",

        "development"
    )

    DEBUG = os.getenv(

        "DEBUG",

        "True"
    ) == "True"

    # ==================================================
    # AI PROVIDERS
    # ==================================================

    OPENAI_API_KEY = os.getenv(
        "OPENAI_API_KEY"
    )

    GEMINI_API_KEY = os.getenv(
        "GEMINI_API_KEY"
    )

    DEFAULT_AI_PROVIDER = os.getenv(

        "DEFAULT_AI_PROVIDER",

        "openai"
    )

    AI_MAX_RETRIES = int(

        os.getenv(

            "AI_MAX_RETRIES",

            3
        )
    )

    AI_TIMEOUT = int(

        os.getenv(

            "AI_TIMEOUT",

            60
        )
    )

    # ==================================================
    # CONTENT GENERATION
    # ==================================================

    DEFAULT_CONTENT_LENGTH = 2000

    MAX_CONTENT_LENGTH = 10000

    DEFAULT_LANGUAGE = "en"

    # ==================================================
    # SEO SETTINGS
    # ==================================================

    MIN_TITLE_LENGTH = 30

    MAX_TITLE_LENGTH = 60

    MIN_META_DESCRIPTION = 120

    MAX_META_DESCRIPTION = 160

    MIN_KEYWORD_DENSITY = 0.5

    MAX_KEYWORD_DENSITY = 2.5

    IDEAL_HEADING_COUNT = 7

    # ==================================================
    # DISCOVERY ENGINE
    # ==================================================

    MAX_DISCOVERY_KEYWORDS = 100

    DEFAULT_DISCOVERY_LIMIT = 20

    MIN_KEYWORD_LENGTH = 3

    # ==================================================
    # COMPETITOR ENGINE
    # ==================================================

    MAX_COMPETITORS = 10

    MIN_CONTENT_WORDS = 1500

    IDEAL_CONTENT_WORDS = 3000

    MIN_STRUCTURE_SECTIONS = 5

    # ==================================================
    # SCORING
    # ==================================================

    MAX_SCORE = 100

    MIN_SCORE = 0

    HIGH_SCORE_THRESHOLD = 80

    MEDIUM_SCORE_THRESHOLD = 50

    LOW_SCORE_THRESHOLD = 30

    # ==================================================
    # LOGGING
    # ==================================================

    LOG_LEVEL = os.getenv(

        "LOG_LEVEL",

        "INFO"
    )

    LOG_AI_REQUESTS = True

    LOG_PIPELINES = True

    LOG_ERRORS = True

    # ==================================================
    # WORDPRESS
    # ==================================================

    WORDPRESS_URL = os.getenv(
        "WORDPRESS_URL"
    )

    WORDPRESS_USERNAME = os.getenv(
        "WORDPRESS_USERNAME"
    )

    WORDPRESS_PASSWORD = os.getenv(
        "WORDPRESS_PASSWORD"
    )

    # ==================================================
    # CELERY / REDIS
    # ==================================================

    REDIS_URL = os.getenv(

        "REDIS_URL",

        "redis://127.0.0.1:6379/0"
    )

    # ==================================================
    # API LIMITS
    # ==================================================

    DEFAULT_PAGE_SIZE = 10

    MAX_PAGE_SIZE = 100

    REQUEST_TIMEOUT = 30

    # ==================================================
    # FUTURE SETTINGS
    # ==================================================

    ENABLE_LOCAL_AI = False

    ENABLE_LEARNING_ENGINE = False

    ENABLE_ANALYTICS = False

    ENABLE_AUTO_PUBLISH = False