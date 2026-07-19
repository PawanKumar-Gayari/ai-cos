"""
Context Builder

Central intelligence aggregation layer.

This module combines:
- topic context
- intent context
- freshness context
- authority context
- competition context
- SERP context

into ONE unified DecisionContext.

Goal:
Create a single intelligence object used by:
- decision engine
- adaptive engine
- strategy engine
- verification engine
- scoring engine
"""

from dataclasses import dataclass, field, asdict
from typing import Dict, Any, List

from .topic_context import (
    TopicContextEngine,
)

from .intent_context import (
    IntentContextEngine,
)

from .freshness_context import (
    FreshnessContextEngine,
)

from .authority_context import (
    AuthorityContextEngine,
)

from .competition_context import (
    CompetitionContextEngine,
)

from .serp_context import (
    SerpContextEngine,
)


# =============================================================
# DECISION CONTEXT
# =============================================================

@dataclass
class DecisionContext:

    # =========================================================
    # INPUT
    # =========================================================

    topic: str

    keyword: str = ""

    niche: str = "default"

    # =========================================================
    # TOPIC
    # =========================================================

    article_type: str = "general"

    semantic_type: str = "general"

    # =========================================================
    # INTENT
    # =========================================================

    intent: str = "informational"

    # =========================================================
    # FRESHNESS
    # =========================================================

    freshness_required: bool = False

    update_frequency: str = "weekly"

    max_age_days: int = 30

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

    content_depth_required: str = "medium"

    authority_gap: float = 0.0

    semantic_gap: float = 0.0

    # =========================================================
    # SERP SIGNALS
    # =========================================================

    faq_dominant: bool = False

    tables_common: bool = False

    video_heavy: bool = False

    featured_snippet: bool = False

    # =========================================================
    # SOURCES
    # =========================================================

    preferred_sources: List[str] = field(
        default_factory=list
    )

    # =========================================================
    # NOTES
    # =========================================================

    notes: List[str] = field(
        default_factory=list
    )


# =============================================================
# CONTEXT BUILDER
# =============================================================

class ContextBuilder:

    """
    Central intelligence aggregation engine.
    """

    def __init__(self):

        self.topic_engine = (
            TopicContextEngine()
        )

        self.intent_engine = (
            IntentContextEngine()
        )

        self.freshness_engine = (
            FreshnessContextEngine()
        )

        self.authority_engine = (
            AuthorityContextEngine()
        )

        self.competition_engine = (
            CompetitionContextEngine()
        )

        self.serp_engine = (
            SerpContextEngine()
        )

    # =========================================================
    # BUILD CONTEXT
    # =========================================================

    def build(
        self,
        topic: str,
        keyword: str = "",
        serp_data: Dict[str, Any] = None,
    ) -> DecisionContext:

        serp_data = serp_data or {}

        # =====================================================
        # TOPIC CONTEXT
        # =====================================================

        topic_context = self.topic_engine.build(
            topic=topic,
        )

        # =====================================================
        # INTENT CONTEXT
        # =====================================================

        intent_context = self.intent_engine.build(
            topic=topic,
        )

        # =====================================================
        # FRESHNESS CONTEXT
        # =====================================================

        freshness_context = (
            self.freshness_engine.build(
                topic=topic,
                niche=topic_context.niche,
            )
        )

        # =====================================================
        # AUTHORITY CONTEXT
        # =====================================================

        authority_context = (
            self.authority_engine.build(
                topic=topic,
                niche=topic_context.niche,
            )
        )

        # =====================================================
        # SERP CONTEXT
        # =====================================================

        serp_context = self.serp_engine.build(
            serp_data=serp_data,
        )

        # =====================================================
        # COMPETITION CONTEXT
        # =====================================================

        competition_context = (
            self.competition_engine.build(
                topic=topic,
                niche=topic_context.niche,
                serp_signals=serp_context,
            )
        )

        # =====================================================
        # BUILD FINAL DECISION CONTEXT
        # =====================================================

        context = DecisionContext(

            topic=topic,

            keyword=keyword,

            # =================================================
            # TOPIC
            # =================================================

            niche=topic_context.niche,

            article_type=(
                topic_context.article_type
            ),

            semantic_type=(
                topic_context.semantic_type
            ),

            # =================================================
            # INTENT
            # =================================================

            intent=intent_context.intent,

            # =================================================
            # FRESHNESS
            # =================================================

            freshness_required=(
                freshness_context.freshness_required
            ),

            update_frequency=(
                freshness_context.update_frequency
            ),

            max_age_days=(
                freshness_context.max_age_days
            ),

            # =================================================
            # AUTHORITY
            # =================================================

            authority_required=(
                authority_context.authority_required
            ),

            official_sources_required=(
                authority_context.official_sources_required
            ),

            verification_strictness=(
                authority_context.verification_strictness
            ),

            trust_level=(
                authority_context.trust_level
            ),

            ymyl_sensitive=(
                authority_context.ymyl_sensitive
            ),

            preferred_sources=(
                authority_context.preferred_sources
            ),

            # =================================================
            # COMPETITION
            # =================================================

            competition_level=(
                competition_context.competition_level
            ),

            content_depth_required=(
                competition_context.content_depth_required
            ),

            authority_gap=(
                competition_context.authority_gap
            ),

            semantic_gap=(
                competition_context.semantic_gap
            ),

            # =================================================
            # SERP
            # =================================================

            faq_dominant=(
                serp_context.get(
                    "faq_dominant",
                    False,
                )
            ),

            tables_common=(
                serp_context.get(
                    "tables_common",
                    False,
                )
            ),

            video_heavy=(
                serp_context.get(
                    "video_heavy",
                    False,
                )
            ),

            featured_snippet=(
                serp_context.get(
                    "featured_snippet",
                    False,
                )
            ),
        )

        # =====================================================
        # NOTES
        # =====================================================

        context.notes.extend(
            topic_context.notes
        )

        context.notes.extend(
            freshness_context.notes
        )

        context.notes.extend(
            authority_context.notes
        )

        context.notes.extend(
            competition_context.notes
        )

        return context

    # =========================================================
    # EXPORT
    # =========================================================

    def export(
        self,
        context: DecisionContext,
    ) -> Dict[str, Any]:

        return asdict(context)