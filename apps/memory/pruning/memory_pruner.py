"""
Memory pruning engine.
"""

from datetime import datetime

from apps.memory.storage.memory_repository import (
    MemoryRepository
)


class MemoryPruner:

    def __init__(self):

        self.repository = (
            MemoryRepository()
        )

    def should_prune(
        self,
        item,
    ):

        """
        Decide whether memory
        should be removed.
        """

        metadata = item.get(
            "metadata",
            {}
        )

        importance = metadata.get(
            "importance",
            0.5,
        )

        usage_count = metadata.get(
            "usage_count",
            0,
        )

        created_at = item.get(
            "created_at"
        )

        if not created_at:

            return False

        created_time = (
            datetime.fromisoformat(
                created_at
            )
        )

        age_days = (

            datetime.utcnow()
            - created_time

        ).days

        if (
            importance < 0.15
            and usage_count < 2
            and age_days > 7
        ):

            return True

        return False

    def prune(self):

        """
        Remove weak memories.
        """

        memories = (
            self.repository.all()
        )

        retained = []

        removed = []

        for item in memories:

            if self.should_prune(
                item
            ):

                removed.append(
                    item
                )

            else:

                retained.append(
                    item
                )

        self.repository.store.save(
            retained
        )

        return {

            "removed_count": len(
                removed
            ),

            "retained_count": len(
                retained
            ),

            "removed_memories": removed,
        }

    def stats(self):

        """
        Memory pruning statistics.
        """

        memories = (
            self.repository.all()
        )

        total = len(
            memories
        )

        low_importance = 0

        for item in memories:

            metadata = item.get(
                "metadata",
                {}
            )

            importance = metadata.get(
                "importance",
                0.5,
            )

            if importance < 0.2:

                low_importance += 1

        return {

            "total_memories": total,

            "low_importance_memories": (
                low_importance
            ),
        }