"""
Custom exceptions for decision engine.
"""


class DecisionEngineError(
    Exception
):

    """
    Base decision engine exception.
    """

    default_message = (
        "Decision engine error."
    )

    def __init__(
        self,
        message=None,
    ):

        self.message = (
            message
            or
            self.default_message
        )

        super().__init__(
            self.message
        )


# ======================================================
# DECISION ERRORS
# ======================================================

class DecisionValidationError(
    DecisionEngineError
):

    default_message = (
        "Invalid decision payload."
    )


class DecisionExecutionError(
    DecisionEngineError
):

    default_message = (
        "Decision execution failed."
    )


# ======================================================
# SCORING ERRORS
# ======================================================

class ScoringError(
    DecisionEngineError
):

    default_message = (
        "Scoring engine failed."
    )


# ======================================================
# PLANNING ERRORS
# ======================================================

class PlanningError(
    DecisionEngineError
):

    default_message = (
        "Planning engine failed."
    )


# ======================================================
# PROVIDER ERRORS
# ======================================================

class ProviderSelectionError(
    DecisionEngineError
):

    default_message = (
        "Provider selection failed."
    )