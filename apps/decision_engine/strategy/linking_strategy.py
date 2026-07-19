"""
Linking Strategy

Purpose:
Generate intelligent internal and external
linking strategy for:
- authority flow
- topical relevance
- crawl optimization
- ranking support
- semantic SEO
- user navigation

Goal:
Build the best link architecture BEFORE
article generation begins.

This becomes the link intelligence layer
of AI_COS.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List


# =============================================================
# LINKING STRATEGY RESULT
# =============================================================

@dataclass
class LinkingStrategyResult:

    # =========================================================
    # STRATEGY
    # =========================================================

    linking_strategy: str = "balanced"

    internal_linking_priority: str = "medium"

    external_linking_priority: str = "low"

    # =========================================================
    # LINK COUNTS
    # =========================================================

    recommended_internal_links: int = 5

    recommended_external_links: int = 2

    recommended_authority_links: int = 2

    # =========================================================
    # SEO
    # =========================================================

    semantic_linking_enabled: bool = False

    authority_linking_enabled: bool = False

    topic_cluster_enabled: bool = False

    crawl_optimization_enabled: bool = False

    # =========================================================
    # LINK TYPES
    # =========================================================

    include_contextual_links: bool = True

    include_navigation_links: bool = True

    include_related_article_links: bool = True

    include_reference_links: bool = False

    include_citation_links: bool = False

    # =========================================================
    # OPPORTUNITIES
    # =========================================================

    authority_boost_opportunity: bool = False

    semantic_boost_opportunity: bool = False

    crawl_depth_optimization: bool = False

    topical_authority_opportunity: bool = False

    # =========================================================
    # RISKS
    # =========================================================

    overlinking_risk: str = "low"

    broken_link_risk: str = "low"

    authority_leak_risk: str = "low"

    irrelevant_link_risk: str = "low"

    # =========================================================
    # LINK STRUCTURE
    # =========================================================

    anchor_text_strategy: str = "natural"

    link_distribution_strategy: str = "balanced"

    link_position_strategy: str = "contextual"

    # =========================================================
    # RECOMMENDED LINKS
    # =========================================================

    recommended_internal_topics: List[str] = field(
        default_factory=list
    )

    recommended_external_sources: List[str] = field(
        default_factory=list
    )

    recommended_anchor_patterns: List[str] = field(
        default_factory=list
    )

    # =========================================================
    # SIGNALS
    # =========================================================

    linking_signals: Dict[str, Any] = field(
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
# LINKING STRATEGY
# =============================================================

class LinkingStrategy:

    """
    Link intelligence strategy engine.
    """

    # =========================================================
    # AUTHORITY DOMAINS
    # =========================================================

    AUTHORITY_DOMAINS = [

        "wikipedia.org",
        "google.com",
        "gov.in",
        "edu",
        "who.int",
    ]

    # =========================================================
    # ANALYZE
    # =========================================================

    def analyze(
        self,
        keyword: str,
        competition_score: float = 50.0,
        authority_score: float = 50.0,
        article_type: str = "informational",
        topic_cluster_available: bool = False,
    ) -> LinkingStrategyResult:

        result = LinkingStrategyResult()

        keyword = (
            keyword or ""
        ).lower()

        article_type = (
            article_type or ""
        ).lower()

        # =====================================================
        # OPPORTUNITIES
        # =====================================================

        self._detect_opportunities(
            result,
            competition_score,
            authority_score,
            topic_cluster_available,
        )

        # =====================================================
        # STRATEGY
        # =====================================================

        self._select_strategy(
            result,
            competition_score,
            authority_score,
        )

        # =====================================================
        # LINK CONFIG
        # =====================================================

        self._configure_links(
            result,
            competition_score,
            article_type,
        )

        # =====================================================
        # STRUCTURE
        # =====================================================

        self._configure_structure(
            result
        )

        # =====================================================
        # RECOMMENDATIONS
        # =====================================================

        self._build_recommendations(
            result,
            keyword,
        )

        # =====================================================
        # FINALIZE
        # =====================================================

        self._finalize(
            result
        )

        return result

    # =========================================================
    # OPPORTUNITIES
    # =========================================================

    def _detect_opportunities(
        self,
        result: LinkingStrategyResult,
        competition_score: float,
        authority_score: float,
        topic_cluster_available: bool,
    ) -> None:

        # =====================================================
        # AUTHORITY
        # =====================================================

        if authority_score < 60:

            result.authority_boost_opportunity = (
                True
            )

            result.authority_linking_enabled = (
                True
            )

        # =====================================================
        # TOPICAL
        # =====================================================

        if topic_cluster_available:

            result.topic_cluster_enabled = (
                True
            )

            result.topical_authority_opportunity = (
                True
            )

        # =====================================================
        # SEMANTIC
        # =====================================================

        if competition_score >= 60:

            result.semantic_boost_opportunity = (
                True
            )

            result.semantic_linking_enabled = (
                True
            )

        # =====================================================
        # CRAWL
        # =====================================================

        if competition_score >= 75:

            result.crawl_depth_optimization = (
                True
            )

            result.crawl_optimization_enabled = (
                True
            )

    # =========================================================
    # STRATEGY
    # =========================================================

    def _select_strategy(
        self,
        result: LinkingStrategyResult,
        competition_score: float,
        authority_score: float,
    ) -> None:

        # =====================================================
        # HIGH COMPETITION
        # =====================================================

        if competition_score >= 75:

            result.linking_strategy = (
                "authority_cluster"
            )

            result.internal_linking_priority = (
                "high"
            )

            result.external_linking_priority = (
                "medium"
            )

        # =====================================================
        # LOW AUTHORITY
        # =====================================================

        elif authority_score < 50:

            result.linking_strategy = (
                "authority_reinforcement"
            )

            result.external_linking_priority = (
                "high"
            )

        # =====================================================
        # DEFAULT
        # =====================================================

        else:

            result.linking_strategy = (
                "balanced_semantic"
            )

    # =========================================================
    # LINK CONFIG
    # =========================================================

    def _configure_links(
        self,
        result: LinkingStrategyResult,
        competition_score: float,
        article_type: str,
    ) -> None:

        # =====================================================
        # HIGH COMPETITION
        # =====================================================

        if competition_score >= 75:

            result.recommended_internal_links = (
                15
            )

            result.recommended_external_links = (
                5
            )

            result.recommended_authority_links = (
                4
            )

        # =====================================================
        # MEDIUM
        # =====================================================

        elif competition_score >= 50:

            result.recommended_internal_links = (
                10
            )

            result.recommended_external_links = (
                3
            )

        # =====================================================
        # LOW
        # =====================================================

        else:

            result.recommended_internal_links = (
                5
            )

            result.recommended_external_links = (
                2
            )

        # =====================================================
        # NEWS
        # =====================================================

        if article_type == "news":

            result.include_reference_links = (
                True
            )

            result.include_citation_links = (
                True
            )

    # =========================================================
    # STRUCTURE
    # =========================================================

    def _configure_structure(
        self,
        result: LinkingStrategyResult,
    ) -> None:

        # =====================================================
        # ANCHOR TEXT
        # =====================================================

        if result.semantic_linking_enabled:

            result.anchor_text_strategy = (
                "semantic_variation"
            )

        # =====================================================
        # DISTRIBUTION
        # =====================================================

        if result.topic_cluster_enabled:

            result.link_distribution_strategy = (
                "topic_cluster"
            )

        # =====================================================
        # POSITION
        # =====================================================

        if result.crawl_optimization_enabled:

            result.link_position_strategy = (
                "hierarchical"
            )

    # =========================================================
    # RECOMMENDATIONS
    # =========================================================

    def _build_recommendations(
        self,
        result: LinkingStrategyResult,
        keyword: str,
    ) -> None:

        # =====================================================
        # INTERNAL TOPICS
        # =====================================================

        result.recommended_internal_topics = [

            f"{keyword} guide",

            f"{keyword} examples",

            f"{keyword} tips",

            f"{keyword} benefits",

            f"{keyword} strategy",
        ]

        # =====================================================
        # SOURCES
        # =====================================================

        result.recommended_external_sources = (
            self.AUTHORITY_DOMAINS
        )

        # =====================================================
        # ANCHORS
        # =====================================================

        result.recommended_anchor_patterns = [

            f"best {keyword}",

            f"{keyword} tutorial",

            f"learn {keyword}",

            f"{keyword} examples",

            f"advanced {keyword}",
        ]

    # =========================================================
    # FINALIZE
    # =========================================================

    def _finalize(
        self,
        result: LinkingStrategyResult,
    ) -> None:

        # =====================================================
        # RISKS
        # =====================================================

        if result.recommended_internal_links >= 20:

            result.overlinking_risk = (
                "medium"
            )

        if result.external_linking_priority == "high":

            result.authority_leak_risk = (
                "medium"
            )

        # =====================================================
        # RECOMMENDATIONS
        # =====================================================

        if result.authority_boost_opportunity:

            result.add_recommendation(
                "Use authoritative external references"
            )

            result.add_action(
                "Add trusted citations"
            )

        if result.topic_cluster_enabled:

            result.add_recommendation(
                "Strengthen topical clusters"
            )

            result.add_action(
                "Interlink related articles"
            )

        if result.semantic_linking_enabled:

            result.add_recommendation(
                "Use semantic anchor variations"
            )

        if result.crawl_optimization_enabled:

            result.add_recommendation(
                "Optimize crawl depth with strategic links"
            )

        result.add_recommendation(
            "Avoid repetitive anchor text"
        )

        result.add_action(
            "Distribute links naturally throughout content"
        )

        result.add_reasoning(
            f"Selected linking strategy: "
            f"{result.linking_strategy}"
        )

    # =========================================================
    # EXPORT
    # =========================================================

    def export(
        self,
        result: LinkingStrategyResult,
    ) -> Dict[str, Any]:

        return {

            "linking_strategy": (
                result.linking_strategy
            ),

            "internal_linking_priority": (
                result.internal_linking_priority
            ),

            "external_linking_priority": (
                result.external_linking_priority
            ),

            "recommended_internal_links": (
                result.recommended_internal_links
            ),

            "recommended_external_links": (
                result.recommended_external_links
            ),

            "recommended_authority_links": (
                result.recommended_authority_links
            ),

            "semantic_linking_enabled": (
                result.semantic_linking_enabled
            ),

            "authority_linking_enabled": (
                result.authority_linking_enabled
            ),

            "topic_cluster_enabled": (
                result.topic_cluster_enabled
            ),

            "crawl_optimization_enabled": (
                result.crawl_optimization_enabled
            ),

            "include_contextual_links": (
                result.include_contextual_links
            ),

            "include_navigation_links": (
                result.include_navigation_links
            ),

            "include_related_article_links": (
                result.include_related_article_links
            ),

            "include_reference_links": (
                result.include_reference_links
            ),

            "include_citation_links": (
                result.include_citation_links
            ),

            "authority_boost_opportunity": (
                result.authority_boost_opportunity
            ),

            "semantic_boost_opportunity": (
                result.semantic_boost_opportunity
            ),

            "crawl_depth_optimization": (
                result.crawl_depth_optimization
            ),

            "topical_authority_opportunity": (
                result.topical_authority_opportunity
            ),

            "overlinking_risk": (
                result.overlinking_risk
            ),

            "broken_link_risk": (
                result.broken_link_risk
            ),

            "authority_leak_risk": (
                result.authority_leak_risk
            ),

            "irrelevant_link_risk": (
                result.irrelevant_link_risk
            ),

            "anchor_text_strategy": (
                result.anchor_text_strategy
            ),

            "link_distribution_strategy": (
                result.link_distribution_strategy
            ),

            "link_position_strategy": (
                result.link_position_strategy
            ),

            "recommended_internal_topics": (
                result.recommended_internal_topics
            ),

            "recommended_external_sources": (
                result.recommended_external_sources
            ),

            "recommended_anchor_patterns": (
                result.recommended_anchor_patterns
            ),

            "linking_signals": (
                result.linking_signals
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