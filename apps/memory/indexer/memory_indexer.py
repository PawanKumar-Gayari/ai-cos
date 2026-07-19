"""
Automatic memory indexing engine.
"""

import hashlib
import logging

from apps.memory.embeddings.embedding_service import (
    EmbeddingService
)

from apps.memory.storage.memory_repository import (
    MemoryRepository
)


logger = logging.getLogger(
    __name__
)


class MemoryIndexer:

    MAX_QUERY_LENGTH = 2000

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

    # ==================================================
    # CLEAN QUERY
    # ==================================================

    def clean_query(
        self,
        query,
    ):

        """
        Clean memory query.
        """

        if not query:

            return ""

        query = str(
            query
        ).strip()

        lowered = (
            query.lower()
        )

        # ==========================================
        # INJECTION FILTER
        # ==========================================

        for pattern in (
            self.BLOCKED_PATTERNS
        ):

            if pattern in lowered:

                return ""

        # ==========================================
        # LIMIT LENGTH
        # ==========================================

        if len(query) > (
            self.MAX_QUERY_LENGTH
        ):

            query = (
                query[
                    :self.MAX_QUERY_LENGTH
                ] + "..."
            )

        return query

    # ==================================================
    # NORMALIZE METADATA
    # ==================================================

    def normalize_metadata(
        self,
        metadata,
    ):

        """
        Normalize metadata.
        """

        if not metadata:

            return {}

        safe_metadata = {}

        for key, value in (
            metadata.items()
        ):

            safe_key = str(
                key
            )[:100]

            safe_value = str(
                value
            )[:500]

            safe_metadata[
                safe_key
            ] = safe_value

        return safe_metadata

    # ==================================================
    # MEMORY HASH
    # ==================================================

    def memory_hash(
        self,
        query,
    ):

        """
        Create stable memory hash.
        """

        return hashlib.md5(

            query.encode(
                "utf-8"
            )

        ).hexdigest()

    # ==================================================
    # VALID EMBEDDING
    # ==================================================

    def valid_embedding(
        self,
        embedding,
    ):

        """
        Validate embedding structure.
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
    # MAIN INDEX
    # ==================================================

    def index(
        self,
        query,
        metadata=None,
    ):

        """
        Automatically:
        - clean query
        - generate embedding
        - persist semantic memory
        """

        try:

            # ==========================================
            # CLEAN QUERY
            # ==========================================

            query = (
                self.clean_query(
                    query
                )
            )

            if not query:

                logger.warning(
                    "Memory indexing skipped: "
                    "empty query."
                )

                return None

            # ==========================================
            # NORMALIZE METADATA
            # ==========================================

            metadata = (
                self.normalize_metadata(
                    metadata
                )
            )

            # ==========================================
            # MEMORY HASH
            # ==========================================

            memory_id = (
                self.memory_hash(
                    query
                )
            )

            metadata[
                "memory_hash"
            ] = memory_id

            logger.info(

                f"Generating embedding "
                f"for memory: {memory_id}"
            )

            # ==========================================
            # EMBEDDING
            # ==========================================

            embedding_result = (
                self.embedding_service.create(
                    query
                )
            )

            embedding = (
                embedding_result.get(
                    "embedding"
                )
            )

            if not self.valid_embedding(
                embedding
            ):

                logger.warning(

                    "Invalid embedding "
                    "generated."
                )

                return None

            # ==========================================
            # STORE MEMORY
            # ==========================================

            stored_item = (

                self.repository.add(

                    query=query,

                    embedding=embedding,

                    metadata=metadata,
                )
            )

            logger.info(

                f"Memory indexed "
                f"successfully: "
                f"{memory_id}"
            )

            return stored_item

        except Exception as error:

            logger.exception(

                f"Memory indexing failed: "
                f"{str(error)}"
            )

            return None