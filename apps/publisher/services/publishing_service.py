"""
Publishing service for WordPress.
"""

from apps.publisher.clients.wordpress_client import (
    WordPressClient,
)


class PublishingService:

    def __init__(self):

        # =========================
        # WORDPRESS CLIENT
        # =========================

        self.wordpress_client = (
            WordPressClient()
        )

    def publish(
        self,
        content_data
    ):

        # =========================
        # EXTRACT CONTENT
        # =========================

        title = content_data.get(
            "title"
        )

        content = content_data.get(
            "content"
        )

        # =========================
        # PUBLISH POST
        # =========================

        result = (
            self.wordpress_client.publish_post(

                title=title,

                content=content,
            )
        )

        return result