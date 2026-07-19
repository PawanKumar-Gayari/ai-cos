class PublishRules:

    """
    Publishing rules engine.
    """

    def evaluate(
        self,
        publish_score,
    ):

        should_publish = (
            publish_score >= 60
        )

        return {

            "should_publish": (
                should_publish
            ),

            "score": publish_score,

            "message": (

                "Ready for publishing"

                if should_publish

                else

                "Manual review required"
            ),
        }