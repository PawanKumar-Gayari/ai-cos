"""
Competitor structure analyzer.
"""

from collections import Counter

from utils.helpers import (
    Helpers,
)

from utils.text_cleaner import (
    TextCleaner,
)

from utils.scoring_helpers import (
    ScoringHelpers,
)

from utils.logger import (
    competitor_logger,
)


class StructureAnalyzer:

    RECOMMENDED_STRUCTURE = [

        "Introduction",

        "Features",

        "Benefits",

        "Comparison",

        "Pros and Cons",

        "Case Study",

        "Expert Tips",

        "FAQ",

        "Conclusion",
    ]

    # ==================================================
    # CLEAN SECTIONS
    # ==================================================

    def clean_sections(
        self,
        headings,
    ):

        """
        Clean and normalize headings.
        """

        cleaned = []

        for heading in headings:

            cleaned_heading = (
                TextCleaner.clean(
                    heading
                )
            )

            if not cleaned_heading:

                continue

            cleaned_heading = (
                cleaned_heading.strip()
            )

            cleaned.append(
                cleaned_heading
            )

        return cleaned

    # ==================================================
    # STRUCTURE DEPTH SCORE
    # ==================================================

    def calculate_structure_depth(
        self,
        average_sections,
    ):

        """
        Calculate structure depth score.
        """

        if average_sections >= 10:

            return 100

        if average_sections >= 7:

            return 80

        if average_sections >= 5:

            return 60

        return 40

    # ==================================================
    # SECTION FREQUENCY
    # ==================================================

    def calculate_section_frequency(
        self,
        sections,
    ):

        """
        Calculate section frequency.
        """

        normalized = []

        for section in sections:

            cleaned = (
                str(section)
                .strip()
                .lower()
            )

            if cleaned:

                normalized.append(
                    cleaned
                )

        counter = Counter(
            normalized
        )

        return dict(
            counter.most_common(25)
        )

    # ==================================================
    # STRUCTURE COMPLEXITY
    # ==================================================

    def calculate_structure_complexity(
        self,
        structures,
    ):

        """
        Estimate structure complexity.
        """

        if not structures:

            return 0

        total_sections = 0

        for structure in structures:

            total_sections += (
                structure.get(
                    "total_sections",
                    0
                )
            )

        average_complexity = (
            total_sections
            / len(structures)
        )

        return round(
            average_complexity,
            2,
        )

    # ==================================================
    # ANALYZE
    # ==================================================

    def analyze(
        self,
        serp_results,
    ):

        """
        Analyze competitor structure quality.
        """

        # ==========================================
        # EXTRACT RESULTS
        # ==========================================

        results = serp_results.get(
            "results",
            []
        )

        competitor_logger.info(

            f"Starting structure analysis "
            f"for {len(results)} competitors"
        )

        # ==========================================
        # EMPTY RESULTS SAFETY
        # ==========================================

        if not results:

            competitor_logger.warning(

                "No competitor results found "
                "for structure analysis."
            )

            return {

                "total_competitors": 0,

                "average_sections": 0,

                "average_structure_depth": 0,

                "structure_depth_score": 0,

                "common_sections": [],

                "section_frequency": {},

                "recommended_structure": [],

                "structures": [],
            }

        # ==========================================
        # ANALYSIS STORAGE
        # ==========================================

        section_counts = []

        all_sections = []

        structures = []

        # ==========================================
        # PROCESS RESULTS
        # ==========================================

        for result in results:

            # --------------------------------------
            # TITLE
            # --------------------------------------

            title = (
                TextCleaner.clean(
                    result.get(
                        "title",
                        ""
                    )
                )
            )

            # --------------------------------------
            # HEADINGS
            # --------------------------------------

            headings = result.get(
                "headings",
                []
            )

            # --------------------------------------
            # CLEAN HEADINGS
            # --------------------------------------

            cleaned_headings = (
                self.clean_sections(
                    headings
                )
            )

            # --------------------------------------
            # NORMALIZED HEADINGS
            # --------------------------------------

            normalized_headings = [

                heading.lower()

                for heading in (
                    cleaned_headings
                )
            ]

            # --------------------------------------
            # SECTION COUNT
            # --------------------------------------

            section_count = len(
                cleaned_headings
            )

            section_counts.append(
                section_count
            )

            # --------------------------------------
            # COLLECT SECTIONS
            # --------------------------------------

            all_sections.extend(
                normalized_headings
            )

            # --------------------------------------
            # STRUCTURE SCORE
            # --------------------------------------

            structure_score = (
                ScoringHelpers.normalize_score(

                    section_count * 15
                )
            )

            # --------------------------------------
            # STRUCTURE DATA
            # --------------------------------------

            structures.append({

                "title": title,

                "total_sections": (
                    section_count
                ),

                "structure_score": (
                    structure_score
                ),

                "sections": (
                    cleaned_headings
                ),
            })

        # ==========================================
        # AVERAGE SECTIONS
        # ==========================================

        average_sections = (
            ScoringHelpers.average_score(
                section_counts
            )
        )

        # ==========================================
        # STRUCTURE COMPLEXITY
        # ==========================================

        average_structure_depth = (
            self.calculate_structure_complexity(
                structures
            )
        )

        # ==========================================
        # SECTION FREQUENCY
        # ==========================================

        section_frequency = (
            self.calculate_section_frequency(
                all_sections
            )
        )

        common_sections = list(
            section_frequency.keys()
        )

        # ==========================================
        # STRUCTURE DEPTH SCORE
        # ==========================================

        structure_depth_score = (
            self.calculate_structure_depth(
                average_sections
            )
        )

        structure_depth_score = (
            ScoringHelpers.normalize_score(
                structure_depth_score
            )
        )

        # ==========================================
        # RECOMMENDED STRUCTURE
        # ==========================================

        recommended_structure = (
            Helpers.unique_list(

                self.RECOMMENDED_STRUCTURE
            )
        )

        recommended_structure.sort()

        competitor_logger.info(

            f"Structure analysis completed "
            f"with average sections: "
            f"{average_sections}"
        )

        # ==========================================
        # RETURN ANALYSIS
        # ==========================================

        return {

            "total_competitors": len(
                results
            ),

            "average_sections": (
                average_sections
            ),

            "average_structure_depth": (
                average_structure_depth
            ),

            "structure_depth_score": (
                structure_depth_score
            ),

            "common_sections": (
                common_sections
            ),

            "section_frequency": (
                section_frequency
            ),

            "recommended_structure": (
                recommended_structure
            ),

            "structures": (
                structures
            ),
        }