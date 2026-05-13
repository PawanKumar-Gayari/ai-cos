"""
Competitor intelligence engine.
"""

import time

from apps.competitor.services.competitor_service import (
    CompetitorService,
)

from utils.keyword_normalizer import (
    KeywordNormalizer,
)

from utils.helpers import (
    Helpers,
)

from utils.logger import (
    competitor_logger,
)

from utils.exceptions import (
    CompetitorException,
    KeywordValidationException,
)


class CompetitorEngine:

    def __init__(self):

        self.competitor_service = (
            CompetitorService()
        )

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

        if len(normalized) < 3:

            raise (
                KeywordValidationException(
                    "Keyword is too short."
                )
            )

        return normalized

    def analyze(
        self,
        keyword,
        include_serp=True,
        include_gaps=True,
        include_weaknesses=True,
    ):

        """
        Run competitor intelligence analysis.
        """

        start_time = time.time()

        competitor_logger.info(

            f"Competitor engine started "
            f"for keyword: {keyword}"
        )

        try:

            # ==========================================
            # VALIDATE KEYWORD
            # ==========================================

            keyword = (
                self.validate_keyword(
                    keyword
                )
            )

            # ==========================================
            # RUN ANALYSIS
            # ==========================================

            result = (
                self.competitor_service.analyze(
                    keyword
                )
            )

            # ==========================================
            # OPTIONAL FILTERS
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
            # ENGINE METADATA
            # ==========================================

            existing_metadata = (
                result.get(
                    "engine_metadata",
                    {}
                )
            )

            existing_metadata.update({

                "engine": (
                    "competitor_intelligence"
                ),

                "version": "2.1.0",

                "execution_time": (
                    execution_time
                ),

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

            result["engine_metadata"] = (
                existing_metadata
            )

            competitor_logger.info(

                f"Competitor engine completed "
                f"in {execution_time}s"
            )

            return result

        except Exception as error:

            competitor_logger.exception(

                f"Competitor engine failed: "
                f"{str(error)}"
            )

            raise CompetitorException(

                f"Competitor engine failed: "
                f"{str(error)}"
            )