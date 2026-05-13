"""
Central text cleaning utility.
"""

import re


class TextCleaner:

    # =========================
    # REMOVE EXTRA WHITESPACES
    # =========================

    @classmethod
    def clean_spaces(
        cls,
        text
    ):

        if not text:

            return ""

        return " ".join(
            text.split()
        )

    # =========================
    # REMOVE EXTRA NEWLINES
    # =========================

    @classmethod
    def clean_newlines(
        cls,
        text
    ):

        if not text:

            return ""

        return re.sub(

            r"\n+",

            "\n",

            text
        )

    # =========================
    # REMOVE HTML TAGS
    # =========================

    @classmethod
    def remove_html(
        cls,
        text
    ):

        if not text:

            return ""

        return re.sub(

            r"<.*?>",

            "",

            text
        )

    # =========================
    # REMOVE SPECIAL CHARACTERS
    # =========================

    @classmethod
    def remove_special_characters(
        cls,
        text
    ):

        if not text:

            return ""

        return re.sub(

            r"[^a-zA-Z0-9\s\.\,\-\_\!\?]",

            "",

            text
        )

    # =========================
    # LOWERCASE TEXT
    # =========================

    @classmethod
    def to_lowercase(
        cls,
        text
    ):

        if not text:

            return ""

        return text.lower()

    # =========================
    # FULL TEXT CLEANING PIPELINE
    # =========================

    @classmethod
    def clean(
        cls,
        text,
        lowercase=False,
        remove_html=True,
        remove_special_chars=False
    ):

        if not text:

            return ""

        # =========================
        # REMOVE HTML
        # =========================

        if remove_html:

            text = cls.remove_html(
                text
            )

        # =========================
        # REMOVE SPECIAL CHARS
        # =========================

        if remove_special_chars:

            text = (
                cls.remove_special_characters(
                    text
                )
            )

        # =========================
        # CLEAN NEWLINES
        # =========================

        text = cls.clean_newlines(
            text
        )

        # =========================
        # CLEAN SPACES
        # =========================

        text = cls.clean_spaces(
            text
        )

        # =========================
        # LOWERCASE
        # =========================

        if lowercase:

            text = cls.to_lowercase(
                text
            )

        # =========================
        # RETURN CLEANED TEXT
        # =========================

        return text