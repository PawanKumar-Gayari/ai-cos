"""
Opportunity Estimator

Purpose:
Estimate SEO and ranking opportunities BEFORE publishing.

This engine predicts:
- ranking opportunity
- snippet opportunity
- traffic opportunity
- low-competition advantages
- semantic exploitability

Goal:
Identify whether a keyword/topic is worth targeting.

This becomes the strategic opportunity brain
of the editorial intelligence system.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List


# =============================================================
# RESULT
# =============================================================

@dataclass
class OpportunityEstimationResult:

    # =========================================================
    # CORE SCORES
    # =========================================================

    opportunity_score: float = 0.0

    ranking_opportunity: float = 0.0

    traffic_opportunity: float = 0.0

    snippet_opportunity: float = 0.0

    # =========================================================
    # COMPETITION
    # =========================================================

    competition_level: str = "medium"

    competition_score: float = 50.0

    authority_gap: float = 0.0

    backlink_pressure: float = 0.0

    # =========================================================
    # SERP ADVANTAGES
    # =========================================================

    weak_serp_detected: bool = False

    weak_content_detected: bool = False

    low_authority_serp: bool = False

    freshness_gap_detected: bool = False

    semantic_gap_detected: bool = False

    # =========================================================
    # FEATURE OPPORTUNITIES
    # =========================================================

    featured_snippet_opportunity: bool = False

    faq_opportunity: bool = False

    table_opportunity: bool = False

    video_opportunity: bool = False

    # =========================================================
    # TRAFFIC
    # =========================================================

    estimated_monthly_traffic: int = 0

    estimated_ctr: float = 0.0

    estimated_impressions: int = 0

    # =========================================================
    # STRATEGIC SIGNALS
    # =========================================================

    long_tail_advantage: bool = False

    freshness_advantage: bool = False

    authority_advantage: bool = False

    topical_advantage: bool = False

    # =========================================================
    # DECISION
    # =========================================================

    worth_targeting: bool = True

    aggressive_strategy_recommended: bool = False

    # =========================================================
    # SIGNALS
    # =========================================================

    opportunity_signals: Dict[str, Any] = field(
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
# OPPORTUNITY ESTIMATOR
# =============================================================

class OpportunityEstimator:

    """
    SEO opportunity intelligence engine.
    """

    # =========================================================
    # MAIN
    # =========================================================

    def estimate(
        self,
        topic: str,
        niche: str = "default",
        serp_data: Dict[str, Any] = None,
    ) -> OpportunityEstimationResult:

        serp_data = serp_data or {}

        result = OpportunityEstimationResult()

        topic = (topic or "").lower()

        niche = (niche or "").lower()

        # =====================================================
        # COMPETITION
        # =====================================================

        self._analyze_competition(
            result,
            serp_data,
        )

        # =====================================================
        # WEAK SERP
        # =====================================================

        self._detect_weak_serp(
            result,
            serp_data,
        )

        # =====================================================
        # FEATURES
        # =====================================================

        self._detect_feature_opportunities(
            result,
            serp_data,
        )

        # =====================================================
        # FRESHNESS
        # =====================================================

        self._detect_freshness_advantage(
            result,
            topic,
            niche,
            serp_data,
        )

        # =====================================================
        # LONG TAIL
        # =====================================================

        self._detect_long_tail_advantage(
            result,
            topic,
        )

        # =====================================================
        # TRAFFIC
        # =====================================================

        self._estimate_traffic(
            result,
            serp_data,
        )

        # =====================================================
        # FINAL SCORE
        # =====================================================

        self._calculate_opportunity_score(
            result
        )

        # =====================================================
        # DECISION
        # =====================================================

        self._evaluate_targeting(
            result
        )

        return result

    # =========================================================
    # COMPETITION
    # =========================================================

    def _analyze_competition(
        self,
        result: OpportunityEstimationResult,
        serp_data: Dict[str, Any],
    ) -> None:

        authority_domains = serp_data.get(
            "authority_domains",
            [],
        )

        backlinks = serp_data.get(
            "average_backlinks",
            0,
        )

        domain_count = len(authority_domains)

        # =====================================================
        # LEVEL
        # =====================================================

        if domain_count >= 7:

            result.competition_level = "very_high"

            result.competition_score = 90

            result.authority_gap = 85

        elif domain_count >= 4:

            result.competition_level = "high"

            result.competition_score = 70

            result.authority_gap = 60

        elif domain_count >= 2:

            result.competition_level = "medium"

            result.competition_score = 50

            result.authority_gap = 40

        else:

            result.competition_level = "low"

            result.competition_score = 25

            result.authority_gap = 20

        # =====================================================
        # BACKLINKS
        # =====================================================

        if backlinks >= 5000:

            result.backlink_pressure = 90

        elif backlinks >= 1000:

            result.backlink_pressure = 70

        elif backlinks >= 300:

            result.backlink_pressure = 50

        else:

            result.backlink_pressure = 20

    # =========================================================
    # WEAK SERP
    # =========================================================

    def _detect_weak_serp(
        self,
        result: OpportunityEstimationResult,
        serp_data: Dict[str, Any],
    ) -> None:

        weak_results = serp_data.get(
            "weak_results",
            0,
        )

        if weak_results >= 3:

            result.weak_serp_detected = True

            result.weak_content_detected = True

            result.low_authority_serp = True

            result.add_reasoning(
                "Weak SERP opportunity detected"
            )

    # =========================================================
    # FEATURES
    # =========================================================

    def _detect_feature_opportunities(
        self,
        result: OpportunityEstimationResult,
        serp_data: Dict[str, Any],
    ) -> None:

        if serp_data.get(
            "featured_snippet",
            False,
        ):

            result.featured_snippet_opportunity = True

            result.snippet_opportunity = 80

            result.add_reasoning(
                "Featured snippet opportunity detected"
            )

        faq_results = serp_data.get(
            "faq_results",
            0,
        )

        if faq_results >= 2:

            result.faq_opportunity = True

        table_results = serp_data.get(
            "table_results",
            0,
        )

        if table_results >= 2:

            result.table_opportunity = True

        video_results = serp_data.get(
            "video_results",
            0,
        )

        if video_results >= 2:

            result.video_opportunity = True

    # =========================================================
    # FRESHNESS
    # =========================================================

    def _detect_freshness_advantage(
        self,
        result: OpportunityEstimationResult,
        topic: str,
        niche: str,
        serp_data: Dict[str, Any],
    ) -> None:

        freshness_keywords = [

            "latest",
            "news",
            "update",
            "result",
            "notification",
        ]

        recent_results = serp_data.get(
            "recent_results",
            0,
        )

        if (

            any(
                keyword in topic
                for keyword in freshness_keywords
            )

            or

            niche in [
                "jobs",
                "news",
                "tech",
            ]
        ):

            if recent_results <= 3:

                result.freshness_gap_detected = True

                result.freshness_advantage = True

                result.add_reasoning(
                    "Freshness advantage detected"
                )

    # =========================================================
    # LONG TAIL
    # =========================================================

    def _detect_long_tail_advantage(
        self,
        result: OpportunityEstimationResult,
        topic: str,
    ) -> None:

        words = topic.split()

        if len(words) >= 5:

            result.long_tail_advantage = True

            result.add_reasoning(
                "Long-tail keyword advantage detected"
            )

    # =========================================================
    # TRAFFIC
    # =========================================================

    def _estimate_traffic(
        self,
        result: OpportunityEstimationResult,
        serp_data: Dict[str, Any],
    ) -> None:

        search_volume = serp_data.get(
            "search_volume",
            0,
        )

        ctr = 0.18

        if result.featured_snippet_opportunity:
            ctr += 0.05

        if result.competition_level == "low":
            ctr += 0.05

        result.estimated_ctr = round(
            ctr,
            2,
        )

        result.estimated_impressions = (
            search_volume
        )

        result.estimated_monthly_traffic = int(
            search_volume * ctr
        )

        result.traffic_opportunity = min(

            (
                result.estimated_monthly_traffic /
                max(search_volume, 1)
            ) * 100,

            100,
        )

    # =========================================================
    # SCORE
    # =========================================================

    def _calculate_opportunity_score(
        self,
        result: OpportunityEstimationResult,
    ) -> None:

        score = 50

        # =====================================================
        # ADVANTAGES
        # =====================================================

        if result.weak_serp_detected:
            score += 20

        if result.featured_snippet_opportunity:
            score += 15

        if result.long_tail_advantage:
            score += 10

        if result.freshness_advantage:
            score += 10

        if result.low_authority_serp:
            score += 15

        # =====================================================
        # PENALTIES
        # =====================================================

        score -= (
            result.competition_score * 0.3
        )

        score -= (
            result.backlink_pressure * 0.2
        )

        result.ranking_opportunity = round(
            max(score, 0),
            2,
        )

        result.opportunity_score = round(

            (
                result.ranking_opportunity +

                result.traffic_opportunity +

                result.snippet_opportunity
            ) / 3,

            2,
        )

    # =========================================================
    # DECISION
    # =========================================================

    def _evaluate_targeting(
        self,
        result: OpportunityEstimationResult,
    ) -> None:

        if result.opportunity_score >= 75:

            result.aggressive_strategy_recommended = True

            result.add_recommendation(
                "Aggressive ranking strategy recommended"
            )

        elif result.opportunity_score < 35:

            result.worth_targeting = False

            result.add_warning(
                "Low opportunity keyword"
            )

            result.add_recommendation(
                "Target semantic variations instead"
            )

        # =====================================================
        # STRATEGY
        # =====================================================

        if result.featured_snippet_opportunity:

            result.add_recommendation(
                "Optimize for featured snippets"
            )

        if result.faq_opportunity:

            result.add_recommendation(
                "Add FAQ sections"
            )

        if result.table_opportunity:

            result.add_recommendation(
                "Use structured comparison tables"
            )

    # =========================================================
    # EXPORT
    # =========================================================

    def export(
        self,
        result: OpportunityEstimationResult,
    ) -> Dict[str, Any]:

        return {

            "opportunity_score": (
                result.opportunity_score
            ),

            "ranking_opportunity": (
                result.ranking_opportunity
            ),

            "traffic_opportunity": (
                result.traffic_opportunity
            ),

            "snippet_opportunity": (
                result.snippet_opportunity
            ),

            "competition_level": (
                result.competition_level
            ),

            "competition_score": (
                result.competition_score
            ),

            "authority_gap": (
                result.authority_gap
            ),

            "backlink_pressure": (
                result.backlink_pressure
            ),

            "weak_serp_detected": (
                result.weak_serp_detected
            ),

            "weak_content_detected": (
                result.weak_content_detected
            ),

            "low_authority_serp": (
                result.low_authority_serp
            ),

            "freshness_gap_detected": (
                result.freshness_gap_detected
            ),

            "semantic_gap_detected": (
                result.semantic_gap_detected
            ),

            "featured_snippet_opportunity": (
                result.featured_snippet_opportunity
            ),

            "faq_opportunity": (
                result.faq_opportunity
            ),

            "table_opportunity": (
                result.table_opportunity
            ),

            "video_opportunity": (
                result.video_opportunity
            ),

            "estimated_monthly_traffic": (
                result.estimated_monthly_traffic
            ),

            "estimated_ctr": (
                result.estimated_ctr
            ),

            "estimated_impressions": (
                result.estimated_impressions
            ),

            "long_tail_advantage": (
                result.long_tail_advantage
            ),

            "freshness_advantage": (
                result.freshness_advantage
            ),

            "authority_advantage": (
                result.authority_advantage
            ),

            "topical_advantage": (
                result.topical_advantage
            ),

            "worth_targeting": (
                result.worth_targeting
            ),

            "aggressive_strategy_recommended": (
                result.aggressive_strategy_recommended
            ),

            "opportunity_signals": (
                result.opportunity_signals
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