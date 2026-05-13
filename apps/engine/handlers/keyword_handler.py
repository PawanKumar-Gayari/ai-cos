"""
Keyword pipeline handler.
"""

from apps.keywords.engine import (
    KeywordEngine,
)


class KeywordHandler:

    def __init__(self):

        # =========================
        # KEYWORD ENGINE
        # =========================

        self.keyword_engine = (
            KeywordEngine()
        )

    def execute(
        self,
        keyword
    ):

        # =========================
        # ANALYZE KEYWORD
        # =========================

        return (
            self.keyword_engine.analyze(
                keyword
            )
        )