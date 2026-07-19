"""
Consensus Engine

Purpose:
Combine intelligence from multiple reasoning
agents and produce the final editorial decision.

Combines:
- authority intelligence
- freshness intelligence
- risk intelligence
- strategy intelligence
- quality intelligence
- SEO intelligence

Goal:
Create multi-agent editorial reasoning.

This becomes the final reasoning brain
of AI_COS.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List


# =============================================================
# CONSENSUS RESULT
# =============================================================

@dataclass
class ConsensusResult:

    # =========================================================
    # FINAL SCORES
    # =========================================================

    final_score: float = 0.0

    confidence_score: float = 0.0

    publish_score: float = 0.0

    # =========================================================
    # FINAL DECISION
    # =========================================================

    final_decision: str = "review"

    publish_allowed: bool = False

    rewrite_required: bool = False

    human_review_required: bool = False

    verification_required: bool = False

    # =========================================================
    # AGENT SCORES
    # =========================================================

    authority_score: float = 0.0

    freshness_score: float = 0.0

    risk_score: float = 0.0

    strategy_score: float = 0.0

    seo_score: float = 0.0

    quality_score: float = 0.0

    # =========================================================
    # CONSENSUS
    # =========================================================

    consensus_strength: str = "medium"

    agent_agreement_score: float = 0.0

    conflicting_signals_detected: bool = False

    # =========================================================
    # RISKS
    # =========================================================

    overall_risk: str = "low"

    ranking_risk: str = "low"

    misinformation_risk: str = "low"

    freshness_risk: str = "low"

    # =========================================================
    # PRIORITIES
    # =========================================================

    freshness_priority: str = "medium"

    authority_priority: str = "medium"

    ranking_priority: str = "medium"

    # =========================================================
    # AGENT DECISIONS
    # =========================================================

    agent_decisions: Dict[str, Any] = field(
        default_factory=dict
    )

    # =========================================================
    # SIGNALS
    # =========================================================

    consensus_signals: Dict[str, Any] = field(
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
# CONSENSUS ENGINE
# =============================================================

class ConsensusEngine:

    """
    Multi-agent reasoning fusion engine.
    """

    # =========================================================
    # AGENT WEIGHTS
    # =========================================================

    DEFAULT_WEIGHTS = {

        "authority": 0.25,

        "freshness": 0.20,

        "risk": 0.25,

        "strategy": 0.15,

        "seo": 0.10,

        "quality": 0.05,
    }

    # =========================================================
    # ANALYZE
    # =========================================================

    def analyze(
        self,
        authority_result=None,
        freshness_result=None,
        risk_result=None,
        strategy_result=None,
        seo_result=None,
        quality_result=None,
    ) -> ConsensusResult:

        result = ConsensusResult()

        # =====================================================
        # STORE SCORES
        # =====================================================

        result.authority_score = getattr(

            authority_result,
            "authority_score",
            50.0,
        )

        result.freshness_score = getattr(

            freshness_result,
            "freshness_score",
            50.0,
        )

        result.risk_score = 100 - getattr(

            risk_result,
            "risk_score",
            50.0,
        )

        result.strategy_score = getattr(

            strategy_result,
            "strategy_score",
            50.0,
        )

        result.seo_score = getattr(

            seo_result,
            "seo_score",
            50.0,
        )

        result.quality_score = getattr(

            quality_result,
            "quality_score",
            50.0,
        )

        # =====================================================
        # AGENT DECISIONS
        # =====================================================

        self._collect_agent_decisions(

            result,

            authority_result,

            freshness_result,

            risk_result,

            strategy_result,

            seo_result,

            quality_result,
        )

        # =====================================================
        # CONSENSUS
        # =====================================================

        self._calculate_consensus(
            result
        )

        # =====================================================
        # CONFLICTS
        # =====================================================

        self._detect_conflicts(
            result
        )

        # =====================================================
        # RISK
        # =====================================================

        self._analyze_risks(
            result,

            authority_result,

            freshness_result,

            risk_result,
        )

        # =====================================================
        # FINAL SCORE
        # =====================================================

        self._calculate_final_score(
            result
        )

        # =====================================================
        # FINAL DECISION
        # =====================================================

        self._final_decision(
            result,

            risk_result,

            freshness_result,
        )

        # =====================================================
        # RECOMMENDATIONS
        # =====================================================

        self._generate_recommendations(
            result
        )

        return result

    # =========================================================
    # AGENT DECISIONS
    # =========================================================

    def _collect_agent_decisions(
        self,
        result: ConsensusResult,
        authority_result,
        freshness_result,
        risk_result,
        strategy_result,
        seo_result,
        quality_result,
    ) -> None:

        result.agent_decisions = {

            "authority": {

                "score": result.authority_score,
            },

            "freshness": {

                "score": result.freshness_score,
            },

            "risk": {

                "score": result.risk_score,
            },

            "strategy": {

                "score": result.strategy_score,
            },

            "seo": {

                "score": result.seo_score,
            },

            "quality": {

                "score": result.quality_score,
            },
        }

        result.add_reasoning(
            "Collected intelligence from all agents"
        )

    # =========================================================
    # CONSENSUS
    # =========================================================

    def _calculate_consensus(
        self,
        result: ConsensusResult,
    ) -> None:

        scores = [

            result.authority_score,

            result.freshness_score,

            result.risk_score,

            result.strategy_score,

            result.seo_score,

            result.quality_score,
        ]

        spread = (
            max(scores) - min(scores)
        )

        # =====================================================
        # AGREEMENT
        # =====================================================

        agreement = max(
            100 - spread,
            0,
        )

        result.agent_agreement_score = round(

            agreement,

            2,
        )

        # =====================================================
        # STRENGTH
        # =====================================================

        if agreement >= 80:

            result.consensus_strength = (
                "strong"
            )

        elif agreement >= 55:

            result.consensus_strength = (
                "medium"
            )

        else:

            result.consensus_strength = (
                "weak"
            )

        result.add_reasoning(
            f"Consensus strength: "
            f"{result.consensus_strength}"
        )

    # =========================================================
    # CONFLICTS
    # =========================================================

    def _detect_conflicts(
        self,
        result: ConsensusResult,
    ) -> None:

        # =====================================================
        # HIGH SEO + HIGH RISK
        # =====================================================

        if (

            result.seo_score >= 80

            and

            result.risk_score <= 40
        ):

            result.conflicting_signals_detected = (
                True
            )

            result.add_warning(
                "SEO strong but safety risk detected"
            )

        # =====================================================
        # HIGH STRATEGY + LOW AUTHORITY
        # =====================================================

        if (

            result.strategy_score >= 80

            and

            result.authority_score <= 40
        ):

            result.conflicting_signals_detected = (
                True
            )

            result.add_warning(
                "Ranking opportunity detected but authority weak"
            )

    # =========================================================
    # RISKS
    # =========================================================

    def _analyze_risks(
        self,
        result: ConsensusResult,
        authority_result,
        freshness_result,
        risk_result,
    ) -> None:

        # =====================================================
        # MISINFORMATION
        # =====================================================

        if getattr(

            risk_result,
            "hallucination_detected",
            False,
        ):

            result.misinformation_risk = (
                "high"
            )

        # =====================================================
        # FRESHNESS
        # =====================================================

        if getattr(

            freshness_result,
            "freshness_expired",
            False,
        ):

            result.freshness_risk = (
                "high"
            )

        # =====================================================
        # OVERALL
        # =====================================================

        if (

            result.misinformation_risk == "high"

            or

            result.freshness_risk == "high"
        ):

            result.overall_risk = (
                "high"
            )

        else:

            result.overall_risk = (
                "low"
            )

    # =========================================================
    # FINAL SCORE
    # =========================================================

    def _calculate_final_score(
        self,
        result: ConsensusResult,
    ) -> None:

        weights = self.DEFAULT_WEIGHTS

        final = (

            result.authority_score *
            weights["authority"]

            +

            result.freshness_score *
            weights["freshness"]

            +

            result.risk_score *
            weights["risk"]

            +

            result.strategy_score *
            weights["strategy"]

            +

            result.seo_score *
            weights["seo"]

            +

            result.quality_score *
            weights["quality"]
        )

        result.final_score = round(
            final,
            2,
        )

        result.publish_score = round(
            final,
            2,
        )

        result.confidence_score = round(

            (
                result.final_score +

                result.agent_agreement_score
            ) / 2,

            2,
        )

        result.add_reasoning(
            f"Final consensus score: "
            f"{result.final_score}"
        )

    # =========================================================
    # FINAL DECISION
    # =========================================================

    def _final_decision(
        self,
        result: ConsensusResult,
        risk_result,
        freshness_result,
    ) -> None:

        # =====================================================
        # BLOCKERS
        # =====================================================

        if getattr(

            risk_result,
            "hallucination_detected",
            False,
        ):

            result.final_decision = (
                "verification_required"
            )

            result.publish_allowed = (
                False
            )

            result.verification_required = (
                True
            )

            result.add_warning(
                "Hallucination detected"
            )

            return

        # =====================================================
        # FRESHNESS
        # =====================================================

        if getattr(

            freshness_result,
            "freshness_expired",
            False,
        ):

            result.final_decision = (
                "update_required"
            )

            result.publish_allowed = (
                False
            )

            result.rewrite_required = (
                True
            )

            result.add_warning(
                "Freshness expired"
            )

            return

        # =====================================================
        # FINAL SCORE
        # =====================================================

        if result.final_score >= 85:

            result.final_decision = (
                "publish"
            )

            result.publish_allowed = (
                True
            )

        elif result.final_score >= 65:

            result.final_decision = (
                "review"
            )

            result.publish_allowed = (
                False
            )

            result.human_review_required = (
                True
            )

        else:

            result.final_decision = (
                "rewrite"
            )

            result.publish_allowed = (
                False
            )

            result.rewrite_required = (
                True
            )

    # =========================================================
    # RECOMMENDATIONS
    # =========================================================

    def _generate_recommendations(
        self,
        result: ConsensusResult,
    ) -> None:

        # =====================================================
        # AUTHORITY
        # =====================================================

        if result.authority_score < 60:

            result.add_recommendation(
                "Improve authority sources"
            )

            result.add_action(
                "Add official citations"
            )

        # =====================================================
        # FRESHNESS
        # =====================================================

        if result.freshness_score < 60:

            result.add_recommendation(
                "Refresh outdated information"
            )

            result.add_action(
                "Update article with latest data"
            )

        # =====================================================
        # RISK
        # =====================================================

        if result.risk_score < 60:

            result.add_recommendation(
                "Reduce misinformation risk"
            )

            result.add_action(
                "Verify all claims"
            )

        # =====================================================
        # STRATEGY
        # =====================================================

        if result.strategy_score >= 80:

            result.add_recommendation(
                "Aggressive ranking opportunity detected"
            )

        # =====================================================
        # CONSENSUS
        # =====================================================

        if result.consensus_strength == "weak":

            result.add_warning(
                "Agents show weak consensus"
            )

            result.human_review_required = (
                True
            )

        result.add_reasoning(
            f"Final editorial decision: "
            f"{result.final_decision}"
        )

    # =========================================================
    # EXPORT
    # =========================================================

    def export(
        self,
        result: ConsensusResult,
    ) -> Dict[str, Any]:

        return {

            "final_score": (
                result.final_score
            ),

            "confidence_score": (
                result.confidence_score
            ),

            "publish_score": (
                result.publish_score
            ),

            "final_decision": (
                result.final_decision
            ),

            "publish_allowed": (
                result.publish_allowed
            ),

            "rewrite_required": (
                result.rewrite_required
            ),

            "human_review_required": (
                result.human_review_required
            ),

            "verification_required": (
                result.verification_required
            ),

            "authority_score": (
                result.authority_score
            ),

            "freshness_score": (
                result.freshness_score
            ),

            "risk_score": (
                result.risk_score
            ),

            "strategy_score": (
                result.strategy_score
            ),

            "seo_score": (
                result.seo_score
            ),

            "quality_score": (
                result.quality_score
            ),

            "consensus_strength": (
                result.consensus_strength
            ),

            "agent_agreement_score": (
                result.agent_agreement_score
            ),

            "conflicting_signals_detected": (
                result.conflicting_signals_detected
            ),

            "overall_risk": (
                result.overall_risk
            ),

            "ranking_risk": (
                result.ranking_risk
            ),

            "misinformation_risk": (
                result.misinformation_risk
            ),

            "freshness_risk": (
                result.freshness_risk
            ),

            "freshness_priority": (
                result.freshness_priority
            ),

            "authority_priority": (
                result.authority_priority
            ),

            "ranking_priority": (
                result.ranking_priority
            ),

            "agent_decisions": (
                result.agent_decisions
            ),

            "consensus_signals": (
                result.consensus_signals
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