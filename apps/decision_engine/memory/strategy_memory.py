"""
Strategy Memory

Purpose:
Store strategic editorial intelligence.

Tracks:
- which strategies succeed
- which structures rank
- which optimizations fail
- niche-specific winning patterns
- SERP adaptation history

Goal:
Create a self-evolving strategy system.

This becomes the strategic intelligence memory
of AI_COS.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Any, List


# =============================================================
# STRATEGY ENTRY
# =============================================================

@dataclass
class StrategyMemoryEntry:

    # =========================================================
    # STRATEGY
    # =========================================================

    strategy_id: str

    strategy_name: str

    niche: str

    keyword_type: str = "general"

    intent_type: str = "informational"

    # =========================================================
    # STRUCTURE
    # =========================================================

    faq_enabled: bool = False

    tables_enabled: bool = False

    comparison_enabled: bool = False

    snippet_optimized: bool = False

    semantic_optimization_enabled: bool = False

    freshness_optimization_enabled: bool = False

    # =========================================================
    # CONTENT STYLE
    # =========================================================

    expert_tone_used: bool = False

    authority_focused: bool = False

    conversational_tone: bool = False

    data_driven_content: bool = False

    # =========================================================
    # SEO STRATEGY
    # =========================================================

    long_tail_strategy: bool = False

    semantic_clustering_enabled: bool = False

    topical_authority_strategy: bool = False

    internal_linking_strategy: bool = False

    # =========================================================
    # VERIFICATION
    # =========================================================

    official_sources_used: bool = False

    citations_added: bool = False

    expert_review_enabled: bool = False

    freshness_verified: bool = False

    # =========================================================
    # PERFORMANCE
    # =========================================================

    ranking_success: bool = False

    featured_snippet_won: bool = False

    high_ctr_detected: bool = False

    high_traffic_detected: bool = False

    stable_rankings_detected: bool = False

    # =========================================================
    # SCORES
    # =========================================================

    average_position: float = 100.0

    average_ctr: float = 0.0

    average_traffic: float = 0.0

    engagement_score: float = 0.0

    strategy_score: float = 0.0

    # =========================================================
    # LEARNING
    # =========================================================

    successful_patterns: List[str] = field(
        default_factory=list
    )

    failed_patterns: List[str] = field(
        default_factory=list
    )

    optimization_notes: List[str] = field(
        default_factory=list
    )

    # =========================================================
    # USAGE
    # =========================================================

    times_used: int = 0

    success_count: int = 0

    failure_count: int = 0

    adaptation_count: int = 0

    # =========================================================
    # TIMESTAMPS
    # =========================================================

    created_at: datetime = field(
        default_factory=datetime.utcnow
    )

    updated_at: datetime = field(
        default_factory=datetime.utcnow
    )

    # =========================================================
    # META
    # =========================================================

    metadata: Dict[str, Any] = field(
        default_factory=dict
    )


# =============================================================
# STRATEGY MEMORY
# =============================================================

class StrategyMemory:

    """
    Strategic editorial intelligence memory.
    """

    def __init__(
        self,
    ) -> None:

        self.strategy_store: List[
            StrategyMemoryEntry
        ] = []

    # =========================================================
    # STORE
    # =========================================================

    def store(
        self,
        entry: StrategyMemoryEntry,
    ) -> None:

        self.strategy_store.append(
            entry
        )

    # =========================================================
    # FIND BY NICHE
    # =========================================================

    def find_by_niche(
        self,
        niche: str,
    ) -> List[StrategyMemoryEntry]:

        return [

            entry

            for entry in self.strategy_store

            if entry.niche == niche
        ]

    # =========================================================
    # TOP STRATEGIES
    # =========================================================

    def top_strategies(
        self,
        limit: int = 10,
    ) -> List[StrategyMemoryEntry]:

        return sorted(

            self.strategy_store,

            key=lambda entry: (
                entry.strategy_score
            ),

            reverse=True,
        )[:limit]

    # =========================================================
    # SUCCESS RATE
    # =========================================================

    def strategy_success_rate(
        self,
        strategy_name: str,
    ) -> float:

        entries = [

            entry

            for entry in self.strategy_store

            if entry.strategy_name
            == strategy_name
        ]

        if not entries:
            return 0.0

        successful = len([

            entry

            for entry in entries

            if entry.ranking_success
        ])

        return round(

            (
                successful /
                len(entries)
            ) * 100,

            2,
        )

    # =========================================================
    # FAQ PERFORMANCE
    # =========================================================

    def faq_strategy_score(
        self,
    ) -> float:

        faq_entries = [

            entry

            for entry in self.strategy_store

            if entry.faq_enabled
        ]

        if not faq_entries:
            return 0.0

        successful = len([

            entry

            for entry in faq_entries

            if entry.ranking_success
        ])

        return round(

            (
                successful /
                len(faq_entries)
            ) * 100,

            2,
        )

    # =========================================================
    # TABLE PERFORMANCE
    # =========================================================

    def table_strategy_score(
        self,
    ) -> float:

        table_entries = [

            entry

            for entry in self.strategy_store

            if entry.tables_enabled
        ]

        if not table_entries:
            return 0.0

        successful = len([

            entry

            for entry in table_entries

            if entry.ranking_success
        ])

        return round(

            (
                successful /
                len(table_entries)
            ) * 100,

            2,
        )

    # =========================================================
    # SNIPPET PERFORMANCE
    # =========================================================

    def snippet_strategy_score(
        self,
    ) -> float:

        snippet_entries = [

            entry

            for entry in self.strategy_store

            if entry.snippet_optimized
        ]

        if not snippet_entries:
            return 0.0

        successful = len([

            entry

            for entry in snippet_entries

            if entry.featured_snippet_won
        ])

        return round(

            (
                successful /
                len(snippet_entries)
            ) * 100,

            2,
        )

    # =========================================================
    # PATTERN LEARNING
    # =========================================================

    def extract_success_patterns(
        self,
    ) -> Dict[str, int]:

        patterns: Dict[str, int] = {}

        successful_entries = [

            entry

            for entry in self.strategy_store

            if entry.ranking_success
        ]

        for entry in successful_entries:

            for pattern in entry.successful_patterns:

                patterns[pattern] = (

                    patterns.get(pattern, 0) + 1
                )

        return patterns

    # =========================================================
    # FAILURE PATTERNS
    # =========================================================

    def extract_failure_patterns(
        self,
    ) -> Dict[str, int]:

        patterns: Dict[str, int] = {}

        failed_entries = [

            entry

            for entry in self.strategy_store

            if not entry.ranking_success
        ]

        for entry in failed_entries:

            for pattern in entry.failed_patterns:

                patterns[pattern] = (

                    patterns.get(pattern, 0) + 1
                )

        return patterns

    # =========================================================
    # UPDATE STRATEGY
    # =========================================================

    def update_strategy_performance(
        self,
        strategy_id: str,
        ranking_success: bool = False,
        traffic: float = 0.0,
        ctr: float = 0.0,
        position: float = 100.0,
    ) -> bool:

        for entry in self.strategy_store:

            if entry.strategy_id == strategy_id:

                entry.times_used += 1

                if ranking_success:

                    entry.success_count += 1

                    entry.ranking_success = True

                else:

                    entry.failure_count += 1

                entry.average_traffic = traffic

                entry.average_ctr = ctr

                entry.average_position = position

                # =============================================
                # STRATEGY SCORE
                # =============================================

                self._calculate_strategy_score(
                    entry
                )

                entry.updated_at = (
                    datetime.utcnow()
                )

                return True

        return False

    # =========================================================
    # SCORE
    # =========================================================

    def _calculate_strategy_score(
        self,
        entry: StrategyMemoryEntry,
    ) -> None:

        success_rate = 0.0

        total = (
            entry.success_count +
            entry.failure_count
        )

        if total > 0:

            success_rate = (
                entry.success_count /
                total
            ) * 100

        score = (

            success_rate * 0.4 +

            entry.average_ctr * 100 * 0.2 +

            entry.engagement_score * 0.2
        )

        # =====================================================
        # BONUS
        # =====================================================

        if entry.featured_snippet_won:
            score += 10

        if entry.high_traffic_detected:
            score += 10

        entry.strategy_score = round(
            min(score, 100),
            2,
        )

    # =========================================================
    # EXPORT
    # =========================================================

    def export_memory(
        self,
    ) -> Dict[str, Any]:

        return {

            "total_strategies": (
                len(self.strategy_store)
            ),

            "faq_strategy_score": (
                self.faq_strategy_score()
            ),

            "table_strategy_score": (
                self.table_strategy_score()
            ),

            "snippet_strategy_score": (
                self.snippet_strategy_score()
            ),

            "success_patterns": (
                self.extract_success_patterns()
            ),

            "failure_patterns": (
                self.extract_failure_patterns()
            ),

            "top_strategies": [

                {
                    "strategy_id": (
                        entry.strategy_id
                    ),

                    "strategy_name": (
                        entry.strategy_name
                    ),

                    "strategy_score": (
                        entry.strategy_score
                    ),

                    "success_count": (
                        entry.success_count
                    ),

                    "failure_count": (
                        entry.failure_count
                    ),
                }

                for entry in self.top_strategies()
            ],
        }