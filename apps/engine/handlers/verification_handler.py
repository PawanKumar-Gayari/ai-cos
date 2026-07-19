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
        # VALIDATE INPUT
        # =========================

        if not isinstance(
            content_data,
            dict
        ):

            return {

                "verified": False,

                "final_score": 0,

                "errors": [
                    "Invalid content data format"
                ],
            }

        # =========================
        # CONTENT CHECK
        # =========================

        raw_content = content_data.get(
            "content",
            ""
        )

        if not raw_content:

            return {

                "verified": False,

                "final_score": 0,

                "errors": [
                    "Content is empty"
                ],
            }

        # =========================
        # RUN VERIFICATION
        # =========================

        verification_result = (

            self.verifier_engine.verify(
                content_data
            )
        )

        # =========================
        # FINAL RESPONSE
        # =========================

        return {

            "verified": verification_result.get(
                "verified",
                False
            ),

            "final_score": verification_result.get(
                "final_score",
                0
            ),

            "title": verification_result.get(
                "title",
                ""
            ),

            "slug": verification_result.get(
                "slug",
                ""
            ),

            "meta_description": (
                verification_result.get(
                    "meta_description",
                    ""
                )
            ),

            "content": verification_result.get(
                "content",
                ""
            ),

            "checks": verification_result.get(
                "checks",
                []
            ),

            "warnings": verification_result.get(
                "warnings",
                []
            ),

            "errors": verification_result.get(
                "errors",
                []
            ),

            "validator_results": (
                verification_result.get(
                    "validator_results",
                    {}
                )
            ),
        }