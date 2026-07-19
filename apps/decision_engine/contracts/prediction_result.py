"""
Prediction Result Contract

Prediction intelligence output used by:
- ranking forecasting
- traffic estimation
- decay prediction
- strategy optimization
- publish confidence

Goal:
Provide predictive intelligence BEFORE publishing.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional


# =============================================================
# PREDICTION RESULT
# =============================================================

@dataclass
class PredictionResult:

    # =========================================================
    # RANKING PREDICTIONS
    # =========================================================

    ranking_probability: float = 0.0

    estimated_position: Optional[int] = None

    ranking_difficulty: float = 0.0

    # =========================================================
    # TRAFFIC PREDICTIONS
    # =========================================================

    estimated_traffic: int = 0

    estimated_ctr: float = 0.0

    estimated_impressions: int = 0

    # =========================================================
    # COMPETITION
    # =========================================================

    competition_level: str = "medium"

    authority_gap: float = 0.0

    semantic_gap: float = 0.0

    backlink_difficulty: float = 0.0

    # =========================================================
    # CONTENT SUCCESS SIGNALS
    # =========================================================

    freshness_advantage: bool = False

    authority_advantage: bool = False

    semantic_advantage: bool = False

    snippet_opportunity: bool = False

    faq_opportunity: bool = False

    # =========================================================
    # CONTENT DECAY
    # =========================================================

    decay_risk: str = "low"

    predicted_decay_days: Optional[int] = None

    update_recommended: bool = False

    # =========================================================
    # CONFIDENCE
    # =========================================================

    confidence_score: float = 0.0

    prediction_quality: str = "medium"

    # =========================================================
    # RECOMMENDATIONS
    # =========================================================

    recommendations: List[str] = field(
        default_factory=list
    )

    warnings: List[str] = field(
        default_factory=list
    )

    opportunities: List[str] = field(
        default_factory=list
    )

    # =========================================================
    # SIGNALS
    # =========================================================

    prediction_signals: Dict[str, Any] = field(
        default_factory=dict
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

    def add_warning(
        self,
        warning: str,
    ) -> None:

        if (
            warning
            and warning
            not in self.warnings
        ):

            self.warnings.append(
                warning
            )

    def add_opportunity(
        self,
        opportunity: str,
    ) -> None:

        if (
            opportunity
            and opportunity
            not in self.opportunities
        ):

            self.opportunities.append(
                opportunity
            )

    def add_signal(
        self,
        key: str,
        value: Any,
    ) -> None:

        self.prediction_signals[key] = value

    # =========================================================
    # PREDICTION QUALITY
    # =========================================================

    def evaluate_prediction_quality(
        self,
    ) -> None:

        if self.confidence_score >= 0.85:

            self.prediction_quality = (
                "very_high"
            )

        elif self.confidence_score >= 0.70:

            self.prediction_quality = (
                "high"
            )

        elif self.confidence_score >= 0.50:

            self.prediction_quality = (
                "medium"
            )

        else:

            self.prediction_quality = (
                "low"
            )

    # =========================================================
    # FINALIZE
    # =========================================================

    def finalize(
        self,
    ) -> None:

        self.evaluate_prediction_quality()

        # =====================================================
        # DECAY LOGIC
        # =====================================================

        if (
            self.decay_risk == "high"
            and self.predicted_decay_days
            and self.predicted_decay_days <= 7
        ):

            self.update_recommended = True

            self.add_warning(
                "Rapid content decay predicted"
            )

        # =====================================================
        # OPPORTUNITY DETECTION
        # =====================================================

        if self.snippet_opportunity:

            self.add_opportunity(
                "Featured snippet opportunity detected"
            )

        if self.faq_opportunity:

            self.add_opportunity(
                "FAQ optimization opportunity detected"
            )

        if self.semantic_advantage:

            self.add_opportunity(
                "Strong semantic coverage advantage"
            )

    # =========================================================
    # EXPORT
    # =========================================================

    def to_dict(
        self,
    ) -> Dict[str, Any]:

        return {

            # =================================================
            # RANKING
            # =================================================

            "ranking_probability": (
                self.ranking_probability
            ),

            "estimated_position": (
                self.estimated_position
            ),

            "ranking_difficulty": (
                self.ranking_difficulty
            ),

            # =================================================
            # TRAFFIC
            # =================================================

            "estimated_traffic": (
                self.estimated_traffic
            ),

            "estimated_ctr": (
                self.estimated_ctr
            ),

            "estimated_impressions": (
                self.estimated_impressions
            ),

            # =================================================
            # COMPETITION
            # =================================================

            "competition_level": (
                self.competition_level
            ),

            "authority_gap": (
                self.authority_gap
            ),

            "semantic_gap": (
                self.semantic_gap
            ),

            "backlink_difficulty": (
                self.backlink_difficulty
            ),

            # =================================================
            # ADVANTAGES
            # =================================================

            "freshness_advantage": (
                self.freshness_advantage
            ),

            "authority_advantage": (
                self.authority_advantage
            ),

            "semantic_advantage": (
                self.semantic_advantage
            ),

            "snippet_opportunity": (
                self.snippet_opportunity
            ),

            "faq_opportunity": (
                self.faq_opportunity
            ),

            # =================================================
            # DECAY
            # =================================================

            "decay_risk": (
                self.decay_risk
            ),

            "predicted_decay_days": (
                self.predicted_decay_days
            ),

            "update_recommended": (
                self.update_recommended
            ),

            # =================================================
            # CONFIDENCE
            # =================================================

            "confidence_score": (
                self.confidence_score
            ),

            "prediction_quality": (
                self.prediction_quality
            ),

            # =================================================
            # OUTPUTS
            # =================================================

            "recommendations": (
                self.recommendations
            ),

            "warnings": (
                self.warnings
            ),

            "opportunities": (
                self.opportunities
            ),

            # =================================================
            # SIGNALS
            # =================================================

            "prediction_signals": (
                self.prediction_signals
            ),

            # =================================================
            # META
            # =================================================

            "metadata": self.metadata,
        }