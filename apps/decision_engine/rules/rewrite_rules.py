class RewriteRules:

    """
    Rewrite decision rules.
    """

    def evaluate(
        self,
        quality_score,
    ):

        rewrite_required = (
            quality_score < 60
        )

        return {

            "rewrite_required": (
                rewrite_required
            ),

            "message": (

                "Rewrite recommended"

                if rewrite_required

                else

                "Rewrite not required"
            ),
        }