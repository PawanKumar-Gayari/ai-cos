"""
Strategy Agent

Purpose:
Determine the best ranking and publishing
strategy for content based on SERP,
competition, intent, freshness, authority,
and opportunity signals.

Analyzes:
- SERP opportunities
- ranking strategies
- snippet opportunities
- content angles
- competitor weaknesses
- search intent alignment
- traffic opportunities

Goal:
Create adaptive ranking intelligence.

This becomes the strategic intelligence layer
of AI_COS.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List


# =============================================================
# STRATEGY RESULT
# =============================================================

@dataclass
class StrategyResult:

    # =========================================================
    # SCORES
    # =========================================================

    strategy_score: float = 0.0

    ranking_opportunity_score: float = 0.0

    snippet_opportunity_score: float = 0.0

    traffic_opportunity_score: float = 0.0

    # =========================================================
    # STRATEGY
    # =========================================================

    primary_strategy: str = "balanced"

    content_angle: str = "general"

    serp_strategy: str = "standard"

    # =========================================================
    # FEATURES
    # =========================================================

    snippet_targeting_enabled: bool = False

    faq_strategy_enabled: bool = False

    authority_strategy_enabled: bool = False

    freshness_strategy_enabled: bool = False

    longtail_strategy_enabled: bool = False

    # =========================================================
    # OPPORTUNITIES
    # =========================================================

    featured_snippet_opportunity: bool = False

    faq_opportunity: bool = False

    low_competition_opportunity: bool = False

    freshness_gap_detected: bool = False

    competitor_weakness_detected: bool = False

    # =========================================================
    # RISKS
    # =========================================================

    competition_risk: str = "low"

    ranking_difficulty: str = "medium"

    traffic_risk: str = "medium"

    # =========================================================
    # DETECTIONS
    # =========================================================

    informational_intent_detected: bool = False

    transactional_intent_detected: bool = False

    comparison_intent_detected: bool = False

    freshness_sensitive_detected: bool = False

    # =========================================================
    # SIGNALS
    # =========================================================

    strategy_signals: Dict[str, Any] = field(
        default_factory=dict
    )

    # =========================================================
    # KEYWORDS
    # =========================================================

    detected_keywords: List[str] = field(
        default_factory=list
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
# STRATEGY AGENT
# =============================================================

class StrategyAgent:

    """
    Ranking strategy intelligence agent.
    """

    # =========================================================
    # KEYWORDS
    # =========================================================

    SNIPPET_KEYWORDS = [

        "how to",
        "what is",
        "best",
        "top",
        "guide",
        "tips",
    ]

    FAQ_KEYWORDS = [

        "why",
        "when",
        "where",
        "can",
        "does",
        "is",
    ]

    TRANSACTIONAL_KEYWORDS = [

        "buy",
        "price",
        "deal",
        "offer",
        "discount",
    ]

    COMPARISON_KEYWORDS = [

        "vs",
        "comparison",
        "better",
        "review",
    ]

    FRESHNESS_KEYWORDS = [

        "latest",
        "2026",
        "today",
        "update",
        "notification",
        "result",
    ]

    # =========================================================
    # ANALYZE
    # =========================================================

    def analyze(
        self,
        topic: str,
        competition_score: float = 50.0,
        freshness_sensitive: bool = False,
    ) -> StrategyResult:

        result = StrategyResult()

        topic = (
            topic or ""
        ).lower()

        # =====================================================
        # INTENT
        # =====================================================

        self._detect_intent(
            result,
            topic,
        )

        # =====================================================
        # SNIPPET
        # =====================================================

        self._detect_snippet_opportunity(
            result,
            topic,
        )

        # =====================================================
        # FAQ
        # =====================================================

        self._detect_faq_opportunity(
            result,
            topic,
        )

        # =====================================================
        # FRESHNESS
        # =====================================================

        self._detect_freshness(
            result,
            topic,
            freshness_sensitive,
        )

        # =====================================================
        # COMPETITION
        # =====================================================

        self._analyze_competition(
            result,
            competition_score,
        )

        # =====================================================
        # STRATEGY
        # =====================================================

        self._select_strategy(
            result
        )

        # =====================================================
        # SCORES
        # =====================================================

        self._calculate_scores(
            result,
            competition_score,
        )

        # =====================================================
        # FINALIZE
        # =====================================================

        self._finalize(
            result
        )

        return result

    # =========================================================
    # INTENT
    # =========================================================

    def _detect_intent(
        self,
        result: StrategyResult,
        topic: str,
    ) -> None:

        # =====================================================
        # TRANSACTIONAL
        # =====================================================

        if any(

            keyword in topic

            for keyword
            in self.TRANSACTIONAL_KEYWORDS
        ):

            result.transactional_intent_detected = (
                True
            )

            result.detected_keywords.append(
                "transactional"
            )

        # =====================================================
        # COMPARISON
        # =====================================================

        if any(

            keyword in topic

            for keyword
            in self.COMPARISON_KEYWORDS
        ):

            result.comparison_intent_detected = (
                True
            )

            result.detected_keywords.append(
                "comparison"
            )

        # =====================================================
        # INFORMATIONAL
        # =====================================================

        if (

            not result.transactional_intent_detected

            and

            not result.comparison_intent_detected
        ):

            result.informational_intent_detected = (
                True
            )

            result.detected_keywords.append(
                "informational"
            )

    # =========================================================
    # SNIPPET
    # =========================================================

    def _detect_snippet_opportunity(
        self,
        result: StrategyResult,
        topic: str,
    ) -> None:

        if any(

            keyword in topic

            for keyword
            in self.SNIPPET_KEYWORDS
        ):

            result.featured_snippet_opportunity = (
                True
            )

            result.snippet_targeting_enabled = (
                True
            )

            result.add_reasoning(
                "Featured snippet opportunity detected"
            )

    # =========================================================
    # FAQ
    # =========================================================

    def _detect_faq_opportunity(
        self,
        result: StrategyResult,
        topic: str,
    ) -> None:

        if any(

            keyword in topic.split()

            for keyword
            in self.FAQ_KEYWORDS
        ):

            result.faq_opportunity = (
                True
            )

            result.faq_strategy_enabled = (
                True
            )

            result.add_reasoning(
                "FAQ optimization opportunity detected"
            )

    # =========================================================
    # FRESHNESS
    # =========================================================

    def _detect_freshness(
        self,
        result: StrategyResult,
        topic: str,
        freshness_sensitive: bool,
    ) -> None:

        if (

            freshness_sensitive

            or

            any(

                keyword in topic

                for keyword
                in self.FRESHNESS_KEYWORDS
            )
        ):

            result.freshness_sensitive_detected = (
                True
            )

            result.freshness_strategy_enabled = (
                True
            )

            result.freshness_gap_detected = (
                True
            )

            result.add_reasoning(
                "Freshness ranking opportunity detected"
            )

    # =========================================================
    # COMPETITION
    # =========================================================

    def _analyze_competition(
        self,
        result: StrategyResult,
        competition_score: float,
    ) -> None:

        # =====================================================
        # LOW COMPETITION
        # =====================================================

        if competition_score < 40:

            result.low_competition_opportunity = (
                True
            )

            result.competitor_weakness_detected = (
                True
            )

            result.ranking_difficulty = (
                "low"
            )

            result.add_reasoning(
                "Low competition ranking opportunity detected"
            )

        # =====================================================
        # MEDIUM
        # =====================================================

        elif competition_score < 70:

            result.ranking_difficulty = (
                "medium"
            )

        # =====================================================
        # HIGH
        # =====================================================

        else:

            result.ranking_difficulty = (
                "high"
            )

            result.competition_risk = (
                "high"
            )

            result.add_warning(
                "High competition detected"
            )

    # =========================================================
    # STRATEGY
    # =========================================================

    def _select_strategy(
        self,
        result: StrategyResult,
    ) -> None:

        # =====================================================
        # FRESHNESS
        # =====================================================

        if result.freshness_sensitive_detected:

            result.primary_strategy = (
                "freshness_first"
            )

            result.serp_strategy = (
                "realtime_ranking"
            )

            result.content_angle = (
                "latest_updates"
            )

        # =====================================================
        # SNIPPET
        # =====================================================

        elif result.featured_snippet_opportunity:

            result.primary_strategy = (
                "snippet_domination"
            )

            result.serp_strategy = (
                "featured_snippet"
            )

            result.content_angle = (
                "structured_answers"
            )

        # =====================================================
        # COMPARISON
        # =====================================================

        elif result.comparison_intent_detected:

            result.primary_strategy = (
                "comparison_ranking"
            )

            result.serp_strategy = (
                "comparison_tables"
            )

            result.content_angle = (
                "vs_analysis"
            )

        # =====================================================
        # TRANSACTIONAL
        # =====================================================

        elif result.transactional_intent_detected:

            result.primary_strategy = (
                "conversion_optimization"
            )

            result.serp_strategy = (
                "ctr_optimization"
            )

            result.content_angle = (
                "buyer_intent"
            )

        # =====================================================
        # DEFAULT
        # =====================================================

        else:

            result.primary_strategy = (
                "authority_growth"
            )

            result.serp_strategy = (
                "longform_content"
            )

            result.content_angle = (
                "expert_guide"
            )

    # =========================================================
    # SCORES
    # =========================================================

    def _calculate_scores(
        self,
        result: StrategyResult,
        competition_score: float,
    ) -> None:

        score = 50

        # =====================================================
        # SNIPPET
        # =====================================================

        if result.featured_snippet_opportunity:

            score += 20

            result.snippet_opportunity_score = (
                85.0
            )

        # =====================================================
        # FAQ
        # =====================================================

        if result.faq_opportunity:

            score += 10

        # =====================================================
        # LOW COMPETITION
        # =====================================================

        if result.low_competition_opportunity:

            score += 20

        # =====================================================
        # FRESHNESS
        # =====================================================

        if result.freshness_gap_detected:

            score += 15

        # =====================================================
        # COMPETITION PENALTY
        # =====================================================

        score -= (
            competition_score * 0.2
        )

        # =====================================================
        # FINAL
        # =====================================================

        result.strategy_score = round(

            min(
                max(score, 0),
                100,
            ),

            2,
        )

        result.ranking_opportunity_score = round(

            result.strategy_score,

            2,
        )

        result.traffic_opportunity_score = round(

            min(
                result.strategy_score + 10,
                100,
            ),

            2,
        )

        result.add_reasoning(
            f"Strategy score calculated: "
            f"{result.strategy_score}"
        )

    # =========================================================
    # FINALIZE
    # =========================================================

    def _finalize(
        self,
        result: StrategyResult,
    ) -> None:

        # =====================================================
        # RECOMMENDATIONS
        # =====================================================

        if result.snippet_targeting_enabled:

            result.add_recommendation(
                "Use structured answers for featured snippets"
            )

            result.add_action(
                "Add snippet-focused headings"
            )

        if result.faq_strategy_enabled:

            result.add_recommendation(
                "Add FAQ schema markup"
            )

            result.add_action(
                "Create FAQ section"
            )

        if result.freshness_strategy_enabled:

            result.add_recommendation(
                "Enable realtime freshness updates"
            )

            result.add_action(
                "Monitor freshness decay"
            )

        if result.low_competition_opportunity:

            result.add_recommendation(
                "Publish aggressively for fast ranking"
            )

        if result.competition_risk == "high":

            result.add_recommendation(
                "Increase authority and backlinks"
            )

        # =====================================================
        # LONGTAIL
        # =====================================================

        if result.ranking_difficulty == "high":

            result.longtail_strategy_enabled = (
                True
            )

            result.add_reasoning(
                "Longtail strategy enabled due to high competition"
            )

        result.add_reasoning(
            f"Primary strategy selected: "
            f"{result.primary_strategy}"
        )

    # =========================================================
    # EXPORT
    # =========================================================

    def export(
        self,
        result: StrategyResult,
    ) -> Dict[str, Any]:

        return {

            "strategy_score": (
                result.strategy_score
            ),

            "ranking_opportunity_score": (
                result.ranking_opportunity_score
            ),

            "snippet_opportunity_score": (
                result.snippet_opportunity_score
            ),

            "traffic_opportunity_score": (
                result.traffic_opportunity_score
            ),

            "primary_strategy": (
                result.primary_strategy
            ),

            "content_angle": (
                result.content_angle
            ),

            "serp_strategy": (
                result.serp_strategy
            ),

            "snippet_targeting_enabled": (
                result.snippet_targeting_enabled
            ),

            "faq_strategy_enabled": (
                result.faq_strategy_enabled
            ),

            "authority_strategy_enabled": (
                result.authority_strategy_enabled
            ),

            "freshness_strategy_enabled": (
                result.freshness_strategy_enabled
            ),

            "longtail_strategy_enabled": (
                result.longtail_strategy_enabled
            ),

            "featured_snippet_opportunity": (
                result.featured_snippet_opportunity
            ),

            "faq_opportunity": (
                result.faq_opportunity
            ),

            "low_competition_opportunity": (
                result.low_competition_opportunity
            ),

            "freshness_gap_detected": (
                result.freshness_gap_detected
            ),

            "competitor_weakness_detected": (
                result.competitor_weakness_detected
            ),

            "competition_risk": (
                result.competition_risk
            ),

            "ranking_difficulty": (
                result.ranking_difficulty
            ),

            "traffic_risk": (
                result.traffic_risk
            ),

            "informational_intent_detected": (
                result.informational_intent_detected
            ),

            "transactional_intent_detected": (
                result.transactional_intent_detected
            ),

            "comparison_intent_detected": (
                result.comparison_intent_detected
            ),

            "freshness_sensitive_detected": (
                result.freshness_sensitive_detected
            ),

            "detected_keywords": (
                result.detected_keywords
            ),

            "strategy_signals": (
                result.strategy_signals
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