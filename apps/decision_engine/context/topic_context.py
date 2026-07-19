"""
Topic Context Engine

This module analyzes the core topic and extracts:
- niche classification
- article archetype
- semantic category
- topic sensitivity
- editorial requirements

Goal:
Understand WHAT the topic actually represents
before any strategy or generation begins.

This becomes the foundational intelligence layer
for the entire decision engine.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any


# =============================================================
# TOPIC CONTEXT
# =============================================================

@dataclass
class TopicContext:

    # =========================================================
    # CORE
    # =========================================================

    topic: str = ""

    niche: str = "default"

    # =========================================================
    # ARTICLE TYPE
    # =========================================================

    article_type: str = "general"

    semantic_type: str = "general"

    # =========================================================
    # CLASSIFICATIONS
    # =========================================================

    is_news_topic: bool = False

    is_evergreen_topic: bool = False

    is_comparison_topic: bool = False

    is_tutorial_topic: bool = False

    is_ymyl_topic: bool = False

    # =========================================================
    # CONTENT NEEDS
    # =========================================================

    faq_recommended: bool = False

    tables_recommended: bool = False

    expert_tone_recommended: bool = False

    freshness_sensitive: bool = False

    # =========================================================
    # CONFIDENCE
    # =========================================================

    confidence: float = 0.5

    # =========================================================
    # NOTES
    # =========================================================

    notes: List[str] = field(
        default_factory=list
    )


# =============================================================
# TOPIC CONTEXT ENGINE
# =============================================================

class TopicContextEngine:

    """
    Detects the true nature of a topic.

    This layer powers:
    - adaptive behavior
    - strategy planning
    - verification requirements
    - editorial intelligence
    """

    # =========================================================
    # MAIN ENTRY
    # =========================================================

    def build(
        self,
        topic: str,
    ) -> TopicContext:

        context = TopicContext()

        context.topic = topic

        topic = (topic or "").lower()

        self._detect_jobs_niche(
            context,
            topic,
        )

        self._detect_health_niche(
            context,
            topic,
        )

        self._detect_finance_niche(
            context,
            topic,
        )

        self._detect_tech_niche(
            context,
            topic,
        )

        self._detect_education_niche(
            context,
            topic,
        )

        self._detect_article_type(
            context,
            topic,
        )

        self._detect_semantic_type(
            context,
            topic,
        )

        self._detect_editorial_requirements(
            context,
        )

        self._apply_default_behavior(
            context,
        )

        return context

    # =========================================================
    # JOBS NICHE
    # =========================================================

    def _detect_jobs_niche(
        self,
        context: TopicContext,
        topic: str,
    ) -> None:

        keywords = [
            "recruitment",
            "vacancy",
            "result",
            "admit card",
            "exam",
            "notification",
            "apply online",
            "syllabus",
        ]

        if any(
            keyword in topic
            for keyword in keywords
        ):

            context.niche = "jobs"

            context.article_type = (
                "notification"
            )

            context.semantic_type = (
                "freshness_sensitive"
            )

            context.is_news_topic = True

            context.freshness_sensitive = True

            context.tables_recommended = True

            context.faq_recommended = True

            context.confidence = 0.92

            context.notes.append(
                "Jobs niche detected"
            )

    # =========================================================
    # HEALTH NICHE
    # =========================================================

    def _detect_health_niche(
        self,
        context: TopicContext,
        topic: str,
    ) -> None:

        keywords = [
            "disease",
            "treatment",
            "health",
            "medicine",
            "symptoms",
            "therapy",
            "nutrition",
        ]

        if any(
            keyword in topic
            for keyword in keywords
        ):

            context.niche = "health"

            context.is_ymyl_topic = True

            context.expert_tone_recommended = True

            context.article_type = (
                "authority_guide"
            )

            context.semantic_type = (
                "high_authority"
            )

            context.confidence = 0.90

            context.notes.append(
                "Health niche detected"
            )

    # =========================================================
    # FINANCE NICHE
    # =========================================================

    def _detect_finance_niche(
        self,
        context: TopicContext,
        topic: str,
    ) -> None:

        keywords = [
            "loan",
            "investment",
            "finance",
            "bank",
            "insurance",
            "stock",
            "tax",
        ]

        if any(
            keyword in topic
            for keyword in keywords
        ):

            context.niche = "finance"

            context.is_ymyl_topic = True

            context.expert_tone_recommended = True

            context.tables_recommended = True

            context.article_type = (
                "financial_guide"
            )

            context.semantic_type = (
                "high_trust"
            )

            context.confidence = 0.88

            context.notes.append(
                "Finance niche detected"
            )

    # =========================================================
    # TECH NICHE
    # =========================================================

    def _detect_tech_niche(
        self,
        context: TopicContext,
        topic: str,
    ) -> None:

        keywords = [
            "ai",
            "software",
            "python",
            "technology",
            "coding",
            "programming",
            "cybersecurity",
        ]

        if any(
            keyword in topic
            for keyword in keywords
        ):

            context.niche = "tech"

            context.article_type = (
                "technical_guide"
            )

            context.semantic_type = (
                "innovation"
            )

            context.is_evergreen_topic = True

            context.confidence = 0.85

            context.notes.append(
                "Tech niche detected"
            )

    # =========================================================
    # EDUCATION NICHE
    # =========================================================

    def _detect_education_niche(
        self,
        context: TopicContext,
        topic: str,
    ) -> None:

        keywords = [
            "education",
            "college",
            "university",
            "study",
            "syllabus",
            "exam pattern",
        ]

        if any(
            keyword in topic
            for keyword in keywords
        ):

            context.niche = "education"

            context.article_type = (
                "educational_guide"
            )

            context.semantic_type = (
                "learning"
            )

            context.faq_recommended = True

            context.tables_recommended = True

            context.confidence = 0.84

            context.notes.append(
                "Education niche detected"
            )

    # =========================================================
    # ARTICLE TYPE
    # =========================================================

    def _detect_article_type(
        self,
        context: TopicContext,
        topic: str,
    ) -> None:

        if "vs" in topic or "comparison" in topic:

            context.article_type = (
                "comparison"
            )

            context.is_comparison_topic = True

            context.tables_recommended = True

            context.notes.append(
                "Comparison article detected"
            )

        elif (
            "how to" in topic
            or "guide" in topic
            or "tutorial" in topic
        ):

            context.article_type = (
                "tutorial"
            )

            context.is_tutorial_topic = True

            context.notes.append(
                "Tutorial article detected"
            )

    # =========================================================
    # SEMANTIC TYPE
    # =========================================================

    def _detect_semantic_type(
        self,
        context: TopicContext,
        topic: str,
    ) -> None:

        if any(
            keyword in topic
            for keyword in [
                "latest",
                "breaking",
                "today",
                "update",
            ]
        ):

            context.semantic_type = (
                "real_time"
            )

            context.freshness_sensitive = True

            context.notes.append(
                "Real-time semantic intent detected"
            )

    # =========================================================
    # EDITORIAL REQUIREMENTS
    # =========================================================

    def _detect_editorial_requirements(
        self,
        context: TopicContext,
    ) -> None:

        if context.is_ymyl_topic:

            context.expert_tone_recommended = True

            context.notes.append(
                "Expert tone recommended"
            )

        if context.freshness_sensitive:

            context.notes.append(
                "Frequent updates recommended"
            )

    # =========================================================
    # DEFAULT
    # =========================================================

    def _apply_default_behavior(
        self,
        context: TopicContext,
    ) -> None:

        if context.niche == "default":

            context.notes.append(
                "Fallback topic classification used"
            )

    # =========================================================
    # EXPORT
    # =========================================================

    def export(
        self,
        context: TopicContext,
    ) -> Dict[str, Any]:

        return {
            "topic": context.topic,
            "niche": context.niche,
            "article_type": (
                context.article_type
            ),
            "semantic_type": (
                context.semantic_type
            ),
            "is_news_topic": (
                context.is_news_topic
            ),
            "is_evergreen_topic": (
                context.is_evergreen_topic
            ),
            "is_comparison_topic": (
                context.is_comparison_topic
            ),
            "is_tutorial_topic": (
                context.is_tutorial_topic
            ),
            "is_ymyl_topic": (
                context.is_ymyl_topic
            ),
            "faq_recommended": (
                context.faq_recommended
            ),
            "tables_recommended": (
                context.tables_recommended
            ),
            "expert_tone_recommended": (
                context.expert_tone_recommended
            ),
            "freshness_sensitive": (
                context.freshness_sensitive
            ),
            "confidence": (
                context.confidence
            ),
            "notes": context.notes,
        }