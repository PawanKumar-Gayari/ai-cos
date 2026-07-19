"""
Context builder.
"""

import logging


logger = logging.getLogger(
    __name__
)


class ContextBuilder:

    MAX_CONTEXT_ITEMS = 3

    MAX_CONTEXT_LENGTH = 1200

    BLOCKED_PATTERNS = [

        "Task 1:",

        "Task 2:",

        "SEO optimization",

        "tutorial",

        "tips",

        "guide",

        "Context:",

        "User Query:",

        "Session Context:",

        "Relevant Memory:",
    ]

    # ==================================================
    # CLEAN TEXT
    # ==================================================

    def clean_text(
        self,
        text,
    ):

        """
        Remove noisy prompt patterns.
        """

        if not text:

            return ""

        text = str(
            text
        ).strip()

        for pattern in (
            self.BLOCKED_PATTERNS
        ):

            text = text.replace(
                pattern,
                ""
            )

        return text.strip()

    # ==================================================
    # SAFE SCORE
    # ==================================================

    def safe_score(
        self,
        score,
    ):

        try:

            return round(
                float(score),
                2,
            )

        except Exception:

            return 0.0

    # ==================================================
    # BUILD CONTEXT
    # ==================================================

    def build(
        self,
        query,
        retrieval_results,
    ):

        """
        Build clean contextual memory payload.
        """

        query = self.clean_text(
            query
        )

        context_items = []

        retrieval_results = (
            retrieval_results[
                :self.MAX_CONTEXT_ITEMS
            ]
        )

        for item in retrieval_results:

            metadata = item.get(
                "metadata",
                {}
            )

            if not isinstance(
                metadata,
                dict,
            ):

                metadata = {}

            title = metadata.get(
                "title",
                "Untitled"
            )

            title = self.clean_text(
                title
            )

            score = self.safe_score(

                item.get(
                    "score",
                    0
                )
            )

            if not title:

                continue

            context_items.append({

                "title": title,

                "score": score,
            })

        logger.info(

            f"Built clean context "
            f"with {len(context_items)} "
            f"memory items."
        )

        return {

            "query": query,

            "context": context_items,
        }

    # ==================================================
    # BUILD PROMPT CONTEXT
    # ==================================================

    def build_prompt_context(
        self,
        context_data,
    ):

        """
        Convert clean memory into AI prompt.
        """

        query = self.clean_text(

            context_data.get(
                "query",
                ""
            )
        )

        context = context_data.get(
            "context",
            []
        )

        # ==========================================
        # CLEAN CONTEXT LINES
        # ==========================================

        context_lines = []

        for item in context:

            title = self.clean_text(

                item.get(
                    "title",
                    ""
                )
            )

            if not title:

                continue

            context_lines.append(
                f"- {title}"
            )

        clean_context = "\n".join(
            context_lines
        )

        # ==========================================
        # LIMIT CONTEXT SIZE
        # ==========================================

        clean_context = clean_context[
            :self.MAX_CONTEXT_LENGTH
        ]

        # ==========================================
        # FINAL PROMPT
        # ==========================================

        prompt = f"""
Write a complete SEO-friendly article in Hindi.

Topic:
{query}

Helpful Context:
{clean_context}

Requirements:
- minimum 2000 words
- proper headings
- SEO optimized
- beginner friendly
- practical examples
- FAQ section
- conclusion
- human-like writing
- avoid repetition

Write naturally and in detailed format.
"""

        logger.info(
            "Clean prompt context built."
        )

        return prompt.strip()