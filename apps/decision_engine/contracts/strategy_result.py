"""
Strategy Result Contract

This module represents the strategy selection output from
the decision engine.

Goal:
Capture the final selected content strategy including:
- content structure
- article depth
- required features
- adaptive signals
- publishing constraints
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List


@dataclass
class StrategyResult:

    # =========================================================
    # ARTICLE STRUCTURE
    # =========================================================

    article_depth: str = "medium"  # low, medium, high, very_high

    faq_enabled: bool = False

    tables_enabled: bool = False

    comparison_enabled: bool = False

    step_by_step_enabled: bool = False

    citations_required: bool = False

    expert_tone_required: bool = False

    official_sources_required: bool = False

    adaptive_signals: Dict[str, Any] = field(
        default_factory=dict
    )

    strategy_notes: List[str] = field(
        default_factory=list
    )

    # =========================================================
    # CONSTRAINTS
    # =========================================================

    human_review_required: bool = False

    publishing_allowed: bool = True

    required_verification_score: float = 0.0

    required_quality_score: float = 0.0

    # =========================================================
    # REASONING
    # =========================================================

    applied_rules: List[str] = field(
        default_factory=list
    )

    warnings: List[str] = field(
        default_factory=list
    )

    recommendations: List[str] = field(
        default_factory=list
    )

    # =========================================================
    # METADATA
    # =========================================================

    metadata: Dict[str, Any] = field(
        default_factory=dict
    )

    # =========================================================
    # UTILITIES
    # =========================================================

    def add_rule(
        self,
        rule_name: str,
    ) -> None:

        if (
            rule_name
            and rule_name not in self.applied_rules
        ):

            self.applied_rules.append(rule_name)

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
            and recommendation not in self.recommendations
        ):

            self.recommendations.append(
                recommendation
            )

    def add_strategy_note(
        self,
        note: str,
    ) -> None:

        if note and note not in self.strategy_notes:

            self.strategy_notes.append(note)

    # =========================================================
    # EXPORT
    # =========================================================

    def to_dict(
        self,
    ) -> Dict[str, Any]:

        return {
            "article_depth": self.article_depth,
            "faq_enabled": self.faq_enabled,
            "tables_enabled": self.tables_enabled,
            "comparison_enabled": self.comparison_enabled,
            "step_by_step_enabled": self.step_by_step_enabled,
            "citations_required": self.citations_required,
            "expert_tone_required": self.expert_tone_required,
            "official_sources_required": self.official_sources_required,
            "adaptive_signals": self.adaptive_signals,
            "strategy_notes": self.strategy_notes,
            "human_review_required": self.human_review_required,
            "publishing_allowed": self.publishing_allowed,
            "required_verification_score": self.required_verification_score,
            "required_quality_score": self.required_quality_score,
            "applied_rules": self.applied_rules,
            "warnings": self.warnings,
            "recommendations": self.recommendations,
            "metadata": self.metadata,
        }