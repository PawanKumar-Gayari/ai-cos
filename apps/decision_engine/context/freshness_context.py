"""
Freshness Context Engine

This module evaluates freshness requirements of a topic
and provides signals for:
- update frequency
- maximum acceptable content age
- freshness criticality
- live verification necessity
"""

from dataclasses import dataclass, field
from typing import List


@dataclass
class FreshnessContext:

    freshness_required: bool = False

    max_age_days: int = 30

    update_frequency: str = "weekly"  # daily, weekly, monthly, hourly

    live_verification_required: bool = False

    notes: List[str] = field(default_factory=list)


class FreshnessContextEngine:

    """
    Determines freshness sensitivity based on:
    - topic type
    - niche
    - known time-critical patterns
    """

    def build(self, topic: str, niche: str = "default") -> FreshnessContext:

        context = FreshnessContext()

        topic = (topic or "").lower()
        niche = (niche or "").lower()

        # Critical freshness topics
        critical_keywords = [
            "recruitment",
            "admit card",
            "exam date",
            "result",
            "notification",
            "breaking",
            "latest",
            "update",
            "news",
        ]

        if any(keyword in topic for keyword in critical_keywords):
            context.freshness_required = True
            context.max_age_days = 1
            context.update_frequency = "daily"
            context.live_verification_required = True
            context.notes.append(
                "Freshness critical topic detected"
            )

        # Jobs niche
        elif niche == "jobs":
            context.freshness_required = True
            context.max_age_days = 2
            context.update_frequency = "daily"
            context.live_verification_required = True
            context.notes.append(
                "Jobs niche requires frequent updates"
            )

        # News/Trends
        elif niche in ["tech", "finance"]:
            context.freshness_required = True
            context.max_age_days = 3
            context.update_frequency = "daily"
            context.live_verification_required = False
            context.notes.append(
                f"{niche.capitalize()} topics are freshness sensitive"
            )

        # Evergreen topics
        else:
            context.freshness_required = False
            context.max_age_days = 30
            context.update_frequency = "weekly"
            context.live_verification_required = False
            context.notes.append(
                "Evergreen or static topic"
            )

        return context