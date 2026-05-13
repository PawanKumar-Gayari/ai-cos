"""
Keyword analysis service.
"""


class KeywordService:

    def analyze(self, keyword):

        return {
            "keyword": keyword,
            "intent": "informational",
            "difficulty": "medium",
            "volume": 1200,
        }