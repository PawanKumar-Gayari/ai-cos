"""
AI response cleaner.
"""

import re


class ResponseCleaner:

    @staticmethod
    def clean(
        content,
    ):

        if not content:

            return ""

        # ==========================================
        # REMOVE COMMON AI PHRASES
        # ==========================================

        unwanted_phrases = [

            "As an AI language model,",

            "As an AI assistant,",

            "Here is your answer:",

            "Sure, here's",

            "Certainly!",

            "Of course!",

            "I hope this helps!",

            "Let me know if you need anything else.",
        ]

        for phrase in unwanted_phrases:

            content = content.replace(
                phrase,
                "",
            )

        # ==========================================
        # REMOVE EXTRA BLANK LINES
        # ==========================================

        content = re.sub(

            r"\n{3,}",

            "\n\n",

            content,
        )

        # ==========================================
        # REMOVE MULTIPLE SPACES
        # ==========================================

        content = re.sub(

            r"[ \t]+",

            " ",

            content,
        )

        # ==========================================
        # CLEAN MARKDOWN HEADERS
        # ==========================================

        content = re.sub(

            r"#+\s*#",

            "#",

            content,
        )

        # ==========================================
        # FINAL STRIP
        # ==========================================

        return content.strip()