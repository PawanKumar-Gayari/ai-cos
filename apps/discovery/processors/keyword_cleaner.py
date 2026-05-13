"""
Keyword cleaner for discovery engine.
"""

import re

from utils.keyword_normalizer import (
    KeywordNormalizer,
)

from utils.helpers import (
    Helpers,
)

from utils.text_cleaner import (
    TextCleaner,
)

from utils.logger import (
    logger,
)


class KeywordCleaner:

    # =========================
    # STOPWORDS
    # =========================

    STOPWORDS = [

        "a",

        "an",

        "the",

        "and",

        "or",

        "for",

        "with",

        "of",
    ]

    def clean(
        self,
        keywords
    ):

        logger.info(

            f"Starting keyword cleaning "
            f"for {len(keywords)} keywords"
        )

        # =========================
        # VALID KEYWORDS
        # =========================

        cleaned_keywords = []

        # =========================
        # PROCESS KEYWORDS
        # =========================

        for keyword in keywords:

            # =====================
            # SKIP EMPTY
            # =====================

            if not keyword:

                continue

            # =====================
            # TEXT CLEANUP
            # =====================

            keyword = (
                TextCleaner.clean(
                    keyword,
                    lowercase=True
                )
            )

            # =====================
            # NORMALIZE KEYWORD
            # =====================

            keyword = (
                KeywordNormalizer.normalize(
                    keyword
                )
            )

            # =====================
            # REMOVE EXTRA SPACES
            # =====================

            keyword = re.sub(

                r"\s+",

                " ",

                keyword
            )

            # =====================
            # REMOVE SPECIAL CHARS
            # =====================

            keyword = re.sub(

                r"[^a-z0-9\s]",

                "",

                keyword
            )

            # =====================
            # REMOVE STOPWORDS
            # =====================

            words = keyword.split()

            filtered_words = [

                word for word in words

                if word not in (
                    self.STOPWORDS
                )
            ]

            cleaned_keyword = (
                " ".join(
                    filtered_words
                )
            )

            # =====================
            # SKIP EMPTY
            # =====================

            if not cleaned_keyword:

                continue

            # =====================
            # REMOVE VERY SHORT
            # =====================

            if len(cleaned_keyword) < 4:

                continue

            cleaned_keywords.append(
                cleaned_keyword
            )

        # =========================
        # REMOVE DUPLICATES
        # =========================

        unique_keywords = (
            Helpers.unique_list(
                cleaned_keywords
            )
        )

        # =========================
        # SORT KEYWORDS
        # =========================

        unique_keywords.sort()

        logger.info(

            f"Keyword cleaning completed "
            f"with {len(unique_keywords)} "
            f"clean keywords"
        )

        # =========================
        # RETURN RESULT
        # =========================

        return {

            "total_keywords": len(
                unique_keywords
            ),

            "keywords": (
                unique_keywords
            ),
        }