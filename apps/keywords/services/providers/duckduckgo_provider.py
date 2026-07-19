"""
Production DuckDuckGo Provider
------------------------------

Lightweight free search provider.

Features:
- free fallback provider
- lightweight search
- normalized results
- duplicate cleanup
- OCI optimized
- production-safe
- stable DDGS integration
"""

from __future__ import annotations

import logging

from ddgs import DDGS

from .base_provider import (
    BaseProvider,
)


logger = logging.getLogger(__name__)


class DuckDuckGoProvider(
    BaseProvider
):

    # =============================================
    # PROVIDER CONFIG
    # =============================================

    PROVIDER_NAME = "duckduckgo"

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

        results = []

        try:

            # =====================================
            # SEARCH
            # =====================================

            with DDGS() as ddgs:

                search_results = ddgs.text(

                    query=keyword,

                    max_results=max_results,
                )

                for item in search_results:

                    results.append(

                        cls.normalize_result(

                            title=
                            item.get(
                                "title",
                                "",
                            ),

                            url=
                            item.get(
                                "href",
                                "",
                            ),

                            description=
                            item.get(
                                "body",
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

            logger.info(

                f"{cls.PROVIDER_NAME} "
                f"extracted "
                f"{len(processed_results)} "
                f"results."
            )

            cls.log_success(
                len(processed_results)
            )

            return processed_results

        # =========================================
        # FAILURE
        # =========================================

        except Exception as error:

            logger.exception(

                f"{cls.PROVIDER_NAME} "
                f"search failed."
            )

            cls.log_failure(error)

            raise