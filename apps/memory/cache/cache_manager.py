"""
Unified enterprise cache manager.
"""

import time
import logging

from apps.memory.cache.local_cache import (
    LocalCache
)


logger = logging.getLogger(
    __name__
)


class CacheManager:

    DEFAULT_TTL = 3600

    MAX_KEY_LENGTH = 300

    def __init__(self):

        self.cache = (
            LocalCache()
        )

        # ==========================================
        # CACHE STATS
        # ==========================================

        self.hit_count = 0

        self.miss_count = 0

    # ==================================================
    # SAFE KEY
    # ==================================================

    def safe_key(
        self,
        key,
    ):

        """
        Normalize cache key.
        """

        if not key:

            return ""

        key = str(
            key
        ).strip().lower()

        if len(key) > (
            self.MAX_KEY_LENGTH
        ):

            key = key[
                :self.MAX_KEY_LENGTH
            ]

        return key

    # ==================================================
    # TTL PAYLOAD
    # ==================================================

    def build_payload(
        self,
        value,
        ttl=None,
    ):

        """
        Build cache payload.
        """

        ttl = ttl or (
            self.DEFAULT_TTL
        )

        now = time.time()

        return {

            "value": value,

            "created_at": now,

            "expires_at": (
                now + ttl
            ),
        }

    # ==================================================
    # EXPIRED
    # ==================================================

    def expired(
        self,
        payload,
    ):

        """
        Check expiration.
        """

        if not payload:

            return True

        expires_at = payload.get(
            "expires_at"
        )

        if not expires_at:

            return True

        return (
            time.time() > expires_at
        )

    # ==================================================
    # CLEANUP KEY
    # ==================================================

    def cleanup_key(
        self,
        key,
    ):

        """
        Remove expired key.
        """

        try:

            self.cache.delete(
                key
            )

        except Exception:

            pass

    # ==================================================
    # SET
    # ==================================================

    def set(
        self,
        key,
        value,
        ttl=None,
    ):

        """
        Store cache value.
        """

        try:

            key = self.safe_key(
                key
            )

            if not key:

                return False

            payload = (
                self.build_payload(

                    value=value,

                    ttl=ttl,
                )
            )

            return self.cache.set(

                key,

                payload,
            )

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
        Retrieve cache value.
        """

        try:

            key = self.safe_key(
                key
            )

            payload = self.cache.get(
                key
            )

            if not payload:

                self.miss_count += 1

                return default

            if self.expired(
                payload
            ):

                self.cleanup_key(
                    key
                )

                self.miss_count += 1

                return default

            self.hit_count += 1

            return payload.get(
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
        Check if cache exists.
        """

        value = self.get(
            key
        )

        return value is not None

    # ==================================================
    # DELETE
    # ==================================================

    def delete(
        self,
        key,
    ):

        """
        Delete cache item.
        """

        try:

            key = self.safe_key(
                key
            )

            return self.cache.delete(
                key
            )

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
        Clear entire cache.
        """

        try:

            logger.warning(
                "Clearing cache."
            )

            return self.cache.clear()

        except Exception as error:

            logger.warning(

                f"Cache clear failed: "
                f"{str(error)}"
            )

            return False

    # ==================================================
    # CLEANUP EXPIRED
    # ==================================================

    def cleanup_expired(
        self
    ):

        """
        Cleanup expired cache entries.
        """

        try:

            data = self.cache.all()

            cleaned = 0

            for key, payload in (
                data.items()
            ):

                if self.expired(
                    payload
                ):

                    self.cleanup_key(
                        key
                    )

                    cleaned += 1

            logger.info(

                f"Expired cache cleanup: "
                f"{cleaned} entries"
            )

            return cleaned

        except Exception as error:

            logger.warning(

                f"Cache cleanup failed: "
                f"{str(error)}"
            )

            return 0

    # ==================================================
    # HIT RATE
    # ==================================================

    def hit_rate(
        self
    ):

        """
        Cache hit percentage.
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
    # STATS
    # ==================================================

    def stats(
        self
    ):

        """
        Return cache statistics.
        """

        try:

            base_stats = (
                self.cache.stats()
            )

        except Exception:

            base_stats = {}

        return {

            "hits": (
                self.hit_count
            ),

            "misses": (
                self.miss_count
            ),

            "hit_rate": (
                self.hit_rate()
            ),

            "default_ttl": (
                self.DEFAULT_TTL
            ),

            "backend": (
                self.cache.__class__.__name__
            ),

            "storage": (
                base_stats
            ),
        }