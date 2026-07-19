"""
Event: Freshness Expired

Triggered when article freshness validity expires.

Purpose:
- detect outdated content
- trigger update workflows
- initiate re-verification
- monitor freshness decay
- feed freshness learning system

Critical for:
- jobs
- news
- finance
- tech updates
- rapidly changing topics
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Any, List


# =============================================================
# EVENT
# =============================================================

@dataclass
class FreshnessExpiredEvent:

    # =========================================================
    # ARTICLE
    # =========================================================

    article_id: str

    title: str

    keyword: str

    niche: str

    url: str

    # =========================================================
    # FRESHNESS STATUS
    # =========================================================

    freshness_expired: bool = True

    freshness_score: float = 0.0

    freshness_required: bool = False

    freshness_severity: str = "medium"

    # =========================================================
    # CONTENT AGE
    # =========================================================

    published_at: datetime = field(
        default_factory=datetime.utcnow
    )

    expired_at: datetime = field(
        default_factory=datetime.utcnow
    )

    content_age_days: int = 0

    max_age_days: int = 30

    # =========================================================
    # OUTDATED SIGNALS
    # =========================================================

    outdated_information_detected: bool = False

    outdated_dates_detected: bool = False

    outdated_links_detected: bool = False

    outdated_statistics_detected: bool = False

    outdated_requirements_detected: bool = False

    # =========================================================
    # UPDATE REQUIREMENTS
    # =========================================================

    update_required: bool = True

    rewrite_required: bool = False

    reverification_required: bool = True

    manual_review_required: bool = False

    # =========================================================
    # FRESHNESS IMPACT
    # =========================================================

    ranking_decay_detected: bool = False

    traffic_decay_detected: bool = False

    trust_decay_detected: bool = False

    # =========================================================
    # CONTEXT
    # =========================================================

    competition_level: str = "medium"

    intent: str = "informational"

    article_type: str = "general"

    semantic_type: str = "general"

    # =========================================================
    # UPDATE PRIORITY
    # =========================================================

    update_priority: str = "medium"

    update_deadline_hours: int = 24

    # =========================================================
    # LEARNING SIGNALS
    # =========================================================

    adaptive_learning_enabled: bool = True

    freshness_learning_enabled: bool = True

    affected_weights: Dict[str, float] = field(
        default_factory=dict
    )

    applied_rules: List[str] = field(
        default_factory=list
    )

    # =========================================================
    # RECOMMENDED ACTIONS
    # =========================================================

    recommended_actions: List[str] = field(
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

    def set_weight_adjustment(
        self,
        key: str,
        value: float,
    ) -> None:

        self.affected_weights[key] = value

    # =========================================================
    # EVALUATION
    # =========================================================

    def evaluate(
        self,
    ) -> None:

        # =====================================================
        # HIGH PRIORITY FRESHNESS
        # =====================================================

        if (
            self.niche in [
                "jobs",
                "news",
                "finance",
            ]
        ):

            self.update_priority = "high"

            self.update_deadline_hours = 6

            self.add_action(
                "Immediate content update required"
            )

        # =====================================================
        # OUTDATED DATA
        # =====================================================

        if (
            self.outdated_information_detected
        ):

            self.rewrite_required = True

            self.add_warning(
                "Outdated information detected"
            )

        # =====================================================
        # RANKING DECAY
        # =====================================================

        if (
            self.ranking_decay_detected
        ):

            self.add_action(
                "Re-optimize SEO structure"
            )

        # =====================================================
        # TRAFFIC DECAY
        # =====================================================

        if (
            self.traffic_decay_detected
        ):

            self.add_action(
                "Refresh title and metadata"
            )

        # =====================================================
        # TRUST DECAY
        # =====================================================

        if (
            self.trust_decay_detected
        ):

            self.manual_review_required = True

            self.add_warning(
                "Trust degradation detected"
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

            "url": self.url,

            # =================================================
            # FRESHNESS
            # =================================================

            "freshness_expired": (
                self.freshness_expired
            ),

            "freshness_score": (
                self.freshness_score
            ),

            "freshness_required": (
                self.freshness_required
            ),

            "freshness_severity": (
                self.freshness_severity
            ),

            # =================================================
            # AGE
            # =================================================

            "published_at": (
                self.published_at.isoformat()
            ),

            "expired_at": (
                self.expired_at.isoformat()
            ),

            "content_age_days": (
                self.content_age_days
            ),

            "max_age_days": (
                self.max_age_days
            ),

            # =================================================
            # OUTDATED
            # =================================================

            "outdated_information_detected": (
                self.outdated_information_detected
            ),

            "outdated_dates_detected": (
                self.outdated_dates_detected
            ),

            "outdated_links_detected": (
                self.outdated_links_detected
            ),

            "outdated_statistics_detected": (
                self.outdated_statistics_detected
            ),

            "outdated_requirements_detected": (
                self.outdated_requirements_detected
            ),

            # =================================================
            # UPDATE
            # =================================================

            "update_required": (
                self.update_required
            ),

            "rewrite_required": (
                self.rewrite_required
            ),

            "reverification_required": (
                self.reverification_required
            ),

            "manual_review_required": (
                self.manual_review_required
            ),

            # =================================================
            # IMPACT
            # =================================================

            "ranking_decay_detected": (
                self.ranking_decay_detected
            ),

            "traffic_decay_detected": (
                self.traffic_decay_detected
            ),

            "trust_decay_detected": (
                self.trust_decay_detected
            ),

            # =================================================
            # CONTEXT
            # =================================================

            "competition_level": (
                self.competition_level
            ),

            "intent": self.intent,

            "article_type": (
                self.article_type
            ),

            "semantic_type": (
                self.semantic_type
            ),

            # =================================================
            # PRIORITY
            # =================================================

            "update_priority": (
                self.update_priority
            ),

            "update_deadline_hours": (
                self.update_deadline_hours
            ),

            # =================================================
            # LEARNING
            # =================================================

            "adaptive_learning_enabled": (
                self.adaptive_learning_enabled
            ),

            "freshness_learning_enabled": (
                self.freshness_learning_enabled
            ),

            "affected_weights": (
                self.affected_weights
            ),

            "applied_rules": (
                self.applied_rules
            ),

            # =================================================
            # ACTIONS
            # =================================================

            "recommended_actions": (
                self.recommended_actions
            ),

            # =================================================
            # REASONING
            # =================================================

            "reasoning": self.reasoning,

            "warnings": self.warnings,

            # =================================================
            # META
            # =================================================

            "metadata": self.metadata,
        }