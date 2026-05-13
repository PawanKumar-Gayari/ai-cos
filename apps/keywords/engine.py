"""
Main keyword intelligence engine.
"""

from apps.keywords.services.intent_service import (
    IntentService,
)

from apps.keywords.services.scoring_service import (
    ScoringService,
)


class KeywordEngine:

    def __init__(self):

        self.intent_service = (
            IntentService()
        )

        self.scoring_service = (
            ScoringService()
        )

    def analyze(
        self,
        keyword,
    ):

        """
        Analyze single keyword.
        """

        intent = (
            self.intent_service.detect_intent(
                keyword
            )
        )

        scoring = (
            self.scoring_service.calculate_score(
                keyword
            )
        )

        return {

            "keyword": keyword,

            "intent": intent,

            "difficulty": scoring.get(
                "difficulty",
                0,
            ),

            "volume": scoring.get(
                "volume",
                0,
            ),

            "score": scoring.get(
                "score",
                0,
            ),
        }

    def expand_keywords(
        self,
        topic,
    ):

        """
        Generate related SEO keywords.
        """

        base_keywords = [

            topic,

            f"best {topic}",

            f"{topic} guide",

            f"{topic} tips",

            f"{topic} tutorial",

            f"{topic} examples",

            f"{topic} strategy",

            f"{topic} checklist",
        ]

        results = []

        for keyword in base_keywords:

            results.append(

                self.analyze(
                    keyword
                )
            )

        return results

    def best_keywords(
        self,
        topic,
        limit=5,
    ):

        """
        Return highest scoring keywords.
        """

        keywords = (
            self.expand_keywords(
                topic
            )
        )

        sorted_keywords = sorted(

            keywords,

            key=lambda item: item.get(
                "score",
                0,
            ),

            reverse=True,
        )

        return sorted_keywords[:limit]