"""
Keyword intent detection service.
"""

import re

from apps.keywords.constants import (

    INTENT_COMMERCIAL,

    INTENT_INFORMATIONAL,

    INTENT_NAVIGATIONAL,

    INTENT_TRANSACTIONAL,
)


class IntentService:

    def contains_word(
        self,
        text,
        words,
    ):

        """
        Match whole words only.
        """

        for word in words:

            pattern = (
                rf"\b{re.escape(word)}\b"
            )

            if re.search(
                pattern,
                text,
            ):

                return True

        return False

    def detect_intent(
        self,
        keyword,
    ):

        """
        Detect keyword search intent.
        """

        keyword = keyword.lower()

        # ==========================================
        # TRANSACTIONAL
        # ==========================================

        transactional_words = [

            "buy",

            "price",

            "deal",

            "discount",

            "coupon",

            "purchase",
        ]

        # ==========================================
        # COMMERCIAL
        # ==========================================

        commercial_words = [

            "best",

            "top",

            "review",

            "vs",

            "comparison",

            "alternative",
        ]

        # ==========================================
        # NAVIGATIONAL
        # ==========================================

        navigational_words = [

            "login",

            "website",

            "official",

            "homepage",
        ]

        # ==========================================
        # DETECTION
        # ==========================================

        if self.contains_word(

            keyword,

            transactional_words,
        ):

            return (
                INTENT_TRANSACTIONAL
            )

        if self.contains_word(

            keyword,

            commercial_words,
        ):

            return (
                INTENT_COMMERCIAL
            )

        if self.contains_word(

            keyword,

            navigational_words,
        ):

            return (
                INTENT_NAVIGATIONAL
            )

        return (
            INTENT_INFORMATIONAL
        )