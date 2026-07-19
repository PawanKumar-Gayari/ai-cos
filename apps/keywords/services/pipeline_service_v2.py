"""
Enterprise SEO Intelligence Pipeline v1.2 - Highly Calibrated
-------------------------------------------------------------------
UPDATES:
1. Revised WEAK_WORDS
2. Added estimate_volume() logic
3. Recalibrated Score Weights (0.4/0.6)
4. Semantic Deduplication in merge_keywords
5. Dynamic Volume Estimation
6. Tightened Clustering Threshold (0.55)
7. Final Quality Boost Logic (Length & Year)
"""

from __future__ import annotations

import logging
import time
from typing import Any

from apps.keywords.models import KeywordAnalysis
from apps.keywords.services.clustering_service import ClusteringService
from apps.keywords.services.competitor_extractor_service import CompetitorExtractorService
from apps.keywords.services.difficulty_service import DifficultyService
from apps.keywords.services.entity_service import EntityService
from apps.keywords.services.google_suggest import GoogleSuggestService
from apps.keywords.services.intent_service import IntentService
from apps.keywords.services.keyword_extractor import KeywordExtractor
from apps.keywords.services.outline_service import OutlineService
from apps.keywords.services.recommendation_service import RecommendationService
from apps.keywords.services.scoring_service import AdvancedScoringService
from apps.keywords.services.serp_service import SERPService

logger = logging.getLogger(__name__)


class PipelineMetrics:
    def __init__(self) -> None:
        self.stage_timings: dict[str, float] = {}
        self.stage_start_times: dict[str, float] = {}

    def start_stage(self, stage_name: str) -> None:
        self.stage_start_times[stage_name] = time.perf_counter()

    def end_stage(self, stage_name: str) -> None:
        if stage_name not in self.stage_start_times:
            return
        start = self.stage_start_times[stage_name]
        duration_ms = (time.perf_counter() - start) * 1000
        self.stage_timings[stage_name] = duration_ms
        logger.info(f"Stage '{stage_name}' completed in {duration_ms:.2f}ms")

    def get_total_duration_ms(self) -> float:
        return sum(self.stage_timings.values())


class ScoringNormalizer:
    @staticmethod
    def normalize_score(score: float, min_val: float = 0.0, max_val: float = 1.0) -> float:
        if score < min_val:
            return 0.0
        if score > max_val:
            return 1.0
        if max_val == min_val:
            return 0.5
        normalized = (score - min_val) / (max_val - min_val)
        return max(0.0, min(1.0, normalized))


