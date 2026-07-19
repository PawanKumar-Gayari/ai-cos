"""
Verification decision service.
"""


class VerificationDecisionService:

    def decide(
        self,
        verification_result
    ):

        # =========================
        # EXTRACT DATA
        # =========================

        final_score = (
            verification_result.get(
                "final_score",
                0
            )
        )

        warnings = (
            verification_result.get(
                "warnings",
                []
            )
        )

        errors = (
            verification_result.get(
                "errors",
                []
            )
        )

        validator_results = (
            verification_result.get(
                "validator_results",
                {}
            )
        )

        # =========================
        # CRITICAL FAILURE
        # =========================

        if errors:

            return {

                "decision": "reject",

                "reason": (
                    "Critical validation errors detected"
                ),
            }

        # =========================
        # FACT VALIDATION FAILURE
        # =========================

        fact_result = (
            validator_results.get(
                "fact",
                {}
            )
        )

        if fact_result.get(
            "fact_score",
            0
        ) < 40:

            return {

                "decision": "regenerate",

                "reason": (
                    "Fact validation confidence too low"
                ),
            }

        # =========================
        # LOW QUALITY CONTENT
        # =========================

        if final_score < 60:

            return {

                "decision": "rewrite",

                "reason": (
                    "Content quality score too low"
                ),
            }

        # =========================
        # WARNING HEAVY CONTENT
        # =========================

        if len(warnings) >= 10:

            return {

                "decision": "rewrite",

                "reason": (
                    "Too many quality warnings detected"
                ),
            }

        # =========================
        # APPROVED CONTENT
        # =========================

        return {

            "decision": "approve",

            "reason": (
                "Content passed verification"
            ),
        }