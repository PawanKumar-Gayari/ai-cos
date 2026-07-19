"""
Citation Extractor

Purpose:
Extract and evaluate citations from:
- URLs
- references
- inline citations
- source mentions
- authority references

Goal:
Measure citation quality and strengthen
verification reliability.

This becomes the citation intelligence
layer of AI_COS.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List
from urllib.parse import urlparse
import re


# =============================================================
# CITATION RESULT
# =============================================================

@dataclass
class Citation:

    # =========================================================
    # DATA
    # =========================================================

    raw: str = ""

    domain: str = ""

    citation_type: str = "unknown"

    # =========================================================
    # FLAGS
    # =========================================================

    valid: bool = False

    official_source: bool = False

    trusted_source: bool = False

    academic_source: bool = False

    government_source: bool = False

    # =========================================================
    # SCORES
    # =========================================================

    authority_score: float = 0.0

    trust_score: float = 0.0

    citation_quality_score: float = 0.0

    # =========================================================
    # RISKS
    # =========================================================

    spam_risk: str = "low"

    misinformation_risk: str = "low"

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
# EXTRACTION RESULT
# =============================================================

@dataclass
class CitationExtractorResult:

    # =========================================================
    # COUNTS
    # =========================================================

    total_citations: int = 0

    valid_citations: int = 0

    trusted_citations: int = 0

    weak_citations: int = 0

    # =========================================================
    # SCORES
    # =========================================================

    citation_score: float = 0.0

    authority_score: float = 0.0

    trust_score: float = 0.0

    # =========================================================
    # CITATIONS
    # =========================================================

    citations: List[Citation] = field(
        default_factory=list
    )

    # =========================================================
    # RISKS
    # =========================================================

    weak_citation_risk: str = "low"

    spam_citation_risk: str = "low"

    misinformation_risk: str = "low"

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
# CITATION EXTRACTOR
# =============================================================

class CitationExtractor:

    """
    Citation extraction and evaluation engine.
    """

    # =========================================================
    # TRUSTED DOMAINS
    # =========================================================

    TRUSTED_DOMAINS = [

        "google.com",
        "wikipedia.org",
        "github.com",
        "openai.com",
        "nih.gov",
        "who.int",
        "nature.com",
        "sciencedirect.com",
    ]

    # =========================================================
    # SPAM DOMAINS
    # =========================================================

    SPAM_SIGNALS = [

        "clickbait",
        "spam",
        "fake",
        "rumor",
        "cheap-seo",
    ]

    # =========================================================
    # URL REGEX
    # =========================================================

    URL_PATTERN = re.compile(

        r"https?://[^\s]+",

        re.IGNORECASE,
    )

    # =========================================================
    # EXTRACT
    # =========================================================

    def extract(
        self,
        content: str,
    ) -> Dict[str, Any]:

        result = (
            CitationExtractorResult()
        )

        content = (
            content or ""
        )

        # =====================================================
        # FIND URLS
        # =====================================================

        matches = self.URL_PATTERN.findall(
            content
        )

        # =====================================================
        # PROCESS
        # =====================================================

        citations = []

        for raw_url in matches:

            citation = (
                self._process_citation(
                    raw_url
                )
            )

            citations.append(
                citation
            )

        result.citations = citations

        # =====================================================
        # COUNTS
        # =====================================================

        result.total_citations = (
            len(citations)
        )

        result.valid_citations = sum(

            1

            for item in citations

            if item.valid
        )

        result.trusted_citations = sum(

            1

            for item in citations

            if item.trusted_source
        )

        result.weak_citations = sum(

            1

            for item in citations

            if item.citation_quality_score < 50
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
    # PROCESS
    # =========================================================

    def _process_citation(
        self,
        raw_url: str,
    ) -> Citation:

        citation = Citation()

        citation.raw = raw_url

        citation.domain = (
            self._extract_domain(
                raw_url
            )
        )

        citation.valid = (
            self._validate_url(
                raw_url
            )
        )

        # =====================================================
        # TYPE
        # =====================================================

        citation.citation_type = (
            self._detect_type(
                citation.domain
            )
        )

        # =====================================================
        # FLAGS
        # =====================================================

        if ".gov" in citation.domain:

            citation.government_source = (
                True
            )

            citation.official_source = (
                True
            )

        if ".edu" in citation.domain:

            citation.academic_source = (
                True
            )

        if any(

            item in citation.domain

            for item
            in self.TRUSTED_DOMAINS
        ):

            citation.trusted_source = (
                True
            )

        # =====================================================
        # SCORES
        # =====================================================

        citation.authority_score = (
            self._calculate_authority(
                citation
            )
        )

        citation.trust_score = (
            self._calculate_trust(
                citation
            )
        )

        citation.citation_quality_score = round(

            (
                citation.authority_score * 0.6
                +
                citation.trust_score * 0.4
            ),

            2,
        )

        # =====================================================
        # RISKS
        # =====================================================

        self._detect_citation_risks(
            citation
        )

        # =====================================================
        # REASONING
        # =====================================================

        citation.add_reasoning(
            f"Citation score: "
            f"{citation.citation_quality_score}"
        )

        return citation

    # =========================================================
    # DOMAIN
    # =========================================================

    def _extract_domain(
        self,
        url: str,
    ) -> str:

        try:

            parsed = (
                urlparse(url)
            )

            return parsed.netloc.lower()

        except Exception:

            return ""

    # =========================================================
    # VALIDATE
    # =========================================================

    def _validate_url(
        self,
        url: str,
    ) -> bool:

        return (

            url.startswith(
                "http://"
            )

            or

            url.startswith(
                "https://"
            )
        )

    # =========================================================
    # TYPE
    # =========================================================

    def _detect_type(
        self,
        domain: str,
    ) -> str:

        if ".gov" in domain:

            return "government"

        if ".edu" in domain:

            return "academic"

        if ".org" in domain:

            return "organization"

        if any(

            item in domain

            for item
            in [

                "news",
                "times",
                "media",
            ]
        ):

            return "news"

        return "general"

    # =========================================================
    # AUTHORITY
    # =========================================================

    def _calculate_authority(
        self,
        citation: Citation,
    ) -> float:

        score = 50.0

        if citation.official_source:

            score += 30

        if citation.academic_source:

            score += 20

        if citation.trusted_source:

            score += 15

        return min(score, 100)

    # =========================================================
    # TRUST
    # =========================================================

    def _calculate_trust(
        self,
        citation: Citation,
    ) -> float:

        score = 50.0

        if citation.valid:

            score += 15

        if citation.raw.startswith(
            "https://"
        ):

            score += 15

        if citation.government_source:

            score += 10

        return min(score, 100)

    # =========================================================
    # RISKS
    # =========================================================

    def _detect_citation_risks(
        self,
        citation: Citation,
    ) -> None:

        domain = citation.domain

        if any(

            item in domain

            for item
            in self.SPAM_SIGNALS
        ):

            citation.spam_risk = (
                "high"
            )

            citation.misinformation_risk = (
                "high"
            )

    # =========================================================
    # SCORES
    # =========================================================

    def _calculate_scores(
        self,
        result: CitationExtractorResult,
    ) -> None:

        if not result.citations:

            return

        authority_scores = [

            item.authority_score

            for item
            in result.citations
        ]

        trust_scores = [

            item.trust_score

            for item
            in result.citations
        ]

        citation_scores = [

            item.citation_quality_score

            for item
            in result.citations
        ]

        result.authority_score = round(

            sum(authority_scores)
            /
            len(authority_scores),

            2,
        )

        result.trust_score = round(

            sum(trust_scores)
            /
            len(trust_scores),

            2,
        )

        result.citation_score = round(

            sum(citation_scores)
            /
            len(citation_scores),

            2,
        )

    # =========================================================
    # RISKS
    # =========================================================

    def _detect_risks(
        self,
        result: CitationExtractorResult,
    ) -> None:

        # =====================================================
        # WEAK
        # =====================================================

        if result.citation_score < 50:

            result.weak_citation_risk = (
                "high"
            )

            result.add_warning(
                "Weak citation quality detected"
            )

        # =====================================================
        # SPAM
        # =====================================================

        spam_count = sum(

            1

            for item
            in result.citations

            if item.spam_risk == "high"
        )

        if spam_count >= 2:

            result.spam_citation_risk = (
                "high"
            )

            result.misinformation_risk = (
                "high"
            )

    # =========================================================
    # FINALIZE
    # =========================================================

    def _finalize(
        self,
        result: CitationExtractorResult,
    ) -> None:

        if result.trusted_citations == 0:

            result.add_recommendation(
                "Add trusted authority citations"
            )

            result.add_action(
                "Use official references"
            )

        if result.weak_citations > 2:

            result.add_recommendation(
                "Replace weak citations"
            )

        result.add_action(
            "Store citation intelligence"
        )

        result.add_reasoning(
            f"Citation score: "
            f"{result.citation_score}"
        )

    # =========================================================
    # EXPORT
    # =========================================================

    def export(
        self,
        result: CitationExtractorResult,
    ) -> Dict[str, Any]:

        return {

            "total_citations": (
                result.total_citations
            ),

            "valid_citations": (
                result.valid_citations
            ),

            "trusted_citations": (
                result.trusted_citations
            ),

            "weak_citations": (
                result.weak_citations
            ),

            "citation_score": (
                result.citation_score
            ),

            "authority_score": (
                result.authority_score
            ),

            "trust_score": (
                result.trust_score
            ),

            "citations": [

                item.__dict__

                for item
                in result.citations
            ],

            "weak_citation_risk": (
                result.weak_citation_risk
            ),

            "spam_citation_risk": (
                result.spam_citation_risk
            ),

            "misinformation_risk": (
                result.misinformation_risk
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