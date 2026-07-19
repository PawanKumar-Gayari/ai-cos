"""
Authority Agent

Purpose:
Analyze authority, trust, credibility,
and source reliability of content.

Analyzes:
- official sources
- E-E-A-T signals
- trustworthiness
- citation quality
- authority coverage
- source reliability
- YMYL safety

Goal:
Ensure trustworthy and authoritative content.

This becomes the trust intelligence layer
of AI_COS.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List


# =============================================================
# AUTHORITY RESULT
# =============================================================

@dataclass
class AuthorityResult:

    # =========================================================
    # SCORES
    # =========================================================

    authority_score: float = 0.0

    trust_score: float = 0.0

    source_quality_score: float = 0.0

    eeat_score: float = 0.0

    # =========================================================
    # SOURCE ANALYSIS
    # =========================================================

    official_sources_count: int = 0

    trusted_sources_count: int = 0

    weak_sources_count: int = 0

    missing_sources_count: int = 0

    # =========================================================
    # FLAGS
    # =========================================================

    authority_passed: bool = False

    official_sources_present: bool = False

    trusted_sources_present: bool = False

    ymyl_safe: bool = True

    # =========================================================
    # RISKS
    # =========================================================

    authority_risk: str = "low"

    misinformation_risk: str = "low"

    citation_risk: str = "low"

    # =========================================================
    # DETECTIONS
    # =========================================================

    unsupported_claims_detected: bool = False

    weak_citations_detected: bool = False

    unverifiable_claims_detected: bool = False

    outdated_authority_detected: bool = False

    # =========================================================
    # SIGNALS
    # =========================================================

    authority_signals: Dict[str, Any] = field(
        default_factory=dict
    )

    # =========================================================
    # REASONING
    # =========================================================

    reasoning: List[str] = field(
        default_factory=list
    )

    warnings: List[str] = field(
        default_factory=list
    )

    recommendations: List[str] = field(
        default_factory=list
    )

    # =========================================================
    # DETECTED SOURCES
    # =========================================================

    official_sources: List[str] = field(
        default_factory=list
    )

    trusted_sources: List[str] = field(
        default_factory=list
    )

    weak_sources: List[str] = field(
        default_factory=list
    )

    # =========================================================
    # META
    # =========================================================

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


# =============================================================
# AUTHORITY AGENT
# =============================================================

class AuthorityAgent:

    """
    Trust and authority intelligence agent.
    """

    # =========================================================
    # TRUSTED DOMAINS
    # =========================================================

    OFFICIAL_DOMAINS = [

        ".gov",
        ".nic.in",
        ".edu",
        ".ac.in",
        ".org",
    ]

    TRUSTED_DOMAINS = [

        "wikipedia.org",
        "who.int",
        "nih.gov",
        "mayoclinic.org",
        "google.com",
        "openai.com",
    ]

    WEAK_DOMAINS = [

        "blogspot.com",
        "medium.com",
        "quora.com",
        "reddit.com",
    ]

    # =========================================================
    # ANALYZE
    # =========================================================

    def analyze(
        self,
        article: str,
        sources: List[str] = None,
        ymyl: bool = False,
    ) -> AuthorityResult:

        result = AuthorityResult()

        article = (
            article or ""
        ).lower()

        sources = sources or []

        # =====================================================
        # SOURCE ANALYSIS
        # =====================================================

        self._analyze_sources(
            result,
            sources,
        )

        # =====================================================
        # CLAIM ANALYSIS
        # =====================================================

        self._detect_claim_risks(
            result,
            article,
        )

        # =====================================================
        # E-E-A-T
        # =====================================================

        self._calculate_eeat(
            result
        )

        # =====================================================
        # YMYL
        # =====================================================

        if ymyl:

            self._apply_ymyl_rules(
                result
            )

        # =====================================================
        # FINAL SCORE
        # =====================================================

        self._calculate_authority_score(
            result
        )

        # =====================================================
        # FINAL DECISION
        # =====================================================

        self._finalize(
            result
        )

        return result

    # =========================================================
    # SOURCE ANALYSIS
    # =========================================================

    def _analyze_sources(
        self,
        result: AuthorityResult,
        sources: List[str],
    ) -> None:

        for source in sources:

            source = source.lower()

            # =================================================
            # OFFICIAL
            # =================================================

            if any(

                domain in source

                for domain in self.OFFICIAL_DOMAINS
            ):

                result.official_sources_count += 1

                result.official_sources_present = (
                    True
                )

                result.official_sources.append(
                    source
                )

            # =================================================
            # TRUSTED
            # =================================================

            elif any(

                domain in source

                for domain
                in self.TRUSTED_DOMAINS
            ):

                result.trusted_sources_count += 1

                result.trusted_sources_present = (
                    True
                )

                result.trusted_sources.append(
                    source
                )

            # =================================================
            # WEAK
            # =================================================

            elif any(

                domain in source

                for domain
                in self.WEAK_DOMAINS
            ):

                result.weak_sources_count += 1

                result.weak_sources.append(
                    source
                )

        # =====================================================
        # MISSING
        # =====================================================

        if not sources:

            result.missing_sources_count = 1

            result.add_warning(
                "No authority sources detected"
            )

    # =========================================================
    # CLAIM RISKS
    # =========================================================

    def _detect_claim_risks(
        self,
        result: AuthorityResult,
        article: str,
    ) -> None:

        risky_patterns = [

            "guaranteed",
            "100% cure",
            "secret trick",
            "instant result",
            "miracle",
        ]

        for pattern in risky_patterns:

            if pattern in article:

                result.unverifiable_claims_detected = (
                    True
                )

                result.add_warning(
                    f"Risky claim detected: {pattern}"
                )

        # =====================================================
        # UNSUPPORTED
        # =====================================================

        if (

            "according to" in article

            and

            result.official_sources_count == 0

            and

            result.trusted_sources_count == 0
        ):

            result.unsupported_claims_detected = (
                True
            )

            result.add_warning(
                "Claims detected without trusted sources"
            )

    # =========================================================
    # E-E-A-T
    # =========================================================

    def _calculate_eeat(
        self,
        result: AuthorityResult,
    ) -> None:

        score = 0

        # =====================================================
        # OFFICIAL
        # =====================================================

        score += (
            result.official_sources_count * 25
        )

        # =====================================================
        # TRUSTED
        # =====================================================

        score += (
            result.trusted_sources_count * 15
        )

        # =====================================================
        # PENALTY
        # =====================================================

        score -= (
            result.weak_sources_count * 10
        )

        result.eeat_score = round(

            min(
                max(score, 0),
                100,
            ),

            2,
        )

        result.add_reasoning(
            f"E-E-A-T score calculated: "
            f"{result.eeat_score}"
        )

    # =========================================================
    # YMYL
    # =========================================================

    def _apply_ymyl_rules(
        self,
        result: AuthorityResult,
    ) -> None:

        # =====================================================
        # STRICT AUTHORITY
        # =====================================================

        if (
            result.official_sources_count == 0
        ):

            result.ymyl_safe = False

            result.authority_risk = (
                "high"
            )

            result.add_warning(
                "YMYL content missing official authority sources"
            )

            result.add_recommendation(
                "Use official sources for YMYL content"
            )

        # =====================================================
        # WEAK SOURCES
        # =====================================================

        if result.weak_sources_count > 0:

            result.citation_risk = (
                "high"
            )

            result.add_warning(
                "Weak citations detected in YMYL content"
            )

    # =========================================================
    # SCORE
    # =========================================================

    def _calculate_authority_score(
        self,
        result: AuthorityResult,
    ) -> None:

        score = 0

        # =====================================================
        # OFFICIAL
        # =====================================================

        score += (
            result.official_sources_count * 30
        )

        # =====================================================
        # TRUSTED
        # =====================================================

        score += (
            result.trusted_sources_count * 20
        )

        # =====================================================
        # E-E-A-T
        # =====================================================

        score += (
            result.eeat_score * 0.4
        )

        # =====================================================
        # PENALTIES
        # =====================================================

        score -= (
            result.weak_sources_count * 10
        )

        if result.unverifiable_claims_detected:

            score -= 25

        if result.unsupported_claims_detected:

            score -= 20

        result.authority_score = round(

            min(
                max(score, 0),
                100,
            ),

            2,
        )

        result.trust_score = round(

            result.authority_score,

            2,
        )

    # =========================================================
    # FINALIZE
    # =========================================================

    def _finalize(
        self,
        result: AuthorityResult,
    ) -> None:

        # =====================================================
        # PASSED
        # =====================================================

        result.authority_passed = (

            result.authority_score >= 60

            and

            not result.unverifiable_claims_detected
        )

        # =====================================================
        # RISK
        # =====================================================

        if result.authority_score >= 85:

            result.authority_risk = "low"

        elif result.authority_score >= 65:

            result.authority_risk = "medium"

        else:

            result.authority_risk = "high"

        # =====================================================
        # RECOMMENDATIONS
        # =====================================================

        if not result.official_sources_present:

            result.add_recommendation(
                "Add official authority sources"
            )

        if result.weak_sources_count > 0:

            result.add_recommendation(
                "Replace weak citations with trusted sources"
            )

        if result.authority_score < 60:

            result.add_recommendation(
                "Improve source trustworthiness"
            )

        result.add_reasoning(
            f"Final authority score: "
            f"{result.authority_score}"
        )

    # =========================================================
    # EXPORT
    # =========================================================

    def export(
        self,
        result: AuthorityResult,
    ) -> Dict[str, Any]:

        return {

            "authority_score": (
                result.authority_score
            ),

            "trust_score": (
                result.trust_score
            ),

            "source_quality_score": (
                result.source_quality_score
            ),

            "eeat_score": (
                result.eeat_score
            ),

            "official_sources_count": (
                result.official_sources_count
            ),

            "trusted_sources_count": (
                result.trusted_sources_count
            ),

            "weak_sources_count": (
                result.weak_sources_count
            ),

            "authority_passed": (
                result.authority_passed
            ),

            "official_sources_present": (
                result.official_sources_present
            ),

            "trusted_sources_present": (
                result.trusted_sources_present
            ),

            "ymyl_safe": (
                result.ymyl_safe
            ),

            "authority_risk": (
                result.authority_risk
            ),

            "misinformation_risk": (
                result.misinformation_risk
            ),

            "citation_risk": (
                result.citation_risk
            ),

            "unsupported_claims_detected": (
                result.unsupported_claims_detected
            ),

            "weak_citations_detected": (
                result.weak_citations_detected
            ),

            "unverifiable_claims_detected": (
                result.unverifiable_claims_detected
            ),

            "official_sources": (
                result.official_sources
            ),

            "trusted_sources": (
                result.trusted_sources
            ),

            "weak_sources": (
                result.weak_sources
            ),

            "reasoning": (
                result.reasoning
            ),

            "warnings": (
                result.warnings
            ),

            "recommendations": (
                result.recommendations
            ),

            "authority_signals": (
                result.authority_signals
            ),

            "metadata": (
                result.metadata
            ),
        }