"""
Production SEO Intelligence Constants
-------------------------------------

Enterprise-grade centralized constants
for the SEO Intelligence Engine.

Features:
- search intent classification
- SEO scoring thresholds
- keyword validation rules
- trend analysis settings
- semantic processing
- provider configuration
- cache management
- security hardening
- scalable architecture
- OCI optimized
"""

from __future__ import annotations

from typing import (
    Final,
)


# =========================================================
# ENGINE METADATA
# =========================================================

ENGINE_NAME: Final[str] = (
    "SEO Intelligence Engine"
)

ENGINE_VERSION: Final[str] = (
    "3.0.0"
)

ENGINE_AUTHOR: Final[str] = (
    "AI COS"
)


# =========================================================
# SEARCH INTENTS
# =========================================================

INTENT_INFORMATIONAL: Final[str] = (
    "informational"
)

INTENT_COMMERCIAL: Final[str] = (
    "commercial"
)

INTENT_TRANSACTIONAL: Final[str] = (
    "transactional"
)

INTENT_NAVIGATIONAL: Final[str] = (
    "navigational"
)

INTENT_COMPARISON: Final[str] = (
    "comparison"
)

INTENT_LOCAL: Final[str] = (
    "local"
)

VALID_INTENTS: Final[set[str]] = {

    INTENT_INFORMATIONAL,

    INTENT_COMMERCIAL,

    INTENT_TRANSACTIONAL,

    INTENT_NAVIGATIONAL,

    INTENT_COMPARISON,

    INTENT_LOCAL,
}


# =========================================================
# SEO DIFFICULTY LEVELS
# =========================================================

DIFFICULTY_LOW: Final[str] = (
    "low"
)

DIFFICULTY_MEDIUM: Final[str] = (
    "medium"
)

DIFFICULTY_HIGH: Final[str] = (
    "high"
)

DIFFICULTY_VERY_HIGH: Final[str] = (
    "very_high"
)

VALID_DIFFICULTY_LEVELS: Final[
    set[str]
] = {

    DIFFICULTY_LOW,

    DIFFICULTY_MEDIUM,

    DIFFICULTY_HIGH,

    DIFFICULTY_VERY_HIGH,
}


# =========================================================
# TREND STATES
# =========================================================

TREND_STABLE: Final[str] = (
    "stable"
)

TREND_RISING: Final[str] = (
    "rising"
)

TREND_DECLINING: Final[str] = (
    "declining"
)

TREND_BREAKOUT: Final[str] = (
    "breakout"
)

VALID_TRENDS: Final[set[str]] = {

    TREND_STABLE,

    TREND_RISING,

    TREND_DECLINING,

    TREND_BREAKOUT,
}


# =========================================================
# SEO SCORE LIMITS
# =========================================================

SEO_SCORE_MIN: Final[int] = 0

SEO_SCORE_MAX: Final[int] = 100

SEO_SCORE_EXCELLENT: Final[int] = 85

SEO_SCORE_GOOD: Final[int] = 70

SEO_SCORE_AVERAGE: Final[int] = 50

SEO_SCORE_POOR: Final[int] = 30


# =========================================================
# TREND SCORE LIMITS
# =========================================================

TREND_SCORE_MIN: Final[int] = 0

TREND_SCORE_MAX: Final[int] = 100


# =========================================================
# KEYWORD VALIDATION
# =========================================================

MIN_KEYWORD_LENGTH: Final[int] = 3

MAX_KEYWORD_LENGTH: Final[int] = 150

MAX_KEYWORD_WORDS: Final[int] = 20

MIN_KEYWORD_SCORE: Final[int] = 0

MAX_KEYWORD_SCORE: Final[int] = 100


# =========================================================
# BLOCKED KEYWORDS
# =========================================================

BLOCKED_KEYWORDS: Final[
    set[str]
] = {

    "",

    " ",

    "null",

    "none",

    "undefined",

    "string",

    "test",

    "testing",

    "asdf",

    "admin",

    "administrator",

    "root",

    "null value",

    "sample",

    "dummy",

    "unknown",
}


# =========================================================
# CONTENT ANALYSIS
# =========================================================

MIN_CONTENT_WORDS: Final[int] = (
    300
)

IDEAL_CONTENT_WORDS: Final[int] = (
    2000
)

MAX_CONTENT_WORDS: Final[int] = (
    10000
)

IDEAL_HEADING_COUNT: Final[int] = (
    15
)

IDEAL_FAQ_COUNT: Final[int] = (
    8
)


# =========================================================
# READABILITY SETTINGS
# =========================================================

MAX_SENTENCE_LENGTH: Final[int] = (
    30
)

MAX_PARAGRAPH_SENTENCES: Final[
    int
] = 6

IDEAL_READABILITY_SCORE: Final[
    int
] = 70


# =========================================================
# SEMANTIC ANALYSIS
# =========================================================

MAX_SEMANTIC_KEYWORDS: Final[
    int
] = 25

MAX_RELATED_TOPICS: Final[
    int
] = 15

MAX_ENTITY_EXTRACTION: Final[
    int
] = 20


# =========================================================
# CLUSTERING SETTINGS
# =========================================================

DEFAULT_CLUSTER_COUNT: Final[
    int
] = 5

MAX_CLUSTER_COUNT: Final[int] = (
    20
)

DEFAULT_CLUSTER_KEYWORDS_LIMIT: (
    Final[int]
) = 100


# =========================================================
# CACHE SETTINGS
# =========================================================

SEO_CACHE_TIMEOUT: Final[int] = (
    60 * 60
)

SERP_CACHE_TIMEOUT: Final[int] = (
    60 * 30
)

KEYWORD_CACHE_TIMEOUT: Final[
    int
] = (

    60 * 60 * 6
)

TREND_CACHE_TIMEOUT: Final[int] = (
    60 * 60 * 3
)


# =========================================================
# PROVIDER LIMITS
# =========================================================

MAX_SERP_RESULTS: Final[int] = (
    10
)

MAX_COMPETITOR_ANALYSIS: (
    Final[int]
) = 5

MAX_ANALYZED_PAGES: Final[int] = (
    3
)

MAX_PROVIDER_TIMEOUT: Final[int] = (
    20
)


# =========================================================
# PAGE ANALYZER
# =========================================================

MAX_HEADINGS_PER_PAGE: (
    Final[int]
) = 20

MAX_FAQS_PER_PAGE: Final[int] = (
    10
)


# =========================================================
# API LIMITS
# =========================================================

MAX_API_KEYWORD_LENGTH: (
    Final[int]
) = 255

MAX_API_RESULTS_LIMIT: Final[int] = (
    50
)


# =========================================================
# SECURITY SETTINGS
# =========================================================

SAFE_LOG_TRUNCATION_LENGTH: (
    Final[int]
) = 300

MAX_INPUT_PAYLOAD_SIZE: (
    Final[int]
) = 5000

MAX_REQUESTS_PER_MINUTE: (
    Final[int]
) = 60


# =========================================================
# DEFAULT LANGUAGE
# =========================================================

DEFAULT_LANGUAGE: Final[str] = (
    "english"
)


# =========================================================
# DEFAULT COMPETITION LEVEL
# =========================================================

DEFAULT_COMPETITION_LEVEL: (
    Final[str]
) = "unknown"