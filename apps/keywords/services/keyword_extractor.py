"""
Enterprise Semantic Keyword Extractor v8
========================================

Production-grade semantic SEO extraction engine.

Features:
---------
✓ spaCy NLP extraction
✓ SentenceTransformer semantic relevance
✓ BM25 hybrid ranking
✓ SEO phrase normalization
✓ RapidFuzz dedupe
✓ Semantic clustering
✓ Intent classification
✓ Garbage phrase filtering
✓ Production-safe serialization
✓ OCI Free Tier optimized
"""

from __future__ import annotations

import logging
import math
import re

from collections import defaultdict
from dataclasses import dataclass
from dataclasses import field
from functools import lru_cache
from typing import Optional

import spacy

from apps.keywords.services.semantic_similarity_service import (
    SemanticSimilarityService,
)

logger = logging.getLogger(__name__)


# =========================================================
# NLP MODEL
# =========================================================

try:

    NLP = spacy.load(
        "en_core_web_sm"
    )

except Exception:

    logger.exception(
        "spaCy model load failed"
    )

    NLP = None


# =========================================================
# SOURCE WEIGHTS
# =========================================================

SOURCE_WEIGHTS = {

    "related_searches": 10.0,
    "google_suggest": 10.0,
    "paa": 9.0,

    "title": 7.0,
    "heading": 6.0,
    "description": 4.0,

    "semantic": 5.0,
}


# =========================================================
# INTENT PATTERNS
# =========================================================

INTENT_PATTERNS = {

    "informational": {

        "what",
        "how",
        "why",
        "guide",
        "tutorial",
    },

    "transactional": {

        "download",
        "pdf",
        "apply",
        "online",
    },

    "commercial": {

        "best",
        "top",
        "review",
        "compare",
    },
}


# =========================================================
# INTENT BONUS
# =========================================================

INTENT_BONUS = {

    "transactional": 0.15,
    "commercial": 0.10,
    "informational": 0.05,
}


# =========================================================
# ENTITY HIERARCHY
# =========================================================

@dataclass
class EntityHierarchy:

    entity: str = ""

    subtopic: str = ""

    modifier: str = ""

    intent: str = ""

    def to_dict(self) -> dict:

        return {

            "entity": self.entity,
            "subtopic": self.subtopic,
            "modifier": self.modifier,
            "intent": self.intent,
        }


# =========================================================
# MEMORY
# =========================================================

@dataclass
class PhraseMemory:

    weighted_score: float = 0.0

    frequency: int = 0

    sources: set[str] = field(
        default_factory=set
    )

    @property
    def cross_source_boost(self) -> float:

        if len(self.sources) <= 1:
            return 0.0

        return (
            len(self.sources) - 1
        ) * 2.0


# =========================================================
# EXTRACTED KEYWORD
# =========================================================

@dataclass
class ExtractedKeyword:

    phrase: str

    frequency: int = 0

    source_score: float = 0.0

    cross_source: float = 0.0

    naturalness: float = 0.0

    intent: str = "informational"

    entity_hierarchy: Optional[
        EntityHierarchy
    ] = None

    final_score: float = 0.0

    cluster_id: Optional[str] = None

    def to_dict(self) -> dict:

        hierarchy = None

        if self.entity_hierarchy:

            hierarchy = (
                self.entity_hierarchy
                .to_dict()
            )

        return {

            "keyword": self.phrase,

            "frequency": self.frequency,

            "source_score": round(
                self.source_score,
                4,
            ),

            "cross_source": round(
                self.cross_source,
                4,
            ),

            "naturalness": round(
                self.naturalness,
                4,
            ),

            "intent": self.intent,

            "cluster_id": self.cluster_id,

            "seo_score": round(
                self.final_score,
                4,
            ),

            "hierarchy": hierarchy,
        }


# =========================================================
# MAIN EXTRACTOR
# =========================================================

