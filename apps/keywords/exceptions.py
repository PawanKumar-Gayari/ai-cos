"""
Production SEO Intelligence Exceptions
--------------------------------------

Enterprise-grade centralized exception
handling system.

Features:
- secure API-safe exceptions
- structured error responses
- provider failure handling
- SEO engine validation
- scalable architecture
- OCI optimized
- production-safe
"""

from __future__ import annotations

from typing import (
    Any,
)


# =========================================================
# BASE EXCEPTION
# =========================================================


class KeywordEngineException(
    Exception
):

    """
    Base exception for the
    SEO Intelligence Engine.
    """

    default_message = (
        "Keyword engine error occurred."
    )

    error_code = (
        "KEYWORD_ENGINE_ERROR"
    )

    status_code = 500

    def __init__(
        self,
        message: str | None = None,
        *,
        error_code: str | None = None,
        status_code: int | None = None,
        details: dict[str, Any] | None = None,
    ) -> None:

        self.message = (

            message

            or self.default_message
        )

        self.error_code = (

            error_code

            or self.error_code
        )

        self.status_code = (

            status_code

            or self.status_code
        )

        self.details = (

            details

            or {}
        )

        super().__init__(
            self.message
        )

    # =====================================================
    # SAFE DICT
    # =====================================================

    def to_dict(
        self,
    ) -> dict[str, Any]:

        return {

            "success":
            False,

            "error": {

                "message":
                self.message,

                "error_code":
                self.error_code,

                "status_code":
                self.status_code,

                "details":
                self.details,
            },
        }

    # =====================================================
    # STRING
    # =====================================================

    def __str__(
        self,
    ) -> str:

        return (

            f"{self.error_code}: "
            f"{self.message}"
        )


# =========================================================
# VALIDATION EXCEPTIONS
# =========================================================


class KeywordValidationException(
    KeywordEngineException
):

    """
    Invalid keyword input.
    """

    default_message = (
        "Keyword validation failed."
    )

    error_code = (
        "KEYWORD_VALIDATION_ERROR"
    )

    status_code = 400


class KeywordLengthException(
    KeywordValidationException
):

    """
    Invalid keyword length.
    """

    default_message = (
        "Keyword length is invalid."
    )

    error_code = (
        "KEYWORD_LENGTH_ERROR"
    )


class BlockedKeywordException(
    KeywordValidationException
):

    """
    Blocked keyword detected.
    """

    default_message = (
        "Blocked keyword detected."
    )

    error_code = (
        "BLOCKED_KEYWORD"
    )


class EmptyKeywordException(
    KeywordValidationException
):

    """
    Empty keyword submitted.
    """

    default_message = (
        "Keyword cannot be empty."
    )

    error_code = (
        "EMPTY_KEYWORD"
    )


# =========================================================
# SEO ANALYSIS EXCEPTIONS
# =========================================================


class IntentDetectionException(
    KeywordEngineException
):

    """
    Intent detection failed.
    """

    default_message = (
        "Intent detection failed."
    )

    error_code = (
        "INTENT_DETECTION_ERROR"
    )

    status_code = 500


class ScoringException(
    KeywordEngineException
):

    """
    SEO scoring failed.
    """

    default_message = (
        "SEO scoring failed."
    )

    error_code = (
        "SEO_SCORING_ERROR"
    )

    status_code = 500


class TrendAnalysisException(
    KeywordEngineException
):

    """
    Trend analysis failed.
    """

    default_message = (
        "Trend analysis failed."
    )

    error_code = (
        "TREND_ANALYSIS_ERROR"
    )

    status_code = 500


class DifficultyAnalysisException(
    KeywordEngineException
):

    """
    Difficulty analysis failed.
    """

    default_message = (
        "Difficulty analysis failed."
    )

    error_code = (
        "DIFFICULTY_ANALYSIS_ERROR"
    )

    status_code = 500


class ClusteringException(
    KeywordEngineException
):

    """
    Keyword clustering failed.
    """

    default_message = (
        "Keyword clustering failed."
    )

    error_code = (
        "CLUSTERING_ERROR"
    )

    status_code = 500


class SemanticAnalysisException(
    KeywordEngineException
):

    """
    Semantic analysis failed.
    """

    default_message = (
        "Semantic analysis failed."
    )

    error_code = (
        "SEMANTIC_ANALYSIS_ERROR"
    )

    status_code = 500


class OutlineGenerationException(
    KeywordEngineException
):

    """
    Outline generation failed.
    """

    default_message = (
        "Outline generation failed."
    )

    error_code = (
        "OUTLINE_GENERATION_ERROR"
    )

    status_code = 500


class RecommendationException(
    KeywordEngineException
):

    """
    Recommendation engine failed.
    """

    default_message = (
        "Recommendation generation failed."
    )

    error_code = (
        "RECOMMENDATION_ERROR"
    )

    status_code = 500


# =========================================================
# PROVIDER EXCEPTIONS
# =========================================================


class ExternalProviderException(
    KeywordEngineException
):

    """
    External provider failure.
    """

    default_message = (
        "External provider unavailable."
    )

    error_code = (
        "EXTERNAL_PROVIDER_ERROR"
    )

    status_code = 503


class SERPProviderException(
    ExternalProviderException
):

    """
    SERP provider failed.
    """

    default_message = (
        "SERP provider failed."
    )

    error_code = (
        "SERP_PROVIDER_ERROR"
    )


class ProviderTimeoutException(
    ExternalProviderException
):

    """
    Provider timeout detected.
    """

    default_message = (
        "Provider request timed out."
    )

    error_code = (
        "PROVIDER_TIMEOUT"
    )


class ProviderAuthenticationException(
    ExternalProviderException
):

    """
    Invalid provider credentials.
    """

    default_message = (
        "Provider authentication failed."
    )

    error_code = (
        "PROVIDER_AUTH_ERROR"
    )


# =========================================================
# PAGE ANALYZER EXCEPTIONS
# =========================================================


class PageAnalysisException(
    KeywordEngineException
):

    """
    Competitor page analysis failed.
    """

    default_message = (
        "Page analysis failed."
    )

    error_code = (
        "PAGE_ANALYSIS_ERROR"
    )

    status_code = 500


class InvalidURLException(
    KeywordEngineException
):

    """
    Invalid page URL.
    """

    default_message = (
        "Invalid URL detected."
    )

    error_code = (
        "INVALID_URL"
    )

    status_code = 400


# =========================================================
# SECURITY EXCEPTIONS
# =========================================================


class SuspiciousKeywordException(
    KeywordValidationException
):

    """
    Suspicious keyword detected.
    """

    default_message = (
        "Suspicious keyword detected."
    )

    error_code = (
        "SUSPICIOUS_KEYWORD"
    )

    status_code = 403


class RateLimitException(
    KeywordEngineException
):

    """
    API rate limit exceeded.
    """

    default_message = (
        "Rate limit exceeded."
    )

    error_code = (
        "RATE_LIMIT_EXCEEDED"
    )

    status_code = 429


class UnauthorizedAPIException(
    KeywordEngineException
):

    """
    Unauthorized API access.
    """

    default_message = (
        "Unauthorized API access."
    )

    error_code = (
        "UNAUTHORIZED_API"
    )

    status_code = 401