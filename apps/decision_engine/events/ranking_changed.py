"""
Event: Ranking Changed

Triggered whenever article ranking changes.

Purpose:
- monitor SEO performance shifts
- detect ranking gains/losses
- feed adaptive learning system
- optimize future strategy decisions
- identify ranking decay patterns

This is a core SEO intelligence signal.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Any, List


# =============================================================
# EVENT
# =============================================================

@dataclass
class RankingChangedEvent:

    # =========================================================
    # ARTICLE
    # =========================================================

    article_id: str

    title: str

    keyword: str

    niche: str

    url: str

    # =========================================================
    # RANKING DATA
    # =========================================================

    previous_position: int = 0

    current_position: int = 0

    ranking_change: int = 0

    ranking_direction: str = "stable"

    # =========================================================
    # VISIBILITY
    # =========================================================

    impressions: int = 0

    clicks: int = 0

    ctr: float = 0.0

    estimated_traffic: int = 0

    # =========================================================
    # FEATURE DETECTION
    # =========================================================

    featured_snippet_gained: bool = False

    featured_snippet_lost: bool = False

    faq_visibility_detected: bool = False

    video_visibility_detected: bool = False

    # =========================================================
    # PERFORMANCE SIGNALS
    # =========================================================

    ranking_improved: bool = False

    ranking_declined: bool = False

    ranking_stable: bool = False

    traffic_growth_detected: bool = False

    traffic_decay_detected: bool = False

    # =========================================================
    # SEO SIGNALS
    # =========================================================

    seo_score: float = 0.0

    quality_score: float = 0.0

    freshness_score: float = 0.0

    authority_score: float = 0.0

    engagement_score: float = 0.0

    # =========================================================
    # COMPETITION
    # =========================================================

    competition_level: str = "medium"

    authority_gap: float = 0.0

    serp_complexity_score: float = 50.0

    # =========================================================
    # LEARNING SIGNALS
    # =========================================================

    adaptive_learning_enabled: bool = True

    performance_learning_enabled: bool = True

    affected_weights: Dict[str, float] = field(
        default_factory=dict
    )

    affected_rules: List[str] = field(
        default_factory=list
    )

    # =========================================================
    # STRATEGY SIGNALS
    # =========================================================

    faq_enabled: bool = False

    tables_enabled: bool = False

    comparison_enabled: bool = False

    official_sources_used: bool = False

    # =========================================================
    # RECOMMENDED ACTIONS
    # =========================================================

    recommended_actions: List[str] = field(
        default_factory=list
    )

    # =========================================================
    # TIMESTAMP
    # =========================================================

    detected_at: datetime = field(
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

    def calculate_change(
        self,
    ) -> None:

        self.ranking_change = (
            self.previous_position
            - self.current_position
        )

        # =====================================================
        # IMPROVED
        # =====================================================

        if self.ranking_change > 0:

            self.ranking_direction = "up"

            self.ranking_improved = True

            self.add_reasoning(
                "Ranking improvement detected"
            )

        # =====================================================
        # DECLINED
        # =====================================================

        elif self.ranking_change < 0:

            self.ranking_direction = "down"

            self.ranking_declined = True

            self.add_warning(
                "Ranking decline detected"
            )

        # =====================================================
        # STABLE
        # =====================================================

        else:

            self.ranking_direction = "stable"

            self.ranking_stable = True

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

        self.calculate_change()

        # =====================================================
        # FEATURED SNIPPET
        # =====================================================

        if self.featured_snippet_gained:

            self.add_action(
                "Increase snippet optimization weight"
            )

            self.add_reasoning(
                "Featured snippet acquired"
            )

        if self.featured_snippet_lost:

            self.add_warning(
                "Featured snippet lost"
            )

            self.add_action(
                "Re-optimize snippet structure"
            )

        # =====================================================
        # RANKING DROP
        # =====================================================

        if (
            self.ranking_declined
            and abs(self.ranking_change) >= 10
        ):

            self.add_warning(
                "Major ranking drop detected"
            )

            self.add_action(
                "Trigger SEO audit"
            )

        # =====================================================
        # TRAFFIC DECAY
        # =====================================================

        if self.traffic_decay_detected:

            self.add_action(
                "Refresh metadata and title"
            )

        # =====================================================
        # FAQ PERFORMANCE
        # =====================================================

        if (
            self.faq_enabled
            and self.ranking_improved
        ):

            self.add_reasoning(
                "FAQ structure may have improved rankings"
            )

            self.set_weight_adjustment(
                "faq_weight",
                0.2,
            )

        # =====================================================
        # TABLE PERFORMANCE
        # =====================================================

        if (
            self.tables_enabled
            and self.ranking_improved
        ):

            self.add_reasoning(
                "Table structure improved SERP performance"
            )

            self.set_weight_adjustment(
                "table_weight",
                0.2,
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
            # RANKINGS
            # =================================================

            "previous_position": (
                self.previous_position
            ),

            "current_position": (
                self.current_position
            ),

            "ranking_change": (
                self.ranking_change
            ),

            "ranking_direction": (
                self.ranking_direction
            ),

            # =================================================
            # VISIBILITY
            # =================================================

            "impressions": (
                self.impressions
            ),

            "clicks": self.clicks,

            "ctr": self.ctr,

            "estimated_traffic": (
                self.estimated_traffic
            ),

            # =================================================
            # FEATURES
            # =================================================

            "featured_snippet_gained": (
                self.featured_snippet_gained
            ),

            "featured_snippet_lost": (
                self.featured_snippet_lost
            ),

            "faq_visibility_detected": (
                self.faq_visibility_detected
            ),

            "video_visibility_detected": (
                self.video_visibility_detected
            ),

            # =================================================
            # PERFORMANCE
            # =================================================

            "ranking_improved": (
                self.ranking_improved
            ),

            "ranking_declined": (
                self.ranking_declined
            ),

            "ranking_stable": (
                self.ranking_stable
            ),

            "traffic_growth_detected": (
                self.traffic_growth_detected
            ),

            "traffic_decay_detected": (
                self.traffic_decay_detected
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

            "engagement_score": (
                self.engagement_score
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

            "serp_complexity_score": (
                self.serp_complexity_score
            ),

            # =================================================
            # LEARNING
            # =================================================

            "adaptive_learning_enabled": (
                self.adaptive_learning_enabled
            ),

            "performance_learning_enabled": (
                self.performance_learning_enabled
            ),

            "affected_weights": (
                self.affected_weights
            ),

            "affected_rules": (
                self.affected_rules
            ),

            # =================================================
            # STRATEGY
            # =================================================

            "faq_enabled": (
                self.faq_enabled
            ),

            "tables_enabled": (
                self.tables_enabled
            ),

            "comparison_enabled": (
                self.comparison_enabled
            ),

            "official_sources_used": (
                self.official_sources_used
            ),

            # =================================================
            # ACTIONS
            # =================================================

            "recommended_actions": (
                self.recommended_actions
            ),

            # =================================================
            # TIMESTAMP
            # =================================================

            "detected_at": (
                self.detected_at.isoformat()
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