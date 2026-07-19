"""
Content gap finder for competitor intelligence engine.
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


class GapFinder:

    ADVANCED_PATTERNS = [

        "advanced guide",

        "case study",

        "expert tips",

        "workflow",

        "automation",

        "use cases",

        "best practices",

        "optimization",
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
    # GAP PRIORITY
    # ==================================================

    def calculate_gap_priority(
        self,
        frequency,
    ):

        """
        Calculate SEO gap priority.
        """

        if frequency >= 8:

            return "critical"

        if frequency >= 5:

            return "high"

        if frequency >= 3:

            return "medium"

        return "low"

    # ==================================================
    # BUILD GAP
    # ==================================================

    def build_gap(
        self,
        gap,
        frequency=0,
    ):

        """
        Build structured gap object.
        """

        priority = (
            self.calculate_gap_priority(
                frequency
            )
        )

        return {

            "gap": gap,

            "frequency": (
                frequency
            ),

            "priority": (
                priority
            ),
        }

    # ==================================================
    # FIND GAPS
    # ==================================================

    def find_gaps(
        self,
        content_analysis,
        structure_analysis,
    ):

        """
        Detect competitor content gaps.
        """

        competitor_logger.info(
            "Starting gap analysis"
        )

        # ==========================================
        # GAP STORAGE
        # ==========================================

        content_gaps = []

        # ==========================================
        # EXTRACT DATA
        # ==========================================

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

        average_word_count = (
            content_analysis.get(
                "average_word_count",
                0
            )
        )

        common_sections = (
            structure_analysis.get(
                "common_sections",
                []
            )
        )

        section_frequency = (
            structure_analysis.get(
                "section_frequency",
                {}
            )
        )

        # ==========================================
        # NORMALIZE DATA
        # ==========================================

        normalized_headings = (
            self.normalize_sections(
                common_headings
            )
        )

        normalized_sections = (
            self.normalize_sections(
                common_sections
            )
        )

        # ==========================================
        # FAQ GAP
        # ==========================================

        faq_frequency = (
            section_frequency.get(
                "faq",
                0
            )
        )

        if not self.section_exists(

            "faq",

            normalized_sections,
        ):

            content_gaps.append(

                self.build_gap(

                    gap=(
                        "Most competitors "
                        "are missing FAQ sections."
                    ),

                    frequency=(
                        faq_frequency
                    ),
                )
            )

        # ==========================================
        # CONCLUSION GAP
        # ==========================================

        conclusion_frequency = (
            section_frequency.get(
                "conclusion",
                0
            )
        )

        if not self.section_exists(

            "conclusion",

            normalized_sections,
        ):

            content_gaps.append(

                self.build_gap(

                    gap=(
                        "Many competitors "
                        "do not include "
                        "strong conclusions."
                    ),

                    frequency=(
                        conclusion_frequency
                    ),
                )
            )

        # ==========================================
        # BUYING GUIDE GAP
        # ==========================================

        buying_guide_frequency = (
            section_frequency.get(
                "buying guide",
                0
            )
        )

        if not self.section_exists(

            "buying guide",

            normalized_sections,
        ):

            content_gaps.append(

                self.build_gap(

                    gap=(
                        "Buying guide content "
                        "opportunity detected."
                    ),

                    frequency=(
                        buying_guide_frequency
                    ),
                )
            )

        # ==========================================
        # LOW CONTENT DEPTH
        # ==========================================

        if average_word_count < (
            Config.IDEAL_CONTENT_WORDS
        ):

            content_gaps.append(

                self.build_gap(

                    gap=(
                        "Competitor articles "
                        "have relatively low "
                        "content depth."
                    ),

                    frequency=5,
                )
            )

        # ==========================================
        # ADVANCED CONTENT GAPS
        # ==========================================

        for pattern in (
            self.ADVANCED_PATTERNS
        ):

            pattern_frequency = (
                heading_frequency.get(
                    pattern,
                    0
                )
            )

            if not self.section_exists(

                pattern,

                normalized_headings,
            ):

                content_gaps.append(

                    self.build_gap(

                        gap=(
                            f"Missing advanced "
                            f"section: "
                            f"{pattern.title()}"
                        ),

                        frequency=(
                            pattern_frequency
                        ),
                    )
                )

        # ==========================================
        # REMOVE DUPLICATES
        # ==========================================

        unique_gaps = []

        seen = set()

        for gap in content_gaps:

            gap_name = gap.get(
                "gap",
                ""
            )

            if gap_name in seen:

                continue

            seen.add(
                gap_name
            )

            unique_gaps.append(
                gap
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

        unique_gaps.sort(

            key=lambda x: (

                priority_order.get(

                    x.get(
                        "priority",
                        "low"
                    ),

                    1,
                ),

                x.get(
                    "frequency",
                    0
                ),
            ),

            reverse=True,
        )

        # ==========================================
        # GAP SCORE
        # ==========================================

        raw_gap_score = (

            len(unique_gaps) * 10
        )

        gap_score = (
            ScoringHelpers.normalize_score(
                raw_gap_score
            )
        )

        # ==========================================
        # GAP OPPORTUNITY LEVEL
        # ==========================================

        opportunity_level = (
            ScoringHelpers.confidence_level(
                gap_score
            )
        )

        competitor_logger.info(

            f"Gap analysis completed "
            f"with {len(unique_gaps)} gaps"
        )

        # ==========================================
        # RETURN RESULT
        # ==========================================

        return {

            "total_gaps": len(
                unique_gaps
            ),

            "gap_score": (
                gap_score
            ),

            "opportunity_level": (
                opportunity_level
            ),

            "content_gaps": (
                unique_gaps
            ),
        }