"""
Enterprise memory-aware intelligent generator.
"""

import logging

from apps.memory.window.context_window import (
    ContextWindow
)

from apps.memory.indexer.memory_indexer import (
    MemoryIndexer
)

from apps.llm.router import (
    LLMRouter
)

from apps.generator.response_cleaner import (
    ResponseCleaner
)

from apps.generator.content_scorer import (
    ContentScorer
)

from apps.keywords.engine import (
    KeywordEngine
)

from apps.competitor.engine import (
    CompetitorEngine
)


logger = logging.getLogger(
    __name__
)


class IntelligentGenerator:

    def __init__(self):

        # ==========================================
        # MEMORY
        # ==========================================

        self.context_window = (
            ContextWindow()
        )

        self.memory_indexer = (
            MemoryIndexer()
        )

        # ==========================================
        # AI ROUTER
        # ==========================================

        self.router = (
            LLMRouter()
        )

        # ==========================================
        # SEO KEYWORDS
        # ==========================================

        self.keyword_engine = (
            KeywordEngine()
        )

        # ==========================================
        # COMPETITOR ENGINE
        # ==========================================

        self.competitor_engine = (
            CompetitorEngine()
        )

    # ==================================================
    # PROMPT BUILDER
    # ==================================================

    def build_prompt(
        self,
        user_query,
        context_prompt,
        task_type="seo",
        seo_keywords=None,
        competitor_context=None,
    ):

        """
        Build optimized prompt
        for cloud + local LLMs.
        """

        lines = []

        # ==========================================
        # CORE RULES
        # ==========================================

        lines.append(
            "Write clear, natural, "
            "human-like content."
        )

        lines.append(
            "Use markdown formatting."
        )

        lines.append(
            "Avoid robotic phrasing."
        )

        lines.append(
            "Do not mention AI."
        )

        lines.append(
            "Write directly without filler."
        )

        lines.append(
            "Keep explanations practical."
        )

        lines.append("")

        # ==========================================
        # TASK RULES
        # ==========================================

        if task_type == "seo":

            lines.append(
                "Focus on SEO optimization."
            )

            lines.append(
                "Use SEO best practices."
            )

            lines.append(
                "Optimize readability."
            )

        elif task_type == "outline":

            lines.append(
                "Create a detailed outline."
            )

            lines.append(
                "Use H1, H2, and H3 headings."
            )

        elif task_type == "keywords":

            lines.append(
                "Generate SEO keywords."
            )

            lines.append(
                "Include long-tail keywords."
            )

            lines.append(
                "Include search intent."
            )

        elif task_type == "article":

            lines.append(
                "Write a complete article."
            )

            lines.append(
                "Use markdown headings."
            )

            lines.append(
                "Use readable paragraphs."
            )

        elif task_type == "reasoning":

            lines.append(
                "Explain concepts simply."
            )

            lines.append(
                "Use practical examples."
            )

        lines.append("")

        # ==========================================
        # SEO KEYWORDS
        # ==========================================

        if seo_keywords:

            lines.append(
                "SEO keywords:"
            )

            for keyword in seo_keywords[:8]:

                lines.append(
                    f"- {keyword}"
                )

            lines.append("")

        # ==========================================
        # MEMORY CONTEXT
        # ==========================================

        if context_prompt:

            lines.append(
                "Relevant context:"
            )

            lines.append(
                context_prompt
            )

            lines.append("")

        # ==========================================
        # COMPETITOR CONTEXT
        # ==========================================

        if competitor_context:

            lines.append(
                "Competitor analysis:"
            )

            lines.append(
                competitor_context
            )

            lines.append("")

        # ==========================================
        # FINAL TASK
        # ==========================================

        lines.append(
            f"Task: {user_query}"
        )

        lines.append("")

        lines.append(
            "Write the final answer directly."
        )

        return "\n".join(
            lines
        )

    # ==================================================
    # TASK DETECTION
    # ==================================================

    def detect_task_type(
        self,
        query,
    ):

        """
        Intelligent task classification.
        """

        query_lower = (
            query.lower()
        )

        seo_keywords = [

            "seo",

            "ranking",

            "google",

            "backlinks",

            "meta title",

            "meta description",

            "search engine",
        ]

        if any(
            keyword in query_lower
            for keyword in seo_keywords
        ):

            return "seo"

        keyword_keywords = [

            "keyword",

            "keywords",

            "search terms",

            "keyword research",
        ]

        if any(
            keyword in query_lower
            for keyword in keyword_keywords
        ):

            return "keywords"

        outline_keywords = [

            "outline",

            "structure",

            "table of contents",

            "headings",
        ]

        if any(
            keyword in query_lower
            for keyword in outline_keywords
        ):

            return "outline"

        article_keywords = [

            "write",

            "article",

            "blog",

            "guide",

            "tutorial",
        ]

        if any(
            keyword in query_lower
            for keyword in article_keywords
        ):

            return "article"

        reasoning_keywords = [

            "explain",

            "why",

            "how",

            "difference",

            "compare",
        ]

        if any(
            keyword in query_lower
            for keyword in reasoning_keywords
        ):

            return "reasoning"

        return "general"

    # ==================================================
    # CONTEXT SANITIZATION
    # ==================================================

    def sanitize_context(
        self,
        context,
    ):

        """
        Remove embeddings
        and internal metadata.
        """

        semantic_memories = (
            context.get(
                "semantic_memories",
                []
            )
        )

        hot_memories = (
            context.get(
                "hot_memories",
                []
            )
        )

        sanitized_semantic = []

        for memory in semantic_memories:

            sanitized_semantic.append({

                "query": memory.get(
                    "query"
                ),

                "score": memory.get(
                    "final_score"
                ),

                "created_at": memory.get(
                    "created_at"
                ),
            })

        sanitized_hot = []

        for memory in hot_memories:

            sanitized_hot.append({

                "query": memory.get(
                    "query"
                ),

                "created_at": memory.get(
                    "created_at"
                ),
            })

        return {

            "query": context.get(
                "query"
            ),

            "semantic_memories_count": (
                len(sanitized_semantic)
            ),

            "hot_memories_count": (
                len(sanitized_hot)
            ),

            "semantic_memories": (
                sanitized_semantic
            ),

            "hot_memories": (
                sanitized_hot
            ),
        }

    # ==================================================
    # COMPETITOR CONTEXT
    # ==================================================

    def build_competitor_context(
        self,
        competitor_data,
    ):

        """
        Build compact competitor insights.
        """

        if not competitor_data:

            return ""

        lines = []

        summary = (
            competitor_data.get(
                "analysis_summary",
                {}
            )
        )

        gap_analysis = (
            competitor_data.get(
                "gap_analysis",
                {}
            )
        )

        weakness_analysis = (
            competitor_data.get(
                "weakness_analysis",
                {}
            )
        )

        competition_level = (
            summary.get(
                "competition_level"
            )
        )

        if competition_level:

            lines.append(

                f"Competition level: "
                f"{competition_level}"
            )

        seo_opportunity = (
            summary.get(
                "seo_opportunity"
            )
        )

        if seo_opportunity:

            lines.append(

                f"SEO opportunity: "
                f"{seo_opportunity}"
            )

        gaps = (
            gap_analysis.get(
                "content_gaps",
                []
            )
        )

        if gaps:

            lines.append("")
            lines.append(
                "Content opportunities:"
            )

            for gap in gaps[:5]:

                lines.append(
                    f"- {gap}"
                )

        weaknesses = (
            weakness_analysis.get(
                "weaknesses",
                []
            )
        )

        if weaknesses:

            lines.append("")
            lines.append(
                "Competitor weaknesses:"
            )

            for weakness in weaknesses[:5]:

                lines.append(
                    f"- {weakness}"
                )

        return "\n".join(
            lines
        )

    # ==================================================
    # MAIN GENERATION
    # ==================================================

    async def generate(
        self,
        query,
        session_id=None,
    ):

        """
        Full intelligent generation pipeline.
        """

        logger.info(

            f"Starting intelligent "
            f"generation for: {query}"
        )

        # ==========================================
        # MEMORY CONTEXT
        # ==========================================

        context = (
            self.context_window.build(

                query=query,

                session_id=session_id,
            )
        )

        context_prompt = (
            self.context_window.prompt_context(
                context
            )
        )

        # ==========================================
        # TASK TYPE
        # ==========================================

        task_type = (
            self.detect_task_type(
                query
            )
        )

        logger.info(

            f"Detected task type: "
            f"{task_type}"
        )

        # ==========================================
        # KEYWORD ENRICHMENT
        # ==========================================

        seo_keywords = []

        try:

            keyword_data = (
                self.keyword_engine.best_keywords(
                    query
                )
            )

            seo_keywords = [

                item["keyword"]

                for item in keyword_data
            ]

        except Exception as error:

            logger.warning(

                f"Keyword enrichment failed: "
                f"{str(error)}"
            )

        # ==========================================
        # COMPETITOR ENRICHMENT
        # ==========================================

        competitor_context = ""

        try:

            competitor_data = (
                self.competitor_engine.analyze(
                    query
                )
            )

            competitor_context = (
                self.build_competitor_context(
                    competitor_data
                )
            )

            logger.info(

                "Competitor enrichment "
                "completed."
            )

        except Exception as error:

            logger.warning(

                f"Competitor analysis failed: "
                f"{str(error)}"
            )

        # ==========================================
        # FINAL PROMPT
        # ==========================================

        final_prompt = (
            self.build_prompt(

                user_query=query,

                context_prompt=context_prompt,

                task_type=task_type,

                seo_keywords=seo_keywords,

                competitor_context=(
                    competitor_context
                ),
            )
        )

        # ==========================================
        # GENERATION
        # ==========================================

        response = await self.router.generate(

            prompt=final_prompt,

            task_type=task_type,
        )

        # ==========================================
        # SAFE EXTRACTION
        # ==========================================

        generated_content = ""

        provider = "unknown"

        success = False

        if isinstance(
            response,
            dict,
        ):

            generated_content = (
                response.get(
                    "content",
                    ""
                )
            )

            provider = (
                response.get(
                    "provider",
                    "unknown"
                )
            )

            success = (
                response.get(
                    "success",
                    False
                )
            )

        else:

            generated_content = str(
                response
            )

        # ==========================================
        # CLEAN RESPONSE
        # ==========================================

        generated_content = (
            ResponseCleaner.clean(
                generated_content
            )
        )

        # ==========================================
        # CONTENT SCORING
        # ==========================================

        content_scores = (
            ContentScorer.score(
                generated_content
            )
        )

        # ==========================================
        # MEMORY INDEXING
        # ==========================================

        try:

            self.memory_indexer.index(

                query=query,

                metadata={

                    "title": query,

                    "source": (
                        "intelligent_generator"
                    ),

                    "importance": 0.8,

                    "task_type": (
                        task_type
                    ),
                }
            )

        except Exception as error:

            logger.warning(

                f"Memory indexing failed: "
                f"{str(error)}"
            )

        clean_context = (
            self.sanitize_context(
                context
            )
        )

        logger.info(

            f"Generation completed "
            f"for: {query}"
        )

        return {

            "success": success,

            "provider": provider,

            "query": query,

            "task_type": (
                task_type
            ),

            "generated_content": (
                generated_content
            ),

            "seo_keywords": (
                seo_keywords
            ),

            "scores": (
                content_scores
            ),

            "context": (
                clean_context
            ),

            "competitor_enrichment": bool(
                competitor_context
            ),
        }

    # ==================================================
    # ARTICLE
    # ==================================================

    async def generate_article(
        self,
        topic,
        session_id=None,
    ):

        article_query = (

            f"Write an SEO article "
            f"about {topic}"
        )

        return await self.generate(

            query=article_query,

            session_id=session_id,
        )

    # ==================================================
    # OUTLINE
    # ==================================================

    async def generate_outline(
        self,
        topic,
        session_id=None,
    ):

        outline_query = (

            f"Create an outline "
            f"for {topic}"
        )

        return await self.generate(

            query=outline_query,

            session_id=session_id,
        )

    # ==================================================
    # KEYWORDS
    # ==================================================

    async def generate_keywords(
        self,
        topic,
        session_id=None,
    ):

        keyword_query = (

            f"Generate keywords "
            f"for {topic}"
        )

        return await self.generate(

            query=keyword_query,

            session_id=session_id,
        )

    # ==================================================
    # SYSTEM STATUS
    # ==================================================

    def system_status(self):

        """
        Generator system status.
        """

        return {

            "generator": "active",

            "memory_system": "active",

            "keyword_engine": "active",

            "competitor_engine": "active",

            "router": (
                self.router.router_status()
            ),
        }