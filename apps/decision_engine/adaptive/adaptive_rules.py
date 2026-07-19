"""
Adaptive Rule Engine

This module dynamically adapts editorial and SEO behavior
based on topic context, niche profile, freshness needs,
authority requirements, and performance signals.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional


@dataclass
class AdaptiveRuleResult:
    """
    Result returned after adaptive rule execution.
    """

    applied_rules: List[str] = field(default_factory=list)

    seo_weight: float = 1.0
    quality_weight: float = 1.0
    freshness_weight: float = 1.0
    authority_weight: float = 1.0

    faq_enabled: bool = False
    tables_enabled: bool = False
    comparison_enabled: bool = False
    official_sources_required: bool = False

    verification_strictness: str = "medium"

    article_depth: str = "medium"

    confidence_modifier: float = 1.0

    notes: List[str] = field(default_factory=list)


class AdaptiveRuleEngine:
    """
    Dynamic adaptive intelligence layer.

    This engine modifies decision behavior based on:
    - niche profile
    - freshness requirements
    - authority requirements
    - competition level
    - search intent
    """

    def evaluate(
        self,
        context,
        niche_profile,
    ) -> AdaptiveRuleResult:

        result = AdaptiveRuleResult()

        self._apply_niche_rules(
            result,
            niche_profile,
        )

        self._apply_freshness_rules(
            result,
            context,
        )

        self._apply_intent_rules(
            result,
            context,
        )

        self._apply_competition_rules(
            result,
            context,
        )

        self._apply_authority_rules(
            result,
            context,
        )

        return result

    # =========================================================
    # NICHE RULES
    # =========================================================

    def _apply_niche_rules(
        self,
        result: AdaptiveRuleResult,
        profile,
    ) -> None:

        if profile.name == "jobs":

            result.faq_enabled = True
            result.tables_enabled = True

            result.official_sources_required = True

            result.freshness_weight = 1.5

            result.verification_strictness = "high"

            result.applied_rules.append(
                "jobs_profile_rules"
            )

        elif profile.name == "health":

            result.authority_weight = 1.8

            result.official_sources_required = True

            result.verification_strictness = "very_high"

            result.article_depth = "high"

            result.applied_rules.append(
                "health_profile_rules"
            )

        elif profile.name == "tech":

            result.comparison_enabled = True

            result.article_depth = "high"

            result.freshness_weight = 1.2

            result.applied_rules.append(
                "tech_profile_rules"
            )

    # =========================================================
    # FRESHNESS RULES
    # =========================================================

    def _apply_freshness_rules(
        self,
        result: AdaptiveRuleResult,
        context,
    ) -> None:

        if getattr(context, "freshness_required", False):

            result.freshness_weight += 0.5

            result.official_sources_required = True

            result.applied_rules.append(
                "freshness_required"
            )

            result.notes.append(
                "Fresh content validation enabled"
            )

    # =========================================================
    # INTENT RULES
    # =========================================================

    def _apply_intent_rules(
        self,
        result: AdaptiveRuleResult,
        context,
    ) -> None:

        intent = getattr(
            context,
            "intent",
            "informational",
        )

        if intent == "commercial":

            result.comparison_enabled = True

            result.tables_enabled = True

            result.applied_rules.append(
                "commercial_intent_rules"
            )

        elif intent == "informational":

            result.article_depth = "high"

            result.applied_rules.append(
                "informational_intent_rules"
            )

    # =========================================================
    # COMPETITION RULES
    # =========================================================

    def _apply_competition_rules(
        self,
        result: AdaptiveRuleResult,
        context,
    ) -> None:

        competition = getattr(
            context,
            "competition_level",
            "medium",
        )

        if competition == "high":

            result.seo_weight += 0.4

            result.quality_weight += 0.3

            result.article_depth = "very_high"

            result.applied_rules.append(
                "high_competition_rules"
            )

    # =========================================================
    # AUTHORITY RULES
    # =========================================================

    def _apply_authority_rules(
        self,
        result: AdaptiveRuleResult,
        context,
    ) -> None:

        authority_required = getattr(
            context,
            "authority_required",
            False,
        )

        if authority_required:

            result.authority_weight += 0.5

            result.article_depth = "high"

            result.applied_rules.append(
                "authority_required"
            )

    # =========================================================
    # FINAL EXPORT
    # =========================================================

    def export(
        self,
        result: AdaptiveRuleResult,
    ) -> Dict[str, Any]:

        return {
            "applied_rules": result.applied_rules,
            "seo_weight": result.seo_weight,
            "quality_weight": result.quality_weight,
            "freshness_weight": result.freshness_weight,
            "authority_weight": result.authority_weight,
            "faq_enabled": result.faq_enabled,
            "tables_enabled": result.tables_enabled,
            "comparison_enabled": result.comparison_enabled,
            "official_sources_required": result.official_sources_required,
            "verification_strictness": result.verification_strictness,
            "article_depth": result.article_depth,
            "confidence_modifier": result.confidence_modifier,
            "notes": result.notes,
        }