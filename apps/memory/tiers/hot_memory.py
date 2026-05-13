"""
Enterprise hot memory storage layer.
"""

import logging
import threading

from datetime import datetime

from apps.memory.storage.memory_repository import (
    MemoryRepository
)


logger = logging.getLogger(
    __name__
)


class HotMemory:

    MAX_HOT_MEMORIES = 100

    MIN_IMPORTANCE = 0.70

    MIN_USAGE = 3

    RECENT_DAYS_BOOST = 7

    def __init__(
        self
    ):

        self.repository = (
            MemoryRepository()
        )

        self._lock = (
            threading.Lock()
        )

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
    # SAFE INT
    # ==================================================

    def safe_int(
        self,
        value,
        default=0,
    ):

        """
        Safe integer conversion.
        """

        try:

            return int(value)

        except Exception:

            return default

    # ==================================================
    # RECENCY SCORE
    # ==================================================

    def recency_score(
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

            age_days = (

                now - created_time
            ).days

            if age_days <= 1:

                return 1.0

            if age_days <= (
                self.RECENT_DAYS_BOOST
            ):

                return 0.8

            if age_days <= 30:

                return 0.5

            return 0.2

        except Exception:

            return 0.0

    # ==================================================
    # HOT SCORE
    # ==================================================

    def hot_score(
        self,
        item,
    ):

        """
        Calculate hot memory score.
        """

        metadata = item.get(
            "metadata",
            {}
        )

        importance = self.safe_float(

            metadata.get(
                "importance",
                0.0,
            )
        )

        usage_count = self.safe_int(

            metadata.get(
                "usage_count",
                0,
            )
        )

        usage_score = min(
            usage_count / 10,
            1.0,
        )

        freshness = (
            self.recency_score(

                item.get(
                    "created_at"
                )
            )
        )

        score = (

            importance * 0.5

            +

            usage_score * 0.3

            +

            freshness * 0.2
        )

        return round(
            score,
            4,
        )

    # ==================================================
    # VALID HOT MEMORY
    # ==================================================

    def valid_hot_memory(
        self,
        item,
    ):

        """
        Validate hot memory eligibility.
        """

        metadata = item.get(
            "metadata",
            {}
        )

        importance = self.safe_float(

            metadata.get(
                "importance",
                0,
            )
        )

        usage_count = self.safe_int(

            metadata.get(
                "usage_count",
                0,
            )
        )

        return (

            importance >= (
                self.MIN_IMPORTANCE
            )

            or

            usage_count >= (
                self.MIN_USAGE
            )
        )

    # ==================================================
    # REMOVE DUPLICATES
    # ==================================================

    def unique_memories(
        self,
        memories,
    ):

        """
        Remove duplicate memories.
        """

        unique = []

        seen = set()

        for item in memories:

            query = (
                item.get(
                    "query",
                    ""
                )
                .strip()
                .lower()
            )

            if not query:

                continue

            if query in seen:

                continue

            seen.add(
                query
            )

            unique.append(
                item
            )

        return unique

    # ==================================================
    # GET HOT MEMORIES
    # ==================================================

    def get_hot_memories(
        self,
        min_importance=None,
        min_usage=None,
    ):

        """
        Return prioritized hot memories.
        """

        with self._lock:

            min_importance = (
                min_importance
                or self.MIN_IMPORTANCE
            )

            min_usage = (
                min_usage
                or self.MIN_USAGE
            )

            memories = (
                self.repository.all()
            )

            hot_memories = []

            for item in memories:

                metadata = item.get(
                    "metadata",
                    {}
                )

                importance = (
                    self.safe_float(

                        metadata.get(
                            "importance",
                            0,
                        )
                    )
                )

                usage_count = (
                    self.safe_int(

                        metadata.get(
                            "usage_count",
                            0,
                        )
                    )
                )

                if (

                    importance >= (
                        min_importance
                    )

                    or

                    usage_count >= (
                        min_usage
                    )
                ):

                    enriched = dict(item)

                    enriched[
                        "hot_score"
                    ] = self.hot_score(
                        item
                    )

                    hot_memories.append(
                        enriched
                    )

            hot_memories = (
                self.unique_memories(
                    hot_memories
                )
            )

            hot_memories = sorted(

                hot_memories,

                key=lambda item: (

                    item.get(
                        "hot_score",
                        0,
                    )
                ),

                reverse=True,
            )

            return hot_memories[
                :self.MAX_HOT_MEMORIES
            ]

    # ==================================================
    # COUNT
    # ==================================================

    def count(
        self
    ):

        """
        Count hot memories.
        """

        return len(
            self.get_hot_memories()
        )

    # ==================================================
    # TOP MEMORIES
    # ==================================================

    def top_memories(
        self,
        limit=5,
    ):

        """
        Return top hot memories.
        """

        hot_memories = (
            self.get_hot_memories()
        )

        return hot_memories[
            :limit
        ]

    # ==================================================
    # HOT MEMORY EXISTS
    # ==================================================

    def exists(
        self,
        query,
    ):

        """
        Check if memory is hot.
        """

        query = (
            str(query)
            .strip()
            .lower()
        )

        memories = (
            self.get_hot_memories()
        )

        for item in memories:

            item_query = (

                item.get(
                    "query",
                    ""
                )
                .strip()
                .lower()
            )

            if item_query == query:

                return True

        return False

    # ==================================================
    # HOT MEMORY STATS
    # ==================================================

    def stats(
        self
    ):

        """
        Hot memory statistics.
        """

        hot_memories = (
            self.get_hot_memories()
        )

        return {

            "total_hot_memories": (
                len(hot_memories)
            ),

            "max_hot_memories": (
                self.MAX_HOT_MEMORIES
            ),

            "min_importance": (
                self.MIN_IMPORTANCE
            ),

            "min_usage": (
                self.MIN_USAGE
            ),
        }