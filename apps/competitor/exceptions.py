"""
Competitor engine exceptions.
"""


class CompetitorException(
    Exception
):

    """
    Base competitor engine exception.
    """

    default_message = (
        "Competitor engine error."
    )

    def __init__(
        self,
        message=None,
    ):

        self.message = (
            message
            or self.default_message
        )

        super().__init__(
            self.message
        )


class CompetitorValidationException(
    CompetitorException
):

    """
    Competitor validation error.
    """

    default_message = (
        "Invalid competitor input."
    )


class CompetitorAnalysisException(
    CompetitorException
):

    """
    Competitor analysis failure.
    """

    default_message = (
        "Competitor analysis failed."
    )


class SERPExtractionException(
    CompetitorException
):

    """
    SERP extraction failure.
    """

    default_message = (
        "SERP extraction failed."
    )


class ContentAnalysisException(
    CompetitorException
):

    """
    Content analysis failure.
    """

    default_message = (
        "Content analysis failed."
    )


class StructureAnalysisException(
    CompetitorException
):

    """
    Structure analysis failure.
    """

    default_message = (
        "Structure analysis failed."
    )


class GapAnalysisException(
    CompetitorException
):

    """
    Gap analysis failure.
    """

    default_message = (
        "Gap analysis failed."
    )


class WeaknessDetectionException(
    CompetitorException
):

    """
    Weakness detection failure.
    """

    default_message = (
        "Weakness detection failed."
    )


class CompetitorScoringException(
    CompetitorException
):

    """
    Competitor scoring failure.
    """

    default_message = (
        "Competitor scoring failed."
    )