class KeywordPipelineService:
    VERSION = "1.2"
    DEFAULT_SERP_RESULTS = 10
    DEFAULT_CLUSTER_COUNT = 5
    MAX_FINAL_KEYWORDS = 50
    MAX_COMPETITOR_URLS = 5

    # 1. UPDATE WEAK WORDS 🔥
    WEAK_WORDS = {
        "check",
        "direct",
        "now",
        "latest",
        "free",
        "click",
        "visit",
        "link",
    }

    def __init__(self) -> None:
        self.google_service = GoogleSuggestService()
        self.cluster_service = ClusteringService()
        self.serp_service = SERPService()
        self.difficulty_service = DifficultyService()
        self.recommendation_service = RecommendationService()
        self.outline_service = OutlineService()
        self.intent_service = IntentService()
        self.entity_service = EntityService()
        self.scoring_service = AdvancedScoringService()
        self.competitor_service = CompetitorExtractorService()

    @staticmethod
    def save_keyword(keyword: str) -> KeywordAnalysis:
        obj, _ = KeywordAnalysis.objects.get_or_create(keyword=keyword)
        return obj

    @staticmethod
    def ensure_list(value: Any) -> list:
        return value if isinstance(value, list) else []

    @staticmethod
    def ensure_dict(value: Any) -> dict:
        return value if isinstance(value, dict) else {}

    @staticmethod
    def clean_keyword(keyword: str) -> str:
        return str(keyword).strip().lower()

    # 2. ADD VOLUME ESTIMATOR 🔥
    @staticmethod
    def estimate_volume(keyword: str) -> int:
        keyword = keyword.lower()
        score = 100

        high_intent_terms = {
            "result": 80,
            "admit card": 70,
            "answer key": 75,
            "syllabus": 60,
            "cut off": 65,
            "notification": 85,
            "vacancy": 90,
            "recruitment": 90,
            "apply online": 95,
            "exam date": 60,
        }

        for term, boost in high_intent_terms.items():
            if term in keyword:
                score += boost

        if "2025" in keyword or "2026" in keyword:
            score += 40

        if len(keyword.split()) >= 6:
            score -= 25

        return max(score, 10)

    def is_valid_keyword(self, keyword: str) -> bool:
        if not keyword:
            return False
        keyword = str(keyword).strip().lower()
        if len(keyword) < 3:
            return False
        words = keyword.split()
        if len(words) > 1:
            duplicate_ratio = len(set(words)) / len(words)
            if duplicate_ratio < 0.7:
                return False
        if len(words) > 12:
            return False
        if sum(word.isdigit() for word in words) > 3:
            return False
        if any(char * 4 in keyword for char in "abcdefghijklmnopqrstuvwxyz"):
            return False
        if any(fragment in keyword for fragment in [".com", ".in", "http", "www"]):
            return False
        semantic_words = [w for w in words if not w.isdigit() and len(w) > 2]
        if len(semantic_words) < 2:
            return False
        if all(w in self.WEAK_WORDS for w in semantic_words):
            return False
        return True

    # 4. ADD SEMANTIC DEDUPLICATION 🔥
    def merge_keywords(self, keywords: list[str]) -> list[str]:
        cleaned = []
        seen = set()

        for keyword in keywords:
            keyword = self.clean_keyword(keyword)

            if not self.is_valid_keyword(keyword):
                continue

            duplicate_found = False
            keyword_tokens = set(keyword.split())

            for existing in seen:
                existing_tokens = set(existing.split())
                
                # Jaccard-like token overlap
                overlap = len(keyword_tokens & existing_tokens)
                similarity = overlap / max(len(keyword_tokens), len(existing_tokens))

                if similarity >= 0.85:
                    duplicate_found = True
                    break

            if duplicate_found:
                continue

            seen.add(keyword)
            cleaned.append(keyword)

        return cleaned

    def build_priority_keywords(
        self, context: dict, validated_competitor_keywords: list
    ) -> list[str]:
        priority_keywords = []
        priority_keywords.extend(context.get("google_suggestions", []))
        priority_keywords.extend(context.get("related_searches", []))
        priority_keywords.extend(context.get("people_also_ask", []))
        priority_keywords.extend(validated_competitor_keywords)
        
        semantic_kw = context.get("semantic_keywords", [])
        priority_keywords.extend(
            [
                item.get("keyword", "")
                for item in semantic_kw
                if isinstance(item, dict) and item.get("keyword")
            ]
        )
        return self.merge_keywords(priority_keywords)

    # 3. IMPROVE SCORE COMBINATION 🔥
    def combine_scores(self, extractor_score: float, service_score: float) -> float:
        norm_extractor = ScoringNormalizer.normalize_score(extractor_score, 0.0, 2.0)
        norm_service = ScoringNormalizer.normalize_score(service_score, 0.0, 1.0)
        
        # New weighted distribution
        combined = (
            norm_extractor * 0.4
            + norm_service * 0.6
        )
        return min(1.0, max(0.0, combined))

    def sort_keywords(
        self, keywords: list[str], semantic_keywords: list[dict]
    ) -> list[dict]:
        extractor_scores = {
            item.get("keyword", ""): item.get("seo_score", 0.0)
            for item in semantic_keywords
            if isinstance(item, dict) and item.get("keyword")
        }
        scored_keywords = []

        for keyword in keywords:
            try:
                extractor_score = extractor_scores.get(keyword, 0.0)
                score_data = self.scoring_service.calculate_advanced_score(keyword)
                service_score = score_data.seo_score / 100
                combined_score = self.combine_scores(extractor_score, service_score)

                # 7. ADD FINAL QUALITY BOOST 🔥
                if len(keyword.split()) >= 5:
                    combined_score += 0.05

                if "2025" in keyword or "2026" in keyword:
                    combined_score += 0.08

                combined_score = min(combined_score, 1.0)

                scored_keywords.append({
                    "keyword": keyword,
                    "seo_score": combined_score,
                    "confidence_score": round(combined_score * 100, 2),
                    "extractor_score": extractor_score,
                    "service_score": service_score,               
                    # 5. UPDATE KEYWORD SCORING (VOLUME) 🔥
                    "volume": self.estimate_volume(keyword),
                    "difficulty": getattr(score_data, "difficulty", "medium"),
                    "intent": getattr(score_data, "intent", "informational"),
                    "journey_stage": getattr(score_data, "journey_stage", "awareness"),
                    "temporal": getattr(score_data, "temporal", "ongoing"),
                    "serp_type": getattr(score_data, "serp_type", "mixed"),
                })
            except Exception as error:
                logger.exception(f"Failed to score keyword '{keyword}': {str(error)}")
                continue

        scored_keywords.sort(key=lambda x: (x["seo_score"], x["volume"]), reverse=True)
        return scored_keywords[: self.MAX_FINAL_KEYWORDS]

    @staticmethod
    def build_context(keyword: str) -> dict[str, Any]:
        return {
            "keyword": keyword,
            "google_suggestions": [],
            "serp_results": [],
            "competitor_data": [],
            "validated_competitor_keywords": [],
            "semantic_keywords": [],
            "related_searches": [],
            "people_also_ask": [],
            "entities": [],
            "entity_hierarchy": {},
            "intent": "",
            "difficulty": {},
            "recommendations": {},
            "outline": {},
            "clusters": {},
            "final_keywords": [],
        }

    def run(self, keyword: str) -> dict[str, Any]:
        metrics = PipelineMetrics()
        logger.info(f"=== SEO Pipeline v{self.VERSION} Started ===")
        
        keyword = str(keyword).strip()
        if not keyword:
            return {}

        metrics.start_stage("save_keyword")
        keyword_obj = self.save_keyword(keyword)
        metrics.end_stage("save_keyword")

        context = self.build_context(keyword)

        # 1. Google Suggest
        metrics.start_stage("google_suggest")
        try:
            suggestions = self.google_service.get_suggestions(keyword)
            context["google_suggestions"] = self.ensure_list(suggestions)
        except Exception as error:
            logger.exception(f"Suggestion error: {str(error)}")
        metrics.end_stage("google_suggest")

        # 2. SERP Analysis
        metrics.start_stage("serp_analysis")
        try:
            serp_results = self.serp_service.search(
                keyword=keyword, max_results=self.DEFAULT_SERP_RESULTS
            )
            context["serp_results"] = self.ensure_list(serp_results)
        except Exception as error:
            logger.exception(f"SERP analysis failed: {str(error)}")
        metrics.end_stage("serp_analysis")

        # 3. Competitor Extraction
        metrics.start_stage("competitor_extraction")
        try:
            competitor_urls = [
                item.get("url", "")
                for item in context["serp_results"]
                if item.get("url")
            ]
            competitor_data = self.competitor_service.extract_urls(
                competitor_urls[: self.MAX_COMPETITOR_URLS]
            )
            context["competitor_data"] = self.ensure_list(competitor_data)

            validated_kws = []
            for item in competitor_data:
                validated_kws.extend(item.get("semantic_keywords", []))
            context["validated_competitor_keywords"] = self.merge_keywords(validated_kws)
        except Exception as error:
            logger.exception(f"Competitor extraction failed: {str(error)}")
        metrics.end_stage("competitor_extraction")

        # 4. Semantic Extraction
        metrics.start_stage("semantic_extraction")
        try:
            combined_results = list(context["serp_results"])
            for item in context["competitor_data"]:
                combined_results.append({
                    "title": " ".join(item.get("headings", [])),
                    "description": " ".join(item.get("semantic_keywords", [])),
                })
            context["semantic_keywords"] = self.ensure_list(
                KeywordExtractor.extract_keywords_rich(
                    combined_results, seed_keyword=keyword
                )
            )
        except Exception as error:
            logger.exception(f"Semantic extraction failed: {str(error)}")
        metrics.end_stage("semantic_extraction")

        # 5. Auxiliary Data
        metrics.start_stage("auxiliary_extraction")
        try:
            paa, rel = [], []
            for result in context["serp_results"]:
                paa.extend(result.get("questions", []))
                rel.extend(result.get("related_searches", []))
            context["people_also_ask"] = self.ensure_list(paa)
            context["related_searches"] = self.ensure_list(rel)

            context["entities"] = self.ensure_list(
                self.entity_service.extract(context["serp_results"])
            )
            context["entity_hierarchy"] = (
                KeywordExtractor.extract_entity_hierarchy(
                    phrase=keyword,
                    seed_tokens=keyword.split(),
                )
            )

            intent_data = self.intent_service.analyze(keyword)
            context["intent"] = intent_data.get("intent", "informational")

            context["difficulty"] = self.ensure_dict(
                self.difficulty_service.calculate(
                    keyword, serp_results=context["serp_results"]
                )
            )
        except Exception as error:
            logger.exception(f"Auxiliary analysis failed: {str(error)}")
        metrics.end_stage("auxiliary_extraction")

        # 6. Final Keyword Merge & Sort
        metrics.start_stage("final_keyword_merge")
        try:
            merged = self.build_priority_keywords(
                context, context.get("validated_competitor_keywords", [])
            )
            context["final_keywords"] = self.sort_keywords(
                merged, context["semantic_keywords"]
            )
        except Exception as error:
            logger.exception(f"Keyword merge failed: {str(error)}")
        metrics.end_stage("final_keyword_merge")

        # 7. Content Strategy
        metrics.start_stage("content_strategy")
        try:
            recs = self.recommendation_service.generate(
                keyword, difficulty_data=context["difficulty"]
            )
            context["recommendations"] = self.ensure_dict(recs)
            context["outline"] = self.ensure_dict(
                self.outline_service.generate(keyword, recommendation_data=recs)
            )
        except Exception as error:
            logger.exception(f"Strategy generation failed: {str(error)}")
        metrics.end_stage("content_strategy")

        # 8. IMPROVE CLUSTERING 🔥
        metrics.start_stage("clustering")
        try:
            final_keyword_list = [
                item.get("keyword", "") for item in context["final_keywords"]
            ]
            clusters = self.cluster_service.cluster_keywords(
                keywords=final_keyword_list,
                similarity_threshold=0.55, # Updated threshold
                min_cluster_size=2,
            )
            context["clusters"] = self.ensure_dict(clusters)
        except Exception as error:
            logger.exception(f"Clustering failed: {str(error)}")
        metrics.end_stage("clustering")

        # 9. Meta-Summary
        avg_confidence = 0.0
        if context["final_keywords"]:
            avg_confidence = round(
                sum(item.get("confidence_score", 0) for item in context["final_keywords"])
                / len(context["final_keywords"]),
                2,
            )

        high_opportunity_count = sum(
            1 for item in context["final_keywords"] if item.get("seo_score", 0) >= 0.7
        )

        total_duration = metrics.get_total_duration_ms()
        logger.info(f"=== SEO Pipeline Completed in {total_duration:.2f}ms ===")

        return {
            "version": self.VERSION,
            "keyword": keyword,
            "keyword_id": keyword_obj.id,
            "suggestions": [item["keyword"] for item in context["final_keywords"]],
            "keyword_data": context["final_keywords"],
            "semantic_keywords": context["semantic_keywords"][:10],
            "related_searches": context["related_searches"],
            "people_also_ask": context["people_also_ask"],
            "entities": context["entities"],
            "entity_hierarchy": context.get("entity_hierarchy", {}),
            "intent": context["intent"],
            "difficulty": context["difficulty"],
            "recommendations": context["recommendations"],
            "outline": context["outline"],
            "clusters": context["clusters"],
            "avg_confidence": avg_confidence,
            "high_opportunity_count": high_opportunity_count,
            "metrics": {
                "stage_timings": metrics.stage_timings,
                "total_duration_ms": total_duration,
            },
        }