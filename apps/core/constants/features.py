"""
Enterprise feature flags.
"""

import os


# ==================================================
# ENV BOOLEAN PARSER
# ==================================================

def env_bool(
    key,
    default=False,
):

    """
    Convert environment variable
    to boolean safely.
    """

    return (
        os.getenv(
            key,
            str(default),
        ).strip().lower()
        in [
            "true",
            "1",
            "yes",
            "on",
        ]
    )


# ==================================================
# CORE FEATURES
# ==================================================

ENABLE_REDIS = env_bool(
    "ENABLE_REDIS",
    False,
)

ENABLE_CELERY = env_bool(
    "ENABLE_CELERY",
    False,
)

ENABLE_ASYNC_GENERATION = env_bool(
    "ENABLE_ASYNC_GENERATION",
    False,
)


# ==================================================
# AI FEATURES
# ==================================================

ENABLE_MEMORY = env_bool(
    "ENABLE_MEMORY",
    True,
)

ENABLE_MONITORING = env_bool(
    "ENABLE_MONITORING",
    True,
)

ENABLE_ANALYTICS = env_bool(
    "ENABLE_ANALYTICS",
    True,
)

ENABLE_PROVIDER_FALLBACK = env_bool(
    "ENABLE_PROVIDER_FALLBACK",
    True,
)

ENABLE_SMART_ROUTING = env_bool(
    "ENABLE_SMART_ROUTING",
    True,
)


# ==================================================
# SECURITY FEATURES
# ==================================================

ENABLE_API_THROTTLING = env_bool(
    "ENABLE_API_THROTTLING",
    True,
)

ENABLE_REQUEST_LOGGING = env_bool(
    "ENABLE_REQUEST_LOGGING",
    True,
)

ENABLE_SECURITY_HEADERS = env_bool(
    "ENABLE_SECURITY_HEADERS",
    True,
)


# ==================================================
# DEVELOPMENT FEATURES
# ==================================================

ENABLE_API_DOCS = env_bool(
    "ENABLE_API_DOCS",
    True,
)

ENABLE_DEBUG_TOOLBAR = env_bool(
    "ENABLE_DEBUG_TOOLBAR",
    False,
)


# ==================================================
# FEATURE EXPORT
# ==================================================

FEATURE_FLAGS = {

    # ==========================================
    # CORE
    # ==========================================

    "redis": ENABLE_REDIS,

    "celery": ENABLE_CELERY,

    "async_generation": (
        ENABLE_ASYNC_GENERATION
    ),

    # ==========================================
    # AI
    # ==========================================

    "memory": ENABLE_MEMORY,

    "monitoring": (
        ENABLE_MONITORING
    ),

    "analytics": (
        ENABLE_ANALYTICS
    ),

    "provider_fallback": (
        ENABLE_PROVIDER_FALLBACK
    ),

    "smart_routing": (
        ENABLE_SMART_ROUTING
    ),

    # ==========================================
    # SECURITY
    # ==========================================

    "api_throttling": (
        ENABLE_API_THROTTLING
    ),

    "request_logging": (
        ENABLE_REQUEST_LOGGING
    ),

    "security_headers": (
        ENABLE_SECURITY_HEADERS
    ),

    # ==========================================
    # DEV
    # ==========================================

    "api_docs": (
        ENABLE_API_DOCS
    ),

    "debug_toolbar": (
        ENABLE_DEBUG_TOOLBAR
    ),
}


# ==================================================
# HELPERS
# ==================================================

def feature_enabled(
    feature_name,
):

    """
    Check feature status safely.
    """

    return FEATURE_FLAGS.get(
        feature_name,
        False,
    )


def enabled_features():

    """
    Return active features.
    """

    return {

        key: value

        for key, value in (
            FEATURE_FLAGS.items()
        )

        if value
    }


def disabled_features():

    """
    Return disabled features.
    """

    return {

        key: value

        for key, value in (
            FEATURE_FLAGS.items()
        )

        if not value
    }