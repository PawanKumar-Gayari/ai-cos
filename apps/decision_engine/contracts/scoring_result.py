"""
Scoring Result Contract

Unified scoring output used across:
- decision engine
- adaptive engine
- verification engine
- prediction engine
- reasoning engine

Goal:
Centralize ALL scoring intelligence into one object.

This prevents:
- scattered score logic
- inconsistent thresholds
- duplicated calculations
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List


# =============================================================
# SCORING RESULT
# =============================================================

@dataclass
class ScoringResult:

    # =========================================================
    # CORE SCORES
    # =========================================================

    seo_score: float = 0.0

    quality_score: float = 0.0

    freshness_score: float = 0.0

    authority_score: float = 0.0

    trust_score: float = 0.0

    verification_score: float = 0.0

    engagement_score: float = 0.0

    competition_score: float = 0.0

    confidence_score: float = 0.0

    # =========================================================
    # WEIGHTED OUTPUTS
    # =========================================================

    weighted_seo_score: float = 0.0

    weighted_quality_score: float = 0.0

    weighted_freshness_score: float = 0.0

    weighted_authority_score: float = 0.0

    weighted_trust_score: float = 0.0

    weighted_verification_score: float = 0.0

    weighted_engagement_score: float = 0.0

    weighted_competition_score: float = 0.0

    # =========================================================
    # FINAL SCORES
    # =========================================================

    overall_score: float = 0.0

    publish_score: float = 0.0

    ranking_score: float = 0.0

    # =========================================================
    # THRESHOLDS
    # =========================================================

    minimum_publish_score: float = 70.0

    minimum_verification_score: float = 70.0

    minimum_quality_score: float = 65.0

    # =========================================================
    # STATUS FLAGS
    # =========================================================

    publish_ready: bool = False

    rewrite_required: bool = False

    verification_required: bool = False

    human_review_required: bool = False

    # =========================================================
    # WEIGHTS
    # =========================================================

    applied_weights: Dict[str, float] = field(
        default_factory=dict
    )

    # =========================================================
    # SCORE BREAKDOWN
    # =========================================================

    score_breakdown: Dict[str, Any] = field(
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
    # METADATA
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

    def set_weight(
        self,
        score_name: str,
        weight: float,
    ) -> None:

        self.applied_weights[
            score_name
        ] = weight

    def set_breakdown(
        self,
        key: str,
        value: Any,
    ) -> None:

        self.score_breakdown[key] = value

    # =========================================================
    # CALCULATE WEIGHTED SCORES
    # =========================================================

    def calculate_weighted_scores(
        self,
    ) -> None:

        self.weighted_seo_score = (
            self.seo_score
            * self.applied_weights.get(
                "seo_weight",
                1.0,
            )
        )

        self.weighted_quality_score = (
            self.quality_score
            * self.applied_weights.get(
                "quality_weight",
                1.0,
            )
        )

        self.weighted_freshness_score = (
            self.freshness_score
            * self.applied_weights.get(
                "freshness_weight",
                1.0,
            )
        )

        self.weighted_authority_score = (
            self.authority_score
            * self.applied_weights.get(
                "authority_weight",
                1.0,
            )
        )

        self.weighted_trust_score = (
            self.trust_score
            * self.applied_weights.get(
                "trust_weight",
                1.0,
            )
        )

        self.weighted_verification_score = (
            self.verification_score
            * self.applied_weights.get(
                "verification_weight",
                1.0,
            )
        )

        self.weighted_engagement_score = (
            self.engagement_score
            * self.applied_weights.get(
                "engagement_weight",
                1.0,
            )
        )

        self.weighted_competition_score = (
            self.competition_score
            * self.applied_weights.get(
                "competition_weight",
                1.0,
            )
        )

    # =========================================================
    # FINAL SCORE CALCULATION
    # =========================================================

    def calculate_final_scores(
        self,
    ) -> None:

        self.calculate_weighted_scores()

        total = (

            self.weighted_seo_score +

            self.weighted_quality_score +

            self.weighted_freshness_score +

            self.weighted_authority_score +

            self.weighted_trust_score +

            self.weighted_verification_score +

            self.weighted_engagement_score +

            self.weighted_competition_score
        )

        divisor = 8

        self.overall_score = round(
            total / divisor,
            2,
        )

        self.publish_score = (
            self.overall_score
        )

        self.ranking_score = round(

            (
                self.seo_score +

                self.quality_score +

                self.authority_score +

                self.engagement_score
            ) / 4,

            2,
        )

    # =========================================================
    # EVALUATION
    # =========================================================

    def evaluate(
        self,
    ) -> None:

        self.calculate_final_scores()

        # =====================================================
        # PUBLISH READINESS
        # =====================================================

        if (

            self.publish_score
            >= self.minimum_publish_score

            and

            self.verification_score
            >= self.minimum_verification_score

            and

            self.quality_score
            >= self.minimum_quality_score
        ):

            self.publish_ready = True

            self.add_reasoning(
                "Publishing thresholds satisfied"
            )

        else:

            self.publish_ready = False

            self.rewrite_required = True

            self.add_warning(
                "Publishing thresholds not satisfied"
            )

        # =====================================================
        # VERIFICATION CHECK
        # =====================================================

        if (
            self.verification_score < 60
        ):

            self.verification_required = True

            self.add_warning(
                "Low verification confidence"
            )

        # =====================================================
        # HUMAN REVIEW
        # =====================================================

        if (
            self.confidence_score < 0.40
        ):

            self.human_review_required = True

            self.add_warning(
                "Low confidence requires human review"
            )

    # =========================================================
    # EXPORT
    # =========================================================

    def to_dict(
        self,
    ) -> Dict[str, Any]:

        return {

            # =================================================
            # RAW SCORES
            # =================================================

            "seo_score": self.seo_score,

            "quality_score": (
                self.quality_score
            ),

            "freshness_score": (
                self.freshness_score
            ),

            "authority_score": (
                self.authority_score
            ),

            "trust_score": (
                self.trust_score
            ),

            "verification_score": (
                self.verification_score
            ),

            "engagement_score": (
                self.engagement_score
            ),

            "competition_score": (
                self.competition_score
            ),

            "confidence_score": (
                self.confidence_score
            ),

            # =================================================
            # WEIGHTED
            # =================================================

            "weighted_seo_score": (
                self.weighted_seo_score
            ),

            "weighted_quality_score": (
                self.weighted_quality_score
            ),

            "weighted_freshness_score": (
                self.weighted_freshness_score
            ),

            "weighted_authority_score": (
                self.weighted_authority_score
            ),

            "weighted_trust_score": (
                self.weighted_trust_score
            ),

            "weighted_verification_score": (
                self.weighted_verification_score
            ),

            "weighted_engagement_score": (
                self.weighted_engagement_score
            ),

            "weighted_competition_score": (
                self.weighted_competition_score
            ),

            # =================================================
            # FINAL
            # =================================================

            "overall_score": (
                self.overall_score
            ),

            "publish_score": (
                self.publish_score
            ),

            "ranking_score": (
                self.ranking_score
            ),

            # =================================================
            # STATUS
            # =================================================

            "publish_ready": (
                self.publish_ready
            ),

            "rewrite_required": (
                self.rewrite_required
            ),

            "verification_required": (
                self.verification_required
            ),

            "human_review_required": (
                self.human_review_required
            ),

            # =================================================
            # WEIGHTS
            # =================================================

            "applied_weights": (
                self.applied_weights
            ),

            # =================================================
            # BREAKDOWN
            # =================================================

            "score_breakdown": (
                self.score_breakdown
            ),

            # =================================================
            # REASONING
            # =================================================

            "reasoning": self.reasoning,

            "warnings": self.warnings,

            "recommendations": (
                self.recommendations
            ),

            # =================================================
            # META
            # =================================================

            "metadata": self.metadata,
        }