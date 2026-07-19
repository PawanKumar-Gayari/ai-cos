"""
Competitor content analyzer.
"""

import re

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


class ContentAnalyzer:

    TITLE_PATTERNS = [

        "best",

        "review",

        "comparison",

        "top",

        "guide",

        "tutorial",

        "tips",

        "vs",
    ]

    # ==================================================
    # TITLE PATTERN DETECTION
    # ==================================================

    def detect_title_patterns(
        self,
        title,
    ):

        """
        Detect SEO title patterns.
        """

        detected = []

        lowered_title = (
            title.lower()
        )

        for pattern in (
            self.TITLE_PATTERNS
        ):

            regex_pattern = (
                rf"\b{re.escape(pattern)}\b"
            )

            if re.search(

                regex_pattern,

                lowered_title,
            ):

                detected.append(
                    pattern
                )

        return detected

    # ==================================================
    # CLEAN HEADINGS
    # ==================================================

    def clean_headings(
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
    # HEADING FREQUENCY
    # ==================================================

    def calculate_heading_frequency(
        self,
        headings,
    ):

        """
        Calculate heading frequency.
        """

        normalized = []

        for heading in headings:

            cleaned = (
                str(heading)
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
            counter.most_common(20)
        )

    # ==================================================
    # TITLE PATTERN FREQUENCY
    # ==================================================

    def calculate_pattern_frequency(
        self,
        patterns,
    ):

        """
        Calculate SEO title pattern frequency.
        """

        normalized = []

        for pattern in patterns:

            cleaned = (
                str(pattern)
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
            counter.most_common(20)
        )

    # ==================================================
    # ANALYZE
    # ==================================================

    def analyze(
        self,
        serp_results,
    ):

        """
        Analyze competitor content quality.
        """

        # ==========================================
        # EXTRACT RESULTS
        # ==========================================

        results = serp_results.get(
            "results",
            []
        )

        competitor_logger.info(

            f"Starting content analysis "
            f"for {len(results)} competitors"
        )

        # ==========================================
        # EMPTY RESULTS SAFETY
        # ==========================================

        if not results:

            competitor_logger.warning(

                "No competitor results found "
                "for content analysis."
            )

            return {

                "total_competitors": 0,

                "average_word_count": 0,

                "content_depth_score": 0,

                "common_headings": [],

                "heading_frequency": {},

                "title_patterns": [],

                "title_pattern_frequency": {},

                "analyzed_results": [],
            }

        # ==========================================
        # ANALYSIS STORAGE
        # ==========================================

        word_counts = []

        all_headings = []

        title_patterns = []

        analyzed_results = []

        # ==========================================
        # PROCESS RESULTS
        # ==========================================

        for result in results:

            # --------------------------------------
            # BASIC DATA
            # --------------------------------------

            title = (
                TextCleaner.clean(
                    result.get(
                        "title",
                        ""
                    )
                )
            )

            word_count = int(
                result.get(
                    "word_count",
                    0
                ) or 0
            )

            headings = result.get(
                "headings",
                []
            )

            # --------------------------------------
            # STORE WORD COUNT
            # --------------------------------------

            word_counts.append(
                word_count
            )

            # --------------------------------------
            # CLEAN HEADINGS
            # --------------------------------------

            cleaned_headings = (
                self.clean_headings(
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
            # COLLECT HEADINGS
            # --------------------------------------

            all_headings.extend(
                normalized_headings
            )

            # --------------------------------------
            # TITLE PATTERN ANALYSIS
            # --------------------------------------

            detected_patterns = (
                self.detect_title_patterns(
                    title
                )
            )

            title_patterns.extend(
                detected_patterns
            )

            # --------------------------------------
            # HEADING SCORE
            # --------------------------------------

            heading_score = (
                ScoringHelpers.normalize_score(

                    len(cleaned_headings)
                    * 10
                )
            )

            # --------------------------------------
            # ANALYZED RESULT
            # --------------------------------------

            analyzed_results.append({

                "title": title,

                "word_count": (
                    word_count
                ),

                "total_headings": len(
                    cleaned_headings
                ),

                "heading_score": (
                    heading_score
                ),

                "title_patterns": (
                    detected_patterns
                ),
            })

        # ==========================================
        # AVERAGE WORD COUNT
        # ==========================================

        average_word_count = (
            ScoringHelpers.average_score(
                word_counts
            )
        )

        # ==========================================
        # HEADING FREQUENCY
        # ==========================================

        heading_frequency = (
            self.calculate_heading_frequency(
                all_headings
            )
        )

        common_headings = list(
            heading_frequency.keys()
        )

        # ==========================================
        # TITLE PATTERN FREQUENCY
        # ==========================================

        title_pattern_frequency = (
            self.calculate_pattern_frequency(
                title_patterns
            )
        )

        unique_patterns = list(
            title_pattern_frequency.keys()
        )

        # ==========================================
        # CONTENT DEPTH SCORE
        # ==========================================

        if average_word_count >= 4000:

            content_depth_score = 100

        elif average_word_count >= 3000:

            content_depth_score = 80

        elif average_word_count >= 2000:

            content_depth_score = 60

        else:

            content_depth_score = 40

        # ==========================================
        # NORMALIZE SCORE
        # ==========================================

        content_depth_score = (
            ScoringHelpers.normalize_score(
                content_depth_score
            )
        )

        competitor_logger.info(

            f"Content analysis completed "
            f"with average word count: "
            f"{average_word_count}"
        )

        # ==========================================
        # RETURN ANALYSIS
        # ==========================================

        return {

            "total_competitors": len(
                results
            ),

            "average_word_count": (
                average_word_count
            ),

            "content_depth_score": (
                content_depth_score
            ),

            "common_headings": (
                common_headings
            ),

            "heading_frequency": (
                heading_frequency
            ),

            "title_patterns": (
                unique_patterns
            ),

            "title_pattern_frequency": (
                title_pattern_frequency
            ),

            "analyzed_results": (
                analyzed_results
            ),
        }