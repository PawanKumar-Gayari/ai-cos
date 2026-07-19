"""
Content Risk Analyzer

Purpose:
Detect risks before publishing.

This engine analyzes:
- hallucination risk
- factual risk
- spam risk
- SEO over-optimization
- outdated content
- YMYL risks
- unsupported claims
- trust degradation

Goal:
Act as an AI safety firewall for the
editorial intelligence system.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List
import re


# =============================================================
# RISK RESULT
# =============================================================

@dataclass
class ContentRiskResult:

    # =========================================================
    # OVERALL
    # =========================================================

    risk_score: float = 0.0

    risk_level: str = "low"

    safe_to_publish: bool = True

    # =========================================================
    # HALLUCINATION
    # =========================================================

    hallucination_risk: str = "low"

    unsupported_claims_detected: bool = False

    unsupported_claims_count: int = 0

    # =========================================================
    # FACTUAL RISK
    # =========================================================

    factual_risk: str = "low"

    outdated_information_detected: bool = False

    contradictory_information_detected: bool = False

    # =========================================================
    # SEO RISK
    # =========================================================

    keyword_stuffing_detected: bool = False

    spam_risk: str = "low"

    over_optimization_detected: bool = False

    # =========================================================
    # TRUST RISK
    # =========================================================

    trust_risk: str = "low"

    weak_sources_detected: bool = False

    missing_citations_detected: bool = False

    # =========================================================
    # YMYL
    # =========================================================

    ymyl_risk_detected: bool = False

    expert_review_required: bool = False

    legal_risk_detected: bool = False

    medical_risk_detected: bool = False

    financial_risk_detected: bool = False

    # =========================================================
    # REVIEW FLAGS
    # =========================================================

    rewrite_required: bool = False

    human_review_required: bool = False

    publishing_blocked: bool = False

    # =========================================================
    # SIGNALS
    # =========================================================

    detected_risks: List[str] = field(
        default_factory=list
    )

    risk_signals: Dict[str, Any] = field(
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

    def add_risk(
        self,
        risk: str,
    ) -> None:

        if (
            risk
            and risk not in self.detected_risks
        ):

            self.detected_risks.append(risk)

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
# CONTENT RISK ANALYZER
# =============================================================

class ContentRiskAnalyzer:

    """
    Editorial AI safety firewall.
    """

    # =========================================================
    # MAIN
    # =========================================================

    def analyze(
        self,
        content: str,
        topic: str = "",
        niche: str = "default",
    ) -> ContentRiskResult:

        result = ContentRiskResult()

        content = content or ""

        topic = (topic or "").lower()

        niche = (niche or "").lower()

        # =====================================================
        # HALLUCINATION
        # =====================================================

        self._detect_hallucination_risk(
            result,
            content,
        )

        # =====================================================
        # FACTUAL RISKS
        # =====================================================

        self._detect_factual_risks(
            result,
            content,
        )

        # =====================================================
        # SEO RISKS
        # =====================================================

        self._detect_seo_risks(
            result,
            content,
        )

        # =====================================================
        # TRUST RISKS
        # =====================================================

        self._detect_trust_risks(
            result,
            content,
        )

        # =====================================================
        # YMYL
        # =====================================================

        self._detect_ymyl_risks(
            result,
            topic,
            niche,
        )

        # =====================================================
        # FINAL SCORE
        # =====================================================

        self._calculate_risk_score(
            result
        )

        # =====================================================
        # FINAL DECISION
        # =====================================================

        self._evaluate_publish_safety(
            result
        )

        return result

    # =========================================================
    # HALLUCINATION
    # =========================================================

    def _detect_hallucination_risk(
        self,
        result: ContentRiskResult,
        content: str,
    ) -> None:

        suspicious_patterns = [

            "according to experts",

            "research proves",

            "scientists say",

            "guaranteed results",

            "100% effective",
        ]

        matches = 0

        for pattern in suspicious_patterns:

            found = re.findall(
                pattern,
                content,
                re.IGNORECASE,
            )

            matches += len(found)

        result.unsupported_claims_count = matches

        if matches >= 5:

            result.hallucination_risk = "high"

            result.unsupported_claims_detected = True

            result.add_warning(
                "High unsupported claim density detected"
            )

            result.add_risk(
                "hallucination_risk"
            )

        elif matches >= 2:

            result.hallucination_risk = "medium"

    # =========================================================
    # FACTUAL
    # =========================================================

    def _detect_factual_risks(
        self,
        result: ContentRiskResult,
        content: str,
    ) -> None:

        outdated_patterns = [

            "2022",
            "2023",
        ]

        if any(
            pattern in content
            for pattern in outdated_patterns
        ):

            result.outdated_information_detected = True

            result.factual_risk = "medium"

            result.add_warning(
                "Potential outdated information detected"
            )

            result.add_risk(
                "outdated_information"
            )

    # =========================================================
    # SEO
    # =========================================================

    def _detect_seo_risks(
        self,
        result: ContentRiskResult,
        content: str,
    ) -> None:

        words = content.lower().split()

        if not words:
            return

        unique_words = len(set(words))

        total_words = len(words)

        # =====================================================
        # KEYWORD STUFFING HEURISTIC
        # =====================================================

        if total_words > 0:

            repetition_ratio = (
                1 - (unique_words / total_words)
            )

            if repetition_ratio >= 0.55:

                result.keyword_stuffing_detected = True

                result.spam_risk = "high"

                result.over_optimization_detected = True

                result.add_warning(
                    "Potential keyword stuffing detected"
                )

                result.add_risk(
                    "seo_spam_risk"
                )

            elif repetition_ratio >= 0.40:

                result.spam_risk = "medium"

    # =========================================================
    # TRUST
    # =========================================================

    def _detect_trust_risks(
        self,
        result: ContentRiskResult,
        content: str,
    ) -> None:

        citation_patterns = [

            "source:",
            "according to",
            "official",
            "reference",
        ]

        citation_found = any(

            pattern in content.lower()

            for pattern in citation_patterns
        )

        if not citation_found:

            result.missing_citations_detected = True

            result.trust_risk = "medium"

            result.add_warning(
                "Missing trust/citation signals"
            )

            result.add_risk(
                "missing_citations"
            )

    # =========================================================
    # YMYL
    # =========================================================

    def _detect_ymyl_risks(
        self,
        result: ContentRiskResult,
        topic: str,
        niche: str,
    ) -> None:

        ymyl_keywords = [

            "health",
            "medicine",
            "loan",
            "finance",
            "investment",
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

            result.ymyl_risk_detected = True

            result.expert_review_required = True

            result.add_warning(
                "YMYL-sensitive content detected"
            )

            result.add_risk(
                "ymyl_risk"
            )

            # =================================================
            # CATEGORY
            # =================================================

            if "health" in topic:

                result.medical_risk_detected = True

            if (
                "finance" in topic
                or
                "investment" in topic
            ):

                result.financial_risk_detected = True

            if (
                "legal" in topic
                or
                "tax" in topic
            ):

                result.legal_risk_detected = True

    # =========================================================
    # SCORE
    # =========================================================

    def _calculate_risk_score(
        self,
        result: ContentRiskResult,
    ) -> None:

        score = 0

        if (
            result.hallucination_risk
            == "high"
        ):
            score += 35

        elif (
            result.hallucination_risk
            == "medium"
        ):
            score += 20

        if (
            result.spam_risk == "high"
        ):
            score += 25

        elif (
            result.spam_risk == "medium"
        ):
            score += 10

        if result.ymyl_risk_detected:
            score += 20

        if result.outdated_information_detected:
            score += 10

        if result.missing_citations_detected:
            score += 10

        result.risk_score = min(
            score,
            100,
        )

        # =====================================================
        # LEVEL
        # =====================================================

        if result.risk_score >= 70:

            result.risk_level = "critical"

        elif result.risk_score >= 50:

            result.risk_level = "high"

        elif result.risk_score >= 25:

            result.risk_level = "medium"

        else:

            result.risk_level = "low"

    # =========================================================
    # SAFETY
    # =========================================================

    def _evaluate_publish_safety(
        self,
        result: ContentRiskResult,
    ) -> None:

        # =====================================================
        # BLOCK
        # =====================================================

        if (
            result.risk_level == "critical"
        ):

            result.publishing_blocked = True

            result.safe_to_publish = False

            result.human_review_required = True

            result.add_warning(
                "Publishing blocked due to critical risks"
            )

            return

        # =====================================================
        # HUMAN REVIEW
        # =====================================================

        if (

            result.hallucination_risk == "high"

            or

            result.ymyl_risk_detected
        ):

            result.human_review_required = True

            result.add_warning(
                "Human review recommended"
            )

        # =====================================================
        # REWRITE
        # =====================================================

        if (

            result.keyword_stuffing_detected

            or

            result.outdated_information_detected
        ):

            result.rewrite_required = True

            result.add_recommendation(
                "Rewrite affected sections"
            )

    # =========================================================
    # EXPORT
    # =========================================================

    def export(
        self,
        result: ContentRiskResult,
    ) -> Dict[str, Any]:

        return {

            "risk_score": (
                result.risk_score
            ),

            "risk_level": (
                result.risk_level
            ),

            "safe_to_publish": (
                result.safe_to_publish
            ),

            "hallucination_risk": (
                result.hallucination_risk
            ),

            "unsupported_claims_detected": (
                result.unsupported_claims_detected
            ),

            "unsupported_claims_count": (
                result.unsupported_claims_count
            ),

            "factual_risk": (
                result.factual_risk
            ),

            "outdated_information_detected": (
                result.outdated_information_detected
            ),

            "contradictory_information_detected": (
                result.contradictory_information_detected
            ),

            "keyword_stuffing_detected": (
                result.keyword_stuffing_detected
            ),

            "spam_risk": (
                result.spam_risk
            ),

            "over_optimization_detected": (
                result.over_optimization_detected
            ),

            "trust_risk": (
                result.trust_risk
            ),

            "weak_sources_detected": (
                result.weak_sources_detected
            ),

            "missing_citations_detected": (
                result.missing_citations_detected
            ),

            "ymyl_risk_detected": (
                result.ymyl_risk_detected
            ),

            "expert_review_required": (
                result.expert_review_required
            ),

            "legal_risk_detected": (
                result.legal_risk_detected
            ),

            "medical_risk_detected": (
                result.medical_risk_detected
            ),

            "financial_risk_detected": (
                result.financial_risk_detected
            ),

            "rewrite_required": (
                result.rewrite_required
            ),

            "human_review_required": (
                result.human_review_required
            ),

            "publishing_blocked": (
                result.publishing_blocked
            ),

            "detected_risks": (
                result.detected_risks
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