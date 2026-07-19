"""
Fact Matcher

Purpose:
Match extracted claims against:
- verified facts
- trusted references
- temporal consistency
- entity consistency
- numerical validation

Goal:
Determine whether claims align with
known verified information.

This becomes the fact matching
intelligence layer of AI_COS.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List
import re


# =============================================================
# FACT MATCH
# =============================================================

@dataclass
class FactMatch:

    # =========================================================
    # DATA
    # =========================================================

    claim: str = ""

    matched_fact: str = ""

    match_type: str = "general"

    # =========================================================
    # SCORES
    # =========================================================

    similarity_score: float = 0.0

    confidence_score: float = 0.0

    verification_score: float = 0.0

    # =========================================================
    # FLAGS
    # =========================================================

    exact_match: bool = False

    partial_match: bool = False

    numerical_match: bool = False

    entity_match: bool = False

    temporal_match: bool = False

    # =========================================================
    # RISKS
    # =========================================================

    misinformation_risk: str = "low"

    trust_risk: str = "low"

    # =========================================================
    # REASONING
    # =========================================================

    reasoning: List[str] = field(
        default_factory=list
    )

    metadata: Dict[str, Any] = field(
        default_factory=dict
    )

    # =========================================================
    # UTILITIES
    # =========================================================

    def add_reasoning(
        self,
        message: str,
    ) -> None:

        if (
            message
            and message not in self.reasoning
        ):

            self.reasoning.append(message)


# =============================================================
# RESULT
# =============================================================

@dataclass
class FactMatcherResult:

    # =========================================================
    # COUNTS
    # =========================================================

    total_claims: int = 0

    matched_claims: int = 0

    unmatched_claims: int = 0

    exact_matches: int = 0

    partial_matches: int = 0

    # =========================================================
    # SCORES
    # =========================================================

    verification_score: float = 0.0

    match_confidence_score: float = 0.0

    factual_accuracy_score: float = 0.0

    # =========================================================
    # MATCHES
    # =========================================================

    matches: List[FactMatch] = field(
        default_factory=list
    )

    unmatched_claim_list: List[str] = field(
        default_factory=list
    )

    # =========================================================
    # RISKS
    # =========================================================

    misinformation_risk: str = "low"

    factual_gap_risk: str = "low"

    trust_decay_risk: str = "low"

    # =========================================================
    # RECOMMENDATIONS
    # =========================================================

    recommendations: List[str] = field(
        default_factory=list
    )

    warnings: List[str] = field(
        default_factory=list
    )

    reasoning: List[str] = field(
        default_factory=list
    )

    # =========================================================
    # ACTIONS
    # =========================================================

    recommended_actions: List[str] = field(
        default_factory=list
    )

    metadata: Dict[str, Any] = field(
        default_factory=dict
    )

    # =========================================================
    # UTILITIES
    # =========================================================

    def add_reasoning(
        self,
        message: str,
    ) -> None:

        if (
            message
            and message not in self.reasoning
        ):

            self.reasoning.append(message)

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
            and recommendation
            not in self.recommendations
        ):

            self.recommendations.append(
                recommendation
            )

    def add_action(
        self,
        action: str,
    ) -> None:

        if (
            action
            and action
            not in self.recommended_actions
        ):

            self.recommended_actions.append(
                action
            )


# =============================================================
# FACT MATCHER
# =============================================================

class FactMatcher:

    """
    Fact matching intelligence engine.
    """

    # =========================================================
    # ENTITY TERMS
    # =========================================================

    ENTITY_TERMS = [

        "google",
        "openai",
        "microsoft",
        "india",
        "government",
        "university",
    ]

    # =========================================================
    # YEAR PATTERN
    # =========================================================

    YEAR_PATTERN = re.compile(
        r"\b(20\d{2})\b"
    )

    # =========================================================
    # NUMBER PATTERN
    # =========================================================

    NUMBER_PATTERN = re.compile(
        r"\b\d+(?:\\.\d+)?\b"
    )

    # =========================================================
    # MATCH
    # =========================================================

    def match(
        self,
        claims: List[str],
        verified_facts: List[str],
    ) -> Dict[str, Any]:

        result = (
            FactMatcherResult()
        )

        claims = claims or []

        verified_facts = (
            verified_facts or []
        )

        result.total_claims = (
            len(claims)
        )

        matches = []

        unmatched = []

        # =====================================================
        # PROCESS CLAIMS
        # =====================================================

        for claim in claims:

            best_match = None

            best_score = 0.0

            for fact in verified_facts:

                match = self._analyze_match(
                    claim,
                    fact,
                )

                if (

                    match.verification_score
                    > best_score
                ):

                    best_score = (
                        match.verification_score
                    )

                    best_match = match

            # =================================================
            # STORE
            # =================================================

            if (

                best_match
                and
                best_match.verification_score
                >= 50
            ):

                matches.append(
                    best_match
                )

            else:

                unmatched.append(
                    claim
                )

        result.matches = matches

        result.unmatched_claim_list = (
            unmatched
        )

        # =====================================================
        # COUNTS
        # =====================================================

        result.matched_claims = (
            len(matches)
        )

        result.unmatched_claims = (
            len(unmatched)
        )

        result.exact_matches = sum(

            1

            for item
            in matches

            if item.exact_match
        )

        result.partial_matches = sum(

            1

            for item
            in matches

            if item.partial_match
        )

        # =====================================================
        # SCORES
        # =====================================================

        self._calculate_scores(
            result
        )

        # =====================================================
        # RISKS
        # =====================================================

        self._detect_risks(
            result
        )

        # =====================================================
        # FINALIZE
        # =====================================================

        self._finalize(
            result
        )

        return self.export(
            result
        )

    # =========================================================
    # ANALYZE MATCH
    # =========================================================

    def _analyze_match(
        self,
        claim: str,
        fact: str,
    ) -> FactMatch:

        match = FactMatch()

        match.claim = claim

        match.matched_fact = fact

        claim_lower = claim.lower()

        fact_lower = fact.lower()

        similarity = 0.0

        # =====================================================
        # TOKEN MATCHING
        # =====================================================

        claim_tokens = set(
            claim_lower.split()
        )

        fact_tokens = set(
            fact_lower.split()
        )

        common_tokens = (
            claim_tokens.intersection(
                fact_tokens
            )
        )

        if claim_tokens:

            similarity = (

                len(common_tokens)
                /
                len(claim_tokens)
            ) * 100

        match.similarity_score = round(

            similarity,

            2,
        )

        # =====================================================
        # EXACT
        # =====================================================

        if claim_lower == fact_lower:

            match.exact_match = (
                True
            )

            match.match_type = (
                "exact"
            )

            match.similarity_score = (
                100.0
            )

        # =====================================================
        # PARTIAL
        # =====================================================

        elif similarity >= 50:

            match.partial_match = (
                True
            )

            match.match_type = (
                "partial"
            )

        # =====================================================
        # NUMERICAL
        # =====================================================

        claim_numbers = self.NUMBER_PATTERN.findall(
            claim
        )

        fact_numbers = self.NUMBER_PATTERN.findall(
            fact
        )

        if (

            claim_numbers
            and
            fact_numbers
            and
            claim_numbers == fact_numbers
        ):

            match.numerical_match = (
                True
            )

            similarity += 15

        # =====================================================
        # TEMPORAL
        # =====================================================

        claim_years = self.YEAR_PATTERN.findall(
            claim
        )

        fact_years = self.YEAR_PATTERN.findall(
            fact
        )

        if (

            claim_years
            and
            fact_years
            and
            claim_years == fact_years
        ):

            match.temporal_match = (
                True
            )

            similarity += 10

        # =====================================================
        # ENTITY
        # =====================================================

        entity_match = any(

            item in claim_lower
            and
            item in fact_lower

            for item
            in self.ENTITY_TERMS
        )

        if entity_match:

            match.entity_match = (
                True
            )

            similarity += 10

        # =====================================================
        # FINAL SCORES
        # =====================================================

        match.confidence_score = min(

            similarity,

            100,
        )

        match.verification_score = round(

            match.confidence_score * 0.95,

            2,
        )

        # =====================================================
        # RISKS
        # =====================================================

        if match.verification_score < 50:

            match.misinformation_risk = (
                "medium"
            )

            match.trust_risk = (
                "medium"
            )

        match.add_reasoning(
            f"Match type: "
            f"{match.match_type}"
        )

        return match

    # =========================================================
    # SCORES
    # =========================================================

    def _calculate_scores(
        self,
        result: FactMatcherResult,
    ) -> None:

        if result.total_claims == 0:

            return

        result.verification_score = round(

            (
                result.matched_claims
                /
                result.total_claims
            ) * 100,

            2,
        )

        if result.matches:

            confidence_scores = [

                item.confidence_score

                for item
                in result.matches
            ]

            result.match_confidence_score = round(

                sum(confidence_scores)
                /
                len(confidence_scores),

                2,
            )

        result.factual_accuracy_score = round(

            (
                result.verification_score * 0.7
                +
                result.match_confidence_score * 0.3
            ),

            2,
        )

    # =========================================================
    # RISKS
    # =========================================================

    def _detect_risks(
        self,
        result: FactMatcherResult,
    ) -> None:

        # =====================================================
        # MISINFORMATION
        # =====================================================

        if result.verification_score < 50:

            result.misinformation_risk = (
                "high"
            )

            result.add_warning(
                "Low claim verification score detected"
            )

        # =====================================================
        # FACTUAL GAP
        # =====================================================

        if result.unmatched_claims >= 2:

            result.factual_gap_risk = (
                "high"
            )

        # =====================================================
        # TRUST
        # =====================================================

        if result.factual_accuracy_score < 60:

            result.trust_decay_risk = (
                "medium"
            )

    # =========================================================
    # FINALIZE
    # =========================================================

    def _finalize(
        self,
        result: FactMatcherResult,
    ) -> None:

        # =====================================================
        # RECOMMENDATIONS
        # =====================================================

        if result.unmatched_claims > 0:

            result.add_recommendation(
                "Verify unmatched claims manually"
            )

            result.add_action(
                "Run external fact validation"
            )

        if result.verification_score < 70:

            result.add_recommendation(
                "Increase verified reference coverage"
            )

        if result.exact_matches == 0:

            result.add_recommendation(
                "Add authoritative factual references"
            )

        result.add_action(
            "Store fact matching intelligence"
        )

        result.add_reasoning(
            f"Verification score: "
            f"{result.verification_score}"
        )

    # =========================================================
    # EXPORT
    # =========================================================

    def export(
        self,
        result: FactMatcherResult,
    ) -> Dict[str, Any]:

        return {

            "total_claims": (
                result.total_claims
            ),

            "matched_claims": (
                result.matched_claims
            ),

            "unmatched_claims": (
                result.unmatched_claims
            ),

            "exact_matches": (
                result.exact_matches
            ),

            "partial_matches": (
                result.partial_matches
            ),

            "verification_score": (
                result.verification_score
            ),

            "match_confidence_score": (
                result.match_confidence_score
            ),

            "factual_accuracy_score": (
                result.factual_accuracy_score
            ),

            "matches": [

                item.__dict__

                for item
                in result.matches
            ],

            "unmatched_claim_list": (
                result.unmatched_claim_list
            ),

            "misinformation_risk": (
                result.misinformation_risk
            ),

            "factual_gap_risk": (
                result.factual_gap_risk
            ),

            "trust_decay_risk": (
                result.trust_decay_risk
            ),

            "recommendations": (
                result.recommendations
            ),

            "warnings": (
                result.warnings
            ),

            "reasoning": (
                result.reasoning
            ),

            "recommended_actions": (
                result.recommended_actions
            ),

            "metadata": (
                result.metadata
            ),
        }