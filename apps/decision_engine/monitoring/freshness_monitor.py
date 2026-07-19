"""
Freshness Monitor

Purpose:
Continuously monitor content freshness lifecycle.

Tracks:
- freshness decay
- stale content
- update urgency
- reverification requirements
- ranking decay risk
- traffic decay risk

Goal:
Enable automated freshness intelligence.

This becomes the freshness observability layer
of AI_COS.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Any, List


# =============================================================
# MONITOR ENTRY
# =============================================================

@dataclass
class FreshnessMonitorEntry:

    # =========================================================
    # ARTICLE
    # =========================================================

    article_id: str

    keyword: str

    niche: str

    url: str

    # =========================================================
    # PUBLISHING
    # =========================================================

    published_at: datetime

    last_verified_at: datetime

    last_updated_at: datetime

    # =========================================================
    # FRESHNESS
    # =========================================================

    freshness_score: float = 100.0

    freshness_valid: bool = True

    freshness_expired: bool = False

    freshness_sensitive: bool = False

    # =========================================================
    # AGE
    # =========================================================

    content_age_days: int = 0

    max_valid_days: int = 30

    predicted_decay_days: int = 30

    # =========================================================
    # DECAY
    # =========================================================

    decay_probability: float = 0.0

    decay_risk: str = "low"

    ranking_decay_risk: str = "low"

    traffic_decay_risk: str = "low"

    # =========================================================
    # UPDATE
    # =========================================================

    update_required: bool = False

    urgent_update_required: bool = False

    reverification_required: bool = False

    auto_refresh_recommended: bool = False

    # =========================================================
    # MONITORING SIGNALS
    # =========================================================

    stale_content_detected: bool = False

    outdated_facts_detected: bool = False

    outdated_statistics_detected: bool = False

    outdated_links_detected: bool = False

    # =========================================================
    # PERFORMANCE
    # =========================================================

    ranking_drop_detected: bool = False

    traffic_drop_detected: bool = False

    ctr_drop_detected: bool = False

    # =========================================================
    # ACTIONS
    # =========================================================

    recommended_actions: List[str] = field(
        default_factory=list
    )

    # =========================================================
    # SIGNALS
    # =========================================================

    freshness_signals: Dict[str, Any] = field(
        default_factory=dict
    )

    # =========================================================
    # REASONING
    # =========================================================

    reasoning: List[str] = field(
        default_factory=list
    )

    warnings: List[str] = field(
        default_factory=list
    )

    recommendations: List[str] = field(
        default_factory=list
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

    # =========================================================
    # UTILITIES
    # =========================================================

    def add_reasoning(
        self,
        message: str,
    ) -> None:

        if (
            message
            and message not in self.reasoning
        ):

            self.reasoning.append(message)

    def add_warning(
        self,
        warning: str,
    ) -> None:

        if (
            warning
            and warning not in self.warnings
        ):

            self.warnings.append(warning)

    def add_recommendation(
        self,
        recommendation: str,
    ) -> None:

        if (
            recommendation
            and recommendation
            not in self.recommendations
        ):

            self.recommendations.append(
                recommendation
            )

    def add_action(
        self,
        action: str,
    ) -> None:

        if (
            action
            and action
            not in self.recommended_actions
        ):

            self.recommended_actions.append(
                action
            )


# =============================================================
# FRESHNESS MONITOR
# =============================================================

class FreshnessMonitor:

    """
    Continuous freshness monitoring engine.
    """

    def __init__(
        self,
    ) -> None:

        self.entries: List[
            FreshnessMonitorEntry
        ] = []

    # =========================================================
    # STORE
    # =========================================================

    def store(
        self,
        entry: FreshnessMonitorEntry,
    ) -> None:

        self.entries.append(entry)

    # =========================================================
    # RUN MONITORING
    # =========================================================

    def monitor(
        self,
    ) -> None:

        for entry in self.entries:

            self._update_age(
                entry
            )

            self._evaluate_decay(
                entry
            )

            self._detect_staleness(
                entry
            )

            self._evaluate_updates(
                entry
            )

            entry.updated_at = (
                datetime.utcnow()
            )

    # =========================================================
    # AGE
    # =========================================================

    def _update_age(
        self,
        entry: FreshnessMonitorEntry,
    ) -> None:

        now = datetime.utcnow()

        delta = (
            now -
            entry.last_updated_at
        )

        entry.content_age_days = (
            delta.days
        )

    # =========================================================
    # DECAY
    # =========================================================

    def _evaluate_decay(
        self,
        entry: FreshnessMonitorEntry,
    ) -> None:

        ratio = (

            entry.content_age_days /

            max(entry.max_valid_days, 1)
        )

        entry.decay_probability = round(
            min(ratio * 100, 100),
            2,
        )

        # =====================================================
        # RISK
        # =====================================================

        if entry.decay_probability >= 80:

            entry.decay_risk = "critical"

        elif entry.decay_probability >= 60:

            entry.decay_risk = "high"

        elif entry.decay_probability >= 35:

            entry.decay_risk = "medium"

        else:

            entry.decay_risk = "low"

        # =====================================================
        # PREDICTED DECAY
        # =====================================================

        entry.predicted_decay_days = max(

            entry.max_valid_days -

            entry.content_age_days,

            0,
        )

    # =========================================================
    # STALE DETECTION
    # =========================================================

    def _detect_staleness(
        self,
        entry: FreshnessMonitorEntry,
    ) -> None:

        # =====================================================
        # STALE
        # =====================================================

        if (
            entry.content_age_days >
            entry.max_valid_days
        ):

            entry.stale_content_detected = (
                True
            )

            entry.freshness_expired = (
                True
            )

            entry.freshness_valid = (
                False
            )

            entry.add_warning(
                "Freshness validity expired"
            )

        # =====================================================
        # OUTDATED
        # =====================================================

        if entry.decay_risk in [
            "high",
            "critical",
        ]:

            entry.outdated_facts_detected = (
                True
            )

            entry.add_warning(
                "Potential outdated facts detected"
            )

    # =========================================================
    # UPDATE EVALUATION
    # =========================================================

    def _evaluate_updates(
        self,
        entry: FreshnessMonitorEntry,
    ) -> None:

        # =====================================================
        # UPDATE REQUIRED
        # =====================================================

        if (

            entry.freshness_expired

            or

            entry.decay_risk in [
                "high",
                "critical",
            ]
        ):

            entry.update_required = True

            entry.reverification_required = (
                True
            )

            entry.add_action(
                "Reverify article facts"
            )

            entry.add_action(
                "Refresh outdated sections"
            )

        # =====================================================
        # URGENT
        # =====================================================

        if (
            entry.decay_risk == "critical"
        ):

            entry.urgent_update_required = (
                True
            )

            entry.auto_refresh_recommended = (
                True
            )

            entry.ranking_decay_risk = (
                "high"
            )

            entry.traffic_decay_risk = (
                "high"
            )

            entry.add_warning(
                "Urgent freshness update required"
            )

        # =====================================================
        # RECOMMENDATIONS
        # =====================================================

        if entry.freshness_sensitive:

            entry.add_recommendation(
                "Increase freshness monitoring frequency"
            )

        if entry.auto_refresh_recommended:

            entry.add_recommendation(
                "Enable automatic refresh pipeline"
            )

    # =========================================================
    # EXPIRED ENTRIES
    # =========================================================

    def expired_entries(
        self,
    ) -> List[FreshnessMonitorEntry]:

        return [

            entry

            for entry in self.entries

            if entry.freshness_expired
        ]

    # =========================================================
    # UPDATE REQUIRED
    # =========================================================

    def update_required_entries(
        self,
    ) -> List[FreshnessMonitorEntry]:

        return [

            entry

            for entry in self.entries

            if entry.update_required
        ]

    # =========================================================
    # URGENT ENTRIES
    # =========================================================

    def urgent_entries(
        self,
    ) -> List[FreshnessMonitorEntry]:

        return [

            entry

            for entry in self.entries

            if entry.urgent_update_required
        ]

    # =========================================================
    # HIGH DECAY
    # =========================================================

    def high_decay_entries(
        self,
    ) -> List[FreshnessMonitorEntry]:

        return [

            entry

            for entry in self.entries

            if entry.decay_risk in [
                "high",
                "critical",
            ]
        ]

    # =========================================================
    # AVERAGE FRESHNESS
    # =========================================================

    def average_freshness_score(
        self,
    ) -> float:

        if not self.entries:
            return 0.0

        return round(

            (
                sum(

                    entry.freshness_score

                    for entry in self.entries
                ) /

                len(self.entries)
            ),

            2,
        )

    # =========================================================
    # EXPORT
    # =========================================================

    def export_metrics(
        self,
    ) -> Dict[str, Any]:

        return {

            "total_entries": (
                len(self.entries)
            ),

            "expired_entries": (
                len(
                    self.expired_entries()
                )
            ),

            "update_required_entries": (
                len(
                    self.update_required_entries()
                )
            ),

            "urgent_entries": (
                len(
                    self.urgent_entries()
                )
            ),

            "high_decay_entries": (
                len(
                    self.high_decay_entries()
                )
            ),

            "average_freshness_score": (
                self.average_freshness_score()
            ),
        }