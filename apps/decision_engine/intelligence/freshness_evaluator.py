"""
Freshness Evaluator

Purpose:
Evaluate:
- content freshness
- decay probability
- update urgency
- freshness competitiveness
- content validity window

Critical for:
- jobs
- exams
- news
- finance
- technology
- rapidly evolving topics

Goal:
Power automated freshness intelligence.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Any, List


# =============================================================
# RESULT
# =============================================================

@dataclass
class FreshnessEvaluationResult:

    # =========================================================
    # SCORES
    # =========================================================

    freshness_score: float = 0.0

    freshness_confidence: float = 0.0

    decay_probability: float = 0.0

    # =========================================================
    # STATUS
    # =========================================================

    freshness_valid: bool = True

    freshness_required: bool = False

    update_required: bool = False

    reverification_required: bool = False

    # =========================================================
    # AGE
    # =========================================================

    content_age_days: int = 0

    max_age_days: int = 30

    # =========================================================
    # DECAY
    # =========================================================

    decay_risk: str = "low"

    predicted_decay_days: int = 0

    traffic_decay_risk: str = "low"

    ranking_decay_risk: str = "low"

    # =========================================================
    # SIGNALS
    # =========================================================

    freshness_sensitive_topic: bool = False

    real_time_topic: bool = False

    outdated_information_detected: bool = False

    outdated_dates_detected: bool = False

    outdated_statistics_detected: bool = False

    outdated_links_detected: bool = False

    # =========================================================
    # COMPETITION
    # =========================================================

    freshness_competition: str = "medium"

    freshness_pressure_score: float = 0.0

    # =========================================================
    # PRIORITY
    # =========================================================

    update_priority: str = "medium"

    update_deadline_hours: int = 24

    # =========================================================
    # RECOMMENDATIONS
    # =========================================================

    recommended_actions: List[str] = field(
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
    # SIGNALS
    # =========================================================

    freshness_signals: Dict[str, Any] = field(
        default_factory=dict
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
# FRESHNESS EVALUATOR
# =============================================================

class FreshnessEvaluator:

    """
    Freshness intelligence engine.
    """

    # =========================================================
    # MAIN
    # =========================================================

    def evaluate(
        self,
        topic: str,
        content: str = "",
        published_at: datetime = None,
        niche: str = "default",
        serp_data: Dict[str, Any] = None,
    ) -> FreshnessEvaluationResult:

        serp_data = serp_data or {}

        result = FreshnessEvaluationResult()

        topic = (topic or "").lower()

        niche = (niche or "").lower()

        content = content or ""

        # =====================================================
        # AGE
        # =====================================================

        self._calculate_age(
            result,
            published_at,
        )

        # =====================================================
        # TOPIC TYPE
        # =====================================================

        self._detect_freshness_sensitive_topic(
            result,
            topic,
            niche,
        )

        # =====================================================
        # OUTDATED SIGNALS
        # =====================================================

        self._detect_outdated_content(
            result,
            content,
        )

        # =====================================================
        # SERP PRESSURE
        # =====================================================

        self._analyze_serp_freshness_pressure(
            result,
            serp_data,
        )

        # =====================================================
        # DECAY
        # =====================================================

        self._calculate_decay(
            result
        )

        # =====================================================
        # FINAL SCORE
        # =====================================================

        self._calculate_freshness_score(
            result
        )

        # =====================================================
        # UPDATE STRATEGY
        # =====================================================

        self._evaluate_update_requirements(
            result
        )

        return result

    # =========================================================
    # AGE
    # =========================================================

    def _calculate_age(
        self,
        result: FreshnessEvaluationResult,
        published_at: datetime = None,
    ) -> None:

        if not published_at:

            result.content_age_days = 0

            return

        now = datetime.utcnow()

        delta = now - published_at

        result.content_age_days = delta.days

    # =========================================================
    # TOPIC DETECTION
    # =========================================================

    def _detect_freshness_sensitive_topic(
        self,
        result: FreshnessEvaluationResult,
        topic: str,
        niche: str,
    ) -> None:

        freshness_keywords = [

            "latest",
            "news",
            "result",
            "notification",
            "exam",
            "admit card",
            "update",
            "today",
            "breaking",
        ]

        if (

            niche in [
                "jobs",
                "finance",
                "tech",
                "news",
            ]

            or

            any(
                keyword in topic
                for keyword in freshness_keywords
            )
        ):

            result.freshness_required = True

            result.freshness_sensitive_topic = True

            result.max_age_days = 7

            result.update_priority = "high"

            result.update_deadline_hours = 6

            result.add_reasoning(
                "Freshness-sensitive topic detected"
            )

        # =====================================================
        # REAL-TIME
        # =====================================================

        if any(

            keyword in topic

            for keyword in [
                "breaking",
                "today",
                "live",
            ]
        ):

            result.real_time_topic = True

            result.max_age_days = 1

            result.add_warning(
                "Real-time topic detected"
            )

    # =========================================================
    # OUTDATED
    # =========================================================

    def _detect_outdated_content(
        self,
        result: FreshnessEvaluationResult,
        content: str,
    ) -> None:

        outdated_years = [

            "2022",
            "2023",
        ]

        if any(
            year in content
            for year in outdated_years
        ):

            result.outdated_dates_detected = True

            result.outdated_information_detected = True

            result.add_warning(
                "Outdated dates detected"
            )

        outdated_patterns = [

            "last year",
            "coming soon",
            "upcoming",
        ]

        if any(

            pattern in content.lower()

            for pattern in outdated_patterns
        ):

            result.outdated_information_detected = True

            result.add_warning(
                "Potential outdated contextual phrases detected"
            )

    # =========================================================
    # SERP PRESSURE
    # =========================================================

    def _analyze_serp_freshness_pressure(
        self,
        result: FreshnessEvaluationResult,
        serp_data: Dict[str, Any],
    ) -> None:

        recent_results = serp_data.get(
            "recent_results",
            0,
        )

        if recent_results >= 7:

            result.freshness_competition = (
                "very_high"
            )

            result.freshness_pressure_score = 90

            result.add_warning(
                "SERP heavily favors fresh content"
            )

        elif recent_results >= 4:

            result.freshness_competition = (
                "high"
            )

            result.freshness_pressure_score = 70

        elif recent_results >= 2:

            result.freshness_competition = (
                "medium"
            )

            result.freshness_pressure_score = 50

        else:

            result.freshness_competition = (
                "low"
            )

            result.freshness_pressure_score = 20

    # =========================================================
    # DECAY
    # =========================================================

    def _calculate_decay(
        self,
        result: FreshnessEvaluationResult,
    ) -> None:

        age_ratio = (

            result.content_age_days /

            max(result.max_age_days, 1)
        )

        result.decay_probability = round(
            min(age_ratio * 100, 100),
            2,
        )

        # =====================================================
        # DECAY RISK
        # =====================================================

        if result.decay_probability >= 80:

            result.decay_risk = "critical"

        elif result.decay_probability >= 60:

            result.decay_risk = "high"

        elif result.decay_probability >= 35:

            result.decay_risk = "medium"

        else:

            result.decay_risk = "low"

        # =====================================================
        # PREDICTION
        # =====================================================

        result.predicted_decay_days = max(

            result.max_age_days -

            result.content_age_days,

            0,
        )

    # =========================================================
    # SCORE
    # =========================================================

    def _calculate_freshness_score(
        self,
        result: FreshnessEvaluationResult,
    ) -> None:

        score = 100

        score -= result.decay_probability * 0.5

        if result.outdated_information_detected:
            score -= 20

        if result.real_time_topic:
            score -= 10

        if result.freshness_pressure_score >= 80:
            score -= 10

        result.freshness_score = round(
            max(score, 0),
            2,
        )

        result.freshness_confidence = round(
            result.freshness_score,
            2,
        )

    # =========================================================
    # UPDATE
    # =========================================================

    def _evaluate_update_requirements(
        self,
        result: FreshnessEvaluationResult,
    ) -> None:

        # =====================================================
        # UPDATE REQUIRED
        # =====================================================

        if (

            result.content_age_days
            > result.max_age_days

            or

            result.outdated_information_detected

            or

            result.decay_risk in [
                "high",
                "critical",
            ]
        ):

            result.update_required = True

            result.reverification_required = True

            result.freshness_valid = False

            result.add_warning(
                "Content freshness expired"
            )

        # =====================================================
        # ACTIONS
        # =====================================================

        if result.update_required:

            result.add_action(
                "Refresh outdated sections"
            )

            result.add_action(
                "Re-verify claims and sources"
            )

        if result.real_time_topic:

            result.add_action(
                "Enable rapid update monitoring"
            )

        if (
            result.freshness_competition
            == "very_high"
        ):

            result.add_action(
                "Increase update frequency"
            )

        # =====================================================
        # RANKING DECAY
        # =====================================================

        if result.decay_risk in [
            "high",
            "critical",
        ]:

            result.ranking_decay_risk = "high"

            result.traffic_decay_risk = "high"

            result.add_recommendation(
                "Update metadata and publication date"
            )

    # =========================================================
    # EXPORT
    # =========================================================

    def export(
        self,
        result: FreshnessEvaluationResult,
    ) -> Dict[str, Any]:

        return {

            "freshness_score": (
                result.freshness_score
            ),

            "freshness_confidence": (
                result.freshness_confidence
            ),

            "decay_probability": (
                result.decay_probability
            ),

            "freshness_valid": (
                result.freshness_valid
            ),

            "freshness_required": (
                result.freshness_required
            ),

            "update_required": (
                result.update_required
            ),

            "reverification_required": (
                result.reverification_required
            ),

            "content_age_days": (
                result.content_age_days
            ),

            "max_age_days": (
                result.max_age_days
            ),

            "decay_risk": (
                result.decay_risk
            ),

            "predicted_decay_days": (
                result.predicted_decay_days
            ),

            "traffic_decay_risk": (
                result.traffic_decay_risk
            ),

            "ranking_decay_risk": (
                result.ranking_decay_risk
            ),

            "freshness_sensitive_topic": (
                result.freshness_sensitive_topic
            ),

            "real_time_topic": (
                result.real_time_topic
            ),

            "outdated_information_detected": (
                result.outdated_information_detected
            ),

            "outdated_dates_detected": (
                result.outdated_dates_detected
            ),

            "outdated_statistics_detected": (
                result.outdated_statistics_detected
            ),

            "outdated_links_detected": (
                result.outdated_links_detected
            ),

            "freshness_competition": (
                result.freshness_competition
            ),

            "freshness_pressure_score": (
                result.freshness_pressure_score
            ),

            "update_priority": (
                result.update_priority
            ),

            "update_deadline_hours": (
                result.update_deadline_hours
            ),

            "recommended_actions": (
                result.recommended_actions
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

            "freshness_signals": (
                result.freshness_signals
            ),

            "metadata": (
                result.metadata
            ),
        }