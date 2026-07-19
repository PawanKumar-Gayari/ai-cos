"""
Production Tavily Provider
--------------------------

AI-powered semantic search provider.

Features:
- semantic web search
- AI-ready results
- normalized responses
- duplicate cleanup
- safe validation
- OCI optimized
- production-safe
"""

from __future__ import annotations

import logging

import requests

from django.conf import settings

from .base_provider import (
    BaseProvider,
)


logger = logging.getLogger(__name__)


class TavilyProvider(
    BaseProvider
):

    # =============================================
    # PROVIDER CONFIG
    # =============================================

    PROVIDER_NAME = "tavily"

    BASE_URL = (
        "https://api.tavily.com/search"
    )

    # =============================================
    # SEARCH
    # =============================================

    @classmethod
    def search(
        cls,
        keyword: str,
        max_results: int = 10,
    ) -> list[dict]:

        logger.info(

            f"{cls.PROVIDER_NAME} "
            f"search started for: "
            f"{keyword}"
        )

        try:

            # =====================================
            # REQUEST
            # =====================================

            response = requests.post(

                cls.BASE_URL,

                json={

                    "api_key":
                    settings.TAVILY_API_KEY,

                    "query":
                    keyword,

                    "max_results":
                    max_results,
                },

                timeout=cls.TIMEOUT,
            )

            # =====================================
            # DEBUG
            # =====================================

            logger.info(

                f"{cls.PROVIDER_NAME} "
                f"status: "
                f"{response.status_code}"
            )

            logger.info(

                f"{cls.PROVIDER_NAME} "
                f"response: "
                f"{response.text[:500]}"
            )

            # =====================================
            # HTTP ERROR
            # =====================================

            response.raise_for_status()

            # =====================================
            # JSON DATA
            # =====================================

            data = response.json()

            tavily_results = data.get(
                "results",
                [],
            )

            results = []

            # =====================================
            # NORMALIZE RESULTS
            # =====================================

            for item in tavily_results:

                results.append(

                    cls.normalize_result(

                        title=
                        item.get(
                            "title",
                            "",
                        ),

                        url=
                        item.get(
                            "url",
                            "",
                        ),

                        description=
                        item.get(
                            "content",
                            "",
                        ),
                    )
                )

            # =====================================
            # PROCESS RESULTS
            # =====================================

            processed_results = (

                cls.process_results(

                    results,

                    max_results,
                )
            )

            cls.log_success(
                len(processed_results)
            )

            return processed_results

        # =========================================
        # FAILURE
        # =========================================

        except Exception as error:

            cls.log_failure(error)

            raise