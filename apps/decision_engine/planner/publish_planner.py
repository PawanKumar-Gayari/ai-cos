class PublishPlanner:

    """
    Publishing strategy planner.
    """

    def build(
        self,
        scores,
    ):

        publish_score = scores.get(
            "publish_score",
            0,
        )

        should_publish = (
            publish_score >= 60
        )

        recommended_schedule = (
            "immediate"
        )

        if publish_score < 70:

            recommended_schedule = (
                "manual_review"
            )

        return {

            "should_publish": (
                should_publish
            ),

            "publish_score": (
                publish_score
            ),

            "schedule": (
                recommended_schedule
            ),
        }