"""
Publisher exceptions.
"""

from __future__ import annotations


# =========================================================
# BASE EXCEPTION
# =========================================================

class PublisherException(
    Exception
):
    """
    Base publisher exception.
    """

    default_message = (
        "Publisher error occurred."
    )

    def __init__(
        self,
        message: str | None = None,
    ):

        self.message = (
            message
            or self.default_message
        )

        super().__init__(
            self.message
        )


# =========================================================
# WORDPRESS EXCEPTIONS
# =========================================================

class WordPressConnectionException(
    PublisherException
):
    """
    Raised when WordPress
    connection fails.
    """

    default_message = (
        "Failed to connect to WordPress."
    )


class WordPressAuthenticationException(
    PublisherException
):
    """
    Raised when WordPress
    authentication fails.
    """

    default_message = (
        "WordPress authentication failed."
    )


class WordPressTimeoutException(
    PublisherException
):
    """
    Raised when WordPress
    request times out.
    """

    default_message = (
        "WordPress request timed out."
    )


class WordPressPublishException(
    PublisherException
):
    """
    Raised when article
    publishing fails.
    """

    default_message = (
        "Failed to publish article."
    )


# =========================================================
# ARTICLE EXCEPTIONS
# =========================================================

class ArticleNotFoundException(
    PublisherException
):
    """
    Raised when article
    does not exist.
    """

    default_message = (
        "Article not found."
    )


class InvalidArticleException(
    PublisherException
):
    """
    Raised when article
    validation fails.
    """

    default_message = (
        "Invalid article data."
    )


class EmptyArticleContentException(
    PublisherException
):
    """
    Raised when article
    content is empty.
    """

    default_message = (
        "Article content is empty."
    )


# =========================================================
# PUBLISHING EXCEPTIONS
# =========================================================

class PublishRetryLimitException(
    PublisherException
):
    """
    Raised when retry limit
    exceeds maximum attempts.
    """

    default_message = (
        "Maximum publish retries exceeded."
    )


class DuplicatePublishException(
    PublisherException
):
    """
    Raised when duplicate
    publish attempt occurs.
    """

    default_message = (
        "Article already published."
    )


class PublishTaskException(
    PublisherException
):
    """
    Raised when background
    publish task fails.
    """

    default_message = (
        "Publish task failed."
    )


# =========================================================
# API EXCEPTIONS
# =========================================================

class PublisherAPIException(
    PublisherException
):
    """
    Raised when publisher
    API request fails.
    """

    default_message = (
        "Publisher API error."
    )


class InvalidAPIResponseException(
    PublisherException
):
    """
    Raised when invalid API
    response received.
    """

    default_message = (
        "Invalid API response."
    )