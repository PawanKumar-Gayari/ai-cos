"""
Authority Score

Purpose:
Calculate source authority score using:
- domain authority
- trust signals
- official status
- educational/government signals
- backlink quality estimation
- reputation indicators

Goal:
Estimate how authoritative a source is
for verification and ranking decisions.

This becomes the authority scoring layer
of AI_COS.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List
from urllib.parse import urlparse


# =============================================================
# AUTHORITY SCORE RESULT
# =============================================================

@dataclass
class AuthorityScoreResult:

    # =========================================================
    # SOURCE
    # =========================================================

    source: str = ""

    domain: str = ""

    # =========================================================
    # SCORES
    # =========================================================

    score: float = 0.0

    domain_authority_score: float = 0.0

    trust_signal_score: float = 0.0

    reputation_score: float = 0.0

    backlink_strength_score: float = 0.0

    # =========================================================
    # FLAGS
    # =========================================================

    official_source: bool = False

    government_source: bool = False

    educational_source: bool = False

    nonprofit_source: bool = False

    news_source: bool = False

    # =========================================================
    # SIGNALS
    # =========================================================

    strong_trust_signals: bool = False

    authority_domain_detected: bool = False

    high_reputation_detected: bool = False

    # =========================================================
    # RISKS
    # =========================================================

    low_authority_risk: str = "low"

    spam_risk: str = "low"

    misinformation_risk: str = "low"

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
# AUTHORITY SCORE
# =============================================================

class AuthorityScore:

    """
    Source authority scoring engine.
    """

    # =========================================================
    # TRUSTED DOMAINS
    # =========================================================

    HIGH_AUTHORITY_DOMAINS = [

        "google.com",
        "wikipedia.org",
        "github.com",
        "microsoft.com",
        "openai.com",
        "who.int",
        "un.org",
        "nih.gov",
        "nature.com",
        "sciencedirect.com",
    ]

    # =========================================================
    # TRUSTED TLD
    # =========================================================

    TRUSTED_TLDS = [

        ".gov",
        ".edu",
        ".org",
    ]

    # =========================================================
    # SPAM SIGNALS
    # =========================================================

    SPAM_SIGNALS = [

        "clickbait",
        "spam",
        "fake",
        "rumor",
        "viral",
        "cheap-seo",
    ]

    # =========================================================
    # NEWS SIGNALS
    # =========================================================

    NEWS_SIGNALS = [

        "news",
        "times",
        "media",
        "journal",
        "post",
    ]

    # =========================================================
    # CALCULATE
    # =========================================================

    def calculate(
        self,
        source: str,
    ) -> Dict[str, Any]:

        result = (
            AuthorityScoreResult()
        )

        result.source = source

        result.domain = (
            self._extract_domain(
                source
            )
        )

        # =====================================================
        # DOMAIN SCORE
        # =====================================================

        self._calculate_domain_score(
            result
        )

        # =====================================================
        # TRUST
        # =====================================================

        self._calculate_trust_signals(
            result
        )

        # =====================================================
        # REPUTATION
        # =====================================================

        self._calculate_reputation(
            result
        )

        # =====================================================
        # BACKLINKS
        # =====================================================

        self._estimate_backlinks(
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
    # DOMAIN SCORE
    # =========================================================

    def _calculate_domain_score(
        self,
        result: AuthorityScoreResult,
    ) -> None:

        domain = result.domain

        score = 50.0

        # =====================================================
        # HIGH AUTHORITY
        # =====================================================

        if any(

            item in domain

            for item
            in self.HIGH_AUTHORITY_DOMAINS
        ):

            score += 35

            result.authority_domain_detected = (
                True
            )

        # =====================================================
        # GOV
        # =====================================================

        if ".gov" in domain:

            score += 25

            result.government_source = (
                True
            )

            result.official_source = (
                True
            )

        # =====================================================
        # EDU
        # =====================================================

        if ".edu" in domain:

            score += 20

            result.educational_source = (
                True
            )

        # =====================================================
        # ORG
        # =====================================================

        if ".org" in domain:

            score += 10

            result.nonprofit_source = (
                True
            )

        result.domain_authority_score = min(

            score,

            100,
        )

    # =========================================================
    # TRUST SIGNALS
    # =========================================================

    def _calculate_trust_signals(
        self,
        result: AuthorityScoreResult,
    ) -> None:

        score = 50.0

        domain = result.domain

        # =====================================================
        # HTTPS
        # =====================================================

        if result.source.startswith(
            "https://"
        ):

            score += 10

        # =====================================================
        # TRUSTED TLD
        # =====================================================

        if any(

            tld in domain

            for tld
            in self.TRUSTED_TLDS
        ):

            score += 20

            result.strong_trust_signals = (
                True
            )

        # =====================================================
        # OFFICIAL
        # =====================================================

        if result.official_source:

            score += 15

        result.trust_signal_score = min(

            score,

            100,
        )

    # =========================================================
    # REPUTATION
    # =========================================================

    def _calculate_reputation(
        self,
        result: AuthorityScoreResult,
    ) -> None:

        domain = result.domain

        score = 55.0

        # =====================================================
        # BIG BRANDS
        # =====================================================

        if any(

            item in domain

            for item
            in [

                "google",
                "microsoft",
                "openai",
                "wikipedia",
                "github",
            ]
        ):

            score += 30

            result.high_reputation_detected = (
                True
            )

        # =====================================================
        # NEWS
        # =====================================================

        if any(

            item in domain

            for item
            in self.NEWS_SIGNALS
        ):

            result.news_source = (
                True
            )

            score += 10

        result.reputation_score = min(

            score,

            100,
        )

    # =========================================================
    # BACKLINKS
    # =========================================================

    def _estimate_backlinks(
        self,
        result: AuthorityScoreResult,
    ) -> None:

        score = 50.0

        domain = result.domain

        # =====================================================
        # BIG DOMAINS
        # =====================================================

        if result.authority_domain_detected:

            score += 30

        if result.government_source:

            score += 15

        if result.educational_source:

            score += 15

        result.backlink_strength_score = min(

            score,

            100,
        )

    # =========================================================
    # FLAGS
    # =========================================================

    def _detect_flags(
        self,
        result: AuthorityScoreResult,
    ) -> None:

        if (

            result.domain_authority_score >= 80

            and

            result.trust_signal_score >= 80
        ):

            result.strong_trust_signals = (
                True
            )

    # =========================================================
    # RISKS
    # =========================================================

    def _detect_risks(
        self,
        result: AuthorityScoreResult,
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

            result.spam_risk = (
                "high"
            )

            result.misinformation_risk = (
                "high"
            )

            result.add_warning(
                "Spam-like domain detected"
            )

        # =====================================================
        # LOW AUTHORITY
        # =====================================================

        if result.domain_authority_score < 50:

            result.low_authority_risk = (
                "high"
            )

    # =========================================================
    # FINAL SCORE
    # =========================================================

    def _calculate_final_score(
        self,
        result: AuthorityScoreResult,
    ) -> None:

        final_score = (

            result.domain_authority_score * 0.35

            +

            result.trust_signal_score * 0.25

            +

            result.reputation_score * 0.25

            +

            result.backlink_strength_score * 0.15
        )

        # =====================================================
        # PENALTIES
        # =====================================================

        if result.spam_risk == "high":

            final_score -= 40

        result.score = round(

            max(final_score, 0),

            2,
        )

    # =========================================================
    # FINALIZE
    # =========================================================

    def _finalize(
        self,
        result: AuthorityScoreResult,
    ) -> None:

        result.add_reasoning(
            f"Authority score calculated: "
            f"{result.score}"
        )

        if result.official_source:

            result.add_reasoning(
                "Official source detected"
            )

        if result.educational_source:

            result.add_reasoning(
                "Educational source detected"
            )

        if result.government_source:

            result.add_reasoning(
                "Government source detected"
            )

    # =========================================================
    # EXPORT
    # =========================================================

    def export(
        self,
        result: AuthorityScoreResult,
    ) -> Dict[str, Any]:

        return {

            "source": (
                result.source
            ),

            "domain": (
                result.domain
            ),

            "score": (
                result.score
            ),

            "domain_authority_score": (
                result.domain_authority_score
            ),

            "trust_signal_score": (
                result.trust_signal_score
            ),

            "reputation_score": (
                result.reputation_score
            ),

            "backlink_strength_score": (
                result.backlink_strength_score
            ),

            "official_source": (
                result.official_source
            ),

            "government_source": (
                result.government_source
            ),

            "educational_source": (
                result.educational_source
            ),

            "nonprofit_source": (
                result.nonprofit_source
            ),

            "news_source": (
                result.news_source
            ),

            "strong_trust_signals": (
                result.strong_trust_signals
            ),

            "authority_domain_detected": (
                result.authority_domain_detected
            ),

            "high_reputation_detected": (
                result.high_reputation_detected
            ),

            "low_authority_risk": (
                result.low_authority_risk
            ),

            "spam_risk": (
                result.spam_risk
            ),

            "misinformation_risk": (
                result.misinformation_risk
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