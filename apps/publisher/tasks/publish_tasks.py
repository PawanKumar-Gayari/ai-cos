"""
Publishing tasks.
"""

from __future__ import annotations

import logging

from apps.publisher.services.publish_service import (
    PublishService,
)

logger = logging.getLogger(
    __name__
)


# =========================================================
# PUBLISH ARTICLE
# =========================================================

def publish_article_task(
    article_id: int,
):

    logger.info(

        "Publish task started "
        "| article_id=%s",

        article_id,
    )

    publish_service = (
        PublishService()
    )

    return (
        publish_service.publish_article(
            article_id=article_id
        )
    )