"""
Performance Memory

Purpose:
Store long-term REAL performance intelligence.

Tracks:
- rankings
- traffic growth
- CTR evolution
- decay patterns
- engagement signals
- strategy effectiveness

Goal:
Create self-improving SEO intelligence.

This becomes the real-world feedback memory
for adaptive optimization.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Any, List, Optional


# =============================================================
# PERFORMANCE ENTRY
# =============================================================

@dataclass
class PerformanceMemoryEntry:

    # =========================================================
    # ARTICLE
    # =========================================================

    article_id: str

    keyword: str

    niche: str

    url: str

    # =========================================================
    # PUBLISH DATA
    # =========================================================

    published_at: datetime = field(
        default_factory=datetime.utcnow
    )

    # =========================================================
    # RANKINGS
    # =========================================================

    initial_position: int = 100

    best_position: int = 100

    current_position: int = 100

    ranking_improved: bool = False

    ranking_declined: bool = False

    # =========================================================
    # TRAFFIC
    # =========================================================

    initial_traffic: int = 0

    peak_traffic: int = 0

    current_traffic: int = 0

    traffic_growth_detected: bool = False

    traffic_decay_detected: bool = False

    # =========================================================
    # CTR
    # =========================================================

    initial_ctr: float = 0.0

    best_ctr: float = 0.0

    current_ctr: float = 0.0

    # =========================================================
    # ENGAGEMENT
    # =========================================================

    engagement_score: float = 0.0

    bounce_rate: float = 0.0

    average_time_on_page: float = 0.0

    # =========================================================
    # SEO FEATURES
    # =========================================================

    featured_snippet_gained: bool = False

    faq_visibility_detected: bool = False

    video_visibility_detected: bool = False

    # =========================================================
    # STRATEGY SIGNALS
    # =========================================================

    faq_enabled: bool = False

    tables_enabled: bool = False

    comparison_enabled: bool = False

    freshness_optimized: bool = False

    official_sources_used: bool = False

    # =========================================================
    # DECAY
    # =========================================================

    freshness_decay_days: int = 0

    ranking_decay_days: int = 0

    traffic_decay_days: int = 0

    # =========================================================
    # SUCCESS SIGNALS
    # =========================================================

    high_performing: bool = False

    stable_rankings: bool = False

    high_conversion_potential: bool = False

    # =========================================================
    # LEARNING
    # =========================================================

    successful_patterns: List[str] = field(
        default_factory=list
    )

    failed_patterns: List[str] = field(
        default_factory=list
    )

    performance_signals: Dict[str, Any] = field(
        default_factory=dict
    )

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
# PERFORMANCE MEMORY
# =============================================================

class PerformanceMemory:

    """
    Real-world SEO performance memory.
    """

    def __init__(
        self,
    ) -> None:

        self.performance_store: List[
            PerformanceMemoryEntry
        ] = []

    # =========================================================
    # STORE
    # =========================================================

    def store(
        self,
        entry: PerformanceMemoryEntry,
    ) -> None:

        self.performance_store.append(
            entry
        )

    # =========================================================
    # UPDATE PERFORMANCE
    # =========================================================

    def update_performance(
        self,
        article_id: str,
        position: Optional[int] = None,
        traffic: Optional[int] = None,
        ctr: Optional[float] = None,
        engagement_score: Optional[float] = None,
    ) -> bool:

        for entry in self.performance_store:

            if entry.article_id == article_id:

                # =============================================
                # POSITION
                # =============================================

                if position is not None:

                    entry.current_position = (
                        position
                    )

                    if (
                        position <
                        entry.best_position
                    ):

                        entry.best_position = (
                            position
                        )

                        entry.ranking_improved = (
                            True
                        )

                # =============================================
                # TRAFFIC
                # =============================================

                if traffic is not None:

                    entry.current_traffic = (
                        traffic
                    )

                    if (
                        traffic >
                        entry.peak_traffic
                    ):

                        entry.peak_traffic = (
                            traffic
                        )

                        entry.traffic_growth_detected = (
                            True
                        )

                # =============================================
                # CTR
                # =============================================

                if ctr is not None:

                    entry.current_ctr = ctr

                    if ctr > entry.best_ctr:

                        entry.best_ctr = ctr

                # =============================================
                # ENGAGEMENT
                # =============================================

                if (
                    engagement_score
                    is not None
                ):

                    entry.engagement_score = (
                        engagement_score
                    )

                # =============================================
                # PERFORMANCE FLAGS
                # =============================================

                self._evaluate_entry(
                    entry
                )

                entry.updated_at = (
                    datetime.utcnow()
                )

                return True

        return False

    # =========================================================
    # EVALUATE ENTRY
    # =========================================================

    def _evaluate_entry(
        self,
        entry: PerformanceMemoryEntry,
    ) -> None:

        # =====================================================
        # HIGH PERFORMANCE
        # =====================================================

        if (

            entry.current_position <= 10

            and

            entry.current_traffic >= 1000
        ):

            entry.high_performing = True

        # =====================================================
        # STABILITY
        # =====================================================

        if (
            entry.current_position <= 10
        ):

            entry.stable_rankings = True

        # =====================================================
        # CONVERSION
        # =====================================================

        if (
            entry.current_ctr >= 0.15
        ):

            entry.high_conversion_potential = (
                True
            )

    # =========================================================
    # TOP ARTICLES
    # =========================================================

    def top_articles(
        self,
        limit: int = 10,
    ) -> List[PerformanceMemoryEntry]:

        return sorted(

            self.performance_store,

            key=lambda entry: (
                entry.current_traffic
            ),

            reverse=True,
        )[:limit]

    # =========================================================
    # FAQ PERFORMANCE
    # =========================================================

    def faq_performance_score(
        self,
    ) -> float:

        faq_entries = [

            entry

            for entry in self.performance_store

            if entry.faq_enabled
        ]

        if not faq_entries:
            return 0.0

        successful = len([

            entry

            for entry in faq_entries

            if entry.high_performing
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

    def table_performance_score(
        self,
    ) -> float:

        table_entries = [

            entry

            for entry in self.performance_store

            if entry.tables_enabled
        ]

        if not table_entries:
            return 0.0

        successful = len([

            entry

            for entry in table_entries

            if entry.high_performing
        ])

        return round(

            (
                successful /
                len(table_entries)
            ) * 100,

            2,
        )

    # =========================================================
    # FEATURED SNIPPET SUCCESS
    # =========================================================

    def snippet_success_rate(
        self,
    ) -> float:

        snippet_entries = [

            entry

            for entry in self.performance_store

            if entry.featured_snippet_gained
        ]

        if not snippet_entries:
            return 0.0

        return round(

            (
                len(snippet_entries) /
                len(self.performance_store)
            ) * 100,

            2,
        )

    # =========================================================
    # DECAY ANALYSIS
    # =========================================================

    def average_decay_days(
        self,
    ) -> float:

        decay_entries = [

            entry.ranking_decay_days

            for entry in self.performance_store

            if entry.ranking_decay_days > 0
        ]

        if not decay_entries:
            return 0.0

        return round(

            (
                sum(decay_entries) /
                len(decay_entries)
            ),

            2,
        )

    # =========================================================
    # SUCCESS PATTERNS
    # =========================================================

    def extract_success_patterns(
        self,
    ) -> Dict[str, int]:

        patterns: Dict[str, int] = {}

        successful_entries = [

            entry

            for entry in self.performance_store

            if entry.high_performing
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

            for entry in self.performance_store

            if not entry.high_performing
        ]

        for entry in failed_entries:

            for pattern in entry.failed_patterns:

                patterns[pattern] = (

                    patterns.get(pattern, 0) + 1
                )

        return patterns

    # =========================================================
    # EXPORT
    # =========================================================

    def export_memory(
        self,
    ) -> Dict[str, Any]:

        return {

            "total_entries": (
                len(self.performance_store)
            ),

            "high_performing_articles": (
                len([

                    entry

                    for entry in self.performance_store

                    if entry.high_performing
                ])
            ),

            "faq_performance_score": (
                self.faq_performance_score()
            ),

            "table_performance_score": (
                self.table_performance_score()
            ),

            "snippet_success_rate": (
                self.snippet_success_rate()
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

            "top_articles": [

                {
                    "article_id": (
                        entry.article_id
                    ),

                    "keyword": (
                        entry.keyword
                    ),

                    "traffic": (
                        entry.current_traffic
                    ),

                    "position": (
                        entry.current_position
                    ),
                }

                for entry in self.top_articles()
            ],
        }