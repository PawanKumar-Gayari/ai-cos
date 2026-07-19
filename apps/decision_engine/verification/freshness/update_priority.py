"""
Update Priority

Purpose:
Calculate content update priority using:
- freshness decay
- SERP volatility
- stale signals
- realtime relevance
- ranking risk

Goal:
Prioritize which content should be updated
first for maximum SEO and ranking impact.

This becomes the update prioritization
layer of AI_COS.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List
from datetime import datetime


# =============================================================
# UPDATE PRIORITY RESULT
# =============================================================

@dataclass
class UpdatePriorityResult:

    # =========================================================
    # STATUS
    # =========================================================

    update_required: bool = False

    urgent_update_required: bool = False

    realtime_refresh_required: bool = False

    # =========================================================
    # SCORES
    # =========================================================

    priority_score: float = 0.0

    freshness_score: float = 0.0

    volatility_score: float = 0.0

    ranking_risk_score: float = 0.0

    # =========================================================
    # DETECTIONS
    # =========================================================

    stale_content_detected: bool = False

    realtime_topic_detected: bool = False

    serp_volatility_detected: bool = False

    outdated_information_detected: bool = False

    trend_shift_detected: bool = False

    # =========================================================
    # PRIORITY
    # =========================================================

    priority_level: str = "medium"

    update_type: str = "partial"

    freshness_status: str = "stable"

    # =========================================================
    # RISKS
    # =========================================================

    ranking_loss_risk: str = "low"

    freshness_decay_risk: str = "low"

    trust_decay_risk: str = "low"

    traffic_loss_risk: str = "low"

    # =========================================================
    # SIGNALS
    # =========================================================

    update_signals: Dict[str, Any] = field(
        default_factory=dict
    )

    matched_patterns: List[str] = field(
        default_factory=list
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

    analyzed_at: str = field(
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
# UPDATE PRIORITY
# =============================================================

class UpdatePriority:

    """
    Update prioritization intelligence engine.
    """

    # =========================================================
    # REALTIME TERMS
    # =========================================================

    REALTIME_TERMS = [

        "latest",
        "today",
        "live",
        "updated",
        "breaking",
        "announcement",
        "new",
    ]

    # =========================================================
    # VOLATILE TERMS
    # =========================================================

    VOLATILE_TERMS = [

        "result",
        "cutoff",
        "ranking",
        "stock",
        "price",
        "exam",
        "admit card",
        "score",
    ]

    # =========================================================
    # OLD TERMS
    # =========================================================

    OLD_TERMS = [

        "2022",
        "2021",
        "2020",
        "old syllabus",
        "deprecated",
        "obsolete",
    ]

    # =========================================================
    # CALCULATE
    # =========================================================

    def calculate(
        self,
        content: str,
        keyword: str = "",
    ) -> Dict[str, Any]:

        result = (
            UpdatePriorityResult()
        )

        combined = (

            (
                keyword or ""
            )

            +

            " "

            +

            (
                content or ""
            )

        ).lower()

        # =====================================================
        # DETECTIONS
        # =====================================================

        self._detect_realtime_topics(
            result,
            combined,
        )

        self._detect_volatility(
            result,
            combined,
        )

        self._detect_staleness(
            result,
            combined,
        )

        # =====================================================
        # SCORES
        # =====================================================

        self._calculate_scores(
            result
        )

        # =====================================================
        # PRIORITY
        # =====================================================

        self._classify_priority(
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
    # REALTIME
    # =========================================================

    def _detect_realtime_topics(
        self,
        result: UpdatePriorityResult,
        content: str,
    ) -> None:

        matches = [

            item

            for item
            in self.REALTIME_TERMS

            if item in content
        ]

        if matches:

            result.realtime_topic_detected = (
                True
            )

            result.realtime_refresh_required = (
                True
            )

            result.matched_patterns.extend(
                matches
            )

    # =========================================================
    # VOLATILITY
    # =========================================================

    def _detect_volatility(
        self,
        result: UpdatePriorityResult,
        content: str,
    ) -> None:

        matches = [

            item

            for item
            in self.VOLATILE_TERMS

            if item in content
        ]

        if matches:

            result.serp_volatility_detected = (
                True
            )

            result.trend_shift_detected = (
                True
            )

            result.matched_patterns.extend(
                matches
            )

    # =========================================================
    # STALENESS
    # =========================================================

    def _detect_staleness(
        self,
        result: UpdatePriorityResult,
        content: str,
    ) -> None:

        matches = [

            item

            for item
            in self.OLD_TERMS

            if item in content
        ]

        if matches:

            result.stale_content_detected = (
                True
            )

            result.outdated_information_detected = (
                True
            )

            result.matched_patterns.extend(
                matches
            )

    # =========================================================
    # SCORES
    # =========================================================

    def _calculate_scores(
        self,
        result: UpdatePriorityResult,
    ) -> None:

        freshness = 80.0

        volatility = 40.0

        ranking_risk = 30.0

        priority = 25.0

        # =====================================================
        # REALTIME
        # =====================================================

        if result.realtime_topic_detected:

            freshness -= 15

            priority += 20

        # =====================================================
        # VOLATILITY
        # =====================================================

        if result.serp_volatility_detected:

            volatility += 40

            ranking_risk += 35

            priority += 25

        # =====================================================
        # STALE
        # =====================================================

        if result.stale_content_detected:

            freshness -= 35

            ranking_risk += 30

            priority += 35

        result.freshness_score = min(

            max(freshness, 0),

            100,
        )

        result.volatility_score = min(

            max(volatility, 0),

            100,
        )

        result.ranking_risk_score = min(

            max(ranking_risk, 0),

            100,
        )

        result.priority_score = min(

            max(priority, 0),

            100,
        )

    # =========================================================
    # PRIORITY
    # =========================================================

    def _classify_priority(
        self,
        result: UpdatePriorityResult,
    ) -> None:

        # =====================================================
        # LEVEL
        # =====================================================

        if result.priority_score >= 80:

            result.priority_level = (
                "critical"
            )

            result.urgent_update_required = (
                True
            )

            result.update_required = (
                True
            )

        elif result.priority_score >= 60:

            result.priority_level = (
                "high"
            )

            result.update_required = (
                True
            )

        elif result.priority_score >= 40:

            result.priority_level = (
                "medium"
            )

        else:

            result.priority_level = (
                "low"
            )

        # =====================================================
        # UPDATE TYPE
        # =====================================================

        if result.stale_content_detected:

            result.update_type = (
                "full_refresh"
            )

        elif result.serp_volatility_detected:

            result.update_type = (
                "partial_refresh"
            )

        else:

            result.update_type = (
                "light_update"
            )

        # =====================================================
        # STATUS
        # =====================================================

        if result.freshness_score >= 75:

            result.freshness_status = (
                "fresh"
            )

        elif result.freshness_score >= 50:

            result.freshness_status = (
                "aging"
            )

        else:

            result.freshness_status = (
                "outdated"
            )

    # =========================================================
    # RISKS
    # =========================================================

    def _detect_risks(
        self,
        result: UpdatePriorityResult,
    ) -> None:

        # =====================================================
        # RANKING
        # =====================================================

        if result.ranking_risk_score >= 70:

            result.ranking_loss_risk = (
                "high"
            )

            result.add_warning(
                "High ranking loss probability detected"
            )

        # =====================================================
        # FRESHNESS
        # =====================================================

        if result.freshness_score < 50:

            result.freshness_decay_risk = (
                "high"
            )

        # =====================================================
        # TRUST
        # =====================================================

        if result.outdated_information_detected:

            result.trust_decay_risk = (
                "medium"
            )

        # =====================================================
        # TRAFFIC
        # =====================================================

        if result.priority_level in [

            "critical",
            "high",
        ]:

            result.traffic_loss_risk = (
                "high"
            )

    # =========================================================
    # FINALIZE
    # =========================================================

    def _finalize(
        self,
        result: UpdatePriorityResult,
    ) -> None:

        # =====================================================
        # RECOMMENDATIONS
        # =====================================================

        if result.urgent_update_required:

            result.add_recommendation(
                "Perform urgent content update"
            )

            result.add_action(
                "Refresh critical sections immediately"
            )

        if result.realtime_refresh_required:

            result.add_recommendation(
                "Enable realtime monitoring"
            )

        if result.stale_content_detected:

            result.add_recommendation(
                "Replace outdated information"
            )

        if result.serp_volatility_detected:

            result.add_recommendation(
                "Monitor SERP changes continuously"
            )

        result.add_action(
            "Store update priority intelligence"
        )

        result.add_reasoning(
            f"Priority score: "
            f"{result.priority_score}"
        )

    # =========================================================
    # EXPORT
    # =========================================================

    def export(
        self,
        result: UpdatePriorityResult,
    ) -> Dict[str, Any]:

        return {

            "update_required": (
                result.update_required
            ),

            "urgent_update_required": (
                result.urgent_update_required
            ),

            "realtime_refresh_required": (
                result.realtime_refresh_required
            ),

            "priority_score": (
                result.priority_score
            ),

            "freshness_score": (
                result.freshness_score
            ),

            "volatility_score": (
                result.volatility_score
            ),

            "ranking_risk_score": (
                result.ranking_risk_score
            ),

            "stale_content_detected": (
                result.stale_content_detected
            ),

            "realtime_topic_detected": (
                result.realtime_topic_detected
            ),

            "serp_volatility_detected": (
                result.serp_volatility_detected
            ),

            "outdated_information_detected": (
                result.outdated_information_detected
            ),

            "trend_shift_detected": (
                result.trend_shift_detected
            ),

            "priority_level": (
                result.priority_level
            ),

            "update_type": (
                result.update_type
            ),

            "freshness_status": (
                result.freshness_status
            ),

            "ranking_loss_risk": (
                result.ranking_loss_risk
            ),

            "freshness_decay_risk": (
                result.freshness_decay_risk
            ),

            "trust_decay_risk": (
                result.trust_decay_risk
            ),

            "traffic_loss_risk": (
                result.traffic_loss_risk
            ),

            "update_signals": (
                result.update_signals
            ),

            "matched_patterns": (
                result.matched_patterns
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

            "analyzed_at": (
                result.analyzed_at
            ),

            "metadata": (
                result.metadata
            ),
        }