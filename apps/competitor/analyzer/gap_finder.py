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

        if not self.section_exists(

            "faq",

            normalized_sections,
        ):

            content_gaps.append(

                "Most competitors are missing FAQ sections."
            )

        # ==========================================
        # CONCLUSION GAP
        # ==========================================

        if not self.section_exists(

            "conclusion",

            normalized_sections,
        ):

            content_gaps.append(

                "Many competitors do not include strong conclusions."
            )

        # ==========================================
        # BUYING GUIDE GAP
        # ==========================================

        if not self.section_exists(

            "buying guide",

            normalized_sections,
        ):

            content_gaps.append(

                "Buying guide content opportunity detected."
            )

        # ==========================================
        # LOW CONTENT DEPTH
        # ==========================================

        if average_word_count < (
            Config.IDEAL_CONTENT_WORDS
        ):

            content_gaps.append(

                "Competitor articles have relatively low content depth."
            )

        # ==========================================
        # ADVANCED CONTENT GAPS
        # ==========================================

        for pattern in (
            self.ADVANCED_PATTERNS
        ):

            if not self.section_exists(

                pattern,

                normalized_headings,
            ):

                content_gaps.append(

                    f"Missing advanced section: {pattern.title()}"
                )

        # ==========================================
        # REMOVE DUPLICATES
        # ==========================================

        unique_gaps = (
            Helpers.unique_list(
                content_gaps
            )
        )

        unique_gaps.sort()

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