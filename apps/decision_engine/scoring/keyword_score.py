class KeywordScore:

    def calculate(
        self,
        keyword,
    ):

        keyword_length = len(
            keyword.split()
        )

        if keyword_length >= 5:

            return 90

        if keyword_length >= 3:

            return 75

        return 50