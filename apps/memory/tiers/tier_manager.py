"""
AI memory tier manager.
"""

from apps.memory.tiers.hot_memory import (
    HotMemory
)

from apps.memory.tiers.cold_memory import (
    ColdMemory
)

from apps.memory.pruning.memory_pruner import (
    MemoryPruner
)


class TierManager:

    def __init__(self):

        self.hot_memory = (
            HotMemory()
        )

        self.cold_memory = (
            ColdMemory()
        )

        self.pruner = (
            MemoryPruner()
        )

    def system_status(self):

        """
        Return memory tier stats.
        """

        hot_count = (
            self.hot_memory.count()
        )

        cold_count = (
            self.cold_memory.count()
        )

        pruning_stats = (
            self.pruner.stats()
        )

        return {

            "hot_memories": (
                hot_count
            ),

            "cold_memories": (
                cold_count
            ),

            "total_memories": (

                pruning_stats[
                    "total_memories"
                ]
            ),

            "low_importance_memories": (

                pruning_stats[
                    "low_importance_memories"
                ]
            ),
        }

    def optimize(self):

        """
        Optimize memory system.
        """

        pruning_result = (
            self.pruner.prune()
        )

        return {

            "optimization": "completed",

            "pruning": pruning_result,

            "hot_memories": (

                self.hot_memory.count()
            ),

            "cold_memories": (

                self.cold_memory.count()
            ),
        }

    def hot_memories(self):

        """
        Return active memory layer.
        """

        return (
            self.hot_memory.get_hot_memories()
        )

    def cold_memories(self):

        """
        Return archive memory layer.
        """

        return (
            self.cold_memory.get_cold_memories()
        )