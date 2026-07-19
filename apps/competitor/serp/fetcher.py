"""
Real SERP fetcher for competitor intelligence.
"""

import requests

from django.conf import settings

from utils.logger import (
    competitor_logger,
)

from utils.text_cleaner import (
    TextCleaner,
)


class SERPFetcher:

    SERPER_ENDPOINT = (
        "https://google.serper.dev/search"
    )

    DEFAULT_TIMEOUT = 30

    DEFAULT_LIMIT = 10

    def __init__(self):

        self.serper_api_key = getattr(
            settings,
            "SERPER_API_KEY",
            "",
        )

    # ==================================================
    # SAFE CLEAN
    # ==================================================

    def safe_clean(
        self,
        value,
    ):

        if not value:

            return ""

        return TextCleaner.clean(
            str(value)
        )

    # ==================================================
    # NORMALIZE RESULT
    # ==================================================

    def normalize_result(
        self,
        result,
        position,
    ):

        return {

            "position": position,

            "title": self.safe_clean(
                result.get(
                    "title",
                    ""
                )
            ),

            "url": self.safe_clean(
                result.get(
                    "link",
                    ""
                )
            ),

            "snippet": self.safe_clean(
                result.get(
                    "snippet",
                    ""
                )
            ),
        }

    # ==================================================
    # FETCH GOOGLE RESULTS
    # ==================================================

    def fetch_google_results(
        self,
        keyword,
        limit=None,
    ):

        """
        Fetch real Google SERP results.
        """

        competitor_logger.info(

            f"[SERPER FETCH START] "
            f"KEYWORD={keyword}"
        )

        if not limit:

            limit = (
                self.DEFAULT_LIMIT
            )

        # ==========================================
        # API VALIDATION
        # ==========================================

        if not self.serper_api_key:

            competitor_logger.warning(
                "SERPER API key missing."
            )

            return []

        try:

            headers = {

                "X-API-KEY": (
                    self.serper_api_key
                ),

                "Content-Type": (
                    "application/json"
                ),
            }

            payload = {

                "q": keyword,

                "num": limit,
            }

            response = requests.post(

                self.SERPER_ENDPOINT,

                json=payload,

                headers=headers,

                timeout=(
                    self.DEFAULT_TIMEOUT
                ),
            )

            response.raise_for_status()

            data = response.json()

            organic_results = (
                data.get(
                    "organic",
                    []
                )
            )

            normalized_results = []

            for index, result in enumerate(

                organic_results,

                start=1,
            ):

                normalized_results.append(

                    self.normalize_result(

                        result,

                        index,
                    )
                )

            competitor_logger.info(

                f"[SERPER FETCH SUCCESS] "
                f"RESULTS={len(normalized_results)}"
            )

            return normalized_results

        except Exception as error:

            competitor_logger.exception(

                f"[SERPER FETCH FAILED] "
                f"{str(error)}"
            )

            return []