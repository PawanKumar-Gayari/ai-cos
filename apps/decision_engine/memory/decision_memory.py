"""
Decision Memory

Purpose:
Store long-term editorial intelligence memory.

This system remembers:
- successful strategies
- failed strategies
- ranking outcomes
- verification patterns
- freshness decay behavior
- adaptive learning history

Goal:
Create persistent self-improving intelligence.

This becomes the memory layer of AI_COS.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Any, List, Optional


# =============================================================
# MEMORY ENTRY
# =============================================================

@dataclass
class DecisionMemoryEntry:

    # =========================================================
    # ARTICLE
    # =========================================================

    article_id: str

    keyword: str

    niche: str

    strategy_type: str = "general"

    # =========================================================
    # SCORES
    # =========================================================

    seo_score: float = 0.0

    quality_score: float = 0.0

    freshness_score: float = 0.0

    authority_score: float = 0.0

    verification_score: float = 0.0

    ranking_probability: float = 0.0

    # =========================================================
    # REAL OUTCOMES
    # =========================================================

    actual_position: int = 100

    actual_ctr: float = 0.0

    actual_traffic: int = 0

    ranking_success: bool = False

    # =========================================================
    # STRATEGY SIGNALS
    # =========================================================

    faq_enabled: bool = False

    tables_enabled: bool = False

    comparison_enabled: bool = False

    official_sources_used: bool = False

    expert_tone_used: bool = False

    freshness_optimized: bool = False

    # =========================================================
    # LEARNING SIGNALS
    # =========================================================

    successful_patterns: List[str] = field(
        default_factory=list
    )

    failed_patterns: List[str] = field(
        default_factory=list
    )

    detected_risks: List[str] = field(
        default_factory=list
    )

    # =========================================================
    # FEEDBACK
    # =========================================================

    human_feedback_score: float = 0.0

    engagement_score: float = 0.0

    trust_feedback_score: float = 0.0

    # =========================================================
    # DECAY
    # =========================================================

    freshness_decay_days: int = 0

    ranking_decay_detected: bool = False

    traffic_decay_detected: bool = False

    # =========================================================
    # TIMESTAMP
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
# DECISION MEMORY
# =============================================================

class DecisionMemory:

    """
    Persistent editorial intelligence memory.
    """

    def __init__(
        self,
    ) -> None:

        self.memory_store: List[
            DecisionMemoryEntry
        ] = []

    # =========================================================
    # STORE
    # =========================================================

    def store(
        self,
        entry: DecisionMemoryEntry,
    ) -> None:

        self.memory_store.append(entry)

    # =========================================================
    # FIND BY NICHE
    # =========================================================

    def find_by_niche(
        self,
        niche: str,
    ) -> List[DecisionMemoryEntry]:

        return [

            entry

            for entry in self.memory_store

            if entry.niche == niche
        ]

    # =========================================================
    # SUCCESSFUL STRATEGIES
    # =========================================================

    def successful_entries(
        self,
    ) -> List[DecisionMemoryEntry]:

        return [

            entry

            for entry in self.memory_store

            if entry.ranking_success
        ]

    # =========================================================
    # FAILED STRATEGIES
    # =========================================================

    def failed_entries(
        self,
    ) -> List[DecisionMemoryEntry]:

        return [

            entry

            for entry in self.memory_store

            if not entry.ranking_success
        ]

    # =========================================================
    # PATTERN LEARNING
    # =========================================================

    def extract_success_patterns(
        self,
    ) -> Dict[str, int]:

        patterns: Dict[str, int] = {}

        for entry in self.successful_entries():

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

        for entry in self.failed_entries():

            for pattern in entry.failed_patterns:

                patterns[pattern] = (
                    patterns.get(pattern, 0) + 1
                )

        return patterns

    # =========================================================
    # FAQ PERFORMANCE
    # =========================================================

    def faq_success_rate(
        self,
    ) -> float:

        faq_entries = [

            entry

            for entry in self.memory_store

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

    def table_success_rate(
        self,
    ) -> float:

        table_entries = [

            entry

            for entry in self.memory_store

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
    # FRESHNESS DECAY
    # =========================================================

    def average_decay_days(
        self,
    ) -> float:

        decay_entries = [

            entry.freshness_decay_days

            for entry in self.memory_store

            if entry.freshness_decay_days > 0
        ]

        if not decay_entries:
            return 0.0

        return round(

            sum(decay_entries) /
            len(decay_entries),

            2,
        )

    # =========================================================
    # TOP STRATEGIES
    # =========================================================

    def top_performing_strategies(
        self,
        limit: int = 5,
    ) -> List[Dict[str, Any]]:

        sorted_entries = sorted(

            self.successful_entries(),

            key=lambda entry: (
                entry.actual_traffic
            ),

            reverse=True,
        )

        top_entries = sorted_entries[:limit]

        return [

            {
                "article_id": (
                    entry.article_id
                ),

                "keyword": (
                    entry.keyword
                ),

                "traffic": (
                    entry.actual_traffic
                ),

                "position": (
                    entry.actual_position
                ),

                "faq_enabled": (
                    entry.faq_enabled
                ),

                "tables_enabled": (
                    entry.tables_enabled
                ),
            }

            for entry in top_entries
        ]

    # =========================================================
    # UPDATE ENTRY
    # =========================================================

    def update_outcome(
        self,
        article_id: str,
        actual_position: Optional[int] = None,
        actual_traffic: Optional[int] = None,
        actual_ctr: Optional[float] = None,
    ) -> bool:

        for entry in self.memory_store:

            if entry.article_id == article_id:

                if actual_position is not None:
                    entry.actual_position = (
                        actual_position
                    )

                if actual_traffic is not None:
                    entry.actual_traffic = (
                        actual_traffic
                    )

                if actual_ctr is not None:
                    entry.actual_ctr = (
                        actual_ctr
                    )

                # =============================================
                # SUCCESS
                # =============================================

                if entry.actual_position <= 10:

                    entry.ranking_success = True

                entry.updated_at = (
                    datetime.utcnow()
                )

                return True

        return False

    # =========================================================
    # EXPORT
    # =========================================================

    def export_memory(
        self,
    ) -> Dict[str, Any]:

        return {

            "total_entries": (
                len(self.memory_store)
            ),

            "successful_entries": (
                len(
                    self.successful_entries()
                )
            ),

            "failed_entries": (
                len(
                    self.failed_entries()
                )
            ),

            "faq_success_rate": (
                self.faq_success_rate()
            ),

            "table_success_rate": (
                self.table_success_rate()
            ),

            "average_decay_days": (
                self.average_decay_days()
            ),

            "success_patterns": (
                self.extract_success_patterns()
            ),

            "failure_patterns": (
                self.extract_failure_patterns()
            ),

            "top_performing_strategies": (
                self.top_performing_strategies()
            ),
        }