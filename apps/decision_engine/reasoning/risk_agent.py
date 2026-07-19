"""
Risk Agent

Purpose:
Detect dangerous content risks, hallucinations,
misinformation, spam patterns, and unsafe
editorial signals.

Analyzes:
- hallucination risk
- misinformation risk
- unverifiable claims
- spam signals
- SEO manipulation
- low-confidence content
- unsafe authority patterns

Goal:
Protect AI_COS from unsafe publishing.

This becomes the editorial safety intelligence
layer of AI_COS.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List


# =============================================================
# RISK RESULT
# =============================================================

@dataclass
class RiskResult:

    # =========================================================
    # SCORES
    # =========================================================

    risk_score: float = 0.0

    hallucination_score: float = 0.0

    misinformation_score: float = 0.0

    spam_score: float = 0.0

    confidence_risk_score: float = 0.0

    # =========================================================
    # FLAGS
    # =========================================================

    safe_to_publish: bool = True

    human_review_required: bool = False

    rewrite_required: bool = False

    verification_required: bool = False

    # =========================================================
    # RISKS
    # =========================================================

    overall_risk: str = "low"

    hallucination_risk: str = "low"

    misinformation_risk: str = "low"

    spam_risk: str = "low"

    seo_manipulation_risk: str = "low"

    # =========================================================
    # DETECTIONS
    # =========================================================

    hallucination_detected: bool = False

    unverifiable_claims_detected: bool = False

    keyword_stuffing_detected: bool = False

    clickbait_detected: bool = False

    ai_generated_pattern_detected: bool = False

    excessive_certainty_detected: bool = False

    # =========================================================
    # SIGNALS
    # =========================================================

    risk_signals: Dict[str, Any] = field(
        default_factory=dict
    )

    # =========================================================
    # DETECTED PATTERNS
    # =========================================================

    hallucination_patterns: List[str] = field(
        default_factory=list
    )

    spam_patterns: List[str] = field(
        default_factory=list
    )

    clickbait_patterns: List[str] = field(
        default_factory=list
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


# =============================================================
# RISK AGENT
# =============================================================

class RiskAgent:

    """
    Editorial safety and hallucination
    intelligence agent.
    """

    # =========================================================
    # HALLUCINATION PATTERNS
    # =========================================================

    HALLUCINATION_PATTERNS = [

        "guaranteed result",
        "100% accurate",
        "always works",
        "confirmed leak",
        "secret formula",
        "miracle cure",
        "instant success",
    ]

    # =========================================================
    # CLICKBAIT PATTERNS
    # =========================================================

    CLICKBAIT_PATTERNS = [

        "you won't believe",
        "shocking",
        "mind blowing",
        "secret revealed",
        "viral trick",
        "unbelievable",
    ]

    # =========================================================
    # SPAM PATTERNS
    # =========================================================

    SPAM_PATTERNS = [

        "buy now",
        "limited time",
        "click here",
        "free money",
        "earn instantly",
    ]

    # =========================================================
    # ANALYZE
    # =========================================================

    def analyze(
        self,
        article: str,
        keyword: str = "",
    ) -> RiskResult:

        result = RiskResult()

        article = (
            article or ""
        ).lower()

        keyword = (
            keyword or ""
        ).lower()

        # =====================================================
        # HALLUCINATION
        # =====================================================

        self._detect_hallucinations(
            result,
            article,
        )

        # =====================================================
        # SPAM
        # =====================================================

        self._detect_spam(
            result,
            article,
        )

        # =====================================================
        # CLICKBAIT
        # =====================================================

        self._detect_clickbait(
            result,
            article,
        )

        # =====================================================
        # SEO MANIPULATION
        # =====================================================

        self._detect_keyword_stuffing(
            result,
            article,
            keyword,
        )

        # =====================================================
        # AI PATTERNS
        # =====================================================

        self._detect_ai_patterns(
            result,
            article,
        )

        # =====================================================
        # SCORE
        # =====================================================

        self._calculate_scores(
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
    # HALLUCINATIONS
    # =========================================================

    def _detect_hallucinations(
        self,
        result: RiskResult,
        article: str,
    ) -> None:

        for pattern in self.HALLUCINATION_PATTERNS:

            if pattern in article:

                result.hallucination_detected = (
                    True
                )

                result.hallucination_patterns.append(
                    pattern
                )

                result.add_warning(
                    f"Hallucination pattern detected: {pattern}"
                )

        # =====================================================
        # CERTAINTY
        # =====================================================

        certainty_patterns = [

            "definitely",
            "absolutely",
            "certainly",
            "undoubtedly",
        ]

        for pattern in certainty_patterns:

            if pattern in article:

                result.excessive_certainty_detected = (
                    True
                )

        # =====================================================
        # CLAIMS
        # =====================================================

        if (

            "according to experts"

            in article

            and

            "source" not in article
        ):

            result.unverifiable_claims_detected = (
                True
            )

            result.add_warning(
                "Expert claim without source detected"
            )

    # =========================================================
    # SPAM
    # =========================================================

    def _detect_spam(
        self,
        result: RiskResult,
        article: str,
    ) -> None:

        for pattern in self.SPAM_PATTERNS:

            if pattern in article:

                result.spam_patterns.append(
                    pattern
                )

                result.add_warning(
                    f"Spam signal detected: {pattern}"
                )

        # =====================================================
        # RISK
        # =====================================================

        if result.spam_patterns:

            result.spam_risk = (
                "high"
            )

    # =========================================================
    # CLICKBAIT
    # =========================================================

    def _detect_clickbait(
        self,
        result: RiskResult,
        article: str,
    ) -> None:

        for pattern in self.CLICKBAIT_PATTERNS:

            if pattern in article:

                result.clickbait_detected = (
                    True
                )

                result.clickbait_patterns.append(
                    pattern
                )

                result.add_warning(
                    f"Clickbait pattern detected: {pattern}"
                )

    # =========================================================
    # KEYWORD STUFFING
    # =========================================================

    def _detect_keyword_stuffing(
        self,
        result: RiskResult,
        article: str,
        keyword: str,
    ) -> None:

        if not keyword:
            return

        count = article.count(keyword)

        word_count = max(
            len(article.split()),
            1,
        )

        density = (
            count / word_count
        ) * 100

        result.risk_signals[
            "keyword_density"
        ] = round(
            density,
            2,
        )

        if density > 5:

            result.keyword_stuffing_detected = (
                True
            )

            result.add_warning(
                "Keyword stuffing detected"
            )

    # =========================================================
    # AI PATTERNS
    # =========================================================

    def _detect_ai_patterns(
        self,
        result: RiskResult,
        article: str,
    ) -> None:

        ai_patterns = [

            "in conclusion",
            "it is important to note",
            "overall",
            "furthermore",
            "moreover",
        ]

        count = 0

        for pattern in ai_patterns:

            if pattern in article:

                count += 1

        if count >= 4:

            result.ai_generated_pattern_detected = (
                True
            )

            result.add_warning(
                "AI-generated writing patterns detected"
            )

    # =========================================================
    # SCORES
    # =========================================================

    def _calculate_scores(
        self,
        result: RiskResult,
    ) -> None:

        hallucination = 0

        misinformation = 0

        spam = 0

        # =====================================================
        # HALLUCINATION
        # =====================================================

        hallucination += (
            len(
                result.hallucination_patterns
            ) * 20
        )

        if result.unverifiable_claims_detected:

            hallucination += 25

        if result.excessive_certainty_detected:

            hallucination += 10

        # =====================================================
        # SPAM
        # =====================================================

        spam += (
            len(
                result.spam_patterns
            ) * 20
        )

        if result.keyword_stuffing_detected:

            spam += 30

        if result.clickbait_detected:

            spam += 20

        # =====================================================
        # MISINFORMATION
        # =====================================================

        misinformation += (
            hallucination * 0.8
        )

        # =====================================================
        # FINAL SCORES
        # =====================================================

        result.hallucination_score = round(

            min(hallucination, 100),

            2,
        )

        result.spam_score = round(

            min(spam, 100),

            2,
        )

        result.misinformation_score = round(

            min(misinformation, 100),

            2,
        )

        result.risk_score = round(

            min(

                (
                    result.hallucination_score +

                    result.spam_score +

                    result.misinformation_score
                ) / 3,

                100,
            ),

            2,
        )

        result.confidence_risk_score = (
            result.risk_score
        )

        result.add_reasoning(
            f"Risk score calculated: "
            f"{result.risk_score}"
        )

    # =========================================================
    # FINALIZE
    # =========================================================

    def _finalize(
        self,
        result: RiskResult,
    ) -> None:

        # =====================================================
        # OVERALL RISK
        # =====================================================

        if result.risk_score >= 80:

            result.overall_risk = (
                "critical"
            )

        elif result.risk_score >= 60:

            result.overall_risk = (
                "high"
            )

        elif result.risk_score >= 35:

            result.overall_risk = (
                "medium"
            )

        else:

            result.overall_risk = (
                "low"
            )

        # =====================================================
        # HALLUCINATION RISK
        # =====================================================

        if result.hallucination_score >= 60:

            result.hallucination_risk = (
                "high"
            )

        elif result.hallucination_score >= 35:

            result.hallucination_risk = (
                "medium"
            )

        else:

            result.hallucination_risk = (
                "low"
            )

        # =====================================================
        # SAFE TO PUBLISH
        # =====================================================

        result.safe_to_publish = (

            result.risk_score < 60

            and

            not result.hallucination_detected
        )

        # =====================================================
        # REVIEW
        # =====================================================

        if result.risk_score >= 50:

            result.human_review_required = (
                True
            )

        # =====================================================
        # REWRITE
        # =====================================================

        if (

            result.keyword_stuffing_detected

            or

            result.clickbait_detected

            or

            result.ai_generated_pattern_detected
        ):

            result.rewrite_required = (
                True
            )

        # =====================================================
        # VERIFY
        # =====================================================

        if (

            result.unverifiable_claims_detected

            or

            result.hallucination_detected
        ):

            result.verification_required = (
                True
            )

        # =====================================================
        # RECOMMENDATIONS
        # =====================================================

        if result.hallucination_detected:

            result.add_recommendation(
                "Verify claims using trusted sources"
            )

        if result.keyword_stuffing_detected:

            result.add_recommendation(
                "Reduce keyword density"
            )

        if result.clickbait_detected:

            result.add_recommendation(
                "Remove clickbait language"
            )

        if result.ai_generated_pattern_detected:

            result.add_recommendation(
                "Humanize article writing style"
            )

        result.add_reasoning(
            f"Final overall risk: "
            f"{result.overall_risk}"
        )

    # =========================================================
    # EXPORT
    # =========================================================

    def export(
        self,
        result: RiskResult,
    ) -> Dict[str, Any]:

        return {

            "risk_score": (
                result.risk_score
            ),

            "hallucination_score": (
                result.hallucination_score
            ),

            "misinformation_score": (
                result.misinformation_score
            ),

            "spam_score": (
                result.spam_score
            ),

            "confidence_risk_score": (
                result.confidence_risk_score
            ),

            "safe_to_publish": (
                result.safe_to_publish
            ),

            "human_review_required": (
                result.human_review_required
            ),

            "rewrite_required": (
                result.rewrite_required
            ),

            "verification_required": (
                result.verification_required
            ),

            "overall_risk": (
                result.overall_risk
            ),

            "hallucination_risk": (
                result.hallucination_risk
            ),

            "misinformation_risk": (
                result.misinformation_risk
            ),

            "spam_risk": (
                result.spam_risk
            ),

            "seo_manipulation_risk": (
                result.seo_manipulation_risk
            ),

            "hallucination_detected": (
                result.hallucination_detected
            ),

            "unverifiable_claims_detected": (
                result.unverifiable_claims_detected
            ),

            "keyword_stuffing_detected": (
                result.keyword_stuffing_detected
            ),

            "clickbait_detected": (
                result.clickbait_detected
            ),

            "ai_generated_pattern_detected": (
                result.ai_generated_pattern_detected
            ),

            "excessive_certainty_detected": (
                result.excessive_certainty_detected
            ),

            "hallucination_patterns": (
                result.hallucination_patterns
            ),

            "spam_patterns": (
                result.spam_patterns
            ),

            "clickbait_patterns": (
                result.clickbait_patterns
            ),

            "risk_signals": (
                result.risk_signals
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