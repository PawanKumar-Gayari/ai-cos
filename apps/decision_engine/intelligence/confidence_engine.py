"""
Confidence Engine

Purpose:
Generate final system confidence using:
- scoring intelligence
- verification intelligence
- prediction intelligence
- authority intelligence
- freshness intelligence
- risk intelligence

This becomes the FINAL orchestration brain
before publish/review/rewrite decisions.

Goal:
Produce:
- publish confidence
- risk level
- decision confidence
- system trust confidence
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List


# =============================================================
# CONFIDENCE RESULT
# =============================================================

@dataclass
class ConfidenceResult:

    # =========================================================
    # CORE CONFIDENCE
    # =========================================================

    confidence_score: float = 0.0

    confidence_level: str = "medium"

    publish_confidence: float = 0.0

    # =========================================================
    # DECISION
    # =========================================================

    decision: str = "review"

    publishing_allowed: bool = False

    human_review_required: bool = False

    rewrite_required: bool = False

    # =========================================================
    # RISK
    # =========================================================

    risk_level: str = "medium"

    hallucination_risk: str = "low"

    freshness_risk: str = "low"

    authority_risk: str = "low"

    # =========================================================
    # COMPONENT SCORES
    # =========================================================

    seo_score: float = 0.0

    quality_score: float = 0.0

    verification_score: float = 0.0

    trust_score: float = 0.0

    freshness_score: float = 0.0

    authority_score: float = 0.0

    prediction_score: float = 0.0

    # =========================================================
    # SIGNALS
    # =========================================================

    confidence_signals: Dict[str, Any] = field(
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

    def add_signal(
        self,
        key: str,
        value: Any,
    ) -> None:

        self.confidence_signals[key] = value


# =============================================================
# CONFIDENCE ENGINE
# =============================================================

class ConfidenceEngine:

    """
    Final orchestration intelligence layer.
    """

    # =========================================================
    # MAIN
    # =========================================================

    def evaluate(
        self,
        scoring_result=None,
        verification_result=None,
        prediction_result=None,
        authority_result=None,
        risk_result=None,
    ) -> ConfidenceResult:

        result = ConfidenceResult()

        # =====================================================
        # EXTRACT SCORES
        # =====================================================

        result.seo_score = getattr(
            scoring_result,
            "seo_score",
            0.0,
        )

        result.quality_score = getattr(
            scoring_result,
            "quality_score",
            0.0,
        )

        result.verification_score = getattr(
            verification_result,
            "verification_score",
            0.0,
        )

        result.trust_score = getattr(
            verification_result,
            "trust_score",
            0.0,
        )

        result.freshness_score = getattr(
            verification_result,
            "freshness_score",
            0.0,
        )

        result.authority_score = getattr(
            authority_result,
            "authority_score",
            0.0,
        )

        result.prediction_score = getattr(
            prediction_result,
            "ranking_probability",
            0.0,
        ) * 100

        # =====================================================
        # RISKS
        # =====================================================

        result.hallucination_risk = getattr(
            verification_result,
            "hallucination_risk",
            "low",
        )

        # =====================================================
        # CONFIDENCE CALCULATION
        # =====================================================

        result.confidence_score = round(

            (
                result.seo_score +

                result.quality_score +

                result.verification_score +

                result.trust_score +

                result.freshness_score +

                result.authority_score +

                result.prediction_score
            ) / 7,

            2,
        )

        result.publish_confidence = (
            result.confidence_score
        )

        # =====================================================
        # CONFIDENCE LEVEL
        # =====================================================

        self._evaluate_confidence_level(
            result
        )

        # =====================================================
        # RISK ANALYSIS
        # =====================================================

        self._evaluate_risk(
            result,
            risk_result,
        )

        # =====================================================
        # DECISION
        # =====================================================

        self._make_decision(
            result
        )

        return result

    # =========================================================
    # CONFIDENCE LEVEL
    # =========================================================

    def _evaluate_confidence_level(
        self,
        result: ConfidenceResult,
    ) -> None:

        if result.confidence_score >= 85:

            result.confidence_level = (
                "very_high"
            )

            result.add_reasoning(
                "Extremely high confidence detected"
            )

        elif result.confidence_score >= 70:

            result.confidence_level = (
                "high"
            )

            result.add_reasoning(
                "High confidence detected"
            )

        elif result.confidence_score >= 50:

            result.confidence_level = (
                "medium"
            )

        else:

            result.confidence_level = (
                "low"
            )

            result.add_warning(
                "Low confidence detected"
            )

    # =========================================================
    # RISK
    # =========================================================

    def _evaluate_risk(
        self,
        result: ConfidenceResult,
        risk_result=None,
    ) -> None:

        # =====================================================
        # HALLUCINATION
        # =====================================================

        if (
            result.hallucination_risk == "high"
        ):

            result.risk_level = "high"

            result.human_review_required = True

            result.publishing_allowed = False

            result.add_warning(
                "High hallucination risk"
            )

        # =====================================================
        # LOW VERIFICATION
        # =====================================================

        if result.verification_score < 60:

            result.risk_level = "high"

            result.add_warning(
                "Verification score too low"
            )

        # =====================================================
        # LOW AUTHORITY
        # =====================================================

        if result.authority_score < 40:

            result.authority_risk = "high"

            result.add_warning(
                "Low authority competitiveness"
            )

        # =====================================================
        # FRESHNESS
        # =====================================================

        if result.freshness_score < 50:

            result.freshness_risk = "high"

            result.add_warning(
                "Freshness risk detected"
            )

    # =========================================================
    # FINAL DECISION
    # =========================================================

    def _make_decision(
        self,
        result: ConfidenceResult,
    ) -> None:

        # =====================================================
        # REJECT
        # =====================================================

        if (

            result.hallucination_risk == "high"

            or

            result.verification_score < 40
        ):

            result.decision = "reject"

            result.publishing_allowed = False

            result.human_review_required = True

            result.add_warning(
                "Critical trust failure detected"
            )

            return

        # =====================================================
        # PUBLISH
        # =====================================================

        if (

            result.confidence_score >= 75

            and

            result.verification_score >= 70

            and

            result.quality_score >= 70
        ):

            result.decision = "publish"

            result.publishing_allowed = True

            result.add_reasoning(
                "Publishing thresholds satisfied"
            )

            return

        # =====================================================
        # REVIEW
        # =====================================================

        if (

            result.confidence_score >= 55

            or

            result.verification_score >= 60
        ):

            result.decision = "review"

            result.human_review_required = True

            result.add_warning(
                "Human review recommended"
            )

            return

        # =====================================================
        # REWRITE
        # =====================================================

        result.decision = "rewrite"

        result.rewrite_required = True

        result.publishing_allowed = False

        result.add_warning(
            "Rewrite required before publishing"
        )

    # =========================================================
    # EXPORT
    # =========================================================

    def export(
        self,
        result: ConfidenceResult,
    ) -> Dict[str, Any]:

        return {

            # =================================================
            # CONFIDENCE
            # =================================================

            "confidence_score": (
                result.confidence_score
            ),

            "confidence_level": (
                result.confidence_level
            ),

            "publish_confidence": (
                result.publish_confidence
            ),

            # =================================================
            # DECISION
            # =================================================

            "decision": result.decision,

            "publishing_allowed": (
                result.publishing_allowed
            ),

            "human_review_required": (
                result.human_review_required
            ),

            "rewrite_required": (
                result.rewrite_required
            ),

            # =================================================
            # RISK
            # =================================================

            "risk_level": (
                result.risk_level
            ),

            "hallucination_risk": (
                result.hallucination_risk
            ),

            "freshness_risk": (
                result.freshness_risk
            ),

            "authority_risk": (
                result.authority_risk
            ),

            # =================================================
            # SCORES
            # =================================================

            "seo_score": (
                result.seo_score
            ),

            "quality_score": (
                result.quality_score
            ),

            "verification_score": (
                result.verification_score
            ),

            "trust_score": (
                result.trust_score
            ),

            "freshness_score": (
                result.freshness_score
            ),

            "authority_score": (
                result.authority_score
            ),

            "prediction_score": (
                result.prediction_score
            ),

            # =================================================
            # SIGNALS
            # =================================================

            "confidence_signals": (
                result.confidence_signals
            ),

            # =================================================
            # REASONING
            # =================================================

            "reasoning": (
                result.reasoning
            ),

            "warnings": (
                result.warnings
            ),

            "recommendations": (
                result.recommendations
            ),

            # =================================================
            # META
            # =================================================

            "metadata": (
                result.metadata
            ),
        }