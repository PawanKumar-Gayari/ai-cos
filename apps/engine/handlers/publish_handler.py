"""
Publishing pipeline handler.
"""

from apps.publisher.engine import (
    PublisherEngine,
)


class PublishHandler:

    def __init__(self):

        # =========================
        # PUBLISHER ENGINE
        # =========================

        self.publisher_engine = (
            PublisherEngine()
        )

    def execute(
        self,
        verified_content
    ):

        # =========================
        # PUBLISH CONTENT
        # =========================

        return (
            self.publisher_engine.publish(
                verified_content
            )
        )