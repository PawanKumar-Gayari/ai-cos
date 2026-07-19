"""
Cleanup publishing tasks.
"""

from __future__ import annotations

import logging

from apps.publisher.models import (
    PublishedPost,
)

logger = logging.getLogger(
    __name__
)


# =========================================================
# CLEANUP OLD FAILURES
# =========================================================

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