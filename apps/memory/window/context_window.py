"""
Unified AI context window builder.
"""

import logging

from apps.memory.search.persistent_retriever import (
    PersistentRetriever
)

from apps.memory.session.session_memory import (
    SessionMemory
)

from apps.memory.tiers.hot_memory import (
    HotMemory
)


logger = logging.getLogger(
    __name__
)


class ContextWindow:

    MAX_SEMANTIC_MEMORIES = 5

    MAX_HOT_MEMORIES = 5

    MAX_SESSION_ITEMS = 10

    MAX_TEXT_LENGTH = 500

    BLOCKED_PATTERNS = [

        "ignore previous instructions",

        "system prompt",

        "developer instructions",

        "assistant instructions",

        "reveal hidden prompt",
    ]

    def __init__(self):

        self.retriever = (
            PersistentRetriever()
        )

        self.session_memory = (
            SessionMemory()
        )

        self.hot_memory = (
            HotMemory()
        )

    # ==================================================
    # CLEAN TEXT
    # ==================================================

    def clean_text(
        self,
        text,
    ):

        """
        Clean memory text.
        """

        if not text:

            return ""

        text = str(
            text
        ).strip()

        # ==========================================
        # INJECTION PROTECTION
        # ==========================================

        lowered = text.lower()

        for pattern in (
            self.BLOCKED_PATTERNS
        ):

            if pattern in lowered:

                return ""

        # ==========================================
        # LIMIT LENGTH
        # ==========================================

        if len(text) > (
            self.MAX_TEXT_LENGTH
        ):

            text = (
                text[
                    :self.MAX_TEXT_LENGTH
                ] + "..."
            )

        return text

    # ==================================================
    # UNIQUE MEMORIES
    # ==================================================

    def unique_memories(
        self,
        memories,
    ):

        """
        Remove duplicate memories.
        """

        unique = []

        seen = set()

        for item in memories:

            query = (
                item.get(
                    "query",
                    ""
                )
                .strip()
                .lower()
            )

            if not query:

                continue

            if query in seen:

                continue

            seen.add(
                query
            )

            unique.append(
                item
            )

        return unique

    # ==================================================
    # BUILD CONTEXT
    # ==================================================

    def build(
        self,
        query,
        session_id=None,
        top_k=3,
    ):

        """
        Build unified AI context.
        """

        logger.info(

            f"Building context window "
            f"for query: {query}"
        )

        # ==========================================
        # SEMANTIC MEMORIES
        # ==========================================

        semantic_memories = (
            self.retriever.search(

                query=query,

                top_k=min(

                    top_k,

                    self.MAX_SEMANTIC_MEMORIES,
                ),
            )
        )

        semantic_memories = (
            self.unique_memories(
                semantic_memories
            )
        )

        # ==========================================
        # HOT MEMORIES
        # ==========================================

        hot_memories = (
            self.hot_memory.top_memories(

                limit=(
                    self.MAX_HOT_MEMORIES
                )
            )
        )

        # ==========================================
        # SESSION CONTEXT
        # ==========================================

        session_context = {}

        if session_id:

            try:

                session_context = (

                    self.session_memory.full_context(
                        session_id
                    )
                )

            except Exception as error:

                logger.warning(

                    f"Session memory failed: "
                    f"{str(error)}"
                )

        logger.info(
            "Context window built successfully."
        )

        return {

            "query": (
                self.clean_text(
                    query
                )
            ),

            "session_context": (
                session_context
            ),

            "semantic_memories": (
                semantic_memories
            ),

            "hot_memories": (
                hot_memories
            ),
        }

    # ==================================================
    # FORMAT SESSION CONTEXT
    # ==================================================

    def format_session_context(
        self,
        session_context,
    ):

        """
        Format session context.
        """

        lines = []

        items = list(
            session_context.items()
        )

        items = items[
            :self.MAX_SESSION_ITEMS
        ]

        for key, value in items:

            clean_key = (
                self.clean_text(
                    key
                )
            )

            clean_value = (
                self.clean_text(
                    value
                )
            )

            if not clean_key:

                continue

            if not clean_value:

                continue

            lines.append(

                f"- {clean_key}: "
                f"{clean_value}"
            )

        return lines

    # ==================================================
    # FORMAT SEMANTIC MEMORIES
    # ==================================================

    def format_semantic_memories(
        self,
        semantic_memories,
    ):

        """
        Format semantic memories.
        """

        lines = []

        for item in semantic_memories:

            query = (
                self.clean_text(
                    item.get(
                        "query",
                        ""
                    )
                )
            )

            if not query:

                continue

            score = item.get(
                "final_score",
                0,
            )

            lines.append(

                f"- {query} "
                f"(score: {score})"
            )

        return lines

    # ==================================================
    # FORMAT HOT MEMORIES
    # ==================================================

    def format_hot_memories(
        self,
        hot_memories,
    ):

        """
        Format hot memories.
        """

        lines = []

        for item in hot_memories:

            metadata = item.get(
                "metadata",
                {}
            )

            title = metadata.get(
                "title",
                "Untitled"
            )

            title = (
                self.clean_text(
                    title
                )
            )

            if not title:

                continue

            lines.append(
                f"- {title}"
            )

        return lines

    # ==================================================
    # PROMPT CONTEXT
    # ==================================================

    def prompt_context(
        self,
        context,
    ):

        """
        Convert context into
        optimized AI prompt window.
        """

        lines = []

        # ==========================================
        # QUERY
        # ==========================================

        query = (
            self.clean_text(
                context.get(
                    "query",
                    ""
                )
            )
        )

        lines.append(
            f"User Query: {query}"
        )

        lines.append("")

        # ==========================================
        # SESSION CONTEXT
        # ==========================================

        session_context = context.get(
            "session_context",
            {}
        )

        if session_context:

            formatted = (
                self.format_session_context(
                    session_context
                )
            )

            if formatted:

                lines.append(
                    "Session Context:"
                )

                lines.extend(
                    formatted
                )

                lines.append("")

        # ==========================================
        # SEMANTIC MEMORIES
        # ==========================================

        semantic_memories = context.get(
            "semantic_memories",
            []
        )

        if semantic_memories:

            formatted = (
                self.format_semantic_memories(
                    semantic_memories
                )
            )

            if formatted:

                lines.append(
                    "Relevant Semantic Memories:"
                )

                lines.extend(
                    formatted
                )

                lines.append("")

        # ==========================================
        # HOT MEMORIES
        # ==========================================

        hot_memories = context.get(
            "hot_memories",
            []
        )

        if hot_memories:

            formatted = (
                self.format_hot_memories(
                    hot_memories
                )
            )

            if formatted:

                lines.append(
                    "Hot Memory Layer:"
                )

                lines.extend(
                    formatted
                )

        final_prompt = "\n".join(
            lines
        )

        logger.info(
            "Prompt context generated."
        )

        return final_prompt