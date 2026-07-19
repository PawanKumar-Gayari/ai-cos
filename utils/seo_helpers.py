"""
Central SEO helper utilities.
"""

import re


class SEOHelpers:

    # =========================
    # GENERATE SEO SLUG
    # =========================

    @classmethod
    def generate_slug(
        cls,
        text
    ):

        if not text:

            return ""

        # =========================
        # LOWERCASE
        # =========================

        text = text.lower()

        # =========================
        # REMOVE SPECIAL CHARS
        # =========================

        text = re.sub(

            r"[^a-z0-9\s-]",

            "",

            text
        )

        # =========================
        # REPLACE SPACES
        # =========================

        text = re.sub(

            r"\s+",

            "-",

            text
        )

        # =========================
        # REMOVE EXTRA DASHES
        # =========================

        text = re.sub(

            r"-+",

            "-",

            text
        )

        return text.strip("-")

    # =========================
    # TITLE LENGTH CHECK
    # =========================

    @classmethod
    def is_title_length_valid(
        cls,
        title
    ):

        length = len(
            title
        )

        return 30 <= length <= 60

    # =========================
    # META DESCRIPTION CHECK
    # =========================

    @classmethod
    def is_meta_description_valid(
        cls,
        meta_description
    ):

        length = len(
            meta_description
        )

        return 120 <= length <= 160

    # =========================
    # KEYWORD DENSITY
    # =========================

    @classmethod
    def keyword_density(
        cls,
        content,
        keyword
    ):

        if not content or not keyword:

            return 0

        content_lower = (
            content.lower()
        )

        keyword_lower = (
            keyword.lower()
        )

        keyword_count = (
            content_lower.count(
                keyword_lower
            )
        )

        total_words = len(

            content_lower.split()
        )

        if total_words == 0:

            return 0

        density = (

            keyword_count / total_words
        ) * 100

        return round(
            density,
            2
        )

    # =========================
    # CHECK KEYWORD IN TITLE
    # =========================

    @classmethod
    def keyword_in_title(
        cls,
        keyword,
        title
    ):

        return (
            keyword.lower()
            in title.lower()
        )

    # =========================
    # CHECK KEYWORD IN META
    # =========================

    @classmethod
    def keyword_in_meta(
        cls,
        keyword,
        meta_description
    ):

        return (
            keyword.lower()
            in meta_description.lower()
        )

    # =========================
    # HEADING SCORE
    # =========================

    @classmethod
    def heading_score(
        cls,
        headings
    ):

        if not headings:

            return 0

        total = len(
            headings
        )

        if total >= 10:

            return 100

        elif total >= 7:

            return 80

        elif total >= 5:

            return 60

        elif total >= 3:

            return 40

        return 20

    # =========================
    # BASIC SEO SCORE
    # =========================

    @classmethod
    def calculate_basic_seo_score(
        cls,
        title,
        meta_description,
        content,
        keyword,
        headings
    ):

        score = 0

        # =========================
        # TITLE
        # =========================

        if cls.is_title_length_valid(
            title
        ):

            score += 20

        if cls.keyword_in_title(
            keyword,
            title
        ):

            score += 20

        # =========================
        # META
        # =========================

        if cls.is_meta_description_valid(
            meta_description
        ):

            score += 15

        if cls.keyword_in_meta(
            keyword,
            meta_description
        ):

            score += 15

        # =========================
        # KEYWORD DENSITY
        # =========================

        density = cls.keyword_density(

            content,

            keyword
        )

        if 0.5 <= density <= 2.5:

            score += 15

        # =========================
        # HEADING SCORE
        # =========================

        score += int(

            cls.heading_score(
                headings
            ) * 0.15
        )

        return min(
            score,
            100
        )