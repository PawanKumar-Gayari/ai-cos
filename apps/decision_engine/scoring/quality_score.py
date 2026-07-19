class QualityScore:

    def calculate(
        self,
        keyword_length,
    ):

        score = 60

        if keyword_length >= 3:

            score += 15

        return min(
            score,
            100,
        )