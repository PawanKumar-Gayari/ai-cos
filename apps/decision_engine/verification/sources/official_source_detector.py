"""
Official Source Detector

Purpose:
Detect whether a source is:
- official
- governmental
- academic
- organizational
- trusted institutional
- authoritative

Goal:
Identify high-trust official sources for:
- factual verification
- citation reinforcement
- E-E-A-T optimization
- hallucination prevention

This becomes the official source
intelligence layer of AI_COS.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List
from urllib.parse import urlparse


# =============================================================
# DETECTOR RESULT
# =============================================================

@dataclass
class OfficialSourceResult:

    # =========================================================
    # SOURCE
    # =========================================================

    source: str = ""

    domain: str = ""

    # =========================================================
    # FLAGS
    # =========================================================

    official: bool = False

    government: bool = False

    educational: bool = False

    nonprofit: bool = False

    international: bool = False

    news_organization: bool = False

    research_source: bool = False

    # =========================================================
    # SCORES
    # =========================================================

    official_score: float = 0.0

    trust_score: float = 0.0

    authority_score: float = 0.0

    # =========================================================
    # SIGNALS
    # =========================================================

    official_tld_detected: bool = False

    known_authority_detected: bool = False

    institutional_signal_detected: bool = False

    # =========================================================
    # RISKS
    # =========================================================

    fake_official_risk: str = "low"

    spoofing_risk: str = "low"

    misinformation_risk: str = "low"

    # =========================================================
    # CLASSIFICATION
    # =========================================================

    source_type: str = "general"

    confidence_level: str = "medium"

    # =========================================================
    # REASONING
    # =========================================================

    reasoning: List[str] = field(
        default_factory=list
    )

    warnings: List[str] = field(
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


# =============================================================
# OFFICIAL SOURCE DETECTOR
# =============================================================

class OfficialSourceDetector:

    """
    Official authority source detection engine.
    """

    # =========================================================
    # GOVERNMENT TLDS
    # =========================================================

    GOVERNMENT_TLDS = [

        ".gov",
        ".gov.in",
        ".nic.in",
    ]

    # =========================================================
    # EDUCATIONAL TLDS
    # =========================================================

    EDUCATIONAL_TLDS = [

        ".edu",
        ".ac.in",
        ".edu.in",
    ]

    # =========================================================
    # INTERNATIONAL
    # =========================================================

    INTERNATIONAL_DOMAINS = [

        "who.int",
        "un.org",
        "unesco.org",
        "worldbank.org",
    ]

    # =========================================================
    # RESEARCH DOMAINS
    # =========================================================

    RESEARCH_DOMAINS = [

        "nature.com",
        "sciencedirect.com",
        "springer.com",
        "nih.gov",
        "pubmed.ncbi.nlm.nih.gov",
    ]

    # =========================================================
    # TRUSTED AUTHORITIES
    # =========================================================

    TRUSTED_AUTHORITIES = [

        "google.com",
        "github.com",
        "microsoft.com",
        "openai.com",
        "wikipedia.org",
    ]

    # =========================================================
    # SPOOFING SIGNALS
    # =========================================================

    SPOOFING_SIGNALS = [

        "gov-secure",
        "official-verify",
        "fake-gov",
        "mirror-site",
        "clone",
    ]

    # =========================================================
    # DETECT
    # =========================================================

    def detect(
        self,
        source: str,
    ) -> Dict[str, Any]:

        result = (
            OfficialSourceResult()
        )

        result.source = source

        result.domain = (
            self._extract_domain(
                source
            )
        )

        # =====================================================
        # GOVERNMENT
        # =====================================================

        self._detect_government(
            result
        )

        # =====================================================
        # EDUCATIONAL
        # =====================================================

        self._detect_educational(
            result
        )

        # =====================================================
        # INTERNATIONAL
        # =====================================================

        self._detect_international(
            result
        )

        # =====================================================
        # RESEARCH
        # =====================================================

        self._detect_research(
            result
        )

        # =====================================================
        # TRUSTED
        # =====================================================

        self._detect_trusted_authorities(
            result
        )

        # =====================================================
        # CLASSIFICATION
        # =====================================================

        self._classify_source(
            result
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
    # DOMAIN
    # =========================================================

    def _extract_domain(
        self,
        source: str,
    ) -> str:

        try:

            parsed = (
                urlparse(source)
            )

            return parsed.netloc.lower()

        except Exception:

            return ""

    # =========================================================
    # GOVERNMENT
    # =========================================================

    def _detect_government(
        self,
        result: OfficialSourceResult,
    ) -> None:

        domain = result.domain

        if any(

            tld in domain

            for tld
            in self.GOVERNMENT_TLDS
        ):

            result.government = (
                True
            )

            result.official = (
                True
            )

            result.official_tld_detected = (
                True
            )

            result.institutional_signal_detected = (
                True
            )

    # =========================================================
    # EDUCATIONAL
    # =========================================================

    def _detect_educational(
        self,
        result: OfficialSourceResult,
    ) -> None:

        domain = result.domain

        if any(

            tld in domain

            for tld
            in self.EDUCATIONAL_TLDS
        ):

            result.educational = (
                True
            )

            result.official = (
                True
            )

            result.institutional_signal_detected = (
                True
            )

    # =========================================================
    # INTERNATIONAL
    # =========================================================

    def _detect_international(
        self,
        result: OfficialSourceResult,
    ) -> None:

        domain = result.domain

        if any(

            item in domain

            for item
            in self.INTERNATIONAL_DOMAINS
        ):

            result.international = (
                True
            )

            result.official = (
                True
            )

            result.known_authority_detected = (
                True
            )

    # =========================================================
    # RESEARCH
    # =========================================================

    def _detect_research(
        self,
        result: OfficialSourceResult,
    ) -> None:

        domain = result.domain

        if any(

            item in domain

            for item
            in self.RESEARCH_DOMAINS
        ):

            result.research_source = (
                True
            )

            result.official = (
                True
            )

            result.known_authority_detected = (
                True
            )

    # =========================================================
    # TRUSTED
    # =========================================================

    def _detect_trusted_authorities(
        self,
        result: OfficialSourceResult,
    ) -> None:

        domain = result.domain

        if any(

            item in domain

            for item
            in self.TRUSTED_AUTHORITIES
        ):

            result.known_authority_detected = (
                True
            )

            result.official = (
                True
            )

    # =========================================================
    # CLASSIFY
    # =========================================================

    def _classify_source(
        self,
        result: OfficialSourceResult,
    ) -> None:

        if result.government:

            result.source_type = (
                "government"
            )

            result.confidence_level = (
                "high"
            )

        elif result.educational:

            result.source_type = (
                "educational"
            )

            result.confidence_level = (
                "high"
            )

        elif result.research_source:

            result.source_type = (
                "research"
            )

            result.confidence_level = (
                "high"
            )

        elif result.international:

            result.source_type = (
                "international"
            )

            result.confidence_level = (
                "high"
            )

        else:

            result.source_type = (
                "general"
            )

    # =========================================================
    # SCORES
    # =========================================================

    def _calculate_scores(
        self,
        result: OfficialSourceResult,
    ) -> None:

        official_score = 40.0

        trust_score = 50.0

        authority_score = 50.0

        # =====================================================
        # OFFICIAL
        # =====================================================

        if result.official:

            official_score += 35

            trust_score += 20

            authority_score += 20

        # =====================================================
        # GOV
        # =====================================================

        if result.government:

            official_score += 20

            authority_score += 15

        # =====================================================
        # EDU
        # =====================================================

        if result.educational:

            official_score += 15

            authority_score += 10

        # =====================================================
        # RESEARCH
        # =====================================================

        if result.research_source:

            trust_score += 15

            authority_score += 15

        # =====================================================
        # INTERNATIONAL
        # =====================================================

        if result.international:

            trust_score += 10

            authority_score += 10

        result.official_score = min(

            official_score,

            100,
        )

        result.trust_score = min(

            trust_score,

            100,
        )

        result.authority_score = min(

            authority_score,

            100,
        )

    # =========================================================
    # RISKS
    # =========================================================

    def _detect_risks(
        self,
        result: OfficialSourceResult,
    ) -> None:

        domain = result.domain

        # =====================================================
        # SPOOFING
        # =====================================================

        if any(

            item in domain

            for item
            in self.SPOOFING_SIGNALS
        ):

            result.spoofing_risk = (
                "high"
            )

            result.fake_official_risk = (
                "high"
            )

            result.misinformation_risk = (
                "high"
            )

            result.add_warning(
                "Potential spoofed official source detected"
            )

        # =====================================================
        # LOW AUTHORITY
        # =====================================================

        if (

            not result.official

            and

            result.authority_score < 60
        ):

            result.fake_official_risk = (
                "medium"
            )

    # =========================================================
    # FINALIZE
    # =========================================================

    def _finalize(
        self,
        result: OfficialSourceResult,
    ) -> None:

        result.add_reasoning(
            f"Detected source type: "
            f"{result.source_type}"
        )

        result.add_reasoning(
            f"Official score: "
            f"{result.official_score}"
        )

        if result.government:

            result.add_reasoning(
                "Government source verified"
            )

        if result.educational:

            result.add_reasoning(
                "Educational source verified"
            )

        if result.research_source:

            result.add_reasoning(
                "Research authority source detected"
            )

        if result.international:

            result.add_reasoning(
                "International institution detected"
            )

    # =========================================================
    # EXPORT
    # =========================================================

    def export(
        self,
        result: OfficialSourceResult,
    ) -> Dict[str, Any]:

        return {

            "source": (
                result.source
            ),

            "domain": (
                result.domain
            ),

            "official": (
                result.official
            ),

            "government": (
                result.government
            ),

            "educational": (
                result.educational
            ),

            "nonprofit": (
                result.nonprofit
            ),

            "international": (
                result.international
            ),

            "news_organization": (
                result.news_organization
            ),

            "research_source": (
                result.research_source
            ),

            "official_score": (
                result.official_score
            ),

            "trust_score": (
                result.trust_score
            ),

            "authority_score": (
                result.authority_score
            ),

            "official_tld_detected": (
                result.official_tld_detected
            ),

            "known_authority_detected": (
                result.known_authority_detected
            ),

            "institutional_signal_detected": (
                result.institutional_signal_detected
            ),

            "fake_official_risk": (
                result.fake_official_risk
            ),

            "spoofing_risk": (
                result.spoofing_risk
            ),

            "misinformation_risk": (
                result.misinformation_risk
            ),

            "source_type": (
                result.source_type
            ),

            "confidence_level": (
                result.confidence_level
            ),

            "reasoning": (
                result.reasoning
            ),

            "warnings": (
                result.warnings
            ),

            "metadata": (
                result.metadata
            ),
        }