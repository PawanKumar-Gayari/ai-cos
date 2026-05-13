"""
Publisher background tasks.
"""

from __future__ import annotations

import logging

from django.db.models import QuerySet

from apps.publisher.models import (
    PublishedPost,
)

from apps.publisher.services.publish_service import (
    PublishService,
)


logger = logging.getLogger(
    __name__
)


# ==================================================
# RETRY FAILED PUBLISHES
# ==================================================

def retry_failed_publishes():

    logger.info(
        "Retry failed publishes started."
    )

    # ==============================================
    # FAILED POSTS
    # ==============================================

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

        "Found failed publish posts=%d",

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

    # ==============================================
    # LOOP POSTS
    # ==============================================

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

            # ======================================
            # INCREMENT ATTEMPTS
            # ======================================

            tracker.publish_attempts += 1

            tracker.save(

                update_fields=[
                    "publish_attempts",
                    "updated_at",
                ]
            )

            # ======================================
            # RETRY PUBLISH
            # ======================================

            result = (

                publish_service.create_draft(
                    article
                )
            )

            if result.get(
                "success"
            ):

                success_count += 1

                logger.info(

                    "Retry publish success "
                    "| tracker_id=%s",

                    tracker.id,
                )

            else:

                failed_count += 1

                logger.warning(

                    "Retry publish failed "
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

                "Retry task crashed "
                "| tracker_id=%s "
                "| error=%s",

                tracker.id,

                error,
            )

    logger.info(

        "Retry task completed "
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


# ==================================================
# CLEANUP OLD FAILURES
# ==================================================

def cleanup_old_failures():

    logger.info(
        "Cleanup old failures started."
    )

    old_failures = (

        PublishedPost.objects.filter(

            status=(
                PublishedPost.STATUS_FAILED
            ),

            publish_attempts__gte=3,
        )
    )

    total = old_failures.count()

    logger.info(

        "Old failed publishes=%d",

        total,
    )

    return {

        "success": True,

        "old_failures": total,
    }


# ==================================================
# PUBLISH HEALTH REPORT
# ==================================================

def publish_health_report():

    total = (
        PublishedPost.objects.count()
    )

    published = (

        PublishedPost.objects.filter(

            status=(
                PublishedPost.STATUS_PUBLISHED
            )
        ).count()
    )

    drafts = (

        PublishedPost.objects.filter(

            status=(
                PublishedPost.STATUS_DRAFT
            )
        ).count()
    )

    failed = (

        PublishedPost.objects.filter(

            status=(
                PublishedPost.STATUS_FAILED
            )
        ).count()
    )

    pending = (

        PublishedPost.objects.filter(

            status=(
                PublishedPost.STATUS_PENDING
            )
        ).count()
    )

    return {

        "total": total,

        "published": published,

        "drafts": drafts,

        "failed": failed,

        "pending": pending,
    }