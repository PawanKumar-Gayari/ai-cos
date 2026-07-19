"""
Publisher constants.
"""

from __future__ import annotations


# =========================================================
# PROVIDERS
# =========================================================

PROVIDER_WORDPRESS = (
    "wordpress"
)


# =========================================================
# PUBLISH METHODS
# =========================================================

PUBLISH_METHOD_REST_API = (
    "rest_api"
)

PUBLISH_METHOD_XMLRPC = (
    "xmlrpc"
)


# =========================================================
# PUBLISH STATUS
# =========================================================

STATUS_PENDING = (
    "pending"
)

STATUS_DRAFT = (
    "draft"
)

STATUS_PUBLISHED = (
    "published"
)

STATUS_FAILED = (
    "failed"
)


# =========================================================
# HTTP STATUS CODES
# =========================================================

HTTP_OK = 200

HTTP_CREATED = 201

HTTP_BAD_REQUEST = 400

HTTP_UNAUTHORIZED = 401

HTTP_FORBIDDEN = 403

HTTP_NOT_FOUND = 404

HTTP_SERVER_ERROR = 500

HTTP_TIMEOUT = 504


# =========================================================
# RETRY CONFIGURATION
# =========================================================

MAX_PUBLISH_RETRIES = 3

RETRY_DELAY_SECONDS = 5


# =========================================================
# REQUEST CONFIGURATION
# =========================================================

DEFAULT_TIMEOUT = 30

DEFAULT_USER_AGENT = (
    "AI-COS-Publisher/1.0"
)


# =========================================================
# WORDPRESS ENDPOINTS
# =========================================================

WORDPRESS_POSTS_ENDPOINT = (
    "/wp-json/wp/v2/posts"
)

WORDPRESS_CATEGORIES_ENDPOINT = (
    "/wp-json/wp/v2/categories"
)

WORDPRESS_TAGS_ENDPOINT = (
    "/wp-json/wp/v2/tags"
)

WORDPRESS_MEDIA_ENDPOINT = (
    "/wp-json/wp/v2/media"
)


# =========================================================
# LOGGING
# =========================================================

LOGGER_NAME = (
    "publisher"
)


# =========================================================
# RESPONSE KEYS
# =========================================================

RESPONSE_SUCCESS = (
    "success"
)

RESPONSE_ERROR = (
    "error"
)

RESPONSE_MESSAGE = (
    "message"
)

RESPONSE_DATA = (
    "data"
)


# =========================================================
# CONTENT TYPES
# =========================================================

CONTENT_TYPE_JSON = (
    "application/json"
)


# =========================================================
# API HEADERS
# =========================================================

HEADER_AUTHORIZATION = (
    "Authorization"
)

HEADER_CONTENT_TYPE = (
    "Content-Type"
)

HEADER_USER_AGENT = (
    "User-Agent"
)


# =========================================================
# WORDPRESS POST STATUS
# =========================================================

WP_STATUS_DRAFT = (
    "draft"
)

WP_STATUS_PUBLISH = (
    "publish"
)

WP_STATUS_PENDING = (
    "pending"
)


# =========================================================
# DEFAULT VALUES
# =========================================================

DEFAULT_LANGUAGE = (
    "en"
)

DEFAULT_CATEGORY = (
    "Uncategorized"
)