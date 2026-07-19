"""
Enterprise Semantic Similarity Service
=====================================

Final Optimized Enterprise Edition

Major Improvements:
-------------------
✓ Shared singleton embedding model
✓ Zero duplicate model loading
✓ Offline HuggingFace runtime
✓ Faster embedding reuse
✓ Lower RAM usage
✓ Lower startup latency
✓ Production-safe semantic engine
✓ OCI optimized
✓ Cached semantic inference
✓ Enterprise clustering pipeline
"""

from __future__ import annotations

import logging
import math
import re

from functools import lru_cache

import numpy as np

from rapidfuzz import fuzz

from rank_bm25 import BM25Okapi

from sklearn.metrics.pairwise import (
    cosine_similarity,
)

from apps.core.model_manager import (
    ModelManager,
)


logger = logging.getLogger(
    __name__
)


# =========================================================
# MODEL
# =========================================================

MODEL_NAME = (
    ModelManager
    .EMBEDDING_MODEL_NAME
)


# =========================================================
# MAIN SERVICE
# =========================================================

class SemanticSimilarityService:

    """
    Enterprise semantic intelligence engine.
    """

    MIN_SIMILARITY = 0.30

    HIGH_SIMILARITY = 0.70

    DEDUPE_THRESHOLD = 88

    MIN_PHRASE_LENGTH = 4

    # =====================================================
    # STOPWORDS
    # =====================================================

    STOPWORDS = {

        "the",
        "and",
        "for",
        "with",
        "that",
        "this",
        "from",
        "your",
        "our",
        "their",
        "what",
        "when",
        "where",
        "which",
        "have",
        "been",
        "will",
        "would",
    }

    # =====================================================
    # CLEAN TEXT
    # =====================================================

    @staticmethod
    @lru_cache(maxsize=10000)
    def clean_text(
        text: str,
    ) -> str:

        if not text:
            return ""

        text = str(text)

        text = re.sub(

            r"[^\w\s\-]",

            " ",

            text,
        )

        text = re.sub(

            r"\s+",

            " ",

            text,
        )

        return text.strip().lower()

    # =====================================================
    # TOKENIZE
    # =====================================================

    @classmethod
    def tokenize(
        cls,
        text: str,
    ) -> list[str]:

        text = cls.clean_text(
            text
        )

        tokens = [

            token

            for token in text.split()

            if (

                token

                and token not in (
                    cls.STOPWORDS
                )

                and len(token) > 1
            )
        ]

        return tokens

    # =====================================================
    # EMBEDDING
    # =====================================================

    @classmethod
    @lru_cache(maxsize=5000)
    def get_embedding(
        cls,
        text: str,
    ):

        # =============================================
        # SHARED SINGLETON MODEL
        # =============================================

        model = (
            ModelManager
            .embedding_model()
        )

        if not model:
            return None

        text = cls.clean_text(
            text
        )

        if not text:
            return None

        try:

            embedding = model.encode(

                text,

                normalize_embeddings=True,
            )

            return embedding

        except Exception:

            logger.exception(
                "Embedding generation failed"
            )

            return None

    # =====================================================
    # COSINE SIMILARITY
    # =====================================================

    @classmethod
    def cosine_score(
        cls,
        text1: str,
        text2: str,
    ) -> float:

        emb1 = cls.get_embedding(
            text1
        )

        emb2 = cls.get_embedding(
            text2
        )

        if (

            emb1 is None

            or

            emb2 is None
        ):

            return 0.0

        try:

            score = cosine_similarity(

                [emb1],

                [emb2],
            )[0][0]

            return round(

                float(score),

                4,
            )

        except Exception:

            logger.exception(
                "Cosine similarity failed"
            )

            return 0.0

    # =====================================================
    # SEED RELEVANCE
    # =====================================================

    @classmethod
    def compute_seed_relevance(
        cls,
        phrase: str,
        seed_keyword: str,
    ) -> float:

        phrase = cls.clean_text(
            phrase
        )

        seed_keyword = cls.clean_text(
            seed_keyword
        )

        if (

            not phrase

            or

            not seed_keyword
        ):

            return 0.0

        # =============================================
        # TOKEN OVERLAP
        # =============================================

        phrase_tokens = set(
            cls.tokenize(phrase)
        )

        seed_tokens = set(
            cls.tokenize(seed_keyword)
        )

        overlap = len(

            phrase_tokens

            &

            seed_tokens
        )

        token_score = (

            overlap

            /

            max(
                1,
                len(seed_tokens),
            )
        )

        # =============================================
        # SEMANTIC SCORE
        # =============================================

        semantic_score = (
            cls.cosine_score(

                phrase,

                seed_keyword,
            )
        )

        # =============================================
        # HYBRID SCORE
        # =============================================

        final_score = (

            token_score * 0.40

            +

            semantic_score * 0.60
        )

        return round(
            final_score,
            4,
        )

    # =====================================================
    # BM25 RANKING
    # =====================================================

    @classmethod
    def bm25_rank(
        cls,
        query: str,
        documents: list[str],
    ) -> list[tuple[str, float]]:

        if not documents:
            return []

        try:

            tokenized_docs = [

                cls.tokenize(doc)

                for doc in documents
            ]

            bm25 = BM25Okapi(
                tokenized_docs
            )

            query_tokens = cls.tokenize(
                query
            )

            scores = bm25.get_scores(
                query_tokens
            )

            results = list(zip(
                documents,
                scores,
            ))

            results.sort(

                key=lambda x: x[1],

                reverse=True,
            )

            return results

        except Exception:

            logger.exception(
                "BM25 ranking failed"
            )

            return []

    # =====================================================
    # SEMANTIC FILTER
    # =====================================================

    @classmethod
    def filter_relevant_keywords(
        cls,
        seed_keyword: str,
        keywords: list[str],
        threshold: float = None,
    ) -> list[dict]:

        if threshold is None:

            threshold = (
                cls.MIN_SIMILARITY
            )

        results = []

        for keyword in keywords:

            try:

                keyword = cls.clean_text(
                    keyword
                )

                if (
                    len(keyword)
                    < cls.MIN_PHRASE_LENGTH
                ):
                    continue

                relevance = (
                    cls.compute_seed_relevance(

                        keyword,

                        seed_keyword,
                    )
                )

                if relevance < threshold:
                    continue

                results.append({

                    "keyword":
                    keyword,

                    "relevance":
                    relevance,

                    "semantic_score":
                    cls.cosine_score(

                        keyword,

                        seed_keyword,
                    ),
                })

            except Exception:

                logger.exception(
                    "Keyword filtering failed"
                )

        results.sort(

            key=lambda x: (
                x["relevance"]
            ),

            reverse=True,
        )

        return results

    # =====================================================
    # FUZZY DEDUPE
    # =====================================================

    @classmethod
    def deduplicate_keywords(
        cls,
        keywords: list[str],
    ) -> list[str]:

        unique = []

        for keyword in keywords:

            keyword = cls.clean_text(
                keyword
            )

            duplicate = False

            for existing in unique:

                similarity = fuzz.ratio(

                    keyword,

                    existing,
                )

                if similarity >= (
                    cls.DEDUPE_THRESHOLD
                ):

                    duplicate = True

                    break

            if not duplicate:

                unique.append(
                    keyword
                )

        return unique

    # =====================================================
    # SEMANTIC CLUSTER
    # =====================================================

    @classmethod
    def semantic_clusters(
        cls,
        keywords: list[str],
        threshold: float = 0.65,
    ) -> dict:

        clusters = {}

        used = set()

        for keyword in keywords:

            if keyword in used:
                continue

            cluster = [keyword]

            used.add(keyword)

            for other in keywords:

                if other in used:
                    continue

                score = (
                    cls.cosine_score(

                        keyword,

                        other,
                    )
                )

                if score >= threshold:

                    cluster.append(
                        other
                    )

                    used.add(other)

            clusters[keyword] = (
                cluster
            )

        return clusters

    # =====================================================
    # BEST MATCH
    # =====================================================

    @classmethod
    def best_match(
        cls,
        query: str,
        candidates: list[str],
    ) -> dict:

        best_keyword = ""

        best_score = 0.0

        for candidate in candidates:

            score = (
                cls.compute_seed_relevance(

                    candidate,

                    query,
                )
            )

            if score > best_score:

                best_score = score

                best_keyword = candidate

        return {

            "query":
            query,

            "best_match":
            best_keyword,

            "score":
            round(
                best_score,
                4,
            ),
        }

    # =====================================================
    # HYBRID SEO RANKING
    # =====================================================

    @classmethod
    def rank_keywords(
        cls,
        seed_keyword: str,
        keywords: list[str],
    ) -> list[dict]:

        keywords = (
            cls.deduplicate_keywords(
                keywords
            )
        )

        bm25_scores = dict(

            cls.bm25_rank(

                seed_keyword,

                keywords,
            )
        )

        results = []

        for keyword in keywords:

            semantic_score = (
                cls.compute_seed_relevance(

                    keyword,

                    seed_keyword,
                )
            )

            bm25_score = float(
                bm25_scores.get(
                    keyword,
                    0.0,
                )
            )

            bm25_normalized = min(

                bm25_score / 10,

                1.0,
            )

            final_score = (

                semantic_score * 0.70

                +

                bm25_normalized * 0.30
            )

            results.append({

                "keyword":
                keyword,

                "semantic_score":
                round(
                    semantic_score,
                    4,
                ),

                "bm25_score":
                round(
                    bm25_normalized,
                    4,
                ),

                "final_score":
                round(
                    final_score,
                    4,
                ),
            })

        results.sort(

            key=lambda x: (
                x["final_score"]
            ),

            reverse=True,
        )

        return results

    # =====================================================
    # HEALTH CHECK
    # =====================================================

    @classmethod
    def health_check(
        cls,
    ) -> dict:

        model_loaded = False

        try:

            model_loaded = (

                ModelManager
                .embedding_model()
                is not None
            )

        except Exception:

            logger.exception(
                "Semantic health check failed"
            )

        return {

            "model_loaded":
            model_loaded,

            "model_name":
            MODEL_NAME,

            "min_similarity":
            cls.MIN_SIMILARITY,

            "high_similarity":
            cls.HIGH_SIMILARITY,
        }