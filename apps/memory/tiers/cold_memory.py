"""
Cold memory storage layer.
"""

from datetime import datetime

from apps.memory.storage.memory_repository import (
    MemoryRepository
)


class ColdMemory:

    def __init__(self):

        self.repository = (
            MemoryRepository()
        )

    def get_cold_memories(
        self,
        max_importance=0.3,
        max_usage=2,
        older_than_days=7,
    ):

        """
        Return low-priority memories.
        """

        memories = (
            self.repository.all()
        )

        cold_memories = []

        for item in memories:

            metadata = item.get(
                "metadata",
                {}
            )

            importance = metadata.get(
                "importance",
                0,
            )

            usage_count = metadata.get(
                "usage_count",
                0,
            )

            created_at = item.get(
                "created_at"
            )

            if not created_at:

                continue

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
                importance <= max_importance
                and usage_count <= max_usage
                and age_days >= older_than_days
            ):

                cold_memories.append(
                    item
                )

        return cold_memories

    def count(self):

        """
        Count cold memories.
        """

        return len(
            self.get_cold_memories()
        )

    def archive_candidates(
        self,
        limit=10,
    ):

        """
        Return memories suitable
        for archive layer.
        """

        cold_memories = (
            self.get_cold_memories()
        )

        sorted_memories = sorted(

            cold_memories,

            key=lambda item: (

                item.get(
                    "metadata",
                    {}
                ).get(
                    "importance",
                    0,
                )
            ),
        )

        return sorted_memories[:limit]