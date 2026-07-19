"""
Production AI Response Cleaner
------------------------------

Enterprise-grade AI response cleanup engine.

Features:
- AI phrase removal
- markdown normalization
- duplicate heading cleanup
- malformed markdown fixes
- table cleanup
- spacing normalization
- AI spam cleanup
- SEO-safe formatting
- production-ready architecture
"""

from __future__ import annotations

import re


class ResponseCleaner:

    """
    Enterprise AI response cleaner.
    """

    MULTI_SPACE_PATTERN = re.compile(
        r"[ \t]+"
    )

    MULTI_NEWLINE_PATTERN = re.compile(
        r"\n{3,}"
    )

    DUPLICATE_HEADING_PATTERN = re.compile(
        r"^(#+)\s+(.*?)\n(?:\1\s+\2\n)+",
        re.MULTILINE,
    )

    BROKEN_HEADER_PATTERN = re.compile(
        r"#+\s*#"
    )

    # =============================================
    # REMOVE AI PHRASES
    # =============================================

    @classmethod
    def remove_ai_phrases(
        cls,
        content,
    ):

        unwanted_phrases = [

            "As an AI language model,",

            "As an AI assistant,",

            "Here is your answer:",

            "Sure, here's",

            "Certainly!",

            "Of course!",

            "I hope this helps!",

            "Let me know if you need anything else.",

            "In conclusion,",

            "Overall,",

            "Furthermore,",

            "Moreover,",

            "It is important to note that",

            "Delve into",

            "Unlock the power of",
        ]

        for phrase in unwanted_phrases:

            content = re.sub(

                re.escape(phrase),

                "",

                content,

                flags=re.IGNORECASE,
            )

        return content

    # =============================================
    # NORMALIZE SPACING
    # =============================================

    @classmethod
    def normalize_spacing(
        cls,
        content,
    ):

        content = (

            cls.MULTI_NEWLINE_PATTERN
            .sub(

                "\n\n",

                content,
            )
        )

        content = (

            cls.MULTI_SPACE_PATTERN
            .sub(

                " ",

                content,
            )
        )

        return content

    # =============================================
    # CLEAN HEADINGS
    # =============================================

    @classmethod
    def clean_headings(
        cls,
        content,
    ):

        # =========================================
        # FIX BROKEN HEADERS
        # =========================================

        content = (

            cls.BROKEN_HEADER_PATTERN
            .sub(

                "#",

                content,
            )
        )

        # =========================================
        # REMOVE DUPLICATE HEADINGS
        # =========================================

        content = (

            cls.DUPLICATE_HEADING_PATTERN
            .sub(

                r"\1 \2\n",

                content,
            )
        )

        # =========================================
        # REMOVE EMPTY HEADINGS
        # =========================================

        content = re.sub(

            r"^#{1,6}\s*$",

            "",

            content,

            flags=re.MULTILINE,
        )

        return content

    # =============================================
    # FIX MARKDOWN TABLES
    # =============================================

    @classmethod
    def clean_tables(
        cls,
        content,
    ):

        lines = content.splitlines()

        cleaned_lines = []

        for line in lines:

            # =====================================
            # FIX TABLE SPACING
            # =====================================

            if "|" in line:

                line = re.sub(

                    r"\s*\|\s*",

                    " | ",

                    line,
                )

                line = re.sub(

                    r"\|{2,}",

                    "|",

                    line,
                )

            cleaned_lines.append(
                line
            )

        return "\n".join(
            cleaned_lines
        )

    # =============================================
    # REMOVE REPEATED PARAGRAPHS
    # =============================================

    @classmethod
    def remove_repetition(
        cls,
        content,
    ):

        paragraphs = [

            p.strip()

            for p in content.split("\n\n")

            if p.strip()
        ]

        unique = []

        seen = set()

        for paragraph in paragraphs:

            normalized = (
                paragraph.lower()
            )

            if normalized in seen:

                continue

            seen.add(
                normalized
            )

            unique.append(
                paragraph
            )

        return "\n\n".join(
            unique
        )

    # =============================================
    # CLEAN BULLETS
    # =============================================

    @classmethod
    def clean_bullets(
        cls,
        content,
    ):

        content = re.sub(

            r"^[•●]\s*",

            "- ",

            content,

            flags=re.MULTILINE,
        )

        return content

    # =============================================
    # FIX MARKDOWN STRUCTURE
    # =============================================

    @classmethod
    def fix_markdown_structure(
        cls,
        content,
    ):

        # =========================================
        # ENSURE SPACE AFTER #
        # =========================================

        content = re.sub(

            r"^(#{1,6})([^#\s])",

            r"\1 \2",

            content,

            flags=re.MULTILINE,
        )

        # =========================================
        # FIX MULTIPLE H1
        # =========================================

        h1_matches = re.findall(

            r"^#\s.+",

            content,

            re.MULTILINE,
        )

        if len(h1_matches) > 1:

            first = True

            lines = []

            for line in content.splitlines():

                if re.match(

                    r"^#\s.+",

                    line,
                ):

                    if first:

                        first = False

                    else:

                        line = re.sub(

                            r"^#\s",

                            "## ",

                            line,
                        )

                lines.append(
                    line
                )

            content = "\n".join(
                lines
            )

        return content

    # =============================================
    # FINAL CLEAN
    # =============================================

    @classmethod
    def final_cleanup(
        cls,
        content,
    ):

        # remove trailing spaces
        content = "\n".join(

            line.rstrip()

            for line in content.splitlines()
        )

        # remove excessive separators
        content = re.sub(

            r"\n[-=]{5,}\n",

            "\n",

            content,
        )

        return content.strip()

    # =============================================
    # CLEAN
    # =============================================

    @classmethod
    def clean(
        cls,
        content,
    ):

        if not content:

            return ""

        # =========================================
        # AI PHRASES
        # =========================================

        content = (
            cls.remove_ai_phrases(
                content
            )
        )

        # =========================================
        # REPETITION
        # =========================================

        content = (
            cls.remove_repetition(
                content
            )
        )

        # =========================================
        # MARKDOWN
        # =========================================

        content = (
            cls.clean_headings(
                content
            )
        )

        content = (
            cls.fix_markdown_structure(
                content
            )
        )

        # =========================================
        # TABLES
        # =========================================

        content = (
            cls.clean_tables(
                content
            )
        )

        # =========================================
        # BULLETS
        # =========================================

        content = (
            cls.clean_bullets(
                content
            )
        )

        # =========================================
        # SPACING
        # =========================================

        content = (
            cls.normalize_spacing(
                content
            )
        )

        # =========================================
        # FINAL
        # =========================================

        content = (
            cls.final_cleanup(
                content
            )
        )

        return content