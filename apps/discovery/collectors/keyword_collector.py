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

    # =========================
    # STATIC PATTERNS
    # =========================

    PREFIX_PATTERNS = [

        "best",

        "top",

        "cheap",

        "free",

        "professional",
    ]

    SUFFIX_PATTERNS = [

        "tools",

        "software",

        "guide",

        "tutorial",

        "examples",

        "tips",

        "strategy",

        "alternatives",

        "comparison",

        "review",

        "trends",

        "checklist",
    ]

    AUDIENCE_PATTERNS = [

        "for beginners",

        "for students",

        "for professionals",

        "for startups",

        "for agencies",
    ]

    LONG_TAIL_PATTERNS = [

        "how to use {}",

        "how to learn {}",

        "best free {}",

        "{} implementation guide",

        "{} best practices",

        "{} use cases",

        "{} roadmap",

        "{} mistakes to avoid",
    ]

    def collect(
        self,
        seed_keyword
    ):

        # =========================
        # VALIDATE INPUT
        # =========================

        if not seed_keyword:

            logger.warning(
                "Empty seed keyword received"
            )

            return {

                "seed_keyword": "",

                "total_keywords": 0,

                "keywords": [],
            }

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
        # KEYWORD STORAGE
        # =========================

        keyword_patterns = []

        # =========================
        # PREFIX PATTERNS
        # =========================

        for prefix in (
            self.PREFIX_PATTERNS
        ):

            keyword_patterns.append(

                KeywordNormalizer.add_prefix(
                    seed_keyword,
                    prefix
                )
            )

        # =========================
        # SUFFIX PATTERNS
        # =========================

        for suffix in (
            self.SUFFIX_PATTERNS
        ):

            keyword_patterns.append(

                KeywordNormalizer.add_suffix(
                    seed_keyword,
                    suffix
                )
            )

        # =========================
        # AUDIENCE PATTERNS
        # =========================

        for audience in (
            self.AUDIENCE_PATTERNS
        ):

            keyword_patterns.append(

                f"{seed_keyword} {audience}"
            )

        # =========================
        # LONG TAIL PATTERNS
        # =========================

        for pattern in (
            self.LONG_TAIL_PATTERNS
        ):

            keyword_patterns.append(
                pattern.format(
                    seed_keyword
                )
            )

        # =========================
        # AI VARIATIONS
        # =========================

        ai_variations = []

        try:

            ai_variations = (
                KeywordNormalizer.generate_variations(
                    seed_keyword
                )
            ) or []

        except Exception as error:

            logger.warning(

                f"Variation generation failed: "
                f"{str(error)}"
            )

        # =========================
        # COMBINE KEYWORDS
        # =========================

        all_keywords = (
            keyword_patterns
            + ai_variations
        )

        # =========================
        # REMOVE EMPTY VALUES
        # =========================

        all_keywords = [

            keyword.strip()

            for keyword in all_keywords

            if keyword
        ]

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