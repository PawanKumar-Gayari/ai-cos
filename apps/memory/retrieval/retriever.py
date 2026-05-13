"""
Semantic retriever.
"""

from apps.memory.embeddings.embedding_service import (
    EmbeddingService
)


class Retriever:

    def __init__(self):

        self.embedding_service = (
            EmbeddingService()
        )

    def similarity_score(
        self,
        embedding_1,
        embedding_2,
    ):

        """
        Calculate similarity score between
        two embeddings.
        """

        return self.embedding_service.compare_embeddings(

            embedding_1,

            embedding_2,
        )

    def retrieve(
        self,
        query_embedding,
        vectors,
        top_k=3,
    ):

        """
        Retrieve most relevant vectors.
        """

        results = []

        for item in vectors:

            score = self.similarity_score(

                query_embedding,

                item["embedding"],
            )

            results.append({

                "id": item["id"],

                "score": score,

                "metadata": item.get(
                    "metadata",
                    {},
                ),
            })

        sorted_results = sorted(

            results,

            key=lambda x: x["score"],

            reverse=True,
        )

        return sorted_results[:top_k]

    def search(
        self,
        query: str,
        vector_manager,
        top_k=3,
    ):

        """
        Full semantic search pipeline.
        """

        query_embedding = (
            self.embedding_service.create(
                query
            )
        )

        vectors = (
            vector_manager.get_all_vectors()
        )

        return self.retrieve(

            query_embedding=query_embedding[
                "embedding"
            ],

            vectors=vectors,

            top_k=top_k,
        )