"""
Central keyword normalization utility.
"""


class KeywordNormalizer:

    # =========================
    # COMMON PREFIXES
    # =========================

    COMMON_PREFIXES = [

        "best",

        "top",

        "cheap",

        "free",

        "ultimate",

        "guide",
    ]

    # =========================
    # COMMON SUFFIXES
    # =========================

    COMMON_SUFFIXES = [

        "review",

        "reviews",

        "guide",

        "tutorial",

        "tips",
    ]

    # =========================
    # NORMALIZE KEYWORD
    # =========================

    @classmethod
    def normalize(
        cls,
        keyword
    ):

        # =========================
        # BASIC CLEANUP
        # =========================

        keyword = (
            keyword
            .strip()
            .lower()
        )

        # =========================
        # REMOVE EXTRA SPACES
        # =========================

        keyword = " ".join(
            keyword.split()
        )

        # =========================
        # SPLIT WORDS
        # =========================

        words = keyword.split()

        # =========================
        # REMOVE DUPLICATE WORDS
        # =========================

        cleaned_words = []

        for word in words:

            if word not in cleaned_words:

                cleaned_words.append(
                    word
                )

        keyword = " ".join(
            cleaned_words
        )

        # =========================
        # RETURN RESULT
        # =========================

        return keyword

    # =========================
    # SAFE PREFIX ADDER
    # =========================

    @classmethod
    def add_prefix(
        cls,
        keyword,
        prefix
    ):

        keyword = cls.normalize(
            keyword
        )

        prefix = (
            prefix
            .strip()
            .lower()
        )

        # =========================
        # PREVENT DUPLICATES
        # =========================

        if keyword.startswith(
            prefix
        ):

            return keyword

        return f"{prefix} {keyword}"

    # =========================
    # SAFE SUFFIX ADDER
    # =========================

    @classmethod
    def add_suffix(
        cls,
        keyword,
        suffix
    ):

        keyword = cls.normalize(
            keyword
        )

        suffix = (
            suffix
            .strip()
            .lower()
        )

        # =========================
        # PREVENT DUPLICATES
        # =========================

        if keyword.endswith(
            suffix
        ):

            return keyword

        return f"{keyword} {suffix}"

    # =========================
    # GENERATE VARIATIONS
    # =========================

    @classmethod
    def generate_variations(
        cls,
        keyword
    ):

        keyword = cls.normalize(
            keyword
        )

        variations = []

        # =========================
        # PREFIX VARIATIONS
        # =========================

        for prefix in cls.COMMON_PREFIXES:

            variations.append(

                cls.add_prefix(
                    keyword,
                    prefix
                )
            )

        # =========================
        # SUFFIX VARIATIONS
        # =========================

        for suffix in cls.COMMON_SUFFIXES:

            variations.append(

                cls.add_suffix(
                    keyword,
                    suffix
                )
            )

        # =========================
        # ORIGINAL KEYWORD
        # =========================

        variations.append(
            keyword
        )

        # =========================
        # UNIQUE RESULTS
        # =========================

        unique_variations = list(

            set(variations)
        )

        unique_variations.sort()

        # =========================
        # RETURN RESULT
        # =========================

        return unique_variations