"""
Competitor intelligence service.
"""

import time

from apps.competitor.serp.extractor import (
    SERPExtractor,
)

from apps.competitor.analyzer.content_analyzer import (
    ContentAnalyzer,
)

from apps.competitor.analyzer.structure_analyzer import (
    StructureAnalyzer,
)

from apps.competitor.analyzer.gap_finder import (
    GapFinder,
)

from apps.competitor.analyzer.weakness_detector import (
    WeaknessDetector,
)

from apps.competitor.scoring.competitor_score import (
    CompetitorScore,
)

from apps.monitoring.models import (
    EngineExecution,
)

from utils.helpers import (
    Helpers,
)

from utils.logger import (
    competitor_logger,
)

from utils.exceptions import (
    CompetitorException,
)


class CompetitorService:

    def __init__(
        self
    ):

        # ==========================================
        # SERP EXTRACTION
        # ==========================================

        self.serp_extractor = (
            SERPExtractor()
        )

        # ==========================================
        # ANALYZERS
        # ==========================================

        self.content_analyzer = (
            ContentAnalyzer()
        )

        self.structure_analyzer = (
            StructureAnalyzer()
        )

        self.gap_finder = (
            GapFinder()
        )

        self.weakness_detector = (
            WeaknessDetector()
        )

        # ==========================================
        # SCORING
        # ==========================================

        self.competitor_score = (
            CompetitorScore()
        )

    # ==================================================
    # SAVE ENGINE EXECUTION
    # ==================================================

    def save_engine_execution(
        self,
        keyword,
        execution_time,
        status,
        score=0,
    ):

        """
        Save competitor engine execution.
        """

        try:

            EngineExecution.objects.create(

                engine_name=(
                    "competitor_engine"
                ),

                keyword=keyword,

                execution_time=(
                    execution_time
                ),

                status=status,

                score=score,
            )

        except Exception as error:

            competitor_logger.exception(

                f"[ENGINE EXECUTION SAVE FAILED] "
                f"{str(error)}"
            )

    # ==================================================
    # BUILD SUMMARY
    # ==================================================

    def build_analysis_summary(
        self,
        competition_analysis,
        gap_analysis,
        weakness_analysis,
    ):

        """
        Build compact analysis summary.
        """

        return {

            "competition_level": (
                competition_analysis.get(
                    "competition_level"
                )
            ),

            "seo_opportunity": (
                competition_analysis.get(
                    "seo_opportunity"
                )
            ),

            "gap_count": (
                gap_analysis.get(
                    "total_gaps",
                    0
                )
            ),

            "weakness_count": (
                weakness_analysis.get(
                    "total_weaknesses",
                    0
                )
            ),
        }

    # ==================================================
    # MAIN ANALYSIS
    # ==================================================

    def analyze(
        self,
        keyword,
    ):

        """
        Run full competitor intelligence analysis.
        """

        start_time = time.time()

        # ==========================================
        # NORMALIZE KEYWORD
        # ==========================================

        keyword = (
            str(keyword)
            .strip()
            .lower()
        )

        competitor_logger.info(

            f"[COMPETITOR ANALYSIS START] "
            f"KEYWORD={keyword}"
        )

        try:

            # ==========================================
            # SERP EXTRACTION
            # ==========================================

            serp_results = (
                self.serp_extractor.extract(
                    keyword
                )
            )

            # ==========================================
            # CONTENT ANALYSIS
            # ==========================================

            content_analysis = (
                self.content_analyzer.analyze(
                    serp_results
                )
            )

            # ==========================================
            # STRUCTURE ANALYSIS
            # ==========================================

            structure_analysis = (
                self.structure_analyzer.analyze(
                    serp_results
                )
            )

            # ==========================================
            # GAP ANALYSIS
            # ==========================================

            gap_analysis = (
                self.gap_finder.find_gaps(

                    content_analysis,

                    structure_analysis,
                )
            )

            # ==========================================
            # WEAKNESS ANALYSIS
            # ==========================================

            weakness_analysis = (
                self.weakness_detector.detect(

                    content_analysis,

                    structure_analysis,
                )
            )

            # ==========================================
            # COMPETITION SCORE
            # ==========================================

            competition_analysis = (
                self.competitor_score.calculate(

                    content_analysis,

                    structure_analysis,

                    gap_analysis,

                    weakness_analysis,
                )
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
            # SCORE
            # ==========================================

            competition_score = (
                competition_analysis.get(

                    "competition_score",

                    0,
                )
            )

            # ==========================================
            # SAVE EXECUTION
            # ==========================================

            self.save_engine_execution(

                keyword=keyword,

                execution_time=(
                    execution_time
                ),

                status="success",

                score=competition_score,
            )

            # ==========================================
            # SUMMARY
            # ==========================================

            analysis_summary = (
                self.build_analysis_summary(

                    competition_analysis,

                    gap_analysis,

                    weakness_analysis,
                )
            )

            competitor_logger.info(

                f"[COMPETITOR ANALYSIS COMPLETE] "
                f"KEYWORD={keyword} | "
                f"TIME={execution_time}s | "
                f"SCORE={competition_score}"
            )

            # ==========================================
            # RETURN RESULT
            # ==========================================

            return {

                "keyword": keyword,

                "serp_results": (
                    serp_results
                ),

                "content_analysis": (
                    content_analysis
                ),

                "structure_analysis": (
                    structure_analysis
                ),

                "gap_analysis": (
                    gap_analysis
                ),

                "weakness_analysis": (
                    weakness_analysis
                ),

                "competition_analysis": (
                    competition_analysis
                ),

                "analysis_summary": (
                    analysis_summary
                ),

                "engine_metadata": {

                    "engine": (
                        "competitor_intelligence"
                    ),

                    "version": (
                        "2.2.0"
                    ),

                    "execution_time": (
                        execution_time
                    ),

                    "analysis_timestamp": (
                        Helpers.current_timestamp()
                    ),

                    "status": "success",
                },
            }

        except Exception as error:

            competitor_logger.exception(

                f"[COMPETITOR ANALYSIS FAILED] "
                f"KEYWORD={keyword} | "
                f"ERROR={str(error)}"
            )

            execution_time = (
                Helpers.execution_timer(
                    start_time
                )
            )

            # ==========================================
            # SAVE FAILED EXECUTION
            # ==========================================

            self.save_engine_execution(

                keyword=keyword,

                execution_time=(
                    execution_time
                ),

                status="failed",

                score=0,
            )

            raise CompetitorException(

                f"Competitor analysis failed: "
                f"{str(error)}"
            )