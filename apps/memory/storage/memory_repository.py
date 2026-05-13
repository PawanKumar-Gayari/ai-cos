"""
Persistent memory repository.
"""

import hashlib
import logging

from datetime import datetime

from apps.memory.storage.json_store import (
    JsonStore
)


logger = logging.getLogger(
    __name__
)


class MemoryRepository:

    MAX_QUERY_LENGTH = 3000

    def __init__(self):

        self.store = JsonStore()

    # ==================================================
    # SAFE LOAD
    # ==================================================

    def safe_load(
        self
    ):

        """
        Safe repository load.
        """

        try:

            data = self.store.load()

            if not isinstance(
                data,
                list,
            ):

                return []

            return data

        except Exception as error:

            logger.exception(

                f"Repository load failed: "
                f"{str(error)}"
            )

            return []

    # ==================================================
    # SAFE SAVE
    # ==================================================

    def safe_save(
        self,
        data,
    ):

        """
        Safe repository save.
        """

        try:

            self.store.save(data)

            return True

        except Exception as error:

            logger.exception(

                f"Repository save failed: "
                f"{str(error)}"
            )

            return False

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

        query = str(
            query
        ).strip().lower()

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

        normalized = {}

        for key, value in (
            metadata.items()
        ):

            normalized[
                str(key)[:100]
            ] = str(value)[:1000]

        return normalized

    # ==================================================
    # MEMORY HASH
    # ==================================================

    def memory_hash(
        self,
        query,
    ):

        """
        Create deterministic memory ID.
        """

        return hashlib.md5(

            query.encode(
                "utf-8"
            )

        ).hexdigest()

    # ==================================================
    # ALL MEMORIES
    # ==================================================

    def all(
        self
    ):

        """
        Return all memory items.
        """

        return self.safe_load()

    # ==================================================
    # MEMORY EXISTS
    # ==================================================

    def memory_exists(
        self,
        query,
    ):

        """
        Check if query already exists.
        """

        normalized_query = (
            self.normalize_query(
                query
            )
        )

        data = self.safe_load()

        for item in data:

            stored_query = (
                self.normalize_query(

                    item.get(
                        "query",
                        ""
                    )
                )
            )

            if stored_query == normalized_query:

                return True

        return False

    # ==================================================
    # ADD MEMORY
    # ==================================================

    def add(
        self,
        query,
        embedding,
        metadata=None,
    ):

        """
        Add persistent semantic memory.
        """

        query = (
            self.normalize_query(
                query
            )
        )

        if not query:

            logger.warning(
                "Skipped empty memory."
            )

            return None

        if not self.valid_embedding(
            embedding
        ):

            logger.warning(
                "Invalid embedding skipped."
            )

            return None

        if self.memory_exists(
            query
        ):

            logger.info(
                "Duplicate memory skipped."
            )

            return None

        metadata = (
            self.normalize_metadata(
                metadata
            )
        )

        memory_id = (
            self.memory_hash(
                query
            )
        )

        data = self.safe_load()

        item = {

            "id": memory_id,

            "query": query,

            "embedding": embedding,

            "metadata": metadata,

            "created_at": (

                datetime.utcnow()
                .isoformat()
            ),
        }

        data.append(item)

        success = (
            self.safe_save(data)
        )

        if not success:

            return None

        logger.info(

            f"Memory stored: "
            f"{memory_id}"
        )

        return item

    # ==================================================
    # COUNT
    # ==================================================

    def count(
        self
    ):

        """
        Return total memory items.
        """

        return len(
            self.safe_load()
        )

    # ==================================================
    # LATEST MEMORIES
    # ==================================================

    def latest(
        self,
        limit=5,
    ):

        """
        Return latest memories.
        """

        data = self.safe_load()

        return data[-limit:]

    # ==================================================
    # SEARCH QUERY
    # ==================================================

    def search_by_query(
        self,
        query,
    ):

        """
        Search memories by query.
        """

        normalized_query = (
            self.normalize_query(
                query
            )
        )

        data = self.safe_load()

        results = []

        for item in data:

            stored_query = (
                self.normalize_query(

                    item.get(
                        "query",
                        ""
                    )
                )
            )

            if normalized_query in (
                stored_query
            ):

                results.append(
                    item
                )

        return results

    # ==================================================
    # DELETE MEMORY
    # ==================================================

    def delete(
        self,
        index,
    ):

        """
        Delete memory by index.
        """

        data = self.safe_load()

        if 0 <= index < len(data):

            deleted_item = (
                data.pop(index)
            )

            self.safe_save(data)

            logger.info(
                "Memory deleted."
            )

            return deleted_item

        return None

    # ==================================================
    # DELETE BY ID
    # ==================================================

    def delete_by_id(
        self,
        memory_id,
    ):

        """
        Delete memory by ID.
        """

        data = self.safe_load()

        filtered = [

            item

            for item in data

            if item.get(
                "id"
            ) != memory_id
        ]

        self.safe_save(filtered)

        logger.info(

            f"Memory deleted: "
            f"{memory_id}"
        )

        return True

    # ==================================================
    # CLEAR REPOSITORY
    # ==================================================

    def clear(
        self
    ):

        """
        Clear all memories.
        """

        logger.warning(
            "Clearing memory repository."
        )

        return self.safe_save([])