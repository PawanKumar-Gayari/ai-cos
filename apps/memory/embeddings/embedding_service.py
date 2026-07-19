"""
Enterprise semantic embedding service.
"""

import logging
import math

from numpy import dot
from numpy.linalg import norm

from apps.core.model_manager import (
    ModelManager
)

from apps.memory.cache.cache_manager import (
    CacheManager
)


logger = logging.getLogger(
    __name__
)


class EmbeddingService:

    MAX_TEXT_LENGTH = 5000

    BLOCKED_PATTERNS = [

        "ignore previous instructions",

        "system prompt",

        "developer instructions",

        "reveal hidden prompt",
    ]

    def __init__(self):

        """
        Load shared embedding model.
        """

        self.model = (
            ModelManager.embedding_model()
        )

        self.cache = (
            CacheManager()
        )

    # ==================================================
    # NORMALIZE TEXT
    # ==================================================

    def normalize_text(
        self,
        text,
    ):

        """
        Normalize text before embedding.
        """

        if not text:

            return ""

        text = str(
            text
        ).strip().lower()

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
    # SAFE TEXT
    # ==================================================

    def safe_text(
        self,
        text,
    ):

        """
        Validate text safety.
        """

        lowered = text.lower()

        for pattern in (
            self.BLOCKED_PATTERNS
        ):

            if pattern in lowered:

                return False

        return True

    # ==================================================
    # CACHE KEY
    # ==================================================

    def embedding_cache_key(
        self,
        text,
    ):

        """
        Generate embedding cache key.
        """

        normalized_text = (
            self.normalize_text(
                text
            )
        )

        return (
            f"embedding:"
            f"{normalized_text}"
        )

    # ==================================================
    # VALID VECTOR
    # ==================================================

    def valid_vector(
        self,
        vector,
    ):

        """
        Validate embedding vector.
        """

        if not vector:

            return False

        if not isinstance(
            vector,
            list,
        ):

            return False

        if len(vector) == 0:

            return False

        for value in vector:

            if value is None:

                return False

            if math.isnan(
                float(value)
            ):

                return False

        return True

    # ==================================================
    # GENERATE EMBEDDING
    # ==================================================

    def generate_embedding(
        self,
        text,
    ):

        """
        Generate semantic embedding.
        """

        normalized_text = (
            self.normalize_text(
                text
            )
        )

        if not normalized_text:

            return {

                "text": "",

                "embedding": [],
            }

        if not self.safe_text(
            normalized_text
        ):

            logger.warning(
                "Blocked unsafe embedding text."
            )

            return {

                "text": normalized_text,

                "embedding": [],
            }

        cache_key = (
            self.embedding_cache_key(
                normalized_text
            )
        )

        # ==========================================
        # CACHE HIT
        # ==========================================

        if self.cache.exists(
            cache_key
        ):

            logger.info(
                "Embedding cache hit."
            )

            return self.cache.get(
                cache_key
            )

        logger.info(
            "Generating embedding."
        )

        embedding = (
            self.model.encode(
                normalized_text
            )
        )

        embedding_list = (
            embedding.tolist()
        )

        if not self.valid_vector(
            embedding_list
        ):

            logger.warning(
                "Invalid embedding generated."
            )

            return {

                "text": normalized_text,

                "embedding": [],
            }

        result = {

            "text": normalized_text,

            "embedding": (
                embedding_list
            ),
        }

        self.cache.set(

            cache_key,

            result,
        )

        return result

    # ==================================================
    # VECTOR LENGTH
    # ==================================================

    def embedding_length(
        self,
        embedding,
    ):

        """
        Return vector length.
        """

        if not embedding:

            return 0

        return len(
            embedding
        )

    # ==================================================
    # COSINE SIMILARITY
    # ==================================================

    def compare_embeddings(
        self,
        embedding_1,
        embedding_2,
    ):

        """
        Calculate cosine similarity.
        """

        try:

            if not self.valid_vector(
                embedding_1
            ):

                return 0.0

            if not self.valid_vector(
                embedding_2
            ):

                return 0.0

            denominator = (

                norm(embedding_1)

                *

                norm(embedding_2)
            )

            if denominator == 0:

                return 0.0

            similarity = (

                dot(
                    embedding_1,
                    embedding_2,
                )

                / denominator
            )

            similarity = float(
                similarity
            )

            if math.isnan(
                similarity
            ):

                return 0.0

            return round(
                similarity,
                6,
            )

        except Exception as error:

            logger.warning(

                f"Embedding comparison failed: "
                f"{str(error)}"
            )

            return 0.0

    # ==================================================
    # CREATE
    # ==================================================

    def create(
        self,
        text,
    ):

        """
        Full embedding pipeline.
        """

        normalized_text = (
            self.normalize_text(
                text
            )
        )

        return self.generate_embedding(
            normalized_text
        )

    # ==================================================
    # BATCH CREATE
    # ==================================================

    def batch_create(
        self,
        texts,
    ):

        """
        Batch embedding generation.
        """

        if not texts:

            return []

        results = []

        uncached_texts = []

        seen = set()

        # ==========================================
        # CACHE CHECK
        # ==========================================

        for text in texts:

            normalized_text = (
                self.normalize_text(
                    text
                )
            )

            if not normalized_text:

                continue

            if normalized_text in seen:

                continue

            seen.add(
                normalized_text
            )

            if not self.safe_text(
                normalized_text
            ):

                continue

            cache_key = (
                self.embedding_cache_key(
                    normalized_text
                )
            )

            if self.cache.exists(
                cache_key
            ):

                cached_result = (
                    self.cache.get(
                        cache_key
                    )
                )

                results.append(
                    cached_result
                )

            else:

                uncached_texts.append(
                    normalized_text
                )

        # ==========================================
        # BATCH EMBEDDINGS
        # ==========================================

        if uncached_texts:

            embeddings = (
                self.model.encode(
                    uncached_texts
                )
            )

            for text, embedding in zip(

                uncached_texts,

                embeddings,
            ):

                embedding_list = (
                    embedding.tolist()
                )

                if not self.valid_vector(
                    embedding_list
                ):

                    continue

                result = {

                    "text": text,

                    "embedding": (
                        embedding_list
                    ),
                }

                cache_key = (
                    self.embedding_cache_key(
                        text
                    )
                )

                self.cache.set(

                    cache_key,

                    result,
                )

                results.append(
                    result
                )

        logger.info(

            f"Batch embeddings completed "
            f"with {len(results)} results"
        )

        return results

    # ==================================================
    # HEALTH CHECK
    # ==================================================

    def health_check(
        self
    ):

        """
        Embedding runtime health.
        """

        try:

            test = self.create(
                "health check"
            )

            embedding = test.get(
                "embedding",
                []
            )

            return {

                "healthy": (
                    len(embedding) > 0
                ),

                "embedding_size": (
                    len(embedding)
                ),

                "shared_runtime": True,
            }

        except Exception as error:

            logger.exception(

                f"Embedding health failed: "
                f"{str(error)}"
            )

            return {

                "healthy": False,

                "error": str(error),
            }

    # ==================================================
    # CLEAR CACHE
    # ==================================================

    def clear_embedding_cache(
        self
    ):

        """
        Clear embedding cache.
        """

        logger.info(
            "Clearing embedding cache."
        )

        return self.cache.clear()

    # ==================================================
    # CACHE STATS
    # ==================================================

    def cache_stats(
        self
    ):

        """
        Return embedding cache stats.
        """

        return self.cache.stats()