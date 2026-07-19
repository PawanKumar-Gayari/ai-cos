"""
Authority Context Engine

This module evaluates:
- authority requirements
- trust sensitivity
- YMYL risk
- official source dependency
- verification strictness

Goal:
Determine how much trust, authority,
and verification a topic requires.

Examples:
- Health → very high authority
- Finance → very high trust
- Jobs → official verification required
- Entertainment → lower authority requirements
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any


# =============================================================
# AUTHORITY CONTEXT
# =============================================================

@dataclass
class AuthorityContext:

    # =========================================================
    # CORE
    # =========================================================

    authority_required: bool = False

    official_sources_required: bool = False

    ymyl_sensitive: bool = False

    # =========================================================
    # TRUST
    # =========================================================

    trust_level: str = "medium"

    verification_strictness: str = "medium"

    fact_accuracy_priority: bool = False

    # =========================================================
    # CONTENT
    # =========================================================

    expert_review_recommended: bool = False

    citation_required: bool = False

    # =========================================================
    # SOURCE PREFERENCES
    # =========================================================

    preferred_sources: List[str] = field(
        default_factory=list
    )

    restricted_sources: List[str] = field(
        default_factory=list
    )

    # =========================================================
    # SCORING
    # =========================================================

    authority_score: float = 1.0

    trust_score: float = 1.0

    # =========================================================
    # NOTES
    # =========================================================

    notes: List[str] = field(
        default_factory=list
    )


# =============================================================
# AUTHORITY CONTEXT ENGINE
# =============================================================

class AuthorityContextEngine:

    """
    Determines authority and trust requirements
    based on topic type and niche.
    """

    # =========================================================
    # MAIN ENTRY
    # =========================================================

    def build(
        self,
        topic: str,
        niche: str = "default",
    ) -> AuthorityContext:

        context = AuthorityContext()

        topic = (topic or "").lower()
        niche = (niche or "").lower()

        self._apply_health_rules(
            context,
            topic,
            niche,
        )

        self._apply_finance_rules(
            context,
            topic,
            niche,
        )

        self._apply_jobs_rules(
            context,
            topic,
            niche,
        )

        self._apply_education_rules(
            context,
            topic,
            niche,
        )

        self._apply_default_rules(
            context,
        )

        return context

    # =========================================================
    # HEALTH RULES
    # =========================================================

    def _apply_health_rules(
        self,
        context: AuthorityContext,
        topic: str,
        niche: str,
    ) -> None:

        health_keywords = [
            "health",
            "disease",
            "treatment",
            "medicine",
            "symptoms",
            "therapy",
            "hospital",
        ]

        if (
            niche == "health"
            or any(
                keyword in topic
                for keyword in health_keywords
            )
        ):

            context.authority_required = True

            context.official_sources_required = True

            context.ymyl_sensitive = True

            context.trust_level = "very_high"

            context.verification_strictness = (
                "very_high"
            )

            context.fact_accuracy_priority = True

            context.expert_review_recommended = True

            context.citation_required = True

            context.authority_score = 2.0

            context.trust_score = 2.0

            context.preferred_sources.extend([
                "WHO",
                "CDC",
                "NIH",
                "PubMed",
            ])

            context.notes.append(
                "Health topic requires strong authority verification"
            )

    # =========================================================
    # FINANCE RULES
    # =========================================================

    def _apply_finance_rules(
        self,
        context: AuthorityContext,
        topic: str,
        niche: str,
    ) -> None:

        finance_keywords = [
            "loan",
            "bank",
            "stock",
            "investment",
            "tax",
            "finance",
            "insurance",
        ]

        if (
            niche == "finance"
            or any(
                keyword in topic
                for keyword in finance_keywords
            )
        ):

            context.authority_required = True

            context.official_sources_required = True

            context.ymyl_sensitive = True

            context.trust_level = "very_high"

            context.verification_strictness = (
                "very_high"
            )

            context.fact_accuracy_priority = True

            context.citation_required = True

            context.authority_score = 1.9

            context.trust_score = 2.0

            context.preferred_sources.extend([
                "RBI",
                "SEBI",
                "official exchanges",
            ])

            context.notes.append(
                "Finance topic requires high trust validation"
            )

    # =========================================================
    # JOBS RULES
    # =========================================================

    def _apply_jobs_rules(
        self,
        context: AuthorityContext,
        topic: str,
        niche: str,
    ) -> None:

        jobs_keywords = [
            "recruitment",
            "vacancy",
            "notification",
            "exam",
            "admit card",
            "result",
        ]

        if (
            niche == "jobs"
            or any(
                keyword in topic
                for keyword in jobs_keywords
            )
        ):

            context.authority_required = True

            context.official_sources_required = True

            context.trust_level = "high"

            context.verification_strictness = "high"

            context.fact_accuracy_priority = True

            context.citation_required = True

            context.authority_score = 1.7

            context.trust_score = 1.8

            context.preferred_sources.extend([
                ".gov.in",
                ".nic.in",
                "official recruitment portals",
            ])

            context.notes.append(
                "Job notifications require official verification"
            )

    # =========================================================
    # EDUCATION RULES
    # =========================================================

    def _apply_education_rules(
        self,
        context: AuthorityContext,
        topic: str,
        niche: str,
    ) -> None:

        education_keywords = [
            "syllabus",
            "college",
            "university",
            "education",
            "exam pattern",
        ]

        if (
            niche == "education"
            or any(
                keyword in topic
                for keyword in education_keywords
            )
        ):

            context.authority_required = True

            context.trust_level = "high"

            context.verification_strictness = "high"

            context.citation_required = True

            context.authority_score = 1.5

            context.trust_score = 1.5

            context.preferred_sources.extend([
                "official universities",
                "education boards",
            ])

            context.notes.append(
                "Educational accuracy important"
            )

    # =========================================================
    # DEFAULT RULES
    # =========================================================

    def _apply_default_rules(
        self,
        context: AuthorityContext,
    ) -> None:

        if not context.preferred_sources:

            context.preferred_sources.extend([
                "official documentation",
                "trusted publications",
            ])

    # =========================================================
    # EXPORT
    # =========================================================

    def export(
        self,
        context: AuthorityContext,
    ) -> Dict[str, Any]:

        return {
            "authority_required": (
                context.authority_required
            ),
            "official_sources_required": (
                context.official_sources_required
            ),
            "ymyl_sensitive": (
                context.ymyl_sensitive
            ),
            "trust_level": (
                context.trust_level
            ),
            "verification_strictness": (
                context.verification_strictness
            ),
            "fact_accuracy_priority": (
                context.fact_accuracy_priority
            ),
            "expert_review_recommended": (
                context.expert_review_recommended
            ),
            "citation_required": (
                context.citation_required
            ),
            "preferred_sources": (
                context.preferred_sources
            ),
            "restricted_sources": (
                context.restricted_sources
            ),
            "authority_score": (
                context.authority_score
            ),
            "trust_score": (
                context.trust_score
            ),
            "notes": context.notes,
        }