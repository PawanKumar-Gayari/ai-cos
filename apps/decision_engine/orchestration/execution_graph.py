"""
Execution Graph

Purpose:
Manage workflow dependency execution graph.

Handles:
- execution order
- dependency management
- parallel execution readiness
- DAG orchestration
- workflow validation
- execution tracing

Goal:
Enable scalable orchestration intelligence.

This becomes the workflow DAG engine
of AI_COS.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Any, List, Optional


# =============================================================
# EXECUTION NODE
# =============================================================

@dataclass
class ExecutionNode:

    # =========================================================
    # CORE
    # =========================================================

    node_id: str

    name: str

    engine: str

    # =========================================================
    # DEPENDENCIES
    # =========================================================

    depends_on: List[str] = field(
        default_factory=list
    )

    children: List[str] = field(
        default_factory=list
    )

    # =========================================================
    # EXECUTION
    # =========================================================

    executed: bool = False

    failed: bool = False

    skipped: bool = False

    retry_count: int = 0

    # =========================================================
    # PRIORITY
    # =========================================================

    priority: str = "medium"

    parallel_execution_allowed: bool = False

    # =========================================================
    # TIMESTAMPS
    # =========================================================

    started_at: Optional[datetime] = None

    completed_at: Optional[datetime] = None

    # =========================================================
    # RESULTS
    # =========================================================

    output: Dict[str, Any] = field(
        default_factory=dict
    )

    errors: List[str] = field(
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

    def add_error(
        self,
        error: str,
    ) -> None:

        if (
            error
            and error not in self.errors
        ):

            self.errors.append(error)


# =============================================================
# EXECUTION GRAPH
# =============================================================

class ExecutionGraph:

    """
    Workflow DAG orchestration engine.
    """

    def __init__(
        self,
    ) -> None:

        # =====================================================
        # NODES
        # =====================================================

        self.nodes: Dict[
            str,
            ExecutionNode
        ] = {}

        # =====================================================
        # EXECUTION ORDER
        # =====================================================

        self.execution_trace: List[str] = []

    # =========================================================
    # ADD NODE
    # =========================================================

    def add_node(
        self,
        node: ExecutionNode,
    ) -> None:

        self.nodes[node.node_id] = node

    # =========================================================
    # CONNECT
    # =========================================================

    def connect(
        self,
        parent_id: str,
        child_id: str,
    ) -> None:

        parent = self.nodes.get(parent_id)

        child = self.nodes.get(child_id)

        if not parent or not child:
            return

        if child_id not in parent.children:

            parent.children.append(
                child_id
            )

        if parent_id not in child.depends_on:

            child.depends_on.append(
                parent_id
            )

    # =========================================================
    # READY NODES
    # =========================================================

    def ready_nodes(
        self,
    ) -> List[ExecutionNode]:

        ready = []

        for node in self.nodes.values():

            if node.executed:
                continue

            if node.failed:
                continue

            dependencies_met = all(

                self.nodes[dependency].executed

                for dependency
                in node.depends_on

                if dependency in self.nodes
            )

            if dependencies_met:

                ready.append(node)

        return ready

    # =========================================================
    # EXECUTE NODE
    # =========================================================

    def execute_node(
        self,
        node_id: str,
        output: Dict[str, Any] = None,
    ) -> bool:

        node = self.nodes.get(node_id)

        if not node:
            return False

        try:

            node.started_at = (
                datetime.utcnow()
            )

            node.executed = True

            node.output = output or {}

            node.completed_at = (
                datetime.utcnow()
            )

            self.execution_trace.append(
                node_id
            )

            return True

        except Exception as error:

            node.failed = True

            node.add_error(
                str(error)
            )

            return False

    # =========================================================
    # FAIL NODE
    # =========================================================

    def fail_node(
        self,
        node_id: str,
        error: str,
    ) -> bool:

        node = self.nodes.get(node_id)

        if not node:
            return False

        node.failed = True

        node.add_error(error)

        node.completed_at = (
            datetime.utcnow()
        )

        return True

    # =========================================================
    # SKIP NODE
    # =========================================================

    def skip_node(
        self,
        node_id: str,
    ) -> bool:

        node = self.nodes.get(node_id)

        if not node:
            return False

        node.skipped = True

        node.completed_at = (
            datetime.utcnow()
        )

        return True

    # =========================================================
    # RETRY NODE
    # =========================================================

    def retry_node(
        self,
        node_id: str,
    ) -> bool:

        node = self.nodes.get(node_id)

        if not node:
            return False

        node.failed = False

        node.executed = False

        node.retry_count += 1

        node.errors = []

        return True

    # =========================================================
    # EXECUTION COMPLETE
    # =========================================================

    def execution_complete(
        self,
    ) -> bool:

        return all(

            node.executed
            or node.skipped

            for node in self.nodes.values()
        )

    # =========================================================
    # FAILED NODES
    # =========================================================

    def failed_nodes(
        self,
    ) -> List[ExecutionNode]:

        return [

            node

            for node in self.nodes.values()

            if node.failed
        ]

    # =========================================================
    # EXECUTED NODES
    # =========================================================

    def executed_nodes(
        self,
    ) -> List[ExecutionNode]:

        return [

            node

            for node in self.nodes.values()

            if node.executed
        ]

    # =========================================================
    # PENDING NODES
    # =========================================================

    def pending_nodes(
        self,
    ) -> List[ExecutionNode]:

        return [

            node

            for node in self.nodes.values()

            if (
                not node.executed
                and not node.failed
                and not node.skipped
            )
        ]

    # =========================================================
    # CRITICAL PATH
    # =========================================================

    def critical_path(
        self,
    ) -> List[str]:

        path = []

        for node in self.nodes.values():

            if node.priority in [
                "high",
                "critical",
            ]:

                path.append(node.node_id)

        return path

    # =========================================================
    # VALIDATE GRAPH
    # =========================================================

    def validate_graph(
        self,
    ) -> bool:

        # =====================================================
        # DEPENDENCY CHECK
        # =====================================================

        for node in self.nodes.values():

            for dependency in node.depends_on:

                if dependency not in self.nodes:

                    return False

        return True

    # =========================================================
    # BUILD DEFAULT WORKFLOW
    # =========================================================

    def build_editorial_workflow(
        self,
    ) -> None:

        # =====================================================
        # DISCOVERY
        # =====================================================

        discovery = ExecutionNode(

            node_id="discovery",

            name="Keyword Discovery",

            engine="discovery_engine",
        )

        # =====================================================
        # SERP
        # =====================================================

        serp = ExecutionNode(

            node_id="serp_analysis",

            name="SERP Analysis",

            engine="serp_engine",
        )

        # =====================================================
        # VERIFICATION
        # =====================================================

        verification = ExecutionNode(

            node_id="verification",

            name="Fact Verification",

            engine="verification_engine",

            priority="critical",
        )

        # =====================================================
        # GENERATION
        # =====================================================

        generation = ExecutionNode(

            node_id="generation",

            name="Article Generation",

            engine="generation_engine",
        )

        # =====================================================
        # SCORING
        # =====================================================

        scoring = ExecutionNode(

            node_id="scoring",

            name="Quality Scoring",

            engine="scoring_engine",
        )

        # =====================================================
        # PREDICTION
        # =====================================================

        prediction = ExecutionNode(

            node_id="prediction",

            name="Ranking Prediction",

            engine="ranking_engine",
        )

        # =====================================================
        # DECISION
        # =====================================================

        decision = ExecutionNode(

            node_id="decision",

            name="Publishing Decision",

            engine="decision_engine",

            priority="critical",
        )

        # =====================================================
        # PUBLISH
        # =====================================================

        publish = ExecutionNode(

            node_id="publish",

            name="Publishing",

            engine="publisher_engine",
        )

        # =====================================================
        # MONITORING
        # =====================================================

        monitoring = ExecutionNode(

            node_id="monitoring",

            name="Freshness Monitoring",

            engine="monitoring_engine",

            parallel_execution_allowed=True,
        )

        # =====================================================
        # REGISTER
        # =====================================================

        nodes = [

            discovery,
            serp,
            verification,
            generation,
            scoring,
            prediction,
            decision,
            publish,
            monitoring,
        ]

        for node in nodes:

            self.add_node(node)

        # =====================================================
        # DEPENDENCIES
        # =====================================================

        self.connect(
            "discovery",
            "serp_analysis",
        )

        self.connect(
            "serp_analysis",
            "verification",
        )

        self.connect(
            "verification",
            "generation",
        )

        self.connect(
            "generation",
            "scoring",
        )

        self.connect(
            "scoring",
            "prediction",
        )

        self.connect(
            "prediction",
            "decision",
        )

        self.connect(
            "decision",
            "publish",
        )

        self.connect(
            "publish",
            "monitoring",
        )

    # =========================================================
    # EXPORT
    # =========================================================

    def export_graph(
        self,
    ) -> Dict[str, Any]:

        return {

            "total_nodes": (
                len(self.nodes)
            ),

            "executed_nodes": (
                len(
                    self.executed_nodes()
                )
            ),

            "failed_nodes": (
                len(
                    self.failed_nodes()
                )
            ),

            "pending_nodes": (
                len(
                    self.pending_nodes()
                )
            ),

            "execution_complete": (
                self.execution_complete()
            ),

            "critical_path": (
                self.critical_path()
            ),

            "execution_trace": (
                self.execution_trace
            ),

            "nodes": {

                node_id: {

                    "name": (
                        node.name
                    ),

                    "engine": (
                        node.engine
                    ),

                    "depends_on": (
                        node.depends_on
                    ),

                    "children": (
                        node.children
                    ),

                    "executed": (
                        node.executed
                    ),

                    "failed": (
                        node.failed
                    ),

                    "priority": (
                        node.priority
                    ),

                    "retry_count": (
                        node.retry_count
                    ),
                }

                for node_id, node
                in self.nodes.items()
            },
        }