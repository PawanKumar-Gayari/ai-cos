"""
Freshness Detector

Purpose:
Detect content freshness using:
- publication recency
- realtime keywords
- trend activity
- update signals
- temporal relevance

Goal:
Measure how fresh and current content is
for SEO and ranking intelligence.

This becomes the freshness detection
layer of AI_COS.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List
from datetime import datetime


# =============================================================
# FRESHNESS RESULT
# =============================================================

@dataclass
class FreshnessResult:

    freshness_score: float = 0.0

    freshness_level: str = "medium"

    realtime_relevance: bool = False

    update_detected: bool = False

    stale_content_detected: bool = False

    freshness_decay_risk: str = "low"

    detected_patterns: List[str] = field(
        default_factory=list
    )

    recommendations: List[str] = field(
        default_factory=list
    )

    reasoning: List[str] = field(
        default_factory=list
    )

    metadata: Dict[str, Any] = field(
        default_factory=dict
    )

    def add_reasoning(
        self,
        message: str,
    ) -> None:

        if (
            message
            and message not in self.reasoning
        ):

            self.reasoning.append(message)


# =============================================================
# FRESHNESS DETECTOR
# =============================================================

class FreshnessDetector:

    """
    Freshness intelligence engine.
    """

    FRESH_TERMS = [

        "2026",
        "latest",
        "today",
        "updated",
        "new",
        "live",
    ]

    OLD_TERMS = [

        "2022",
        "2021",
        "2020",
    ]

    # =========================================================
    # DETECT
    # =========================================================

    def detect(
        self,
        content: str,
        keyword: str = "",
    ) -> Dict[str, Any]:

        result = FreshnessResult()

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

        score = 55.0

        # =====================================================
        # FRESH TERMS
        # =====================================================

        fresh_matches = [

            item

            for item
            in self.FRESH_TERMS

            if item in combined
        ]

        if fresh_matches:

            score += (
                len(fresh_matches) * 6
            )

            result.detected_patterns.extend(
                fresh_matches
            )

            result.update_detected = True

        # =====================================================
        # OLD TERMS
        # =====================================================

        old_matches = [

            item

            for item
            in self.OLD_TERMS

            if item in combined
        ]

        if old_matches:

            score -= (
                len(old_matches) * 10
            )

            result.stale_content_detected = (
                True
            )

        # =====================================================
        # CURRENT YEAR
        # =====================================================

        current_year = str(
            datetime.utcnow().year
        )

        if current_year in combined:

            score += 15

            result.realtime_relevance = (
                True
            )

        result.freshness_score = min(

            max(score, 0),

            100,
        )

        # =====================================================
        # LEVELS
        # =====================================================

        if result.freshness_score >= 80:

            result.freshness_level = (
                "high"
            )

        elif result.freshness_score >= 60:

            result.freshness_level = (
                "medium"
            )

        else:

            result.freshness_level = (
                "low"
            )

        # =====================================================
        # RISKS
        # =====================================================

        if result.freshness_score < 50:

            result.freshness_decay_risk = (
                "high"
            )

        # =====================================================
        # RECOMMENDATIONS
        # =====================================================

        if result.stale_content_detected:

            result.recommendations.append(
                "Refresh outdated information"
            )

        if result.realtime_relevance:

            result.recommendations.append(
                "Maintain realtime monitoring"
            )

        result.add_reasoning(
            f"Freshness score: "
            f"{result.freshness_score}"
        )

        return self.export(
            result
        )

    # =========================================================
    # EXPORT
    # =========================================================

    def export(
        self,
        result: FreshnessResult,
    ) -> Dict[str, Any]:

        return {

            "freshness_score": (
                result.freshness_score
            ),

            "freshness_level": (
                result.freshness_level
            ),

            "realtime_relevance": (
                result.realtime_relevance
            ),

            "update_detected": (
                result.update_detected
            ),

            "stale_content_detected": (
                result.stale_content_detected
            ),

            "freshness_decay_risk": (
                result.freshness_decay_risk
            ),

            "detected_patterns": (
                result.detected_patterns
            ),

            "recommendations": (
                result.recommendations
            ),

            "reasoning": (
                result.reasoning
            ),

            "metadata": (
                result.metadata
            ),
        }