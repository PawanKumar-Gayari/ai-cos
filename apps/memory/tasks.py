"""
Memory background tasks.
"""

from celery import shared_task


@shared_task
def health_check():

    """
    Memory system health check.
    """

    return {

        "memory": "healthy",

        "status": "active",
    }