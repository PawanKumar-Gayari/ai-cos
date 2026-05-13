"""
Keyword collector for discovery engine.
"""

from utils.keyword_normalizer import (
    KeywordNormalizer,
)

from utils.helpers import (
    Helpers,
)

from utils.logger import (
    logger,
)


class KeywordCollector:

    def collect(
        self,
        seed_keyword
    ):

        # =========================
        # NORMALIZE INPUT
        # =========================

        seed_keyword = (
            KeywordNormalizer.normalize(
                seed_keyword
            )
        )

        logger.info(

            f"Collecting keywords for: "
            f"{seed_keyword}"
        )

        # =========================
        # BASE PATTERNS
        # =========================

        keyword_patterns = [

            KeywordNormalizer.add_prefix(
                seed_keyword,
                "best"
            ),

            f"{seed_keyword} for beginners",

            f"{seed_keyword} for students",

            f"{seed_keyword} for professionals",

            KeywordNormalizer.add_prefix(
                seed_keyword,
                "cheap"
            ),

            KeywordNormalizer.add_prefix(
                seed_keyword,
                "top"
            ),

            KeywordNormalizer.add_suffix(
                seed_keyword,
                "tools"
            ),

            KeywordNormalizer.add_suffix(
                seed_keyword,
                "software"
            ),

            KeywordNormalizer.add_suffix(
                seed_keyword,
                "guide"
            ),

            KeywordNormalizer.add_suffix(
                seed_keyword,
                "tutorial"
            ),

            f"how to use {seed_keyword}",

            KeywordNormalizer.add_suffix(
                seed_keyword,
                "examples"
            ),

            KeywordNormalizer.add_suffix(
                seed_keyword,
                "tips"
            ),

            KeywordNormalizer.add_suffix(
                seed_keyword,
                "strategy"
            ),

            KeywordNormalizer.add_suffix(
                seed_keyword,
                "alternatives"
            ),

            f"best free {seed_keyword}",

            KeywordNormalizer.add_suffix(
                seed_keyword,
                "comparison"
            ),

            KeywordNormalizer.add_suffix(
                seed_keyword,
                "review"
            ),

            KeywordNormalizer.add_suffix(
                seed_keyword,
                "trends"
            ),

            KeywordNormalizer.add_suffix(
                seed_keyword,
                "checklist"
            ),
        ]

        # =========================
        # AI VARIATIONS
        # =========================

        ai_variations = (
            KeywordNormalizer.generate_variations(
                seed_keyword
            )
        )

        # =========================
        # COMBINE KEYWORDS
        # =========================

        all_keywords = (
            keyword_patterns
            + ai_variations
        )

        # =========================
        # REMOVE DUPLICATES
        # =========================

        unique_keywords = (
            Helpers.unique_list(
                all_keywords
            )
        )

        # =========================
        # SORT RESULTS
        # =========================

        unique_keywords.sort()

        logger.info(

            f"Generated "
            f"{len(unique_keywords)} "
            f"keywords"
        )

        # =========================
        # RETURN RESULT
        # =========================

        return {

            "seed_keyword": (
                seed_keyword
            ),

            "total_keywords": len(
                unique_keywords
            ),

            "keywords": (
                unique_keywords
            ),
        }