"""
SEO Agent

Purpose:
Analyze SEO quality, semantic optimization,
SERP optimization, entity coverage,
and ranking readiness.

Analyzes:
- keyword optimization
- semantic SEO
- entity coverage
- heading optimization
- internal SEO signals
- snippet readiness
- search intent alignment

Goal:
Ensure AI_COS produces search-engine
optimized editorial content.

This becomes the SEO intelligence layer
of AI_COS.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List


# =============================================================
# SEO RESULT
# =============================================================

@dataclass
class SEOResult:

    # =========================================================
    # SCORES
    # =========================================================

    seo_score: float = 0.0

    keyword_score: float = 0.0

    semantic_score: float = 0.0

    heading_score: float = 0.0

    snippet_score: float = 0.0

    intent_match_score: float = 0.0

    # =========================================================
    # FLAGS
    # =========================================================

    seo_passed: bool = False

    snippet_ready: bool = False

    semantic_optimized: bool = False

    intent_aligned: bool = False

    rewrite_required: bool = False

    # =========================================================
    # RISKS
    # =========================================================

    seo_risk: str = "low"

    keyword_stuffing_risk: str = "low"

    semantic_gap_risk: str = "low"

    ranking_risk: str = "low"

    # =========================================================
    # DETECTIONS
    # =========================================================

    keyword_stuffing_detected: bool = False

    missing_headings_detected: bool = False

    weak_semantic_coverage_detected: bool = False

    poor_intent_match_detected: bool = False

    snippet_opportunity_detected: bool = False

    # =========================================================
    # METRICS
    # =========================================================

    keyword_density: float = 0.0

    heading_count: int = 0

    keyword_mentions: int = 0

    entity_mentions: int = 0

    # =========================================================
    # ENTITIES
    # =========================================================

    detected_entities: List[str] = field(
        default_factory=list
    )

    missing_entities: List[str] = field(
        default_factory=list
    )

    semantic_keywords: List[str] = field(
        default_factory=list
    )

    # =========================================================
    # SIGNALS
    # =========================================================

    seo_signals: Dict[str, Any] = field(
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
    # ACTIONS
    # =========================================================

    recommended_actions: List[str] = field(
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
# SEO AGENT
# =============================================================

class SEOAgent:

    """
    SEO intelligence agent.
    """

    # =========================================================
    # SNIPPET KEYWORDS
    # =========================================================

    SNIPPET_KEYWORDS = [

        "how to",
        "what is",
        "best",
        "guide",
        "tips",
        "steps",
    ]

    # =========================================================
    # SEMANTIC TERMS
    # =========================================================

    COMMON_SEMANTIC_TERMS = [

        "benefits",
        "features",
        "examples",
        "advantages",
        "methods",
        "process",
        "strategy",
    ]

    # =========================================================
    # ANALYZE
    # =========================================================

    def analyze(
        self,
        article: str,
        keyword: str = "",
        entities: List[str] = None,
    ) -> SEOResult:

        result = SEOResult()

        article = article or ""

        article_lower = article.lower()

        keyword = (
            keyword or ""
        ).lower()

        entities = entities or []

        # =====================================================
        # KEYWORD
        # =====================================================

        self._analyze_keyword(
            result,
            article_lower,
            keyword,
        )

        # =====================================================
        # HEADINGS
        # =====================================================

        self._analyze_headings(
            result,
            article,
        )

        # =====================================================
        # SEMANTIC
        # =====================================================

        self._analyze_semantics(
            result,
            article_lower,
        )

        # =====================================================
        # ENTITIES
        # =====================================================

        self._analyze_entities(
            result,
            article_lower,
            entities,
        )

        # =====================================================
        # SNIPPETS
        # =====================================================

        self._analyze_snippets(
            result,
            article_lower,
        )

        # =====================================================
        # INTENT
        # =====================================================

        self._analyze_intent(
            result,
            article_lower,
            keyword,
        )

        # =====================================================
        # FINAL SCORE
        # =====================================================

        self._calculate_seo_score(
            result
        )

        # =====================================================
        # FINALIZE
        # =====================================================

        self._finalize(
            result
        )

        return result

    # =========================================================
    # KEYWORD
    # =========================================================

    def _analyze_keyword(
        self,
        result: SEOResult,
        article: str,
        keyword: str,
    ) -> None:

        if not keyword:
            return

        words = article.split()

        word_count = max(
            len(words),
            1,
        )

        mentions = article.count(
            keyword
        )

        density = (
            mentions / word_count
        ) * 100

        result.keyword_mentions = (
            mentions
        )

        result.keyword_density = round(
            density,
            2,
        )

        # =====================================================
        # SCORE
        # =====================================================

        score = 100

        if density < 0.5:

            score -= 40

            result.add_warning(
                "Keyword usage too low"
            )

        elif density > 5:

            score -= 50

            result.keyword_stuffing_detected = (
                True
            )

            result.add_warning(
                "Keyword stuffing detected"
            )

        elif density > 3:

            score -= 20

        result.keyword_score = round(

            max(score, 0),

            2,
        )

        result.add_reasoning(
            f"Keyword density: "
            f"{result.keyword_density}%"
        )

    # =========================================================
    # HEADINGS
    # =========================================================

    def _analyze_headings(
        self,
        result: SEOResult,
        article: str,
    ) -> None:

        headings = article.count("#")

        result.heading_count = headings

        score = 100

        if headings == 0:

            score -= 50

            result.missing_headings_detected = (
                True
            )

            result.add_warning(
                "No headings detected"
            )

        elif headings < 3:

            score -= 20

        result.heading_score = round(

            max(score, 0),

            2,
        )

    # =========================================================
    # SEMANTICS
    # =========================================================

    def _analyze_semantics(
        self,
        result: SEOResult,
        article: str,
    ) -> None:

        semantic_hits = 0

        for term in self.COMMON_SEMANTIC_TERMS:

            if term in article:

                semantic_hits += 1

                result.semantic_keywords.append(
                    term
                )

        score = semantic_hits * 15

        if semantic_hits < 3:

            result.weak_semantic_coverage_detected = (
                True
            )

            result.add_warning(
                "Weak semantic SEO coverage"
            )

        result.semantic_score = round(

            min(score, 100),

            2,
        )

        result.semantic_optimized = (
            result.semantic_score >= 60
        )

    # =========================================================
    # ENTITIES
    # =========================================================

    def _analyze_entities(
        self,
        result: SEOResult,
        article: str,
        entities: List[str],
    ) -> None:

        for entity in entities:

            entity_lower = entity.lower()

            if entity_lower in article:

                result.detected_entities.append(
                    entity
                )

            else:

                result.missing_entities.append(
                    entity
                )

        result.entity_mentions = len(
            result.detected_entities
        )

    # =========================================================
    # SNIPPETS
    # =========================================================

    def _analyze_snippets(
        self,
        result: SEOResult,
        article: str,
    ) -> None:

        score = 50

        for keyword in self.SNIPPET_KEYWORDS:

            if keyword in article:

                score += 10

                result.snippet_opportunity_detected = (
                    True
                )

        if (
            "?" in article
            or
            "steps" in article
        ):

            score += 15

        result.snippet_score = round(

            min(score, 100),

            2,
        )

        result.snippet_ready = (
            result.snippet_score >= 70
        )

    # =========================================================
    # INTENT
    # =========================================================

    def _analyze_intent(
        self,
        result: SEOResult,
        article: str,
        keyword: str,
    ) -> None:

        score = 50

        informational = [

            "guide",
            "how",
            "what",
            "tips",
        ]

        transactional = [

            "buy",
            "price",
            "deal",
        ]

        if any(
            word in keyword
            for word in informational
        ):

            if (
                "how"
                in article
                or
                "guide"
                in article
            ):

                score += 40

        elif any(
            word in keyword
            for word in transactional
        ):

            if (
                "buy"
                in article
                or
                "price"
                in article
            ):

                score += 40

        else:

            score += 20

        result.intent_match_score = round(

            min(score, 100),

            2,
        )

        result.intent_aligned = (
            result.intent_match_score >= 70
        )

        if not result.intent_aligned:

            result.poor_intent_match_detected = (
                True
            )

    # =========================================================
    # SEO SCORE
    # =========================================================

    def _calculate_seo_score(
        self,
        result: SEOResult,
    ) -> None:

        seo = (

            result.keyword_score * 0.30

            +

            result.semantic_score * 0.20

            +

            result.heading_score * 0.15

            +

            result.snippet_score * 0.15

            +

            result.intent_match_score * 0.20
        )

        # =====================================================
        # PENALTIES
        # =====================================================

        if result.keyword_stuffing_detected:

            seo -= 20

        if result.weak_semantic_coverage_detected:

            seo -= 10

        if result.missing_headings_detected:

            seo -= 10

        result.seo_score = round(

            max(seo, 0),

            2,
        )

        result.add_reasoning(
            f"SEO score calculated: "
            f"{result.seo_score}"
        )

    # =========================================================
    # FINALIZE
    # =========================================================

    def _finalize(
        self,
        result: SEOResult,
    ) -> None:

        # =====================================================
        # PASSED
        # =====================================================

        result.seo_passed = (
            result.seo_score >= 65
        )

        # =====================================================
        # RISK
        # =====================================================

        if result.seo_score >= 85:

            result.seo_risk = "low"

        elif result.seo_score >= 65:

            result.seo_risk = "medium"

        else:

            result.seo_risk = "high"

        # =====================================================
        # KEYWORD RISK
        # =====================================================

        if result.keyword_stuffing_detected:

            result.keyword_stuffing_risk = (
                "high"
            )

        # =====================================================
        # SEMANTIC RISK
        # =====================================================

        if result.weak_semantic_coverage_detected:

            result.semantic_gap_risk = (
                "high"
            )

        # =====================================================
        # REWRITE
        # =====================================================

        if (

            result.seo_score < 60

            or

            result.keyword_stuffing_detected

            or

            result.missing_headings_detected
        ):

            result.rewrite_required = (
                True
            )

        # =====================================================
        # RECOMMENDATIONS
        # =====================================================

        if result.keyword_stuffing_detected:

            result.add_recommendation(
                "Reduce keyword density"
            )

            result.add_action(
                "Rewrite repetitive keyword sections"
            )

        if result.missing_headings_detected:

            result.add_recommendation(
                "Add SEO-friendly headings"
            )

            result.add_action(
                "Create structured H2 and H3 headings"
            )

        if result.weak_semantic_coverage_detected:

            result.add_recommendation(
                "Improve semantic keyword coverage"
            )

            result.add_action(
                "Add related topical terms"
            )

        if result.snippet_opportunity_detected:

            result.add_recommendation(
                "Optimize for featured snippets"
            )

        if not result.intent_aligned:

            result.add_recommendation(
                "Improve search intent alignment"
            )

        result.add_reasoning(
            f"Final SEO score: "
            f"{result.seo_score}"
        )

    # =========================================================
    # EXPORT
    # =========================================================

    def export(
        self,
        result: SEOResult,
    ) -> Dict[str, Any]:

        return {

            "seo_score": (
                result.seo_score
            ),

            "keyword_score": (
                result.keyword_score
            ),

            "semantic_score": (
                result.semantic_score
            ),

            "heading_score": (
                result.heading_score
            ),

            "snippet_score": (
                result.snippet_score
            ),

            "intent_match_score": (
                result.intent_match_score
            ),

            "seo_passed": (
                result.seo_passed
            ),

            "snippet_ready": (
                result.snippet_ready
            ),

            "semantic_optimized": (
                result.semantic_optimized
            ),

            "intent_aligned": (
                result.intent_aligned
            ),

            "rewrite_required": (
                result.rewrite_required
            ),

            "seo_risk": (
                result.seo_risk
            ),

            "keyword_stuffing_risk": (
                result.keyword_stuffing_risk
            ),

            "semantic_gap_risk": (
                result.semantic_gap_risk
            ),

            "ranking_risk": (
                result.ranking_risk
            ),

            "keyword_stuffing_detected": (
                result.keyword_stuffing_detected
            ),

            "missing_headings_detected": (
                result.missing_headings_detected
            ),

            "weak_semantic_coverage_detected": (
                result.weak_semantic_coverage_detected
            ),

            "poor_intent_match_detected": (
                result.poor_intent_match_detected
            ),

            "snippet_opportunity_detected": (
                result.snippet_opportunity_detected
            ),

            "keyword_density": (
                result.keyword_density
            ),

            "heading_count": (
                result.heading_count
            ),

            "keyword_mentions": (
                result.keyword_mentions
            ),

            "entity_mentions": (
                result.entity_mentions
            ),

            "detected_entities": (
                result.detected_entities
            ),

            "missing_entities": (
                result.missing_entities
            ),

            "semantic_keywords": (
                result.semantic_keywords
            ),

            "seo_signals": (
                result.seo_signals
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

            "recommended_actions": (
                result.recommended_actions
            ),

            "metadata": (
                result.metadata
            ),
        }