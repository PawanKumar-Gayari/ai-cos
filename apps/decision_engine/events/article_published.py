"""
Event: Article Published

Triggered after successful article publishing.

Purpose:
- initialize ranking tracking
- start freshness monitoring
- feed adaptive learning
- capture publish-time intelligence snapshot
- monitor prediction accuracy over time
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Any, List


# =============================================================
# EVENT
# =============================================================

@dataclass
class ArticlePublishedEvent:

    # =========================================================
    # ARTICLE
    # =========================================================

    article_id: str

    title: str

    keyword: str

    niche: str

    url: str

    # =========================================================
    # PUBLISH INFO
    # =========================================================

    published_at: datetime = field(
        default_factory=datetime.utcnow
    )

    published_by: str = "system"

    publishing_allowed: bool = True

    # =========================================================
    # SCORES SNAPSHOT
    # =========================================================

    overall_score: float = 0.0

    seo_score: float = 0.0

    quality_score: float = 0.0

    freshness_score: float = 0.0

    authority_score: float = 0.0

    trust_score: float = 0.0

    verification_score: float = 0.0

    ranking_score: float = 0.0

    # =========================================================
    # PREDICTION SNAPSHOT
    # =========================================================

    predicted_ranking_probability: float = 0.0

    predicted_position: int = 0

    predicted_traffic: int = 0

    predicted_ctr: float = 0.0

    prediction_confidence: float = 0.0

    # =========================================================
    # STRATEGY SNAPSHOT
    # =========================================================

    article_depth: str = "medium"

    faq_enabled: bool = False

    tables_enabled: bool = False

    comparison_enabled: bool = False

    citations_required: bool = False

    expert_tone_used: bool = False

    official_sources_used: bool = False

    # =========================================================
    # CONTEXT SNAPSHOT
    # =========================================================

    intent: str = "informational"

    article_type: str = "general"

    semantic_type: str = "general"

    competition_level: str = "medium"

    freshness_required: bool = False

    authority_required: bool = False

    ymyl_sensitive: bool = False

    # =========================================================
    # SERP SNAPSHOT
    # =========================================================

    featured_snippet_targeted: bool = False

    faq_dominant_serp: bool = False

    video_heavy_serp: bool = False

    authority_sites_dominant: bool = False

    serp_complexity_score: float = 50.0

    # =========================================================
    # ADAPTIVE LEARNING
    # =========================================================

    adaptive_weights: Dict[str, float] = field(
        default_factory=dict
    )

    adaptive_rules: Dict[str, Any] = field(
        default_factory=dict
    )

    applied_rules: List[str] = field(
        default_factory=list
    )

    # =========================================================
    # TRACKING FLAGS
    # =========================================================

    ranking_tracking_enabled: bool = True

    freshness_tracking_enabled: bool = True

    performance_learning_enabled: bool = True

    adaptive_learning_enabled: bool = True

    # =========================================================
    # REASONING
    # =========================================================

    reasoning: List[str] = field(
        default_factory=list
    )

    recommendations: List[str] = field(
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

            "url": self.url,

            # =================================================
            # PUBLISH
            # =================================================

            "published_at": (
                self.published_at.isoformat()
            ),

            "published_by": (
                self.published_by
            ),

            "publishing_allowed": (
                self.publishing_allowed
            ),

            # =================================================
            # SCORES
            # =================================================

            "overall_score": (
                self.overall_score
            ),

            "seo_score": (
                self.seo_score
            ),

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

            "ranking_score": (
                self.ranking_score
            ),

            # =================================================
            # PREDICTIONS
            # =================================================

            "predicted_ranking_probability": (
                self.predicted_ranking_probability
            ),

            "predicted_position": (
                self.predicted_position
            ),

            "predicted_traffic": (
                self.predicted_traffic
            ),

            "predicted_ctr": (
                self.predicted_ctr
            ),

            "prediction_confidence": (
                self.prediction_confidence
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

            "expert_tone_used": (
                self.expert_tone_used
            ),

            "official_sources_used": (
                self.official_sources_used
            ),

            # =================================================
            # CONTEXT
            # =================================================

            "intent": self.intent,

            "article_type": (
                self.article_type
            ),

            "semantic_type": (
                self.semantic_type
            ),

            "competition_level": (
                self.competition_level
            ),

            "freshness_required": (
                self.freshness_required
            ),

            "authority_required": (
                self.authority_required
            ),

            "ymyl_sensitive": (
                self.ymyl_sensitive
            ),

            # =================================================
            # SERP
            # =================================================

            "featured_snippet_targeted": (
                self.featured_snippet_targeted
            ),

            "faq_dominant_serp": (
                self.faq_dominant_serp
            ),

            "video_heavy_serp": (
                self.video_heavy_serp
            ),

            "authority_sites_dominant": (
                self.authority_sites_dominant
            ),

            "serp_complexity_score": (
                self.serp_complexity_score
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

            "applied_rules": (
                self.applied_rules
            ),

            # =================================================
            # TRACKING
            # =================================================

            "ranking_tracking_enabled": (
                self.ranking_tracking_enabled
            ),

            "freshness_tracking_enabled": (
                self.freshness_tracking_enabled
            ),

            "performance_learning_enabled": (
                self.performance_learning_enabled
            ),

            "adaptive_learning_enabled": (
                self.adaptive_learning_enabled
            ),

            # =================================================
            # REASONING
            # =================================================

            "reasoning": self.reasoning,

            "recommendations": (
                self.recommendations
            ),

            "warnings": (
                self.warnings
            ),

            # =================================================
            # META
            # =================================================

            "metadata": self.metadata,
        }