"""
Enterprise WordPress API Client
-------------------------------

Production-grade WordPress connector client.

Features:
- retry-safe requests
- timeout-safe publishing
- API authentication
- SEO metadata support
- featured image support
- category/tag support
- health monitoring
- response validation
- production-safe orchestration
"""

from __future__ import annotations

import json
import logging
import os
import time

from typing import Any

import requests

from requests import Response

from requests.exceptions import (

    ConnectionError,

    RequestException,

    Timeout,
)

from apps.publisher.constants import (

    CONTENT_TYPE_JSON,

    DEFAULT_TIMEOUT,

    DEFAULT_USER_AGENT,

    HEADER_AUTHORIZATION,

    HEADER_CONTENT_TYPE,

    HEADER_USER_AGENT,

    HTTP_CREATED,

    HTTP_OK,

    WORDPRESS_POSTS_ENDPOINT,
)

from apps.publisher.exceptions import (

    InvalidAPIResponseException,

    WordPressAuthenticationException,

    WordPressConnectionException,

    WordPressPublishException,

    WordPressTimeoutException,
)


logger = logging.getLogger(
    __name__
)


# =========================================================
# WORDPRESS CLIENT
# =========================================================

class WordPressClient:

    """
    Enterprise WordPress API client.
    """

    MAX_RETRIES = 3

    RETRY_DELAY = 2

    # =====================================================
    # INIT
    # =====================================================

    def __init__(
        self,
    ):

        self.wordpress_url = os.getenv(

            "WORDPRESS_URL",

            "",
        ).rstrip("/")

        self.api_key = os.getenv(

            "WORDPRESS_API_KEY",

            "",
        )

        if not self.wordpress_url:

            raise (
                WordPressConnectionException(
                    "WORDPRESS_URL missing."
                )
            )

        # =================================================
        # ENDPOINTS
        # =================================================

        self.health_api = (

            f"{self.wordpress_url}"
            "/wp-json/aicos/v1/health"
        )

        self.publish_api = (

            f"{self.wordpress_url}"
            "/wp-json/aicos/v1/publish"
        )

        self.posts_api = (

            f"{self.wordpress_url}"
            f"{WORDPRESS_POSTS_ENDPOINT}"
        )

        # =================================================
        # HEADERS
        # =================================================

        self.headers = {

            HEADER_CONTENT_TYPE: (
                CONTENT_TYPE_JSON
            ),

            "Accept": (
                CONTENT_TYPE_JSON
            ),

            HEADER_USER_AGENT: (
                DEFAULT_USER_AGENT
            ),
        }

        if self.api_key:

            self.headers[
                HEADER_AUTHORIZATION
            ] = (

                f"Bearer {self.api_key}"
            )

        self.session = (
            requests.Session()
        )

        logger.info(
            "WordPress client initialized."
        )

    # =====================================================
    # SAFE JSON
    # =====================================================

    def safe_json(
        self,
        response,
    ):

        try:

            return response.json()

        except json.JSONDecodeError:

            logger.error(

                "Invalid JSON response "
                "| response=%s",

                response.text,
            )

            raise (
                InvalidAPIResponseException(
                    "Invalid JSON response."
                )
            )

    # =====================================================
    # REQUEST
    # =====================================================

    def request(
        self,
        method,
        url,
        **kwargs,
    ):

        for attempt in range(

            1,

            self.MAX_RETRIES + 1,
        ):

            try:

                extra_headers = kwargs.pop(

                    "headers",

                    {},
                )

                headers = {

                    **self.headers,

                    **extra_headers,
                }

                started = time.time()

                response = (

                    self.session.request(

                        method=method,

                        url=url,

                        headers=headers,

                        timeout=(
                            DEFAULT_TIMEOUT
                        ),

                        **kwargs,
                    )
                )

                latency = round(

                    time.time()
                    - started,

                    2,
                )

                logger.info(

                    "WordPress request "
                    "| method=%s "
                    "| status=%s "
                    "| latency=%ss "
                    "| url=%s",

                    method,

                    response.status_code,

                    latency,

                    url,
                )

                return response

            except Timeout as error:

                logger.exception(

                    "WordPress timeout "
                    "| attempt=%s "
                    "| error=%s",

                    attempt,

                    error,
                )

                if attempt >= (
                    self.MAX_RETRIES
                ):

                    raise (
                        WordPressTimeoutException(
                            str(error)
                        )
                    )

            except ConnectionError as error:

                logger.exception(

                    "WordPress connection failed "
                    "| attempt=%s "
                    "| error=%s",

                    attempt,

                    error,
                )

                if attempt >= (
                    self.MAX_RETRIES
                ):

                    raise (
                        WordPressConnectionException(
                            str(error)
                        )
                    )

            except RequestException as error:

                logger.exception(

                    "WordPress request failed "
                    "| attempt=%s "
                    "| error=%s",

                    attempt,

                    error,
                )

                if attempt >= (
                    self.MAX_RETRIES
                ):

                    raise (
                        WordPressConnectionException(
                            str(error)
                        )
                    )

            time.sleep(
                attempt
            )

    # =====================================================
    # HANDLE RESPONSE
    # =====================================================

    def handle_response(
        self,
        response: Response,
    ):

        data = (
            self.safe_json(
                response
            )
        )

        if response.status_code in [

            HTTP_OK,

            HTTP_CREATED,
        ]:

            return {

                "success": True,

                "data": data,
            }

        if response.status_code == 401:

            raise (
                WordPressAuthenticationException(
                    "Authentication failed."
                )
            )

        raise (
            WordPressPublishException(

                data.get(

                    "message",

                    "WordPress API error.",
                )
            )
        )

    # =====================================================
    # TEST CONNECTION
    # =====================================================

    def test_connection(
        self,
    ):

        logger.info(
            "Testing WordPress connection."
        )

        response = self.request(

            "GET",

            self.health_api,
        )

        return self.handle_response(
            response
        )

    # =====================================================
    # BUILD PAYLOAD
    # =====================================================

    def build_payload(

        self,

        title,

        content,

        status="draft",

        excerpt=None,

        slug=None,

        categories=None,

        tags=None,

        featured_image=None,
    ):

        payload = {

            "title": title,

            "content": content,

            "status": status,
        }

        if excerpt:

            payload[
                "excerpt"
            ] = excerpt

        if slug:

            payload[
                "slug"
            ] = slug

        if categories:

            payload[
                "categories"
            ] = categories

        if tags:

            payload[
                "tags"
            ] = tags

        if featured_image:

            payload[
                "featured_image"
            ] = featured_image

        return payload

    # =====================================================
    # CREATE POST
    # =====================================================

    def create_post(

        self,

        title,

        content,

        status="draft",

        excerpt=None,

        slug=None,

        categories=None,

        tags=None,

        featured_image=None,
    ):

        payload = self.build_payload(

            title=title,

            content=content,

            status=status,

            excerpt=excerpt,

            slug=slug,

            categories=categories,

            tags=tags,

            featured_image=(
                featured_image
            ),
        )

        logger.info(

            "Creating WordPress post "
            "| status=%s "
            "| title=%s",

            status,

            title,
        )

        response = self.request(

            "POST",

            self.publish_api,

            json=payload,
        )

        result = (
            self.handle_response(
                response
            )
        )

        data = result.get(
            "data",
            {},
        )

        logger.info(

            "WordPress post created "
            "| post_id=%s",

            data.get(
                "post_id"
            ),
        )

        return {

            "success": True,

            "post_id": data.get(
                "post_id"
            ),

            "status": data.get(
                "status"
            ),

            "url": data.get(
                "url"
            ),

            "response": data,
        }

    # =====================================================
    # CREATE DRAFT
    # =====================================================

    def create_draft(

        self,

        title,

        content,

        excerpt=None,
    ):

        return self.create_post(

            title=title,

            content=content,

            excerpt=excerpt,

            status="draft",
        )

    # =====================================================
    # PUBLISH POST
    # =====================================================

    def publish_post(

        self,

        title,

        content,

        excerpt=None,
    ):

        return self.create_post(

            title=title,

            content=content,

            excerpt=excerpt,

            status="publish",
        )

    # =====================================================
    # CLIENT HEALTH
    # =====================================================

    def health_check(
        self,
    ):

        try:

            connection = (
                self.test_connection()
            )

            return {

                "success": True,

                "wordpress": (
                    self.wordpress_url
                ),

                "connected": True,

                "response": connection,
            }

        except Exception as error:

            logger.exception(

                f"WordPress health failed: "
                f"{str(error)}"
            )

            return {

                "success": False,

                "connected": False,

                "error": str(error),
            }