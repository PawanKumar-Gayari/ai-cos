class QualityRules:

    """
    Content quality rules.
    """

    def evaluate(
        self,
        quality_score,
    ):

        passed = (
            quality_score >= 60
        )

        return {

            "passed": passed,

            "score": quality_score,

            "message": (

                "Content quality acceptable"

                if passed

                else

                "Content quality below threshold"
            ),
        }