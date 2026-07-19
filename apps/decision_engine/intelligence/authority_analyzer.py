"""
Authority Analyzer

Purpose:
Evaluate whether content can realistically compete
within the SERP ecosystem.

This engine analyzes:
- authority pressure
- trust requirements
- topical competition
- EEAT difficulty
- YMYL sensitivity
- official source dependency

Goal:
Produce strategic authority intelligence for:
- scoring
- prediction
- strategy planning
- verification strictness
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List


# =============================================================
# AUTHORITY RESULT
# =============================================================

@dataclass
class AuthorityAnalysisResult:

    # =========================================================
    # SCORES
    # =========================================================

    authority_score: float = 0.0

    trust_score: float = 0.0

    eeat_score: float = 0.0

    # =========================================================
    # PRESSURE
    # =========================================================

    authority_gap: float = 0.0

    backlink_pressure: float = 0.0

    topical_authority_pressure: float = 0.0

    # =========================================================
    # FLAGS
    # =========================================================

    authority_required: bool = False

    official_sources_required: bool = False

    expert_review_required: bool = False

    ymyl_sensitive: bool = False

    # =========================================================
    # COMPETITION
    # =========================================================

    authority_difficulty: str = "medium"

    trust_difficulty: str = "medium"

    # =========================================================
    # SIGNALS
    # =========================================================

    dominant_authority_sites: List[str] = field(
        default_factory=list
    )

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

    def add_authority_site(
        self,
        domain: str,
    ) -> None:

        if (
            domain
            and domain
            not in self.dominant_authority_sites
        ):

            self.dominant_authority_sites.append(
                domain
            )


# =============================================================
# AUTHORITY ANALYZER
# =============================================================

class AuthorityAnalyzer:

    """
    Authority intelligence engine.
    """

    # =========================================================
    # MAIN ANALYSIS
    # =========================================================

    def analyze(
        self,
        topic: str,
        niche: str = "default",
        serp_data: Dict[str, Any] = None,
    ) -> AuthorityAnalysisResult:

        serp_data = serp_data or {}

        result = AuthorityAnalysisResult()

        topic = (topic or "").lower()

        niche = (niche or "").lower()

        # =====================================================
        # YMYL DETECTION
        # =====================================================

        self._detect_ymyl(
            result,
            topic,
            niche,
        )

        # =====================================================
        # AUTHORITY DOMINANCE
        # =====================================================

        self._analyze_authority_sites(
            result,
            serp_data,
        )

        # =====================================================
        # BACKLINK PRESSURE
        # =====================================================

        self._analyze_backlink_pressure(
            result,
            serp_data,
        )

        # =====================================================
        # TOPICAL PRESSURE
        # =====================================================

        self._analyze_topical_authority(
            result,
            serp_data,
        )

        # =====================================================
        # OFFICIAL SOURCES
        # =====================================================

        self._detect_official_source_requirements(
            result,
            topic,
            niche,
        )

        # =====================================================
        # EEAT
        # =====================================================

        self._calculate_eeat_score(
            result,
        )

        # =====================================================
        # FINAL SCORE
        # =====================================================

        self._calculate_authority_score(
            result,
        )

        return result

    # =========================================================
    # YMYL
    # =========================================================

    def _detect_ymyl(
        self,
        result: AuthorityAnalysisResult,
        topic: str,
        niche: str,
    ) -> None:

        ymyl_keywords = [

            "health",
            "medicine",
            "disease",
            "finance",
            "investment",
            "loan",
            "insurance",
            "legal",
            "tax",
        ]

        if (
            niche in [
                "health",
                "finance",
            ]
            or
            any(
                keyword in topic
                for keyword in ymyl_keywords
            )
        ):

            result.ymyl_sensitive = True

            result.authority_required = True

            result.expert_review_required = True

            result.trust_difficulty = "high"

            result.add_reasoning(
                "YMYL-sensitive topic detected"
            )

    # =========================================================
    # AUTHORITY DOMINANCE
    # =========================================================

    def _analyze_authority_sites(
        self,
        result: AuthorityAnalysisResult,
        serp_data: Dict[str, Any],
    ) -> None:

        domains = serp_data.get(
            "authority_domains",
            [],
        )

        authority_count = len(domains)

        for domain in domains:

            result.add_authority_site(
                domain
            )

        if authority_count >= 7:

            result.authority_gap = 85

            result.authority_difficulty = (
                "very_high"
            )

            result.add_warning(
                "SERP dominated by authority domains"
            )

        elif authority_count >= 4:

            result.authority_gap = 60

            result.authority_difficulty = (
                "high"
            )

        elif authority_count >= 2:

            result.authority_gap = 40

            result.authority_difficulty = (
                "medium"
            )

        else:

            result.authority_gap = 20

            result.authority_difficulty = (
                "low"
            )

    # =========================================================
    # BACKLINK PRESSURE
    # =========================================================

    def _analyze_backlink_pressure(
        self,
        result: AuthorityAnalysisResult,
        serp_data: Dict[str, Any],
    ) -> None:

        backlinks = serp_data.get(
            "average_backlinks",
            0,
        )

        if backlinks >= 5000:

            result.backlink_pressure = 90

            result.add_warning(
                "Extreme backlink competition detected"
            )

        elif backlinks >= 1000:

            result.backlink_pressure = 70

        elif backlinks >= 300:

            result.backlink_pressure = 50

        else:

            result.backlink_pressure = 25

    # =========================================================
    # TOPICAL AUTHORITY
    # =========================================================

    def _analyze_topical_authority(
        self,
        result: AuthorityAnalysisResult,
        serp_data: Dict[str, Any],
    ) -> None:

        pressure = serp_data.get(
            "topical_authority_pressure",
            50,
        )

        result.topical_authority_pressure = (
            pressure
        )

        if pressure >= 80:

            result.add_warning(
                "High topical authority competition"
            )

    # =========================================================
    # OFFICIAL SOURCES
    # =========================================================

    def _detect_official_source_requirements(
        self,
        result: AuthorityAnalysisResult,
        topic: str,
        niche: str,
    ) -> None:

        keywords = [

            "recruitment",
            "notification",
            "result",
            "government",
            "policy",
            "admit card",
            "exam",
        ]

        if (
            niche == "jobs"
            or
            any(
                keyword in topic
                for keyword in keywords
            )
        ):

            result.official_sources_required = True

            result.add_reasoning(
                "Official source dependency detected"
            )

    # =========================================================
    # EEAT
    # =========================================================

    def _calculate_eeat_score(
        self,
        result: AuthorityAnalysisResult,
    ) -> None:

        score = 50

        if result.official_sources_required:
            score += 15

        if result.ymyl_sensitive:
            score += 20

        if result.expert_review_required:
            score += 10

        score -= (
            result.authority_gap * 0.1
        )

        result.eeat_score = round(
            max(min(score, 100), 0),
            2,
        )

    # =========================================================
    # FINAL SCORE
    # =========================================================

    def _calculate_authority_score(
        self,
        result: AuthorityAnalysisResult,
    ) -> None:

        authority_score = (

            100 -

            (
                (
                    result.authority_gap +

                    result.backlink_pressure +

                    result.topical_authority_pressure
                ) / 3
            )
        )

        result.authority_score = round(
            max(authority_score, 0),
            2,
        )

        result.trust_score = round(

            (
                result.eeat_score +

                result.authority_score
            ) / 2,

            2,
        )

        # =====================================================
        # RECOMMENDATIONS
        # =====================================================

        if result.authority_score < 40:

            result.add_recommendation(
                "Target long-tail semantic variants"
            )

            result.add_recommendation(
                "Increase topical depth"
            )

        if result.official_sources_required:

            result.add_recommendation(
                "Use government and official references"
            )

        if result.ymyl_sensitive:

            result.add_recommendation(
                "Add expert-reviewed citations"
            )

    # =========================================================
    # EXPORT
    # =========================================================

    def export(
        self,
        result: AuthorityAnalysisResult,
    ) -> Dict[str, Any]:

        return {

            "authority_score": (
                result.authority_score
            ),

            "trust_score": (
                result.trust_score
            ),

            "eeat_score": (
                result.eeat_score
            ),

            "authority_gap": (
                result.authority_gap
            ),

            "backlink_pressure": (
                result.backlink_pressure
            ),

            "topical_authority_pressure": (
                result.topical_authority_pressure
            ),

            "authority_required": (
                result.authority_required
            ),

            "official_sources_required": (
                result.official_sources_required
            ),

            "expert_review_required": (
                result.expert_review_required
            ),

            "ymyl_sensitive": (
                result.ymyl_sensitive
            ),

            "authority_difficulty": (
                result.authority_difficulty
            ),

            "trust_difficulty": (
                result.trust_difficulty
            ),

            "dominant_authority_sites": (
                result.dominant_authority_sites
            ),

            "authority_signals": (
                result.authority_signals
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

            "metadata": (
                result.metadata
            ),
        }