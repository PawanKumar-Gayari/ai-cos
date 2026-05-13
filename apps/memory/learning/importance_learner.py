"""
Enterprise adaptive memory importance learner.
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


class ImportanceLearner:

    MIN_IMPORTANCE = 0.0

    MAX_IMPORTANCE = 1.0

    DEFAULT_IMPORTANCE = 0.5

    MAX_BOOST = 0.25

    MAX_REDUCTION = 0.15

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
    # NORMALIZE QUERY
    # ==================================================

    def normalize_query(
        self,
        query,
    ):

        """
        Normalize memory query.
        """

        if not query:

            return ""

        return (
            str(query)
            .strip()
            .lower()
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
    # CLAMP IMPORTANCE
    # ==================================================

    def clamp_importance(
        self,
        value,
    ):

        """
        Clamp importance score.
        """

        value = self.safe_float(
            value,
            self.DEFAULT_IMPORTANCE,
        )

        return max(

            self.MIN_IMPORTANCE,

            min(
                value,
                self.MAX_IMPORTANCE,
            ),
        )

    # ==================================================
    # TIMESTAMP
    # ==================================================

    def timestamp(
        self
    ):

        """
        UTC timestamp.
        """

        return (
            datetime.utcnow()
            .isoformat()
        )

    # ==================================================
    # SAFE METADATA
    # ==================================================

    def safe_metadata(
        self,
        metadata,
    ):

        """
        Normalize metadata.
        """

        if not metadata:

            return {}

        return dict(metadata)

    # ==================================================
    # UPDATE IMPORTANCE
    # ==================================================

    def update_importance(
        self,
        query,
        delta,
        reason="adaptive_learning",
    ):

        """
        Generic importance updater.
        """

        normalized_query = (
            self.normalize_query(
                query
            )
        )

        if not normalized_query:

            return False

        with self._lock:

            memories = (
                self.repository.all()
            )

            updated = False

            for item in memories:

                item_query = (
                    self.normalize_query(

                        item.get(
                            "query",
                            ""
                        )
                    )
                )

                if item_query != (
                    normalized_query
                ):

                    continue

                metadata = (
                    self.safe_metadata(

                        item.get(
                            "metadata",
                            {}
                        )
                    )
                )

                current_importance = (
                    self.clamp_importance(

                        metadata.get(
                            "importance",
                            self.DEFAULT_IMPORTANCE,
                        )
                    )
                )

                new_importance = (
                    self.clamp_importance(

                        current_importance
                        + delta
                    )
                )

                metadata[
                    "importance"
                ] = round(
                    new_importance,
                    4,
                )

                metadata[
                    "importance_updated_at"
                ] = self.timestamp()

                metadata[
                    "importance_reason"
                ] = reason

                metadata[
                    "adaptive_learning"
                ] = True

                item[
                    "metadata"
                ] = metadata

                updated = True

                logger.info(

                    f"Importance updated "
                    f"for memory: "
                    f"{normalized_query}"
                )

                break

            if updated:

                return (
                    self.repository.safe_save(
                        memories
                    )
                )

            return False

    # ==================================================
    # BOOST IMPORTANCE
    # ==================================================

    def boost_importance(
        self,
        query,
        amount=0.05,
        reason="high_relevance",
    ):

        """
        Increase memory importance.
        """

        amount = min(
            amount,
            self.MAX_BOOST,
        )

        return self.update_importance(

            query=query,

            delta=amount,

            reason=reason,
        )

    # ==================================================
    # REDUCE IMPORTANCE
    # ==================================================

    def reduce_importance(
        self,
        query,
        amount=0.02,
        reason="low_relevance",
    ):

        """
        Reduce memory importance.
        """

        amount = min(
            amount,
            self.MAX_REDUCTION,
        )

        return self.update_importance(

            query=query,

            delta=-amount,

            reason=reason,
        )

    # ==================================================
    # GET IMPORTANCE
    # ==================================================

    def get_importance(
        self,
        query,
    ):

        """
        Return importance score.
        """

        normalized_query = (
            self.normalize_query(
                query
            )
        )

        memories = (
            self.repository.all()
        )

        for item in memories:

            item_query = (
                self.normalize_query(

                    item.get(
                        "query",
                        ""
                    )
                )
            )

            if item_query == (
                normalized_query
            ):

                metadata = item.get(
                    "metadata",
                    {}
                )

                return self.clamp_importance(

                    metadata.get(
                        "importance",
                        self.DEFAULT_IMPORTANCE,
                    )
                )

        return (
            self.DEFAULT_IMPORTANCE
        )

    # ==================================================
    # TOP IMPORTANT
    # ==================================================

    def top_important(
        self,
        limit=10,
    ):

        """
        Return highest-importance memories.
        """

        memories = (
            self.repository.all()
        )

        sorted_memories = sorted(

            memories,

            key=lambda item: (

                item.get(
                    "metadata",
                    {}
                ).get(
                    "importance",
                    self.DEFAULT_IMPORTANCE,
                )
            ),

            reverse=True,
        )

        return sorted_memories[
            :limit
        ]

    # ==================================================
    # DECAY LOW USAGE MEMORIES
    # ==================================================

    def decay_low_usage(
        self,
        threshold=0,
        decay_amount=0.01,
    ):

        """
        Reduce stale memory importance.
        """

        memories = (
            self.repository.all()
        )

        updated = False

        for item in memories:

            metadata = item.get(
                "metadata",
                {}
            )

            usage_count = int(

                metadata.get(
                    "usage_count",
                    0,
                )
            )

            if usage_count > threshold:

                continue

            current_importance = (
                self.clamp_importance(

                    metadata.get(
                        "importance",
                        self.DEFAULT_IMPORTANCE,
                    )
                )
            )

            new_importance = (
                self.clamp_importance(

                    current_importance
                    - decay_amount
                )
            )

            metadata[
                "importance"
            ] = round(
                new_importance,
                4,
            )

            metadata[
                "importance_decay"
            ] = True

            metadata[
                "importance_updated_at"
            ] = self.timestamp()

            item[
                "metadata"
            ] = metadata

            updated = True

        if updated:

            logger.info(
                "Importance decay applied."
            )

            return (
                self.repository.safe_save(
                    memories
                )
            )

        return False

    # ==================================================
    # SYSTEM STATS
    # ==================================================

    def stats(
        self
    ):

        """
        Importance learner statistics.
        """

        memories = (
            self.repository.all()
        )

        importance_values = []

        for item in memories:

            metadata = item.get(
                "metadata",
                {}
            )

            importance = (
                self.clamp_importance(

                    metadata.get(
                        "importance",
                        self.DEFAULT_IMPORTANCE,
                    )
                )
            )

            importance_values.append(
                importance
            )

        average_importance = 0.0

        if importance_values:

            average_importance = round(

                sum(
                    importance_values
                )

                / len(
                    importance_values
                ),

                4,
            )

        return {

            "tracked_memories": (
                len(importance_values)
            ),

            "average_importance": (
                average_importance
            ),

            "max_importance": (
                self.MAX_IMPORTANCE
            ),

            "min_importance": (
                self.MIN_IMPORTANCE
            ),
        }