"""
Stale Content Detector

Purpose:
Detect stale and outdated content using:
- old year detection
- outdated terminology
- freshness decay
- realtime relevance gaps
- temporal aging analysis

Goal:
Identify content that may hurt:
- rankings
- trust
- authority
- SEO freshness

This becomes the stale content
intelligence layer of AI_COS.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List
from datetime import datetime
import re


# =============================================================
# STALE RESULT
# =============================================================

@dataclass
class StaleContentResult:

    # =========================================================
    # STATUS
    # =========================================================

    stale_content_detected: bool = False

    severe_staleness_detected: bool = False

    freshness_gap_detected: bool = False

    # =========================================================
    # SCORES
    # =========================================================

    staleness_score: float = 0.0

    freshness_score: float = 0.0

    decay_score: float = 0.0

    # =========================================================
    # DETECTIONS
    # =========================================================

    outdated_year_detected: bool = False

    deprecated_information_detected: bool = False

    missing_realtime_signals: bool = False

    historical_bias_detected: bool = False

    # =========================================================
    # YEARS
    # =========================================================

    detected_old_years: List[str] = field(
        default_factory=list
    )

    newest_year: str = ""

    oldest_year: str = ""

    # =========================================================
    # CLASSIFICATION
    # =========================================================

    staleness_level: str = "low"

    freshness_status: str = "stable"

    # =========================================================
    # RISKS
    # =========================================================

    ranking_decay_risk: str = "low"

    trust_decay_risk: str = "low"

    seo_freshness_risk: str = "low"

    misinformation_risk: str = "low"

    # =========================================================
    # SIGNALS
    # =========================================================

    stale_signals: Dict[str, Any] = field(
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
# STALE CONTENT DETECTOR
# =============================================================

class StaleContentDetector:

    """
    Stale content detection intelligence engine.
    """

    # =========================================================
    # YEAR PATTERN
    # =========================================================

    YEAR_PATTERN = re.compile(
        r"\b(20\d{2})\b"
    )

    # =========================================================
    # OUTDATED TERMS
    # =========================================================

    OUTDATED_TERMS = [

        "old syllabus",
        "previous pattern",
        "deprecated",
        "obsolete",
        "legacy",
        "expired",
    ]

    # =========================================================
    # REALTIME TERMS
    # =========================================================

    REALTIME_TERMS = [

        "latest",
        "today",
        "live",
        "updated",
        "2026",
        "new",
    ]

    # =========================================================
    # DETECT
    # =========================================================

    def detect(
        self,
        content: str,
        keyword: str = "",
    ) -> Dict[str, Any]:

        result = (
            StaleContentResult()
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

        self._detect_old_years(
            result,
            combined,
        )

        # =====================================================
        # OUTDATED TERMS
        # =====================================================

        self._detect_outdated_terms(
            result,
            combined,
        )

        # =====================================================
        # REALTIME GAPS
        # =====================================================

        self._detect_realtime_gaps(
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

    def _detect_old_years(
        self,
        result: StaleContentResult,
        content: str,
    ) -> None:

        matches = self.YEAR_PATTERN.findall(
            content
        )

        current_year = datetime.utcnow().year

        old_years = []

        for year_str in matches:

            year = int(year_str)

            if year <= current_year - 3:

                old_years.append(
                    year_str
                )

        if old_years:

            result.outdated_year_detected = (
                True
            )

            result.detected_old_years = (
                sorted(
                    list(set(old_years))
                )
            )

            result.oldest_year = min(
                result.detected_old_years
            )

            result.newest_year = max(
                result.detected_old_years
            )

            result.stale_content_detected = (
                True
            )

    # =========================================================
    # OUTDATED TERMS
    # =========================================================

    def _detect_outdated_terms(
        self,
        result: StaleContentResult,
        content: str,
    ) -> None:

        matches = [

            item

            for item
            in self.OUTDATED_TERMS

            if item in content
        ]

        if matches:

            result.deprecated_information_detected = (
                True
            )

            result.matched_patterns.extend(
                matches
            )

            result.stale_content_detected = (
                True
            )

    # =========================================================
    # REALTIME GAPS
    # =========================================================

    def _detect_realtime_gaps(
        self,
        result: StaleContentResult,
        content: str,
    ) -> None:

        realtime_found = any(

            item in content

            for item
            in self.REALTIME_TERMS
        )

        if not realtime_found:

            result.missing_realtime_signals = (
                True
            )

            result.freshness_gap_detected = (
                True
            )

    # =========================================================
    # SCORES
    # =========================================================

    def _calculate_scores(
        self,
        result: StaleContentResult,
    ) -> None:

        staleness = 20.0

        freshness = 80.0

        # =====================================================
        # OLD YEARS
        # =====================================================

        if result.outdated_year_detected:

            staleness += 35

            freshness -= 30

        # =====================================================
        # OUTDATED TERMS
        # =====================================================

        if result.deprecated_information_detected:

            staleness += 25

            freshness -= 20

        # =====================================================
        # REALTIME GAP
        # =====================================================

        if result.missing_realtime_signals:

            staleness += 15

            freshness -= 15

        result.staleness_score = min(

            max(staleness, 0),

            100,
        )

        result.freshness_score = min(

            max(freshness, 0),

            100,
        )

        result.decay_score = round(

            result.staleness_score * 0.9,

            2,
        )

        # =====================================================
        # LEVELS
        # =====================================================

        if result.staleness_score >= 75:

            result.staleness_level = (
                "high"
            )

            result.severe_staleness_detected = (
                True
            )

            result.freshness_status = (
                "outdated"
            )

        elif result.staleness_score >= 50:

            result.staleness_level = (
                "medium"
            )

            result.freshness_status = (
                "aging"
            )

        else:

            result.staleness_level = (
                "low"
            )

            result.freshness_status = (
                "stable"
            )

    # =========================================================
    # RISKS
    # =========================================================

    def _detect_risks(
        self,
        result: StaleContentResult,
    ) -> None:

        # =====================================================
        # RANKING
        # =====================================================

        if result.staleness_score >= 60:

            result.ranking_decay_risk = (
                "high"
            )

            result.add_warning(
                "Ranking freshness decay detected"
            )

        # =====================================================
        # TRUST
        # =====================================================

        if result.deprecated_information_detected:

            result.trust_decay_risk = (
                "medium"
            )

        # =====================================================
        # SEO
        # =====================================================

        if result.freshness_gap_detected:

            result.seo_freshness_risk = (
                "high"
            )

        # =====================================================
        # MISINFORMATION
        # =====================================================

        if result.severe_staleness_detected:

            result.misinformation_risk = (
                "medium"
            )

    # =========================================================
    # FINALIZE
    # =========================================================

    def _finalize(
        self,
        result: StaleContentResult,
    ) -> None:

        # =====================================================
        # RECOMMENDATIONS
        # =====================================================

        if result.outdated_year_detected:

            result.add_recommendation(
                "Replace outdated year references"
            )

            result.add_action(
                "Refresh temporal information"
            )

        if result.deprecated_information_detected:

            result.add_recommendation(
                "Update deprecated information"
            )

        if result.freshness_gap_detected:

            result.add_recommendation(
                "Add realtime freshness signals"
            )

        if result.severe_staleness_detected:

            result.add_recommendation(
                "Perform full content refresh"
            )

        result.add_action(
            "Store stale content intelligence"
        )

        result.add_reasoning(
            f"Staleness score: "
            f"{result.staleness_score}"
        )

    # =========================================================
    # EXPORT
    # =========================================================

    def export(
        self,
        result: StaleContentResult,
    ) -> Dict[str, Any]:

        return {

            "stale_content_detected": (
                result.stale_content_detected
            ),

            "severe_staleness_detected": (
                result.severe_staleness_detected
            ),

            "freshness_gap_detected": (
                result.freshness_gap_detected
            ),

            "staleness_score": (
                result.staleness_score
            ),

            "freshness_score": (
                result.freshness_score
            ),

            "decay_score": (
                result.decay_score
            ),

            "outdated_year_detected": (
                result.outdated_year_detected
            ),

            "deprecated_information_detected": (
                result.deprecated_information_detected
            ),

            "missing_realtime_signals": (
                result.missing_realtime_signals
            ),

            "historical_bias_detected": (
                result.historical_bias_detected
            ),

            "detected_old_years": (
                result.detected_old_years
            ),

            "newest_year": (
                result.newest_year
            ),

            "oldest_year": (
                result.oldest_year
            ),

            "staleness_level": (
                result.staleness_level
            ),

            "freshness_status": (
                result.freshness_status
            ),

            "ranking_decay_risk": (
                result.ranking_decay_risk
            ),

            "trust_decay_risk": (
                result.trust_decay_risk
            ),

            "seo_freshness_risk": (
                result.seo_freshness_risk
            ),

            "misinformation_risk": (
                result.misinformation_risk
            ),

            "stale_signals": (
                result.stale_signals
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