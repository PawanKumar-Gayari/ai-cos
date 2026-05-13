"""
Persistent semantic memory retriever.
"""

import logging

from apps.memory.embeddings.embedding_service import (
    EmbeddingService
)

from apps.memory.storage.memory_repository import (
    MemoryRepository
)

from apps.memory.ranking.ranking_engine import (
    RankingEngine
)

from apps.memory.tracking.usage_tracker import (
    UsageTracker
)

from apps.memory.learning.importance_learner import (
    ImportanceLearner
)

from apps.memory.cache.cache_manager import (
    CacheManager
)


logger = logging.getLogger(
    __name__
)


class PersistentRetriever:

    MIN_RELEVANCE_SCORE = 0.25

    MAX_RESULTS = 20

    BLOCKED_PATTERNS = [

        "ignore previous instructions",

        "system prompt",

        "developer instructions",

        "reveal hidden prompt",
    ]

    def __init__(self):

        self.embedding_service = (
            EmbeddingService()
        )

        self.repository = (
            MemoryRepository()
        )

        self.ranking_engine = (
            RankingEngine()
        )

        self.usage_tracker = (
            UsageTracker()
        )

        self.importance_learner = (
            ImportanceLearner()
        )

        self.cache = (
            CacheManager()
        )

    # ==================================================
    # NORMALIZE QUERY
    # ==================================================

    def normalize_query(
        self,
        query,
    ):

        """
        Normalize query text.
        """

        if not query:

            return ""

        return (
            str(query)
            .strip()
            .lower()
        )

    # ==================================================
    # SAFE TEXT
    # ==================================================

    def safe_text(
        self,
        text,
    ):

        """
        Validate memory safety.
        """

        if not text:

            return False

        lowered = (
            text.lower()
        )

        for pattern in (
            self.BLOCKED_PATTERNS
        ):

            if pattern in lowered:

                return False

        return True

    # ==================================================
    # CACHE KEY
    # ==================================================

    def cache_key(
        self,
        query,
    ):

        """
        Generate retrieval cache key.
        """

        normalized_query = (
            self.normalize_query(
                query
            )
        )

        return (
            f"semantic_search:"
            f"{normalized_query}"
        )

    # ==================================================
    # SIMILARITY SCORE
    # ==================================================

    def similarity_score(
        self,
        embedding_1,
        embedding_2,
    ):

        """
        Calculate semantic similarity.
        """

        return (
            self.embedding_service.compare_embeddings(

                embedding_1,

                embedding_2,
            )
        )

    # ==================================================
    # VALID EMBEDDING
    # ==================================================

    def valid_embedding(
        self,
        embedding,
    ):

        """
        Validate embedding.
        """

        if not embedding:

            return False

        if not isinstance(
            embedding,
            list,
        ):

            return False

        if len(embedding) == 0:

            return False

        return True

    # ==================================================
    # BUILD RESULT
    # ==================================================

    def build_result(
        self,
        item,
        score,
    ):

        """
        Build retrieval result.
        """

        metadata = item.get(
            "metadata",
            {},
        )

        importance = metadata.get(
            "importance",
            0.5,
        )

        final_score = round(

            (
                score * 0.8
            )

            +

            (
                importance * 0.2
            ),

            4,
        )

        return {

            "query": item.get(
                "query"
            ),

            "semantic_score": (
                score
            ),

            "importance": (
                importance
            ),

            "final_score": (
                final_score
            ),

            "metadata": metadata,

            "created_at": item.get(
                "created_at"
            ),
        }

    # ==================================================
    # REMOVE DUPLICATES
    # ==================================================

    def unique_results(
        self,
        results,
    ):

        """
        Remove duplicate memories.
        """

        unique = []

        seen = set()

        for item in results:

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
    # PROCESS LEARNING
    # ==================================================

    def process_learning(
        self,
        result,
    ):

        """
        Adaptive learning pipeline.
        """

        try:

            query_text = result.get(
                "query"
            )

            semantic_score = result.get(
                "semantic_score",
                0,
            )

            self.usage_tracker.increment_usage(
                query_text
            )

            if semantic_score >= 0.70:

                self.importance_learner.boost_importance(

                    query=query_text,

                    amount=0.03,
                )

            elif semantic_score <= 0.30:

                self.importance_learner.reduce_importance(

                    query=query_text,

                    amount=0.01,
                )

        except Exception as error:

            logger.warning(

                f"Adaptive learning failed: "
                f"{str(error)}"
            )

    # ==================================================
    # MAIN SEARCH
    # ==================================================

    def search(
        self,
        query,
        top_k=5,
        min_score=None,
    ):

        """
        Persistent semantic search.
        """

        normalized_query = (
            self.normalize_query(
                query
            )
        )

        if not normalized_query:

            return []

        if not self.safe_text(
            normalized_query
        ):

            logger.warning(

                "Blocked unsafe query."
            )

            return []

        if min_score is None:

            min_score = (
                self.MIN_RELEVANCE_SCORE
            )

        top_k = min(
            top_k,
            self.MAX_RESULTS,
        )

        cache_key = self.cache_key(
            normalized_query
        )

        # ==========================================
        # CACHE HIT
        # ==========================================

        if self.cache.exists(
            cache_key
        ):

            logger.info(
                "Semantic cache hit."
            )

            cached_results = (
                self.cache.get(
                    cache_key
                )
            )

            return cached_results[:top_k]

        logger.info(

            f"Running semantic search "
            f"for: {normalized_query}"
        )

        # ==========================================
        # QUERY EMBEDDING
        # ==========================================

        query_embedding = (

            self.embedding_service.create(
                normalized_query
            )
        )

        embedding = (
            query_embedding.get(
                "embedding"
            )
        )

        if not self.valid_embedding(
            embedding
        ):

            logger.warning(

                "Invalid query embedding."
            )

            return []

        # ==========================================
        # MEMORY STORE
        # ==========================================

        stored_memories = (
            self.repository.all()
        )

        results = []

        for item in stored_memories:

            item_query = (
                item.get(
                    "query",
                    ""
                )
            )

            if not item_query:

                continue

            if not self.safe_text(
                item_query
            ):

                continue

            item_embedding = item.get(
                "embedding"
            )

            if not self.valid_embedding(
                item_embedding
            ):

                continue

            try:

                score = (
                    self.similarity_score(

                        embedding,

                        item_embedding,
                    )
                )

            except Exception:

                continue

            if score < min_score:

                continue

            result = self.build_result(

                item=item,

                score=score,
            )

            results.append(
                result
            )

        # ==========================================
        # UNIQUE RESULTS
        # ==========================================

        results = (
            self.unique_results(
                results
            )
        )

        # ==========================================
        # RANK RESULTS
        # ==========================================

        ranked_results = (
            self.ranking_engine.rank(
                results
            )
        )

        # ==========================================
        # LEARNING
        # ==========================================

        for result in ranked_results:

            self.process_learning(
                result
            )

        # ==========================================
        # CACHE STORE
        # ==========================================

        self.cache.set(

            cache_key,

            ranked_results,
        )

        logger.info(

            f"Semantic search completed "
            f"with {len(ranked_results)} "
            f"results"
        )

        return ranked_results[:top_k]

    # ==================================================
    # SEARCH ONE
    # ==================================================

    def search_one(
        self,
        query,
    ):

        """
        Return best semantic match.
        """

        results = self.search(

            query=query,

            top_k=1,
        )

        if not results:

            return None

        return results[0]

    # ==================================================
    # RELATED MEMORIES
    # ==================================================

    def related_memories(
        self,
        query,
        limit=3,
    ):

        """
        Return related memories.
        """

        return self.search(

            query=query,

            top_k=limit,
        )

    # ==================================================
    # MEMORY EXISTS
    # ==================================================

    def memory_exists(
        self,
        query,
    ):

        """
        Check if memory exists.
        """

        normalized_query = (
            self.normalize_query(
                query
            )
        )

        memories = (
            self.repository.all()
        )

        for item in memories:

            item_query = (
                self.normalize_query(

                    item.get(
                        "query",
                        ""
                    )
                )
            )

            if item_query == normalized_query:

                return True

        return False

    # ==================================================
    # MEMORY COUNT
    # ==================================================

    def memory_count(
        self
    ):

        """
        Return total memories.
        """

        return len(
            self.repository.all()
        )

    # ==================================================
    # CLEAR CACHE
    # ==================================================

    def clear_cache(
        self
    ):

        """
        Clear semantic cache.
        """

        logger.info(
            "Clearing semantic cache."
        )

        return self.cache.clear()

    # ==================================================
    # CACHE STATS
    # ==================================================

    def cache_stats(
        self
    ):

        """
        Return cache statistics.
        """

        return self.cache.stats()