"""
Enterprise SEO Intelligence Pipeline v3
=======================================

Next-generation SEO orchestration engine.

Major Improvements:
-------------------
✓ spaCy semantic pipeline integration
✓ trafilatura competitor intelligence
✓ garbage keyword elimination
✓ semantic phrase prioritization
✓ cleaner clustering
✓ resilient execution architecture
✓ safer serialization
✓ NLP-enhanced validation
✓ production-safe metrics
✓ semantic deduplication
✓ smarter ranking pipeline
✓ scalable orchestration

Architecture:
-------------
Google Suggest
    ↓
SERP Analysis
    ↓
Competitor Intelligence
    ↓
Semantic NLP Extraction
    ↓
Intent + Entity Analysis
    ↓
SEO Scoring
    ↓
Clustering
    ↓
Content Strategy
"""

from __future__ import annotations

import logging
import time

from typing import Any

from apps.keywords.models import KeywordAnalysis

from apps.keywords.services.clustering_service import (
    ClusteringService,
)

from apps.keywords.services.competitor_extractor_service import (
    CompetitorExtractorService,
)

from apps.keywords.services.difficulty_service import (
    DifficultyService,
)

from apps.keywords.services.entity_service import (
    EntityService,
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

from apps.keywords.services.outline_service import (
    OutlineService,
)

from apps.keywords.services.recommendation_service import (
    RecommendationService,
)

from apps.keywords.services.scoring_service import (
    AdvancedScoringService,
)

from apps.keywords.services.serp_service import (
    SERPService,
)


logger = logging.getLogger(__name__)


# =========================================================
# PIPELINE METRICS
# =========================================================

class PipelineMetrics:

    def __init__(self):

        self.timings = {}

        self._start = {}

    def start(
        self,
        stage: str,
    ):

        self._start[stage] = (
            time.perf_counter()
        )

    def end(
        self,
        stage: str,
    ):

        started = self._start.get(
            stage
        )

        if not started:
            return

        duration = (
            time.perf_counter()
            - started
        ) * 1000

        self.timings[stage] = round(
            duration,
            2,
        )

        logger.info(

            "[PIPELINE] %s completed in %.2fms",

            stage,

            duration,
        )

    @property
    def total_duration_ms(
        self,
    ) -> float:

        return round(
            sum(
                self.timings.values()
            ),
            2,
        )


# =========================================================
# SCORE NORMALIZER
# =========================================================

class ScoreNormalizer:

    @staticmethod
    def normalize(
        value: float,
        min_value: float = 0.0,
        max_value: float = 1.0,
    ) -> float:

        if max_value <= min_value:
            return 0.0

        normalized = (
            value - min_value
        ) / (
            max_value - min_value
        )

        return max(
            0.0,
            min(1.0, normalized),
        )


# =========================================================
# MAIN PIPELINE
# =========================================================

class KeywordPipelineService:

    VERSION = "3.0"

    DEFAULT_SERP_RESULTS = 10

    MAX_COMPETITOR_URLS = 5

    MAX_FINAL_KEYWORDS = 50

    CLUSTER_THRESHOLD = 0.55

    # =====================================================
    # NOISE PATTERNS
    # =====================================================

    NOISE_PATTERNS = {

        "opens in new window",
        "uploaded by",
        "save save",
        "document useful",
        "click here",
        "download now",
        "show more",
        "read more",
        "pdf for later",
        "free trial",
        "sign in",
        "login",
    }

    WEAK_WORDS = {

        "check",
        "latest",
        "free",
        "click",
        "visit",
        "website",
        "download",
        "share",
        "document",
    }

    # =====================================================
    # INIT
    # =====================================================

    def __init__(self):

        self.google_service = (
            GoogleSuggestService()
        )

        self.serp_service = (
            SERPService()
        )

        self.competitor_service = (
            CompetitorExtractorService()
        )

        self.intent_service = (
            IntentService()
        )

        self.entity_service = (
            EntityService()
        )

        self.difficulty_service = (
            DifficultyService()
        )

        self.recommendation_service = (
            RecommendationService()
        )

        self.outline_service = (
            OutlineService()
        )

        self.cluster_service = (
            ClusteringService()
        )

        self.scoring_service = (
            AdvancedScoringService()
        )

    # =====================================================
    # HELPERS
    # =====================================================

    @staticmethod
    def ensure_list(
        value: Any,
    ) -> list:

        return (
            value
            if isinstance(value, list)
            else []
        )

    @staticmethod
    def ensure_dict(
        value: Any,
    ) -> dict:

        return (
            value
            if isinstance(value, dict)
            else {}
        )

    @staticmethod
    def clean_keyword(
        keyword: str,
    ) -> str:

        return str(
            keyword
        ).strip().lower()

    @staticmethod
    def save_keyword(
        keyword: str,
    ) -> KeywordAnalysis:

        obj, _ = (
            KeywordAnalysis.objects
            .get_or_create(
                keyword=keyword
            )
        )

        return obj

    # =====================================================
    # CONTEXT
    # =====================================================

    @staticmethod
    def build_context(
        keyword: str,
    ) -> dict:

        return {

            "keyword":
            keyword,

            "google_suggestions":
            [],

            "serp_results":
            [],

            "competitor_data":
            [],

            "semantic_keywords":
            [],

            "validated_competitor_keywords":
            [],

            "related_searches":
            [],

            "people_also_ask":
            [],

            "entities":
            [],

            "entity_hierarchy":
            {},

            "intent":
            "informational",

            "difficulty":
            {},

            "recommendations":
            {},

            "outline":
            {},

            "clusters":
            {},

            "final_keywords":
            [],
        }

    # =====================================================
    # NOISE FILTER
    # =====================================================

    def is_noise(
        self,
        text: str,
    ) -> bool:

        if not text:
            return True

        text = text.lower()

        if text in (
            self.NOISE_PATTERNS
        ):
            return True

        for pattern in (
            self.NOISE_PATTERNS
        ):

            if pattern in text:
                return True

        return False

    # =====================================================
    # VALIDATION
    # =====================================================

    def is_valid_keyword(
        self,
        keyword: str,
    ) -> bool:

        if not keyword:
            return False

        keyword = self.clean_keyword(
            keyword
        )

        if self.is_noise(
            keyword
        ):
            return False

        if len(keyword) < 4:
            return False

        words = keyword.split()

        if len(words) > 10:
            return False

        non_weak = [

            w
            for w in words

            if (
                w not in self.WEAK_WORDS
                and len(w) > 2
            )
        ]

        if len(non_weak) < 1:
            return False

        # repeated spam
        if len(set(words)) < (
            len(words) * 0.5
        ):
            return False

        return True

    # =====================================================
    # DEDUPLICATION
    # =====================================================

    def merge_keywords(
        self,
        keywords: list[str],
    ) -> list[str]:

        cleaned = []

        seen = set()

        for keyword in keywords:

            keyword = self.clean_keyword(
                keyword
            )

            if not (
                self.is_valid_keyword(
                    keyword
                )
            ):
                continue

            tokens = set(
                keyword.split()
            )

            duplicate = False

            for existing in seen:

                existing_tokens = set(
                    existing.split()
                )

                overlap = len(
                    tokens
                    & existing_tokens
                )

                similarity = overlap / max(
                    len(tokens),
                    len(existing_tokens),
                )

                if similarity >= 0.85:

                    duplicate = True

                    break

            if duplicate:
                continue

            seen.add(keyword)

            cleaned.append(
                keyword
            )

        return cleaned

    # =====================================================
    # SEO SCORE COMBINATION
    # =====================================================

    def combine_scores(
        self,
        extractor_score: float,
        service_score: float,
    ) -> float:

        extractor_score = (
            ScoreNormalizer.normalize(
                extractor_score,
                0.0,
                2.0,
            )
        )

        service_score = (
            ScoreNormalizer.normalize(
                service_score,
                0.0,
                1.0,
            )
        )

        combined = (

            extractor_score * 0.45

            +

            service_score * 0.55
        )

        return round(
            max(
                0.0,
                min(1.0, combined),
            ),
            4,
        )

    # =====================================================
    # SEARCH VOLUME
    # =====================================================

    @staticmethod
    def estimate_volume(
        keyword: str,
    ) -> int:

        keyword = keyword.lower()

        score = 100

        boosters = {

            "result": 90,
            "syllabus": 70,
            "vacancy": 100,
            "notification": 90,
            "answer key": 80,
            "admit card": 85,
            "exam date": 60,
            "cutoff": 70,
            "salary": 50,
        }

        for term, boost in (
            boosters.items()
        ):

            if term in keyword:
                score += boost

        if any(
            year in keyword
            for year in (
                "2025",
                "2026",
                "2027",
            )
        ):
            score += 50

        return max(score, 10)

    # =====================================================
    # PRIORITY KEYWORDS
    # =====================================================

    def build_priority_keywords(
        self,
        context: dict,
    ) -> list[str]:

        keywords = []

        keywords.extend(
            context.get(
                "google_suggestions",
                [],
            )
        )

        keywords.extend(
            context.get(
                "related_searches",
                [],
            )
        )

        keywords.extend(
            context.get(
                "people_also_ask",
                [],
            )
        )

        keywords.extend(
            context.get(
                "validated_competitor_keywords",
                [],
            )
        )

        semantic = context.get(
            "semantic_keywords",
            [],
        )

        keywords.extend([

            item.get(
                "keyword",
                "",
            )

            for item in semantic

            if isinstance(
                item,
                dict,
            )
        ])

        return self.merge_keywords(
            keywords
        )

    # =====================================================
    # SORT KEYWORDS
    # =====================================================

    def sort_keywords(
        self,
        keywords: list[str],
        semantic_keywords: list[dict],
    ) -> list[dict]:

        semantic_scores = {

            item.get("keyword", ""):
            item.get("seo_score", 0.0)

            for item in semantic_keywords

            if isinstance(item, dict)
        }

        results = []

        for keyword in keywords:

            try:

                extractor_score = (
                    semantic_scores.get(
                        keyword,
                        0.0,
                    )
                )

                score_data = (
                    self.scoring_service
                    .calculate_advanced_score(
                        keyword
                    )
                )

                service_score = (
                    score_data.seo_score
                    / 100
                )

                final_score = (
                    self.combine_scores(
                        extractor_score,
                        service_score,
                    )
                )

                if any(
                    year in keyword
                    for year in (
                        "2025",
                        "2026",
                        "2027",
                    )
                ):
                    final_score += 0.08

                final_score = min(
                    final_score,
                    1.0,
                )

                results.append({

                    "keyword":
                    keyword,

                    "seo_score":
                    round(
                        final_score,
                        4,
                    ),

                    "confidence_score":
                    round(
                        final_score * 100,
                        2,
                    ),

                    "extractor_score":
                    extractor_score,

                    "service_score":
                    round(
                        service_score,
                        4,
                    ),

                    "volume":
                    self.estimate_volume(
                        keyword
                    ),

                    "difficulty":
                    getattr(
                        score_data,
                        "difficulty",
                        "medium",
                    ),

                    "intent":
                    getattr(
                        score_data,
                        "intent",
                        "informational",
                    ),

                    "journey_stage":
                    getattr(
                        score_data,
                        "journey_stage",
                        "awareness",
                    ),

                    "temporal":
                    getattr(
                        score_data,
                        "temporal",
                        "ongoing",
                    ),

                    "serp_type":
                    getattr(
                        score_data,
                        "serp_type",
                        "mixed",
                    ),
                })

            except Exception:

                logger.exception(
                    "Keyword scoring failed: %s",
                    keyword,
                )

        results.sort(

            key=lambda x: (
                x["seo_score"],
                x["volume"],
            ),

            reverse=True,
        )

        return results[
            :self.MAX_FINAL_KEYWORDS
        ]

    # =====================================================
    # MAIN PIPELINE
    # =====================================================

    def run(
        self,
        keyword: str,
    ) -> dict[str, Any]:

        metrics = PipelineMetrics()

        logger.info(
            "=== SEO Pipeline v%s Started ===",
            self.VERSION,
        )

        keyword = str(keyword).strip()

        if not keyword:
            return {}

        # =================================================
        # SAVE KEYWORD
        # =================================================

        metrics.start(
            "save_keyword"
        )

        keyword_obj = (
            self.save_keyword(
                keyword
            )
        )

        metrics.end(
            "save_keyword"
        )

        context = self.build_context(
            keyword
        )

        # =================================================
        # GOOGLE SUGGEST
        # =================================================

        metrics.start(
            "google_suggest"
        )

        try:

            suggestions = (
                self.google_service
                .get_suggestions(
                    keyword
                )
            )

            context[
                "google_suggestions"
            ] = self.ensure_list(
                suggestions
            )

        except Exception:

            logger.exception(
                "Google suggest failed"
            )

        metrics.end(
            "google_suggest"
        )

        # =================================================
        # SERP ANALYSIS
        # =================================================

        metrics.start(
            "serp_analysis"
        )

        try:

            serp_results = (
                self.serp_service.search(
                    keyword=keyword,
                    max_results=(
                        self.DEFAULT_SERP_RESULTS
                    ),
                )
            )

            context[
                "serp_results"
            ] = self.ensure_list(
                serp_results
            )

        except Exception:

            logger.exception(
                "SERP analysis failed"
            )

        metrics.end(
            "serp_analysis"
        )

        # =================================================
        # COMPETITOR EXTRACTION
        # =================================================

        metrics.start(
            "competitor_extraction"
        )

        try:

            competitor_urls = [

                item.get("url", "")

                for item in context[
                    "serp_results"
                ]

                if item.get("url")
            ]

            competitor_data = (
                self.competitor_service
                .extract_urls(

                    competitor_urls[
                        :self.MAX_COMPETITOR_URLS
                    ]
                )
            )

            cleaned_competitors = []

            validated_keywords = []

            for item in competitor_data:

                semantic = [

                    kw

                    for kw in item.get(
                        "semantic_keywords",
                        [],
                    )

                    if not self.is_noise(
                        kw
                    )
                ]

                item[
                    "semantic_keywords"
                ] = semantic

                validated_keywords.extend(
                    semantic
                )

                cleaned_competitors.append(
                    item
                )

            context[
                "competitor_data"
            ] = cleaned_competitors

            context[
                "validated_competitor_keywords"
            ] = self.merge_keywords(
                validated_keywords
            )

        except Exception:

            logger.exception(
                "Competitor extraction failed"
            )

        metrics.end(
            "competitor_extraction"
        )

        # =================================================
        # SEMANTIC NLP EXTRACTION
        # =================================================

        metrics.start(
            "semantic_extraction"
        )

        try:

            combined_results = list(
                context[
                    "serp_results"
                ]
            )

            combined_results.extend([

                {

                    "title": " ".join(
                        item.get(
                            "headings",
                            [],
                        )
                    ),

                    "description": " ".join(
                        item.get(
                            "semantic_keywords",
                            [],
                        )
                    ),

                    "headings": item.get(
                        "headings",
                        [],
                    ),
                }

                for item in context[
                    "competitor_data"
                ]
            ])

            semantic_keywords = (
                KeywordExtractor
                .extract_keywords_rich(

                    combined_results,

                    seed_keyword=keyword,
                )
            )

            context[
                "semantic_keywords"
            ] = self.ensure_list(
                semantic_keywords
            )

        except Exception:

            logger.exception(
                "Semantic extraction failed"
            )

        metrics.end(
            "semantic_extraction"
        )

        # =================================================
        # AUXILIARY ANALYSIS
        # =================================================

        metrics.start(
            "auxiliary_analysis"
        )

        try:

            people_also_ask = []

            related_searches = []

            for result in context[
                "serp_results"
            ]:

                people_also_ask.extend(
                    result.get(
                        "questions",
                        [],
                    )
                )

                related_searches.extend(
                    result.get(
                        "related_searches",
                        [],
                    )
                )

            context[
                "people_also_ask"
            ] = self.ensure_list(
                people_also_ask
            )

            context[
                "related_searches"
            ] = self.ensure_list(
                related_searches
            )

            # =============================================
            # ENTITY EXTRACTION
            # =============================================

            entities = (
                self.entity_service.extract(
                    context[
                        "serp_results"
                    ]
                )
            )

            context["entities"] = (
                self.ensure_list(
                    entities
                )
            )

            # =============================================
            # ENTITY HIERARCHY
            # =============================================

            hierarchy = (
                KeywordExtractor
                .extract_entity_hierarchy(

                    phrase=keyword,

                    seed_tokens=frozenset(
                        keyword.lower().split()
                    ),
                )
            )

            context[
                "entity_hierarchy"
            ] = hierarchy.to_dict()

            # =============================================
            # INTENT
            # =============================================

            intent_data = (
                self.intent_service.analyze(
                    keyword
                )
            )

            context["intent"] = (
                intent_data.get(
                    "intent",
                    "informational",
                )
            )

            # =============================================
            # DIFFICULTY
            # =============================================

            difficulty = (
                self.difficulty_service
                .calculate(

                    keyword,

                    serp_results=context[
                        "serp_results"
                    ],
                )
            )

            context["difficulty"] = (
                self.ensure_dict(
                    difficulty
                )
            )

        except Exception:

            logger.exception(
                "Auxiliary analysis failed"
            )

        metrics.end(
            "auxiliary_analysis"
        )

        # =================================================
        # FINAL KEYWORDS
        # =================================================

        metrics.start(
            "final_keywords"
        )

        try:

            merged_keywords = (
                self.build_priority_keywords(
                    context
                )
            )

            context[
                "final_keywords"
            ] = self.sort_keywords(

                merged_keywords,

                context.get(
                    "semantic_keywords",
                    [],
                ),
            )

        except Exception:

            logger.exception(
                "Final keyword generation failed"
            )

        metrics.end(
            "final_keywords"
        )

        # =================================================
        # CONTENT STRATEGY
        # =================================================

        metrics.start(
            "content_strategy"
        )

        try:

            recommendations = (
                self.recommendation_service
                .generate(

                    keyword,

                    difficulty_data=context[
                        "difficulty"
                    ],
                )
            )

            context[
                "recommendations"
            ] = self.ensure_dict(
                recommendations
            )

            outline = (
                self.outline_service
                .generate(

                    keyword,

                    recommendation_data=(
                        recommendations
                    ),
                )
            )

            context["outline"] = (
                self.ensure_dict(
                    outline
                )
            )

        except Exception:

            logger.exception(
                "Content strategy failed"
            )

        metrics.end(
            "content_strategy"
        )

        # =================================================
        # CLUSTERING
        # =================================================

        metrics.start(
            "clustering"
        )

        try:

            keyword_list = [

                item.get(
                    "keyword",
                    "",
                )

                for item in context[
                    "final_keywords"
                ]
            ]

            clusters = (
                self.cluster_service
                .cluster_keywords(

                    keywords=keyword_list,

                    similarity_threshold=(
                        self.CLUSTER_THRESHOLD
                    ),

                    min_cluster_size=2,
                )
            )

            context["clusters"] = (
                self.ensure_dict(
                    clusters
                )
            )

        except Exception:

            logger.exception(
                "Clustering failed"
            )

        metrics.end(
            "clustering"
        )

        # =================================================
        # SUMMARY
        # =================================================

        keyword_data = (
            self.ensure_list(
                context[
                    "final_keywords"
                ]
            )
        )

        avg_confidence = 0.0

        if keyword_data:

            avg_confidence = round(

                sum(

                    item.get(
                        "confidence_score",
                        0,
                    )

                    for item in keyword_data
                )

                / len(keyword_data),

                2,
            )

        high_opportunity_count = sum(

            1

            for item in keyword_data

            if item.get(
                "seo_score",
                0,
            ) >= 0.7
        )

        logger.info(

            "=== SEO Pipeline Completed in %.2fms ===",

            metrics.total_duration_ms,
        )

        return {

            "version":
            self.VERSION,

            "keyword":
            keyword,

            "keyword_id":
            keyword_obj.id,

            "suggestions": [

                item.get(
                    "keyword",
                    ""
                )

                for item in keyword_data
            ],

            "keyword_data":
            keyword_data,

            "semantic_keywords":
            self.ensure_list(
                context[
                    "semantic_keywords"
                ]
            )[:10],

            "related_searches":
            context[
                "related_searches"
            ],

            "people_also_ask":
            context[
                "people_also_ask"
            ],

            "entities":
            context[
                "entities"
            ],

            "entity_hierarchy":
            context.get(
                "entity_hierarchy",
                {},
            ),

            "intent":
            context[
                "intent"
            ],

            "difficulty":
            context[
                "difficulty"
            ],

            "recommendations":
            context[
                "recommendations"
            ],

            "outline":
            context[
                "outline"
            ],

            "clusters":
            context[
                "clusters"
            ],

            "avg_confidence":
            avg_confidence,

            "high_opportunity_count":
            high_opportunity_count,

            "metrics": {

                "stage_timings":
                metrics.timings,

                "total_duration_ms":
                metrics.total_duration_ms,
            },
        }
