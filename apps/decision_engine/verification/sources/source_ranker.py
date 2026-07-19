"""
Source Ranker

Purpose:
Rank and prioritize sources using:
- authority score
- trust score
- citation quality
- relevance
- freshness
- official verification

Goal:
Select the BEST factual sources for:
- article generation
- verification
- ranking intelligence
- hallucination prevention

This becomes the source ranking
intelligence layer of AI_COS.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List
from urllib.parse import urlparse


# =============================================================
# IMPORTS
# =============================================================

from .authority_score import (
    AuthorityScore,
)

from .domain_trust import (
    DomainTrust,
)

from .official_source_detector import (
    OfficialSourceDetector,
)

from .citation_extractor import (
    CitationExtractor,
)


# =============================================================
# RANKED SOURCE
# =============================================================

@dataclass
class RankedSource:

    # =========================================================
    # SOURCE
    # =========================================================

    source: str = ""

    domain: str = ""

    # =========================================================
    # SCORES
    # =========================================================

    authority_score: float = 0.0

    trust_score: float = 0.0

    citation_score: float = 0.0

    relevance_score: float = 0.0

    freshness_score: float = 0.0

    official_score: float = 0.0

    final_score: float = 0.0

    # =========================================================
    # FLAGS
    # =========================================================

    trusted: bool = False

    official: bool = False

    government: bool = False

    educational: bool = False

    research_source: bool = False

    # =========================================================
    # RISKS
    # =========================================================

    misinformation_risk: str = "low"

    spam_risk: str = "low"

    low_quality_risk: str = "low"

    # =========================================================
    # CLASSIFICATION
    # =========================================================

    source_tier: str = "medium"

    source_type: str = "general"

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
# SOURCE RANKER RESULT
# =============================================================

@dataclass
class SourceRankerResult:

    # =========================================================
    # SCORES
    # =========================================================

    average_score: float = 0.0

    highest_score: float = 0.0

    lowest_score: float = 0.0

    # =========================================================
    # COUNTS
    # =========================================================

    total_sources: int = 0

    trusted_sources: int = 0

    official_sources: int = 0

    weak_sources: int = 0

    # =========================================================
    # RANKING
    # =========================================================

    ranked_sources: List[RankedSource] = field(
        default_factory=list
    )

    top_sources: List[str] = field(
        default_factory=list
    )

    # =========================================================
    # QUALITY
    # =========================================================

    source_quality: str = "medium"

    verification_strength: str = "medium"

    # =========================================================
    # RISKS
    # =========================================================

    misinformation_risk: str = "medium"

    authority_gap_risk: str = "medium"

    source_quality_risk: str = "medium"

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
# SOURCE RANKER
# =============================================================

class SourceRanker:

    """
    Source ranking intelligence engine.
    """

    # =========================================================
    # INIT
    # =========================================================

    def __init__(self):

        self.authority_engine = (
            AuthorityScore()
        )

        self.trust_engine = (
            DomainTrust()
        )

        self.official_detector = (
            OfficialSourceDetector()
        )

        self.citation_extractor = (
            CitationExtractor()
        )

    # =========================================================
    # RANK
    # =========================================================

    def rank(
        self,
        sources: List[str],
        keyword: str = "",
    ) -> Dict[str, Any]:

        result = (
            SourceRankerResult()
        )

        sources = (
            sources or []
        )

        result.total_sources = (
            len(sources)
        )

        ranked_sources = []

        # =====================================================
        # PROCESS
        # =====================================================

        for source in sources:

            ranked = (
                self._rank_source(
                    source=source,
                    keyword=keyword,
                )
            )

            ranked_sources.append(
                ranked
            )

        # =====================================================
        # SORT
        # =====================================================

        ranked_sources.sort(

            key=lambda item: item.final_score,

            reverse=True,
        )

        result.ranked_sources = (
            ranked_sources
        )

        # =====================================================
        # TOP SOURCES
        # =====================================================

        result.top_sources = [

            item.source

            for item
            in ranked_sources[:5]
        ]

        # =====================================================
        # COUNTS
        # =====================================================

        result.trusted_sources = sum(

            1

            for item
            in ranked_sources

            if item.trusted
        )

        result.official_sources = sum(

            1

            for item
            in ranked_sources

            if item.official
        )

        result.weak_sources = sum(

            1

            for item
            in ranked_sources

            if item.final_score < 50
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
    # RANK SINGLE
    # =========================================================

    def _rank_source(
        self,
        source: str,
        keyword: str = "",
    ) -> RankedSource:

        ranked = RankedSource()

        ranked.source = source

        ranked.domain = (
            self._extract_domain(
                source
            )
        )

        # =====================================================
        # AUTHORITY
        # =====================================================

        authority = (
            self.authority_engine.calculate(
                source=source,
            )
        )

        ranked.authority_score = (
            authority.get(
                "score",
                0.0,
            )
        )

        # =====================================================
        # TRUST
        # =====================================================

        trust = (
            self.trust_engine.evaluate(
                domain=ranked.domain,
            )
        )

        ranked.trust_score = (
            trust.get(
                "trust_score",
                0.0,
            )
        )

        ranked.trusted = (
            trust.get(
                "trusted",
                False,
            )
        )

        # =====================================================
        # OFFICIAL
        # =====================================================

        official = (
            self.official_detector.detect(
                source=source,
            )
        )

        ranked.official = (
            official.get(
                "official",
                False,
            )
        )

        ranked.government = (
            official.get(
                "government",
                False,
            )
        )

        ranked.educational = (
            official.get(
                "educational",
                False,
            )
        )

        ranked.research_source = (
            official.get(
                "research_source",
                False,
            )
        )

        ranked.official_score = (
            official.get(
                "official_score",
                0.0,
            )
        )

        ranked.source_type = (
            official.get(
                "source_type",
                "general",
            )
        )

        # =====================================================
        # CITATIONS
        # =====================================================

        citation_data = (
            self.citation_extractor.extract(
                content=source,
            )
        )

        ranked.citation_score = (
            citation_data.get(
                "citation_score",
                0.0,
            )
        )

        # =====================================================
        # RELEVANCE
        # =====================================================

        ranked.relevance_score = (
            self._calculate_relevance(
                source=source,
                keyword=keyword,
            )
        )

        # =====================================================
        # FRESHNESS
        # =====================================================

        ranked.freshness_score = (
            self._calculate_freshness(
                source=source,
            )
        )

        # =====================================================
        # FINAL SCORE
        # =====================================================

        ranked.final_score = round(

            (
                ranked.authority_score * 0.25
                +
                ranked.trust_score * 0.20
                +
                ranked.official_score * 0.20
                +
                ranked.citation_score * 0.10
                +
                ranked.relevance_score * 0.15
                +
                ranked.freshness_score * 0.10
            ),

            2,
        )

        # =====================================================
        # TIER
        # =====================================================

        if ranked.final_score >= 85:

            ranked.source_tier = (
                "elite"
            )

        elif ranked.final_score >= 70:

            ranked.source_tier = (
                "high"
            )

        elif ranked.final_score >= 50:

            ranked.source_tier = (
                "medium"
            )

        else:

            ranked.source_tier = (
                "low"
            )

        # =====================================================
        # RISKS
        # =====================================================

        self._detect_source_risks(
            ranked
        )

        # =====================================================
        # REASONING
        # =====================================================

        ranked.add_reasoning(
            f"Final ranking score: "
            f"{ranked.final_score}"
        )

        return ranked

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
    # RELEVANCE
    # =========================================================

    def _calculate_relevance(
        self,
        source: str,
        keyword: str,
    ) -> float:

        if not keyword:

            return 70.0

        source = source.lower()

        keyword = keyword.lower()

        matches = 0

        for token in keyword.split():

            if token in source:

                matches += 1

        score = min(

            50 + (matches * 12),

            100,
        )

        return float(score)

    # =========================================================
    # FRESHNESS
    # =========================================================

    def _calculate_freshness(
        self,
        source: str,
    ) -> float:

        source = source.lower()

        if "2026" in source:

            return 95.0

        if "2025" in source:

            return 85.0

        if "2024" in source:

            return 75.0

        return 65.0

    # =========================================================
    # SOURCE RISKS
    # =========================================================

    def _detect_source_risks(
        self,
        ranked: RankedSource,
    ) -> None:

        if ranked.final_score < 40:

            ranked.low_quality_risk = (
                "high"
            )

        if ranked.trust_score < 40:

            ranked.misinformation_risk = (
                "high"
            )

        suspicious_terms = [

            "spam",
            "fake",
            "clickbait",
            "rumor",
        ]

        if any(

            item in ranked.domain

            for item
            in suspicious_terms
        ):

            ranked.spam_risk = (
                "high"
            )

            ranked.misinformation_risk = (
                "high"
            )

    # =========================================================
    # CALCULATE SCORES
    # =========================================================

    def _calculate_scores(
        self,
        result: SourceRankerResult,
    ) -> None:

        if not result.ranked_sources:

            return

        scores = [

            item.final_score

            for item
            in result.ranked_sources
        ]

        result.average_score = round(

            sum(scores)
            /
            len(scores),

            2,
        )

        result.highest_score = max(
            scores
        )

        result.lowest_score = min(
            scores
        )

        # =====================================================
        # QUALITY
        # =====================================================

        if result.average_score >= 80:

            result.source_quality = (
                "high"
            )

            result.verification_strength = (
                "strong"
            )

        elif result.average_score >= 60:

            result.source_quality = (
                "medium"
            )

            result.verification_strength = (
                "moderate"
            )

        else:

            result.source_quality = (
                "low"
            )

            result.verification_strength = (
                "weak"
            )

    # =========================================================
    # RISKS
    # =========================================================

    def _detect_risks(
        self,
        result: SourceRankerResult,
    ) -> None:

        # =====================================================
        # MISINFORMATION
        # =====================================================

        if result.weak_sources >= 3:

            result.misinformation_risk = (
                "high"
            )

            result.add_warning(
                "Multiple weak sources detected"
            )

        # =====================================================
        # AUTHORITY
        # =====================================================

        if result.official_sources == 0:

            result.authority_gap_risk = (
                "high"
            )

        # =====================================================
        # QUALITY
        # =====================================================

        if result.average_score < 50:

            result.source_quality_risk = (
                "high"
            )

    # =========================================================
    # FINALIZE
    # =========================================================

    def _finalize(
        self,
        result: SourceRankerResult,
    ) -> None:

        # =====================================================
        # RECOMMENDATIONS
        # =====================================================

        if result.authority_gap_risk == "high":

            result.add_recommendation(
                "Add official authority sources"
            )

            result.add_action(
                "Use government and research references"
            )

        if result.source_quality == "low":

            result.add_recommendation(
                "Replace low quality domains"
            )

        if result.verification_strength == "weak":

            result.add_recommendation(
                "Increase trusted source ratio"
            )

        result.add_action(
            "Store source ranking intelligence"
        )

        result.add_reasoning(
            f"Average ranking score: "
            f"{result.average_score}"
        )

    # =========================================================
    # EXPORT
    # =========================================================

    def export(
        self,
        result: SourceRankerResult,
    ) -> Dict[str, Any]:

        return {

            "average_score": (
                result.average_score
            ),

            "highest_score": (
                result.highest_score
            ),

            "lowest_score": (
                result.lowest_score
            ),

            "total_sources": (
                result.total_sources
            ),

            "trusted_sources": (
                result.trusted_sources
            ),

            "official_sources": (
                result.official_sources
            ),

            "weak_sources": (
                result.weak_sources
            ),

            "ranked_sources": [

                item.__dict__

                for item
                in result.ranked_sources
            ],

            "top_sources": (
                result.top_sources
            ),

            "source_quality": (
                result.source_quality
            ),

            "verification_strength": (
                result.verification_strength
            ),

            "misinformation_risk": (
                result.misinformation_risk
            ),

            "authority_gap_risk": (
                result.authority_gap_risk
            ),

            "source_quality_risk": (
                result.source_quality_risk
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