"""
Context builder.
"""


class ContextBuilder:

    def build(
        self,
        query,
        retrieval_results,
    ):

        """
        Build contextual memory payload.
        """

        context_items = []

        for item in retrieval_results:

            metadata = item.get(
                "metadata",
                {}
            )

            title = metadata.get(
                "title",
                "Untitled"
            )

            score = item.get(
                "score",
                0
            )

            context_items.append({

                "title": title,

                "score": score,
            })

        return {

            "query": query,

            "context": context_items,
        }

    def build_prompt_context(
        self,
        context_data,
    ):

        """
        Convert context into AI prompt text.
        """

        query = context_data["query"]

        context = context_data["context"]

        lines = [

            f"User Query: {query}",

            "",

            "Relevant Memory:",
        ]

        for item in context:

            lines.append(

                f"- {item['title']} "
                f"(score: {item['score']:.2f})"
            )

        return "\n".join(lines)