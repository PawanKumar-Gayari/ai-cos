"""
Competitor weakness detector.
"""

from utils.helpers import (
    Helpers,
)

from utils.scoring_helpers import (
    ScoringHelpers,
)

from utils.logger import (
    competitor_logger,
)

from utils.config import (
    Config,
)


class WeaknessDetector:

    BUYER_SECTIONS = [

        "pricing",

        "deals",

        "discount",

        "buy now",

        "coupons",

        "offers",
    ]

    TRUST_SECTIONS = [

        "case study",

        "testimonials",

        "expert review",

        "user experience",
    ]

    def normalize_sections(
        self,
        sections,
    ):

        """
        Normalize headings/sections.
        """

        normalized = []

        for section in sections:

            if not section:

                continue

            normalized.append(

                str(section)
                .strip()
                .lower()
            )

        return normalized

    def section_exists(
        self,
        target,
        sections,
    ):

        """
        Case-insensitive section lookup.
        """

        target = (
            target.strip().lower()
        )

        return target in sections

    def any_section_exists(
        self,
        targets,
        sections,
    ):

        """
        Check if any section exists.
        """

        for target in targets:

            if self.section_exists(

                target,

                sections,
            ):

                return True

        return False

    def detect(
        self,
        content_analysis,
        structure_analysis,
    ):

        """
        Detect competitor weaknesses.
        """

        competitor_logger.info(
            "Starting weakness detection"
        )

        # ==========================================
        # WEAKNESS STORAGE
        # ==========================================

        weaknesses = []

        # ==========================================
        # EXTRACT DATA
        # ==========================================

        average_word_count = (
            content_analysis.get(
                "average_word_count",
                0
            )
        )

        common_headings = (
            content_analysis.get(
                "common_headings",
                []
            )
        )

        average_sections = (
            structure_analysis.get(
                "average_sections",
                0
            )
        )

        # ==========================================
        # NORMALIZE HEADINGS
        # ==========================================

        normalized_headings = (
            self.normalize_sections(
                common_headings
            )
        )

        # ==========================================
        # LOW WORD COUNT
        # ==========================================

        if average_word_count < (
            Config.MIN_CONTENT_WORDS
        ):

            weaknesses.append(

                "Competitors have low average word count."
            )

        # ==========================================
        # LOW STRUCTURE DEPTH
        # ==========================================

        if average_sections < (
            Config.MIN_STRUCTURE_SECTIONS
        ):

            weaknesses.append(

                "Competitor articles lack detailed structure."
            )

        # ==========================================
        # FAQ WEAKNESS
        # ==========================================

        if not self.section_exists(

            "faq",

            normalized_headings,
        ):

            weaknesses.append(

                "Most competitors are missing FAQ optimization."
            )

        # ==========================================
        # COMPARISON WEAKNESS
        # ==========================================

        if not self.section_exists(

            "comparison",

            normalized_headings,
        ):

            weaknesses.append(

                "Competitors lack detailed comparison sections."
            )

        # ==========================================
        # BUYER INTENT WEAKNESS
        # ==========================================

        buyer_found = (
            self.any_section_exists(

                self.BUYER_SECTIONS,

                normalized_headings,
            )
        )

        if not buyer_found:

            weaknesses.append(

                "Buyer intent optimization is weak among competitors."
            )

        # ==========================================
        # TRUST SIGNAL WEAKNESS
        # ==========================================

        trust_found = (
            self.any_section_exists(

                self.TRUST_SECTIONS,

                normalized_headings,
            )
        )

        if not trust_found:

            weaknesses.append(

                "Competitors lack trust-building content sections."
            )

        # ==========================================
        # REMOVE DUPLICATES
        # ==========================================

        unique_weaknesses = (
            Helpers.unique_list(
                weaknesses
            )
        )

        unique_weaknesses.sort()

        # ==========================================
        # WEAKNESS SCORE
        # ==========================================

        raw_weakness_score = (

            len(unique_weaknesses)
            * 15
        )

        weakness_score = (
            ScoringHelpers.normalize_score(
                raw_weakness_score
            )
        )

        # ==========================================
        # WEAKNESS LEVEL
        # ==========================================

        weakness_level = (
            ScoringHelpers.confidence_level(
                weakness_score
            )
        )

        competitor_logger.info(

            f"Weakness detection completed "
            f"with {len(unique_weaknesses)} "
            f"weaknesses"
        )

        # ==========================================
        # RETURN RESULT
        # ==========================================

        return {

            "total_weaknesses": len(
                unique_weaknesses
            ),

            "weakness_score": (
                weakness_score
            ),

            "weakness_level": (
                weakness_level
            ),

            "weaknesses": (
                unique_weaknesses
            ),
        }