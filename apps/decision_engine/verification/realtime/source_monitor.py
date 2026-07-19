"""
Source Monitor

Purpose:
Monitor source ecosystem health using:
- source stability
- authority consistency
- trust fluctuations
- realtime source changes
- freshness monitoring

Goal:
Continuously track whether content sources
remain trustworthy and reliable over time.

This becomes the source monitoring
intelligence layer of AI_COS.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List
from datetime import datetime


# =============================================================
# MONITOR RESULT
# =============================================================

@dataclass
class SourceMonitorResult:

    # =========================================================
    # STATUS
    # =========================================================

    monitoring_active: bool = False

    monitoring_score: float = 0.0

    source_stability_score: float = 0.0

    # =========================================================
    # COUNTS
    # =========================================================

    total_sources: int = 0

    trusted_sources: int = 0

    unstable_sources: int = 0

    flagged_sources: int = 0

    # =========================================================
    # DETECTIONS
    # =========================================================

    trust_shift_detected: bool = False

    authority_drop_detected: bool = False

    freshness_issue_detected: bool = False

    realtime_change_detected: bool = False

    # =========================================================
    # RISKS
    # =========================================================

    source_decay_risk: str = "low"

    misinformation_risk: str = "low"

    trust_instability_risk: str = "low"

    freshness_risk: str = "low"

    # =========================================================
    # SOURCE DATA
    # =========================================================

    monitored_sources: List[Dict[str, Any]] = field(
        default_factory=list
    )

    unstable_source_list: List[str] = field(
        default_factory=list
    )

    flagged_source_list: List[str] = field(
        default_factory=list
    )

    # =========================================================
    # SIGNALS
    # =========================================================

    monitoring_signals: Dict[str, Any] = field(
        default_factory=dict
    )

    # =========================================================
    # RECOMMENDATIONS
    # =========================================================

    recommendations: List[str] = field(
        default_factory=list
    )

    warnings: List[str] = field(
        default_factory=list
    )

    reasoning: List[str] = field(
        default_factory=list
    )

    # =========================================================
    # ACTIONS
    # =========================================================

    recommended_actions: List[str] = field(
        default_factory=list
    )

    # =========================================================
    # META
    # =========================================================

    monitored_at: str = field(
        default_factory=lambda:
        datetime.utcnow().isoformat()
    )

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
# SOURCE MONITOR
# =============================================================

class SourceMonitor:

    """
    Source monitoring intelligence engine.
    """

    # =========================================================
    # TRUSTED DOMAINS
    # =========================================================

    TRUSTED_DOMAINS = [

        "google.com",
        "github.com",
        "openai.com",
        "wikipedia.org",
        "nih.gov",
        "nature.com",
    ]

    # =========================================================
    # FLAGGED SIGNALS
    # =========================================================

    FLAGGED_SIGNALS = [

        "spam",
        "fake",
        "rumor",
        "clickbait",
        "mirror-site",
    ]

    # =========================================================
    # MONITOR
    # =========================================================

    def monitor(
        self,
        sources: List[str],
    ) -> Dict[str, Any]:

        result = (
            SourceMonitorResult()
        )

        sources = (
            sources or []
        )

        result.total_sources = (
            len(sources)
        )

        result.monitoring_active = (
            True
        )

        monitored = []

        # =====================================================
        # PROCESS
        # =====================================================

        for source in sources:

            source_data = (
                self._monitor_source(
                    source
                )
            )

            monitored.append(
                source_data
            )

        result.monitored_sources = (
            monitored
        )

        # =====================================================
        # COUNTS
        # =====================================================

        result.trusted_sources = sum(

            1

            for item
            in monitored

            if item.get(
                "trusted",
                False,
            )
        )

        result.unstable_sources = sum(

            1

            for item
            in monitored

            if item.get(
                "unstable",
                False,
            )
        )

        result.flagged_sources = sum(

            1

            for item
            in monitored

            if item.get(
                "flagged",
                False,
            )
        )

        result.unstable_source_list = [

            item["source"]

            for item
            in monitored

            if item.get(
                "unstable",
                False,
            )
        ]

        result.flagged_source_list = [

            item["source"]

            for item
            in monitored

            if item.get(
                "flagged",
                False,
            )
        ]

        # =====================================================
        # DETECTIONS
        # =====================================================

        self._detect_changes(
            result
        )

        # =====================================================
        # SCORES
        # =====================================================

        self._calculate_scores(
            result
        )

        # =====================================================
        # RISKS
        # =====================================================

        self._detect_risks(
            result
        )

        # =====================================================
        # FINALIZE
        # =====================================================

        self._finalize(
            result
        )

        return self.export(
            result
        )

    # =========================================================
    # MONITOR SOURCE
    # =========================================================

    def _monitor_source(
        self,
        source: str,
    ) -> Dict[str, Any]:

        source_lower = (
            source.lower()
        )

        trusted = any(

            item in source_lower

            for item
            in self.TRUSTED_DOMAINS
        )

        flagged = any(

            item in source_lower

            for item
            in self.FLAGGED_SIGNALS
        )

        unstable = (

            "2023" in source_lower
            or
            "old" in source_lower
        )

        freshness_score = 70.0

        if "2026" in source_lower:

            freshness_score = 95.0

        elif "2025" in source_lower:

            freshness_score = 85.0

        elif "2024" in source_lower:

            freshness_score = 75.0

        return {

            "source": source,

            "trusted": trusted,

            "flagged": flagged,

            "unstable": unstable,

            "freshness_score": freshness_score,
        }

    # =========================================================
    # DETECT CHANGES
    # =========================================================

    def _detect_changes(
        self,
        result: SourceMonitorResult,
    ) -> None:

        if result.unstable_sources > 0:

            result.trust_shift_detected = (
                True
            )

            result.freshness_issue_detected = (
                True
            )

        if result.flagged_sources > 0:

            result.authority_drop_detected = (
                True
            )

            result.realtime_change_detected = (
                True
            )

    # =========================================================
    # SCORES
    # =========================================================

    def _calculate_scores(
        self,
        result: SourceMonitorResult,
    ) -> None:

        if result.total_sources == 0:

            return

        trusted_ratio = (

            result.trusted_sources
            /
            result.total_sources
        ) * 100

        penalty = (

            result.flagged_sources * 15
            +
            result.unstable_sources * 10
        )

        score = max(

            trusted_ratio - penalty,

            0,
        )

        result.monitoring_score = round(

            score,

            2,
        )

        result.source_stability_score = round(

            max(
                100 - penalty,
                0,
            ),

            2,
        )

    # =========================================================
    # RISKS
    # =========================================================

    def _detect_risks(
        self,
        result: SourceMonitorResult,
    ) -> None:

        # =====================================================
        # DECAY
        # =====================================================

        if result.unstable_sources >= 2:

            result.source_decay_risk = (
                "high"
            )

            result.add_warning(
                "Source instability detected"
            )

        # =====================================================
        # MISINFORMATION
        # =====================================================

        if result.flagged_sources >= 1:

            result.misinformation_risk = (
                "high"
            )

            result.add_warning(
                "Flagged source patterns detected"
            )

        # =====================================================
        # TRUST
        # =====================================================

        if result.monitoring_score < 50:

            result.trust_instability_risk = (
                "high"
            )

        # =====================================================
        # FRESHNESS
        # =====================================================

        if result.freshness_issue_detected:

            result.freshness_risk = (
                "medium"
            )

    # =========================================================
    # FINALIZE
    # =========================================================

    def _finalize(
        self,
        result: SourceMonitorResult,
    ) -> None:

        # =====================================================
        # RECOMMENDATIONS
        # =====================================================

        if result.source_decay_risk == "high":

            result.add_recommendation(
                "Replace unstable sources"
            )

            result.add_action(
                "Refresh outdated references"
            )

        if result.misinformation_risk == "high":

            result.add_recommendation(
                "Remove flagged domains"
            )

            result.add_action(
                "Use verified authority sources"
            )

        if result.trust_instability_risk == "high":

            result.add_recommendation(
                "Increase trusted source ratio"
            )

        result.add_action(
            "Store source monitoring intelligence"
        )

        result.add_reasoning(
            f"Monitoring score: "
            f"{result.monitoring_score}"
        )

    # =========================================================
    # EXPORT
    # =========================================================

    def export(
        self,
        result: SourceMonitorResult,
    ) -> Dict[str, Any]:

        return {

            "monitoring_active": (
                result.monitoring_active
            ),

            "monitoring_score": (
                result.monitoring_score
            ),

            "source_stability_score": (
                result.source_stability_score
            ),

            "total_sources": (
                result.total_sources
            ),

            "trusted_sources": (
                result.trusted_sources
            ),

            "unstable_sources": (
                result.unstable_sources
            ),

            "flagged_sources": (
                result.flagged_sources
            ),

            "trust_shift_detected": (
                result.trust_shift_detected
            ),

            "authority_drop_detected": (
                result.authority_drop_detected
            ),

            "freshness_issue_detected": (
                result.freshness_issue_detected
            ),

            "realtime_change_detected": (
                result.realtime_change_detected
            ),

            "source_decay_risk": (
                result.source_decay_risk
            ),

            "misinformation_risk": (
                result.misinformation_risk
            ),

            "trust_instability_risk": (
                result.trust_instability_risk
            ),

            "freshness_risk": (
                result.freshness_risk
            ),

            "monitored_sources": (
                result.monitored_sources
            ),

            "unstable_source_list": (
                result.unstable_source_list
            ),

            "flagged_source_list": (
                result.flagged_source_list
            ),

            "monitoring_signals": (
                result.monitoring_signals
            ),

            "recommendations": (
                result.recommendations
            ),

            "warnings": (
                result.warnings
            ),

            "reasoning": (
                result.reasoning
            ),

            "recommended_actions": (
                result.recommended_actions
            ),

            "monitored_at": (
                result.monitored_at
            ),

            "metadata": (
                result.metadata
            ),
        }