"""
Traffic Estimator

Purpose:
Estimate traffic potential BEFORE publishing.

This engine predicts:
- expected traffic
- CTR potential
- impression potential
- traffic decay risk
- click opportunity

Goal:
Estimate the real business impact of content.

This becomes the traffic intelligence layer
of the editorial system.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List


# =============================================================
# RESULT
# =============================================================

@dataclass
class TrafficEstimationResult:

    # =========================================================
    # TRAFFIC
    # =========================================================

    estimated_monthly_traffic: int = 0

    estimated_daily_traffic: int = 0

    estimated_impressions: int = 0

    estimated_clicks: int = 0

    # =========================================================
    # CTR
    # =========================================================

    estimated_ctr: float = 0.0

    ctr_potential: str = "medium"

    # =========================================================
    # VISIBILITY
    # =========================================================

    visibility_score: float = 0.0

    click_opportunity_score: float = 0.0

    # =========================================================
    # TRAFFIC QUALITY
    # =========================================================

    traffic_quality: str = "medium"

    conversion_potential: str = "medium"

    engagement_probability: float = 0.0

    # =========================================================
    # DECAY
    # =========================================================

    traffic_decay_risk: str = "low"

    traffic_stability: str = "medium"

    predicted_decay_percentage: float = 0.0

    # =========================================================
    # RANKING DEPENDENCY
    # =========================================================

    predicted_position: int = 50

    top_10_probability: float = 0.0

    top_3_probability: float = 0.0

    # =========================================================
    # SERP FEATURES
    # =========================================================

    featured_snippet_boost: bool = False

    faq_boost: bool = False

    video_boost: bool = False

    # =========================================================
    # ADVANTAGES
    # =========================================================

    freshness_advantage: bool = False

    long_tail_advantage: bool = False

    weak_serp_advantage: bool = False

    # =========================================================
    # DECISION
    # =========================================================

    high_traffic_potential: bool = False

    worth_targeting: bool = True

    # =========================================================
    # SIGNALS
    # =========================================================

    traffic_signals: Dict[str, Any] = field(
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


# =============================================================
# TRAFFIC ESTIMATOR
# =============================================================

class TrafficEstimator:

    """
    Traffic intelligence engine.
    """

    # =========================================================
    # MAIN
    # =========================================================

    def estimate(
        self,
        search_volume: int = 0,
        ranking_result=None,
        opportunity_result=None,
    ) -> TrafficEstimationResult:

        result = TrafficEstimationResult()

        # =====================================================
        # IMPORT PREDICTIONS
        # =====================================================

        self._import_ranking_data(
            result,
            ranking_result,
        )

        # =====================================================
        # IMPORT OPPORTUNITY
        # =====================================================

        self._import_opportunity_data(
            result,
            opportunity_result,
        )

        # =====================================================
        # CTR
        # =====================================================

        self._calculate_ctr(
            result
        )

        # =====================================================
        # TRAFFIC
        # =====================================================

        self._calculate_traffic(
            result,
            search_volume,
        )

        # =====================================================
        # QUALITY
        # =====================================================

        self._evaluate_traffic_quality(
            result
        )

        # =====================================================
        # STABILITY
        # =====================================================

        self._evaluate_stability(
            result
        )

        # =====================================================
        # FINAL DECISION
        # =====================================================

        self._evaluate_traffic_potential(
            result
        )

        return result

    # =========================================================
    # IMPORT RANKING
    # =========================================================

    def _import_ranking_data(
        self,
        result: TrafficEstimationResult,
        ranking_result=None,
    ) -> None:

        if not ranking_result:
            return

        result.predicted_position = getattr(
            ranking_result,
            "predicted_position",
            50,
        )

        result.top_10_probability = getattr(
            ranking_result,
            "top_10_probability",
            0.0,
        )

        result.top_3_probability = getattr(
            ranking_result,
            "top_3_probability",
            0.0,
        )

        # =====================================================
        # FEATURES
        # =====================================================

        snippet_probability = getattr(
            ranking_result,
            "featured_snippet_probability",
            0.0,
        )

        if snippet_probability >= 70:

            result.featured_snippet_boost = True

        faq_probability = getattr(
            ranking_result,
            "faq_visibility_probability",
            0.0,
        )

        if faq_probability >= 70:

            result.faq_boost = True

        video_probability = getattr(
            ranking_result,
            "video_visibility_probability",
            0.0,
        )

        if video_probability >= 70:

            result.video_boost = True

    # =========================================================
    # IMPORT OPPORTUNITY
    # =========================================================

    def _import_opportunity_data(
        self,
        result: TrafficEstimationResult,
        opportunity_result=None,
    ) -> None:

        if not opportunity_result:
            return

        result.freshness_advantage = getattr(
            opportunity_result,
            "freshness_advantage",
            False,
        )

        result.long_tail_advantage = getattr(
            opportunity_result,
            "long_tail_advantage",
            False,
        )

        result.weak_serp_advantage = getattr(
            opportunity_result,
            "weak_serp_detected",
            False,
        )

    # =========================================================
    # CTR
    # =========================================================

    def _calculate_ctr(
        self,
        result: TrafficEstimationResult,
    ) -> None:

        position = result.predicted_position

        # =====================================================
        # BASE CTR
        # =====================================================

        if position <= 1:

            ctr = 0.32

        elif position <= 3:

            ctr = 0.22

        elif position <= 5:

            ctr = 0.14

        elif position <= 10:

            ctr = 0.08

        elif position <= 20:

            ctr = 0.03

        else:

            ctr = 0.01

        # =====================================================
        # BOOSTS
        # =====================================================

        if result.featured_snippet_boost:
            ctr += 0.08

        if result.faq_boost:
            ctr += 0.03

        if result.video_boost:
            ctr += 0.02

        if result.long_tail_advantage:
            ctr += 0.03

        result.estimated_ctr = round(
            min(ctr, 1.0),
            2,
        )

        # =====================================================
        # CTR POTENTIAL
        # =====================================================

        if result.estimated_ctr >= 0.25:

            result.ctr_potential = "very_high"

        elif result.estimated_ctr >= 0.15:

            result.ctr_potential = "high"

        elif result.estimated_ctr >= 0.07:

            result.ctr_potential = "medium"

        else:

            result.ctr_potential = "low"

    # =========================================================
    # TRAFFIC
    # =========================================================

    def _calculate_traffic(
        self,
        result: TrafficEstimationResult,
        search_volume: int,
    ) -> None:

        result.estimated_impressions = (
            search_volume
        )

        estimated_clicks = int(

            search_volume *

            result.estimated_ctr
        )

        result.estimated_clicks = (
            estimated_clicks
        )

        result.estimated_monthly_traffic = (
            estimated_clicks
        )

        result.estimated_daily_traffic = int(
            estimated_clicks / 30
        )

        # =====================================================
        # VISIBILITY
        # =====================================================

        result.visibility_score = round(

            (
                result.top_10_probability +

                result.top_3_probability
            ) / 2,

            2,
        )

        result.click_opportunity_score = round(

            result.estimated_ctr * 100,

            2,
        )

    # =========================================================
    # QUALITY
    # =========================================================

    def _evaluate_traffic_quality(
        self,
        result: TrafficEstimationResult,
    ) -> None:

        # =====================================================
        # ENGAGEMENT
        # =====================================================

        engagement = 50

        if result.long_tail_advantage:
            engagement += 20

        if result.freshness_advantage:
            engagement += 10

        if result.featured_snippet_boost:
            engagement += 10

        result.engagement_probability = round(
            min(engagement, 100),
            2,
        )

        # =====================================================
        # TRAFFIC QUALITY
        # =====================================================

        if result.engagement_probability >= 80:

            result.traffic_quality = "very_high"

            result.conversion_potential = "high"

        elif result.engagement_probability >= 65:

            result.traffic_quality = "high"

            result.conversion_potential = "medium"

        elif result.engagement_probability >= 45:

            result.traffic_quality = "medium"

        else:

            result.traffic_quality = "low"

    # =========================================================
    # STABILITY
    # =========================================================

    def _evaluate_stability(
        self,
        result: TrafficEstimationResult,
    ) -> None:

        decay = 20

        if result.freshness_advantage:
            decay -= 10

        if result.predicted_position > 10:
            decay += 25

        if result.predicted_position > 20:
            decay += 25

        result.predicted_decay_percentage = round(
            min(max(decay, 0), 100),
            2,
        )

        # =====================================================
        # RISK
        # =====================================================

        if result.predicted_decay_percentage >= 70:

            result.traffic_decay_risk = "high"

            result.traffic_stability = "low"

        elif result.predicted_decay_percentage >= 40:

            result.traffic_decay_risk = "medium"

            result.traffic_stability = "medium"

        else:

            result.traffic_decay_risk = "low"

            result.traffic_stability = "high"

    # =========================================================
    # FINAL
    # =========================================================

    def _evaluate_traffic_potential(
        self,
        result: TrafficEstimationResult,
    ) -> None:

        # =====================================================
        # HIGH POTENTIAL
        # =====================================================

        if result.estimated_monthly_traffic >= 5000:

            result.high_traffic_potential = True

            result.add_reasoning(
                "High traffic potential detected"
            )

        # =====================================================
        # LOW VALUE
        # =====================================================

        if result.estimated_monthly_traffic < 100:

            result.worth_targeting = False

            result.add_warning(
                "Low traffic opportunity"
            )

        # =====================================================
        # RECOMMENDATIONS
        # =====================================================

        if result.featured_snippet_boost:

            result.add_recommendation(
                "Optimize snippet formatting"
            )

        if result.faq_boost:

            result.add_recommendation(
                "Expand FAQ coverage"
            )

        if result.long_tail_advantage:

            result.add_recommendation(
                "Target semantic long-tail variations"
            )

    # =========================================================
    # EXPORT
    # =========================================================

    def export(
        self,
        result: TrafficEstimationResult,
    ) -> Dict[str, Any]:

        return {

            "estimated_monthly_traffic": (
                result.estimated_monthly_traffic
            ),

            "estimated_daily_traffic": (
                result.estimated_daily_traffic
            ),

            "estimated_impressions": (
                result.estimated_impressions
            ),

            "estimated_clicks": (
                result.estimated_clicks
            ),

            "estimated_ctr": (
                result.estimated_ctr
            ),

            "ctr_potential": (
                result.ctr_potential
            ),

            "visibility_score": (
                result.visibility_score
            ),

            "click_opportunity_score": (
                result.click_opportunity_score
            ),

            "traffic_quality": (
                result.traffic_quality
            ),

            "conversion_potential": (
                result.conversion_potential
            ),

            "engagement_probability": (
                result.engagement_probability
            ),

            "traffic_decay_risk": (
                result.traffic_decay_risk
            ),

            "traffic_stability": (
                result.traffic_stability
            ),

            "predicted_decay_percentage": (
                result.predicted_decay_percentage
            ),

            "predicted_position": (
                result.predicted_position
            ),

            "top_10_probability": (
                result.top_10_probability
            ),

            "top_3_probability": (
                result.top_3_probability
            ),

            "featured_snippet_boost": (
                result.featured_snippet_boost
            ),

            "faq_boost": (
                result.faq_boost
            ),

            "video_boost": (
                result.video_boost
            ),

            "freshness_advantage": (
                result.freshness_advantage
            ),

            "long_tail_advantage": (
                result.long_tail_advantage
            ),

            "weak_serp_advantage": (
                result.weak_serp_advantage
            ),

            "high_traffic_potential": (
                result.high_traffic_potential
            ),

            "worth_targeting": (
                result.worth_targeting
            ),

            "traffic_signals": (
                result.traffic_signals
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

            "metadata": (
                result.metadata
            ),
        }