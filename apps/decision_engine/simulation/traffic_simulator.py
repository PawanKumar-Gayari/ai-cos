"""
Traffic Simulator

Purpose:
Predict future traffic potential BEFORE
publishing based on ranking probability,
CTR behavior, freshness, competition,
and trend velocity.

Analyzes:
- ranking traffic potential
- organic CTR opportunity
- trend growth
- freshness traffic spikes
- long-term traffic stability
- traffic decay probability

Goal:
Predict estimated organic traffic and
future growth opportunities.

This becomes the predictive traffic
intelligence layer of AI_COS.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List


# =============================================================
# TRAFFIC RESULT
# =============================================================

@dataclass
class TrafficSimulationResult:

    # =========================================================
    # TRAFFIC
    # =========================================================

    estimated_monthly_clicks: int = 0

    estimated_daily_clicks: int = 0

    estimated_yearly_clicks: int = 0

    traffic_probability: float = 0.0

    # =========================================================
    # CTR
    # =========================================================

    estimated_ctr: float = 0.0

    ctr_opportunity_score: float = 0.0

    snippet_ctr_boost: float = 0.0

    # =========================================================
    # GROWTH
    # =========================================================

    traffic_growth_probability: float = 0.0

    viral_probability: float = 0.0

    trend_growth_score: float = 0.0

    longterm_stability_score: float = 0.0

    # =========================================================
    # FLAGS
    # =========================================================

    high_traffic_potential: bool = False

    viral_potential_detected: bool = False

    trend_traffic_detected: bool = False

    freshness_spike_possible: bool = False

    # =========================================================
    # OPPORTUNITIES
    # =========================================================

    snippet_traffic_opportunity: bool = False

    low_competition_traffic_opportunity: bool = False

    longtail_traffic_opportunity: bool = False

    authority_traffic_advantage: bool = False

    # =========================================================
    # RISKS
    # =========================================================

    traffic_decay_risk: str = "medium"

    volatility_risk: str = "medium"

    competition_risk: str = "medium"

    ctr_risk: str = "medium"

    # =========================================================
    # TRAFFIC WINDOWS
    # =========================================================

    expected_peak_days: int = 30

    expected_traffic_lifespan_days: int = 180

    traffic_velocity: str = "medium"

    # =========================================================
    # SIGNALS
    # =========================================================

    traffic_signals: Dict[str, Any] = field(
        default_factory=dict
    )

    # =========================================================
    # PREDICTIONS
    # =========================================================

    traffic_predictions: Dict[str, Any] = field(
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
    # ACTIONS
    # =========================================================

    recommended_actions: List[str] = field(
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
# TRAFFIC SIMULATOR
# =============================================================

class TrafficSimulator:

    """
    Predictive organic traffic simulator.
    """

    # =========================================================
    # CTR MAP
    # =========================================================

    POSITION_CTR = {

        1: 28.0,
        2: 15.0,
        3: 11.0,
        4: 8.0,
        5: 6.0,
        6: 4.5,
        7: 3.5,
        8: 2.8,
        9: 2.0,
        10: 1.5,
    }

    # =========================================================
    # ANALYZE
    # =========================================================

    def analyze(
        self,
        keyword_volume: int = 1000,
        expected_position: int = 20,
        ranking_probability: float = 50.0,
        freshness_score: float = 50.0,
        competition_score: float = 50.0,
        authority_score: float = 50.0,
        snippet_ready: bool = False,
        trend_sensitive: bool = False,
    ) -> TrafficSimulationResult:

        result = TrafficSimulationResult()

        # =====================================================
        # CTR
        # =====================================================

        self._calculate_ctr(
            result,
            expected_position,
            snippet_ready,
        )

        # =====================================================
        # TRAFFIC
        # =====================================================

        self._predict_traffic(
            result,
            keyword_volume,
            ranking_probability,
        )

        # =====================================================
        # GROWTH
        # =====================================================

        self._predict_growth(
            result,
            freshness_score,
            trend_sensitive,
            authority_score,
        )

        # =====================================================
        # OPPORTUNITIES
        # =====================================================

        self._detect_opportunities(
            result,
            competition_score,
            snippet_ready,
            authority_score,
        )

        # =====================================================
        # RISKS
        # =====================================================

        self._detect_risks(
            result,
            competition_score,
            freshness_score,
        )

        # =====================================================
        # WINDOWS
        # =====================================================

        self._predict_traffic_windows(
            result,
            freshness_score,
            trend_sensitive,
        )

        # =====================================================
        # FINALIZE
        # =====================================================

        self._finalize(
            result
        )

        return result

    # =========================================================
    # CTR
    # =========================================================

    def _calculate_ctr(
        self,
        result: TrafficSimulationResult,
        expected_position: int,
        snippet_ready: bool,
    ) -> None:

        # =====================================================
        # BASE CTR
        # =====================================================

        ctr = self.POSITION_CTR.get(

            expected_position,

            1.0
        )

        # =====================================================
        # SNIPPET BOOST
        # =====================================================

        if snippet_ready:

            result.snippet_traffic_opportunity = (
                True
            )

            result.snippet_ctr_boost = (
                5.0
            )

            ctr += 5.0

            result.add_reasoning(
                "Featured snippet CTR boost predicted"
            )

        result.estimated_ctr = round(
            ctr,
            2,
        )

        result.ctr_opportunity_score = round(

            ctr * 3,

            2,
        )

    # =========================================================
    # TRAFFIC
    # =========================================================

    def _predict_traffic(
        self,
        result: TrafficSimulationResult,
        keyword_volume: int,
        ranking_probability: float,
    ) -> None:

        # =====================================================
        # TRAFFIC FORMULA
        # =====================================================

        monthly_clicks = (

            keyword_volume *

            (result.estimated_ctr / 100)

            *

            (ranking_probability / 100)
        )

        result.estimated_monthly_clicks = int(
            monthly_clicks
        )

        result.estimated_daily_clicks = int(

            monthly_clicks / 30
        )

        result.estimated_yearly_clicks = int(

            monthly_clicks * 12
        )

        result.traffic_probability = round(

            ranking_probability,

            2,
        )

        result.add_reasoning(
            f"Estimated monthly traffic: "
            f"{result.estimated_monthly_clicks}"
        )

    # =========================================================
    # GROWTH
    # =========================================================

    def _predict_growth(
        self,
        result: TrafficSimulationResult,
        freshness_score: float,
        trend_sensitive: bool,
        authority_score: float,
    ) -> None:

        growth = 50

        # =====================================================
        # FRESHNESS
        # =====================================================

        if freshness_score >= 80:

            growth += 20

            result.freshness_spike_possible = (
                True
            )

        # =====================================================
        # TREND
        # =====================================================

        if trend_sensitive:

            growth += 25

            result.trend_traffic_detected = (
                True
            )

            result.viral_potential_detected = (
                True
            )

        # =====================================================
        # AUTHORITY
        # =====================================================

        if authority_score >= 80:

            growth += 15

            result.authority_traffic_advantage = (
                True
            )

        result.traffic_growth_probability = round(

            min(growth, 100),

            2,
        )

        result.trend_growth_score = round(

            min(growth + 10, 100),

            2,
        )

        # =====================================================
        # VIRAL
        # =====================================================

        result.viral_probability = round(

            min(growth * 0.8, 100),

            2,
        )

        # =====================================================
        # STABILITY
        # =====================================================

        stability = 100 - abs(
            70 - freshness_score
        )

        result.longterm_stability_score = round(

            max(stability, 20),

            2,
        )

    # =========================================================
    # OPPORTUNITIES
    # =========================================================

    def _detect_opportunities(
        self,
        result: TrafficSimulationResult,
        competition_score: float,
        snippet_ready: bool,
        authority_score: float,
    ) -> None:

        # =====================================================
        # LOW COMPETITION
        # =====================================================

        if competition_score < 40:

            result.low_competition_traffic_opportunity = (
                True
            )

            result.add_reasoning(
                "Low competition traffic opportunity detected"
            )

        # =====================================================
        # LONGTAIL
        # =====================================================

        if competition_score <= 55:

            result.longtail_traffic_opportunity = (
                True
            )

        # =====================================================
        # AUTHORITY
        # =====================================================

        if authority_score >= 75:

            result.authority_traffic_advantage = (
                True
            )

    # =========================================================
    # RISKS
    # =========================================================

    def _detect_risks(
        self,
        result: TrafficSimulationResult,
        competition_score: float,
        freshness_score: float,
    ) -> None:

        # =====================================================
        # COMPETITION
        # =====================================================

        if competition_score >= 75:

            result.competition_risk = (
                "high"
            )

            result.add_warning(
                "High traffic competition detected"
            )

        elif competition_score >= 55:

            result.competition_risk = (
                "medium"
            )

        else:

            result.competition_risk = (
                "low"
            )

        # =====================================================
        # DECAY
        # =====================================================

        if freshness_score < 50:

            result.traffic_decay_risk = (
                "high"
            )

        elif freshness_score < 70:

            result.traffic_decay_risk = (
                "medium"
            )

        else:

            result.traffic_decay_risk = (
                "low"
            )

    # =========================================================
    # WINDOWS
    # =========================================================

    def _predict_traffic_windows(
        self,
        result: TrafficSimulationResult,
        freshness_score: float,
        trend_sensitive: bool,
    ) -> None:

        # =====================================================
        # TREND
        # =====================================================

        if trend_sensitive:

            result.expected_peak_days = 7

            result.expected_traffic_lifespan_days = (
                60
            )

            result.traffic_velocity = (
                "fast"
            )

        # =====================================================
        # FRESHNESS
        # =====================================================

        elif freshness_score >= 80:

            result.expected_peak_days = 14

            result.expected_traffic_lifespan_days = (
                120
            )

            result.traffic_velocity = (
                "medium"
            )

        # =====================================================
        # EVERGREEN
        # =====================================================

        else:

            result.expected_peak_days = 60

            result.expected_traffic_lifespan_days = (
                365
            )

            result.traffic_velocity = (
                "slow"
            )

    # =========================================================
    # FINALIZE
    # =========================================================

    def _finalize(
        self,
        result: TrafficSimulationResult,
    ) -> None:

        # =====================================================
        # HIGH TRAFFIC
        # =====================================================

        if result.estimated_monthly_clicks >= 10000:

            result.high_traffic_potential = (
                True
            )

        # =====================================================
        # VOLATILITY
        # =====================================================

        if result.trend_traffic_detected:

            result.volatility_risk = (
                "high"
            )

        elif result.traffic_velocity == "fast":

            result.volatility_risk = (
                "medium"
            )

        else:

            result.volatility_risk = (
                "low"
            )

        # =====================================================
        # CTR RISK
        # =====================================================

        if result.estimated_ctr < 2:

            result.ctr_risk = (
                "high"
            )

        elif result.estimated_ctr < 5:

            result.ctr_risk = (
                "medium"
            )

        else:

            result.ctr_risk = (
                "low"
            )

        # =====================================================
        # RECOMMENDATIONS
        # =====================================================

        if result.snippet_traffic_opportunity:

            result.add_recommendation(
                "Optimize aggressively for featured snippets"
            )

            result.add_action(
                "Add concise snippet answer blocks"
            )

        if result.low_competition_traffic_opportunity:

            result.add_recommendation(
                "Publish quickly to capture traffic"
            )

        if result.viral_potential_detected:

            result.add_recommendation(
                "Promote article immediately for viral growth"
            )

        if result.traffic_decay_risk == "high":

            result.add_recommendation(
                "Enable freshness monitoring and updates"
            )

        if result.estimated_ctr < 3:

            result.add_recommendation(
                "Improve titles and meta descriptions"
            )

        result.add_reasoning(
            f"Traffic velocity predicted: "
            f"{result.traffic_velocity}"
        )

    # =========================================================
    # EXPORT
    # =========================================================

    def export(
        self,
        result: TrafficSimulationResult,
    ) -> Dict[str, Any]:

        return {

            "estimated_monthly_clicks": (
                result.estimated_monthly_clicks
            ),

            "estimated_daily_clicks": (
                result.estimated_daily_clicks
            ),

            "estimated_yearly_clicks": (
                result.estimated_yearly_clicks
            ),

            "traffic_probability": (
                result.traffic_probability
            ),

            "estimated_ctr": (
                result.estimated_ctr
            ),

            "ctr_opportunity_score": (
                result.ctr_opportunity_score
            ),

            "snippet_ctr_boost": (
                result.snippet_ctr_boost
            ),

            "traffic_growth_probability": (
                result.traffic_growth_probability
            ),

            "viral_probability": (
                result.viral_probability
            ),

            "trend_growth_score": (
                result.trend_growth_score
            ),

            "longterm_stability_score": (
                result.longterm_stability_score
            ),

            "high_traffic_potential": (
                result.high_traffic_potential
            ),

            "viral_potential_detected": (
                result.viral_potential_detected
            ),

            "trend_traffic_detected": (
                result.trend_traffic_detected
            ),

            "freshness_spike_possible": (
                result.freshness_spike_possible
            ),

            "snippet_traffic_opportunity": (
                result.snippet_traffic_opportunity
            ),

            "low_competition_traffic_opportunity": (
                result.low_competition_traffic_opportunity
            ),

            "longtail_traffic_opportunity": (
                result.longtail_traffic_opportunity
            ),

            "authority_traffic_advantage": (
                result.authority_traffic_advantage
            ),

            "traffic_decay_risk": (
                result.traffic_decay_risk
            ),

            "volatility_risk": (
                result.volatility_risk
            ),

            "competition_risk": (
                result.competition_risk
            ),

            "ctr_risk": (
                result.ctr_risk
            ),

            "expected_peak_days": (
                result.expected_peak_days
            ),

            "expected_traffic_lifespan_days": (
                result.expected_traffic_lifespan_days
            ),

            "traffic_velocity": (
                result.traffic_velocity
            ),

            "traffic_signals": (
                result.traffic_signals
            ),

            "traffic_predictions": (
                result.traffic_predictions
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

            "recommended_actions": (
                result.recommended_actions
            ),

            "metadata": (
                result.metadata
            ),
        }