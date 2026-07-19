"""
Verified Facts Memory

Purpose:
Store VERIFIED factual intelligence.

Tracks:
- verified claims
- official sources
- fact confidence
- source trustworthiness
- freshness validity
- historical verification outcomes

Goal:
Prevent hallucinations and reuse trusted facts.

This becomes the factual memory layer
of AI_COS.
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional


# =============================================================
# VERIFIED FACT
# =============================================================

@dataclass
class VerifiedFactEntry:

    # =========================================================
    # FACT
    # =========================================================

    fact_id: str

    topic: str

    claim: str

    normalized_claim: str

    # =========================================================
    # VERIFICATION
    # =========================================================

    verified: bool = False

    verification_confidence: float = 0.0

    fact_confidence: float = 0.0

    # =========================================================
    # SOURCE
    # =========================================================

    source_url: str = ""

    source_name: str = ""

    source_type: str = "general"

    official_source: bool = False

    trusted_source: bool = False

    source_authority_score: float = 0.0

    # =========================================================
    # FRESHNESS
    # =========================================================

    verified_at: datetime = field(
        default_factory=datetime.utcnow
    )

    expires_at: Optional[datetime] = None

    freshness_days: int = 30

    freshness_valid: bool = True

    # =========================================================
    # FACT CATEGORY
    # =========================================================

    fact_type: str = "general"

    ymyl_sensitive: bool = False

    requires_reverification: bool = False

    # =========================================================
    # USAGE
    # =========================================================

    usage_count: int = 0

    successful_usage_count: int = 0

    failed_usage_count: int = 0

    # =========================================================
    # RISK
    # =========================================================

    contradiction_detected: bool = False

    outdated_detected: bool = False

    disputed_claim: bool = False

    # =========================================================
    # SIGNALS
    # =========================================================

    supporting_sources: List[str] = field(
        default_factory=list
    )

    contradiction_sources: List[str] = field(
        default_factory=list
    )

    verification_notes: List[str] = field(
        default_factory=list
    )

    # =========================================================
    # TIMESTAMPS
    # =========================================================

    created_at: datetime = field(
        default_factory=datetime.utcnow
    )

    updated_at: datetime = field(
        default_factory=datetime.utcnow
    )

    # =========================================================
    # META
    # =========================================================

    metadata: Dict[str, Any] = field(
        default_factory=dict
    )


# =============================================================
# VERIFIED FACTS MEMORY
# =============================================================

class VerifiedFactsMemory:

    """
    Persistent verified factual memory.
    """

    def __init__(
        self,
    ) -> None:

        self.fact_store: List[
            VerifiedFactEntry
        ] = []

    # =========================================================
    # STORE
    # =========================================================

    def store_fact(
        self,
        fact: VerifiedFactEntry,
    ) -> None:

        self.fact_store.append(
            fact
        )

    # =========================================================
    # FIND FACT
    # =========================================================

    def find_fact(
        self,
        normalized_claim: str,
    ) -> Optional[VerifiedFactEntry]:

        for fact in self.fact_store:

            if (
                fact.normalized_claim
                == normalized_claim
            ):

                return fact

        return None

    # =========================================================
    # FIND BY TOPIC
    # =========================================================

    def find_by_topic(
        self,
        topic: str,
    ) -> List[VerifiedFactEntry]:

        return [

            fact

            for fact in self.fact_store

            if fact.topic == topic
        ]

    # =========================================================
    # VERIFIED FACTS
    # =========================================================

    def verified_facts(
        self,
    ) -> List[VerifiedFactEntry]:

        return [

            fact

            for fact in self.fact_store

            if fact.verified
        ]

    # =========================================================
    # OFFICIAL FACTS
    # =========================================================

    def official_facts(
        self,
    ) -> List[VerifiedFactEntry]:

        return [

            fact

            for fact in self.fact_store

            if fact.official_source
        ]

    # =========================================================
    # TRUSTED FACTS
    # =========================================================

    def trusted_facts(
        self,
        min_confidence: float = 80.0,
    ) -> List[VerifiedFactEntry]:

        return [

            fact

            for fact in self.fact_store

            if (
                fact.fact_confidence
                >= min_confidence
            )
        ]

    # =========================================================
    # UPDATE USAGE
    # =========================================================

    def update_usage(
        self,
        fact_id: str,
        success: bool = True,
    ) -> bool:

        for fact in self.fact_store:

            if fact.fact_id == fact_id:

                fact.usage_count += 1

                if success:

                    fact.successful_usage_count += 1

                else:

                    fact.failed_usage_count += 1

                fact.updated_at = (
                    datetime.utcnow()
                )

                return True

        return False

    # =========================================================
    # REVERIFY CHECK
    # =========================================================

    def facts_requiring_reverification(
        self,
    ) -> List[VerifiedFactEntry]:

        now = datetime.utcnow()

        results = []

        for fact in self.fact_store:

            if fact.expires_at:

                if now >= fact.expires_at:

                    fact.requires_reverification = (
                        True
                    )

                    fact.freshness_valid = False

                    results.append(fact)

        return results

    # =========================================================
    # OUTDATED FACTS
    # =========================================================

    def outdated_facts(
        self,
    ) -> List[VerifiedFactEntry]:

        return [

            fact

            for fact in self.fact_store

            if fact.outdated_detected
        ]

    # =========================================================
    # CONTRADICTED FACTS
    # =========================================================

    def contradicted_facts(
        self,
    ) -> List[VerifiedFactEntry]:

        return [

            fact

            for fact in self.fact_store

            if fact.contradiction_detected
        ]

    # =========================================================
    # SUCCESS RATE
    # =========================================================

    def fact_success_rate(
        self,
    ) -> float:

        verified = self.verified_facts()

        if not verified:
            return 0.0

        successful = len([

            fact

            for fact in verified

            if (
                fact.successful_usage_count >
                fact.failed_usage_count
            )
        ])

        return round(

            (
                successful /
                len(verified)
            ) * 100,

            2,
        )

    # =========================================================
    # TRUSTED SOURCE RATE
    # =========================================================

    def trusted_source_rate(
        self,
    ) -> float:

        if not self.fact_store:
            return 0.0

        trusted = len([

            fact

            for fact in self.fact_store

            if fact.trusted_source
        ])

        return round(

            (
                trusted /
                len(self.fact_store)
            ) * 100,

            2,
        )

    # =========================================================
    # OFFICIAL SOURCE RATE
    # =========================================================

    def official_source_rate(
        self,
    ) -> float:

        if not self.fact_store:
            return 0.0

        official = len([

            fact

            for fact in self.fact_store

            if fact.official_source
        ])

        return round(

            (
                official /
                len(self.fact_store)
            ) * 100,

            2,
        )

    # =========================================================
    # ADD SUPPORTING SOURCE
    # =========================================================

    def add_supporting_source(
        self,
        fact_id: str,
        source_url: str,
    ) -> bool:

        for fact in self.fact_store:

            if fact.fact_id == fact_id:

                if (
                    source_url
                    not in fact.supporting_sources
                ):

                    fact.supporting_sources.append(
                        source_url
                    )

                return True

        return False

    # =========================================================
    # MARK CONTRADICTION
    # =========================================================

    def mark_contradiction(
        self,
        fact_id: str,
        contradiction_source: str,
    ) -> bool:

        for fact in self.fact_store:

            if fact.fact_id == fact_id:

                fact.contradiction_detected = (
                    True
                )

                fact.disputed_claim = True

                fact.freshness_valid = False

                if (
                    contradiction_source
                    not in fact.contradiction_sources
                ):

                    fact.contradiction_sources.append(
                        contradiction_source
                    )

                return True

        return False

    # =========================================================
    # AUTO EXPIRY
    # =========================================================

    def apply_auto_expiry(
        self,
    ) -> None:

        for fact in self.fact_store:

            fact.expires_at = (

                fact.verified_at +

                timedelta(
                    days=fact.freshness_days
                )
            )

    # =========================================================
    # EXPORT
    # =========================================================

    def export_memory(
        self,
    ) -> Dict[str, Any]:

        return {

            "total_facts": (
                len(self.fact_store)
            ),

            "verified_facts": (
                len(
                    self.verified_facts()
                )
            ),

            "official_facts": (
                len(
                    self.official_facts()
                )
            ),

            "trusted_facts": (
                len(
                    self.trusted_facts()
                )
            ),

            "outdated_facts": (
                len(
                    self.outdated_facts()
                )
            ),

            "contradicted_facts": (
                len(
                    self.contradicted_facts()
                )
            ),

            "fact_success_rate": (
                self.fact_success_rate()
            ),

            "trusted_source_rate": (
                self.trusted_source_rate()
            ),

            "official_source_rate": (
                self.official_source_rate()
            ),

            "facts_requiring_reverification": (
                len(
                    self.facts_requiring_reverification()
                )
            ),
        }