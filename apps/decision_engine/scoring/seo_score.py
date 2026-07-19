class SEOScore:

    def calculate(
        self,
        keyword,
    ):

        score = 50

        keyword = keyword.lower()

        if len(keyword.split()) >= 3:

            score += 20

        if "best" in keyword:

            score += 10

        if "guide" in keyword:

            score += 10

        return min(
            score,
            100,
        )