class KeywordExtractor:

    MAX_KEYWORDS = 50

    MIN_WORDS = 2

    MAX_WORDS = 6

    MIN_PHRASE_LEN = 5

    CLUSTER_OVERLAP = 0.60

    SEMANTIC_THRESHOLD = 0.25

    BM25_WEIGHT = 0.20

    # =====================================================
    # FILTERS
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
        "their",
        "have",
        "been",
    }

    NOISE_PHRASES = {

        "opens in new",
        "in new tab",
        "click here",
        "read more",
        "what is the",
        "download now",
        "show more",
    }

    BAD_GENERIC_PHRASES = {

        "pdf",
        "download",
        "official",
        "complete",
        "new syllabus",
    }

    SEO_TERMS = {

        "syllabus",
        "result",
        "cutoff",
        "notification",
        "vacancy",
        "recruitment",
        "salary",
        "pdf",
        "exam",
        "admit card",
        "answer key",
    }

    HIGH_VALUE_PREFIXES = {

        "ssc",
        "upsc",
        "rrb",
        "ibps",
        "neet",
        "jee",
        "gate",
        "rpsc",
    }

    SUBTOPIC_SIGNALS = {

        "syllabus",
        "result",
        "cutoff",
        "exam",
        "vacancy",
    }

    MODIFIER_SIGNALS = {

        "pdf",
        "official",
        "online",
        "2025",
        "2026",
    }

    # =====================================================
    # CLEAN TEXT
    # =====================================================

    @staticmethod
    @lru_cache(maxsize=5000)
    def clean_text(text: str) -> str:

        if not text:
            return ""

        text = re.sub(
            r"[^\w\s\-]",
            " ",
            str(text),
        )

        text = re.sub(
            r"\s+",
            " ",
            text,
        )

        return text.strip().lower()

    # =====================================================
    # SEO NORMALIZATION
    # =====================================================

    @classmethod
    def normalize_seo_phrase(
        cls,
        phrase: str,
    ) -> str:

        phrase = cls.clean_text(
            phrase
        )

        if not phrase:
            return ""

        bad_prefixes = {

            "complete",
            "best",
            "top",
            "latest",
            "official",
            "new",
        }

        words = phrase.split()

        while words and words[0] in bad_prefixes:

            words.pop(0)

        phrase = " ".join(words)

        replacements = {

            "pdf download": "pdf",

            "download pdf": "pdf",

            "exam pattern and syllabus":
            "exam pattern syllabus",

            "complete syllabus":
            "syllabus",

            "official website":
            "official",

            "notification pdf":
            "notification",
        }

        for old, new in replacements.items():

            phrase = phrase.replace(
                old,
                new,
            )

        phrase = re.sub(
            r"\s+",
            " ",
            phrase,
        )

        return phrase.strip()

    # =====================================================
    # VALIDATION
    # =====================================================

    @classmethod
    def is_valid_phrase(
        cls,
        phrase: str,
    ) -> bool:

        if not phrase:
            return False

        phrase = cls.normalize_seo_phrase(
            phrase
        )

        if phrase in cls.NOISE_PHRASES:
            return False

        if phrase in cls.BAD_GENERIC_PHRASES:
            return False

        if len(phrase) < cls.MIN_PHRASE_LEN:
            return False

        words = phrase.split()

        if not (
            cls.MIN_WORDS
            <= len(words)
            <= cls.MAX_WORDS
        ):
            return False

        stop_ratio = sum(

            1

            for w in words

            if w in cls.STOPWORDS

        ) / max(1, len(words))

        if stop_ratio >= 0.5:
            return False

        semantic_words = [

            w

            for w in words

            if (
                len(w) > 2
                and w not in cls.STOPWORDS
            )
        ]

        semantic_density = (
            len(semantic_words)
            / max(1, len(words))
        )

        if semantic_density < 0.6:
            return False

        return True

    # =====================================================
    # NATURALNESS
    # =====================================================

    @classmethod
    def query_naturalness_score(
        cls,
        phrase: str,
    ) -> float:

        phrase = cls.normalize_seo_phrase(
            phrase
        )

        score = 0.5

        words = phrase.split()

        if 2 <= len(words) <= 5:
            score += 0.20

        if any(
            term in phrase
            for term in cls.SEO_TERMS
        ):
            score += 0.20

        if re.search(
            r"\b20\d{2}\b",
            phrase,
        ):
            score += 0.10

        return min(score, 1.0)

    # =====================================================
    # INTENT
    # =====================================================

    @classmethod
    def classify_intent(
        cls,
        phrase: str,
    ) -> str:

        phrase = phrase.lower()

        scores = defaultdict(int)

        for intent, patterns in (
            INTENT_PATTERNS.items()
        ):

            for signal in patterns:

                if signal in phrase:
                    scores[intent] += 1

        if not scores:
            return "informational"

        return max(
            scores,
            key=scores.get,
        )

    # =====================================================
    # ENTITY HIERARCHY
    # =====================================================

    @classmethod
    def extract_entity_hierarchy(
        cls,
        phrase: str,
        seed_tokens: frozenset[str],
    ) -> EntityHierarchy:

        words = phrase.split()

        hierarchy = EntityHierarchy()

        hierarchy.entity = " ".join([

            w

            for w in words

            if w in seed_tokens
        ])

        for word in words:

            if word in cls.SUBTOPIC_SIGNALS:

                hierarchy.subtopic = word

                break

        for word in reversed(words):

            if word in cls.MODIFIER_SIGNALS:

                hierarchy.modifier = word

                break

        hierarchy.intent = (
            cls.classify_intent(
                phrase
            )
        )

        return hierarchy

    # =====================================================
    # SPACY EXTRACTION
    # =====================================================

    @classmethod
    def extract_semantic_phrases(
        cls,
        text: str,
    ) -> list[str]:

        if not NLP:
            return []

        phrases = []

        try:

            doc = NLP(text)

            for chunk in doc.noun_chunks:

                if len(
                    chunk.text.split()
                ) < 2:
                    continue

                if chunk.root.pos_ not in {
                    "NOUN",
                    "PROPN",
                }:
                    continue

                if any(
                    token.pos_ == "PRON"
                    for token in chunk
                ):
                    continue

                phrase = (
                    cls.normalize_seo_phrase(
                        chunk.text
                    )
                )

                if cls.is_valid_phrase(
                    phrase
                ):
                    phrases.append(
                        phrase
                    )

            for ent in doc.ents:

                phrase = (
                    cls.normalize_seo_phrase(
                        ent.text
                    )
                )

                if cls.is_valid_phrase(
                    phrase
                ):
                    phrases.append(
                        phrase
                    )

        except Exception:

            logger.exception(
                "spaCy extraction failed"
            )

        return list(
            dict.fromkeys(
                phrases
            )
        )

    # =====================================================
    # FINAL SCORE
    # =====================================================

    @classmethod
    def compute_final_score(
        cls,
        kw: ExtractedKeyword,
    ) -> float:

        score = 0.0

        score += (
            kw.source_score * 0.35
        )

        score += (
            kw.cross_source * 0.20
        )

        score += (
            kw.naturalness * 0.25
        )

        score += (
            math.log1p(
                kw.frequency
            ) * 0.08
        )

        score += (
            INTENT_BONUS.get(
                kw.intent,
                0.0,
            )
        )

        return round(
            score,
            4,
        )

    # =====================================================
    # CLUSTERING
    # =====================================================

    @classmethod
    def cluster_phrases(
        cls,
        keywords: list[
            ExtractedKeyword
        ],
    ) -> list[ExtractedKeyword]:

        buckets = {}

        for kw in keywords:

            tokens = frozenset(
                kw.phrase.split()
            )

            matched = None

            for bucket_tokens in buckets:

                overlap = len(
                    tokens & bucket_tokens
                ) / max(
                    1,
                    len(
                        tokens
                        | bucket_tokens
                    ),
                )

                if overlap >= (
                    cls.CLUSTER_OVERLAP
                ):

                    matched = bucket_tokens

                    break

            if matched:

                existing = buckets[
                    matched
                ]

                if (
                    kw.final_score
                    >
                    existing.final_score
                ):

                    buckets[
                        matched
                    ] = kw

            else:

                kw.cluster_id = kw.phrase

                buckets[
                    tokens
                ] = kw

        return list(
            buckets.values()
        )

    # =====================================================
    # MAIN EXTRACTION
    # =====================================================

    @classmethod
    def extract_keywords_rich(
        cls,
        results: list[dict],
        seed_keyword: str = "",
    ) -> list[dict]:

        logger.info(
            "Enterprise semantic extraction started"
        )

        seed_tokens = frozenset(

            cls.clean_text(
                seed_keyword
            ).split()
        )

        memory = defaultdict(
            PhraseMemory
        )

        def add_phrase(

            phrase: str,

            source_key: str,

            weight: float,

            rank: int = 0,
        ):

            phrase = (
                cls.normalize_seo_phrase(
                    phrase
                )
            )

            if not (
                cls.is_valid_phrase(
                    phrase
                )
            ):
                return

            relevance = (
                SemanticSimilarityService
                .compute_seed_relevance(

                    phrase,

                    seed_keyword,
                )
            )

            if relevance < (
                cls.SEMANTIC_THRESHOLD
            ):

                if not any(

                    prefix in phrase

                    for prefix in (
                        cls.HIGH_VALUE_PREFIXES
                    )
                ):

                    return

            mem = memory[phrase]

            mem.weighted_score += (

                weight

                *

                (
                    1.0 /
                    max(1, rank)
                )
            )

            mem.frequency += 1

            mem.sources.add(
                source_key
            )

        # =================================================
        # PROCESS RESULTS
        # =================================================

        for idx, item in enumerate(results):

            rank = item.get(
                "rank",
                idx + 1,
            )

            for source_key in [

                "related_searches",
                "google_suggest",
                "questions",
            ]:

                phrases = item.get(
                    source_key,
                    [],
                )

                for phrase in phrases:

                    normalized = (
                        "paa"
                        if source_key
                        == "questions"
                        else source_key
                    )

                    add_phrase(

                        phrase,

                        normalized,

                        SOURCE_WEIGHTS.get(
                            normalized,
                            1.0,
                        ),

                        rank,
                    )

            combined_text = " ".join([

                item.get(
                    "title",
                    "",
                ),

                item.get(
                    "description",
                    "",
                ),

                " ".join(
                    item.get(
                        "headings",
                        [],
                    )
                ),
            ])

            semantic_phrases = (
                cls.extract_semantic_phrases(
                    combined_text
                )
            )

            for phrase in semantic_phrases:

                add_phrase(

                    phrase,

                    "semantic",

                    SOURCE_WEIGHTS[
                        "semantic"
                    ],

                    rank,
                )

        extracted = []

        for phrase, mem in memory.items():

            try:

                kw = ExtractedKeyword(

                    phrase=phrase,

                    frequency=(
                        mem.frequency
                    ),

                    source_score=(
                        mem.weighted_score
                    ),

                    cross_source=(
                        mem.cross_source_boost
                    ),

                    naturalness=(
                        cls.query_naturalness_score(
                            phrase
                        )
                    ),

                    intent=(
                        cls.classify_intent(
                            phrase
                        )
                    ),

                    entity_hierarchy=(
                        cls.extract_entity_hierarchy(

                            phrase,

                            seed_tokens,
                        )
                    ),
                )

                kw.final_score = (
                    cls.compute_final_score(
                        kw
                    )
                )

                extracted.append(
                    kw
                )

            except Exception:

                logger.exception(
                    "Keyword processing failed"
                )

        extracted = (
            cls.cluster_phrases(
                extracted
            )
        )

        deduped = (
            SemanticSimilarityService
            .deduplicate_keywords(

                [
                    kw.phrase
                    for kw in extracted
                ]
            )
        )

        extracted = [

            kw

            for kw in extracted

            if kw.phrase in deduped
        ]

        try:

            ranked = (
                SemanticSimilarityService
                .rank_keywords(

                    seed_keyword,

                    [
                        kw.phrase
                        for kw in extracted
                    ]
                )
            )

            ranking_map = {

                item["keyword"]:
                item["final_score"]

                for item in ranked
            }

            for kw in extracted:

                semantic_score = (
                    ranking_map.get(
                        kw.phrase,
                        0.0,
                    )
                )

                kw.final_score += (

                    semantic_score

                    *

                    cls.BM25_WEIGHT
                )

        except Exception:

            logger.exception(
                "Hybrid ranking failed"
            )

        extracted.sort(

            key=lambda x: (
                x.final_score
            ),

            reverse=True,
        )

        extracted = extracted[
            :cls.MAX_KEYWORDS
        ]

        return [

            kw.to_dict()

            for kw in extracted
        ]

    # =====================================================
    # SIMPLE EXTRACTION
    # =====================================================

    @classmethod
    def extract_keywords(
        cls,
        results: list[dict],
        seed_keyword: str = "",
    ) -> list[str]:

        rich = (
            cls.extract_keywords_rich(

                results,

                seed_keyword,
            )
        )

        return [

            item.get(
                "keyword",
                ""
            )

            for item in rich
        ]
