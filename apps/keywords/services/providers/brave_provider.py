"""
Production Brave Search Provider
--------------------------------

Independent web search provider.

Features:
- privacy-focused search
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


class BraveProvider(
    BaseProvider
):

    # =============================================
    # PROVIDER CONFIG
    # =============================================

    PROVIDER_NAME = "brave"

    BASE_URL = (
        "https://api.search.brave.com/res/v1/web/search"
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

            response = requests.get(

                cls.BASE_URL,

                headers={

                    "Accept":
                    "application/json",

                    "X-Subscription-Token":
                    settings.BRAVE_API_KEY,
                },

                params={

                    "q":
                    keyword,

                    "count":
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

            # =====================================
            # HTTP ERROR
            # =====================================

            response.raise_for_status()

            # =====================================
            # JSON DATA
            # =====================================

            data = response.json()

            web_results = (

                data.get(
                    "web",
                    {},
                )
                .get(
                    "results",
                    [],
                )
            )

            results = []

            # =====================================
            # NORMALIZE RESULTS
            # =====================================

            for item in web_results:

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
                            "description",
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