class UpdatePlanner:

    """
    Content update strategy planner.
    """

    def build(
        self,
        keyword,
    ):

        keyword_length = len(
            keyword.split()
        )

        update_frequency = (
            "monthly"
        )

        if keyword_length <= 2:

            update_frequency = (
                "weekly"
            )

        elif keyword_length >= 5:

            update_frequency = (
                "quarterly"
            )

        return {

            "keyword": keyword,

            "update_frequency": (
                update_frequency
            ),

            "refresh_required": True,
        }