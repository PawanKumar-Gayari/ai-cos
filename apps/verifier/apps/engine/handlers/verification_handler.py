"""
Verification pipeline handler.
"""

from apps.verifier.services.verification_service import (
    VerificationService,
)


class VerificationHandler:

    def __init__(self):

        # =========================
        # VERIFICATION SERVICE
        # =========================

        self.verification_service = (
            VerificationService()
        )

    def execute(
        self,
        content_data
    ):

        # =========================
        # VERIFY CONTENT
        # =========================

        return (
            self.verification_service.verify(
                content_data
            )
        )