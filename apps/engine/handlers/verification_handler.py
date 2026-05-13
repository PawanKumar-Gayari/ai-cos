"""
Content verification handler.
"""

from apps.verifier.engine import (
    VerifierEngine,
)


class VerificationHandler:

    def __init__(self):

        # =========================
        # VERIFIER ENGINE
        # =========================

        self.verifier_engine = (
            VerifierEngine()
        )

    def execute(
        self,
        content_data
    ):

        # =========================
        # VERIFY CONTENT
        # =========================

        return (
            self.verifier_engine.verify(
                content_data
            )
        )