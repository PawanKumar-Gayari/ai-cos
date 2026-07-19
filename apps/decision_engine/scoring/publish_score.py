class PublishScore:

    def calculate(
        self,
        seo_score,
        quality_score,
    ):

        final_score = (

            seo_score * 0.6

            +

            quality_score * 0.4
        )

        return round(
            final_score,
            2,
        )