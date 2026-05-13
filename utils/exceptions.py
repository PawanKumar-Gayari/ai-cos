"""
Central exception system for AI COS.
"""


# ==================================================
# BASE EXCEPTION
# ==================================================

class AICOSException(Exception):

    """
    Base exception for all AI COS errors.
    """

    default_message = (
        "An unknown AI COS error occurred."
    )

    def __init__(
        self,
        message=None
    ):

        self.message = (
            message
            or self.default_message
        )

        super().__init__(
            self.message
        )


# ==================================================
# VALIDATION ERRORS
# ==================================================

class ValidationException(
    AICOSException
):

    default_message = (
        "Validation failed."
    )


class KeywordValidationException(
    ValidationException
):

    default_message = (
        "Keyword validation failed."
    )


class ContentValidationException(
    ValidationException
):

    default_message = (
        "Content validation failed."
    )


# ==================================================
# AI ERRORS
# ==================================================

class AIException(
    AICOSException
):

    default_message = (
        "AI provider error occurred."
    )


class OpenAIException(
    AIException
):

    default_message = (
        "OpenAI request failed."
    )


class GeminiException(
    AIException
):

    default_message = (
        "Gemini request failed."
    )


class LocalAIException(
    AIException
):

    default_message = (
        "Local AI engine failed."
    )


class AIRateLimitException(
    AIException
):

    default_message = (
        "AI provider rate limit exceeded."
    )


# ==================================================
# DISCOVERY ERRORS
# ==================================================

class DiscoveryException(
    AICOSException
):

    default_message = (
        "Discovery engine error."
    )


class KeywordCollectionException(
    DiscoveryException
):

    default_message = (
        "Keyword collection failed."
    )


class TrendCollectionException(
    DiscoveryException
):

    default_message = (
        "Trend collection failed."
    )


# ==================================================
# COMPETITOR ERRORS
# ==================================================

class CompetitorException(
    AICOSException
):

    default_message = (
        "Competitor analysis failed."
    )


class SERPExtractionException(
    CompetitorException
):

    default_message = (
        "SERP extraction failed."
    )


class GapAnalysisException(
    CompetitorException
):

    default_message = (
        "Gap analysis failed."
    )


class WeaknessDetectionException(
    CompetitorException
):

    default_message = (
        "Weakness detection failed."
    )


# ==================================================
# SEO ERRORS
# ==================================================

class SEOException(
    AICOSException
):

    default_message = (
        "SEO processing failed."
    )


class SEOScoreException(
    SEOException
):

    default_message = (
        "SEO scoring failed."
    )


class KeywordDensityException(
    SEOException
):

    default_message = (
        "Keyword density calculation failed."
    )


# ==================================================
# PUBLISHING ERRORS
# ==================================================

class PublishingException(
    AICOSException
):

    default_message = (
        "Publishing failed."
    )


class WordPressPublishingException(
    PublishingException
):

    default_message = (
        "WordPress publishing failed."
    )


# ==================================================
# PIPELINE ERRORS
# ==================================================

class PipelineException(
    AICOSException
):

    default_message = (
        "Pipeline execution failed."
    )


class OrchestratorException(
    PipelineException
):

    default_message = (
        "Orchestrator execution failed."
    )


# ==================================================
# STORAGE / DATABASE ERRORS
# ==================================================

class StorageException(
    AICOSException
):

    default_message = (
        "Storage operation failed."
    )


class ArticleSaveException(
    StorageException
):

    default_message = (
        "Failed to save article."
    )