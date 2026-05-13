"""
Content quality scoring engine.
"""

import re


class ContentScorer:

    @staticmethod
    def word_count(
        content,
    ):

        return len(
            content.split()
        )

    @staticmethod
    def heading_score(
        content,
    ):

        headings = re.findall(

            r"^#+\s",

            content,

            re.MULTILINE,
        )

        if len(headings) >= 3:

            return 100

        if len(headings) >= 1:

            return 70

        return 30

    @staticmethod
    def readability_score(
        content,
    ):

        sentences = re.split(

            r"[.!?]",

            content,
        )

        sentence_count = max(

            len(sentences),

            1,
        )

        words = content.split()

        word_count = max(

            len(words),

            1,
        )

        avg_sentence_length = (

            word_count / sentence_count
        )

        if avg_sentence_length <= 14:

            return 95

        if avg_sentence_length <= 20:

            return 80

        if avg_sentence_length <= 30:

            return 60

        return 40

    @staticmethod
    def seo_score(
        content,
    ):

        score = 0

        if "# " in content:

            score += 25

        if "## " in content:

            score += 25

        if len(content.split()) > 300:

            score += 25

        if "-" in content or "*" in content:

            score += 25

        return score

    @staticmethod
    def ai_risk_score(
        content,
    ):

        robotic_phrases = [

            "in conclusion",

            "as an ai",

            "overall",

            "furthermore",

            "moreover",
        ]

        risk = 0

        content_lower = (
            content.lower()
        )

        for phrase in robotic_phrases:

            if phrase in content_lower:

                risk += 20

        return min(
            risk,
            100,
        )

    @classmethod
    def score(
        cls,
        content,
    ):

        return {

            "word_count": (
                cls.word_count(
                    content
                )
            ),

            "heading_score": (
                cls.heading_score(
                    content
                )
            ),

            "readability_score": (
                cls.readability_score(
                    content
                )
            ),

            "seo_score": (
                cls.seo_score(
                    content
                )
            ),

            "ai_risk_score": (
                cls.ai_risk_score(
                    content
                )
            ),
        }