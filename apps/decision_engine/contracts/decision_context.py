"""
Decision Context Contract

Central intelligence state object for the entire
decision engine ecosystem.

This contract is shared across:
- context layer
- adaptive layer
- strategy engine
- verification engine
- scoring engine
- reasoning engine
- prediction engine

Goal:
Provide ONE unified source of truth.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional


# =============================================================
# DECISION CONTEXT
# =============================================================

@dataclass
class DecisionContext:

    # =========================================================
    # CORE INPUT
    # =========================================================

    topic: str

    keyword: str = ""

    niche: str = "default"

    # =========================================================
    # ARTICLE CLASSIFICATION
    # =========================================================

    article_type: str = "general"

    semantic_type: str = "general"

    intent: str = "informational"

    # =========================================================
    # FRESHNESS
    # =========================================================

    freshness_required: bool = False

    freshness_sensitive: bool = False

    update_frequency: str = "weekly"

    max_age_days: int = 30

    live_verification_required: bool = False

    # =========================================================
    # AUTHORITY
    # =========================================================

    authority_required: bool = False

    official_sources_required: bool = False

    verification_strictness: str = "medium"

    trust_level: str = "medium"

    ymyl_sensitive: bool = False

    # =========================================================
    # COMPETITION
    # =========================================================

    competition_level: str = "medium"

    authority_gap: float = 0.0

    semantic_gap: float = 0.0

    backlink_pressure: float = 0.0

    content_depth_required: str = "medium"

    # =========================================================
    # SERP SIGNALS
    # =========================================================

    faq_dominant: bool = False

    tables_common: bool = False

    video_heavy: bool = False

    featured_snippet: bool = False

    freshness_dominant: bool = False

    authority_sites_dominant: bool = False

    forum_results_present: bool = False

    ecommerce_dominant: bool = False

    serp_complexity_score: float = 50.0

    # =========================================================
    # CONTENT REQUIREMENTS
    # =========================================================

    faq_required: bool = False

    tables_required: bool = False

    comparison_required: bool = False

    expert_tone_required: bool = False

    citations_required: bool = False

    step_by_step_required: bool = False

    # =========================================================
    # SOURCE INTELLIGENCE
    # =========================================================

    preferred_sources: List[str] = field(
        default_factory=list
    )

    restricted_sources: List[str] = field(
        default_factory=list
    )

    # =========================================================
    # ADAPTIVE SIGNALS
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
    # PREDICTION SIGNALS
    # =========================================================

    ranking_probability: float = 0.0

    estimated_traffic: int = 0

    confidence_score: float = 0.0

    # =========================================================
    # VERIFICATION SIGNALS
    # =========================================================

    verification_score: float = 0.0

    trust_score: float = 0.0

    freshness_score: float = 0.0

    # =========================================================
    # METADATA
    # =========================================================

    metadata: Dict[str, Any] = field(
        default_factory=dict
    )

    # =========================================================
    # NOTES
    # =========================================================

    notes: List[str] = field(
        default_factory=list
    )

    # =========================================================
    # FLAGS
    # =========================================================

    requires_human_review: bool = False

    publishing_allowed: bool = True

    # =========================================================
    # UTILITIES
    # =========================================================

    def add_note(
        self,
        note: str,
    ) -> None:

        if note and note not in self.notes:

            self.notes.append(note)

    def set_adaptive_weight(
        self,
        key: str,
        value: float,
    ) -> None:

        self.adaptive_weights[key] = value

    def set_adaptive_rule(
        self,
        key: str,
        value: Any,
    ) -> None:

        self.adaptive_rules[key] = value

    def set_strategy_signal(
        self,
        key: str,
        value: Any,
    ) -> None:

        self.strategy_signals[key] = value

    # =========================================================
    # EXPORT
    # =========================================================

    def to_dict(
        self,
    ) -> Dict[str, Any]:

        return {

            # =================================================
            # CORE
            # =================================================

            "topic": self.topic,
            "keyword": self.keyword,
            "niche": self.niche,

            # =================================================
            # CLASSIFICATION
            # =================================================

            "article_type": self.article_type,
            "semantic_type": self.semantic_type,
            "intent": self.intent,

            # =================================================
            # FRESHNESS
            # =================================================

            "freshness_required": (
                self.freshness_required
            ),

            "freshness_sensitive": (
                self.freshness_sensitive
            ),

            "update_frequency": (
                self.update_frequency
            ),

            "max_age_days": (
                self.max_age_days
            ),

            "live_verification_required": (
                self.live_verification_required
            ),

            # =================================================
            # AUTHORITY
            # =================================================

            "authority_required": (
                self.authority_required
            ),

            "official_sources_required": (
                self.official_sources_required
            ),

            "verification_strictness": (
                self.verification_strictness
            ),

            "trust_level": (
                self.trust_level
            ),

            "ymyl_sensitive": (
                self.ymyl_sensitive
            ),

            # =================================================
            # COMPETITION
            # =================================================

            "competition_level": (
                self.competition_level
            ),

            "authority_gap": (
                self.authority_gap
            ),

            "semantic_gap": (
                self.semantic_gap
            ),

            "backlink_pressure": (
                self.backlink_pressure
            ),

            "content_depth_required": (
                self.content_depth_required
            ),

            # =================================================
            # SERP
            # =================================================

            "faq_dominant": (
                self.faq_dominant
            ),

            "tables_common": (
                self.tables_common
            ),

            "video_heavy": (
                self.video_heavy
            ),

            "featured_snippet": (
                self.featured_snippet
            ),

            "freshness_dominant": (
                self.freshness_dominant
            ),

            "authority_sites_dominant": (
                self.authority_sites_dominant
            ),

            "forum_results_present": (
                self.forum_results_present
            ),

            "ecommerce_dominant": (
                self.ecommerce_dominant
            ),

            "serp_complexity_score": (
                self.serp_complexity_score
            ),

            # =================================================
            # CONTENT
            # =================================================

            "faq_required": (
                self.faq_required
            ),

            "tables_required": (
                self.tables_required
            ),

            "comparison_required": (
                self.comparison_required
            ),

            "expert_tone_required": (
                self.expert_tone_required
            ),

            "citations_required": (
                self.citations_required
            ),

            "step_by_step_required": (
                self.step_by_step_required
            ),

            # =================================================
            # SOURCES
            # =================================================

            "preferred_sources": (
                self.preferred_sources
            ),

            "restricted_sources": (
                self.restricted_sources
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
            # STRATEGY
            # =================================================

            "strategy_signals": (
                self.strategy_signals
            ),

            # =================================================
            # PREDICTION
            # =================================================

            "ranking_probability": (
                self.ranking_probability
            ),

            "estimated_traffic": (
                self.estimated_traffic
            ),

            "confidence_score": (
                self.confidence_score
            ),

            # =================================================
            # VERIFICATION
            # =================================================

            "verification_score": (
                self.verification_score
            ),

            "trust_score": (
                self.trust_score
            ),

            "freshness_score": (
                self.freshness_score
            ),

            # =================================================
            # META
            # =================================================

            "metadata": self.metadata,

            "notes": self.notes,

            "requires_human_review": (
                self.requires_human_review
            ),

            "publishing_allowed": (
                self.publishing_allowed
            ),
        }