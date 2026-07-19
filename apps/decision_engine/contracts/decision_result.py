"""
Decision Result Contract

Final orchestration result returned by the
decision engine.

This object represents:
- final publish decision
- confidence
- reasoning
- scoring
- strategy outputs
- verification outcomes

Goal:
Provide a single structured response
from the decision engine pipeline.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional


# =============================================================
# DECISION RESULT
# =============================================================

@dataclass
class DecisionResult:

    # =========================================================
    # FINAL DECISION
    # =========================================================

    decision: str = "review"

    publishing_allowed: bool = False

    requires_human_review: bool = False

    # =========================================================
    # CONFIDENCE
    # =========================================================

    confidence_score: float = 0.0

    confidence_level: str = "medium"

    # =========================================================
    # SCORING
    # =========================================================

    seo_score: float = 0.0

    quality_score: float = 0.0

    freshness_score: float = 0.0

    authority_score: float = 0.0

    trust_score: float = 0.0

    verification_score: float = 0.0

    overall_score: float = 0.0

    # =========================================================
    # PREDICTIONS
    # =========================================================

    ranking_probability: float = 0.0

    estimated_traffic: int = 0

    estimated_position: Optional[int] = None

    # =========================================================
    # STRATEGY OUTPUT
    # =========================================================

    article_depth: str = "medium"

    faq_enabled: bool = False

    tables_enabled: bool = False

    comparison_enabled: bool = False

    citations_required: bool = False

    expert_tone_required: bool = False

    official_sources_required: bool = False

    # =========================================================
    # VERIFICATION
    # =========================================================

    verified: bool = False

    freshness_verified: bool = False

    claims_verified: bool = False

    source_trust_verified: bool = False

    # =========================================================
    # REASONING
    # =========================================================

    reasoning: List[str] = field(
        default_factory=list
    )

    applied_rules: List[str] = field(
        default_factory=list
    )

    warnings: List[str] = field(
        default_factory=list
    )

    recommendations: List[str] = field(
        default_factory=list
    )

    # =========================================================
    # ADAPTIVE OUTPUTS
    # =========================================================

    adaptive_weights: Dict[str, float] = field(
        default_factory=dict
    )

    adaptive_rules: Dict[str, Any] = field(
        default_factory=dict
    )

    # =========================================================
    # STRATEGY SIGNALS
    # =========================================================

    strategy_signals: Dict[str, Any] = field(
        default_factory=dict
    )

    # =========================================================
    # VERIFICATION DETAILS
    # =========================================================

    verified_sources: List[str] = field(
        default_factory=list
    )

    rejected_sources: List[str] = field(
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

    def add_applied_rule(
        self,
        rule_name: str,
    ) -> None:

        if (
            rule_name
            and rule_name
            not in self.applied_rules
        ):

            self.applied_rules.append(
                rule_name
            )

    # =========================================================
    # CONFIDENCE EVALUATION
    # =========================================================

    def evaluate_confidence_level(
        self,
    ) -> None:

        if self.confidence_score >= 0.85:

            self.confidence_level = "very_high"

        elif self.confidence_score >= 0.70:

            self.confidence_level = "high"

        elif self.confidence_score >= 0.50:

            self.confidence_level = "medium"

        else:

            self.confidence_level = "low"

    # =========================================================
    # FINALIZE
    # =========================================================

    def finalize(
        self,
    ) -> None:

        self.evaluate_confidence_level()

        if (
            self.confidence_score >= 0.75
            and self.verification_score >= 0.70
            and self.quality_score >= 0.70
        ):

            self.publishing_allowed = True

            self.decision = "publish"

        elif self.requires_human_review:

            self.decision = "review"

            self.publishing_allowed = False

        else:

            self.decision = "rewrite"

            self.publishing_allowed = False

    # =========================================================
    # EXPORT
    # =========================================================

    def to_dict(
        self,
    ) -> Dict[str, Any]:

        return {

            # =================================================
            # DECISION
            # =================================================

            "decision": self.decision,

            "publishing_allowed": (
                self.publishing_allowed
            ),

            "requires_human_review": (
                self.requires_human_review
            ),

            # =================================================
            # CONFIDENCE
            # =================================================

            "confidence_score": (
                self.confidence_score
            ),

            "confidence_level": (
                self.confidence_level
            ),

            # =================================================
            # SCORES
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

            "overall_score": (
                self.overall_score
            ),

            # =================================================
            # PREDICTIONS
            # =================================================

            "ranking_probability": (
                self.ranking_probability
            ),

            "estimated_traffic": (
                self.estimated_traffic
            ),

            "estimated_position": (
                self.estimated_position
            ),

            # =================================================
            # STRATEGY
            # =================================================

            "article_depth": (
                self.article_depth
            ),

            "faq_enabled": (
                self.faq_enabled
            ),

            "tables_enabled": (
                self.tables_enabled
            ),

            "comparison_enabled": (
                self.comparison_enabled
            ),

            "citations_required": (
                self.citations_required
            ),

            "expert_tone_required": (
                self.expert_tone_required
            ),

            "official_sources_required": (
                self.official_sources_required
            ),

            # =================================================
            # VERIFICATION
            # =================================================

            "verified": self.verified,

            "freshness_verified": (
                self.freshness_verified
            ),

            "claims_verified": (
                self.claims_verified
            ),

            "source_trust_verified": (
                self.source_trust_verified
            ),

            # =================================================
            # REASONING
            # =================================================

            "reasoning": self.reasoning,

            "applied_rules": (
                self.applied_rules
            ),

            "warnings": self.warnings,

            "recommendations": (
                self.recommendations
            ),

            # =================================================
            # ADAPTIVE
            # =================================================

            "adaptive_weights": (
                self.adaptive_weights
            ),

            "adaptive_rules": (
                self.adaptive_rules
            ),

            # =================================================
            # STRATEGY SIGNALS
            # =================================================

            "strategy_signals": (
                self.strategy_signals
            ),

            # =================================================
            # VERIFICATION DETAILS
            # =================================================

            "verified_sources": (
                self.verified_sources
            ),

            "rejected_sources": (
                self.rejected_sources
            ),

            # =================================================
            # META
            # =================================================

            "metadata": self.metadata,
        }