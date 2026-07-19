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

    STOPWORDS = {

        "a",

        "an",

        "the",

        "and",

        "or",

        "for",

        "with",

        "of",
    }

    # =========================
    # MINIMUM KEYWORD LENGTH
    # =========================

    MIN_KEYWORD_LENGTH = 2

    def clean(
        self,
        keywords
    ):

        # =========================
        # VALIDATE INPUT
        # =========================

        if not keywords:

            logger.warning(
                "No keywords received for cleaning"
            )

            return {

                "total_keywords": 0,

                "keywords": [],
            }

        logger.info(

            f"Starting keyword cleaning "
            f"for {len(keywords)} keywords"
        )

        # =========================
        # CLEANED KEYWORDS
        # =========================

        cleaned_keywords = []

        # =========================
        # PROCESS KEYWORDS
        # =========================

        for keyword in keywords:

            try:

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
                # REMOVE SPECIAL CHARS
                # =====================

                keyword = re.sub(

                    r"[^a-zA-Z0-9\s]",

                    " ",

                    keyword
                )

                # =====================
                # REMOVE EXTRA SPACES
                # =====================

                keyword = re.sub(

                    r"\s+",

                    " ",

                    keyword
                ).strip()

                # =====================
                # SPLIT WORDS
                # =====================

                words = keyword.split()

                # =====================
                # REMOVE STOPWORDS
                # =====================

                filtered_words = [

                    word

                    for word in words

                    if word not in (
                        self.STOPWORDS
                    )
                ]

                cleaned_keyword = (
                    " ".join(
                        filtered_words
                    ).strip()
                )

                # =====================
                # SKIP EMPTY
                # =====================

                if not cleaned_keyword:

                    continue

                # =====================
                # KEEP SEO SHORT TERMS
                # =====================

                if len(
                    cleaned_keyword
                ) < self.MIN_KEYWORD_LENGTH:

                    continue

                cleaned_keywords.append(
                    cleaned_keyword
                )

            except Exception as error:

                logger.warning(

                    f"Failed to clean keyword: "
                    f"{keyword} | "
                    f"{str(error)}"
                )

                continue

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