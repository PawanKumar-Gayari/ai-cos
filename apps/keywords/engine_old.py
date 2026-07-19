"""
Enterprise SEO Intelligence Engine
----------------------------------
"""

from __future__ import annotations

import logging
import re

from typing import Any

from apps.keywords.constants import (
    BLOCKED_KEYWORDS,
    MAX_KEYWORD_LENGTH,
    MAX_KEYWORD_WORDS,
    MIN_KEYWORD_LENGTH,
)

from apps.keywords.exceptions import (
    KeywordValidationException,
)

from apps.keywords.services.clustering_service import (
    ClusteringService,
)

from apps.keywords.services.google_suggest import (
    GoogleSuggestService,
)

from apps.keywords.services.intent_service import (
    IntentService,
)

from apps.keywords.services.keyword_extractor import (
    KeywordExtractor,
)

from apps.keywords.services.scoring_service import (
    AdvancedScoringService,
)

logger = logging.getLogger(__name__)


class KeywordEngine:

    HINDI_PATTERN = re.compile(
        r"[\u0900-\u097F]"
    )

    MULTI_SPACE_PATTERN = re.compile(
        r"\s+"
    )

    REPEATED_WORD_PATTERN = re.compile(
        r"\b(\w+)(\s+\1\b)+",
        re.IGNORECASE,
    )

    MIN_TOKEN_MATCH = 1

    # =============================================
    # INIT
    # =============================================

    def __init__(self):

        self.intent_service = (
            IntentService()
        )

        self.scoring_service = (
            AdvancedScoringService()
        )

        self.google_service = (
            GoogleSuggestService()
        )

        self.cluster_service = (
            ClusteringService()
        )

    # =============================================
    # VALIDATE
    # =============================================

    def validate_keyword(
        self,
        keyword,
    ):

        if not isinstance(keyword, str):

            raise KeywordValidationException(
                "Keyword must be string."
            )

        keyword = keyword.strip()

        if not keyword:

            raise KeywordValidationException(
                "Keyword cannot be empty."
            )

        normalized = keyword.lower()

        if normalized in BLOCKED_KEYWORDS:

            raise KeywordValidationException(
                "Blocked keyword detected."
            )

        if len(keyword) < MIN_KEYWORD_LENGTH:

            raise KeywordValidationException(
                "Keyword too short."
            )

        if len(keyword) > MAX_KEYWORD_LENGTH:

            raise KeywordValidationException(
                "Keyword too long."
            )

        if len(keyword.split()) > MAX_KEYWORD_WORDS:

            raise KeywordValidationException(
                "Too many words."
            )

        return keyword

    # =============================================
    # LANGUAGE
    # =============================================

    def detect_language(
        self,
        text,
    ):

        if self.HINDI_PATTERN.search(text):

            return "hindi"

        return "english"

    # =============================================
    # NORMALIZE
    # =============================================

    def normalize_keyword(
        self,
        keyword,
    ):

        keyword = str(keyword).strip().lower()

        keyword = re.sub(
            r"[^\w\s\u0900-\u097F]",
            " ",
            keyword,
        )

        keyword = (
            self.MULTI_SPACE_PATTERN.sub(
                " ",
                keyword,
            )
        )

        keyword = (
            self.REPEATED_WORD_PATTERN.sub(
                r"\1",
                keyword,
            )
        )

        return keyword.strip()

    # =============================================
    # TOKENS
    # =============================================

    def keyword_tokens(
        self,
        keyword,
    ):

        keyword = (
            self.normalize_keyword(keyword)
        )

        return set(keyword.split())

    # =============================================
    # RELEVANCE
    # =============================================

    def relevant(
        self,
        source,
        target,
    ):

        source_tokens = (
            self.keyword_tokens(source)
        )

        target_tokens = (
            self.keyword_tokens(target)
        )

        overlap = (
            source_tokens & target_tokens
        )

        return (
            len(overlap)
            >= self.MIN_TOKEN_MATCH
        )

    # =============================================
    # CLEAN
    # =============================================

    def clean_keywords(
        self,
        source_topic,
        keywords,
    ):

        cleaned = []

        seen = set()

        for keyword in keywords:

            keyword = (
                self.normalize_keyword(keyword)
            )

            if not keyword:
                continue

            if keyword in seen:
                continue

            if len(keyword) < 4:
                continue

            if not self.relevant(
                source_topic,
                keyword,
            ):
                continue

            seen.add(keyword)

            cleaned.append(keyword)

        return cleaned

    # =============================================
    # SAFE SCORING ACCESS
    # =============================================

    def scoring_value(
        self,
        scoring,
        field,
        default=None,
    ):

        if scoring is None:
            return default

        if isinstance(scoring, dict):
            return scoring.get(field, default)

        return getattr(
            scoring,
            field,
            default,
        )

    # =============================================
    # ANALYZE
    # =============================================

    def analyze(
        self,
        keyword,
    ):

        keyword = (
            self.validate_keyword(keyword)
        )

        keyword = (
            self.normalize_keyword(keyword)
        )

        language = (
            self.detect_language(keyword)
        )

        intent = (
            KeywordExtractor.classify_intent(
                keyword
            )
        )

        scoring = (
            self.scoring_service
            .calculate_advanced_score(
                keyword
            )
        )

        return {

            "keyword":
            keyword,

            "language":
            language,

            "intent":
            intent,

            "difficulty":
            self.scoring_value(
                scoring,
                "difficulty",
                "unknown",
            ),

            "volume":
            self.scoring_value(
                scoring,
                "volume",
                0,
            ),

            "raw_volume":
            self.scoring_value(
                scoring,
                "raw_volume",
                0,
            ),

            "score":
            self.scoring_value(
                scoring,
                "score",
                0,
            ),

            "seo_priority":
            self.seo_priority(
                scoring
            ),

            "word_count":
            self.scoring_value(
                scoring,
                "word_count",
                0,
            ),

            "character_count":
            self.scoring_value(
                scoring,
                "character_count",
                0,
            ),
        }

    # =============================================
    # SEO PRIORITY
    # =============================================

    def seo_priority(
        self,
        scoring,
    ):

        score = float(
            self.scoring_value(
                scoring,
                "score",
                0,
            )
        )

        volume = float(
            self.scoring_value(
                scoring,
                "volume",
                0,
            )
        )

        return round(
            (
                score * 0.7
            )
            +
            (
                volume * 0.3
            ),
            2,
        )

    # =============================================
    # SEMANTIC
    # =============================================

    def semantic_keywords(
        self,
        topic,
    ):

        topic = (
            self.validate_keyword(topic)
        )

        topic = (
            self.normalize_keyword(topic)
        )

        logger.info(
            "Generating semantic keywords."
        )

        google_keywords = (
            self.google_service
            .get_suggestions(topic)
        )

        internal_keywords = [

            topic,

            f"best {topic}",

            f"{topic} guide",

            f"{topic} tips",

            f"{topic} review",

            f"{topic} for beginners",

            f"{topic} in india",

            f"{topic} tutorial",

            f"{topic} examples",

            f"{topic} tools",
        ]

        combined = (
            google_keywords
            + internal_keywords
        )

        return self.clean_keywords(
            topic,
            combined,
        )

    # =============================================
    # EXPAND
    # =============================================

    def expand_keywords(
        self,
        topic,
        limit=50,
    ):

        logger.info(
            "Keyword expansion started."
        )

        topic = (
            self.validate_keyword(topic)
        )

        keywords = (
            self.semantic_keywords(topic)
        )

        results = []

        for keyword in keywords:

            try:

                analyzed = (
                    self.analyze(keyword)
                )

                results.append(analyzed)

            except Exception as error:

                logger.exception(
                    f"Keyword failed: {str(error)}"
                )

        logger.info(
            "Keyword expansion completed."
        )

        return results[:limit]

    # =============================================
    # BEST KEYWORDS
    # =============================================

    def best_keywords(
        self,
        topic,
        limit=10,
    ):

        keywords = (
            self.expand_keywords(
                topic,
                limit=100,
            )
        )

        sorted_keywords = sorted(

            keywords,

            key=lambda item:

            (

                item.get(
                    "seo_priority",
                    0,
                ),

                item.get(
                    "score",
                    0,
                ),

                item.get(
                    "volume",
                    0,
                ),
            ),

            reverse=True,
        )

        return sorted_keywords[:limit]

    # =============================================
    # CLUSTERS
    # =============================================

    def clusters(
        self,
        topic,
        limit=50,
    ):

        keywords = (
            self.expand_keywords(
                topic,
                limit=limit,
            )
        )

        keyword_list = [

            item.get("keyword")

            for item in keywords

            if item.get("keyword")
        ]

        return (
            self.cluster_service
            .cluster_keywords(
                keyword_list
            )
        )

    # =============================================
    # FULL ANALYSIS
    # =============================================

    def analyze_keyword(
        self,
        topic,
    ):

        logger.info(
            "Full SEO analysis started."
        )

        best_keywords = (
            self.best_keywords(
                topic,
                limit=15,
            )
        )

        suggestions = [

            item["keyword"]

            for item in best_keywords
        ]

        primary = (

            suggestions[0]

            if suggestions

            else topic
        )

        intent = (

            best_keywords[0].get(
                "intent",
                "informational",
            )

            if best_keywords

            else "informational"
        )

        avg_score = 0

        if best_keywords:

            avg_score = round(

                sum(

                    item.get(
                        "score",
                        0,
                    )

                    for item in best_keywords
                )

                / len(best_keywords),

                2,
            )

        result = {

            "keyword":
            primary,

            "suggestions":
            suggestions,

            "best_keywords":
            best_keywords,

            "semantic_keywords":
            suggestions,

            "search_intent":
            intent,

            "seo_score":
            avg_score,

            "competition_level":

            (
                best_keywords[0].get(
                    "difficulty",
                    "unknown",
                )

                if best_keywords
                else "unknown"
            ),

            "clusters":
            self.clusters(
                topic,
                limit=50,
            ),

            "total_keywords":
            len(best_keywords),
        }

        logger.info(
            "Full SEO analysis completed."
        )

        return result