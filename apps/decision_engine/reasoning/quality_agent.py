"""
Quality Agent

Purpose:
Analyze editorial quality, readability,
humanization, structure, engagement,
and content depth.

Analyzes:
- readability
- content depth
- structure quality
- humanization
- engagement quality
- repetition
- formatting quality

Goal:
Ensure AI_COS produces high-quality,
human-like editorial content.

This becomes the editorial quality
intelligence layer of AI_COS.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List


# =============================================================
# QUALITY RESULT
# =============================================================

@dataclass
class QualityResult:

    # =========================================================
    # SCORES
    # =========================================================

    quality_score: float = 0.0

    readability_score: float = 0.0

    engagement_score: float = 0.0

    structure_score: float = 0.0

    humanization_score: float = 0.0

    depth_score: float = 0.0

    # =========================================================
    # FLAGS
    # =========================================================

    quality_passed: bool = False

    human_like_content: bool = True

    engaging_content: bool = True

    rewrite_required: bool = False

    # =========================================================
    # RISKS
    # =========================================================

    quality_risk: str = "low"

    readability_risk: str = "low"

    ai_detection_risk: str = "low"

    thin_content_risk: str = "low"

    # =========================================================
    # DETECTIONS
    # =========================================================

    repetitive_content_detected: bool = False

    thin_content_detected: bool = False

    poor_structure_detected: bool = False

    ai_patterns_detected: bool = False

    low_engagement_detected: bool = False

    # =========================================================
    # METRICS
    # =========================================================

    word_count: int = 0

    paragraph_count: int = 0

    sentence_count: int = 0

    average_sentence_length: float = 0.0

    heading_count: int = 0

    # =========================================================
    # SIGNALS
    # =========================================================

    quality_signals: Dict[str, Any] = field(
        default_factory=dict
    )

    # =========================================================
    # PATTERNS
    # =========================================================

    detected_ai_patterns: List[str] = field(
        default_factory=list
    )

    repetitive_phrases: List[str] = field(
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
# QUALITY AGENT
# =============================================================

class QualityAgent:

    """
    Editorial quality intelligence agent.
    """

    # =========================================================
    # AI PATTERNS
    # =========================================================

    AI_PATTERNS = [

        "in conclusion",
        "it is important to note",
        "overall",
        "furthermore",
        "moreover",
        "additionally",
    ]

    # =========================================================
    # ENGAGEMENT WORDS
    # =========================================================

    ENGAGEMENT_WORDS = [

        "you",
        "your",
        "important",
        "help",
        "easy",
        "best",
        "guide",
    ]

    # =========================================================
    # ANALYZE
    # =========================================================

    def analyze(
        self,
        article: str,
    ) -> QualityResult:

        result = QualityResult()

        article = article or ""

        # =====================================================
        # BASIC METRICS
        # =====================================================

        self._calculate_metrics(
            result,
            article,
        )

        # =====================================================
        # READABILITY
        # =====================================================

        self._analyze_readability(
            result
        )

        # =====================================================
        # STRUCTURE
        # =====================================================

        self._analyze_structure(
            result,
            article,
        )

        # =====================================================
        # HUMANIZATION
        # =====================================================

        self._analyze_humanization(
            result,
            article,
        )

        # =====================================================
        # ENGAGEMENT
        # =====================================================

        self._analyze_engagement(
            result,
            article,
        )

        # =====================================================
        # DEPTH
        # =====================================================

        self._analyze_depth(
            result
        )

        # =====================================================
        # REPETITION
        # =====================================================

        self._detect_repetition(
            result,
            article,
        )

        # =====================================================
        # QUALITY SCORE
        # =====================================================

        self._calculate_quality_score(
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
    # METRICS
    # =========================================================

    def _calculate_metrics(
        self,
        result: QualityResult,
        article: str,
    ) -> None:

        words = article.split()

        result.word_count = len(words)

        result.paragraph_count = len([

            paragraph

            for paragraph
            in article.split("\n\n")

            if paragraph.strip()
        ])

        sentences = [

            sentence

            for sentence
            in article.replace("?", ".")
            .replace("!", ".")
            .split(".")

            if sentence.strip()
        ]

        result.sentence_count = len(
            sentences
        )

        # =====================================================
        # AVG SENTENCE
        # =====================================================

        if result.sentence_count > 0:

            result.average_sentence_length = round(

                result.word_count /

                result.sentence_count,

                2,
            )

        # =====================================================
        # HEADINGS
        # =====================================================

        result.heading_count = article.count(
            "#"
        )

    # =========================================================
    # READABILITY
    # =========================================================

    def _analyze_readability(
        self,
        result: QualityResult,
    ) -> None:

        score = 100

        # =====================================================
        # LONG SENTENCES
        # =====================================================

        if result.average_sentence_length > 30:

            score -= 30

            result.add_warning(
                "Sentences too long"
            )

        elif result.average_sentence_length > 22:

            score -= 15

        # =====================================================
        # VERY SHORT
        # =====================================================

        if result.word_count < 500:

            score -= 25

            result.thin_content_detected = (
                True
            )

        result.readability_score = round(

            max(score, 0),

            2,
        )

        result.add_reasoning(
            f"Readability score: "
            f"{result.readability_score}"
        )

    # =========================================================
    # STRUCTURE
    # =========================================================

    def _analyze_structure(
        self,
        result: QualityResult,
        article: str,
    ) -> None:

        score = 100

        # =====================================================
        # HEADINGS
        # =====================================================

        if result.heading_count == 0:

            score -= 35

            result.poor_structure_detected = (
                True
            )

            result.add_warning(
                "No headings detected"
            )

        # =====================================================
        # PARAGRAPHS
        # =====================================================

        if result.paragraph_count < 3:

            score -= 25

        result.structure_score = round(

            max(score, 0),

            2,
        )

    # =========================================================
    # HUMANIZATION
    # =========================================================

    def _analyze_humanization(
        self,
        result: QualityResult,
        article: str,
    ) -> None:

        score = 100

        ai_count = 0

        article_lower = article.lower()

        for pattern in self.AI_PATTERNS:

            if pattern in article_lower:

                ai_count += 1

                result.detected_ai_patterns.append(
                    pattern
                )

        # =====================================================
        # AI RISK
        # =====================================================

        if ai_count >= 4:

            result.ai_patterns_detected = (
                True
            )

            score -= 40

            result.add_warning(
                "AI writing patterns detected"
            )

        elif ai_count >= 2:

            score -= 20

        result.humanization_score = round(

            max(score, 0),

            2,
        )

    # =========================================================
    # ENGAGEMENT
    # =========================================================

    def _analyze_engagement(
        self,
        result: QualityResult,
        article: str,
    ) -> None:

        article_lower = article.lower()

        engagement = 50

        for word in self.ENGAGEMENT_WORDS:

            if word in article_lower:

                engagement += 5

        # =====================================================
        # LOW ENGAGEMENT
        # =====================================================

        if engagement < 60:

            result.low_engagement_detected = (
                True
            )

        result.engagement_score = round(

            min(engagement, 100),

            2,
        )

    # =========================================================
    # DEPTH
    # =========================================================

    def _analyze_depth(
        self,
        result: QualityResult,
    ) -> None:

        depth = 0

        # =====================================================
        # WORD COUNT
        # =====================================================

        if result.word_count >= 2000:

            depth += 100

        elif result.word_count >= 1500:

            depth += 80

        elif result.word_count >= 1000:

            depth += 65

        elif result.word_count >= 700:

            depth += 50

        else:

            depth += 30

            result.thin_content_detected = (
                True
            )

        result.depth_score = round(
            depth,
            2,
        )

    # =========================================================
    # REPETITION
    # =========================================================

    def _detect_repetition(
        self,
        result: QualityResult,
        article: str,
    ) -> None:

        article_lower = article.lower()

        common_phrases = [

            "in conclusion",
            "it is important",
            "overall",
        ]

        for phrase in common_phrases:

            count = article_lower.count(
                phrase
            )

            if count >= 2:

                result.repetitive_content_detected = (
                    True
                )

                result.repetitive_phrases.append(
                    phrase
                )

                result.add_warning(
                    f"Repetitive phrase detected: {phrase}"
                )

    # =========================================================
    # QUALITY SCORE
    # =========================================================

    def _calculate_quality_score(
        self,
        result: QualityResult,
    ) -> None:

        quality = (

            result.readability_score * 0.25

            +

            result.structure_score * 0.20

            +

            result.humanization_score * 0.20

            +

            result.engagement_score * 0.15

            +

            result.depth_score * 0.20
        )

        # =====================================================
        # PENALTIES
        # =====================================================

        if result.repetitive_content_detected:

            quality -= 10

        if result.ai_patterns_detected:

            quality -= 15

        if result.thin_content_detected:

            quality -= 20

        result.quality_score = round(

            max(quality, 0),

            2,
        )

        result.add_reasoning(
            f"Quality score calculated: "
            f"{result.quality_score}"
        )

    # =========================================================
    # FINALIZE
    # =========================================================

    def _finalize(
        self,
        result: QualityResult,
    ) -> None:

        # =====================================================
        # PASSED
        # =====================================================

        result.quality_passed = (
            result.quality_score >= 65
        )

        # =====================================================
        # RISK
        # =====================================================

        if result.quality_score >= 85:

            result.quality_risk = "low"

        elif result.quality_score >= 65:

            result.quality_risk = "medium"

        else:

            result.quality_risk = "high"

        # =====================================================
        # AI DETECTION
        # =====================================================

        if result.ai_patterns_detected:

            result.ai_detection_risk = (
                "high"
            )

            result.human_like_content = (
                False
            )

        # =====================================================
        # THIN CONTENT
        # =====================================================

        if result.thin_content_detected:

            result.thin_content_risk = (
                "high"
            )

        # =====================================================
        # REWRITE
        # =====================================================

        if (

            result.quality_score < 60

            or

            result.ai_patterns_detected

            or

            result.poor_structure_detected
        ):

            result.rewrite_required = (
                True
            )

        # =====================================================
        # RECOMMENDATIONS
        # =====================================================

        if result.thin_content_detected:

            result.add_recommendation(
                "Increase article depth"
            )

            result.add_action(
                "Add more detailed sections"
            )

        if result.poor_structure_detected:

            result.add_recommendation(
                "Improve article structure"
            )

            result.add_action(
                "Add headings and sections"
            )

        if result.ai_patterns_detected:

            result.add_recommendation(
                "Humanize writing style"
            )

            result.add_action(
                "Reduce AI-style transitions"
            )

        if result.low_engagement_detected:

            result.add_recommendation(
                "Improve reader engagement"
            )

        result.add_reasoning(
            f"Final quality score: "
            f"{result.quality_score}"
        )

    # =========================================================
    # EXPORT
    # =========================================================

    def export(
        self,
        result: QualityResult,
    ) -> Dict[str, Any]:

        return {

            "quality_score": (
                result.quality_score
            ),

            "readability_score": (
                result.readability_score
            ),

            "engagement_score": (
                result.engagement_score
            ),

            "structure_score": (
                result.structure_score
            ),

            "humanization_score": (
                result.humanization_score
            ),

            "depth_score": (
                result.depth_score
            ),

            "quality_passed": (
                result.quality_passed
            ),

            "human_like_content": (
                result.human_like_content
            ),

            "engaging_content": (
                result.engaging_content
            ),

            "rewrite_required": (
                result.rewrite_required
            ),

            "quality_risk": (
                result.quality_risk
            ),

            "readability_risk": (
                result.readability_risk
            ),

            "ai_detection_risk": (
                result.ai_detection_risk
            ),

            "thin_content_risk": (
                result.thin_content_risk
            ),

            "repetitive_content_detected": (
                result.repetitive_content_detected
            ),

            "thin_content_detected": (
                result.thin_content_detected
            ),

            "poor_structure_detected": (
                result.poor_structure_detected
            ),

            "ai_patterns_detected": (
                result.ai_patterns_detected
            ),

            "low_engagement_detected": (
                result.low_engagement_detected
            ),

            "word_count": (
                result.word_count
            ),

            "paragraph_count": (
                result.paragraph_count
            ),

            "sentence_count": (
                result.sentence_count
            ),

            "average_sentence_length": (
                result.average_sentence_length
            ),

            "heading_count": (
                result.heading_count
            ),

            "detected_ai_patterns": (
                result.detected_ai_patterns
            ),

            "repetitive_phrases": (
                result.repetitive_phrases
            ),

            "quality_signals": (
                result.quality_signals
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