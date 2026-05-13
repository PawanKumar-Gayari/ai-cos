"""
AI COS WordPress Connector Client
"""

from __future__ import annotations

import json
import logging
import os
from typing import Any

import requests

from requests.exceptions import (
    RequestException,
)

logger = logging.getLogger(
    __name__
)


class WordPressClient:

    # ==================================================
    # INIT
    # ==================================================

    def __init__(
        self,
    ):

        # ==========================================
        # CONFIG
        # ==========================================

        self.wordpress_url = os.getenv(
            "WORDPRESS_URL",
            "",
        ).rstrip("/")

        self.api_key = os.getenv(
            "WORDPRESS_API_KEY",
            "",
        )

        # ==========================================
        # VALIDATION
        # ==========================================

        if not self.wordpress_url:

            raise ValueError(
                "WORDPRESS_URL is missing"
            )

        # ==========================================
        # AI COS CONNECTOR ENDPOINTS
        # ==========================================

        self.health_api = (

            f"{self.wordpress_url}"
            "/wp-json/aicos/v1/health"
        )

        self.publish_api = (

            f"{self.wordpress_url}"
            "/wp-json/aicos/v1/publish"
        )

        # ==========================================
        # DEFAULT HEADERS
        # ==========================================

        self.headers = {

            "Content-Type": (
                "application/json"
            ),

            "Accept": (
                "application/json"
            ),

            # ======================================
            # Browser-like headers
            # Helps bypass LiteSpeed challenges
            # ======================================

            "User-Agent": (

                "Mozilla/5.0 "
                "(Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 "
                "(KHTML, like Gecko) "
                "Chrome/124.0 Safari/537.36"
            ),
        }

        # ==========================================
        # OPTIONAL API KEY
        # ==========================================

        if self.api_key:

            self.headers[
                "X-AICOS-KEY"
            ] = self.api_key

        logger.info(
            "AI COS WordPress connector initialized."
        )

    # ==================================================
    # COMMON REQUEST
    # ==================================================

    def _request(
        self,
        method: str,
        url: str,
        **kwargs,
    ) -> requests.Response:

        try:

            # ======================================
            # EXTRA HEADERS
            # ======================================

            extra_headers = kwargs.pop(
                "headers",
                {},
            )

            headers = {
                **self.headers,
                **extra_headers,
            }

            response = requests.request(

                method=method,

                url=url,

                headers=headers,

                timeout=60,

                **kwargs,
            )

            logger.info(

                "Connector request "
                "| method=%s "
                "| status=%s "
                "| url=%s",

                method,

                response.status_code,

                url,
            )

            return response

        except RequestException as error:

            logger.exception(

                "Connector request failed: %s",

                error,
            )

            raise

    # ==================================================
    # SAFE JSON RESPONSE
    # ==================================================

    def _safe_json_response(
        self,
        response: requests.Response,
    ) -> dict[str, Any]:

        raw_text = response.text.strip()

        print(
            "\n========== RAW RESPONSE =========="
        )

        print(raw_text)

        print(
            "==================================\n"
        )

        try:

            return response.json()

        except json.JSONDecodeError:

            logger.error(

                "Invalid JSON response "
                "| response=%s",

                raw_text,
            )

            return {

                "success": False,

                "error": (
                    "Invalid JSON response"
                ),

                "raw_response": raw_text,
            }

    # ==================================================
    # TEST CONNECTION
    # ==================================================

    def test_connection(
        self,
    ) -> dict[str, Any]:

        try:

            response = self._request(

                "GET",

                self.health_api,
            )

            data = (
                self._safe_json_response(
                    response
                )
            )

            if response.status_code == 200:

                return {

                    "success": True,

                    "message": (
                        "Connector active"
                    ),

                    "response": data,
                }

            return {

                "success": False,

                "status_code": (
                    response.status_code
                ),

                "error": data,
            }

        except Exception as error:

            logger.exception(

                "Connection test failed: %s",

                error,
            )

            return {

                "success": False,

                "error": str(error),
            }

    # ==================================================
    # CREATE POST
    # ==================================================

    def create_post(
        self,
        title: str,
        content: str,
        status: str = "draft",
        excerpt: str | None = None,
    ) -> dict[str, Any]:

        # ==========================================
        # PAYLOAD
        # ==========================================

        payload = {

            "title": title,

            "content": content,

            "status": status,
        }

        if excerpt:

            payload[
                "excerpt"
            ] = excerpt

        try:

            response = self._request(

                "POST",

                self.publish_api,

                json=payload,
            )

            data = (
                self._safe_json_response(
                    response
                )
            )

            # ======================================
            # FAILED JSON
            # ======================================

            if not data.get(
                "success",
                False,
            ):

                return data

            # ======================================
            # SUCCESS
            # ======================================

            logger.info(

                "Post published successfully "
                "| post_id=%s",

                data.get(
                    "post_id"
                ),
            )

            return {

                "success": True,

                "status": (
                    data.get("status")
                ),

                "post_id": (
                    data.get("post_id")
                ),

                "url": (
                    data.get("url")
                ),

                "response": data,
            }

        except Exception as error:

            logger.exception(

                "Create post failed: %s",

                error,
            )

            return {

                "success": False,

                "error": str(error),
            }

    # ==================================================
    # CREATE DRAFT
    # ==================================================

    def create_draft(
        self,
        title: str,
        content: str,
        excerpt: str | None = None,
    ) -> dict[str, Any]:

        return self.create_post(

            title=title,

            content=content,

            excerpt=excerpt,

            status="draft",
        )

    # ==================================================
    # PUBLISH POST
    # ==================================================

    def publish_post(
        self,
        title: str,
        content: str,
        excerpt: str | None = None,
    ) -> dict[str, Any]:

        return self.create_post(

            title=title,

            content=content,

            excerpt=excerpt,

            status="publish",
        )