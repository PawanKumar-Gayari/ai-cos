"""
Contradiction Detector
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List
import re


# =============================================================
# CONTRADICTION
# =============================================================

@dataclass
class Contradiction:

    statement_a: str = ""

    statement_b: str = ""

    contradiction_type: str = "general"

    confidence_score: float = 0.0

    severity_score: float = 0.0

    numerical_conflict: bool = False

    temporal_conflict: bool = False

    semantic_conflict: bool = False

    factual_conflict: bool = False

    misinformation_risk: str = "low"

    trust_risk: str = "low"

    reasoning: List[str] = field(
        default_factory=list
    )

    metadata: Dict[str, Any] = field(
        default_factory=dict
    )

    def add_reasoning(
        self,
        message: str,
    ) -> None:

        if (
            message
            and
            message not in self.reasoning
        ):

            self.reasoning.append(
                message
            )


# =============================================================
# RESULT
# =============================================================

@dataclass
class ContradictionDetectorResult:

    total_statements: int = 0

    contradictions_detected: int = 0

    severe_contradictions: int = 0

    contradiction_score: float = 0.0

    consistency_score: float = 0.0

    reliability_score: float = 0.0

    contradictions: List[
        Contradiction
    ] = field(
        default_factory=list
    )

    misinformation_risk: str = "low"

    factual_consistency_risk: str = "low"

    trust_decay_risk: str = "low"

    recommendations: List[str] = field(
        default_factory=list
    )

    warnings: List[str] = field(
        default_factory=list
    )

    reasoning: List[str] = field(
        default_factory=list
    )

    recommended_actions: List[str] = field(
        default_factory=list
    )

    metadata: Dict[str, Any] = field(
        default_factory=dict
    )

    def add_reasoning(
        self,
        message: str,
    ) -> None:

        if (
            message
            and
            message not in self.reasoning
        ):

            self.reasoning.append(
                message
            )

    def add_warning(
        self,
        warning: str,
    ) -> None:

        if (
            warning
            and
            warning not in self.warnings
        ):

            self.warnings.append(
                warning
            )

    def add_recommendation(
        self,
        recommendation: str,
    ) -> None:

        if (
            recommendation
            and
            recommendation
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
            and
            action
            not in self.recommended_actions
        ):

            self.recommended_actions.append(
                action
            )


# =============================================================
# DETECTOR
# =============================================================

class ContradictionDetector:

    NEGATIVE_TERMS = [

        "not",
        "never",
        "false",
        "incorrect",
        "wrong",
        "no",
        "denied",
        "reject",
        "rejected",
        "closed",
        "stopped",
        "failed",
        "lost",
        "decrease",
        "decreased",
        "fall",
        "fell",
    ]

    POSITIVE_TERMS = [

        "is",
        "true",
        "correct",
        "confirmed",
        "yes",
        "released",
        "approved",
        "increase",
        "increased",
        "open",
        "opened",
        "started",
        "won",
        "passed",
        "rise",
        "rising",
    ]

    SEMANTIC_CONFLICT_PAIRS = [

        ("released", "denied"),

        ("approved", "rejected"),

        ("increase", "decrease"),

        ("increased", "decreased"),

        ("rise", "fall"),

        ("rises", "falls"),

        ("won", "lost"),

        ("pass", "fail"),

        ("passed", "failed"),

        ("open", "closed"),

        ("opened", "closed"),

        ("start", "stop"),

        ("started", "stopped"),

        ("allow", "deny"),

        ("allowed", "denied"),

        ("true", "false"),

        ("reduces", "increases"),

        ("reduce", "increase"),
    ]

    YEAR_PATTERN = re.compile(
        r"\b20\d{2}\b"
    )

    NUMBER_PATTERN = re.compile(
        r"\b\d+(?:\.\d+)?\b"
    )

    # =========================================================
    # DETECT
    # =========================================================

    def detect(
        self,
        content: str,
    ) -> Dict[str, Any]:

        result = (
            ContradictionDetectorResult()
        )

        statements = [

            item.strip()

            for item
            in re.split(
                r"[.\n]",
                content or "",
            )

            if item.strip()
        ]

        result.total_statements = (
            len(statements)
        )

        contradictions = []

        for i in range(
            len(statements)
        ):

            for j in range(
                i + 1,
                len(statements),
            ):

                contradiction = (
                    self._analyze_pair(
                        statements[i],
                        statements[j],
                    )
                )

                if contradiction:

                    contradictions.append(
                        contradiction
                    )

        result.contradictions = (
            contradictions
        )

        result.contradictions_detected = (
            len(contradictions)
        )

        result.severe_contradictions = sum(

            1

            for item
            in contradictions

            if item.severity_score >= 75
        )

        self._calculate_scores(
            result
        )

        self._detect_risks(
            result
        )

        self._finalize(
            result
        )

        return self.export(
            result
        )

    # =========================================================
    # ANALYZE PAIR
    # =========================================================

    def _analyze_pair(
        self,
        statement_a: str,
        statement_b: str,
    ) -> Contradiction | None:

        contradiction = (
            Contradiction()
        )

        contradiction.statement_a = (
            statement_a
        )

        contradiction.statement_b = (
            statement_b
        )

        conflict_detected = False

        statement_a_lower = (
            statement_a.lower()
        )

        statement_b_lower = (
            statement_b.lower()
        )

        words_a = set(
            statement_a_lower.split()
        )

        words_b = set(
            statement_b_lower.split()
        )

        shared_words = (
            words_a.intersection(
                words_b
            )
        )

        meaningful_shared_words = [

            item

            for item
            in shared_words

            if len(item) > 3
        ]

        shared_context = (
            len(
                meaningful_shared_words
            ) >= 1
        )

        # =====================================================
        # NUMERICAL
        # =====================================================

        numbers_a = self.NUMBER_PATTERN.findall(
            statement_a
        )

        numbers_b = self.NUMBER_PATTERN.findall(
            statement_b
        )

        if (

            shared_context
            and
            numbers_a
            and
            numbers_b
            and
            numbers_a != numbers_b
        ):

            contradiction.numerical_conflict = (
                True
            )

            contradiction.contradiction_type = (
                "numerical"
            )

            contradiction.confidence_score = (
                80.0
            )

            contradiction.severity_score = (
                75.0
            )

            conflict_detected = True

        # =====================================================
        # TEMPORAL
        # =====================================================

        years_a = self.YEAR_PATTERN.findall(
            statement_a
        )

        years_b = self.YEAR_PATTERN.findall(
            statement_b
        )

        if (

            shared_context
            and
            years_a
            and
            years_b
            and
            years_a != years_b
        ):

            contradiction.temporal_conflict = (
                True
            )

            contradiction.contradiction_type = (
                "temporal"
            )

            contradiction.confidence_score = max(
                contradiction.confidence_score,
                70.0,
            )

            contradiction.severity_score = max(
                contradiction.severity_score,
                65.0,
            )

            conflict_detected = True

        # =====================================================
        # SEMANTIC
        # =====================================================

        semantic_conflict_detected = False

        for positive_term, negative_term in (

            self.SEMANTIC_CONFLICT_PAIRS
        ):

            conflict_a = (

                positive_term in statement_a_lower
                and
                negative_term in statement_b_lower
            )

            conflict_b = (

                positive_term in statement_b_lower
                and
                negative_term in statement_a_lower
            )

            if (

                shared_context
                and
                (
                    conflict_a
                    or
                    conflict_b
                )
            ):

                semantic_conflict_detected = (
                    True
                )

                break

        positive_a = any(

            item in statement_a_lower

            for item
            in self.POSITIVE_TERMS
        )

        negative_b = any(

            item in statement_b_lower

            for item
            in self.NEGATIVE_TERMS
        )

        positive_b = any(

            item in statement_b_lower

            for item
            in self.POSITIVE_TERMS
        )

        negative_a = any(

            item in statement_a_lower

            for item
            in self.NEGATIVE_TERMS
        )

        basic_semantic_conflict = (

            (
                positive_a
                and
                negative_b
            )
            or
            (
                positive_b
                and
                negative_a
            )
        )

        if (

            shared_context
            and
            (
                semantic_conflict_detected
                or
                basic_semantic_conflict
            )
        ):

            contradiction.semantic_conflict = (
                True
            )

            contradiction.contradiction_type = (
                "semantic"
            )

            contradiction.confidence_score = max(
                contradiction.confidence_score,
                70.0,
            )

            contradiction.severity_score = max(
                contradiction.severity_score,
                65.0,
            )

            conflict_detected = True

        if not conflict_detected:

            return None

        contradiction.factual_conflict = (
            True
        )

        contradiction.misinformation_risk = (
            "medium"
        )

        contradiction.trust_risk = (
            "medium"
        )

        contradiction.add_reasoning(
            f"Detected "
            f"{contradiction.contradiction_type} "
            f"contradiction"
        )

        return contradiction

    # =========================================================
    # SCORES
    # =========================================================

    def _calculate_scores(
        self,
        result: ContradictionDetectorResult,
    ) -> None:

        if result.total_statements == 0:

            result.contradiction_score = (
                0.0
            )

            result.consistency_score = (
                100.0
            )

            result.reliability_score = (
                100.0
            )

            return

        contradiction_ratio = (

            result.contradictions_detected
            /
            result.total_statements
        )

        result.contradiction_score = round(

            contradiction_ratio * 100,

            2,
        )

        result.consistency_score = round(

            max(
                100 - result.contradiction_score,
                0,
            ),

            2,
        )

        result.reliability_score = round(

            result.consistency_score * 0.9,

            2,
        )

    # =========================================================
    # RISKS
    # =========================================================

    def _detect_risks(
        self,
        result: ContradictionDetectorResult,
    ) -> None:

        if result.severe_contradictions >= 1:

            result.misinformation_risk = (
                "high"
            )

            result.add_warning(
                "Severe factual contradictions detected"
            )

        if result.consistency_score < 60:

            result.factual_consistency_risk = (
                "high"
            )

        if result.contradictions_detected >= 2:

            result.trust_decay_risk = (
                "medium"
            )

    # =========================================================
    # FINALIZE
    # =========================================================

    def _finalize(
        self,
        result: ContradictionDetectorResult,
    ) -> None:

        if result.contradictions_detected > 0:

            result.add_recommendation(
                "Resolve contradictory statements"
            )

            result.add_action(
                "Run factual verification workflow"
            )

        if result.severe_contradictions > 0:

            result.add_recommendation(
                "Perform manual fact validation"
            )

        if result.consistency_score < 70:

            result.add_recommendation(
                "Improve factual consistency"
            )

        result.add_action(
            "Store contradiction intelligence"
        )

        result.add_reasoning(
            f"Consistency score: "
            f"{result.consistency_score}"
        )

    # =========================================================
    # EXPORT
    # =========================================================

    def export(
        self,
        result: ContradictionDetectorResult,
    ) -> Dict[str, Any]:

        return {

            "total_statements": (
                result.total_statements
            ),

            "contradictions_detected": (
                result.contradictions_detected
            ),

            "severe_contradictions": (
                result.severe_contradictions
            ),

            "contradiction_score": (
                result.contradiction_score
            ),

            "consistency_score": (
                result.consistency_score
            ),

            "reliability_score": (
                result.reliability_score
            ),

            "contradictions": [

                item.__dict__

                for item
                in result.contradictions
            ],

            "misinformation_risk": (
                result.misinformation_risk
            ),

            "factual_consistency_risk": (
                result.factual_consistency_risk
            ),

            "trust_decay_risk": (
                result.trust_decay_risk
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