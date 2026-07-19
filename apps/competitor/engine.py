"""
Enterprise competitor intelligence engine.
"""

import time
import logging
import asyncio

from apps.competitor.services.competitor_service import (
    CompetitorService,
)

from utils.keyword_normalizer import (
    KeywordNormalizer,
)

from utils.helpers import (
    Helpers,
)

from utils.exceptions import (

    CompetitorException,

    KeywordValidationException,
)


logger = logging.getLogger(
    __name__
)


class CompetitorEngine:

    """
    Enterprise async competitor engine.
    """

    ANALYSIS_TIMEOUT = 120

    def __init__(
        self
    ):

        self.competitor_service = (
            CompetitorService()
        )

    # ==================================================
    # VALIDATE KEYWORD
    # ==================================================

    def validate_keyword(
        self,
        keyword,
    ):

        """
        Validate competitor keyword.
        """

        if keyword is None:

            raise (
                KeywordValidationException(
                    "Keyword is required."
                )
            )

        keyword = str(
            keyword
        ).strip()

        if not keyword:

            raise (
                KeywordValidationException(
                    "Keyword is empty."
                )
            )

        normalized = (
            KeywordNormalizer.normalize(
                keyword
            )
        )

        if len(
            normalized
        ) < 3:

            raise (
                KeywordValidationException(
                    "Keyword is too short."
                )
            )

        return normalized

    # ==================================================
    # SAFE RESULT
    # ==================================================

    def safe_result(
        self,
        result,
    ):

        """
        Normalize competitor result.
        """

        if not isinstance(
            result,
            dict,
        ):

            return {

                "success": False,

                "analysis_summary": {},

                "serp_results": [],

                "gap_analysis": {},

                "weakness_analysis": {},

                "engine_metadata": {},
            }

        return result

    # ==================================================
    # EXECUTE ANALYSIS
    # ==================================================

    async def execute_analysis(
        self,
        keyword,
    ):

        """
        Async-safe analysis execution.
        """

        result = await asyncio.to_thread(

            self.competitor_service.analyze,

            keyword,
        )

        return result

    # ==================================================
    # ANALYZE
    # ==================================================

    async def analyze(
        self,
        keyword,
        include_serp=True,
        include_gaps=True,
        include_weaknesses=True,
    ):

        """
        Run enterprise competitor analysis.
        """

        start_time = time.time()

        logger.info(

            f"COMPETITOR ENGINE START: "
            f"{keyword}"
        )

        try:

            # ==========================================
            # VALIDATE
            # ==========================================

            keyword = (
                self.validate_keyword(
                    keyword
                )
            )

            logger.info(

                f"VALIDATED KEYWORD: "
                f"{keyword}"
            )

            # ==========================================
            # EXECUTE
            # ==========================================

            result = await asyncio.wait_for(

                self.execute_analysis(
                    keyword
                ),

                timeout=(
                    self.ANALYSIS_TIMEOUT
                ),
            )

            result = (
                self.safe_result(
                    result
                )
            )

            logger.info(
                "COMPETITOR ANALYSIS "
                "COMPLETED"
            )

            # ==========================================
            # FILTERS
            # ==========================================

            if not include_serp:

                result.pop(
                    "serp_results",
                    None,
                )

            if not include_gaps:

                result.pop(
                    "gap_analysis",
                    None,
                )

            if not include_weaknesses:

                result.pop(
                    "weakness_analysis",
                    None,
                )

            # ==========================================
            # EXECUTION TIME
            # ==========================================

            execution_time = (
                Helpers.execution_timer(
                    start_time
                )
            )

            # ==========================================
            # METADATA
            # ==========================================

            metadata = (

                result.get(
                    "engine_metadata",
                    {}
                )

                or {}
            )

            metadata.update({

                "engine": (
                    "competitor_intelligence"
                ),

                "version": "4.0.0",

                "status": "success",

                "execution_time": (
                    execution_time
                ),

                "keyword": keyword,

                "filters": {

                    "include_serp": (
                        include_serp
                    ),

                    "include_gaps": (
                        include_gaps
                    ),

                    "include_weaknesses": (
                        include_weaknesses
                    ),
                },
            })

            result[
                "engine_metadata"
            ] = metadata

            result["success"] = True

            logger.info(

                f"COMPETITOR ENGINE "
                f"COMPLETED IN "
                f"{execution_time}s"
            )

            return result

        except asyncio.TimeoutError:

            logger.exception(
                "Competitor analysis "
                "timed out."
            )

            return {

                "success": False,

                "error": (
                    "Analysis timed out."
                ),

                "analysis_summary": {},

                "serp_results": [],

                "gap_analysis": {},

                "weakness_analysis": {},

                "engine_metadata": {

                    "engine": (
                        "competitor_intelligence"
                    ),

                    "version": "4.0.0",

                    "status": "timeout",
                },
            }

        except Exception as error:

            logger.exception(

                f"Competitor engine failed: "
                f"{str(error)}"
            )

            return {

                "success": False,

                "error": str(error),

                "analysis_summary": {},

                "serp_results": [],

                "gap_analysis": {},

                "weakness_analysis": {},

                "engine_metadata": {

                    "engine": (
                        "competitor_intelligence"
                    ),

                    "version": "4.0.0",

                    "status": "failed",
                },
            }

    # ==================================================
    # QUICK SUMMARY
    # ==================================================

    async def quick_summary(
        self,
        keyword,
    ):

        """
        Lightweight competitor summary.
        """

        result = await self.analyze(

            keyword,

            include_serp=False,

            include_gaps=False,
        )

        return {

            "success": (
                result.get(
                    "success",
                    False,
                )
            ),

            "summary": (

                result.get(
                    "analysis_summary",
                    {}
                )
            ),
        }

    # ==================================================
    # ENGINE STATUS
    # ==================================================

    def engine_status(
        self
    ):

        """
        Engine status.
        """

        return {

            "engine": (
                "competitor_intelligence"
            ),

            "version": "4.0.0",

            "status": "active",

            "timeout": (
                self.ANALYSIS_TIMEOUT
            ),
        }