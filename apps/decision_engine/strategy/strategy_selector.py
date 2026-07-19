"""
Strategy Selector

Purpose:
Central orchestration layer for selecting
the BEST combined strategy across:
- article strategy
- FAQ strategy
- linking strategy
- SEO strategy
- freshness strategy
- authority strategy
- structure strategy

Goal:
Build the optimal unified editorial strategy
BEFORE article generation begins.

This becomes the master strategic brain
of AI_COS.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List

# =============================================================
# IMPORT STRATEGIES
# =============================================================

from .article_strategy import (
    ArticleStrategy,
)

from .faq_strategy import (
    FAQStrategy,
)

from .linking_strategy import (
    LinkingStrategy,
)


# =============================================================
# STRATEGY SELECTOR RESULT
# =============================================================

@dataclass
class StrategySelectorResult:

    # =========================================================
    # MASTER STRATEGY
    # =========================================================

    master_strategy: str = "balanced"

    strategy_confidence: float = 0.0

    execution_priority: str = "medium"

    # =========================================================
    # SUB STRATEGIES
    # =========================================================

    article_strategy: Dict[str, Any] = field(
        default_factory=dict
    )

    faq_strategy: Dict[str, Any] = field(
        default_factory=dict
    )

    linking_strategy: Dict[str, Any] = field(
        default_factory=dict
    )

    # =========================================================
    # PRIORITIES
    # =========================================================

    seo_priority: bool = False

    freshness_priority: bool = False

    authority_priority: bool = False

    snippet_priority: bool = False

    traffic_priority: bool = False

    # =========================================================
    # EXECUTION
    # =========================================================

    aggressive_strategy_enabled: bool = False

    realtime_strategy_enabled: bool = False

    authority_building_enabled: bool = False

    semantic_domination_enabled: bool = False

    # =========================================================
    # CONTENT PLAN
    # =========================================================

    recommended_word_count: int = 1500

    recommended_heading_count: int = 10

    recommended_faq_count: int = 5

    recommended_internal_links: int = 5

    # =========================================================
    # SEO PLAN
    # =========================================================

    target_keyword_density: float = 1.5

    semantic_optimization_level: str = "medium"

    ranking_strategy: str = "balanced"

    # =========================================================
    # RISKS
    # =========================================================

    competition_risk: str = "medium"

    ranking_risk: str = "medium"

    authority_risk: str = "medium"

    execution_risk: str = "medium"

    # =========================================================
    # OPPORTUNITIES
    # =========================================================

    low_competition_opportunity: bool = False

    snippet_opportunity: bool = False

    freshness_opportunity: bool = False

    traffic_opportunity: bool = False

    # =========================================================
    # SIGNALS
    # =========================================================

    strategy_signals: Dict[str, Any] = field(
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
# STRATEGY SELECTOR
# =============================================================

class StrategySelector:

    """
    Master strategy orchestration engine.
    """

    # =========================================================
    # INIT
    # =========================================================

    def __init__(self):

        self.article_strategy = (
            ArticleStrategy()
        )

        self.faq_strategy = (
            FAQStrategy()
        )

        self.linking_strategy = (
            LinkingStrategy()
        )

    # =========================================================
    # ANALYZE
    # =========================================================

    def analyze(
        self,
        keyword: str,
        competition_score: float = 50.0,
        freshness_score: float = 50.0,
        authority_score: float = 50.0,
        ranking_probability: float = 50.0,
        snippet_opportunity: bool = False,
        trend_sensitive: bool = False,
        topic_cluster_available: bool = False,
    ) -> StrategySelectorResult:

        result = StrategySelectorResult()

        # =====================================================
        # ARTICLE STRATEGY
        # =====================================================

        article_result = (
            self.article_strategy.analyze(
                keyword=keyword,
                competition_score=competition_score,
                freshness_score=freshness_score,
                authority_score=authority_score,
                ranking_probability=ranking_probability,
                trend_sensitive=trend_sensitive,
                snippet_opportunity=snippet_opportunity,
            )
        )

        # =====================================================
        # FAQ STRATEGY
        # =====================================================

        faq_result = (
            self.faq_strategy.analyze(
                keyword=keyword,
                competition_score=competition_score,
                snippet_opportunity=snippet_opportunity,
                voice_search_trend=True,
                article_type=article_result.article_type,
            )
        )

        # =====================================================
        # LINKING STRATEGY
        # =====================================================

        linking_result = (
            self.linking_strategy.analyze(
                keyword=keyword,
                competition_score=competition_score,
                authority_score=authority_score,
                article_type=article_result.article_type,
                topic_cluster_available=topic_cluster_available,
            )
        )

        # =====================================================
        # STORE
        # =====================================================

        result.article_strategy = (
            article_result.__dict__
        )

        result.faq_strategy = (
            faq_result.__dict__
        )

        result.linking_strategy = (
            linking_result.__dict__
        )

        # =====================================================
        # MASTER STRATEGY
        # =====================================================

        self._select_master_strategy(
            result,
            article_result,
            faq_result,
            linking_result,
            competition_score,
            freshness_score,
            ranking_probability,
        )

        # =====================================================
        # CONTENT PLAN
        # =====================================================

        self._build_content_plan(
            result,
            article_result,
            faq_result,
            linking_result,
        )

        # =====================================================
        # FLAGS
        # =====================================================

        self._build_flags(
            result,
            article_result,
            faq_result,
            linking_result,
        )

        # =====================================================
        # RISKS
        # =====================================================

        self._detect_risks(
            result,
            competition_score,
            authority_score,
        )

        # =====================================================
        # FINALIZE
        # =====================================================

        self._finalize(
            result
        )

        return result

    # =========================================================
    # MASTER STRATEGY
    # =========================================================

    def _select_master_strategy(
        self,
        result: StrategySelectorResult,
        article_result,
        faq_result,
        linking_result,
        competition_score: float,
        freshness_score: float,
        ranking_probability: float,
    ) -> None:

        # =====================================================
        # REALTIME
        # =====================================================

        if article_result.freshness_priority:

            result.master_strategy = (
                "realtime_domination"
            )

            result.realtime_strategy_enabled = (
                True
            )

            result.execution_priority = (
                "critical"
            )

        # =====================================================
        # LOW COMPETITION
        # =====================================================

        elif competition_score <= 40:

            result.master_strategy = (
                "aggressive_longtail_capture"
            )

            result.aggressive_strategy_enabled = (
                True
            )

        # =====================================================
        # HIGH COMPETITION
        # =====================================================

        elif competition_score >= 75:

            result.master_strategy = (
                "authority_semantic_domination"
            )

            result.authority_building_enabled = (
                True
            )

            result.semantic_domination_enabled = (
                True
            )

        # =====================================================
        # HIGH RANKING
        # =====================================================

        elif ranking_probability >= 80:

            result.master_strategy = (
                "ranking_acceleration"
            )

        # =====================================================
        # DEFAULT
        # =====================================================

        else:

            result.master_strategy = (
                "balanced_growth"
            )

        # =====================================================
        # CONFIDENCE
        # =====================================================

        confidence = (

            ranking_probability * 0.5

            +

            (100 - competition_score) * 0.3

            +

            freshness_score * 0.2
        )

        result.strategy_confidence = round(

            min(confidence, 100),

            2,
        )

        result.add_reasoning(
            f"Master strategy selected: "
            f"{result.master_strategy}"
        )

    # =========================================================
    # CONTENT PLAN
    # =========================================================

    def _build_content_plan(
        self,
        result: StrategySelectorResult,
        article_result,
        faq_result,
        linking_result,
    ) -> None:

        result.recommended_word_count = (
            article_result.recommended_word_count
        )

        result.recommended_heading_count = (
            article_result.recommended_heading_count
        )

        result.recommended_faq_count = (
            faq_result.recommended_faq_count
        )

        result.recommended_internal_links = (
            linking_result.recommended_internal_links
        )

        result.target_keyword_density = (
            article_result.target_keyword_density
        )

        result.semantic_optimization_level = (
            article_result.semantic_optimization_level
        )

        result.ranking_strategy = (
            article_result.ranking_strategy
        )

    # =========================================================
    # FLAGS
    # =========================================================

    def _build_flags(
        self,
        result: StrategySelectorResult,
        article_result,
        faq_result,
        linking_result,
    ) -> None:

        result.seo_priority = (
            article_result.seo_aggressiveness
            == "high"
        )

        result.freshness_priority = (
            article_result.freshness_priority
        )

        result.authority_priority = (
            article_result.authority_priority
        )

        result.snippet_priority = (
            faq_result.snippet_focus
        )

        result.traffic_priority = (
            article_result.traffic_opportunity
        )

        result.low_competition_opportunity = (
            article_result.low_competition_opportunity
        )

        result.snippet_opportunity = (
            faq_result.snippet_opportunity_detected
        )

        result.freshness_opportunity = (
            article_result.freshness_opportunity
        )

        result.traffic_opportunity = (
            article_result.traffic_opportunity
        )

    # =========================================================
    # RISKS
    # =========================================================

    def _detect_risks(
        self,
        result: StrategySelectorResult,
        competition_score: float,
        authority_score: float,
    ) -> None:

        # =====================================================
        # COMPETITION
        # =====================================================

        if competition_score >= 75:

            result.competition_risk = (
                "high"
            )

            result.execution_risk = (
                "high"
            )

            result.add_warning(
                "High competition execution environment"
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
        # AUTHORITY
        # =====================================================

        if authority_score < 50:

            result.authority_risk = (
                "high"
            )

            result.add_warning(
                "Authority gap detected"
            )

    # =========================================================
    # FINALIZE
    # =========================================================

    def _finalize(
        self,
        result: StrategySelectorResult,
    ) -> None:

        # =====================================================
        # RECOMMENDATIONS
        # =====================================================

        if result.aggressive_strategy_enabled:

            result.add_recommendation(
                "Execute aggressive SEO expansion"
            )

            result.add_action(
                "Increase semantic depth"
            )

        if result.realtime_strategy_enabled:

            result.add_recommendation(
                "Enable realtime publishing workflow"
            )

            result.add_action(
                "Prioritize freshness indexing"
            )

        if result.authority_building_enabled:

            result.add_recommendation(
                "Strengthen authority signals"
            )

            result.add_action(
                "Add official references"
            )

        if result.semantic_domination_enabled:

            result.add_recommendation(
                "Expand topic cluster coverage"
            )

            result.add_action(
                "Create semantic entity network"
            )

        if result.snippet_priority:

            result.add_recommendation(
                "Optimize for featured snippets"
            )

        result.add_reasoning(
            f"Strategy confidence: "
            f"{result.strategy_confidence}"
        )

    # =========================================================
    # EXPORT
    # =========================================================

    def export(
        self,
        result: StrategySelectorResult,
    ) -> Dict[str, Any]:

        return {

            "master_strategy": (
                result.master_strategy
            ),

            "strategy_confidence": (
                result.strategy_confidence
            ),

            "execution_priority": (
                result.execution_priority
            ),

            "article_strategy": (
                result.article_strategy
            ),

            "faq_strategy": (
                result.faq_strategy
            ),

            "linking_strategy": (
                result.linking_strategy
            ),

            "seo_priority": (
                result.seo_priority
            ),

            "freshness_priority": (
                result.freshness_priority
            ),

            "authority_priority": (
                result.authority_priority
            ),

            "snippet_priority": (
                result.snippet_priority
            ),

            "traffic_priority": (
                result.traffic_priority
            ),

            "aggressive_strategy_enabled": (
                result.aggressive_strategy_enabled
            ),

            "realtime_strategy_enabled": (
                result.realtime_strategy_enabled
            ),

            "authority_building_enabled": (
                result.authority_building_enabled
            ),

            "semantic_domination_enabled": (
                result.semantic_domination_enabled
            ),

            "recommended_word_count": (
                result.recommended_word_count
            ),

            "recommended_heading_count": (
                result.recommended_heading_count
            ),

            "recommended_faq_count": (
                result.recommended_faq_count
            ),

            "recommended_internal_links": (
                result.recommended_internal_links
            ),

            "target_keyword_density": (
                result.target_keyword_density
            ),

            "semantic_optimization_level": (
                result.semantic_optimization_level
            ),

            "ranking_strategy": (
                result.ranking_strategy
            ),

            "competition_risk": (
                result.competition_risk
            ),

            "ranking_risk": (
                result.ranking_risk
            ),

            "authority_risk": (
                result.authority_risk
            ),

            "execution_risk": (
                result.execution_risk
            ),

            "low_competition_opportunity": (
                result.low_competition_opportunity
            ),

            "snippet_opportunity": (
                result.snippet_opportunity
            ),

            "freshness_opportunity": (
                result.freshness_opportunity
            ),

            "traffic_opportunity": (
                result.traffic_opportunity
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