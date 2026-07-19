"""
Update Checker

Purpose:
Track and validate update requirements using:
- freshness shifts
- realtime change detection
- version monitoring
- SERP volatility
- content aging analysis

Goal:
Determine when content should be updated
to maintain ranking, trust, and accuracy.

This becomes the update intelligence
layer of AI_COS.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List
from datetime import datetime


# =============================================================
# UPDATE RESULT
# =============================================================

@dataclass
class UpdateCheckResult:

    # =========================================================
    # STATUS
    # =========================================================

    update_required: bool = False

    urgent_update_required: bool = False

    freshness_valid: bool = True

    # =========================================================
    # SCORES
    # =========================================================

    freshness_score: float = 0.0

    update_priority_score: float = 0.0

    content_age_score: float = 0.0

    volatility_score: float = 0.0

    # =========================================================
    # DETECTIONS
    # =========================================================

    outdated_information_detected: bool = False

    serp_shift_detected: bool = False

    ranking_drop_detected: bool = False

    realtime_change_detected: bool = False

    trend_shift_detected: bool = False

    # =========================================================
    # UPDATE TYPES
    # =========================================================

    partial_update_recommended: bool = False

    full_rewrite_recommended: bool = False

    fact_refresh_required: bool = False

    citation_refresh_required: bool = False

    # =========================================================
    # RISKS
    # =========================================================

    freshness_decay_risk: str = "low"

    ranking_loss_risk: str = "low"

    outdated_content_risk: str = "low"

    trust_decay_risk: str = "low"

    # =========================================================
    # SIGNALS
    # =========================================================

    update_signals: Dict[str, Any] = field(
        default_factory=dict
    )

    detected_patterns: List[str] = field(
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

    checked_at: str = field(
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
# UPDATE CHECKER
# =============================================================

class UpdateChecker:

    """
    Content freshness and update intelligence engine.
    """

    # =========================================================
    # FRESH TERMS
    # =========================================================

    FRESH_TERMS = [

        "2026",
        "latest",
        "today",
        "new",
        "updated",
        "live",
        "announcement",
    ]

    # =========================================================
    # VOLATILE TOPICS
    # =========================================================

    VOLATILE_TOPICS = [

        "result",
        "cutoff",
        "ranking",
        "stock",
        "election",
        "price",
        "exam",
        "admit card",
    ]

    # =========================================================
    # CHECK
    # =========================================================

    def check(
        self,
        keyword: str,
        content: str = "",
    ) -> Dict[str, Any]:

        result = (
            UpdateCheckResult()
        )

        keyword = (
            keyword or ""
        ).lower()

        content = (
            content or ""
        ).lower()

        # =====================================================
        # FRESHNESS
        # =====================================================

        self._analyze_freshness(
            result,
            keyword,
            content,
        )

        # =====================================================
        # VOLATILITY
        # =====================================================

        self._analyze_volatility(
            result,
            keyword,
        )

        # =====================================================
        # REALTIME SHIFTS
        # =====================================================

        self._detect_realtime_changes(
            result,
            keyword,
            content,
        )

        # =====================================================
        # UPDATE REQUIREMENTS
        # =====================================================

        self._detect_update_requirements(
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
    # FRESHNESS
    # =========================================================

    def _analyze_freshness(
        self,
        result: UpdateCheckResult,
        keyword: str,
        content: str,
    ) -> None:

        combined = (
            keyword + " " + content
        )

        matches = [

            item

            for item
            in self.FRESH_TERMS

            if item in combined
        ]

        freshness_score = 55.0

        if matches:

            freshness_score += (
                len(matches) * 5
            )

            result.detected_patterns.extend(
                matches
            )

        # =====================================================
        # CURRENT YEAR
        # =====================================================

        current_year = str(
            datetime.utcnow().year
        )

        if current_year in combined:

            freshness_score += 15

        # =====================================================
        # OLD YEARS
        # =====================================================

        if "2023" in combined:

            freshness_score -= 20

            result.outdated_information_detected = (
                True
            )

        result.freshness_score = min(

            max(freshness_score, 0),

            100,
        )

        result.content_age_score = (
            result.freshness_score
        )

    # =========================================================
    # VOLATILITY
    # =========================================================

    def _analyze_volatility(
        self,
        result: UpdateCheckResult,
        keyword: str,
    ) -> None:

        matches = [

            item

            for item
            in self.VOLATILE_TOPICS

            if item in keyword
        ]

        if matches:

            result.serp_shift_detected = (
                True
            )

            result.ranking_drop_detected = (
                True
            )

            result.detected_patterns.extend(
                matches
            )

            result.volatility_score = 85.0

        else:

            result.volatility_score = 45.0

    # =========================================================
    # REALTIME
    # =========================================================

    def _detect_realtime_changes(
        self,
        result: UpdateCheckResult,
        keyword: str,
        content: str,
    ) -> None:

        combined = (
            keyword + " " + content
        )

        realtime_terms = [

            "live",
            "breaking",
            "latest",
            "today",
            "new update",
        ]

        if any(

            item in combined

            for item
            in realtime_terms
        ):

            result.realtime_change_detected = (
                True
            )

            result.trend_shift_detected = (
                True
            )

    # =========================================================
    # UPDATE REQUIREMENTS
    # =========================================================

    def _detect_update_requirements(
        self,
        result: UpdateCheckResult,
    ) -> None:

        # =====================================================
        # OUTDATED
        # =====================================================

        if result.outdated_information_detected:

            result.update_required = (
                True
            )

            result.fact_refresh_required = (
                True
            )

        # =====================================================
        # VOLATILITY
        # =====================================================

        if result.volatility_score >= 80:

            result.partial_update_recommended = (
                True
            )

        # =====================================================
        # LOW FRESHNESS
        # =====================================================

        if result.freshness_score < 50:

            result.full_rewrite_recommended = (
                True
            )

            result.urgent_update_required = (
                True
            )

        # =====================================================
        # CITATIONS
        # =====================================================

        if result.realtime_change_detected:

            result.citation_refresh_required = (
                True
            )

    # =========================================================
    # SCORES
    # =========================================================

    def _calculate_scores(
        self,
        result: UpdateCheckResult,
    ) -> None:

        score = (

            result.freshness_score * 0.5

            +

            result.volatility_score * 0.3

            +

            (
                100
                if result.realtime_change_detected
                else 50
            ) * 0.2
        )

        result.update_priority_score = round(

            100 - score,

            2,
        )

        result.freshness_valid = (

            result.freshness_score >= 60
        )

    # =========================================================
    # RISKS
    # =========================================================

    def _detect_risks(
        self,
        result: UpdateCheckResult,
    ) -> None:

        # =====================================================
        # FRESHNESS
        # =====================================================

        if result.freshness_score < 50:

            result.freshness_decay_risk = (
                "high"
            )

            result.add_warning(
                "Freshness decay detected"
            )

        # =====================================================
        # RANKING
        # =====================================================

        if result.serp_shift_detected:

            result.ranking_loss_risk = (
                "high"
            )

        # =====================================================
        # OUTDATED
        # =====================================================

        if result.outdated_information_detected:

            result.outdated_content_risk = (
                "high"
            )

        # =====================================================
        # TRUST
        # =====================================================

        if result.citation_refresh_required:

            result.trust_decay_risk = (
                "medium"
            )

    # =========================================================
    # FINALIZE
    # =========================================================

    def _finalize(
        self,
        result: UpdateCheckResult,
    ) -> None:

        # =====================================================
        # RECOMMENDATIONS
        # =====================================================

        if result.urgent_update_required:

            result.add_recommendation(
                "Perform urgent content refresh"
            )

            result.add_action(
                "Rewrite outdated sections"
            )

        if result.fact_refresh_required:

            result.add_recommendation(
                "Update factual information"
            )

        if result.citation_refresh_required:

            result.add_recommendation(
                "Refresh citations and references"
            )

        if result.partial_update_recommended:

            result.add_recommendation(
                "Refresh volatile content sections"
            )

        result.add_action(
            "Store freshness update intelligence"
        )

        result.add_reasoning(
            f"Update priority score: "
            f"{result.update_priority_score}"
        )

    # =========================================================
    # EXPORT
    # =========================================================

    def export(
        self,
        result: UpdateCheckResult,
    ) -> Dict[str, Any]:

        return {

            "update_required": (
                result.update_required
            ),

            "urgent_update_required": (
                result.urgent_update_required
            ),

            "freshness_valid": (
                result.freshness_valid
            ),

            "freshness_score": (
                result.freshness_score
            ),

            "update_priority_score": (
                result.update_priority_score
            ),

            "content_age_score": (
                result.content_age_score
            ),

            "volatility_score": (
                result.volatility_score
            ),

            "outdated_information_detected": (
                result.outdated_information_detected
            ),

            "serp_shift_detected": (
                result.serp_shift_detected
            ),

            "ranking_drop_detected": (
                result.ranking_drop_detected
            ),

            "realtime_change_detected": (
                result.realtime_change_detected
            ),

            "trend_shift_detected": (
                result.trend_shift_detected
            ),

            "partial_update_recommended": (
                result.partial_update_recommended
            ),

            "full_rewrite_recommended": (
                result.full_rewrite_recommended
            ),

            "fact_refresh_required": (
                result.fact_refresh_required
            ),

            "citation_refresh_required": (
                result.citation_refresh_required
            ),

            "freshness_decay_risk": (
                result.freshness_decay_risk
            ),

            "ranking_loss_risk": (
                result.ranking_loss_risk
            ),

            "outdated_content_risk": (
                result.outdated_content_risk
            ),

            "trust_decay_risk": (
                result.trust_decay_risk
            ),

            "update_signals": (
                result.update_signals
            ),

            "detected_patterns": (
                result.detected_patterns
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

            "checked_at": (
                result.checked_at
            ),

            "metadata": (
                result.metadata
            ),
        }