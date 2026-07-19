"""
Enterprise Google Suggest Intelligence Service
----------------------------------------------

Final Optimized Enterprise Edition

Major Improvements:
-------------------
✓ Redis cached suggestions
✓ Shared requests session
✓ Reduced Google request volume
✓ Faster SEO keyword extraction
✓ OCI optimized
✓ Lower latency architecture
✓ Lower worker blocking
✓ Production-safe keyword pipeline
✓ Better Redis namespacing
✓ Reduced rate-limit risk
"""

from __future__ import annotations

import logging
import random
import re

from hashlib import md5

import requests

from django.core.cache import cache

from apps.keywords.models import (
    KeywordAnalysis,
)


logger = logging.getLogger(
    __name__
)


class GoogleSuggestService:

    """
    Enterprise SEO keyword intelligence service.
    """

    BASE_URL = (

        "https://suggestqueries.google.com/"
        "complete/search"
    )

    CACHE_TIMEOUT = 60 * 60 * 24

    MAX_SUGGESTIONS = 50

    REQUEST_TIMEOUT = 8

    # =====================================================
    # OPTIMIZED SEO TOKENS
    # =====================================================

    EXPANSION_SUFFIXES = [

        "2026",

        "result",

        "admit card",

        "syllabus",

        "exam date",

        "notification",

        "vacancy",

        "apply online",

        "salary",

        "cut off",
    ]

    # =====================================================
    # BLOCKED KEYWORDS
    # =====================================================

    BLOCKED_KEYWORDS = [

        "sex",
        "porn",

        "hack",
        "crack",
        "torrent",

        "xbet",
        "betting",
        "casino",

        "tutorial",
        "guide",
        "tips",
        "tools",
        "review",
        "reviews",
        "strategy",
        "best way",
    ]

    # =====================================================
    # INIT
    # =====================================================

    def __init__(
        self,
    ):

        # =============================================
        # SHARED HTTP SESSION
        # =============================================

        self.session = (
            requests.Session()
        )

    # =====================================================
    # NORMALIZE KEYWORD
    # =====================================================

    @staticmethod
    def normalize_keyword(
        keyword,
    ):

        keyword = str(
            keyword
        ).lower().strip()

        keyword = re.sub(

            r"[^\w\s\u0900-\u097F]",

            " ",

            keyword,
        )

        keyword = re.sub(

            r"\s+",

            " ",

            keyword,
        )

        replacements = {

            "rajatan":
            "rajasthan",

            "vacany":
            "vacancy",

            "nokri":
            "naukri",

            "govt":
            "government",

            "admitcard":
            "admit card",

            "cutoff":
            "cut off",
        }

        for wrong, correct in (
            replacements.items()
        ):

            keyword = keyword.replace(

                wrong,

                correct,
            )

        return keyword.strip()

    # =====================================================
    # CACHE KEY
    # =====================================================

    @staticmethod
    def get_cache_key(
        keyword,
    ):

        hashed = md5(

            keyword.encode()
        ).hexdigest()

        return (

            "seo:google_suggest:"
            f"{hashed}"
        )

    # =====================================================
    # HEADERS
    # =====================================================

    @staticmethod
    def get_headers():

        agents = [

            "Mozilla/5.0 "
            "(Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 "
            "(KHTML, like Gecko) "
            "Chrome/137.0 Safari/537.36",

            "Mozilla/5.0 "
            "(X11; Linux x86_64) "
            "AppleWebKit/537.36 "
            "(KHTML, like Gecko) "
            "Chrome/136.0 Safari/537.36",
        ]

        return {

            "User-Agent":
            random.choice(agents),

            "Accept-Language":
            "en-US,en;q=0.9",
        }

    # =====================================================
    # FETCH REQUEST
    # =====================================================

    def fetch_request(
        self,
        keyword,
    ):

        params = {

            "client":
            "firefox",

            "hl":
            "en",

            "q":
            keyword,
        }

        response = self.session.get(

            self.BASE_URL,

            params=params,

            headers=self.get_headers(),

            timeout=self.REQUEST_TIMEOUT,
        )

        response.raise_for_status()

        data = response.json()

        if (

            isinstance(data, list)

            and len(data) > 1
        ):

            return data[1]

        return []

    # =====================================================
    # RELEVANCE CHECK
    # =====================================================

    def relevant(
        self,
        source_keyword,
        suggestion,
    ):

        source_tokens = set(

            self.normalize_keyword(
                source_keyword
            ).split()
        )

        suggestion_tokens = set(

            self.normalize_keyword(
                suggestion
            ).split()
        )

        overlap = (
            source_tokens
            & suggestion_tokens
        )

        return len(overlap) >= 1

    # =====================================================
    # LOW QUALITY FILTER
    # =====================================================

    def low_quality(
        self,
        keyword,
    ):

        keyword = (
            self.normalize_keyword(
                keyword
            )
        )

        words = keyword.split()

        if len(words) < 2:
            return True

        blocked = any(

            bad in keyword

            for bad in (
                self.BLOCKED_KEYWORDS
            )
        )

        if blocked:
            return True

        if (

            len(words)

            != len(set(words))
        ):

            return True

        return False

    # =====================================================
    # FILTER SUGGESTIONS
    # =====================================================

    def filter_suggestions(

        self,

        source_keyword,

        suggestions,
    ):

        cleaned = []

        seen = set()

        source_keyword = (
            self.normalize_keyword(
                source_keyword
            )
        )

        for item in suggestions:

            if not item:
                continue

            item = (
                self.normalize_keyword(
                    item
                )
            )

            if len(item) < 4:
                continue

            if item in seen:
                continue

            if self.low_quality(
                item
            ):

                continue

            if not self.relevant(

                source_keyword,

                item,
            ):

                continue

            seen.add(
                item
            )

            cleaned.append(item)

        return cleaned[
            :self.MAX_SUGGESTIONS
        ]

    # =====================================================
    # FETCH KEYWORDS
    # =====================================================

    def fetch_keywords(
        self,
        keyword,
    ):

        keyword = (
            self.normalize_keyword(
                keyword
            )
        )

        cache_key = (
            self.get_cache_key(
                keyword
            )
        )

        # =============================================
        # CACHE HIT
        # =============================================

        cached = cache.get(
            cache_key
        )

        if cached:

            logger.info(
                "Google suggestion cache hit."
            )

            return cached

        all_suggestions = []

        try:

            # =========================================
            # MAIN QUERY
            # =========================================

            main_results = (
                self.fetch_request(
                    keyword
                )
            )

            all_suggestions.extend(
                main_results
            )

            # =========================================
            # OPTIMIZED SEO EXPANSIONS
            # =========================================

            for suffix in (
                self.EXPANSION_SUFFIXES
            ):

                try:

                    expanded_query = (
                        f"{keyword} "
                        f"{suffix}"
                    )

                    expanded_results = (

                        self.fetch_request(
                            expanded_query
                        )
                    )

                    all_suggestions.extend(
                        expanded_results
                    )

                except Exception:

                    logger.warning(

                        f"Expansion failed: "
                        f"{suffix}"
                    )

            # =========================================
            # FILTER
            # =========================================

            cleaned = (
                self.filter_suggestions(

                    keyword,

                    all_suggestions,
                )
            )

            # =========================================
            # ENSURE MAIN KEYWORD
            # =========================================

            if keyword not in cleaned:

                cleaned.insert(
                    0,
                    keyword,
                )

            # =========================================
            # CACHE STORE
            # =========================================

            cache.set(

                cache_key,

                cleaned,

                timeout=(
                    self.CACHE_TIMEOUT
                ),
            )

            logger.info(

                f"Collected "
                f"{len(cleaned)} "
                f"SEO keywords."
            )

            return cleaned

        except Exception:

            logger.exception(
                "Google Suggest failed."
            )

            return [keyword]

    # =====================================================
    # GET SUGGESTIONS
    # =====================================================

    def get_suggestions(
        self,
        keyword,
    ):

        return self.fetch_keywords(
            keyword
        )

    # =====================================================
    # STORE
    # =====================================================

    def collect_and_store(
        self,
        keyword,
    ):

        keywords = (
            self.fetch_keywords(
                keyword
            )
        )

        saved_keywords = []

        for item in keywords:

            try:

                obj, created = (

                    KeywordAnalysis.objects
                    .get_or_create(
                        keyword=item
                    )
                )

                saved_keywords.append({

                    "keyword":
                    obj.keyword,

                    "created":
                    created,

                    "score":
                    obj.keyword_score,

                    "intent":
                    obj.search_intent,
                })

            except Exception:

                logger.exception(
                    "Keyword save failed."
                )

        return saved_keywords