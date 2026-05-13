"""
Publisher engine.
"""

from apps.publisher.services.publishing_service import (
    PublishingService,
)


class PublisherEngine:

    def __init__(self):

        # =========================
        # PUBLISHING SERVICE
        # =========================

        self.publishing_service = (
            PublishingService()
        )

    def publish(
        self,
        content_data
    ):

        # =========================
        # PUBLISH CONTENT
        # =========================

        return (
            self.publishing_service.publish(
                content_data
            )
        )