"""
Adaptive Weight Intelligence System

This module dynamically adjusts scoring weights
based on:
- niche profile
- freshness importance
- authority requirements
- competition level
- intent
- performance feedback

Goal:
Replace static scoring with adaptive contextual scoring.
"""

from dataclasses import dataclass, field
from typing import Dict, Any


@dataclass
class AdaptiveWeights:

    seo_weight: float = 1.0

    quality_weight: float = 1.0

    freshness_weight: float = 1.0

    authority_weight: float = 1.0

    engagement_weight: float = 1.0

    trust_weight: float = 1.0

    competition_weight: float = 1.0

    verification_weight: float = 1.0

    confidence_weight: float = 1.0

    notes: list[str] = field(default_factory=list)


class AdaptiveWeightEngine:

    """
    Dynamic scoring weight engine.

    This system adapts decision weights
    depending on:
    - topic type
    - SERP competition
    - freshness sensitivity
    - authority requirements
    - search intent
    """

    def calculate(
        self,
        context,
        niche_profile,
    ) -> AdaptiveWeights:

        weights = AdaptiveWeights()

        self._apply_niche_weights(
            weights,
            niche_profile,
        )

        self._apply_freshness_weights(
            weights,
            context,
        )

        self._apply_authority_weights(
            weights,
            context,
        )

        self._apply_competition_weights(
            weights,
            context,
        )

        self._apply_intent_weights(
            weights,
            context,
        )

        self._normalize(weights)

        return weights

    # =========================================================
    # NICHE WEIGHTS
    # =========================================================

    def _apply_niche_weights(
        self,
        weights: AdaptiveWeights,
        profile,
    ) -> None:

        if profile.name == "jobs":

            weights.freshness_weight += 0.8

            weights.verification_weight += 0.7

            weights.trust_weight += 0.6

            weights.notes.append(
                "Jobs niche prioritizes freshness and verification"
            )

        elif profile.name == "health":

            weights.authority_weight += 1.0

            weights.verification_weight += 1.0

            weights.trust_weight += 0.8

            weights.quality_weight += 0.5

            weights.notes.append(
                "Health niche prioritizes authority and trust"
            )

        elif profile.name == "finance":

            weights.authority_weight += 0.8

            weights.verification_weight += 0.9

            weights.trust_weight += 0.9

            weights.notes.append(
                "Finance niche requires high trust"
            )

        elif profile.name == "tech":

            weights.freshness_weight += 0.4

            weights.engagement_weight += 0.3

            weights.notes.append(
                "Tech niche values freshness and engagement"
            )

        elif profile.name == "education":

            weights.quality_weight += 0.6

            weights.authority_weight += 0.4

            weights.notes.append(
                "Education niche prioritizes depth and clarity"
            )

    # =========================================================
    # FRESHNESS WEIGHTS
    # =========================================================

    def _apply_freshness_weights(
        self,
        weights: AdaptiveWeights,
        context,
    ) -> None:

        freshness_required = getattr(
            context,
            "freshness_required",
            False,
        )

        if freshness_required:

            weights.freshness_weight += 0.7

            weights.verification_weight += 0.4

            weights.notes.append(
                "Freshness-sensitive topic detected"
            )

    # =========================================================
    # AUTHORITY WEIGHTS
    # =========================================================

    def _apply_authority_weights(
        self,
        weights: AdaptiveWeights,
        context,
    ) -> None:

        authority_required = getattr(
            context,
            "authority_required",
            False,
        )

        if authority_required:

            weights.authority_weight += 0.7

            weights.trust_weight += 0.5

            weights.notes.append(
                "Authority requirement detected"
            )

    # =========================================================
    # COMPETITION WEIGHTS
    # =========================================================

    def _apply_competition_weights(
        self,
        weights: AdaptiveWeights,
        context,
    ) -> None:

        competition_level = getattr(
            context,
            "competition_level",
            "medium",
        )

        if competition_level == "high":

            weights.seo_weight += 0.6

            weights.quality_weight += 0.5

            weights.engagement_weight += 0.3

            weights.notes.append(
                "High competition detected"
            )

        elif competition_level == "very_high":

            weights.seo_weight += 1.0

            weights.quality_weight += 0.8

            weights.engagement_weight += 0.5

            weights.authority_weight += 0.4

            weights.notes.append(
                "Very high competition environment"
            )

    # =========================================================
    # INTENT WEIGHTS
    # =========================================================

    def _apply_intent_weights(
        self,
        weights: AdaptiveWeights,
        context,
    ) -> None:

        intent = getattr(
            context,
            "intent",
            "informational",
        )

        if intent == "commercial":

            weights.engagement_weight += 0.5

            weights.seo_weight += 0.4

            weights.notes.append(
                "Commercial intent optimization enabled"
            )

        elif intent == "informational":

            weights.quality_weight += 0.4

            weights.authority_weight += 0.3

            weights.notes.append(
                "Informational intent prioritizes depth"
            )

        elif intent == "transactional":

            weights.seo_weight += 0.5

            weights.engagement_weight += 0.6

            weights.notes.append(
                "Transactional intent detected"
            )

    # =========================================================
    # NORMALIZATION
    # =========================================================

    def _normalize(
        self,
        weights: AdaptiveWeights,
    ) -> None:

        minimum = 0.5
        maximum = 3.0

        for field_name in vars(weights):

            value = getattr(weights, field_name)

            if isinstance(value, float):

                if value < minimum:
                    setattr(
                        weights,
                        field_name,
                        minimum,
                    )

                elif value > maximum:
                    setattr(
                        weights,
                        field_name,
                        maximum,
                    )

    # =========================================================
    # EXPORT
    # =========================================================

    def export(
        self,
        weights: AdaptiveWeights,
    ) -> Dict[str, Any]:

        return {
            "seo_weight": weights.seo_weight,
            "quality_weight": weights.quality_weight,
            "freshness_weight": weights.freshness_weight,
            "authority_weight": weights.authority_weight,
            "engagement_weight": weights.engagement_weight,
            "trust_weight": weights.trust_weight,
            "competition_weight": weights.competition_weight,
            "verification_weight": weights.verification_weight,
            "confidence_weight": weights.confidence_weight,
            "notes": weights.notes,
        }