"""
Publishing service.
"""

from __future__ import annotations

import logging
from typing import Any

from django.utils import timezone

from apps.publisher.clients.wordpress_client import (
    WordPressClient,
)

from apps.publisher.models import (
    PublishedPost,
)


logger = logging.getLogger(
    __name__
)


class PublishService:

    # ==================================================
    # INIT
    # ==================================================

    def __init__(
        self,
    ):

        self.wordpress = (
            WordPressClient()
        )

    # ==================================================
    # CREATE TRACKER
    # ==================================================

    def _create_tracker(
        self,
        article,
    ) -> PublishedPost:

        return PublishedPost.objects.create(

            article=article,

            status=(
                PublishedPost.STATUS_PENDING
            ),

            publish_attempts=1,
        )

    # ==================================================
    # UPDATE FAILED TRACKER
    # ==================================================

    def _mark_failed(
        self,
        tracker: PublishedPost,
        error_message: str,
        response_data: dict | None = None,
    ) -> None:

        tracker.status = (
            PublishedPost.STATUS_FAILED
        )

        tracker.error_message = (
            error_message
        )

        if response_data:

            tracker.response_data = (
                response_data
            )

        tracker.save()

    # ==================================================
    # UPDATE SUCCESS TRACKER
    # ==================================================

    def _mark_success(
        self,
        tracker: PublishedPost,
        response: dict,
        publish: bool,
    ) -> None:

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

        tracker.published_at = (
            timezone.now()
        )

        if publish:

            tracker.status = (
                PublishedPost.STATUS_PUBLISHED
            )

        else:

            tracker.status = (
                PublishedPost.STATUS_DRAFT
            )

        tracker.save()

    # ==================================================
    # PUBLISH ARTICLE
    # ==================================================

    def publish_article(
        self,
        article,
        publish: bool = False,
    ) -> dict[str, Any]:

        # ==========================================
        # VALIDATE ARTICLE
        # ==========================================

        if not article:

            return {

                "success": False,

                "error": (
                    "Article is required"
                ),
            }

        title = getattr(
            article,
            "title",
            None,
        )

        content = getattr(
            article,
            "content",
            None,
        )

        meta_description = getattr(
            article,
            "meta_description",
            "",
        )

        if not title:

            return {

                "success": False,

                "error": (
                    "Article title missing"
                ),
            }

        if not content:

            return {

                "success": False,

                "error": (
                    "Article content missing"
                ),
            }

        logger.info(

            "Publishing started "
            "| article_id=%s",

            article.id,
        )

        # ==========================================
        # TRACKER
        # ==========================================

        tracker = self._create_tracker(
            article
        )

        # ==========================================
        # STATUS
        # ==========================================

        status = "draft"

        if publish:

            status = "publish"

        # ==========================================
        # WORDPRESS REQUEST
        # ==========================================

        try:

            response = (

                self.wordpress.create_post(

                    title=title,

                    content=content,

                    excerpt=meta_description,

                    status=status,
                )
            )

            # ======================================
            # FAILED
            # ======================================

            if not response.get(
                "success"
            ):

                error_message = response.get(
                    "error",
                    "Unknown publishing error",
                )

                logger.error(

                    "Publishing failed "
                    "| article_id=%s "
                    "| error=%s",

                    article.id,

                    error_message,
                )

                self._mark_failed(

                    tracker=tracker,

                    error_message=(
                        error_message
                    ),

                    response_data=response,
                )

                return {

                    "success": False,

                    "status": (
                        "failed"
                    ),

                    "tracker_id": (
                        tracker.id
                    ),

                    "error": (
                        error_message
                    ),

                    "response": response,
                }

            # ======================================
            # SUCCESS
            # ======================================

            self._mark_success(

                tracker=tracker,

                response=response,

                publish=publish,
            )

            # ======================================
            # UPDATE ARTICLE
            # ======================================

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

            logger.info(

                "Publishing successful "
                "| article_id=%s "
                "| wordpress_post_id=%s",

                article.id,

                response.get(
                    "post_id"
                ),
            )

            return {

                "success": True,

                "status": (
                    response.get(
                        "status"
                    )
                ),

                "article_id": (
                    article.id
                ),

                "tracker_id": (
                    tracker.id
                ),

                "wordpress_post_id": (

                    response.get(
                        "post_id"
                    )
                ),

                "url": (
                    response.get(
                        "url"
                    )
                ),

                "response": response,
            }

        except Exception as error:

            logger.exception(

                "Publish service failed "
                "| article_id=%s "
                "| error=%s",

                article.id,

                error,
            )

            self._mark_failed(

                tracker=tracker,

                error_message=str(
                    error
                ),
            )

            return {

                "success": False,

                "status": "failed",

                "tracker_id": (
                    tracker.id
                ),

                "error": str(error),
            }

    # ==================================================
    # CREATE DRAFT
    # ==================================================

    def create_draft(
        self,
        article,
    ) -> dict[str, Any]:

        return self.publish_article(

            article=article,

            publish=False,
        )

    # ==================================================
    # PUBLISH LIVE
    # ==================================================

    def publish_live(
        self,
        article,
    ) -> dict[str, Any]:

        return self.publish_article(

            article=article,

            publish=True,
        )

    # ==================================================
    # TEST CONNECTION
    # ==================================================

    def test_connection(
        self,
    ) -> dict[str, Any]:

        logger.info(
            "Testing WordPress connection."
        )

        return (
            self.wordpress.test_connection()
        )