"""
Trend collector for discovery engine.
"""

import random


class TrendCollector:

    def collect(
        self,
        seed_keyword
    ):

        # =========================
        # NORMALIZE INPUT
        # =========================

        seed_keyword = (
            seed_keyword
            .strip()
            .lower()
        )

        # =========================
        # TREND PATTERNS
        # =========================

        trend_keywords = [

            f"{seed_keyword} trends 2026",

            f"latest {seed_keyword}",

            f"best {seed_keyword} tools",

            f"{seed_keyword} ai tools",

            f"{seed_keyword} automation",

            f"{seed_keyword} strategy",

            f"{seed_keyword} tutorial",

            f"{seed_keyword} guide",

            f"future of {seed_keyword}",

            f"{seed_keyword} tips",

            f"{seed_keyword} workflow",

            f"{seed_keyword} ideas",

            f"{seed_keyword} hacks",

            f"{seed_keyword} for beginners",

            f"{seed_keyword} advanced guide",
        ]

        # =========================
        # BUILD TREND DATA
        # =========================

        trends = []

        for keyword in trend_keywords:

            trends.append({

                "keyword": keyword,

                "trend_score": random.randint(
                    50,
                    100
                ),

                "growth": random.randint(
                    1,
                    100
                ),

                "search_volume": random.randint(
                    100,
                    10000
                ),
            })

        # =========================
        # SORT BY TREND SCORE
        # =========================

        trends.sort(

            key=lambda item: item[
                "trend_score"
            ],

            reverse=True
        )

        # =========================
        # RETURN RESULT
        # =========================

        return {

            "seed_keyword": seed_keyword,

            "total_trends": len(
                trends
            ),

            "trends": trends,
        }