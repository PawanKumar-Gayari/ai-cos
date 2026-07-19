"""
Decision Router

Purpose:
Route articles into the correct intelligence
strategy and workflow pipeline.

Routes based on:
- niche
- intent
- risk
- freshness sensitivity
- authority requirements
- verification requirements

Goal:
Enable adaptive orchestration intelligence.

This becomes the adaptive routing brain
of AI_COS.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List


# =============================================================
# ROUTE RESULT
# =============================================================

@dataclass
class DecisionRouteResult:

    # =========================================================
    # ROUTING
    # =========================================================

    workflow: str = "general_workflow"

    strategy: str = "general_strategy"

    pipeline: str = "default_pipeline"

    # =========================================================
    # ENGINE PRIORITIES
    # =========================================================

    freshness_priority: str = "medium"

    verification_priority: str = "medium"

    authority_priority: str = "medium"

    ranking_priority: str = "medium"

    # =========================================================
    # FLAGS
    # =========================================================

    human_review_required: bool = False

    aggressive_verification_required: bool = False

    freshness_monitoring_required: bool = False

    expert_review_required: bool = False

    # =========================================================
    # WORKFLOW FEATURES
    # =========================================================

    realtime_verification_enabled: bool = False

    auto_refresh_enabled: bool = False

    ranking_tracking_enabled: bool = True

    serp_monitoring_enabled: bool = True

    # =========================================================
    # STRATEGY FEATURES
    # =========================================================

    faq_strategy_enabled: bool = False

    snippet_strategy_enabled: bool = False

    authority_strategy_enabled: bool = False

    freshness_strategy_enabled: bool = False

    # =========================================================
    # DECISION SIGNALS
    # =========================================================

    routing_signals: Dict[str, Any] = field(
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
# DECISION ROUTER
# =============================================================

class DecisionRouter:

    """
    Adaptive workflow routing engine.
    """

    # =========================================================
    # MAIN ROUTER
    # =========================================================

    def route(
        self,
        topic: str,
        niche: str = "general",
        intent: str = "informational",
        ymyl: bool = False,
        freshness_sensitive: bool = False,
    ) -> DecisionRouteResult:

        result = DecisionRouteResult()

        topic = (topic or "").lower()

        niche = (niche or "").lower()

        intent = (intent or "").lower()

        # =====================================================
        # NICHE ROUTING
        # =====================================================

        self._route_by_niche(
            result,
            niche,
        )

        # =====================================================
        # INTENT ROUTING
        # =====================================================

        self._route_by_intent(
            result,
            intent,
        )

        # =====================================================
        # YMYL ROUTING
        # =====================================================

        if ymyl:

            self._apply_ymyl_strategy(
                result
            )

        # =====================================================
        # FRESHNESS
        # =====================================================

        if freshness_sensitive:

            self._apply_freshness_strategy(
                result
            )

        # =====================================================
        # TOPIC SIGNALS
        # =====================================================

        self._analyze_topic_signals(
            result,
            topic,
        )

        # =====================================================
        # FINAL WORKFLOW
        # =====================================================

        self._finalize_workflow(
            result
        )

        return result

    # =========================================================
    # NICHE ROUTING
    # =========================================================

    def _route_by_niche(
        self,
        result: DecisionRouteResult,
        niche: str,
    ) -> None:

        # =====================================================
        # JOBS
        # =====================================================

        if niche in [
            "jobs",
            "government_jobs",
            "recruitment",
        ]:

            result.workflow = (
                "freshness_heavy_workflow"
            )

            result.strategy = (
                "freshness_first_strategy"
            )

            result.pipeline = (
                "realtime_pipeline"
            )

            result.freshness_priority = (
                "critical"
            )

            result.freshness_monitoring_required = (
                True
            )

            result.auto_refresh_enabled = (
                True
            )

            result.freshness_strategy_enabled = (
                True
            )

            result.add_reasoning(
                "Jobs niche requires realtime freshness monitoring"
            )

        # =====================================================
        # MEDICAL
        # =====================================================

        elif niche in [
            "medical",
            "health",
            "finance",
            "legal",
        ]:

            result.workflow = (
                "verification_heavy_workflow"
            )

            result.strategy = (
                "authority_first_strategy"
            )

            result.pipeline = (
                "verification_pipeline"
            )

            result.verification_priority = (
                "critical"
            )

            result.authority_priority = (
                "critical"
            )

            result.aggressive_verification_required = (
                True
            )

            result.expert_review_required = (
                True
            )

            result.authority_strategy_enabled = (
                True
            )

            result.add_reasoning(
                "YMYL-sensitive niche detected"
            )

        # =====================================================
        # AFFILIATE
        # =====================================================

        elif niche in [
            "affiliate",
            "reviews",
            "products",
        ]:

            result.workflow = (
                "conversion_workflow"
            )

            result.strategy = (
                "ctr_optimization_strategy"
            )

            result.pipeline = (
                "ranking_pipeline"
            )

            result.ranking_priority = (
                "high"
            )

            result.snippet_strategy_enabled = (
                True
            )

            result.faq_strategy_enabled = (
                True
            )

            result.add_reasoning(
                "Affiliate optimization workflow selected"
            )

        # =====================================================
        # NEWS
        # =====================================================

        elif niche in [
            "news",
            "technology",
            "updates",
        ]:

            result.workflow = (
                "news_workflow"
            )

            result.strategy = (
                "rapid_publish_strategy"
            )

            result.pipeline = (
                "fast_index_pipeline"
            )

            result.freshness_priority = (
                "critical"
            )

            result.realtime_verification_enabled = (
                True
            )

            result.add_reasoning(
                "News workflow requires rapid freshness validation"
            )

        # =====================================================
        # DEFAULT
        # =====================================================

        else:

            result.workflow = (
                "general_workflow"
            )

            result.strategy = (
                "balanced_strategy"
            )

            result.pipeline = (
                "default_pipeline"
            )

            result.add_reasoning(
                "General workflow selected"
            )

    # =========================================================
    # INTENT
    # =========================================================

    def _route_by_intent(
        self,
        result: DecisionRouteResult,
        intent: str,
    ) -> None:

        # =====================================================
        # TRANSACTIONAL
        # =====================================================

        if intent == "transactional":

            result.snippet_strategy_enabled = (
                True
            )

            result.faq_strategy_enabled = (
                True
            )

            result.ranking_priority = (
                "high"
            )

            result.add_reasoning(
                "Transactional intent optimization enabled"
            )

        # =====================================================
        # INFORMATIONAL
        # =====================================================

        elif intent == "informational":

            result.authority_strategy_enabled = (
                True
            )

            result.add_reasoning(
                "Authority-focused informational strategy enabled"
            )

        # =====================================================
        # COMPARISON
        # =====================================================

        elif intent == "comparison":

            result.faq_strategy_enabled = (
                True
            )

            result.snippet_strategy_enabled = (
                True
            )

            result.add_reasoning(
                "Comparison SERP strategy enabled"
            )

    # =========================================================
    # YMYL
    # =========================================================

    def _apply_ymyl_strategy(
        self,
        result: DecisionRouteResult,
    ) -> None:

        result.human_review_required = (
            True
        )

        result.expert_review_required = (
            True
        )

        result.aggressive_verification_required = (
            True
        )

        result.verification_priority = (
            "critical"
        )

        result.authority_priority = (
            "critical"
        )

        result.add_warning(
            "YMYL workflow protections enabled"
        )

    # =========================================================
    # FRESHNESS
    # =========================================================

    def _apply_freshness_strategy(
        self,
        result: DecisionRouteResult,
    ) -> None:

        result.freshness_priority = (
            "critical"
        )

        result.freshness_monitoring_required = (
            True
        )

        result.auto_refresh_enabled = (
            True
        )

        result.realtime_verification_enabled = (
            True
        )

        result.add_reasoning(
            "Freshness-sensitive workflow enabled"
        )

    # =========================================================
    # TOPIC SIGNALS
    # =========================================================

    def _analyze_topic_signals(
        self,
        result: DecisionRouteResult,
        topic: str,
    ) -> None:

        freshness_keywords = [

            "latest",
            "today",
            "result",
            "notification",
            "update",
            "breaking",
        ]

        if any(
            keyword in topic
            for keyword in freshness_keywords
        ):

            result.freshness_strategy_enabled = (
                True
            )

            result.auto_refresh_enabled = (
                True
            )

            result.add_reasoning(
                "Freshness-sensitive topic detected"
            )

        # =====================================================
        # SNIPPET
        # =====================================================

        snippet_keywords = [

            "how to",
            "best",
            "top",
            "guide",
            "vs",
        ]

        if any(
            keyword in topic
            for keyword in snippet_keywords
        ):

            result.snippet_strategy_enabled = (
                True
            )

            result.faq_strategy_enabled = (
                True
            )

            result.add_reasoning(
                "Featured snippet optimization opportunity detected"
            )

    # =========================================================
    # FINALIZE
    # =========================================================

    def _finalize_workflow(
        self,
        result: DecisionRouteResult,
    ) -> None:

        # =====================================================
        # RECOMMENDATIONS
        # =====================================================

        if result.freshness_priority == "critical":

            result.add_recommendation(
                "Enable aggressive freshness monitoring"
            )

        if result.verification_priority == "critical":

            result.add_recommendation(
                "Use official authority sources only"
            )

        if result.snippet_strategy_enabled:

            result.add_recommendation(
                "Optimize content for featured snippets"
            )

        if result.faq_strategy_enabled:

            result.add_recommendation(
                "Add FAQ schema optimization"
            )

    # =========================================================
    # EXPORT
    # =========================================================

    def export(
        self,
        result: DecisionRouteResult,
    ) -> Dict[str, Any]:

        return {

            "workflow": (
                result.workflow
            ),

            "strategy": (
                result.strategy
            ),

            "pipeline": (
                result.pipeline
            ),

            "freshness_priority": (
                result.freshness_priority
            ),

            "verification_priority": (
                result.verification_priority
            ),

            "authority_priority": (
                result.authority_priority
            ),

            "ranking_priority": (
                result.ranking_priority
            ),

            "human_review_required": (
                result.human_review_required
            ),

            "aggressive_verification_required": (
                result.aggressive_verification_required
            ),

            "freshness_monitoring_required": (
                result.freshness_monitoring_required
            ),

            "expert_review_required": (
                result.expert_review_required
            ),

            "realtime_verification_enabled": (
                result.realtime_verification_enabled
            ),

            "auto_refresh_enabled": (
                result.auto_refresh_enabled
            ),

            "ranking_tracking_enabled": (
                result.ranking_tracking_enabled
            ),

            "serp_monitoring_enabled": (
                result.serp_monitoring_enabled
            ),

            "faq_strategy_enabled": (
                result.faq_strategy_enabled
            ),

            "snippet_strategy_enabled": (
                result.snippet_strategy_enabled
            ),

            "authority_strategy_enabled": (
                result.authority_strategy_enabled
            ),

            "freshness_strategy_enabled": (
                result.freshness_strategy_enabled
            ),

            "routing_signals": (
                result.routing_signals
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