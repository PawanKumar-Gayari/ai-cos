"""
Production Google CSE Provider
------------------------------

Google Custom Search provider.

Features:
- Google search results
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


class GoogleCSEProvider(
    BaseProvider
):

    # =============================================
    # PROVIDER CONFIG
    # =============================================

    PROVIDER_NAME = "google_cse"

    BASE_URL = (
        "https://www.googleapis.com/customsearch/v1"
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

                params={

                    "q":
                    keyword,

                    "key":
                    settings.GOOGLE_CSE_API_KEY,

                    "cx":
                    settings.GOOGLE_CSE_ID,

                    "num":
                    min(
                        max_results,
                        10,
                    ),
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

            google_results = data.get(
                "items",
                [],
            )

            results = []

            # =====================================
            # NORMALIZE RESULTS
            # =====================================

            for item in google_results:

                results.append(

                    cls.normalize_result(

                        title=
                        item.get(
                            "title",
                            "",
                        ),

                        url=
                        item.get(
                            "link",
                            "",
                        ),

                        description=
                        item.get(
                            "snippet",
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