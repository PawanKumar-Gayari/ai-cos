"""
Freshness Agent

Purpose:
Analyze content freshness, update urgency,
realtime sensitivity, and content decay risk.

Analyzes:
- freshness validity
- outdated information
- realtime sensitivity
- content decay
- update urgency
- freshness lifespan

Goal:
Keep AI_COS content continuously fresh
and ranking-safe.

This becomes the freshness intelligence layer
of AI_COS.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Any, List


# =============================================================
# FRESHNESS RESULT
# =============================================================

@dataclass
class FreshnessResult:

    # =========================================================
    # SCORES
    # =========================================================

    freshness_score: float = 0.0

    freshness_confidence: float = 0.0

    update_urgency_score: float = 0.0

    decay_probability: float = 0.0

    # =========================================================
    # VALIDITY
    # =========================================================

    freshness_valid: bool = True

    freshness_expired: bool = False

    freshness_sensitive: bool = False

    realtime_sensitive: bool = False

    # =========================================================
    # CONTENT AGE
    # =========================================================

    detected_years: List[int] = field(
        default_factory=list
    )

    outdated_years: List[int] = field(
        default_factory=list
    )

    latest_detected_year: int = 0

    # =========================================================
    # RISKS
    # =========================================================

    freshness_risk: str = "low"

    ranking_decay_risk: str = "low"

    traffic_decay_risk: str = "low"

    outdated_information_risk: str = "low"

    # =========================================================
    # DETECTIONS
    # =========================================================

    outdated_content_detected: bool = False

    stale_statistics_detected: bool = False

    expired_information_detected: bool = False

    update_required: bool = False

    urgent_update_required: bool = False

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
    # KEYWORDS
    # =========================================================

    freshness_keywords_detected: List[str] = field(
        default_factory=list
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


# =============================================================
# FRESHNESS AGENT
# =============================================================

class FreshnessAgent:

    """
    Freshness intelligence agent.
    """

    # =========================================================
    # REALTIME KEYWORDS
    # =========================================================

    REALTIME_KEYWORDS = [

        "latest",
        "today",
        "new",
        "update",
        "notification",
        "result",
        "breaking",
        "live",
        "current",
        "2026",
    ]

    # =========================================================
    # FRESHNESS-SENSITIVE NICHES
    # =========================================================

    FRESHNESS_NICHES = [

        "jobs",
        "news",
        "technology",
        "government_jobs",
        "results",
        "admit_card",
        "crypto",
    ]

    # =========================================================
    # ANALYZE
    # =========================================================

    def analyze(
        self,
        article: str,
        topic: str = "",
        niche: str = "general",
    ) -> FreshnessResult:

        result = FreshnessResult()

        article = (
            article or ""
        ).lower()

        topic = (
            topic or ""
        ).lower()

        niche = (
            niche or ""
        ).lower()

        # =====================================================
        # KEYWORDS
        # =====================================================

        self._detect_freshness_keywords(
            result,
            article,
            topic,
        )

        # =====================================================
        # YEARS
        # =====================================================

        self._detect_years(
            result,
            article,
        )

        # =====================================================
        # NICHE
        # =====================================================

        self._analyze_niche(
            result,
            niche,
        )

        # =====================================================
        # DECAY
        # =====================================================

        self._calculate_decay(
            result
        )

        # =====================================================
        # SCORE
        # =====================================================

        self._calculate_score(
            result
        )

        # =====================================================
        # FINALIZE
        # =====================================================

        self._finalize(
            result
        )

        return result

    # =========================================================
    # KEYWORDS
    # =========================================================

    def _detect_freshness_keywords(
        self,
        result: FreshnessResult,
        article: str,
        topic: str,
    ) -> None:

        combined = (
            article + " " + topic
        )

        for keyword in self.REALTIME_KEYWORDS:

            if keyword in combined:

                result.freshness_keywords_detected.append(
                    keyword
                )

        # =====================================================
        # REALTIME
        # =====================================================

        if result.freshness_keywords_detected:

            result.freshness_sensitive = (
                True
            )

            result.realtime_sensitive = (
                True
            )

            result.add_reasoning(
                "Realtime-sensitive keywords detected"
            )

    # =========================================================
    # YEARS
    # =========================================================

    def _detect_years(
        self,
        result: FreshnessResult,
        article: str,
    ) -> None:

        current_year = (
            datetime.utcnow().year
        )

        # =====================================================
        # DETECT YEARS
        # =====================================================

        for year in range(2020, 2035):

            if str(year) in article:

                result.detected_years.append(
                    year
                )

        # =====================================================
        # LATEST
        # =====================================================

        if result.detected_years:

            result.latest_detected_year = max(
                result.detected_years
            )

        # =====================================================
        # OUTDATED
        # =====================================================

        for year in result.detected_years:

            if year < current_year:

                result.outdated_years.append(
                    year
                )

        # =====================================================
        # OUTDATED CONTENT
        # =====================================================

        if result.outdated_years:

            result.outdated_content_detected = (
                True
            )

            result.add_warning(
                "Outdated years detected in content"
            )

    # =========================================================
    # NICHE
    # =========================================================

    def _analyze_niche(
        self,
        result: FreshnessResult,
        niche: str,
    ) -> None:

        if niche in self.FRESHNESS_NICHES:

            result.freshness_sensitive = (
                True
            )

            result.realtime_sensitive = (
                True
            )

            result.add_reasoning(
                "Freshness-sensitive niche detected"
            )

    # =========================================================
    # DECAY
    # =========================================================

    def _calculate_decay(
        self,
        result: FreshnessResult,
    ) -> None:

        decay = 0

        # =====================================================
        # OUTDATED YEARS
        # =====================================================

        decay += (
            len(result.outdated_years) * 15
        )

        # =====================================================
        # REALTIME
        # =====================================================

        if result.realtime_sensitive:

            decay += 25

        result.decay_probability = round(

            min(decay, 100),

            2,
        )

        # =====================================================
        # RISK
        # =====================================================

        if result.decay_probability >= 80:

            result.freshness_risk = (
                "critical"
            )

        elif result.decay_probability >= 60:

            result.freshness_risk = (
                "high"
            )

        elif result.decay_probability >= 35:

            result.freshness_risk = (
                "medium"
            )

        else:

            result.freshness_risk = (
                "low"
            )

    # =========================================================
    # SCORE
    # =========================================================

    def _calculate_score(
        self,
        result: FreshnessResult,
    ) -> None:

        score = 100

        # =====================================================
        # PENALTIES
        # =====================================================

        score -= (
            len(result.outdated_years) * 15
        )

        if result.outdated_content_detected:

            score -= 20

        if result.realtime_sensitive:

            score -= 10

        # =====================================================
        # FINAL
        # =====================================================

        result.freshness_score = round(

            max(score, 0),

            2,
        )

        result.freshness_confidence = round(

            result.freshness_score,

            2,
        )

        result.update_urgency_score = round(

            result.decay_probability,

            2,
        )

        result.add_reasoning(
            f"Freshness score calculated: "
            f"{result.freshness_score}"
        )

    # =========================================================
    # FINALIZE
    # =========================================================

    def _finalize(
        self,
        result: FreshnessResult,
    ) -> None:

        # =====================================================
        # EXPIRED
        # =====================================================

        if result.freshness_score < 50:

            result.freshness_expired = (
                True
            )

            result.freshness_valid = (
                False
            )

            result.update_required = (
                True
            )

        # =====================================================
        # URGENT
        # =====================================================

        if result.freshness_risk in [
            "high",
            "critical",
        ]:

            result.urgent_update_required = (
                True
            )

            result.ranking_decay_risk = (
                "high"
            )

            result.traffic_decay_risk = (
                "high"
            )

            result.add_warning(
                "High freshness decay risk detected"
            )

        # =====================================================
        # RECOMMENDATIONS
        # =====================================================

        if result.outdated_content_detected:

            result.add_recommendation(
                "Update outdated content references"
            )

        if result.realtime_sensitive:

            result.add_recommendation(
                "Enable realtime freshness monitoring"
            )

        if result.freshness_score < 60:

            result.add_recommendation(
                "Refresh article with latest data"
            )

        result.add_reasoning(
            f"Final freshness score: "
            f"{result.freshness_score}"
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

            "freshness_confidence": (
                result.freshness_confidence
            ),

            "update_urgency_score": (
                result.update_urgency_score
            ),

            "decay_probability": (
                result.decay_probability
            ),

            "freshness_valid": (
                result.freshness_valid
            ),

            "freshness_expired": (
                result.freshness_expired
            ),

            "freshness_sensitive": (
                result.freshness_sensitive
            ),

            "realtime_sensitive": (
                result.realtime_sensitive
            ),

            "detected_years": (
                result.detected_years
            ),

            "outdated_years": (
                result.outdated_years
            ),

            "latest_detected_year": (
                result.latest_detected_year
            ),

            "freshness_risk": (
                result.freshness_risk
            ),

            "ranking_decay_risk": (
                result.ranking_decay_risk
            ),

            "traffic_decay_risk": (
                result.traffic_decay_risk
            ),

            "outdated_information_risk": (
                result.outdated_information_risk
            ),

            "outdated_content_detected": (
                result.outdated_content_detected
            ),

            "stale_statistics_detected": (
                result.stale_statistics_detected
            ),

            "expired_information_detected": (
                result.expired_information_detected
            ),

            "update_required": (
                result.update_required
            ),

            "urgent_update_required": (
                result.urgent_update_required
            ),

            "freshness_keywords_detected": (
                result.freshness_keywords_detected
            ),

            "reasoning": (
                result.reasoning
            ),

            "warnings": (
                result.warnings
            ),

            "recommendations": (
                result.recommendations
            ),

            "freshness_signals": (
                result.freshness_signals
            ),

            "metadata": (
                result.metadata
            ),
        }