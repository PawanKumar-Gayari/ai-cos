"""
Retry publishing tasks.
"""

from __future__ import annotations

import logging

from django.db import transaction
from django.db.models import QuerySet
from django.utils import timezone

from apps.publisher.models import (
    PublishedPost,
)

from apps.publisher.services.publish_service import (
    PublishService,
)

logger = logging.getLogger(
    __name__
)


# =========================================================
# RETRY FAILED PUBLISHES
# =========================================================

def retry_failed_publishes():

    logger.info(
        "Retry failed publishes started."
    )

    failed_posts: QuerySet = (

        PublishedPost.objects.filter(

            status=(
                PublishedPost.STATUS_FAILED
            ),

            publish_attempts__lt=3,
        )
    )

    total = failed_posts.count()

    logger.info(

        "Failed publishes found=%d",

        total,
    )

    if total == 0:

        return {

            "success": True,

            "message": (
                "No failed publishes found."
            ),

            "retried": 0,
        }

    publish_service = (
        PublishService()
    )

    success_count = 0

    failed_count = 0

    for tracker in failed_posts:

        try:

            article = tracker.article

            logger.info(

                "Retrying publish "
                "| tracker_id=%s "
                "| article_id=%s",

                tracker.id,

                article.id,
            )

            with transaction.atomic():

                tracker.publish_attempts += 1

                tracker.status = (
                    PublishedPost.STATUS_PENDING
                )

                tracker.save(

                    update_fields=[

                        "publish_attempts",

                        "status",

                        "updated_at",
                    ]
                )

            result = (

                publish_service.publish_article(
                    article_id=article.id
                )
            )

            if result.get(
                "success"
            ):

                success_count += 1

                logger.info(

                    "Retry success "
                    "| tracker_id=%s",

                    tracker.id,
                )

            else:

                failed_count += 1

                tracker.status = (
                    PublishedPost.STATUS_FAILED
                )

                tracker.last_error_at = (
                    timezone.now()
                )

                tracker.error_message = (
                    result.get(
                        "error"
                    )
                )

                tracker.save(

                    update_fields=[

                        "status",

                        "last_error_at",

                        "error_message",

                        "updated_at",
                    ]
                )

                logger.warning(

                    "Retry failed "
                    "| tracker_id=%s "
                    "| error=%s",

                    tracker.id,

                    result.get(
                        "error"
                    ),
                )

        except Exception as error:

            failed_count += 1

            logger.exception(

                "Retry crashed "
                "| tracker_id=%s "
                "| error=%s",

                tracker.id,

                error,
            )

    logger.info(

        "Retry completed "
        "| success=%d "
        "| failed=%d",

        success_count,

        failed_count,
    )

    return {

        "success": True,

        "retried": total,

        "successful_retries": (
            success_count
        ),

        "failed_retries": (
            failed_count
        ),
    }