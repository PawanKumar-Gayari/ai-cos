"""
Claim Extractor

Purpose:
Extract factual claims from content using:
- sentence parsing
- factual pattern detection
- numerical claim detection
- entity extraction
- verification tagging

Goal:
Identify statements that require verification.

This becomes the claim extraction
layer of AI_COS.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List
import re


# =============================================================
# CLAIM
# =============================================================

@dataclass
class Claim:

    text: str = ""

    claim_type: str = "general"

    confidence: float = 0.0

    verification_required: bool = True

    numerical_claim: bool = False

    date_claim: bool = False

    entity_claim: bool = False

    reasoning: List[str] = field(
        default_factory=list
    )


# =============================================================
# RESULT
# =============================================================

@dataclass
class ClaimExtractorResult:

    total_claims: int = 0

    factual_claims: int = 0

    numerical_claims: int = 0

    date_claims: int = 0

    entity_claims: int = 0

    claims: List[Claim] = field(
        default_factory=list
    )

    extraction_score: float = 0.0

    reasoning: List[str] = field(
        default_factory=list
    )

    metadata: Dict[str, Any] = field(
        default_factory=dict
    )


# =============================================================
# CLAIM EXTRACTOR
# =============================================================

class ClaimExtractor:

    """
    Claim extraction intelligence engine.
    """

    YEAR_PATTERN = re.compile(
        r"\b(19|20)\d{2}\b"
    )

    NUMBER_PATTERN = re.compile(
        r"\b\d+(\.\d+)?\b"
    )

    ENTITY_TERMS = [

        "google",
        "openai",
        "microsoft",
        "india",
        "university",
        "government",
    ]

    # =========================================================
    # EXTRACT
    # =========================================================

    def extract(
        self,
        content: str,
    ) -> Dict[str, Any]:

        result = (
            ClaimExtractorResult()
        )

        content = (
            content or ""
        )

        sentences = [

            item.strip()

            for item
            in content.split(".")

            if item.strip()
        ]

        claims = []

        for sentence in sentences:

            claim = (
                self._process_claim(
                    sentence
                )
            )

            claims.append(
                claim
            )

        result.claims = claims

        result.total_claims = (
            len(claims)
        )

        result.factual_claims = sum(

            1

            for item
            in claims

            if item.verification_required
        )

        result.numerical_claims = sum(

            1

            for item
            in claims

            if item.numerical_claim
        )

        result.date_claims = sum(

            1

            for item
            in claims

            if item.date_claim
        )

        result.entity_claims = sum(

            1

            for item
            in claims

            if item.entity_claim
        )

        # =====================================================
        # SCORE
        # =====================================================

        if result.total_claims > 0:

            result.extraction_score = round(

                (
                    result.factual_claims
                    /
                    result.total_claims
                ) * 100,

                2,
            )

        result.reasoning.append(
            f"Extracted "
            f"{result.total_claims} claims"
        )

        return self.export(
            result
        )

    # =========================================================
    # PROCESS
    # =========================================================

    def _process_claim(
        self,
        sentence: str,
    ) -> Claim:

        claim = Claim()

        claim.text = sentence

        claim.confidence = 70.0

        # =====================================================
        # NUMERICAL
        # =====================================================

        if self.NUMBER_PATTERN.search(
            sentence
        ):

            claim.numerical_claim = (
                True
            )

            claim.claim_type = (
                "numerical"
            )

        # =====================================================
        # DATE
        # =====================================================

        if self.YEAR_PATTERN.search(
            sentence
        ):

            claim.date_claim = (
                True
            )

            claim.claim_type = (
                "date"
            )

        # =====================================================
        # ENTITY
        # =====================================================

        if any(

            item.lower() in sentence.lower()

            for item
            in self.ENTITY_TERMS
        ):

            claim.entity_claim = (
                True
            )

            claim.claim_type = (
                "entity"
            )

        claim.reasoning.append(
            f"Claim classified as "
            f"{claim.claim_type}"
        )

        return claim

    # =========================================================
    # EXPORT
    # =========================================================

    def export(
        self,
        result: ClaimExtractorResult,
    ) -> Dict[str, Any]:

        return {

            "total_claims": (
                result.total_claims
            ),

            "factual_claims": (
                result.factual_claims
            ),

            "numerical_claims": (
                result.numerical_claims
            ),

            "date_claims": (
                result.date_claims
            ),

            "entity_claims": (
                result.entity_claims
            ),

            "claims": [

                item.__dict__

                for item
                in result.claims
            ],

            "extraction_score": (
                result.extraction_score
            ),

            "reasoning": (
                result.reasoning
            ),

            "metadata": (
                result.metadata
            ),
        }