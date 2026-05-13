"""
Rewrite cache system.
"""

import hashlib
import time


class RewriteCache:

    def __init__(self):

        # =========================
        # IN-MEMORY CACHE
        # =========================

        self.cache = {}

        # =========================
        # CACHE TTL
        # =========================

        self.default_ttl = 3600

    def generate_key(
        self,
        content,
    ):

        # =========================
        # VALIDATE CONTENT
        # =========================

        if not content:

            return None

        # =========================
        # GENERATE HASH
        # =========================

        return hashlib.md5(

            content.encode(
                "utf-8"
            )

        ).hexdigest()

    def get(
        self,
        content,
    ):

        # =========================
        # GENERATE KEY
        # =========================

        cache_key = self.generate_key(
            content
        )

        if not cache_key:

            return None

        # =========================
        # CHECK CACHE
        # =========================

        cached_item = self.cache.get(
            cache_key
        )

        if not cached_item:

            return None

        # =========================
        # CHECK EXPIRATION
        # =========================

        expires_at = cached_item.get(
            "expires_at"
        )

        current_time = time.time()

        if current_time > expires_at:

            # =====================
            # REMOVE EXPIRED ITEM
            # =====================

            del self.cache[
                cache_key
            ]

            return None

        # =========================
        # RETURN DATA
        # =========================

        return cached_item.get(
            "data"
        )

    def set(
        self,
        content,
        data,
        ttl=None,
    ):

        # =========================
        # GENERATE KEY
        # =========================

        cache_key = self.generate_key(
            content
        )

        if not cache_key:

            return

        # =========================
        # TTL
        # =========================

        if ttl is None:

            ttl = self.default_ttl

        # =========================
        # SAVE CACHE
        # =========================

        self.cache[
            cache_key
        ] = {

            "data": data,

            "created_at": (
                time.time()
            ),

            "expires_at": (
                time.time() + ttl
            ),
        }

    def delete(
        self,
        content,
    ):

        # =========================
        # GENERATE KEY
        # =========================

        cache_key = self.generate_key(
            content
        )

        if not cache_key:

            return

        # =========================
        # DELETE CACHE
        # =========================

        if cache_key in self.cache:

            del self.cache[
                cache_key
            ]

    def clear(self):

        # =========================
        # CLEAR CACHE
        # =========================

        self.cache.clear()

    def stats(self):

        # =========================
        # CACHE STATS
        # =========================

        return {

            "total_items": len(
                self.cache
            ),

            "default_ttl": (
                self.default_ttl
            ),
        }