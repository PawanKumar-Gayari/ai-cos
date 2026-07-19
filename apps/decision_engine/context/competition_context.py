"""
Competition Context Engine

This module evaluates the competition environment for a topic.
It provides intelligence signals to the decision engine regarding:
- SERP difficulty
- topical authority gap
- content depth required
- ranking challenges
- strategic adjustments for high competition topics
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any


@dataclass
class CompetitionContext:

    competition_level: str = "medium"  # low, medium, high, very_high

    authority_gap: float = 0.0  # 0-100, how strong competitors are

    content_depth_required: str = "medium"  # low, medium, high, very_high

    semantic_gap: float = 0.0  # 0-100, coverage vs competitors

    backlink_pressure: float = 0.0  # 0-100, link difficulty

    faq_presence: bool = False

    table_presence: bool = False

    video_presence: bool = False

    snippet_presence: bool = False

    notes: List[str] = field(default_factory=list)


class CompetitionContextEngine:

    """
    Evaluates competitive intensity of a topic based on:
    - niche
    - topic
    - SERP analysis signals
    - historical ranking data
    """

    def build(
        self,
        topic: str,
        niche: str = "default",
        serp_signals: Dict[str, Any] = None,
    ) -> CompetitionContext:

        context = CompetitionContext()

        topic = (topic or "").lower()
        niche = (niche or "").lower()
        serp_signals = serp_signals or {}

        # =====================================================
        # Basic competition detection based on niche
        # =====================================================
        if niche in ["jobs", "finance", "health"]:
            context.competition_level = "high"
            context.content_depth_required = "high"
            context.authority_gap = 75
            context.notes.append(
                f"{niche} niche generally has high competition"
            )

        elif niche in ["tech", "education"]:
            context.competition_level = "medium"
            context.content_depth_required = "medium"
            context.authority_gap = 60
            context.notes.append(
                f"{niche} niche has moderate competition"
            )

        else:
            context.competition_level = "medium"
            context.content_depth_required = "medium"
            context.authority_gap = 50
            context.notes.append(
                "Default competition assumptions applied"
            )

        # =====================================================
        # Adjust based on SERP signals if available
        # =====================================================
        if serp_signals:
            context.faq_presence = serp_signals.get(
                "faq_dominant", False
            )
            context.table_presence = serp_signals.get(
                "tables_common", False
            )
            context.video_presence = serp_signals.get(
                "video_heavy", False
            )
            context.snippet_presence = serp_signals.get(
                "featured_snippet", False
            )

            # Adjust competition level based on observed SERP complexity
            complexity_score = serp_signals.get(
                "complexity_score", 50
            )  # 0-100

            if complexity_score > 80:
                context.competition_level = "very_high"
                context.content_depth_required = "very_high"
                context.notes.append(
                    "High SERP complexity detected"
                )
            elif complexity_score > 60:
                context.competition_level = "high"
                context.content_depth_required = "high"
                context.notes.append(
                    "Moderate SERP complexity detected"
                )

            # Adjust semantic gap if provided
            context.semantic_gap = serp_signals.get(
                "semantic_gap", 0
            )

            # Adjust backlink pressure if available
            context.backlink_pressure = serp_signals.get(
                "backlink_pressure", 0
            )

        return context

    # =========================================================
    # EXPORT
    # =========================================================

    def export(
        self,
        context: CompetitionContext,
    ) -> Dict[str, Any]:

        return {
            "competition_level": context.competition_level,
            "authority_gap": context.authority_gap,
            "content_depth_required": context.content_depth_required,
            "semantic_gap": context.semantic_gap,
            "backlink_pressure": context.backlink_pressure,
            "faq_presence": context.faq_presence,
            "table_presence": context.table_presence,
            "video_presence": context.video_presence,
            "snippet_presence": context.snippet_presence,
            "notes": context.notes,
        }