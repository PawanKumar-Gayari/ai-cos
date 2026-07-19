"""
Trend collector for discovery engine.
"""

import random

from utils.logger import (
    logger,
)


class TrendCollector:

    # =========================
    # TREND PATTERNS
    # =========================

    TREND_PATTERNS = [

        "latest {}",

        "{} trends",

        "{} tools",

        "{} software",

        "{} automation",

        "{} strategy",

        "{} tutorial",

        "{} guide",

        "future of {}",

        "{} tips",

        "{} workflow",

        "{} ideas",

        "{} hacks",

        "{} for beginners",

        "{} advanced guide",

        "{} best practices",

        "{} use cases",

        "{} roadmap",

        "{} implementation",
    ]

    def _calculate_trend_score(
        self,
        keyword
    ):

        score = 50

        boost_patterns = {

            "ai": 15,

            "automation": 12,

            "tools": 10,

            "strategy": 8,

            "guide": 6,

            "tutorial": 6,

            "workflow": 8,

            "roadmap": 8,
        }

        keyword_lower = (
            keyword.lower()
        )

        for pattern, boost in (
            boost_patterns.items()
        ):

            if pattern in keyword_lower:

                score += boost

        score += random.randint(
            0,
            10
        )

        return min(
            score,
            100
        )

    def _calculate_growth(
        self,
        trend_score
    ):

        minimum = max(
            1,
            trend_score - 40
        )

        maximum = min(
            100,
            trend_score + 10
        )

        return random.randint(
            minimum,
            maximum
        )

    def _calculate_search_volume(
        self,
        trend_score
    ):

        base_volume = (
            trend_score * 100
        )

        variation = random.randint(
            100,
            2000
        )

        return (
            base_volume
            + variation
        )

    def collect(
        self,
        seed_keyword
    ):

        # =========================
        # VALIDATE INPUT
        # =========================

        if not seed_keyword:

            logger.warning(
                "Empty seed keyword received"
            )

            return {

                "seed_keyword": "",

                "total_trends": 0,

                "trends": [],
            }

        # =========================
        # NORMALIZE INPUT
        # =========================

        seed_keyword = (
            seed_keyword
            .strip()
            .lower()
        )

        logger.info(

            f"Collecting trends for: "
            f"{seed_keyword}"
        )

        # =========================
        # BUILD TREND KEYWORDS
        # =========================

        trend_keywords = []

        for pattern in (
            self.TREND_PATTERNS
        ):

            trend_keywords.append(
                pattern.format(
                    seed_keyword
                )
            )

        # =========================
        # BUILD TREND DATA
        # =========================

        trends = []

        for keyword in (
            trend_keywords
        ):

            trend_score = (
                self._calculate_trend_score(
                    keyword
                )
            )

            growth = (
                self._calculate_growth(
                    trend_score
                )
            )

            search_volume = (
                self._calculate_search_volume(
                    trend_score
                )
            )

            trends.append({

                "keyword": keyword,

                "trend_score": (
                    trend_score
                ),

                "growth": (
                    growth
                ),

                "search_volume": (
                    search_volume
                ),
            })

        # =========================
        # REMOVE DUPLICATES
        # =========================

        unique_trends = {}

        for trend in trends:

            unique_trends[
                trend["keyword"]
            ] = trend

        trends = list(
            unique_trends.values()
        )

        # =========================
        # SORT BY TREND SCORE
        # =========================

        trends.sort(

            key=lambda item: item[
                "trend_score"
            ],

            reverse=True
        )

        logger.info(

            f"Generated "
            f"{len(trends)} "
            f"trend keywords"
        )

        # =========================
        # RETURN RESULT
        # =========================

        return {

            "seed_keyword": (
                seed_keyword
            ),

            "total_trends": len(
                trends
            ),

            "trends": (
                trends
            ),
        }