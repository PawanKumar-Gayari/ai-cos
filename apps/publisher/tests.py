"""
Publisher tests.
"""

from __future__ import annotations

from unittest.mock import patch

from django.test import (
    TestCase,
)

from rest_framework.test import (
    APIClient,
)

from apps.engine.models import (
    Article,
)

from apps.publisher.models import (
    PublishedPost,
)

from apps.publisher.services.publish_service import (
    PublishService,
)


# =========================================================
# HEALTH API TESTS
# =========================================================

class HealthAPIViewTests(
    TestCase
):

    def setUp(
        self,
    ):

        self.client = (
            APIClient()
        )

    def test_health_api(
        self,
    ):

        response = self.client.get(
            "/api/publisher/health/"
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        self.assertTrue(
            response.data["success"]
        )


# =========================================================
# PUBLISH SERVICE TESTS
# =========================================================

class PublishServiceTests(
    TestCase
):

    def setUp(
        self,
    ):

        self.article = Article.objects.create(

            title="Test Article",

            content=(
                "This is test content."
            ),
        )

        self.service = (
            PublishService()
        )

    # =====================================================
    # TEST DRAFT PUBLISH
    # =====================================================

    @patch(
        "apps.publisher.clients.wordpress_client.WordPressClient.create_post"
    )
    def test_create_draft_success(
        self,
        mock_create_post,
    ):

        mock_create_post.return_value = {

            "success": True,

            "post_id": "123",

            "status": "draft",

            "url": (
                "https://example.com/test"
            ),
        }

        result = (
            self.service.create_draft(
                self.article
            )
        )

        self.assertTrue(
            result["success"]
        )

        self.assertEqual(

            result["status"],

            "draft",
        )

        tracker = (
            PublishedPost.objects.first()
        )

        self.assertEqual(

            tracker.status,

            PublishedPost.STATUS_DRAFT,
        )

    # =====================================================
    # TEST LIVE PUBLISH
    # =====================================================

    @patch(
        "apps.publisher.clients.wordpress_client.WordPressClient.create_post"
    )
    def test_publish_live_success(
        self,
        mock_create_post,
    ):

        mock_create_post.return_value = {

            "success": True,

            "post_id": "456",

            "status": "publish",

            "url": (
                "https://example.com/live"
            ),
        }

        result = (
            self.service.publish_live(
                self.article
            )
        )

        self.assertTrue(
            result["success"]
        )

        tracker = (
            PublishedPost.objects.first()
        )

        self.assertEqual(

            tracker.status,

            PublishedPost.STATUS_PUBLISHED,
        )

    # =====================================================
    # TEST FAILED PUBLISH
    # =====================================================

    @patch(
        "apps.publisher.clients.wordpress_client.WordPressClient.create_post"
    )
    def test_publish_failure(
        self,
        mock_create_post,
    ):

        mock_create_post.return_value = {

            "success": False,

            "error": (
                "WordPress API failed."
            ),
        }

        result = (
            self.service.publish_live(
                self.article
            )
        )

        self.assertFalse(
            result["success"]
        )

        tracker = (
            PublishedPost.objects.first()
        )

        self.assertEqual(

            tracker.status,

            PublishedPost.STATUS_FAILED,
        )

    # =====================================================
    # TEST EMPTY ARTICLE
    # =====================================================

    def test_empty_article(
        self,
    ):

        self.article.content = ""
        self.article.save()

        result = (
            self.service.publish_live(
                self.article
            )
        )

        self.assertFalse(
            result["success"]
        )


# =========================================================
# PUBLISH API TESTS
# =========================================================

class PublishAPIViewTests(
    TestCase
):

    def setUp(
        self,
    ):

        self.client = (
            APIClient()
        )

        self.article = (
            Article.objects.create(

                title="API Test",

                content="API content",
            )
        )

    @patch(
        "apps.publisher.clients.wordpress_client.WordPressClient.create_post"
    )
    def test_publish_api(
        self,
        mock_create_post,
    ):

        mock_create_post.return_value = {

            "success": True,

            "post_id": "999",

            "status": "draft",

            "url": (
                "https://example.com/api"
            ),
        }

        response = self.client.post(

            "/api/publisher/publish/",

            {

                "article_id": (
                    self.article.id
                ),

                "publish": False,
            },

            format="json",
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        self.assertTrue(
            response.data["success"]
        )


# =========================================================
# SERIALIZER TESTS
# =========================================================

class SerializerValidationTests(
    TestCase
):

    def setUp(
        self,
    ):

        self.client = (
            APIClient()
        )

    def test_generate_validation(
        self,
    ):

        response = self.client.post(

            "/api/publisher/generate/",

            {},

            format="json",
        )

        self.assertEqual(
            response.status_code,
            400,
        )

        self.assertFalse(
            response.data["success"]
        )

    def test_publish_validation(
        self,
    ):

        response = self.client.post(

            "/api/publisher/publish/",

            {},

            format="json",
        )

        self.assertEqual(
            response.status_code,
            400,
        )

        self.assertFalse(
            response.data["success"]
        )