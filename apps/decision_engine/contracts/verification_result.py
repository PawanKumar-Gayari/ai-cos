"""
Verification Result Contract

This module represents the output of the
verification engine.

Goal:
Centralize:
- fact verification
- freshness validation
- source trust analysis
- authority validation
- hallucination detection

This becomes the trust layer of the system.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List


# =============================================================
# VERIFICATION RESULT
# =============================================================

@dataclass
class VerificationResult:

    # =========================================================
    # OVERALL STATUS
    # =========================================================

    verified: bool = False

    verification_score: float = 0.0

    trust_score: float = 0.0

    freshness_score: float = 0.0

    authority_score: float = 0.0

    # =========================================================
    # FACT VALIDATION
    # =========================================================

    claims_verified: bool = False

    factual_accuracy_score: float = 0.0

    hallucination_risk: str = "low"

    unsupported_claims_count: int = 0

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

    content_age_days: int = 0

    freshness_required: bool = False

    outdated_information_detected: bool = False

    # =========================================================
    # AUTHORITY
    # =========================================================

    authority_verified: bool = False

    ymyl_compliance: bool = False

    expert_review_required: bool = False

    citation_coverage_score: float = 0.0

    # =========================================================
    # SAFETY FLAGS
    # =========================================================

    human_review_required: bool = False

    publishing_allowed: bool = True

    rewrite_required: bool = False

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
    # VERIFICATION DETAILS
    # =========================================================

    verification_breakdown: Dict[str, Any] = field(
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

    def add_verified_source(
        self,
        source: str,
    ) -> None:

        if (
            source
            and source not in self.verified_sources
        ):

            self.verified_sources.append(
                source
            )

    def add_rejected_source(
        self,
        source: str,
    ) -> None:

        if (
            source
            and source not in self.rejected_sources
        ):

            self.rejected_sources.append(
                source
            )

    def add_weak_source(
        self,
        source: str,
    ) -> None:

        if (
            source
            and source not in self.weak_sources
        ):

            self.weak_sources.append(
                source
            )

    def set_breakdown(
        self,
        key: str,
        value: Any,
    ) -> None:

        self.verification_breakdown[
            key
        ] = value

    # =========================================================
    # EVALUATION
    # =========================================================

    def evaluate(
        self,
    ) -> None:

        # =====================================================
        # OVERALL VERIFICATION
        # =====================================================

        if (

            self.verification_score >= 70

            and

            self.factual_accuracy_score >= 70

            and

            self.trust_score >= 70
        ):

            self.verified = True

            self.add_reasoning(
                "Verification thresholds satisfied"
            )

        else:

            self.verified = False

            self.rewrite_required = True

            self.add_warning(
                "Verification thresholds not satisfied"
            )

        # =====================================================
        # HALLUCINATION RISK
        # =====================================================

        if (
            self.hallucination_risk == "high"
        ):

            self.human_review_required = True

            self.publishing_allowed = False

            self.add_warning(
                "High hallucination risk detected"
            )

        # =====================================================
        # OUTDATED CONTENT
        # =====================================================

        if (
            self.outdated_information_detected
        ):

            self.rewrite_required = True

            self.add_warning(
                "Outdated information detected"
            )

        # =====================================================
        # YMYL
        # =====================================================

        if (
            self.expert_review_required
            and not self.authority_verified
        ):

            self.human_review_required = True

            self.publishing_allowed = False

            self.add_warning(
                "Expert authority verification required"
            )

        # =====================================================
        # UNSUPPORTED CLAIMS
        # =====================================================

        if (
            self.unsupported_claims_count >= 3
        ):

            self.rewrite_required = True

            self.add_warning(
                "Multiple unsupported claims detected"
            )

    # =========================================================
    # EXPORT
    # =========================================================

    def to_dict(
        self,
    ) -> Dict[str, Any]:

        return {

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

            "freshness_score": (
                self.freshness_score
            ),

            "authority_score": (
                self.authority_score
            ),

            # =================================================
            # FACTS
            # =================================================

            "claims_verified": (
                self.claims_verified
            ),

            "factual_accuracy_score": (
                self.factual_accuracy_score
            ),

            "hallucination_risk": (
                self.hallucination_risk
            ),

            "unsupported_claims_count": (
                self.unsupported_claims_count
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

            "content_age_days": (
                self.content_age_days
            ),

            "freshness_required": (
                self.freshness_required
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

            "ymyl_compliance": (
                self.ymyl_compliance
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

            "human_review_required": (
                self.human_review_required
            ),

            "publishing_allowed": (
                self.publishing_allowed
            ),

            "rewrite_required": (
                self.rewrite_required
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
            # BREAKDOWN
            # =================================================

            "verification_breakdown": (
                self.verification_breakdown
            ),

            # =================================================
            # META
            # =================================================

            "metadata": self.metadata,
        }