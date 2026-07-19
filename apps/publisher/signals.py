"""
Publisher signals.
"""

from __future__ import annotations

import logging

from django.db.models.signals import (
    post_save,
)

from django.dispatch import (
    receiver,
)

from apps.publisher.models import (
    PublishedPost,
)

logger = logging.getLogger(
    __name__
)


# =========================================================
# PUBLISHED POST CREATED
# =========================================================

@receiver(
    post_save,
    sender=PublishedPost,
)
def published_post_created(
    sender,
    instance,
    created,
    **kwargs,
):

    if not created:

        return

    logger.info(

        "PublishedPost created "
        "| tracker_id=%s "
        "| article_id=%s "
        "| status=%s",

        instance.id,

        instance.article.id,

        instance.status,
    )


# =========================================================
# PUBLISHED SUCCESS
# =========================================================

@receiver(
    post_save,
    sender=PublishedPost,
)
def published_post_success(
    sender,
    instance,
    created,
    **kwargs,
):

    if created:

        return

    if (
        instance.status
        != PublishedPost.STATUS_PUBLISHED
    ):

        return

    logger.info(

        "Article published successfully "
        "| tracker_id=%s "
        "| article_id=%s "
        "| wordpress_post_id=%s",

        instance.id,

        instance.article.id,

        instance.wordpress_post_id,
    )


# =========================================================
# PUBLISH FAILED
# =========================================================

@receiver(
    post_save,
    sender=PublishedPost,
)
def published_post_failed(
    sender,
    instance,
    created,
    **kwargs,
):

    if created:

        return

    if (
        instance.status
        != PublishedPost.STATUS_FAILED
    ):

        return

    logger.warning(

        "Publishing failed "
        "| tracker_id=%s "
        "| article_id=%s "
        "| attempts=%s "
        "| error=%s",

        instance.id,

        instance.article.id,

        instance.publish_attempts,

        instance.error_message,
    )