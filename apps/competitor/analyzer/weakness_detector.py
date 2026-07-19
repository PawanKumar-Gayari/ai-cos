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

    MEDIA_SECTIONS = [

        "infographic",

        "video",

        "chart",

        "table",
    ]

    AI_OVERVIEW_SECTIONS = [

        "summary",

        "quick answer",

        "key takeaways",

        "faq",
    ]

    # ==================================================
    # NORMALIZE SECTIONS
    # ==================================================

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

    # ==================================================
    # SECTION EXISTS
    # ==================================================

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

    # ==================================================
    # ANY SECTION EXISTS
    # ==================================================

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

    # ==================================================
    # WEAKNESS PRIORITY
    # ==================================================

    def calculate_weakness_priority(
        self,
        severity,
    ):

        """
        Calculate weakness priority.
        """

        if severity >= 8:

            return "critical"

        if severity >= 5:

            return "high"

        if severity >= 3:

            return "medium"

        return "low"

    # ==================================================
    # BUILD WEAKNESS
    # ==================================================

    def build_weakness(
        self,
        weakness,
        severity=5,
    ):

        """
        Build structured weakness object.
        """

        priority = (
            self.calculate_weakness_priority(
                severity
            )
        )

        return {

            "weakness": weakness,

            "severity": severity,

            "priority": priority,
        }

    # ==================================================
    # DETECT WEAKNESSES
    # ==================================================

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

        heading_frequency = (
            content_analysis.get(
                "heading_frequency",
                {}
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

                self.build_weakness(

                    weakness=(
                        "Competitors have low "
                        "average word count."
                    ),

                    severity=8,
                )
            )

        # ==========================================
        # LOW STRUCTURE DEPTH
        # ==========================================

        if average_sections < (
            Config.MIN_STRUCTURE_SECTIONS
        ):

            weaknesses.append(

                self.build_weakness(

                    weakness=(
                        "Competitor articles "
                        "lack detailed structure."
                    ),

                    severity=7,
                )
            )

        # ==========================================
        # FAQ WEAKNESS
        # ==========================================

        faq_frequency = (
            heading_frequency.get(
                "faq",
                0
            )
        )

        if faq_frequency < 3:

            weaknesses.append(

                self.build_weakness(

                    weakness=(
                        "Most competitors are "
                        "missing FAQ optimization."
                    ),

                    severity=9,
                )
            )

        # ==========================================
        # COMPARISON WEAKNESS
        # ==========================================

        comparison_frequency = (
            heading_frequency.get(
                "comparison",
                0
            )
        )

        if comparison_frequency < 3:

            weaknesses.append(

                self.build_weakness(

                    weakness=(
                        "Competitors lack detailed "
                        "comparison sections."
                    ),

                    severity=8,
                )
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

                self.build_weakness(

                    weakness=(
                        "Buyer intent optimization "
                        "is weak among competitors."
                    ),

                    severity=8,
                )
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

                self.build_weakness(

                    weakness=(
                        "Competitors lack "
                        "trust-building content."
                    ),

                    severity=9,
                )
            )

        # ==========================================
        # MEDIA CONTENT WEAKNESS
        # ==========================================

        media_found = (
            self.any_section_exists(

                self.MEDIA_SECTIONS,

                normalized_headings,
            )
        )

        if not media_found:

            weaknesses.append(

                self.build_weakness(

                    weakness=(
                        "Competitors are missing "
                        "media-rich content "
                        "sections."
                    ),

                    severity=6,
                )
            )

        # ==========================================
        # AI OVERVIEW WEAKNESS
        # ==========================================

        ai_overview_found = (
            self.any_section_exists(

                self.AI_OVERVIEW_SECTIONS,

                normalized_headings,
            )
        )

        if not ai_overview_found:

            weaknesses.append(

                self.build_weakness(

                    weakness=(
                        "Competitors are not "
                        "optimized for AI overview "
                        "summaries."
                    ),

                    severity=8,
                )
            )

        # ==========================================
        # FRESHNESS WEAKNESS
        # ==========================================

        current_year_found = (
            self.section_exists(

                "2026",

                normalized_headings,
            )
        )

        if not current_year_found:

            weaknesses.append(

                self.build_weakness(

                    weakness=(
                        "Competitor content lacks "
                        "freshness optimization."
                    ),

                    severity=7,
                )
            )

        # ==========================================
        # REMOVE DUPLICATES
        # ==========================================

        unique_weaknesses = []

        seen = set()

        for weakness in weaknesses:

            weakness_name = (
                weakness.get(
                    "weakness",
                    ""
                )
            )

            if weakness_name in seen:

                continue

            seen.add(
                weakness_name
            )

            unique_weaknesses.append(
                weakness
            )

        # ==========================================
        # SORT BY PRIORITY
        # ==========================================

        priority_order = {

            "critical": 4,

            "high": 3,

            "medium": 2,

            "low": 1,
        }

        unique_weaknesses.sort(

            key=lambda x: (

                priority_order.get(

                    x.get(
                        "priority",
                        "low"
                    ),

                    1,
                ),

                x.get(
                    "severity",
                    0
                ),
            ),

            reverse=True,
        )

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