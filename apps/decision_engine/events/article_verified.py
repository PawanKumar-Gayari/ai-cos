"""
Event: Article Verified

Triggered after the verification engine completes.

Purpose:
- track verification outcomes
- learn trust patterns
- monitor hallucination risk
- improve source intelligence
- feed adaptive verification learning
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Any, List


# =============================================================
# EVENT
# =============================================================

@dataclass
class ArticleVerifiedEvent:

    # =========================================================
    # ARTICLE
    # =========================================================

    article_id: str

    title: str

    keyword: str

    niche: str

    # =========================================================
    # VERIFICATION STATUS
    # =========================================================

    verified: bool = False

    verification_score: float = 0.0

    trust_score: float = 0.0

    authority_score: float = 0.0

    freshness_score: float = 0.0

    factual_accuracy_score: float = 0.0

    # =========================================================
    # FACT VALIDATION
    # =========================================================

    claims_verified: bool = False

    unsupported_claims_count: int = 0

    hallucination_risk: str = "low"

    # =========================================================
    # SOURCE VALIDATION
    # =========================================================

    official_sources_used: bool = False

    source_trust_verified: bool = False

    verified_sources: List[str] = field(
        default_factory=list
    )

    rejected_sources: List[str] = field(
        default_factory=list
    )

    weak_sources: List[str] = field(
        default_factory=list
    )

    # =========================================================
    # FRESHNESS
    # =========================================================

    freshness_verified: bool = False

    freshness_required: bool = False

    content_age_days: int = 0

    outdated_information_detected: bool = False

    # =========================================================
    # AUTHORITY
    # =========================================================

    authority_verified: bool = False

    ymyl_sensitive: bool = False

    expert_review_required: bool = False

    citation_coverage_score: float = 0.0

    # =========================================================
    # DECISION FLAGS
    # =========================================================

    publishing_allowed: bool = True

    rewrite_required: bool = False

    human_review_required: bool = False

    # =========================================================
    # CONTEXT SIGNALS
    # =========================================================

    intent: str = "informational"

    competition_level: str = "medium"

    verification_strictness: str = "medium"

    # =========================================================
    # LEARNING SIGNALS
    # =========================================================

    adaptive_weights: Dict[str, float] = field(
        default_factory=dict
    )

    applied_rules: List[str] = field(
        default_factory=list
    )

    # =========================================================
    # TIMESTAMP
    # =========================================================

    verified_at: datetime = field(
        default_factory=datetime.utcnow
    )

    verified_by: str = "system"

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

    # =========================================================
    # EXPORT
    # =========================================================

    def to_dict(
        self,
    ) -> Dict[str, Any]:

        return {

            # =================================================
            # ARTICLE
            # =================================================

            "article_id": self.article_id,

            "title": self.title,

            "keyword": self.keyword,

            "niche": self.niche,

            # =================================================
            # STATUS
            # =================================================

            "verified": self.verified,

            "verification_score": (
                self.verification_score
            ),

            "trust_score": (
                self.trust_score
            ),

            "authority_score": (
                self.authority_score
            ),

            "freshness_score": (
                self.freshness_score
            ),

            "factual_accuracy_score": (
                self.factual_accuracy_score
            ),

            # =================================================
            # FACTS
            # =================================================

            "claims_verified": (
                self.claims_verified
            ),

            "unsupported_claims_count": (
                self.unsupported_claims_count
            ),

            "hallucination_risk": (
                self.hallucination_risk
            ),

            # =================================================
            # SOURCES
            # =================================================

            "official_sources_used": (
                self.official_sources_used
            ),

            "source_trust_verified": (
                self.source_trust_verified
            ),

            "verified_sources": (
                self.verified_sources
            ),

            "rejected_sources": (
                self.rejected_sources
            ),

            "weak_sources": (
                self.weak_sources
            ),

            # =================================================
            # FRESHNESS
            # =================================================

            "freshness_verified": (
                self.freshness_verified
            ),

            "freshness_required": (
                self.freshness_required
            ),

            "content_age_days": (
                self.content_age_days
            ),

            "outdated_information_detected": (
                self.outdated_information_detected
            ),

            # =================================================
            # AUTHORITY
            # =================================================

            "authority_verified": (
                self.authority_verified
            ),

            "ymyl_sensitive": (
                self.ymyl_sensitive
            ),

            "expert_review_required": (
                self.expert_review_required
            ),

            "citation_coverage_score": (
                self.citation_coverage_score
            ),

            # =================================================
            # FLAGS
            # =================================================

            "publishing_allowed": (
                self.publishing_allowed
            ),

            "rewrite_required": (
                self.rewrite_required
            ),

            "human_review_required": (
                self.human_review_required
            ),

            # =================================================
            # CONTEXT
            # =================================================

            "intent": self.intent,

            "competition_level": (
                self.competition_level
            ),

            "verification_strictness": (
                self.verification_strictness
            ),

            # =================================================
            # LEARNING
            # =================================================

            "adaptive_weights": (
                self.adaptive_weights
            ),

            "applied_rules": (
                self.applied_rules
            ),

            # =================================================
            # TIMESTAMP
            # =================================================

            "verified_at": (
                self.verified_at.isoformat()
            ),

            "verified_by": (
                self.verified_by
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