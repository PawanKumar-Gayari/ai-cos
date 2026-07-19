"""
Intent Context Engine

This module detects the primary search intent
behind a topic/query.

Goal:
Understand WHAT the user wants so the system
can adapt:
- article structure
- SEO strategy
- depth
- comparisons
- CTA behavior
- content layout

Intent Types:
- informational
- commercial
- transactional
- navigational
- comparison
- tutorial
- news
"""

from dataclasses import dataclass, field
from typing import List


# =============================================================
# INTENT CONTEXT
# =============================================================

@dataclass
class IntentContext:

    intent: str = "informational"

    confidence: float = 0.5

    requires_comparison: bool = False

    requires_tables: bool = False

    requires_step_by_step: bool = False

    requires_cta: bool = False

    requires_faq: bool = False

    article_style: str = "guide"

    notes: List[str] = field(
        default_factory=list
    )


# =============================================================
# INTENT CONTEXT ENGINE
# =============================================================

class IntentContextEngine:

    """
    Detects user intent from topic/query.
    """

    # =========================================================
    # MAIN ENTRY
    # =========================================================

    def build(
        self,
        topic: str,
    ) -> IntentContext:

        context = IntentContext()

        topic = (topic or "").lower()

        # =====================================================
        # COMMERCIAL INTENT
        # =====================================================

        commercial_keywords = [
            "best",
            "top",
            "vs",
            "review",
            "comparison",
            "compare",
            "alternative",
            "price",
        ]

        # =====================================================
        # TRANSACTIONAL INTENT
        # =====================================================

        transactional_keywords = [
            "buy",
            "download",
            "apply",
            "register",
            "book",
            "join",
            "signup",
        ]

        # =====================================================
        # TUTORIAL INTENT
        # =====================================================

        tutorial_keywords = [
            "how to",
            "guide",
            "tutorial",
            "learn",
            "setup",
            "install",
            "configure",
        ]

        # =====================================================
        # NEWS INTENT
        # =====================================================

        news_keywords = [
            "latest",
            "breaking",
            "update",
            "news",
            "today",
            "announcement",
        ]

        # =====================================================
        # COMPARISON
        # =====================================================

        if any(
            keyword in topic
            for keyword in commercial_keywords
        ):

            context.intent = "commercial"

            context.requires_comparison = True

            context.requires_tables = True

            context.requires_cta = True

            context.requires_faq = True

            context.article_style = "comparison"

            context.confidence = 0.85

            context.notes.append(
                "Commercial intent detected"
            )

        # =====================================================
        # TRANSACTIONAL
        # =====================================================

        elif any(
            keyword in topic
            for keyword in transactional_keywords
        ):

            context.intent = "transactional"

            context.requires_cta = True

            context.requires_step_by_step = True

            context.article_style = "action"

            context.confidence = 0.80

            context.notes.append(
                "Transactional intent detected"
            )

        # =====================================================
        # TUTORIAL
        # =====================================================

        elif any(
            keyword in topic
            for keyword in tutorial_keywords
        ):

            context.intent = "tutorial"

            context.requires_step_by_step = True

            context.requires_tables = False

            context.requires_faq = True

            context.article_style = "tutorial"

            context.confidence = 0.90

            context.notes.append(
                "Tutorial intent detected"
            )

        # =====================================================
        # NEWS
        # =====================================================

        elif any(
            keyword in topic
            for keyword in news_keywords
        ):

            context.intent = "news"

            context.requires_faq = False

            context.requires_cta = False

            context.article_style = "news"

            context.confidence = 0.88

            context.notes.append(
                "News intent detected"
            )

        # =====================================================
        # DEFAULT INFORMATIONAL
        # =====================================================

        else:

            context.intent = "informational"

            context.requires_faq = True

            context.article_style = "guide"

            context.confidence = 0.70

            context.notes.append(
                "Default informational intent"
            )

        return context

    # =========================================================
    # EXPORT
    # =========================================================

    def export(
        self,
        context: IntentContext,
    ) -> dict:

        return {
            "intent": context.intent,
            "confidence": context.confidence,
            "requires_comparison": (
                context.requires_comparison
            ),
            "requires_tables": (
                context.requires_tables
            ),
            "requires_step_by_step": (
                context.requires_step_by_step
            ),
            "requires_cta": (
                context.requires_cta
            ),
            "requires_faq": (
                context.requires_faq
            ),
            "article_style": (
                context.article_style
            ),
            "notes": context.notes,
        }