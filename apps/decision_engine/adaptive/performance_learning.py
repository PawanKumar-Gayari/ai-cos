"""
Performance Learning Engine

This module enables adaptive editorial learning.

Goal:
Learn from real-world article performance and
continuously optimize:
- scoring
- strategies
- adaptive weights
- decision confidence

Future Vision:
AI_COS should evolve based on:
- rankings
- CTR
- engagement
- freshness decay
- authority signals
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any


# =============================================================
# PERFORMANCE RECORD
# =============================================================

@dataclass
class PerformanceRecord:

    article_id: str

    niche: str

    keyword: str

    rankings: int = 0

    impressions: int = 0

    ctr: float = 0.0

    engagement_score: float = 0.0

    bounce_rate: float = 0.0

    freshness_score: float = 0.0

    authority_score: float = 0.0

    quality_score: float = 0.0

    seo_score: float = 0.0

    faq_enabled: bool = False

    tables_enabled: bool = False

    official_sources_used: bool = False

    verification_score: float = 0.0

    indexed: bool = False

    notes: List[str] = field(
        default_factory=list
    )


# =============================================================
# LEARNING RESULT
# =============================================================

@dataclass
class LearningResult:

    adjustments: Dict[str, float] = field(
        default_factory=dict
    )

    learned_patterns: List[str] = field(
        default_factory=list
    )

    confidence: float = 0.0

    notes: List[str] = field(
        default_factory=list
    )


# =============================================================
# PERFORMANCE LEARNING ENGINE
# =============================================================

class PerformanceLearningEngine:

    """
    Adaptive editorial learning system.

    Learns from:
    - rankings
    - CTR
    - engagement
    - freshness performance
    - verification success
    """

    # =========================================================
    # MAIN ENTRY
    # =========================================================

    def analyze(
        self,
        record: PerformanceRecord,
    ) -> LearningResult:

        result = LearningResult()

        self._analyze_ctr(
            record,
            result,
        )

        self._analyze_rankings(
            record,
            result,
        )

        self._analyze_engagement(
            record,
            result,
        )

        self._analyze_freshness(
            record,
            result,
        )

        self._analyze_verification(
            record,
            result,
        )

        self._calculate_confidence(
            result,
        )

        return result

    # =========================================================
    # CTR ANALYSIS
    # =========================================================

    def _analyze_ctr(
        self,
        record: PerformanceRecord,
        result: LearningResult,
    ) -> None:

        if record.ctr >= 8.0:

            result.learned_patterns.append(
                "High CTR article detected"
            )

            result.adjustments[
                "engagement_weight"
            ] = 0.2

            if record.faq_enabled:

                result.learned_patterns.append(
                    "FAQ sections improved CTR"
                )

                result.adjustments[
                    "faq_priority"
                ] = 0.3

        elif record.ctr <= 2.0:

            result.learned_patterns.append(
                "Low CTR detected"
            )

            result.adjustments[
                "headline_optimization"
            ] = 0.5

    # =========================================================
    # RANKING ANALYSIS
    # =========================================================

    def _analyze_rankings(
        self,
        record: PerformanceRecord,
        result: LearningResult,
    ) -> None:

        if record.rankings <= 5:

            result.learned_patterns.append(
                "Top ranking article"
            )

            result.adjustments[
                "seo_weight"
            ] = 0.2

            if record.tables_enabled:

                result.learned_patterns.append(
                    "Tables improved rankings"
                )

                result.adjustments[
                    "tables_priority"
                ] = 0.2

        elif record.rankings >= 50:

            result.learned_patterns.append(
                "Poor ranking performance"
            )

            result.adjustments[
                "semantic_depth"
            ] = 0.5

    # =========================================================
    # ENGAGEMENT ANALYSIS
    # =========================================================

    def _analyze_engagement(
        self,
        record: PerformanceRecord,
        result: LearningResult,
    ) -> None:

        if record.engagement_score >= 80:

            result.learned_patterns.append(
                "High engagement content"
            )

            result.adjustments[
                "quality_weight"
            ] = 0.3

        if record.bounce_rate >= 80:

            result.learned_patterns.append(
                "High bounce rate detected"
            )

            result.adjustments[
                "readability_improvement"
            ] = 0.5

    # =========================================================
    # FRESHNESS ANALYSIS
    # =========================================================

    def _analyze_freshness(
        self,
        record: PerformanceRecord,
        result: LearningResult,
    ) -> None:

        if record.freshness_score >= 85:

            result.learned_patterns.append(
                "Fresh content performed well"
            )

            result.adjustments[
                "freshness_weight"
            ] = 0.4

        elif record.freshness_score <= 40:

            result.learned_patterns.append(
                "Outdated content detected"
            )

            result.adjustments[
                "update_priority"
            ] = 0.7

    # =========================================================
    # VERIFICATION ANALYSIS
    # =========================================================

    def _analyze_verification(
        self,
        record: PerformanceRecord,
        result: LearningResult,
    ) -> None:

        if (
            record.official_sources_used
            and record.verification_score >= 85
        ):

            result.learned_patterns.append(
                "Official sources improved trust"
            )

            result.adjustments[
                "verification_weight"
            ] = 0.5

            result.adjustments[
                "trust_weight"
            ] = 0.4

    # =========================================================
    # CONFIDENCE
    # =========================================================

    def _calculate_confidence(
        self,
        result: LearningResult,
    ) -> None:

        pattern_count = len(
            result.learned_patterns
        )

        confidence = min(
            pattern_count * 0.15,
            1.0,
        )

        result.confidence = round(
            confidence,
            2,
        )

    # =========================================================
    # EXPORT
    # =========================================================

    def export(
        self,
        result: LearningResult,
    ) -> Dict[str, Any]:

        return {
            "adjustments": result.adjustments,
            "learned_patterns": result.learned_patterns,
            "confidence": result.confidence,
            "notes": result.notes,
        }