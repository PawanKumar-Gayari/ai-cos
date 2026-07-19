"""
Decision Metrics

Purpose:
Measure decision engine intelligence accuracy.

Tracks:
- decision quality
- prediction accuracy
- publish success rate
- rewrite effectiveness
- verification accuracy
- ranking prediction accuracy
- freshness prediction accuracy

Goal:
Continuously improve AI_COS intelligence.

This becomes the central evaluation layer
for adaptive learning.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Any, List


# =============================================================
# METRIC ENTRY
# =============================================================

@dataclass
class DecisionMetricEntry:

    # =========================================================
    # ARTICLE
    # =========================================================

    article_id: str

    keyword: str

    niche: str

    # =========================================================
    # DECISION
    # =========================================================

    decision: str

    confidence_score: float = 0.0

    predicted_position: int = 100

    actual_position: int = 100

    # =========================================================
    # PREDICTION
    # =========================================================

    ranking_prediction_accuracy: float = 0.0

    traffic_prediction_accuracy: float = 0.0

    freshness_prediction_accuracy: float = 0.0

    verification_prediction_accuracy: float = 0.0

    # =========================================================
    # RESULTS
    # =========================================================

    publish_success: bool = False

    ranking_success: bool = False

    traffic_success: bool = False

    verification_success: bool = False

    freshness_success: bool = False

    # =========================================================
    # ERRORS
    # =========================================================

    false_positive: bool = False

    false_negative: bool = False

    hallucination_detected: bool = False

    freshness_failure_detected: bool = False

    # =========================================================
    # SCORES
    # =========================================================

    seo_score: float = 0.0

    quality_score: float = 0.0

    freshness_score: float = 0.0

    authority_score: float = 0.0

    verification_score: float = 0.0

    # =========================================================
    # LEARNING
    # =========================================================

    learning_signals: Dict[str, Any] = field(
        default_factory=dict
    )

    # =========================================================
    # TIMESTAMPS
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
# DECISION METRICS
# =============================================================

class DecisionMetrics:

    """
    Central decision evaluation system.
    """

    def __init__(
        self,
    ) -> None:

        self.metrics: List[
            DecisionMetricEntry
        ] = []

    # =========================================================
    # STORE
    # =========================================================

    def store(
        self,
        entry: DecisionMetricEntry,
    ) -> None:

        self.metrics.append(entry)

    # =========================================================
    # UPDATE RESULTS
    # =========================================================

    def update_results(
        self,
        article_id: str,
        actual_position: int = 100,
        publish_success: bool = False,
        ranking_success: bool = False,
        traffic_success: bool = False,
        verification_success: bool = False,
        freshness_success: bool = False,
    ) -> bool:

        for entry in self.metrics:

            if entry.article_id == article_id:

                entry.actual_position = (
                    actual_position
                )

                entry.publish_success = (
                    publish_success
                )

                entry.ranking_success = (
                    ranking_success
                )

                entry.traffic_success = (
                    traffic_success
                )

                entry.verification_success = (
                    verification_success
                )

                entry.freshness_success = (
                    freshness_success
                )

                # =============================================
                # ACCURACY
                # =============================================

                self._calculate_prediction_accuracy(
                    entry
                )

                self._detect_failures(
                    entry
                )

                entry.updated_at = (
                    datetime.utcnow()
                )

                return True

        return False

    # =========================================================
    # ACCURACY
    # =========================================================

    def _calculate_prediction_accuracy(
        self,
        entry: DecisionMetricEntry,
    ) -> None:

        # =====================================================
        # RANKING
        # =====================================================

        difference = abs(

            entry.predicted_position -

            entry.actual_position
        )

        ranking_accuracy = max(

            100 - (difference * 5),

            0,
        )

        entry.ranking_prediction_accuracy = (
            round(
                ranking_accuracy,
                2,
            )
        )

        # =====================================================
        # VERIFICATION
        # =====================================================

        if entry.verification_success:

            entry.verification_prediction_accuracy = (
                entry.verification_score
            )

        else:

            entry.verification_prediction_accuracy = (
                max(
                    100 - entry.verification_score,
                    0,
                )
            )

        # =====================================================
        # FRESHNESS
        # =====================================================

        if entry.freshness_success:

            entry.freshness_prediction_accuracy = (
                entry.freshness_score
            )

        else:

            entry.freshness_prediction_accuracy = (
                max(
                    100 - entry.freshness_score,
                    0,
                )
            )

        # =====================================================
        # TRAFFIC
        # =====================================================

        if entry.traffic_success:

            entry.traffic_prediction_accuracy = (
                90.0
            )

        else:

            entry.traffic_prediction_accuracy = (
                40.0
            )

    # =========================================================
    # FAILURE DETECTION
    # =========================================================

    def _detect_failures(
        self,
        entry: DecisionMetricEntry,
    ) -> None:

        # =====================================================
        # FALSE POSITIVE
        # =====================================================

        if (

            entry.confidence_score >= 80

            and

            not entry.publish_success
        ):

            entry.false_positive = True

        # =====================================================
        # FALSE NEGATIVE
        # =====================================================

        if (

            entry.confidence_score < 50

            and

            entry.publish_success
        ):

            entry.false_negative = True

        # =====================================================
        # HALLUCINATION
        # =====================================================

        if (

            entry.verification_score >= 80

            and

            not entry.verification_success
        ):

            entry.hallucination_detected = (
                True
            )

        # =====================================================
        # FRESHNESS FAILURE
        # =====================================================

        if (

            entry.freshness_score >= 80

            and

            not entry.freshness_success
        ):

            entry.freshness_failure_detected = (
                True
            )

    # =========================================================
    # ALL METRICS
    # =========================================================

    def all_metrics(
        self,
    ) -> List[DecisionMetricEntry]:

        return self.metrics

    # =========================================================
    # PUBLISH SUCCESS
    # =========================================================

    def publish_success_rate(
        self,
    ) -> float:

        if not self.metrics:
            return 0.0

        successful = len([

            entry

            for entry in self.metrics

            if entry.publish_success
        ])

        return round(

            (
                successful /
                len(self.metrics)
            ) * 100,

            2,
        )

    # =========================================================
    # RANKING ACCURACY
    # =========================================================

    def average_ranking_accuracy(
        self,
    ) -> float:

        if not self.metrics:
            return 0.0

        return round(

            (
                sum(

                    entry.ranking_prediction_accuracy

                    for entry in self.metrics
                ) /

                len(self.metrics)
            ),

            2,
        )

    # =========================================================
    # VERIFICATION ACCURACY
    # =========================================================

    def verification_accuracy(
        self,
    ) -> float:

        if not self.metrics:
            return 0.0

        return round(

            (
                sum(

                    entry.verification_prediction_accuracy

                    for entry in self.metrics
                ) /

                len(self.metrics)
            ),

            2,
        )

    # =========================================================
    # FRESHNESS ACCURACY
    # =========================================================

    def freshness_accuracy(
        self,
    ) -> float:

        if not self.metrics:
            return 0.0

        return round(

            (
                sum(

                    entry.freshness_prediction_accuracy

                    for entry in self.metrics
                ) /

                len(self.metrics)
            ),

            2,
        )

    # =========================================================
    # FALSE POSITIVE RATE
    # =========================================================

    def false_positive_rate(
        self,
    ) -> float:

        if not self.metrics:
            return 0.0

        false_positives = len([

            entry

            for entry in self.metrics

            if entry.false_positive
        ])

        return round(

            (
                false_positives /
                len(self.metrics)
            ) * 100,

            2,
        )

    # =========================================================
    # FALSE NEGATIVE RATE
    # =========================================================

    def false_negative_rate(
        self,
    ) -> float:

        if not self.metrics:
            return 0.0

        false_negatives = len([

            entry

            for entry in self.metrics

            if entry.false_negative
        ])

        return round(

            (
                false_negatives /
                len(self.metrics)
            ) * 100,

            2,
        )

    # =========================================================
    # HALLUCINATION RATE
    # =========================================================

    def hallucination_rate(
        self,
    ) -> float:

        if not self.metrics:
            return 0.0

        hallucinations = len([

            entry

            for entry in self.metrics

            if entry.hallucination_detected
        ])

        return round(

            (
                hallucinations /
                len(self.metrics)
            ) * 100,

            2,
        )

    # =========================================================
    # TOP PERFORMERS
    # =========================================================

    def top_performing_entries(
        self,
        limit: int = 10,
    ) -> List[DecisionMetricEntry]:

        return sorted(

            self.metrics,

            key=lambda entry: (
                entry.ranking_prediction_accuracy
            ),

            reverse=True,
        )[:limit]

    # =========================================================
    # EXPORT
    # =========================================================

    def export_metrics(
        self,
    ) -> Dict[str, Any]:

        return {

            "total_entries": (
                len(self.metrics)
            ),

            "publish_success_rate": (
                self.publish_success_rate()
            ),

            "average_ranking_accuracy": (
                self.average_ranking_accuracy()
            ),

            "verification_accuracy": (
                self.verification_accuracy()
            ),

            "freshness_accuracy": (
                self.freshness_accuracy()
            ),

            "false_positive_rate": (
                self.false_positive_rate()
            ),

            "false_negative_rate": (
                self.false_negative_rate()
            ),

            "hallucination_rate": (
                self.hallucination_rate()
            ),

            "top_performing_entries": [

                {
                    "article_id": (
                        entry.article_id
                    ),

                    "keyword": (
                        entry.keyword
                    ),

                    "ranking_accuracy": (
                        entry.ranking_prediction_accuracy
                    ),

                    "predicted_position": (
                        entry.predicted_position
                    ),

                    "actual_position": (
                        entry.actual_position
                    ),
                }

                for entry in self.top_performing_entries()
            ],
        }