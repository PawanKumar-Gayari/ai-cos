"""
Event: Feedback Received

Triggered when feedback is received from:
- human editors
- QA reviewers
- SEO reviewers
- users
- engagement systems

Purpose:
- train adaptive intelligence
- improve decision quality
- learn failure patterns
- optimize scoring systems
- evolve editorial behavior

This is a core self-improvement signal.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Any, List


# =============================================================
# EVENT
# =============================================================

@dataclass
class FeedbackReceivedEvent:

    # =========================================================
    # ARTICLE
    # =========================================================

    article_id: str

    title: str

    keyword: str

    niche: str

    # =========================================================
    # FEEDBACK SOURCE
    # =========================================================

    feedback_source: str = "system"

    reviewer_type: str = "human"

    reviewer_id: str = ""

    # =========================================================
    # FEEDBACK TYPE
    # =========================================================

    feedback_type: str = "general"

    severity: str = "medium"

    feedback_score: float = 0.0

    # =========================================================
    # QUALITY SIGNALS
    # =========================================================

    seo_issue_detected: bool = False

    quality_issue_detected: bool = False

    freshness_issue_detected: bool = False

    authority_issue_detected: bool = False

    verification_issue_detected: bool = False

    readability_issue_detected: bool = False

    hallucination_detected: bool = False

    # =========================================================
    # POSITIVE SIGNALS
    # =========================================================

    high_quality_detected: bool = False

    high_engagement_detected: bool = False

    strong_seo_detected: bool = False

    strong_readability_detected: bool = False

    strong_verification_detected: bool = False

    # =========================================================
    # EDITORIAL FEEDBACK
    # =========================================================

    feedback_message: str = ""

    rewrite_reason: str = ""

    improvement_suggestions: List[str] = field(
        default_factory=list
    )

    # =========================================================
    # LEARNING SIGNALS
    # =========================================================

    affected_weights: Dict[str, float] = field(
        default_factory=dict
    )

    affected_rules: List[str] = field(
        default_factory=list
    )

    adaptive_learning_enabled: bool = True

    # =========================================================
    # PERFORMANCE SIGNALS
    # =========================================================

    ctr: float = 0.0

    bounce_rate: float = 0.0

    engagement_score: float = 0.0

    average_time_on_page: float = 0.0

    # =========================================================
    # REVIEW DECISION
    # =========================================================

    publishing_allowed: bool = True

    rewrite_required: bool = False

    human_review_required: bool = False

    # =========================================================
    # TIMESTAMP
    # =========================================================

    received_at: datetime = field(
        default_factory=datetime.utcnow
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

    def add_improvement(
        self,
        suggestion: str,
    ) -> None:

        if (
            suggestion
            and suggestion
            not in self.improvement_suggestions
        ):

            self.improvement_suggestions.append(
                suggestion
            )

    def set_weight_adjustment(
        self,
        key: str,
        value: float,
    ) -> None:

        self.affected_weights[key] = value

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
            # SOURCE
            # =================================================

            "feedback_source": (
                self.feedback_source
            ),

            "reviewer_type": (
                self.reviewer_type
            ),

            "reviewer_id": (
                self.reviewer_id
            ),

            # =================================================
            # FEEDBACK
            # =================================================

            "feedback_type": (
                self.feedback_type
            ),

            "severity": self.severity,

            "feedback_score": (
                self.feedback_score
            ),

            # =================================================
            # ISSUES
            # =================================================

            "seo_issue_detected": (
                self.seo_issue_detected
            ),

            "quality_issue_detected": (
                self.quality_issue_detected
            ),

            "freshness_issue_detected": (
                self.freshness_issue_detected
            ),

            "authority_issue_detected": (
                self.authority_issue_detected
            ),

            "verification_issue_detected": (
                self.verification_issue_detected
            ),

            "readability_issue_detected": (
                self.readability_issue_detected
            ),

            "hallucination_detected": (
                self.hallucination_detected
            ),

            # =================================================
            # POSITIVE
            # =================================================

            "high_quality_detected": (
                self.high_quality_detected
            ),

            "high_engagement_detected": (
                self.high_engagement_detected
            ),

            "strong_seo_detected": (
                self.strong_seo_detected
            ),

            "strong_readability_detected": (
                self.strong_readability_detected
            ),

            "strong_verification_detected": (
                self.strong_verification_detected
            ),

            # =================================================
            # EDITORIAL
            # =================================================

            "feedback_message": (
                self.feedback_message
            ),

            "rewrite_reason": (
                self.rewrite_reason
            ),

            "improvement_suggestions": (
                self.improvement_suggestions
            ),

            # =================================================
            # LEARNING
            # =================================================

            "affected_weights": (
                self.affected_weights
            ),

            "affected_rules": (
                self.affected_rules
            ),

            "adaptive_learning_enabled": (
                self.adaptive_learning_enabled
            ),

            # =================================================
            # PERFORMANCE
            # =================================================

            "ctr": self.ctr,

            "bounce_rate": (
                self.bounce_rate
            ),

            "engagement_score": (
                self.engagement_score
            ),

            "average_time_on_page": (
                self.average_time_on_page
            ),

            # =================================================
            # REVIEW
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
            # TIMESTAMP
            # =================================================

            "received_at": (
                self.received_at.isoformat()
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