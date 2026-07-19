"""
Discovery service for keyword opportunity engine.
"""

import time

from apps.discovery.collectors.keyword_collector import (
    KeywordCollector,
)

from apps.discovery.collectors.trend_collector import (
    TrendCollector,
)

from apps.discovery.processors.keyword_cleaner import (
    KeywordCleaner,
)

from apps.discovery.processors.intent_detector import (
    IntentDetector,
)

from apps.discovery.processors.keyword_cluster import (
    KeywordCluster,
)

from apps.discovery.scoring.opportunity_scorer import (
    OpportunityScorer,
)

from utils.keyword_normalizer import (
    KeywordNormalizer,
)

from utils.helpers import (
    Helpers,
)

from utils.logger import (
    logger,
)

from utils.exceptions import (
    DiscoveryException,
    KeywordValidationException,
)


class DiscoveryService:

    def __init__(self):

        # =========================
        # COLLECTORS
        # =========================

        self.keyword_collector = (
            KeywordCollector()
        )

        self.trend_collector = (
            TrendCollector()
        )

        # =========================
        # PROCESSORS
        # =========================

        self.keyword_cleaner = (
            KeywordCleaner()
        )

        self.intent_detector = (
            IntentDetector()
        )

        self.keyword_cluster = (
            KeywordCluster()
        )

        # =========================
        # SCORING
        # =========================

        self.opportunity_scorer = (
            OpportunityScorer()
        )

    def _build_trend_map(
        self,
        trends
    ):

        trend_map = {}

        for trend in trends:

            keyword = (
                trend.get(
                    "keyword",
                    ""
                )
                .strip()
                .lower()
            )

            trend_map[keyword] = (
                trend.get(
                    "trend_score",
                    50
                )
            )

        return trend_map

    def _find_trend_score(
        self,
        keyword,
        trend_map
    ):

        keyword = (
            keyword.strip()
            .lower()
        )

        # =========================
        # EXACT MATCH
        # =========================

        if keyword in trend_map:

            return trend_map[keyword]

        # =========================
        # PARTIAL MATCH
        # =========================

        for trend_keyword, score in (
            trend_map.items()
        ):

            if keyword in trend_keyword:

                return score

        return 50

    def discover(
        self,
        seed_keyword
    ):

        start_time = time.time()

        logger.info(

            f"Starting discovery engine "
            f"for keyword: {seed_keyword}"
        )

        try:

            # =========================
            # VALIDATE KEYWORD
            # =========================

            if not seed_keyword:

                raise (
                    KeywordValidationException(
                        "Seed keyword is required."
                    )
                )

            seed_keyword = (
                KeywordNormalizer.normalize(
                    seed_keyword
                )
            )

            if len(seed_keyword) < 2:

                raise (
                    KeywordValidationException(
                        "Keyword is too short."
                    )
                )

            # =========================
            # COLLECT KEYWORDS
            # =========================

            keyword_result = (
                self.keyword_collector.collect(
                    seed_keyword
                )
            )

            raw_keywords = (
                keyword_result.get(
                    "keywords",
                    []
                )
            )

            logger.info(

                f"Collected "
                f"{len(raw_keywords)} "
                f"raw keywords"
            )

            # =========================
            # CLEAN KEYWORDS
            # =========================

            cleaned_result = (
                self.keyword_cleaner.clean(
                    raw_keywords
                )
            )

            cleaned_keywords = (
                cleaned_result.get(
                    "keywords",
                    []
                )
            )

            cleaned_keywords = (
                Helpers.unique_list(
                    cleaned_keywords
                )
            )

            logger.info(

                f"Cleaned keyword count: "
                f"{len(cleaned_keywords)}"
            )

            # =========================
            # COLLECT TRENDS
            # =========================

            try:

                trend_result = (
                    self.trend_collector.collect(
                        seed_keyword
                    )
                )

                trends = (
                    trend_result.get(
                        "trends",
                        []
                    )
                )

            except Exception as error:

                logger.warning(

                    f"Trend collection failed: "
                    f"{str(error)}"
                )

                trends = []

            # =========================
            # TREND MAP
            # =========================

            trend_map = (
                self._build_trend_map(
                    trends
                )
            )

            # =========================
            # BUILD OPPORTUNITIES
            # =========================

            opportunities = []

            for keyword in (
                cleaned_keywords
            ):

                try:

                    # =====================
                    # INTENT DETECTION
                    # =====================

                    intent_result = (
                        self.intent_detector.detect(
                            keyword
                        )
                    )

                    intent = (
                        intent_result.get(
                            "intent",
                            "general"
                        )
                    )

                    # =====================
                    # TREND SCORE
                    # =====================

                    trend_score = (
                        self._find_trend_score(
                            keyword,
                            trend_map
                        )
                    )

                    # =====================
                    # SCORE
                    # =====================

                    score_result = (
                        self.opportunity_scorer.score(

                            keyword=keyword,

                            intent=intent,

                            trend_score=trend_score
                        )
                    )

                    opportunities.append(
                        score_result
                    )

                except Exception as error:

                    logger.warning(

                        f"Failed processing keyword: "
                        f"{keyword} | "
                        f"{str(error)}"
                    )

                    continue

            # =========================
            # SORT OPPORTUNITIES
            # =========================

            opportunities.sort(

                key=lambda item: item[
                    "opportunity_score"
                ],

                reverse=True
            )

            # =========================
            # CLUSTER KEYWORDS
            # =========================

            try:

                cluster_result = (
                    self.keyword_cluster.cluster(
                        cleaned_keywords
                    )
                )

            except Exception as error:

                logger.warning(

                    f"Clustering failed: "
                    f"{str(error)}"
                )

                cluster_result = {

                    "total_clusters": 0,

                    "clusters": [],
                }

            # =========================
            # EXECUTION TIME
            # =========================

            execution_time = (
                Helpers.execution_timer(
                    start_time
                )
            )

            logger.info(

                f"Discovery engine completed "
                f"in {execution_time}s"
            )

            # =========================
            # RETURN RESULT
            # =========================

            return {

                "success": True,

                "seed_keyword": (
                    seed_keyword
                ),

                "execution_time": (
                    execution_time
                ),

                "total_keywords": len(
                    cleaned_keywords
                ),

                "top_opportunities": (
                    opportunities[:10]
                ),

                "clusters": (
                    cluster_result
                ),

                "trends": (
                    trends[:10]
                ),
            }

        except KeywordValidationException:

            raise

        except Exception as error:

            logger.error(

                f"Discovery engine failed: "
                f"{str(error)}"
            )

            raise DiscoveryException(

                f"Discovery engine failed: "
                f"{str(error)}"
            )