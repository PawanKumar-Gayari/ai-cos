class ArticlePlanner:

    """
    Article structure planner.
    """

    def build(
        self,
        keyword,
        intent,
    ):

        sections = [

            "Introduction",

            "Key Insights",

            "Benefits",

            "Conclusion",
        ]

        if intent == "commercial":

            sections = [

                "Introduction",

                "Top Recommendations",

                "Comparison Table",

                "Pros and Cons",

                "Buyer Guide",

                "Conclusion",
            ]

        elif intent == "informational":

            sections = [

                "Introduction",

                "Step-by-Step Guide",

                "Examples",

                "Common Mistakes",

                "FAQs",

                "Conclusion",
            ]

        return {

            "keyword": keyword,

            "intent": intent,

            "sections": sections,
        }