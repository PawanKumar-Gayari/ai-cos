"""
Confidence Logs

Purpose:
Track every confidence decision made by the
editorial intelligence system.

Tracks:
- confidence scores
- publish/review/rewrite decisions
- risk levels
- reasoning trails
- confidence evolution
- confidence accuracy

Goal:
Create explainable confidence intelligence.

This becomes the confidence observability layer
of AI_COS.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Any, List


# =============================================================
# CONFIDENCE LOG ENTRY
# =============================================================

@dataclass
class ConfidenceLogEntry:

    # =========================================================
    # ARTICLE
    # =========================================================

    article_id: str

    keyword: str

    niche: str

    # =========================================================
    # CONFIDENCE
    # =========================================================

    confidence_score: float = 0.0

    confidence_level: str = "medium"

    publish_confidence: float = 0.0

    # =========================================================
    # DECISION
    # =========================================================

    decision: str = "review"

    publishing_allowed: bool = False

    human_review_required: bool = False

    rewrite_required: bool = False

    # =========================================================
    # RISK
    # =========================================================

    risk_level: str = "medium"

    hallucination_risk: str = "low"

    freshness_risk: str = "low"

    authority_risk: str = "low"

    # =========================================================
    # COMPONENT SCORES
    # =========================================================

    seo_score: float = 0.0

    quality_score: float = 0.0

    verification_score: float = 0.0

    freshness_score: float = 0.0

    authority_score: float = 0.0

    prediction_score: float = 0.0

    # =========================================================
    # OUTCOME
    # =========================================================

    ranking_success: bool = False

    ranking_position: int = 100

    traffic_success: bool = False

    verification_success: bool = False

    # =========================================================
    # EXPLAINABILITY
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

    confidence_signals: Dict[str, Any] = field(
        default_factory=dict
    )

    # =========================================================
    # CALIBRATION
    # =========================================================

    prediction_accuracy: float = 0.0

    confidence_accuracy: float = 0.0

    false_positive_detected: bool = False

    false_negative_detected: bool = False

    # =========================================================
    # TIMESTAMP
    # =========================================================

    created_at: datetime = field(
        default_factory=datetime.utcnow
    )

    updated_at: datetime = field(
        default_factory=datetime.utcnow
    )

    # =========================================================
    # META
    # =========================================================

    metadata: Dict[str, Any] = field(
        default_factory=dict
    )


# =============================================================
# CONFIDENCE LOGS
# =============================================================

class ConfidenceLogs:

    """
    Confidence observability system.
    """

    def __init__(
        self,
    ) -> None:

        self.logs: List[
            ConfidenceLogEntry
        ] = []

    # =========================================================
    # STORE
    # =========================================================

    def store(
        self,
        entry: ConfidenceLogEntry,
    ) -> None:

        self.logs.append(entry)

    # =========================================================
    # ALL LOGS
    # =========================================================

    def all_logs(
        self,
    ) -> List[ConfidenceLogEntry]:

        return self.logs

    # =========================================================
    # PUBLISH LOGS
    # =========================================================

    def publish_logs(
        self,
    ) -> List[ConfidenceLogEntry]:

        return [

            log

            for log in self.logs

            if log.decision == "publish"
        ]

    # =========================================================
    # REVIEW LOGS
    # =========================================================

    def review_logs(
        self,
    ) -> List[ConfidenceLogEntry]:

        return [

            log

            for log in self.logs

            if log.decision == "review"
        ]

    # =========================================================
    # REWRITE LOGS
    # =========================================================

    def rewrite_logs(
        self,
    ) -> List[ConfidenceLogEntry]:

        return [

            log

            for log in self.logs

            if log.decision == "rewrite"
        ]

    # =========================================================
    # REJECT LOGS
    # =========================================================

    def reject_logs(
        self,
    ) -> List[ConfidenceLogEntry]:

        return [

            log

            for log in self.logs

            if log.decision == "reject"
        ]

    # =========================================================
    # HIGH RISK
    # =========================================================

    def high_risk_logs(
        self,
    ) -> List[ConfidenceLogEntry]:

        return [

            log

            for log in self.logs

            if log.risk_level in [
                "high",
                "critical",
            ]
        ]

    # =========================================================
    # LOW CONFIDENCE
    # =========================================================

    def low_confidence_logs(
        self,
    ) -> List[ConfidenceLogEntry]:

        return [

            log

            for log in self.logs

            if log.confidence_score < 50
        ]

    # =========================================================
    # UPDATE OUTCOME
    # =========================================================

    def update_outcome(
        self,
        article_id: str,
        ranking_position: int = 100,
        ranking_success: bool = False,
        traffic_success: bool = False,
        verification_success: bool = False,
    ) -> bool:

        for log in self.logs:

            if log.article_id == article_id:

                log.ranking_position = (
                    ranking_position
                )

                log.ranking_success = (
                    ranking_success
                )

                log.traffic_success = (
                    traffic_success
                )

                log.verification_success = (
                    verification_success
                )

                # =============================================
                # CALIBRATION
                # =============================================

                self._evaluate_accuracy(
                    log
                )

                log.updated_at = (
                    datetime.utcnow()
                )

                return True

        return False

    # =========================================================
    # ACCURACY
    # =========================================================

    def _evaluate_accuracy(
        self,
        log: ConfidenceLogEntry,
    ) -> None:

        # =====================================================
        # HIGH CONFIDENCE FAILURE
        # =====================================================

        if (

            log.confidence_score >= 80

            and

            not log.ranking_success
        ):

            log.false_positive_detected = (
                True
            )

        # =====================================================
        # LOW CONFIDENCE SUCCESS
        # =====================================================

        if (

            log.confidence_score < 50

            and

            log.ranking_success
        ):

            log.false_negative_detected = (
                True
            )

        # =====================================================
        # CONFIDENCE ACCURACY
        # =====================================================

        if log.ranking_success:

            log.confidence_accuracy = round(

                log.confidence_score,

                2,
            )

        else:

            log.confidence_accuracy = round(

                100 - log.confidence_score,

                2,
            )

    # =========================================================
    # DECISION COUNTS
    # =========================================================

    def decision_counts(
        self,
    ) -> Dict[str, int]:

        return {

            "publish": len(
                self.publish_logs()
            ),

            "review": len(
                self.review_logs()
            ),

            "rewrite": len(
                self.rewrite_logs()
            ),

            "reject": len(
                self.reject_logs()
            ),
        }

    # =========================================================
    # SUCCESS RATE
    # =========================================================

    def publish_success_rate(
        self,
    ) -> float:

        published = self.publish_logs()

        if not published:
            return 0.0

        successful = len([

            log

            for log in published

            if log.ranking_success
        ])

        return round(

            (
                successful /
                len(published)
            ) * 100,

            2,
        )

    # =========================================================
    # FALSE POSITIVE RATE
    # =========================================================

    def false_positive_rate(
        self,
    ) -> float:

        if not self.logs:
            return 0.0

        false_positives = len([

            log

            for log in self.logs

            if log.false_positive_detected
        ])

        return round(

            (
                false_positives /
                len(self.logs)
            ) * 100,

            2,
        )

    # =========================================================
    # FALSE NEGATIVE RATE
    # =========================================================

    def false_negative_rate(
        self,
    ) -> float:

        if not self.logs:
            return 0.0

        false_negatives = len([

            log

            for log in self.logs

            if log.false_negative_detected
        ])

        return round(

            (
                false_negatives /
                len(self.logs)
            ) * 100,

            2,
        )

    # =========================================================
    # AVERAGE CONFIDENCE
    # =========================================================

    def average_confidence(
        self,
    ) -> float:

        if not self.logs:
            return 0.0

        return round(

            (
                sum(

                    log.confidence_score

                    for log in self.logs
                ) /

                len(self.logs)
            ),

            2,
        )

    # =========================================================
    # EXPORT
    # =========================================================

    def export_metrics(
        self,
    ) -> Dict[str, Any]:

        return {

            "total_logs": (
                len(self.logs)
            ),

            "decision_counts": (
                self.decision_counts()
            ),

            "publish_success_rate": (
                self.publish_success_rate()
            ),

            "false_positive_rate": (
                self.false_positive_rate()
            ),

            "false_negative_rate": (
                self.false_negative_rate()
            ),

            "average_confidence": (
                self.average_confidence()
            ),

            "high_risk_logs": (
                len(
                    self.high_risk_logs()
                )
            ),

            "low_confidence_logs": (
                len(
                    self.low_confidence_logs()
                )
            ),
        }