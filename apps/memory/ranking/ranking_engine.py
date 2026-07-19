"""
Semantic memory ranking engine.
"""

import logging

from datetime import datetime
from math import exp


logger = logging.getLogger(
    __name__
)


class RankingEngine:

    MIN_SCORE = 0.0

    MAX_SCORE = 1.0

    DUPLICATE_PENALTY = 0.05

    def __init__(self):

        # ==========================================
        # WEIGHTS
        # ==========================================

        self.semantic_weight = 0.55

        self.recency_weight = 0.15

        self.importance_weight = 0.15

        self.usage_weight = 0.15

    # ==================================================
    # SAFE FLOAT
    # ==================================================

    def safe_float(
        self,
        value,
        default=0.0,
    ):

        """
        Safe float conversion.
        """

        try:

            return float(value)

        except Exception:

            return default

    # ==================================================
    # CLAMP SCORE
    # ==================================================

    def clamp_score(
        self,
        score,
    ):

        """
        Clamp score between 0 and 1.
        """

        score = self.safe_float(
            score
        )

        return max(

            self.MIN_SCORE,

            min(
                score,
                self.MAX_SCORE,
            ),
        )

    # ==================================================
    # RECENCY SCORE
    # ==================================================

    def calculate_recency_score(
        self,
        created_at,
    ):

        """
        Calculate freshness score.
        """

        if not created_at:

            return 0.0

        try:

            created_time = (
                datetime.fromisoformat(
                    created_at
                )
            )

            now = datetime.utcnow()

            age_seconds = (
                now - created_time
            ).total_seconds()

            if age_seconds < 0:

                return 0.0

            decay_days = (
                age_seconds / 86400
            )

            score = exp(
                -decay_days / 30
            )

            return round(

                self.clamp_score(
                    score
                ),

                4,
            )

        except Exception:

            return 0.0

    # ==================================================
    # IMPORTANCE SCORE
    # ==================================================

    def calculate_importance_score(
        self,
        metadata,
    ):

        """
        Calculate importance score.
        """

        if not metadata:

            return 0.0

        importance = metadata.get(
            "importance",
            0.5,
        )

        return round(

            self.clamp_score(
                importance
            ),

            4,
        )

    # ==================================================
    # USAGE SCORE
    # ==================================================

    def calculate_usage_score(
        self,
        metadata,
    ):

        """
        Calculate usage frequency score.
        """

        if not metadata:

            return 0.0

        usage_count = (
            metadata.get(
                "usage_count",
                0,
            )
        )

        usage_count = max(
            usage_count,
            0,
        )

        score = min(
            usage_count / 10,
            1.0,
        )

        return round(

            self.clamp_score(
                score
            ),

            4,
        )

    # ==================================================
    # DECAY PENALTY
    # ==================================================

    def calculate_decay_penalty(
        self,
        recency_score,
    ):

        """
        Additional decay penalty
        for very old memories.
        """

        if recency_score < 0.10:

            return 0.15

        if recency_score < 0.20:

            return 0.10

        return 0.0

    # ==================================================
    # DUPLICATE PENALTY
    # ==================================================

    def duplicate_penalty(
        self,
        item,
        seen_queries,
    ):

        """
        Penalize duplicate memories.
        """

        query = (
            item.get(
                "query",
                ""
            )
            .strip()
            .lower()
        )

        if query in seen_queries:

            return self.DUPLICATE_PENALTY

        seen_queries.add(
            query
        )

        return 0.0

    # ==================================================
    # FINAL SCORE
    # ==================================================

    def calculate_final_score(
        self,
        semantic_score,
        recency_score,
        importance_score,
        usage_score,
        duplicate_penalty=0.0,
    ):

        """
        Weighted ranking score.
        """

        final_score = (

            semantic_score
            * self.semantic_weight

        ) + (

            recency_score
            * self.recency_weight

        ) + (

            importance_score
            * self.importance_weight

        ) + (

            usage_score
            * self.usage_weight
        )

        decay_penalty = (
            self.calculate_decay_penalty(
                recency_score
            )
        )

        final_score = (

            final_score

            - decay_penalty

            - duplicate_penalty
        )

        return round(

            self.clamp_score(
                final_score
            ),

            4,
        )

    # ==================================================
    # ENRICH RESULT
    # ==================================================

    def enrich_result(
        self,
        item,
        semantic_score,
        recency_score,
        importance_score,
        usage_score,
        final_score,
    ):

        """
        Add ranking metadata.
        """

        enriched = dict(item)

        enriched[
            "semantic_score"
        ] = semantic_score

        enriched[
            "recency_score"
        ] = recency_score

        enriched[
            "importance_score"
        ] = importance_score

        enriched[
            "usage_score"
        ] = usage_score

        enriched[
            "final_score"
        ] = final_score

        return enriched

    # ==================================================
    # MAIN RANKING
    # ==================================================

    def rank(
        self,
        results,
    ):

        """
        Rank memory search results.
        """

        if not results:

            return []

        ranked_results = []

        seen_queries = set()

        for item in results:

            semantic_score = (
                self.clamp_score(

                    item.get(
                        "score",

                        item.get(
                            "semantic_score",
                            0,
                        ),
                    )
                )
            )

            recency_score = (
                self.calculate_recency_score(

                    item.get(
                        "created_at"
                    )
                )
            )

            importance_score = (
                self.calculate_importance_score(

                    item.get(
                        "metadata",
                        {},
                    )
                )
            )

            usage_score = (
                self.calculate_usage_score(

                    item.get(
                        "metadata",
                        {},
                    )
                )
            )

            duplicate_penalty = (
                self.duplicate_penalty(

                    item,

                    seen_queries,
                )
            )

            final_score = (
                self.calculate_final_score(

                    semantic_score,

                    recency_score,

                    importance_score,

                    usage_score,

                    duplicate_penalty,
                )
            )

            enriched_item = (
                self.enrich_result(

                    item=item,

                    semantic_score=(
                        semantic_score
                    ),

                    recency_score=(
                        recency_score
                    ),

                    importance_score=(
                        importance_score
                    ),

                    usage_score=(
                        usage_score
                    ),

                    final_score=(
                        final_score
                    ),
                )
            )

            ranked_results.append(
                enriched_item
            )

        # ==========================================
        # STABLE SORT
        # ==========================================

        ranked_results = sorted(

            ranked_results,

            key=lambda x: (

                x.get(
                    "final_score",
                    0,
                ),

                x.get(
                    "semantic_score",
                    0,
                ),

                x.get(
                    "importance_score",
                    0,
                ),
            ),

            reverse=True,
        )

        logger.info(

            f"Ranking completed "
            f"with {len(ranked_results)} "
            f"results"
        )

        return ranked_results

    # ==================================================
    # RERANK
    # ==================================================

    def rerank(
        self,
        results,
    ):

        """
        Alias for rank().
        """

        return self.rank(
            results
        )