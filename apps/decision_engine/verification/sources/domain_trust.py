"""
Domain Trust

Purpose:
Evaluate trustworthiness of domains using:
- TLD trust
- HTTPS security
- official signals
- spam indicators
- domain reputation
- authority patterns

Goal:
Estimate whether a domain should be trusted
for verification and factual reasoning.

This becomes the domain trust intelligence
layer of AI_COS.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List
from urllib.parse import urlparse


# =============================================================
# DOMAIN TRUST RESULT
# =============================================================

@dataclass
class DomainTrustResult:

    # =========================================================
    # DOMAIN
    # =========================================================

    domain: str = ""

    # =========================================================
    # SCORES
    # =========================================================

    trust_score: float = 0.0

    security_score: float = 0.0

    authority_score: float = 0.0

    reputation_score: float = 0.0

    # =========================================================
    # FLAGS
    # =========================================================

    trusted: bool = False

    official_domain: bool = False

    government_domain: bool = False

    educational_domain: bool = False

    nonprofit_domain: bool = False

    secure_connection: bool = False

    # =========================================================
    # SIGNALS
    # =========================================================

    strong_trust_signals: bool = False

    authority_domain_detected: bool = False

    spam_signals_detected: bool = False

    # =========================================================
    # RISKS
    # =========================================================

    spam_risk: str = "low"

    phishing_risk: str = "low"

    misinformation_risk: str = "low"

    low_trust_risk: str = "low"

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
# DOMAIN TRUST
# =============================================================

class DomainTrust:

    """
    Domain trust evaluation engine.
    """

    # =========================================================
    # TRUSTED DOMAINS
    # =========================================================

    HIGH_TRUST_DOMAINS = [

        "google.com",
        "github.com",
        "microsoft.com",
        "openai.com",
        "wikipedia.org",
        "who.int",
        "nih.gov",
        "nature.com",
        "sciencedirect.com",
    ]

    # =========================================================
    # TRUSTED TLDS
    # =========================================================

    TRUSTED_TLDS = [

        ".gov",
        ".edu",
        ".org",
        ".int",
    ]

    # =========================================================
    # SPAM SIGNALS
    # =========================================================

    SPAM_SIGNALS = [

        "spam",
        "clickbait",
        "fake",
        "rumor",
        "cheap",
        "viral",
        "seo-fast",
    ]

    # =========================================================
    # PHISHING SIGNALS
    # =========================================================

    PHISHING_SIGNALS = [

        "secure-login",
        "verify-now",
        "free-money",
        "account-reset",
    ]

    # =========================================================
    # EVALUATE
    # =========================================================

    def evaluate(
        self,
        domain: str,
    ) -> Dict[str, Any]:

        result = (
            DomainTrustResult()
        )

        result.domain = (
            self._normalize_domain(
                domain
            )
        )

        # =====================================================
        # SECURITY
        # =====================================================

        self._calculate_security(
            result
        )

        # =====================================================
        # AUTHORITY
        # =====================================================

        self._calculate_authority(
            result
        )

        # =====================================================
        # REPUTATION
        # =====================================================

        self._calculate_reputation(
            result
        )

        # =====================================================
        # FLAGS
        # =====================================================

        self._detect_flags(
            result
        )

        # =====================================================
        # RISKS
        # =====================================================

        self._detect_risks(
            result
        )

        # =====================================================
        # FINAL SCORE
        # =====================================================

        self._calculate_final_score(
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
    # NORMALIZE
    # =========================================================

    def _normalize_domain(
        self,
        domain: str,
    ) -> str:

        domain = (
            domain or ""
        ).lower().strip()

        if domain.startswith(
            "http://"
        ) or domain.startswith(
            "https://"
        ):

            try:

                parsed = (
                    urlparse(domain)
                )

                domain = parsed.netloc

            except Exception:

                pass

        return domain

    # =========================================================
    # SECURITY
    # =========================================================

    def _calculate_security(
        self,
        result: DomainTrustResult,
    ) -> None:

        score = 50.0

        domain = result.domain

        # =====================================================
        # TRUSTED TLD
        # =====================================================

        if any(

            tld in domain

            for tld
            in self.TRUSTED_TLDS
        ):

            score += 25

            result.strong_trust_signals = (
                True
            )

        # =====================================================
        # GOV
        # =====================================================

        if ".gov" in domain:

            score += 20

            result.government_domain = (
                True
            )

            result.official_domain = (
                True
            )

        # =====================================================
        # EDU
        # =====================================================

        if ".edu" in domain:

            score += 15

            result.educational_domain = (
                True
            )

        # =====================================================
        # ORG
        # =====================================================

        if ".org" in domain:

            result.nonprofit_domain = (
                True
            )

        result.security_score = min(

            score,

            100,
        )

    # =========================================================
    # AUTHORITY
    # =========================================================

    def _calculate_authority(
        self,
        result: DomainTrustResult,
    ) -> None:

        score = 50.0

        domain = result.domain

        if any(

            item in domain

            for item
            in self.HIGH_TRUST_DOMAINS
        ):

            score += 35

            result.authority_domain_detected = (
                True
            )

        if result.government_domain:

            score += 15

        if result.educational_domain:

            score += 10

        result.authority_score = min(

            score,

            100,
        )

    # =========================================================
    # REPUTATION
    # =========================================================

    def _calculate_reputation(
        self,
        result: DomainTrustResult,
    ) -> None:

        score = 55.0

        domain = result.domain

        # =====================================================
        # BIG BRANDS
        # =====================================================

        if any(

            item in domain

            for item
            in [

                "google",
                "github",
                "openai",
                "microsoft",
                "wikipedia",
            ]
        ):

            score += 25

        # =====================================================
        # OFFICIAL
        # =====================================================

        if result.official_domain:

            score += 15

        result.reputation_score = min(

            score,

            100,
        )

    # =========================================================
    # FLAGS
    # =========================================================

    def _detect_flags(
        self,
        result: DomainTrustResult,
    ) -> None:

        if (

            result.authority_score >= 80

            and

            result.security_score >= 80
        ):

            result.trusted = (
                True
            )

        if result.official_domain:

            result.trusted = (
                True
            )

    # =========================================================
    # RISKS
    # =========================================================

    def _detect_risks(
        self,
        result: DomainTrustResult,
    ) -> None:

        domain = result.domain

        # =====================================================
        # SPAM
        # =====================================================

        if any(

            item in domain

            for item
            in self.SPAM_SIGNALS
        ):

            result.spam_signals_detected = (
                True
            )

            result.spam_risk = (
                "high"
            )

            result.misinformation_risk = (
                "high"
            )

            result.add_warning(
                "Spam-like domain pattern detected"
            )

        # =====================================================
        # PHISHING
        # =====================================================

        if any(

            item in domain

            for item
            in self.PHISHING_SIGNALS
        ):

            result.phishing_risk = (
                "high"
            )

            result.add_warning(
                "Potential phishing indicators detected"
            )

        # =====================================================
        # LOW TRUST
        # =====================================================

        if (

            result.authority_score < 50

            or

            result.reputation_score < 50
        ):

            result.low_trust_risk = (
                "medium"
            )

    # =========================================================
    # FINAL SCORE
    # =========================================================

    def _calculate_final_score(
        self,
        result: DomainTrustResult,
    ) -> None:

        score = (

            result.security_score * 0.35

            +

            result.authority_score * 0.35

            +

            result.reputation_score * 0.30
        )

        # =====================================================
        # PENALTIES
        # =====================================================

        if result.spam_risk == "high":

            score -= 40

        if result.phishing_risk == "high":

            score -= 50

        result.trust_score = round(

            max(score, 0),

            2,
        )

        # =====================================================
        # TRUSTED
        # =====================================================

        result.trusted = (

            result.trust_score >= 70

            and

            result.spam_risk == "low"
        )

    # =========================================================
    # FINALIZE
    # =========================================================

    def _finalize(
        self,
        result: DomainTrustResult,
    ) -> None:

        result.add_reasoning(
            f"Domain trust score: "
            f"{result.trust_score}"
        )

        if result.trusted:

            result.add_reasoning(
                "Trusted domain verified"
            )

        if result.official_domain:

            result.add_reasoning(
                "Official domain detected"
            )

        if result.government_domain:

            result.add_reasoning(
                "Government domain detected"
            )

        if result.educational_domain:

            result.add_reasoning(
                "Educational domain detected"
            )

    # =========================================================
    # EXPORT
    # =========================================================

    def export(
        self,
        result: DomainTrustResult,
    ) -> Dict[str, Any]:

        return {

            "domain": (
                result.domain
            ),

            "trust_score": (
                result.trust_score
            ),

            "security_score": (
                result.security_score
            ),

            "authority_score": (
                result.authority_score
            ),

            "reputation_score": (
                result.reputation_score
            ),

            "trusted": (
                result.trusted
            ),

            "official_domain": (
                result.official_domain
            ),

            "government_domain": (
                result.government_domain
            ),

            "educational_domain": (
                result.educational_domain
            ),

            "nonprofit_domain": (
                result.nonprofit_domain
            ),

            "secure_connection": (
                result.secure_connection
            ),

            "strong_trust_signals": (
                result.strong_trust_signals
            ),

            "authority_domain_detected": (
                result.authority_domain_detected
            ),

            "spam_signals_detected": (
                result.spam_signals_detected
            ),

            "spam_risk": (
                result.spam_risk
            ),

            "phishing_risk": (
                result.phishing_risk
            ),

            "misinformation_risk": (
                result.misinformation_risk
            ),

            "low_trust_risk": (
                result.low_trust_risk
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