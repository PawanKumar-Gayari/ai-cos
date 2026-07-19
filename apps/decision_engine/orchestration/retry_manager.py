"""
Retry Manager

Purpose:
Handle intelligent retries for failed workflows,
failed engines, failed verification, and unstable
AI operations.

Handles:
- retry strategies
- exponential backoff
- retry classification
- failure recovery
- fallback execution
- adaptive retries

Goal:
Create resilient autonomous intelligence.

This becomes the resilience engine
of AI_COS.
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional


# =============================================================
# RETRY ENTRY
# =============================================================

@dataclass
class RetryEntry:

    # =========================================================
    # CORE
    # =========================================================

    retry_id: str

    workflow_id: str

    node_id: str

    engine: str

    # =========================================================
    # FAILURE
    # =========================================================

    failure_type: str

    error_message: str

    recoverable: bool = True

    # =========================================================
    # RETRIES
    # =========================================================

    retry_count: int = 0

    max_retries: int = 3

    retry_allowed: bool = True

    retry_successful: bool = False

    # =========================================================
    # STRATEGY
    # =========================================================

    retry_strategy: str = "standard"

    backoff_seconds: int = 5

    fallback_enabled: bool = False

    fallback_engine: Optional[str] = None

    # =========================================================
    # STATUS
    # =========================================================

    completed: bool = False

    failed_permanently: bool = False

    escalated_to_human: bool = False

    # =========================================================
    # EXECUTION
    # =========================================================

    next_retry_at: Optional[datetime] = None

    last_retry_at: Optional[datetime] = None

    # =========================================================
    # SIGNALS
    # =========================================================

    retry_signals: Dict[str, Any] = field(
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
# RETRY MANAGER
# =============================================================

class RetryManager:

    """
    Intelligent retry orchestration engine.
    """

    def __init__(
        self,
    ) -> None:

        self.retries: List[
            RetryEntry
        ] = []

    # =========================================================
    # REGISTER FAILURE
    # =========================================================

    def register_failure(
        self,
        workflow_id: str,
        node_id: str,
        engine: str,
        failure_type: str,
        error_message: str,
    ) -> RetryEntry:

        retry = RetryEntry(

            retry_id=(
                f"retry_{datetime.utcnow().timestamp()}"
            ),

            workflow_id=workflow_id,

            node_id=node_id,

            engine=engine,

            failure_type=failure_type,

            error_message=error_message,
        )

        # =====================================================
        # STRATEGY
        # =====================================================

        self._assign_strategy(
            retry
        )

        self.retries.append(
            retry
        )

        return retry

    # =========================================================
    # STRATEGY
    # =========================================================

    def _assign_strategy(
        self,
        retry: RetryEntry,
    ) -> None:

        failure = retry.failure_type.lower()

        # =====================================================
        # NETWORK
        # =====================================================

        if failure in [
            "timeout",
            "network",
            "rate_limit",
        ]:

            retry.retry_strategy = (
                "exponential_backoff"
            )

            retry.backoff_seconds = 10

            retry.max_retries = 5

            retry.add_reasoning(
                "Network instability retry strategy selected"
            )

        # =====================================================
        # VERIFICATION
        # =====================================================

        elif failure in [
            "verification_failed",
            "hallucination",
        ]:

            retry.retry_strategy = (
                "verification_retry"
            )

            retry.max_retries = 2

            retry.fallback_enabled = True

            retry.fallback_engine = (
                "official_source_engine"
            )

            retry.add_reasoning(
                "Verification fallback strategy enabled"
            )

        # =====================================================
        # GENERATION
        # =====================================================

        elif failure in [
            "generation_failed",
            "llm_error",
        ]:

            retry.retry_strategy = (
                "regeneration"
            )

            retry.max_retries = 3

            retry.fallback_enabled = True

            retry.fallback_engine = (
                "backup_llm_engine"
            )

            retry.add_reasoning(
                "LLM regeneration strategy enabled"
            )

        # =====================================================
        # CRITICAL
        # =====================================================

        elif failure in [
            "critical_failure",
            "data_corruption",
        ]:

            retry.retry_allowed = False

            retry.escalated_to_human = (
                True
            )

            retry.add_warning(
                "Critical failure escalated to human review"
            )

        # =====================================================
        # DEFAULT
        # =====================================================

        else:

            retry.retry_strategy = (
                "standard"
            )

            retry.max_retries = 3

            retry.backoff_seconds = 5

            retry.add_reasoning(
                "Standard retry strategy selected"
            )

    # =========================================================
    # CAN RETRY
    # =========================================================

    def can_retry(
        self,
        retry: RetryEntry,
    ) -> bool:

        if not retry.retry_allowed:
            return False

        if retry.failed_permanently:
            return False

        if retry.retry_count >= retry.max_retries:

            retry.failed_permanently = (
                True
            )

            retry.add_warning(
                "Maximum retries exceeded"
            )

            return False

        return True

    # =========================================================
    # EXECUTE RETRY
    # =========================================================

    def execute_retry(
        self,
        retry_id: str,
    ) -> bool:

        retry = self.find_retry(
            retry_id
        )

        if not retry:
            return False

        if not self.can_retry(retry):
            return False

        # =====================================================
        # RETRY
        # =====================================================

        retry.retry_count += 1

        retry.last_retry_at = (
            datetime.utcnow()
        )

        retry.next_retry_at = (

            datetime.utcnow() +

            timedelta(
                seconds=(
                    retry.backoff_seconds *
                    retry.retry_count
                )
            )
        )

        retry.updated_at = (
            datetime.utcnow()
        )

        retry.add_reasoning(
            f"Retry attempt #{retry.retry_count}"
        )

        return True

    # =========================================================
    # MARK SUCCESS
    # =========================================================

    def mark_success(
        self,
        retry_id: str,
    ) -> bool:

        retry = self.find_retry(
            retry_id
        )

        if not retry:
            return False

        retry.retry_successful = (
            True
        )

        retry.completed = (
            True
        )

        retry.updated_at = (
            datetime.utcnow()
        )

        retry.add_reasoning(
            "Retry recovered successfully"
        )

        return True

    # =========================================================
    # MARK FAILURE
    # =========================================================

    def mark_failure(
        self,
        retry_id: str,
    ) -> bool:

        retry = self.find_retry(
            retry_id
        )

        if not retry:
            return False

        if retry.retry_count >= retry.max_retries:

            retry.failed_permanently = (
                True
            )

            retry.add_warning(
                "Retry permanently failed"
            )

        retry.updated_at = (
            datetime.utcnow()
        )

        return True

    # =========================================================
    # FIND
    # =========================================================

    def find_retry(
        self,
        retry_id: str,
    ) -> Optional[RetryEntry]:

        for retry in self.retries:

            if retry.retry_id == retry_id:

                return retry

        return None

    # =========================================================
    # FAILED RETRIES
    # =========================================================

    def failed_retries(
        self,
    ) -> List[RetryEntry]:

        return [

            retry

            for retry in self.retries

            if retry.failed_permanently
        ]

    # =========================================================
    # ACTIVE RETRIES
    # =========================================================

    def active_retries(
        self,
    ) -> List[RetryEntry]:

        return [

            retry

            for retry in self.retries

            if (
                not retry.completed
                and not retry.failed_permanently
            )
        ]

    # =========================================================
    # HUMAN ESCALATIONS
    # =========================================================

    def escalated_retries(
        self,
    ) -> List[RetryEntry]:

        return [

            retry

            for retry in self.retries

            if retry.escalated_to_human
        ]

    # =========================================================
    # SUCCESS RATE
    # =========================================================

    def retry_success_rate(
        self,
    ) -> float:

        completed = [

            retry

            for retry in self.retries

            if retry.completed
        ]

        if not completed:
            return 0.0

        successful = len([

            retry

            for retry in completed

            if retry.retry_successful
        ])

        return round(

            (
                successful /
                len(completed)
            ) * 100,

            2,
        )

    # =========================================================
    # FAILURE RATE
    # =========================================================

    def permanent_failure_rate(
        self,
    ) -> float:

        if not self.retries:
            return 0.0

        failed = len(
            self.failed_retries()
        )

        return round(

            (
                failed /
                len(self.retries)
            ) * 100,

            2,
        )

    # =========================================================
    # EXPORT
    # =========================================================

    def export_metrics(
        self,
    ) -> Dict[str, Any]:

        return {

            "total_retries": (
                len(self.retries)
            ),

            "active_retries": (
                len(
                    self.active_retries()
                )
            ),

            "failed_retries": (
                len(
                    self.failed_retries()
                )
            ),

            "escalated_retries": (
                len(
                    self.escalated_retries()
                )
            ),

            "retry_success_rate": (
                self.retry_success_rate()
            ),

            "permanent_failure_rate": (
                self.permanent_failure_rate()
            ),
        }