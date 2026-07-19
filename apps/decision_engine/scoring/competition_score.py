class CompetitionScore:

    def calculate(
        self,
        keyword_length,
    ):

        if keyword_length <= 2:

            return 85

        if keyword_length <= 4:

            return 60

        return 35