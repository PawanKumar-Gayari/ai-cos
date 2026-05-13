"""
Enterprise memory usage tracking engine.
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


class UsageTracker:

    MAX_USAGE_COUNT = 1_000_000

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
    # CURRENT TIMESTAMP
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
        Ensure metadata exists.
        """

        if not metadata:

            return {}

        return dict(metadata)

    # ==================================================
    # INCREMENT USAGE
    # ==================================================

    def increment_usage(
        self,
        query,
        amount=1,
    ):

        """
        Increment memory usage count.
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

                current_usage = int(

                    metadata.get(
                        "usage_count",
                        0,
                    )
                )

                new_usage = min(

                    current_usage + amount,

                    self.MAX_USAGE_COUNT,
                )

                metadata[
                    "usage_count"
                ] = new_usage

                metadata[
                    "last_used_at"
                ] = self.timestamp()

                metadata[
                    "usage_updated"
                ] = True

                item[
                    "metadata"
                ] = metadata

                updated = True

                logger.info(

                    f"Usage updated for "
                    f"memory: {normalized_query}"
                )

                break

            if updated:

                save_result = (
                    self.repository.safe_save(
                        memories
                    )
                )

                return save_result

            return False

    # ==================================================
    # GET USAGE COUNT
    # ==================================================

    def get_usage_count(
        self,
        query,
    ):

        """
        Get usage count for memory.
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

                return int(

                    metadata.get(
                        "usage_count",
                        0,
                    )
                )

        return 0

    # ==================================================
    # LAST USED
    # ==================================================

    def last_used_at(
        self,
        query,
    ):

        """
        Return last usage timestamp.
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

                return metadata.get(
                    "last_used_at"
                )

        return None

    # ==================================================
    # MOST USED MEMORIES
    # ==================================================

    def most_used(
        self,
        limit=5,
    ):

        """
        Return most used memories.
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
                    "usage_count",
                    0,
                )
            ),

            reverse=True,
        )

        return sorted_memories[
            :limit
        ]

    # ==================================================
    # RESET USAGE
    # ==================================================

    def reset_usage(
        self,
        query,
    ):

        """
        Reset memory usage count.
        """

        normalized_query = (
            self.normalize_query(
                query
            )
        )

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

            metadata[
                "usage_count"
            ] = 0

            metadata[
                "last_used_at"
            ] = None

            item[
                "metadata"
            ] = metadata

            updated = True

            break

        if updated:

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
        Usage tracker statistics.
        """

        memories = (
            self.repository.all()
        )

        total_usage = 0

        tracked_memories = 0

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

            total_usage += usage_count

            if usage_count > 0:

                tracked_memories += 1

        return {

            "tracked_memories": (
                tracked_memories
            ),

            "total_usage": (
                total_usage
            ),

            "max_usage_count": (
                self.MAX_USAGE_COUNT
            ),
        }