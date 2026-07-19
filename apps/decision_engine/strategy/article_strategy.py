"""
Article Strategy

Purpose:
Generate the best article creation strategy
based on:
- ranking opportunities
- freshness
- competition
- authority
- SEO
- search intent
- content depth

Goal:
Select the optimal article strategy BEFORE
generation begins.

This becomes the strategic editorial planning
layer of AI_COS.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List


# =============================================================
# ARTICLE STRATEGY RESULT
# =============================================================

@dataclass
class ArticleStrategyResult:

    # =========================================================
    # STRATEGY
    # =========================================================

    selected_strategy: str = "standard"

    article_type: str = "informational"

    content_depth: str = "medium"

    ranking_strategy: str = "balanced"

    publishing_strategy: str = "normal"

    # =========================================================
    # FLAGS
    # =========================================================

    aggressive_ranking_strategy: bool = False

    freshness_priority: bool = False

    authority_priority: bool = False

    snippet_focused: bool = False

    longtail_strategy: bool = False

    # =========================================================
    # CONTENT
    # =========================================================

    recommended_word_count: int = 1500

    recommended_heading_count: int = 10

    recommended_entity_count: int = 15

    recommended_internal_links: int = 5

    recommended_faq_count: int = 3

    # =========================================================
    # SEO
    # =========================================================

    target_keyword_density: float = 1.5

    semantic_optimization_level: str = "medium"

    seo_aggressiveness: str = "medium"

    # =========================================================
    # RISKS
    # =========================================================

    competition_risk: str = "medium"

    ranking_risk: str = "medium"

    freshness_risk: str = "medium"

    authority_risk: str = "medium"

    # =========================================================
    # OPPORTUNITIES
    # =========================================================

    freshness_opportunity: bool = False

    low_competition_opportunity: bool = False

    snippet_opportunity: bool = False

    traffic_opportunity: bool = False

    # =========================================================
    # STRUCTURE
    # =========================================================

    recommended_sections: List[str] = field(
        default_factory=list
    )

    recommended_features: List[str] = field(
        default_factory=list
    )

    # =========================================================
    # SIGNALS
    # =========================================================

    strategy_signals: Dict[str, Any] = field(
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
# ARTICLE STRATEGY
# =============================================================

class ArticleStrategy:

    """
    Editorial article strategy selector.
    """

    # =========================================================
    # ANALYZE
    # =========================================================

    def analyze(
        self,
        keyword: str,
        competition_score: float = 50.0,
        freshness_score: float = 50.0,
        authority_score: float = 50.0,
        ranking_probability: float = 50.0,
        trend_sensitive: bool = False,
        snippet_opportunity: bool = False,
    ) -> ArticleStrategyResult:

        result = ArticleStrategyResult()

        keyword = (
            keyword or ""
        ).lower()

        # =====================================================
        # ARTICLE TYPE
        # =====================================================

        self._detect_article_type(
            result,
            keyword,
        )

        # =====================================================
        # OPPORTUNITIES
        # =====================================================

        self._detect_opportunities(
            result,
            competition_score,
            freshness_score,
            ranking_probability,
            snippet_opportunity,
        )

        # =====================================================
        # STRATEGY
        # =====================================================

        self._select_strategy(
            result,
            competition_score,
            freshness_score,
            authority_score,
            trend_sensitive,
        )

        # =====================================================
        # CONTENT
        # =====================================================

        self._configure_content(
            result,
            competition_score,
            ranking_probability,
        )

        # =====================================================
        # SEO
        # =====================================================

        self._configure_seo(
            result,
            snippet_opportunity,
            competition_score,
        )

        # =====================================================
        # STRUCTURE
        # =====================================================

        self._build_structure(
            result
        )

        # =====================================================
        # FINALIZE
        # =====================================================

        self._finalize(
            result
        )

        return result

    # =========================================================
    # ARTICLE TYPE
    # =========================================================

    def _detect_article_type(
        self,
        result: ArticleStrategyResult,
        keyword: str,
    ) -> None:

        # =====================================================
        # GUIDE
        # =====================================================

        if (

            "how to" in keyword

            or

            "guide" in keyword
        ):

            result.article_type = (
                "guide"
            )

            result.content_depth = (
                "deep"
            )

        # =====================================================
        # LISTICLE
        # =====================================================

        elif (

            "best" in keyword

            or

            "top" in keyword
        ):

            result.article_type = (
                "listicle"
            )

        # =====================================================
        # NEWS
        # =====================================================

        elif (

            "result" in keyword

            or

            "notification" in keyword

            or

            "latest" in keyword
        ):

            result.article_type = (
                "news"
            )

            result.freshness_priority = (
                True
            )

        # =====================================================
        # REVIEW
        # =====================================================

        elif (

            "review" in keyword

            or

            "vs" in keyword
        ):

            result.article_type = (
                "comparison"
            )

        else:

            result.article_type = (
                "informational"
            )

    # =========================================================
    # OPPORTUNITIES
    # =========================================================

    def _detect_opportunities(
        self,
        result: ArticleStrategyResult,
        competition_score: float,
        freshness_score: float,
        ranking_probability: float,
        snippet_opportunity: bool,
    ) -> None:

        # =====================================================
        # LOW COMPETITION
        # =====================================================

        if competition_score <= 40:

            result.low_competition_opportunity = (
                True
            )

            result.longtail_strategy = (
                True
            )

        # =====================================================
        # FRESHNESS
        # =====================================================

        if freshness_score >= 80:

            result.freshness_opportunity = (
                True
            )

        # =====================================================
        # RANKING
        # =====================================================

        if ranking_probability >= 75:

            result.traffic_opportunity = (
                True
            )

            result.aggressive_ranking_strategy = (
                True
            )

        # =====================================================
        # SNIPPETS
        # =====================================================

        if snippet_opportunity:

            result.snippet_opportunity = (
                True
            )

            result.snippet_focused = (
                True
            )

    # =========================================================
    # STRATEGY
    # =========================================================

    def _select_strategy(
        self,
        result: ArticleStrategyResult,
        competition_score: float,
        freshness_score: float,
        authority_score: float,
        trend_sensitive: bool,
    ) -> None:

        # =====================================================
        # NEWS
        # =====================================================

        if result.article_type == "news":

            result.selected_strategy = (
                "realtime_news"
            )

            result.publishing_strategy = (
                "immediate"
            )

            result.ranking_strategy = (
                "freshness_domination"
            )

        # =====================================================
        # LOW COMPETITION
        # =====================================================

        elif competition_score <= 40:

            result.selected_strategy = (
                "aggressive_longtail"
            )

            result.ranking_strategy = (
                "rapid_ranking"
            )

        # =====================================================
        # HIGH COMPETITION
        # =====================================================

        elif competition_score >= 75:

            result.selected_strategy = (
                "authority_first"
            )

            result.authority_priority = (
                True
            )

            result.ranking_strategy = (
                "authority_building"
            )

        # =====================================================
        # TREND
        # =====================================================

        elif trend_sensitive:

            result.selected_strategy = (
                "trend_capture"
            )

            result.publishing_strategy = (
                "fast_publish"
            )

        # =====================================================
        # DEFAULT
        # =====================================================

        else:

            result.selected_strategy = (
                "balanced_seo"
            )

    # =========================================================
    # CONTENT
    # =========================================================

    def _configure_content(
        self,
        result: ArticleStrategyResult,
        competition_score: float,
        ranking_probability: float,
    ) -> None:

        # =====================================================
        # HIGH COMPETITION
        # =====================================================

        if competition_score >= 70:

            result.recommended_word_count = (
                3000
            )

            result.recommended_heading_count = (
                18
            )

            result.recommended_entity_count = (
                35
            )

        # =====================================================
        # MEDIUM
        # =====================================================

        elif competition_score >= 45:

            result.recommended_word_count = (
                2200
            )

            result.recommended_heading_count = (
                14
            )

            result.recommended_entity_count = (
                25
            )

        # =====================================================
        # LOW
        # =====================================================

        else:

            result.recommended_word_count = (
                1500
            )

            result.recommended_heading_count = (
                10
            )

            result.recommended_entity_count = (
                15
            )

        # =====================================================
        # HIGH RANKING
        # =====================================================

        if ranking_probability >= 80:

            result.recommended_internal_links = (
                10
            )

            result.recommended_faq_count = (
                5
            )

    # =========================================================
    # SEO
    # =========================================================

    def _configure_seo(
        self,
        result: ArticleStrategyResult,
        snippet_opportunity: bool,
        competition_score: float,
    ) -> None:

        # =====================================================
        # SNIPPETS
        # =====================================================

        if snippet_opportunity:

            result.semantic_optimization_level = (
                "high"
            )

            result.seo_aggressiveness = (
                "high"
            )

            result.target_keyword_density = (
                1.8
            )

        # =====================================================
        # COMPETITION
        # =====================================================

        if competition_score >= 70:

            result.semantic_optimization_level = (
                "aggressive"
            )

            result.seo_aggressiveness = (
                "high"
            )

    # =========================================================
    # STRUCTURE
    # =========================================================

    def _build_structure(
        self,
        result: ArticleStrategyResult,
    ) -> None:

        sections = [

            "Introduction",

            "Main Content",

            "Examples",

            "Expert Insights",

            "FAQ",

            "Conclusion",
        ]

        # =====================================================
        # NEWS
        # =====================================================

        if result.article_type == "news":

            sections = [

                "Breaking Update",

                "Official Information",

                "Important Dates",

                "Key Details",

                "FAQ",
            ]

        # =====================================================
        # GUIDE
        # =====================================================

        elif result.article_type == "guide":

            sections = [

                "Introduction",

                "Step-by-Step Guide",

                "Examples",

                "Common Mistakes",

                "Tips",

                "FAQ",

                "Conclusion",
            ]

        result.recommended_sections = (
            sections
        )

        # =====================================================
        # FEATURES
        # =====================================================

        features = [

            "Tables",

            "Bullet Lists",

            "Internal Links",
        ]

        if result.snippet_focused:

            features.append(
                "Snippet Blocks"
            )

        if result.article_type == "guide":

            features.append(
                "Step Boxes"
            )

        result.recommended_features = (
            features
        )

    # =========================================================
    # FINALIZE
    # =========================================================

    def _finalize(
        self,
        result: ArticleStrategyResult,
    ) -> None:

        # =====================================================
        # RISKS
        # =====================================================

        if result.authority_priority:

            result.authority_risk = (
                "high"
            )

        if result.freshness_priority:

            result.freshness_risk = (
                "high"
            )

        # =====================================================
        # RECOMMENDATIONS
        # =====================================================

        if result.aggressive_ranking_strategy:

            result.add_recommendation(
                "Use aggressive SEO optimization"
            )

            result.add_action(
                "Expand semantic coverage"
            )

        if result.snippet_focused:

            result.add_recommendation(
                "Optimize heavily for snippets"
            )

            result.add_action(
                "Add concise answer sections"
            )

        if result.authority_priority:

            result.add_recommendation(
                "Add authoritative references"
            )

            result.add_action(
                "Use official citations"
            )

        if result.freshness_priority:

            result.add_recommendation(
                "Publish immediately after generation"
            )

        result.add_reasoning(
            f"Selected strategy: "
            f"{result.selected_strategy}"
        )

    # =========================================================
    # EXPORT
    # =========================================================

    def export(
        self,
        result: ArticleStrategyResult,
    ) -> Dict[str, Any]:

        return {

            "selected_strategy": (
                result.selected_strategy
            ),

            "article_type": (
                result.article_type
            ),

            "content_depth": (
                result.content_depth
            ),

            "ranking_strategy": (
                result.ranking_strategy
            ),

            "publishing_strategy": (
                result.publishing_strategy
            ),

            "aggressive_ranking_strategy": (
                result.aggressive_ranking_strategy
            ),

            "freshness_priority": (
                result.freshness_priority
            ),

            "authority_priority": (
                result.authority_priority
            ),

            "snippet_focused": (
                result.snippet_focused
            ),

            "longtail_strategy": (
                result.longtail_strategy
            ),

            "recommended_word_count": (
                result.recommended_word_count
            ),

            "recommended_heading_count": (
                result.recommended_heading_count
            ),

            "recommended_entity_count": (
                result.recommended_entity_count
            ),

            "recommended_internal_links": (
                result.recommended_internal_links
            ),

            "recommended_faq_count": (
                result.recommended_faq_count
            ),

            "target_keyword_density": (
                result.target_keyword_density
            ),

            "semantic_optimization_level": (
                result.semantic_optimization_level
            ),

            "seo_aggressiveness": (
                result.seo_aggressiveness
            ),

            "competition_risk": (
                result.competition_risk
            ),

            "ranking_risk": (
                result.ranking_risk
            ),

            "freshness_risk": (
                result.freshness_risk
            ),

            "authority_risk": (
                result.authority_risk
            ),

            "freshness_opportunity": (
                result.freshness_opportunity
            ),

            "low_competition_opportunity": (
                result.low_competition_opportunity
            ),

            "snippet_opportunity": (
                result.snippet_opportunity
            ),

            "traffic_opportunity": (
                result.traffic_opportunity
            ),

            "recommended_sections": (
                result.recommended_sections
            ),

            "recommended_features": (
                result.recommended_features
            ),

            "strategy_signals": (
                result.strategy_signals
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