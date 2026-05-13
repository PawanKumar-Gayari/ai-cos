"""
Local in-memory cache layer.
"""

import time
import logging
import threading


logger = logging.getLogger(
    __name__
)


class LocalCache:

    MAX_CACHE_ITEMS = 5000

    def __init__(
        self
    ):

        # ==========================================
        # CACHE STORAGE
        # ==========================================

        self.cache = {}

        # ==========================================
        # THREAD LOCK
        # ==========================================

        self._lock = (
            threading.Lock()
        )

        # ==========================================
        # CACHE STATS
        # ==========================================

        self.hit_count = 0

        self.miss_count = 0

    # ==================================================
    # CURRENT TIME
    # ==================================================

    def now(
        self
    ):

        return time.time()

    # ==================================================
    # VALID KEY
    # ==================================================

    def valid_key(
        self,
        key,
    ):

        """
        Validate cache key.
        """

        if key is None:

            return False

        if not isinstance(
            key,
            str,
        ):

            return False

        if not key.strip():

            return False

        return True

    # ==================================================
    # EVICTION
    # ==================================================

    def evict_if_needed(
        self
    ):

        """
        Simple FIFO eviction.
        """

        if len(self.cache) < (
            self.MAX_CACHE_ITEMS
        ):

            return

        oldest_key = None

        oldest_time = None

        for key, item in (
            self.cache.items()
        ):

            created_at = item.get(
                "created_at",
                0,
            )

            if (

                oldest_time is None

                or

                created_at < oldest_time
            ):

                oldest_time = (
                    created_at
                )

                oldest_key = key

        if oldest_key:

            del self.cache[
                oldest_key
            ]

            logger.warning(

                f"Cache evicted key: "
                f"{oldest_key}"
            )

    # ==================================================
    # SET
    # ==================================================

    def set(
        self,
        key,
        value,
    ):

        """
        Store cache item.
        """

        if not self.valid_key(
            key
        ):

            return False

        with self._lock:

            try:

                self.evict_if_needed()

                self.cache[key] = {

                    "value": value,

                    "created_at": (
                        self.now()
                    ),

                    "last_accessed": (
                        self.now()
                    ),
                }

                return True

            except Exception as error:

                logger.warning(

                    f"Cache set failed: "
                    f"{str(error)}"
                )

                return False

    # ==================================================
    # GET
    # ==================================================

    def get(
        self,
        key,
        default=None,
    ):

        """
        Retrieve cache item.
        """

        if not self.valid_key(
            key
        ):

            self.miss_count += 1

            return default

        with self._lock:

            try:

                item = self.cache.get(
                    key
                )

                if not item:

                    self.miss_count += 1

                    return default

                item[
                    "last_accessed"
                ] = self.now()

                self.hit_count += 1

                return item.get(
                    "value",
                    default,
                )

            except Exception as error:

                logger.warning(

                    f"Cache get failed: "
                    f"{str(error)}"
                )

                self.miss_count += 1

                return default

    # ==================================================
    # EXISTS
    # ==================================================

    def exists(
        self,
        key,
    ):

        """
        Check cache existence.
        """

        if not self.valid_key(
            key
        ):

            return False

        with self._lock:

            return key in self.cache

    # ==================================================
    # DELETE
    # ==================================================

    def delete(
        self,
        key,
    ):

        """
        Remove cache item.
        """

        if not self.valid_key(
            key
        ):

            return False

        with self._lock:

            try:

                if key in self.cache:

                    del self.cache[key]

                    return True

                return False

            except Exception as error:

                logger.warning(

                    f"Cache delete failed: "
                    f"{str(error)}"
                )

                return False

    # ==================================================
    # CLEAR
    # ==================================================

    def clear(
        self
    ):

        """
        Clear full cache.
        """

        with self._lock:

            try:

                self.cache.clear()

                logger.warning(
                    "Local cache cleared."
                )

                return True

            except Exception as error:

                logger.warning(

                    f"Cache clear failed: "
                    f"{str(error)}"
                )

                return False

    # ==================================================
    # KEYS
    # ==================================================

    def keys(
        self
    ):

        """
        Return cache keys.
        """

        with self._lock:

            return list(
                self.cache.keys()
            )

    # ==================================================
    # COUNT
    # ==================================================

    def count(
        self
    ):

        """
        Return cache size.
        """

        with self._lock:

            return len(
                self.cache
            )

    # ==================================================
    # ALL
    # ==================================================

    def all(
        self
    ):

        """
        Return raw cache storage.
        """

        with self._lock:

            return dict(
                self.cache
            )

    # ==================================================
    # HIT RATE
    # ==================================================

    def hit_rate(
        self
    ):

        """
        Cache hit rate.
        """

        total = (

            self.hit_count

            + self.miss_count
        )

        if total == 0:

            return 0.0

        return round(

            (
                self.hit_count
                / total
            ) * 100,

            2,
        )

    # ==================================================
    # CLEANUP
    # ==================================================

    def cleanup(
        self
    ):

        """
        Manual cleanup hook.
        """

        with self._lock:

            cleaned = 0

            invalid_keys = []

            for key, item in (
                self.cache.items()
            ):

                if not isinstance(
                    item,
                    dict,
                ):

                    invalid_keys.append(
                        key
                    )

            for key in invalid_keys:

                del self.cache[key]

                cleaned += 1

            logger.info(

                f"Cache cleanup removed "
                f"{cleaned} entries"
            )

            return cleaned

    # ==================================================
    # STATS
    # ==================================================

    def stats(
        self
    ):

        """
        Cache statistics.
        """

        return {

            "total_keys": (
                self.count()
            ),

            "max_cache_items": (
                self.MAX_CACHE_ITEMS
            ),

            "hits": (
                self.hit_count
            ),

            "misses": (
                self.miss_count
            ),

            "hit_rate": (
                self.hit_rate()
            ),

            "keys": (
                self.keys()
            ),
        }