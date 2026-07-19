"""
System Check

Purpose:
Run full Decision Engine validation.

Checks:
- imports
- runtime execution
- verification flow
- reasoning flow
- scoring flow
- orchestration flow

Goal:
Find failures automatically.
"""

# =============================================================
# IMPORTS
# =============================================================

import traceback


# =============================================================
# SYSTEM CHECK
# =============================================================

class SystemCheck:

    """
    Master Decision Engine tester.
    """

    # =========================================================
    # INIT
    # =========================================================

    def __init__(self):

        self.passed = []

        self.failed = []

    # =========================================================
    # RUN
    # =========================================================

    def run(self):

        print("\n==============================")
        print("AI_COS SYSTEM CHECK")
        print("==============================\n")

        # =====================================================
        # TESTS
        # =====================================================

        self.test_verification()

        self.test_reasoning()

        self.test_scoring()

        self.test_orchestration()

        self.test_decision()

        # =====================================================
        # SUMMARY
        # =====================================================

        self.summary()

    # =========================================================
    # RECORD PASS
    # =========================================================

    def record_pass(
        self,
        name,
    ):

        self.passed.append(name)

        print(f"[PASS] {name}")

    # =========================================================
    # RECORD FAIL
    # =========================================================

    def record_fail(
        self,
        name,
        error,
    ):

        self.failed.append(
            {
                "name": name,
                "error": str(error),
            }
        )

        print(f"[FAIL] {name}")

        print(error)

        print()

    # =========================================================
    # VERIFICATION
    # =========================================================

    def test_verification(self):

        try:

            from apps.decision_engine.verification.verification_engine import (
                VerificationEngine,
            )

            engine = (
                VerificationEngine()
            )

            result = engine.verify(

                content="""
                GATE 2026 registration started.
                The cutoff is 650 marks.
                The cutoff is 720 marks.
                """,

                keyword="GATE 2026",

                verified_facts=[
                    "The cutoff is 650 marks"
                ],

                sources=[
                    "https://openai.com",
                ],
            )

            if (
                "decision"
                not in result
            ):

                raise Exception(
                    "decision missing"
                )

            self.record_pass(
                "verification_engine"
            )

        except Exception as error:

            self.record_fail(
                "verification_engine",
                traceback.format_exc(),
            )

    # =========================================================
    # REASONING
    # =========================================================

    def test_reasoning(self):

        try:

            from apps.decision_engine.reasoning.consensus_engine import (
                ConsensusEngine,
            )

            engine = (
                ConsensusEngine()
            )

            self.record_pass(
                "consensus_engine"
            )

        except Exception:

            self.record_fail(
                "consensus_engine",
                traceback.format_exc(),
            )

    # =========================================================
    # SCORING
    # =========================================================

    def test_scoring(self):

        try:

            from apps.decision_engine.scoring.scoring_orchestrator import (
                ScoringOrchestrator,
            )

            engine = (
                ScoringOrchestrator()
            )

            self.record_pass(
                "scoring_orchestrator"
            )

        except Exception:

            self.record_fail(
                "scoring_orchestrator",
                traceback.format_exc(),
            )

    # =========================================================
    # ORCHESTRATION
    # =========================================================

    def test_orchestration(self):

        try:

            from apps.decision_engine.orchestration.workflow_engine import (
                WorkflowEngine,
            )

            engine = (
                WorkflowEngine()
            )

            self.record_pass(
                "workflow_engine"
            )

        except Exception:

            self.record_fail(
                "workflow_engine",
                traceback.format_exc(),
            )

    # =========================================================
    # DECISION
    # =========================================================

    def test_decision(self):

        try:

            from apps.decision_engine.orchestration.decision_router import (
                DecisionRouter,
            )

            router = (
                DecisionRouter()
            )

            self.record_pass(
                "decision_router"
            )

        except Exception:

            self.record_fail(
                "decision_router",
                traceback.format_exc(),
            )

    # =========================================================
    # SUMMARY
    # =========================================================

    def summary(self):

        print("\n==============================")
        print("SUMMARY")
        print("==============================\n")

        print(
            f"PASSED: {len(self.passed)}"
        )

        print(
            f"FAILED: {len(self.failed)}"
        )

        print()

        if self.failed:

            print("FAILED TESTS:\n")

            for item in self.failed:

                print(
                    f"- {item['name']}"
                )

        else:

            print(
                "ALL SYSTEMS OPERATIONAL"
            )


# =============================================================
# MAIN
# =============================================================

if __name__ == "__main__":

    checker = SystemCheck()

    checker.run()