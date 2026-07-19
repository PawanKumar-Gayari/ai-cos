class SEORules:

    """
    SEO validation rules.
    """

    def evaluate(
        self,
        seo_score,
    ):

        passed = (
            seo_score >= 50
        )

        return {

            "passed": passed,

            "score": seo_score,

            "message": (

                "SEO score acceptable"

                if passed

                else

                "SEO score too low"
            ),
        }