"""
Recency Score

Purpose:
Calculate recency intelligence using:
- year detection
- freshness indicators
- realtime signals
- update relevance
- temporal scoring

Goal:
Measure how recent and time-relevant
content is for SEO freshness optimization.

This becomes the recency scoring
layer of AI_COS.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List
from datetime import datetime
import re


# =============================================================
# RECENCY RESULT
# =============================================================

@dataclass
class RecencyScoreResult:

    # =========================================================
    # SCORES
    # =========================================================

    recency_score: float = 0.0

    temporal_relevance_score: float = 0.0

    freshness_confidence: float = 0.0

    # =========================================================
    # DETECTIONS
    # =========================================================

    current_year_detected: bool = False

    future_year_detected: bool = False

    outdated_year_detected: bool = False

    realtime_signal_detected: bool = False

    # =========================================================
    # YEARS
    # =========================================================

    detected_years: List[str] = field(
        default_factory=list
    )

    newest_year: str = ""

    oldest_year: str = ""

    # =========================================================
    # CLASSIFICATION
    # =========================================================

    recency_level: str = "medium"

    freshness_status: str = "stable"

    # =========================================================
    # RISKS
    # =========================================================

    outdated_content_risk: str = "low"

    temporal_decay_risk: str = "low"

    stale_information_risk: str = "low"

    # =========================================================
    # SIGNALS
    # =========================================================

    recency_signals: Dict[str, Any] = field(
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
# RECENCY SCORE
# =============================================================

class RecencyScore:

    """
    Recency scoring intelligence engine.
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
        "new",
        "announcement",
    ]

    # =========================================================
    # YEAR PATTERN
    # =========================================================

    YEAR_PATTERN = re.compile(
        r"\b(20\d{2})\b"
    )

    # =========================================================
    # CALCULATE
    # =========================================================

    def calculate(
        self,
        content: str,
        keyword: str = "",
    ) -> Dict[str, Any]:

        result = (
            RecencyScoreResult()
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
        # YEARS
        # =====================================================

        self._detect_years(
            result,
            combined,
        )

        # =====================================================
        # REALTIME
        # =====================================================

        self._detect_realtime_signals(
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
    # YEARS
    # =========================================================

    def _detect_years(
        self,
        result: RecencyScoreResult,
        content: str,
    ) -> None:

        matches = self.YEAR_PATTERN.findall(
            content
        )

        current_year = datetime.utcnow().year

        if matches:

            unique_years = sorted(
                list(set(matches))
            )

            result.detected_years = (
                unique_years
            )

            result.newest_year = max(
                unique_years
            )

            result.oldest_year = min(
                unique_years
            )

            # =================================================
            # CHECK YEARS
            # =================================================

            for year_str in unique_years:

                year = int(year_str)

                if year == current_year:

                    result.current_year_detected = (
                        True
                    )

                elif year > current_year:

                    result.future_year_detected = (
                        True
                    )

                elif year <= current_year - 3:

                    result.outdated_year_detected = (
                        True
                    )

    # =========================================================
    # REALTIME
    # =========================================================

    def _detect_realtime_signals(
        self,
        result: RecencyScoreResult,
        content: str,
    ) -> None:

        matches = [

            item

            for item
            in self.REALTIME_TERMS

            if item in content
        ]

        if matches:

            result.realtime_signal_detected = (
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
        result: RecencyScoreResult,
    ) -> None:

        score = 50.0

        # =====================================================
        # CURRENT YEAR
        # =====================================================

        if result.current_year_detected:

            score += 25

        # =====================================================
        # FUTURE
        # =====================================================

        if result.future_year_detected:

            score += 10

        # =====================================================
        # REALTIME
        # =====================================================

        if result.realtime_signal_detected:

            score += 10

        # =====================================================
        # OUTDATED
        # =====================================================

        if result.outdated_year_detected:

            score -= 25

        result.recency_score = min(

            max(score, 0),

            100,
        )

        result.temporal_relevance_score = (
            result.recency_score
        )

        result.freshness_confidence = round(

            result.recency_score * 0.95,

            2,
        )

        # =====================================================
        # LEVEL
        # =====================================================

        if result.recency_score >= 80:

            result.recency_level = (
                "high"
            )

            result.freshness_status = (
                "fresh"
            )

        elif result.recency_score >= 60:

            result.recency_level = (
                "medium"
            )

            result.freshness_status = (
                "stable"
            )

        else:

            result.recency_level = (
                "low"
            )

            result.freshness_status = (
                "outdated"
            )

    # =========================================================
    # RISKS
    # =========================================================

    def _detect_risks(
        self,
        result: RecencyScoreResult,
    ) -> None:

        # =====================================================
        # OUTDATED
        # =====================================================

        if result.outdated_year_detected:

            result.outdated_content_risk = (
                "high"
            )

            result.add_warning(
                "Outdated year references detected"
            )

        # =====================================================
        # TEMPORAL DECAY
        # =====================================================

        if result.recency_score < 50:

            result.temporal_decay_risk = (
                "high"
            )

        # =====================================================
        # STALE
        # =====================================================

        if not result.realtime_signal_detected:

            result.stale_information_risk = (
                "medium"
            )

    # =========================================================
    # FINALIZE
    # =========================================================

    def _finalize(
        self,
        result: RecencyScoreResult,
    ) -> None:

        # =====================================================
        # RECOMMENDATIONS
        # =====================================================

        if result.outdated_content_risk == "high":

            result.add_recommendation(
                "Replace outdated year references"
            )

            result.add_action(
                "Refresh temporal information"
            )

        if result.realtime_signal_detected:

            result.add_recommendation(
                "Maintain realtime freshness monitoring"
            )

        if result.recency_level == "low":

            result.add_recommendation(
                "Update content with recent data"
            )

        result.add_action(
            "Store recency intelligence"
        )

        result.add_reasoning(
            f"Recency score: "
            f"{result.recency_score}"
        )

    # =========================================================
    # EXPORT
    # =========================================================

    def export(
        self,
        result: RecencyScoreResult,
    ) -> Dict[str, Any]:

        return {

            "recency_score": (
                result.recency_score
            ),

            "temporal_relevance_score": (
                result.temporal_relevance_score
            ),

            "freshness_confidence": (
                result.freshness_confidence
            ),

            "current_year_detected": (
                result.current_year_detected
            ),

            "future_year_detected": (
                result.future_year_detected
            ),

            "outdated_year_detected": (
                result.outdated_year_detected
            ),

            "realtime_signal_detected": (
                result.realtime_signal_detected
            ),

            "detected_years": (
                result.detected_years
            ),

            "newest_year": (
                result.newest_year
            ),

            "oldest_year": (
                result.oldest_year
            ),

            "recency_level": (
                result.recency_level
            ),

            "freshness_status": (
                result.freshness_status
            ),

            "outdated_content_risk": (
                result.outdated_content_risk
            ),

            "temporal_decay_risk": (
                result.temporal_decay_risk
            ),

            "stale_information_risk": (
                result.stale_information_risk
            ),

            "recency_signals": (
                result.recency_signals
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