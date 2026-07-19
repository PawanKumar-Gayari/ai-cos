"""
Verifier engine for AI COS.
"""

from apps.verifier.services.verification_service import (
    VerificationService,
)


class VerifierEngine:

    def __init__(self):

        # =========================
        # VERIFICATION SERVICE
        # =========================

        self.verification_service = (
            VerificationService()
        )

    def verify(
        self,
        content_data
    ):

        # =========================
        # RUN VERIFICATION
        # =========================

        return (
            self.verification_service.verify(
                content_data
            )
        )