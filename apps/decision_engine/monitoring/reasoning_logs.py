"""
Reasoning Logs

Purpose:
Store explainable reasoning trails behind
every AI_COS decision.

Tracks:
- why decisions happened
- why articles were published
- why rewrites occurred
- why risks were detected
- why confidence changed
- why rankings were predicted

Goal:
Create enterprise-grade explainability,
traceability, and auditability.

This becomes the explainability engine
of AI_COS.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Any, List


# =============================================================
# REASONING ENTRY
# =============================================================

@dataclass
class ReasoningLogEntry:

    # =========================================================
    # ARTICLE
    # =========================================================

    article_id: str

    keyword: str

    niche: str

    workflow_id: str = ""

    # =========================================================
    # DECISION
    # =========================================================

    decision: str = "review"

    confidence_score: float = 0.0

    risk_level: str = "medium"

    # =========================================================
    # REASONING LAYERS
    # =========================================================

    scoring_reasoning: List[str] = field(
        default_factory=list
    )

    verification_reasoning: List[str] = field(
        default_factory=list
    )

    freshness_reasoning: List[str] = field(
        default_factory=list
    )

    authority_reasoning: List[str] = field(
        default_factory=list
    )

    ranking_reasoning: List[str] = field(
        default_factory=list
    )

    strategy_reasoning: List[str] = field(
        default_factory=list
    )

    # =========================================================
    # FINAL EXPLANATION
    # =========================================================

    final_reasoning: List[str] = field(
        default_factory=list
    )

    warnings: List[str] = field(
        default_factory=list
    )

    recommendations: List[str] = field(
        default_factory=list
    )

    # =========================================================
    # DECISION FACTORS
    # =========================================================

    positive_factors: List[str] = field(
        default_factory=list
    )

    negative_factors: List[str] = field(
        default_factory=list
    )

    critical_factors: List[str] = field(
        default_factory=list
    )

    # =========================================================
    # COMPONENT SCORES
    # =========================================================

    seo_score: float = 0.0

    quality_score: float = 0.0

    freshness_score: float = 0.0

    authority_score: float = 0.0

    verification_score: float = 0.0

    prediction_score: float = 0.0

    # =========================================================
    # RISKS
    # =========================================================

    hallucination_risk: str = "low"

    freshness_risk: str = "low"

    authority_risk: str = "low"

    spam_risk: str = "low"

    # =========================================================
    # EXPLAINABILITY
    # =========================================================

    explainability_score: float = 0.0

    traceability_enabled: bool = True

    audit_ready: bool = True

    # =========================================================
    # SIGNALS
    # =========================================================

    reasoning_signals: Dict[str, Any] = field(
        default_factory=dict
    )

    # =========================================================
    # EVENTS
    # =========================================================

    triggering_events: List[str] = field(
        default_factory=list
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

    # =========================================================
    # UTILITIES
    # =========================================================

    def add_reasoning(
        self,
        category: str,
        message: str,
    ) -> None:

        if not message:
            return

        mapping = {

            "scoring": (
                self.scoring_reasoning
            ),

            "verification": (
                self.verification_reasoning
            ),

            "freshness": (
                self.freshness_reasoning
            ),

            "authority": (
                self.authority_reasoning
            ),

            "ranking": (
                self.ranking_reasoning
            ),

            "strategy": (
                self.strategy_reasoning
            ),

            "final": (
                self.final_reasoning
            ),
        }

        target = mapping.get(category)

        if (
            target is not None
            and message not in target
        ):

            target.append(message)

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

    def add_positive_factor(
        self,
        factor: str,
    ) -> None:

        if (
            factor
            and factor
            not in self.positive_factors
        ):

            self.positive_factors.append(
                factor
            )

    def add_negative_factor(
        self,
        factor: str,
    ) -> None:

        if (
            factor
            and factor
            not in self.negative_factors
        ):

            self.negative_factors.append(
                factor
            )

    def add_critical_factor(
        self,
        factor: str,
    ) -> None:

        if (
            factor
            and factor
            not in self.critical_factors
        ):

            self.critical_factors.append(
                factor
            )

    def add_event(
        self,
        event: str,
    ) -> None:

        if (
            event
            and event
            not in self.triggering_events
        ):

            self.triggering_events.append(
                event
            )


# =============================================================
# REASONING LOGS
# =============================================================

class ReasoningLogs:

    """
    Explainability and auditability engine.
    """

    def __init__(
        self,
    ) -> None:

        self.logs: List[
            ReasoningLogEntry
        ] = []

    # =========================================================
    # STORE
    # =========================================================

    def store(
        self,
        entry: ReasoningLogEntry,
    ) -> None:

        self._calculate_explainability(
            entry
        )

        self.logs.append(entry)

    # =========================================================
    # EXPLAINABILITY
    # =========================================================

    def _calculate_explainability(
        self,
        entry: ReasoningLogEntry,
    ) -> None:

        total_reasoning = (

            len(entry.scoring_reasoning) +

            len(entry.verification_reasoning) +

            len(entry.freshness_reasoning) +

            len(entry.authority_reasoning) +

            len(entry.ranking_reasoning) +

            len(entry.strategy_reasoning) +

            len(entry.final_reasoning)
        )

        score = min(
            total_reasoning * 10,
            100,
        )

        entry.explainability_score = round(
            score,
            2,
        )

    # =========================================================
    # ALL LOGS
    # =========================================================

    def all_logs(
        self,
    ) -> List[ReasoningLogEntry]:

        return self.logs

    # =========================================================
    # PUBLISH LOGS
    # =========================================================

    def publish_logs(
        self,
    ) -> List[ReasoningLogEntry]:

        return [

            log

            for log in self.logs

            if log.decision == "publish"
        ]

    # =========================================================
    # HIGH RISK LOGS
    # =========================================================

    def high_risk_logs(
        self,
    ) -> List[ReasoningLogEntry]:

        return [

            log

            for log in self.logs

            if log.risk_level in [
                "high",
                "critical",
            ]
        ]

    # =========================================================
    # HALLUCINATION LOGS
    # =========================================================

    def hallucination_risk_logs(
        self,
    ) -> List[ReasoningLogEntry]:

        return [

            log

            for log in self.logs

            if log.hallucination_risk
            == "high"
        ]

    # =========================================================
    # LOW EXPLAINABILITY
    # =========================================================

    def low_explainability_logs(
        self,
    ) -> List[ReasoningLogEntry]:

        return [

            log

            for log in self.logs

            if log.explainability_score < 50
        ]

    # =========================================================
    # TRACE ARTICLE
    # =========================================================

    def trace_article(
        self,
        article_id: str,
    ) -> List[ReasoningLogEntry]:

        return [

            log

            for log in self.logs

            if log.article_id == article_id
        ]

    # =========================================================
    # EXPORT TRACE
    # =========================================================

    def export_trace(
        self,
        article_id: str,
    ) -> Dict[str, Any]:

        traces = self.trace_article(
            article_id
        )

        return {

            "article_id": article_id,

            "trace_count": (
                len(traces)
            ),

            "traces": [

                {
                    "decision": (
                        trace.decision
                    ),

                    "confidence_score": (
                        trace.confidence_score
                    ),

                    "risk_level": (
                        trace.risk_level
                    ),

                    "final_reasoning": (
                        trace.final_reasoning
                    ),

                    "warnings": (
                        trace.warnings
                    ),

                    "recommendations": (
                        trace.recommendations
                    ),

                    "events": (
                        trace.triggering_events
                    ),

                    "created_at": (
                        trace.created_at.isoformat()
                    ),
                }

                for trace in traces
            ],
        }

    # =========================================================
    # REASONING STATISTICS
    # =========================================================

    def average_explainability(
        self,
    ) -> float:

        if not self.logs:
            return 0.0

        return round(

            (
                sum(

                    log.explainability_score

                    for log in self.logs
                ) /

                len(self.logs)
            ),

            2,
        )

    # =========================================================
    # AUDIT READY RATE
    # =========================================================

    def audit_ready_rate(
        self,
    ) -> float:

        if not self.logs:
            return 0.0

        audit_ready = len([

            log

            for log in self.logs

            if log.audit_ready
        ])

        return round(

            (
                audit_ready /
                len(self.logs)
            ) * 100,

            2,
        )

    # =========================================================
    # TRACEABILITY RATE
    # =========================================================

    def traceability_rate(
        self,
    ) -> float:

        if not self.logs:
            return 0.0

        traceable = len([

            log

            for log in self.logs

            if log.traceability_enabled
        ])

        return round(

            (
                traceable /
                len(self.logs)
            ) * 100,

            2,
        )

    # =========================================================
    # EXPORT METRICS
    # =========================================================

    def export_metrics(
        self,
    ) -> Dict[str, Any]:

        return {

            "total_logs": (
                len(self.logs)
            ),

            "publish_logs": (
                len(
                    self.publish_logs()
                )
            ),

            "high_risk_logs": (
                len(
                    self.high_risk_logs()
                )
            ),

            "hallucination_risk_logs": (
                len(
                    self.hallucination_risk_logs()
                )
            ),

            "low_explainability_logs": (
                len(
                    self.low_explainability_logs()
                )
            ),

            "average_explainability": (
                self.average_explainability()
            ),

            "audit_ready_rate": (
                self.audit_ready_rate()
            ),

            "traceability_rate": (
                self.traceability_rate()
            ),
        }