"""
Memory-aware AI generator.
"""

from apps.memory.embeddings.embedding_service import (
    EmbeddingService
)

from apps.memory.retrieval.retriever import (
    Retriever
)

from apps.memory.context.context_builder import (
    ContextBuilder
)


class MemoryGenerator:

    def __init__(
        self,
        vector_manager,
    ):

        self.vector_manager = (
            vector_manager
        )

        self.embedding_service = (
            EmbeddingService()
        )

        self.retriever = Retriever()

        self.context_builder = (
            ContextBuilder()
        )

    def generate(
        self,
        query,
    ):

        retrieval_results = (

            self.retriever.search(

                query=query,

                vector_manager=self.vector_manager,
            )
        )

        context = (

            self.context_builder.build(

                query=query,

                retrieval_results=retrieval_results,
            )
        )

        prompt_context = (

            self.context_builder.build_prompt_context(
                context
            )
        )

        return {

            "query": query,

            "retrieval_results": retrieval_results,

            "prompt_context": prompt_context,
        }