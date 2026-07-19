"""
Event Dispatcher

Purpose:
Central event-driven orchestration system.

Handles:
- event publishing
- event subscriptions
- workflow triggers
- async orchestration
- monitoring triggers
- adaptive learning triggers

Goal:
Enable event-driven autonomous intelligence.

This becomes the event nervous system
of AI_COS.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Any, List, Callable


# =============================================================
# EVENT
# =============================================================

@dataclass
class Event:

    # =========================================================
    # CORE
    # =========================================================

    event_id: str

    event_type: str

    source: str

    # =========================================================
    # PAYLOAD
    # =========================================================

    payload: Dict[str, Any] = field(
        default_factory=dict
    )

    # =========================================================
    # PRIORITY
    # =========================================================

    priority: str = "medium"

    async_event: bool = False

    # =========================================================
    # STATUS
    # =========================================================

    processed: bool = False

    failed: bool = False

    retry_count: int = 0

    # =========================================================
    # TIMESTAMPS
    # =========================================================

    created_at: datetime = field(
        default_factory=datetime.utcnow
    )

    processed_at: datetime = None

    # =========================================================
    # META
    # =========================================================

    metadata: Dict[str, Any] = field(
        default_factory=dict
    )


# =============================================================
# EVENT DISPATCHER
# =============================================================

class EventDispatcher:

    """
    Central event orchestration system.
    """

    def __init__(
        self,
    ) -> None:

        # =====================================================
        # EVENT STORE
        # =====================================================

        self.events: List[Event] = []

        # =====================================================
        # SUBSCRIBERS
        # =====================================================

        self.subscribers: Dict[
            str,
            List[Callable]
        ] = {}

    # =========================================================
    # SUBSCRIBE
    # =========================================================

    def subscribe(
        self,
        event_type: str,
        handler: Callable,
    ) -> None:

        if (
            event_type
            not in self.subscribers
        ):

            self.subscribers[event_type] = []

        self.subscribers[event_type].append(
            handler
        )

    # =========================================================
    # DISPATCH
    # =========================================================

    def dispatch(
        self,
        event: Event,
    ) -> None:

        self.events.append(event)

        handlers = self.subscribers.get(
            event.event_type,
            [],
        )

        for handler in handlers:

            try:

                handler(event)

            except Exception:

                event.failed = True

                event.retry_count += 1

        event.processed = True

        event.processed_at = (
            datetime.utcnow()
        )

    # =========================================================
    # CREATE EVENT
    # =========================================================

    def create_event(
        self,
        event_id: str,
        event_type: str,
        source: str,
        payload: Dict[str, Any] = None,
        priority: str = "medium",
        async_event: bool = False,
    ) -> Event:

        return Event(

            event_id=event_id,

            event_type=event_type,

            source=source,

            payload=payload or {},

            priority=priority,

            async_event=async_event,
        )

    # =========================================================
    # PUBLISH
    # =========================================================

    def publish(
        self,
        event_type: str,
        source: str,
        payload: Dict[str, Any] = None,
        priority: str = "medium",
        async_event: bool = False,
    ) -> Event:

        event = self.create_event(

            event_id=(
                f"{event_type}_"
                f"{datetime.utcnow().timestamp()}"
            ),

            event_type=event_type,

            source=source,

            payload=payload,

            priority=priority,

            async_event=async_event,
        )

        self.dispatch(event)

        return event

    # =========================================================
    # EVENT TYPES
    # =========================================================

    def article_published(
        self,
        article_id: str,
        payload: Dict[str, Any] = None,
    ) -> Event:

        return self.publish(

            event_type="article_published",

            source="publisher",

            payload={

                "article_id": article_id,

                **(payload or {})
            },

            priority="high",
        )

    # =========================================================
    # VERIFIED
    # =========================================================

    def article_verified(
        self,
        article_id: str,
        payload: Dict[str, Any] = None,
    ) -> Event:

        return self.publish(

            event_type="article_verified",

            source="verifier",

            payload={

                "article_id": article_id,

                **(payload or {})
            },

            priority="high",
        )

    # =========================================================
    # FRESHNESS
    # =========================================================

    def freshness_expired(
        self,
        article_id: str,
        payload: Dict[str, Any] = None,
    ) -> Event:

        return self.publish(

            event_type="freshness_expired",

            source="freshness_monitor",

            payload={

                "article_id": article_id,

                **(payload or {})
            },

            priority="critical",
        )

    # =========================================================
    # RANKING CHANGE
    # =========================================================

    def ranking_changed(
        self,
        article_id: str,
        old_position: int,
        new_position: int,
        payload: Dict[str, Any] = None,
    ) -> Event:

        return self.publish(

            event_type="ranking_changed",

            source="ranking_monitor",

            payload={

                "article_id": article_id,

                "old_position": old_position,

                "new_position": new_position,

                **(payload or {})
            },

            priority="high",
        )

    # =========================================================
    # FEEDBACK
    # =========================================================

    def feedback_received(
        self,
        article_id: str,
        feedback: str,
        payload: Dict[str, Any] = None,
    ) -> Event:

        return self.publish(

            event_type="feedback_received",

            source="feedback_engine",

            payload={

                "article_id": article_id,

                "feedback": feedback,

                **(payload or {})
            },

            priority="medium",
        )

    # =========================================================
    # HALLUCINATION
    # =========================================================

    def hallucination_detected(
        self,
        article_id: str,
        payload: Dict[str, Any] = None,
    ) -> Event:

        return self.publish(

            event_type="hallucination_detected",

            source="verification_engine",

            payload={

                "article_id": article_id,

                **(payload or {})
            },

            priority="critical",
        )

    # =========================================================
    # VERIFICATION FAILURE
    # =========================================================

    def verification_failed(
        self,
        article_id: str,
        payload: Dict[str, Any] = None,
    ) -> Event:

        return self.publish(

            event_type="verification_failed",

            source="verification_engine",

            payload={

                "article_id": article_id,

                **(payload or {})
            },

            priority="critical",
        )

    # =========================================================
    # RETRY
    # =========================================================

    def retry_requested(
        self,
        workflow_id: str,
        payload: Dict[str, Any] = None,
    ) -> Event:

        return self.publish(

            event_type="retry_requested",

            source="retry_manager",

            payload={

                "workflow_id": workflow_id,

                **(payload or {})
            },

            priority="high",
        )

    # =========================================================
    # EVENT FILTERS
    # =========================================================

    def all_events(
        self,
    ) -> List[Event]:

        return self.events

    def failed_events(
        self,
    ) -> List[Event]:

        return [

            event

            for event in self.events

            if event.failed
        ]

    def processed_events(
        self,
    ) -> List[Event]:

        return [

            event

            for event in self.events

            if event.processed
        ]

    def critical_events(
        self,
    ) -> List[Event]:

        return [

            event

            for event in self.events

            if event.priority == "critical"
        ]

    # =========================================================
    # METRICS
    # =========================================================

    def event_counts(
        self,
    ) -> Dict[str, int]:

        counts: Dict[str, int] = {}

        for event in self.events:

            counts[event.event_type] = (

                counts.get(
                    event.event_type,
                    0,
                ) + 1
            )

        return counts

    # =========================================================
    # FAILURE RATE
    # =========================================================

    def failure_rate(
        self,
    ) -> float:

        if not self.events:
            return 0.0

        failures = len(
            self.failed_events()
        )

        return round(

            (
                failures /
                len(self.events)
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

            "total_events": (
                len(self.events)
            ),

            "processed_events": (
                len(
                    self.processed_events()
                )
            ),

            "failed_events": (
                len(
                    self.failed_events()
                )
            ),

            "critical_events": (
                len(
                    self.critical_events()
                )
            ),

            "failure_rate": (
                self.failure_rate()
            ),

            "event_counts": (
                self.event_counts()
            ),

            "registered_event_types": (
                list(
                    self.subscribers.keys()
                )
            ),
        }