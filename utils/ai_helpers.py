"""
Central AI helper utilities.
"""

import re


class AIHelpers:

    # =========================
    # CLEAN PROMPT
    # =========================

    @classmethod
    def clean_prompt(
        cls,
        prompt
    ):

        if not prompt:

            return ""

        # =========================
        # REMOVE EXTRA SPACES
        # =========================

        prompt = " ".join(
            prompt.split()
        )

        return prompt.strip()

    # =========================
    # ESTIMATE TOKENS
    # =========================

    @classmethod
    def estimate_tokens(
        cls,
        text
    ):

        if not text:

            return 0

        # =========================
        # SIMPLE TOKEN ESTIMATION
        # =========================

        return int(

            len(text.split()) * 1.3
        )

    # =========================
    # REMOVE MARKDOWN
    # =========================

    @classmethod
    def remove_markdown(
        cls,
        text
    ):

        if not text:

            return ""

        # =========================
        # REMOVE CODE BLOCKS
        # =========================

        text = re.sub(

            r"```.*?```",

            "",

            text,

            flags=re.DOTALL
        )

        # =========================
        # REMOVE INLINE MARKDOWN
        # =========================

        text = re.sub(

            r"[*_#>`\-]",

            "",

            text
        )

        return text.strip()

    # =========================
    # CLEAN AI RESPONSE
    # =========================

    @classmethod
    def clean_ai_response(
        cls,
        text
    ):

        if not text:

            return ""

        # =========================
        # REMOVE MARKDOWN
        # =========================

        text = cls.remove_markdown(
            text
        )

        # =========================
        # REMOVE EXTRA SPACES
        # =========================

        text = " ".join(
            text.split()
        )

        return text.strip()

    # =========================
    # FORMAT FALLBACK RESPONSE
    # =========================

    @classmethod
    def fallback_response(
        cls,
        keyword
    ):

        return (

            f"Content generation temporarily unavailable for '{keyword}'. "
            f"Fallback system activated."
        )

    # =========================
    # FORMAT AI ERROR
    # =========================

    @classmethod
    def format_ai_error(
        cls,
        provider,
        error
    ):

        return {

            "provider": provider,

            "success": False,

            "error": str(error),
        }

    # =========================
    # DETECT EMPTY RESPONSE
    # =========================

    @classmethod
    def is_response_empty(
        cls,
        response
    ):

        if not response:

            return True

        cleaned = response.strip()

        return len(cleaned) == 0

    # =========================
    # TRUNCATE TEXT
    # =========================

    @classmethod
    def truncate_text(
        cls,
        text,
        max_length=500
    ):

        if not text:

            return ""

        if len(text) <= max_length:

            return text

        return (

            text[:max_length]
            + "..."
        )