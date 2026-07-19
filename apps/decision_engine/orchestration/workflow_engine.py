"""
Workflow Engine

Purpose:
Master orchestration controller for AI_COS.

Controls:
- workflow execution
- orchestration lifecycle
- engine coordination
- adaptive execution
- event-driven intelligence
- monitoring integration
- retry integration
- execution graph lifecycle

Goal:
Create autonomous editorial intelligence.

This becomes the master AI controller
of AI_COS.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Any, List, Optional

from apps.decision_engine.orchestration.execution_graph import (
    ExecutionGraph,
)

from apps.decision_engine.orchestration.decision_router import (
    DecisionRouter,
)

from apps.decision_engine.orchestration.event_dispatcher import (
    EventDispatcher,
)

from apps.decision_engine.orchestration.retry_manager import (
    RetryManager,
)


# =============================================================
# WORKFLOW RESULT
# =============================================================

@dataclass
class WorkflowResult:

    # =========================================================
    # CORE
    # =========================================================

    workflow_id: str

    workflow_name: str

    workflow_type: str

    # =========================================================
    # STATUS
    # =========================================================

    started: bool = False

    completed: bool = False

    failed: bool = False

    partially_completed: bool = False

    # =========================================================
    # EXECUTION
    # =========================================================

    executed_nodes: List[str] = field(
        default_factory=list
    )

    failed_nodes: List[str] = field(
        default_factory=list
    )

    skipped_nodes: List[str] = field(
        default_factory=list
    )

    # =========================================================
    # DECISION
    # =========================================================

    final_decision: str = "review"

    confidence_score: float = 0.0

    publish_allowed: bool = False

    # =========================================================
    # EVENTS
    # =========================================================

    triggered_events: List[str] = field(
        default_factory=list
    )

    # =========================================================
    # RETRIES
    # =========================================================

    retries_triggered: int = 0

    recovery_successful: bool = False

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
    # OUTPUTS
    # =========================================================

    outputs: Dict[str, Any] = field(
        default_factory=dict
    )

    # =========================================================
    # TIMESTAMPS
    # =========================================================

    started_at: Optional[datetime] = None

    completed_at: Optional[datetime] = None

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
# WORKFLOW ENGINE
# =============================================================

class WorkflowEngine:

    """
    Master orchestration controller.
    """

    def __init__(
        self,
    ) -> None:

        # =====================================================
        # ORCHESTRATION
        # =====================================================

        self.router = DecisionRouter()

        self.dispatcher = EventDispatcher()

        self.retry_manager = RetryManager()

        self.execution_graph = ExecutionGraph()

        # =====================================================
        # WORKFLOW HISTORY
        # =====================================================

        self.workflow_history: List[
            WorkflowResult
        ] = []

    # =========================================================
    # EXECUTE WORKFLOW
    # =========================================================

    def execute(
        self,
        topic: str,
        niche: str = "general",
        intent: str = "informational",
        ymyl: bool = False,
        freshness_sensitive: bool = False,
    ) -> WorkflowResult:

        workflow = WorkflowResult(

            workflow_id=(
                f"workflow_"
                f"{datetime.utcnow().timestamp()}"
            ),

            workflow_name="editorial_workflow",

            workflow_type=niche,
        )

        workflow.started = True

        workflow.started_at = (
            datetime.utcnow()
        )

        # =====================================================
        # ROUTING
        # =====================================================

        route = self.router.route(

            topic=topic,

            niche=niche,

            intent=intent,

            ymyl=ymyl,

            freshness_sensitive=(
                freshness_sensitive
            ),
        )

        workflow.add_reasoning(
            f"Workflow routed to: "
            f"{route.workflow}"
        )

        # =====================================================
        # BUILD GRAPH
        # =====================================================

        self.execution_graph = (
            ExecutionGraph()
        )

        self.execution_graph.build_editorial_workflow()

        # =====================================================
        # VALIDATE
        # =====================================================

        if not self.execution_graph.validate_graph():

            workflow.failed = True

            workflow.add_warning(
                "Workflow graph validation failed"
            )

            return workflow

        # =====================================================
        # EXECUTION LOOP
        # =====================================================

        while not (
            self.execution_graph.execution_complete()
        ):

            ready_nodes = (
                self.execution_graph.ready_nodes()
            )

            if not ready_nodes:

                workflow.failed = True

                workflow.add_warning(
                    "Deadlock detected in execution graph"
                )

                break

            for node in ready_nodes:

                success = self._execute_node(
                    workflow,
                    node.node_id,
                )

                if not success:

                    workflow.failed_nodes.append(
                        node.node_id
                    )

                    recovered = (
                        self._attempt_recovery(
                            workflow,
                            node.node_id,
                            node.engine,
                        )
                    )

                    if not recovered:

                        workflow.failed = True

                        workflow.add_warning(
                            f"Node failed permanently: "
                            f"{node.node_id}"
                        )

                else:

                    workflow.executed_nodes.append(
                        node.node_id
                    )

        # =====================================================
        # FINALIZE
        # =====================================================

        self._finalize_workflow(
            workflow,
            route,
        )

        # =====================================================
        # STORE
        # =====================================================

        self.workflow_history.append(
            workflow
        )

        return workflow

    # =========================================================
    # EXECUTE NODE
    # =========================================================

    def _execute_node(
        self,
        workflow: WorkflowResult,
        node_id: str,
    ) -> bool:

        try:

            output = {

                "status": "success",

                "node_id": node_id,

                "executed_at": (
                    datetime.utcnow().isoformat()
                ),
            }

            success = (
                self.execution_graph.execute_node(
                    node_id=node_id,
                    output=output,
                )
            )

            if success:

                workflow.outputs[node_id] = (
                    output
                )

                workflow.add_reasoning(
                    f"Executed node: {node_id}"
                )

            return success

        except Exception as error:

            workflow.add_warning(
                f"Execution failed: {node_id}"
            )

            self.execution_graph.fail_node(
                node_id,
                str(error),
            )

            return False

    # =========================================================
    # RECOVERY
    # =========================================================

    def _attempt_recovery(
        self,
        workflow: WorkflowResult,
        node_id: str,
        engine: str,
    ) -> bool:

        retry = (
            self.retry_manager.register_failure(

                workflow_id=(
                    workflow.workflow_id
                ),

                node_id=node_id,

                engine=engine,

                failure_type="execution_failed",

                error_message=(
                    f"{node_id} execution failure"
                ),
            )
        )

        workflow.retries_triggered += 1

        workflow.triggered_events.append(
            "retry_requested"
        )

        # =====================================================
        # RETRY
        # =====================================================

        allowed = (
            self.retry_manager.execute_retry(
                retry.retry_id
            )
        )

        if not allowed:

            return False

        # =====================================================
        # RETRY EXECUTION
        # =====================================================

        recovered = (
            self.execution_graph.retry_node(
                node_id
            )
        )

        if recovered:

            workflow.recovery_successful = (
                True
            )

            workflow.add_reasoning(
                f"Recovered node: {node_id}"
            )

            self.retry_manager.mark_success(
                retry.retry_id
            )

            return True

        self.retry_manager.mark_failure(
            retry.retry_id
        )

        return False

    # =========================================================
    # FINALIZE
    # =========================================================

    def _finalize_workflow(
        self,
        workflow: WorkflowResult,
        route,
    ) -> None:

        workflow.completed = (
            not workflow.failed
        )

        workflow.completed_at = (
            datetime.utcnow()
        )

        # =====================================================
        # DECISION
        # =====================================================

        if workflow.failed:

            workflow.final_decision = (
                "review"
            )

            workflow.publish_allowed = (
                False
            )

            workflow.confidence_score = (
                40.0
            )

        else:

            workflow.final_decision = (
                "publish"
            )

            workflow.publish_allowed = (
                True
            )

            workflow.confidence_score = (
                85.0
            )

        # =====================================================
        # EVENTS
        # =====================================================

        if workflow.publish_allowed:

            event = (
                self.dispatcher.article_published(

                    article_id=(
                        workflow.workflow_id
                    ),
                )
            )

            workflow.triggered_events.append(
                event.event_type
            )

        # =====================================================
        # RECOMMENDATIONS
        # =====================================================

        if route.freshness_strategy_enabled:

            workflow.add_recommendation(
                "Enable freshness monitoring"
            )

        if route.snippet_strategy_enabled:

            workflow.add_recommendation(
                "Optimize for featured snippets"
            )

        workflow.add_reasoning(
            "Workflow finalized successfully"
        )

    # =========================================================
    # WORKFLOW HISTORY
    # =========================================================

    def workflows(
        self,
    ) -> List[WorkflowResult]:

        return self.workflow_history

    # =========================================================
    # FAILED WORKFLOWS
    # =========================================================

    def failed_workflows(
        self,
    ) -> List[WorkflowResult]:

        return [

            workflow

            for workflow
            in self.workflow_history

            if workflow.failed
        ]

    # =========================================================
    # SUCCESSFUL WORKFLOWS
    # =========================================================

    def successful_workflows(
        self,
    ) -> List[WorkflowResult]:

        return [

            workflow

            for workflow
            in self.workflow_history

            if workflow.completed
        ]

    # =========================================================
    # SUCCESS RATE
    # =========================================================

    def workflow_success_rate(
        self,
    ) -> float:

        if not self.workflow_history:
            return 0.0

        successful = len(
            self.successful_workflows()
        )

        return round(

            (
                successful /
                len(self.workflow_history)
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

            "total_workflows": (
                len(self.workflow_history)
            ),

            "successful_workflows": (
                len(
                    self.successful_workflows()
                )
            ),

            "failed_workflows": (
                len(
                    self.failed_workflows()
                )
            ),

            "workflow_success_rate": (
                self.workflow_success_rate()
            ),

            "execution_graph": (
                self.execution_graph.export_graph()
            ),

            "retry_metrics": (
                self.retry_manager.export_metrics()
            ),

            "event_metrics": (
                self.dispatcher.export_metrics()
            ),
        }