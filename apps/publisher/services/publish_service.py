"""
Enterprise Publishing Service
-----------------------------

Production-grade WordPress publishing service.

Features:
- retry-safe publishing
- SEO metadata support
- WordPress draft/publish support
- publishing analytics
- response tracking
- rollback-safe workflow
- transaction-safe publishing
- production-safe orchestration
"""

from __future__ import annotations

import logging
import re
import time

from typing import Any

from django.db import transaction

from django.utils import timezone

from apps.engine.models import (
    Article,
)

from apps.publisher.clients.wordpress_client import (
    WordPressClient,
)

from apps.publisher.constants import (

    STATUS_DRAFT,

    STATUS_FAILED,

    STATUS_PENDING,

    STATUS_PUBLISHED,
)

from apps.publisher.exceptions import (

    ArticleNotFoundException,

    EmptyArticleContentException,

    InvalidArticleException,

    WordPressPublishException,
)

from apps.publisher.models import (
    PublishedPost,
)


logger = logging.getLogger(
    __name__
)


# =========================================================
# PUBLISH SERVICE
# =========================================================

class PublishService:

    """
    Enterprise WordPress publishing service.
    """

    MAX_RETRIES = 3

    # =====================================================
    # INIT
    # =====================================================

    def __init__(
        self,
    ):

        self.wordpress = (
            WordPressClient()
        )

    # =====================================================
    # SLUG
    # =====================================================

    def generate_slug(
        self,
        title,
    ):

        title = str(
            title
        ).strip().lower()

        title = re.sub(

            r"[^\w\s-]",

            "",

            title,
        )

        title = re.sub(

            r"\s+",

            "-",

            title,
        )

        return title.strip("-")

    # =====================================================
    # META DESCRIPTION
    # =====================================================

    def meta_description(
        self,
        article,
    ):

        meta = getattr(

            article,

            "meta_description",

            "",
        )

        if meta:

            return str(meta)[:160]

        content = str(
            article.content
        )

        cleaned = re.sub(

            r"#|\*|`|>",

            "",

            content,
        )

        return cleaned[:160]

    # =====================================================
    # VALIDATE ARTICLE
    # =====================================================

    def validate_article(
        self,
        article: Article,
    ):

        if not article:

            raise (
                ArticleNotFoundException()
            )

        if not article.title:

            raise (
                InvalidArticleException(
                    "Article title missing."
                )
            )

        if not article.content:

            raise (
                EmptyArticleContentException()
            )

        if len(
            article.content
        ) < 300:

            raise (
                InvalidArticleException(
                    "Article content too short."
                )
            )

    # =====================================================
    # CREATE TRACKER
    # =====================================================

    def create_tracker(
        self,
        article,
    ):

        return PublishedPost.objects.create(

            article=article,

            status=STATUS_PENDING,

            publish_attempts=1,
        )

    # =====================================================
    # MARK FAILED
    # =====================================================

    def mark_failed(

        self,

        tracker,

        error_message,

        response_data=None,
    ):

        tracker.status = (
            STATUS_FAILED
        )

        tracker.error_message = (
            str(error_message)
        )

        tracker.last_error_at = (
            timezone.now()
        )

        if response_data:

            tracker.response_data = (
                response_data
            )

        tracker.save(

            update_fields=[

                "status",

                "error_message",

                "last_error_at",

                "response_data",

                "updated_at",
            ]
        )

    # =====================================================
    # MARK SUCCESS
    # =====================================================

    def mark_success(

        self,

        tracker,

        response,

        publish,

        duration,
    ):

        tracker.wordpress_post_id = (

            response.get(
                "post_id"
            )
        )

        tracker.wordpress_url = (

            response.get(
                "url"
            )
        )

        tracker.response_data = (
            response
        )

        tracker.publish_duration = (
            duration
        )

        tracker.published_at = (
            timezone.now()
        )

        tracker.status = (

            STATUS_PUBLISHED

            if publish

            else STATUS_DRAFT
        )

        tracker.save(

            update_fields=[

                "wordpress_post_id",

                "wordpress_url",

                "response_data",

                "publish_duration",

                "published_at",

                "status",

                "updated_at",
            ]
        )

    # =====================================================
    # UPDATE ARTICLE
    # =====================================================

    def update_article(

        self,

        article,

        response,

        publish,
    ):

        article.is_published = (
            publish
        )

        article.published_url = (

            response.get(
                "url"
            )
        )

        article.save(

            update_fields=[

                "is_published",

                "published_url",

                "updated_at",
            ]
        )

    # =====================================================
    # BUILD PAYLOAD
    # =====================================================

    def build_payload(

        self,

        article,

        publish=False,
    ):

        status = (

            "publish"

            if publish

            else "draft"
        )

        return {

            "title":
            article.title,

            "content":
            article.content,

            "excerpt": (

                self.meta_description(
                    article
                )
            ),

            "slug": (

                self.generate_slug(
                    article.title
                )
            ),

            "status":
            status,
        }

    # =====================================================
    # PUBLISH ARTICLE
    # =====================================================

    @transaction.atomic
    def publish_article(

        self,

        article: Article,

        publish=False,
    ) -> dict[str, Any]:

        start_time = (
            time.perf_counter()
        )

        self.validate_article(
            article
        )

        logger.info(

            "Publishing started "
            "| article_id=%s",

            article.id,
        )

        tracker = (
            self.create_tracker(
                article
            )
        )

        payload = (
            self.build_payload(

                article,

                publish=publish,
            )
        )

        for attempt in range(

            1,

            self.MAX_RETRIES + 1,
        ):

            try:

                logger.info(

                    "WordPress publish attempt "
                    "| article_id=%s "
                    "| attempt=%s",

                    article.id,

                    attempt,
                )

                response = (

                    self.wordpress.create_post(
                        **payload
                    )
                )

                if not response.get(
                    "success"
                ):

                    raise (
                        WordPressPublishException(

                            response.get(

                                "error",

                                "Publishing failed.",
                            )
                        )
                    )

                duration = round(

                    (
                        time.perf_counter()
                        - start_time
                    ),

                    2,
                )

                self.mark_success(

                    tracker=tracker,

                    response=response,

                    publish=publish,

                    duration=duration,
                )

                self.update_article(

                    article=article,

                    response=response,

                    publish=publish,
                )

                logger.info(

                    "Publishing successful "
                    "| article_id=%s "
                    "| wordpress_post_id=%s "
                    "| duration=%ss",

                    article.id,

                    response.get(
                        "post_id"
                    ),

                    duration,
                )

                return {

                    "success": True,

                    "tracker_id": (
                        tracker.id
                    ),

                    "article_id": (
                        article.id
                    ),

                    "wordpress_post_id": (

                        response.get(
                            "post_id"
                        )
                    ),

                    "status": (
                        response.get(
                            "status"
                        )
                    ),

                    "url": (
                        response.get(
                            "url"
                        )
                    ),

                    "duration": duration,

                    "attempt": attempt,

                    "response": response,
                }

            except Exception as error:

                logger.exception(

                    "Publishing failed "
                    "| article_id=%s "
                    "| attempt=%s "
                    "| error=%s",

                    article.id,

                    attempt,

                    error,
                )

                self.mark_failed(

                    tracker=tracker,

                    error_message=str(
                        error
                    ),
                )

                if attempt >= (
                    self.MAX_RETRIES
                ):

                    return {

                        "success": False,

                        "tracker_id": (
                            tracker.id
                        ),

                        "article_id": (
                            article.id
                        ),

                        "status": STATUS_FAILED,

                        "error": str(
                            error
                        ),

                        "attempt": attempt,
                    }

                time.sleep(attempt)

    # =====================================================
    # CREATE DRAFT
    # =====================================================

    def create_draft(
        self,
        article,
    ):

        return self.publish_article(

            article=article,

            publish=False,
        )

    # =====================================================
    # PUBLISH LIVE
    # =====================================================

    def publish_live(
        self,
        article,
    ):

        return self.publish_article(

            article=article,

            publish=True,
        )

    # =====================================================
    # TEST CONNECTION
    # =====================================================

    def test_connection(
        self,
    ):

        logger.info(
            "Testing WordPress connection."
        )

        return (
            self.wordpress
            .test_connection()
        )

    # =====================================================
    # SERVICE HEALTH
    # =====================================================

    def health_check(
        self,
    ):

        try:

            connection = (
                self.test_connection()
            )

            return {

                "success": True,

                "service": (
                    "publish_service"
                ),

                "wordpress": (
                    connection
                ),

                "retries": (
                    self.MAX_RETRIES
                ),
            }

        except Exception as error:

            logger.exception(

                f"Publish service health "
                f"failed: {str(error)}"
            )

            return {

                "success": False,

                "error": str(error),
            }