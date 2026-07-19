"""
Production-Grade SEO Clustering Engine v1.1
==========================================

FINAL REFINEMENT PASS:
1. Token-aware boundary matching (no substrings)
2. Weighted similarity (entity, journey, temporal, phrase-chains)
3. Semantic coherence confidence scoring
4. Phrase-chain ecosystem intelligence
5. Long-tail specificity preservation
6. Contradiction detection

Deterministic heuristics only - no ML, embeddings, or vectors.
"""

from __future__ import annotations

import logging
import re
from collections import Counter, defaultdict
from dataclasses import dataclass
from enum import Enum
from typing import Final, Any
from math import log

logger = logging.getLogger(__name__)

# =====================================================
# JOURNEY STAGES
# =====================================================

class UserJourneyStage(str, Enum):
    """User journey stages in exam cycle."""
    
    NOTIFICATION = "notification"
    ELIGIBILITY = "eligibility"
    SYLLABUS = "syllabus"
    ADMIT_CARD = "admit_card"
    ANSWER_KEY = "answer_key"
    RESULT = "result"
    COUNSELING = "counseling"


class ContentFormat(str, Enum):
    """Predicted content format."""
    
    OFFICIAL = "official"
    BLOG = "blog"
    VIDEO = "video"
    PDF = "pdf"
    FORUM = "forum"


# =====================================================
# TOKEN BOUNDARY MATCHER (Refined)
# =====================================================

class TokenBoundaryMatcher:
    """
    Match tokens with proper word boundaries.
    No substring matching.
    """
    
    @staticmethod
    def tokenize(keyword: str) -> list[str]:
        """Tokenize into words."""
        return keyword.lower().split()
    
    @staticmethod
    def phrase_in_keyword(
        phrase: str,
        keyword: str,
    ) -> bool:
        """
        Check if phrase matches with word boundaries.
        
        Examples:
        - "admit card" matches in "ssc gd admit card 2025" ✓
        - "admit" does NOT match in "unadmitted" ✗
        """
        
        keyword_lower = keyword.lower()
        phrase_lower = phrase.lower()
        
        # Escape special regex chars
        escaped_phrase = re.escape(phrase_lower)
        
        # Word boundary pattern
        pattern = rf"\b{escaped_phrase}\b"
        
        return bool(
            re.search(
                pattern,
                keyword_lower,
            )
        )


# =====================================================
# STOPWORD MANAGEMENT
# =====================================================

class SEOStopwordManager:
    """Intelligent stopword management."""
    
    NOISE_WORDS: Final[set[str]] = {
        "the", "a", "an", "is", "are", "was", "be",
        "do", "does", "did", "have", "has",
        "in", "on", "at", "to", "of", "and", "or",
        "but", "not", "what", "which", "who",
        "by", "from", "with", "as",
    }
    
    SEO_KEYWORDS: Final[set[str]] = {
        "official", "latest", "new", "best", "top",
        "free", "easy", "complete", "guide", "tutorial",
        "review", "tips", "syllabus", "pattern",
        "strategy", "download", "pdf", "notification",
        "certified", "authorized", "verified",
        "government",
    }
    
    @staticmethod
    def is_stopword(word: str) -> bool:
        """Check if word should be removed."""
        word_lower = word.lower()
        if word_lower in SEOStopwordManager.SEO_KEYWORDS:
            return False
        return word_lower in SEOStopwordManager.NOISE_WORDS


# =====================================================
# PHRASE-CHAIN ECOSYSTEM MATCHER (New)
# =====================================================

class PhraseChainMatcher:
    """
    Detect high-value phrase chains.
    """
    
    # High-value phrase chains
    PHRASE_CHAINS: Final[dict[str, float]] = {
        # Answer key chains
        "answer key pdf": 1.0,
        "answer key download": 0.95,
        "official answer key": 0.90,
        
        # Admit card chains
        "admit card download": 1.0,
        "admit card pdf": 0.95,
        "download admit card": 0.90,
        
        # Notification chains
        "official notification": 0.90,
        "notification pdf": 0.85,
        "latest notification": 0.80,
        
        # Exam date chains
        "exam date 2026": 0.90,
        "exam date 2025": 0.85,
        "exam date announced": 0.80,
        
        # Result chains
        "result declared": 0.85,
        "results announced": 0.85,
        "official result": 0.80,
    }
    
    @staticmethod
    def extract_phrase_chains(
        keyword: str,
    ) -> set[str]:
        """Extract phrase chains from keyword."""
        
        chains = set()
        
        for chain in PhraseChainMatcher.PHRASE_CHAINS.keys():
            if TokenBoundaryMatcher.phrase_in_keyword(
                chain,
                keyword,
            ):
                chains.add(chain)
        
        return chains
    
    @staticmethod
    def calculate_chain_weight(
        chains_a: set[str],
        chains_b: set[str],
    ) -> float:
        """
        Calculate phrase-chain overlap weight (0-1).
        """
        
        if not chains_a and not chains_b:
            return 1.0
        
        if not chains_a or not chains_b:
            return 0.0
        
        overlap = chains_a & chains_b
        
        if not overlap:
            return 0.0
        
        # Sum of weights
        overlap_weight = sum(
            PhraseChainMatcher.PHRASE_CHAINS[chain]
            for chain in overlap
        )
        
        max_weight = sum(
            PhraseChainMatcher.PHRASE_CHAINS[chain]
            for chain in (chains_a | chains_b)
        )
        
        return overlap_weight / max_weight if max_weight > 0 else 0.0


# =====================================================
# JOURNEY STAGE DETECTOR (Unchanged)
# =====================================================

class JourneyStageDetector:
    """Detect user journey stage."""
    
    STAGE_KEYWORDS: Final[
        dict[UserJourneyStage, set[str]]
    ] = {
        UserJourneyStage.NOTIFICATION: {
            "notification", "official notification",
            "notice", "announcement", "released",
        },
        UserJourneyStage.ELIGIBILITY: {
            "eligibility", "eligible", "qualification",
            "requirements", "criteria", "age limit",
        },
        UserJourneyStage.SYLLABUS: {
            "syllabus", "curriculum", "topics",
            "course content", "subjects", "chapters",
        },
        UserJourneyStage.ADMIT_CARD: {
            "admit card", "admission card",
            "hall ticket", "entry pass",
        },
        UserJourneyStage.ANSWER_KEY: {
            "answer key", "official answer",
            "solution", "answers", "answer sheet",
        },
        UserJourneyStage.RESULT: {
            "result", "score", "marks", "scorecard",
            "declared", "announced", "results out",
        },
        UserJourneyStage.COUNSELING: {
            "counseling", "counselling", "merit list",
            "cutoff", "selection", "interview",
        },
    }
    
    @staticmethod
    def detect_stage(
        keyword: str,
    ) -> UserJourneyStage | None:
        """Detect journey stage."""
        
        for stage in [
            UserJourneyStage.NOTIFICATION,
            UserJourneyStage.ADMIT_CARD,
            UserJourneyStage.ANSWER_KEY,
            UserJourneyStage.RESULT,
            UserJourneyStage.COUNSELING,
            UserJourneyStage.SYLLABUS,
            UserJourneyStage.ELIGIBILITY,
        ]:
            keywords = JourneyStageDetector.STAGE_KEYWORDS[stage]
            
            for keyword_phrase in keywords:
                if TokenBoundaryMatcher.phrase_in_keyword(
                    keyword_phrase,
                    keyword,
                ):
                    return stage
        
        return None


# =====================================================
# TEMPORAL CLASSIFIER
# =====================================================

class TemporalClassifier:
    """Classify temporal aspect."""
    
    TEMPORAL_PATTERNS: Final[dict[str, set[str]]] = {
        "future_2026": {"2026", "2025 onwards"},
        "current_2025": {"2025", "this year"},
        "recent_2024": {"2024", "last year"},
        "latest": {"latest", "new", "recent"},
        "ongoing": {"current", "ongoing", "now"},
        "old": {"previous", "old", "past", "archived"},
    }
    
    @staticmethod
    def classify_temporal(
        keyword: str,
    ) -> str:
        """Classify temporal aspect."""
        
        for temporal_class, patterns in (
            TemporalClassifier.TEMPORAL_PATTERNS.items()
        ):
            for pattern in patterns:
                if TokenBoundaryMatcher.phrase_in_keyword(
                    pattern,
                    keyword,
                ):
                    return temporal_class
        
        return "timeless"


# =====================================================
# CONTRADICTION DETECTOR (New)
# =====================================================

class ContradictionDetector:
    """
    Detect contradictory signals in keywords.
    """
    
    CONTRADICTIONS: Final[list[tuple[set[str], set[str]]]] = [
        # latest vs archived/old
        ({"latest", "new", "recent"}, {"archived", "old", "previous"}),
        # official vs unofficial
        ({"official", "authorized", "government"}, {"unofficial", "unconfirmed"}),
        # current vs past
        ({"2025", "current", "ongoing"}, {"2024", "2023", "past"}),
    ]
    
    @staticmethod
    def detect_contradictions(
        keyword: str,
    ) -> bool:
        """
        Detect contradictory signals.
        
        Returns True if contradictions found.
        """
        
        keyword_lower = keyword.lower()
        
        for positive_set, negative_set in (
            ContradictionDetector.CONTRADICTIONS
        ):
            has_positive = any(
                TokenBoundaryMatcher.phrase_in_keyword(
                    word,
                    keyword,
                )
                for word in positive_set
            )
            
            has_negative = any(
                TokenBoundaryMatcher.phrase_in_keyword(
                    word,
                    keyword,
                )
                for word in negative_set
            )
            
            if has_positive and has_negative:
                logger.debug(
                    f"Contradiction detected in: {keyword}"
                )
                return True
        
        return False


# =====================================================
# ENTITY DETECTOR
# =====================================================

class EntityDetector:
    """Detect exam entities."""
    
    ENTITIES: Final[dict[str, set[str]]] = {
        "gate": {"gate", "gate exam"},
        "upsc": {"upsc", "ias", "ips"},
        "ssc": {"ssc", "ssc gd", "ssc cgl"},
        "ugc_net": {"ugc net", "net exam"},
        "ibps": {"ibps", "ibps po", "ibps clerk"},
        "neet": {"neet", "neet exam"},
        "jee": {"jee", "jee main", "jee advanced"},
        "rpsc": {"rpsc", "rajasthan psc"},
        "reet": {"reet", "teacher exam"},
    }
    
    @staticmethod
    def detect_entity(
        keyword: str,
    ) -> str | None:
        """Detect exam entity."""
        
        for entity, patterns in (
            EntityDetector.ENTITIES.items()
        ):
            for pattern in patterns:
                if TokenBoundaryMatcher.phrase_in_keyword(
                    pattern,
                    keyword,
                ):
                    return entity
        
        return None


# =====================================================
# WEIGHTED SIMILARITY CALCULATOR (Refined)
# =====================================================

class WeightedSimilarityCalculator:
    """
    Calculate weighted similarity with multiple factors.
    """
    
    @staticmethod
    def tokenize_semantic(
        keyword: str,
    ) -> set[str]:
        """Tokenize, removing stopwords."""
        
        tokens = TokenBoundaryMatcher.tokenize(keyword)
        
        return {
            t for t in tokens
            if not SEOStopwordManager.is_stopword(t)
        }
    
    @staticmethod
    def calculate_weighted_similarity(
        keyword_a: str,
        keyword_b: str,
    ) -> float:
        """
        Calculate weighted similarity (0-1).
        
        Factors:
        - Entity overlap (0.25 weight)
        - Journey stage overlap (0.25 weight)
        - Temporal alignment (0.20 weight)
        - Phrase-chain similarity (0.20 weight)
        - Token overlap (0.10 weight)
        """
        
        # =============================================
        # Entity overlap (0.25 weight)
        # =============================================
        
        entity_a = EntityDetector.detect_entity(keyword_a)
        entity_b = EntityDetector.detect_entity(keyword_b)
        
        entity_score = 1.0 if (
            entity_a and entity_b and
            entity_a == entity_b
        ) else (0.5 if not entity_a and not entity_b else 0.0)
        
        # =============================================
        # Journey stage overlap (0.25 weight)
        # =============================================
        
        stage_a = JourneyStageDetector.detect_stage(
            keyword_a
        )
        stage_b = JourneyStageDetector.detect_stage(
            keyword_b
        )
        
        stage_score = 1.0 if (
            stage_a and stage_b and
            stage_a == stage_b
        ) else (0.5 if not stage_a and not stage_b else 0.0)
        
        # =============================================
        # Temporal alignment (0.20 weight)
        # =============================================
        
        temporal_a = TemporalClassifier.classify_temporal(
            keyword_a
        )
        temporal_b = TemporalClassifier.classify_temporal(
            keyword_b
        )
        
        temporal_score = 1.0 if (
            temporal_a == temporal_b
        ) else 0.0
        
        # =============================================
        # Phrase-chain similarity (0.20 weight)
        # =============================================
        
        chains_a = PhraseChainMatcher.extract_phrase_chains(
            keyword_a
        )
        chains_b = PhraseChainMatcher.extract_phrase_chains(
            keyword_b
        )
        
        phrase_chain_score = (
            PhraseChainMatcher.calculate_chain_weight(
                chains_a,
                chains_b,
            )
        )
        
        # =============================================
        # Token overlap (0.10 weight)
        # =============================================
        
        tokens_a = (
            WeightedSimilarityCalculator
            .tokenize_semantic(keyword_a)
        )
        tokens_b = (
            WeightedSimilarityCalculator
            .tokenize_semantic(keyword_b)
        )
        
        if not tokens_a and not tokens_b:
            token_score = 1.0
        elif not tokens_a or not tokens_b:
            token_score = 0.0
        else:
            intersection = tokens_a & tokens_b
            union = tokens_a | tokens_b
            token_score = (
                len(intersection) / len(union)
            )
        
        # =============================================
        # Composite weighted similarity
        # =============================================
        
        weighted_similarity = (
            (entity_score * 0.25) +
            (stage_score * 0.25) +
            (temporal_score * 0.20) +
            (phrase_chain_score * 0.20) +
            (token_score * 0.10)
        )
        
        return min(1.0, weighted_similarity)


# =====================================================
# LONG-TAIL SPECIFICITY PRESERVER (New)
# =====================================================

class LongTailPreserver:
    """
    Prevent over-merging of highly specific queries.
    """
    
    @staticmethod
    def is_highly_specific(
        keyword: str,
    ) -> bool:
        """
        Check if keyword is highly specific.
        
        Highly specific if:
        - Contains exam code + year + stage + detail
        - Example: "ssc gd 2025 admit card pdf download"
        """
        
        tokens = TokenBoundaryMatcher.tokenize(keyword)
        
        # Must have at least 4 specific tokens
        semantic_tokens = (
            WeightedSimilarityCalculator
            .tokenize_semantic(keyword)
        )
        
        return len(semantic_tokens) >= 4
    
    @staticmethod
    def should_skip_merge(
        keyword_a: str,
        keyword_b: str,
        similarity: float,
    ) -> bool:
        """
        Decide if should skip merge despite similarity.
        """
        
        spec_a = (
            LongTailPreserver.is_highly_specific(
                keyword_a
            )
        )
        spec_b = (
            LongTailPreserver.is_highly_specific(
                keyword_b
            )
        )
        
        # Both highly specific + low similarity = skip
        if spec_a and spec_b and similarity < 0.5:
            return True
        
        return False


# =====================================================
# SEMANTIC COHERENCE SCORER (New)
# =====================================================

class SemanticCoherenceScorer:
    """
    Score semantic coherence of cluster.
    """
    
    @staticmethod
    def score_coherence(
        keywords: list[str],
    ) -> float:
        """
        Score semantic coherence (0-1).
        
        Measures:
        - Average pairwise similarity
        - Homogeneity of entities
        - Homogeneity of journey stages
        - Homogeneity of temporal classes
        """
        
        if len(keywords) < 2:
            return 1.0
        
        # Average pairwise similarity
        similarities = []
        
        for i, kw_a in enumerate(keywords):
            for kw_b in keywords[i+1:]:
                sim = (
                    WeightedSimilarityCalculator
                    .calculate_weighted_similarity(
                        kw_a,
                        kw_b,
                    )
                )
                similarities.append(sim)
        
        avg_similarity = (
            sum(similarities) / len(similarities)
            if similarities else 0.5
        )
        
        # Entity homogeneity
        entities = set()
        for kw in keywords:
            entity = EntityDetector.detect_entity(kw)
            if entity:
                entities.add(entity)
        
        entity_homogeneity = (
            1.0 if len(entities) <= 1 else
            1.0 / len(entities)
        )
        
        # Journey stage homogeneity
        stages = set()
        for kw in keywords:
            stage = (
                JourneyStageDetector.detect_stage(kw)
            )
            if stage:
                stages.add(stage)
        
        stage_homogeneity = (
            1.0 if len(stages) <= 1 else
            1.0 / len(stages)
        )
        
        # Temporal homogeneity
        temporals = set()
        for kw in keywords:
            temporal = (
                TemporalClassifier.classify_temporal(kw)
            )
            temporals.add(temporal)
        
        temporal_homogeneity = (
            1.0 if len(temporals) <= 1 else
            1.0 / len(temporals)
        )
        
        # Composite coherence
        coherence = (
            (avg_similarity * 0.40) +
            (entity_homogeneity * 0.25) +
            (stage_homogeneity * 0.20) +
            (temporal_homogeneity * 0.15)
        )
        
        return min(1.0, coherence)


# =====================================================
# MAIN CLUSTERING ENGINE (Refined)
# =====================================================

class SEOEcosystemClusteringEngine:
    """
    Production-grade clustering with refinements.
    """
    
    def __init__(self) -> None:
        self.similarity_calc = (
            WeightedSimilarityCalculator()
        )
        self.coherence_scorer = (
            SemanticCoherenceScorer()
        )
        self.long_tail = LongTailPreserver()
        self.contradiction = (
            ContradictionDetector()
        )
    
    def normalize_keyword(
        self,
        keyword: str,
    ) -> str:
        """Normalize keyword."""
        keyword = keyword.strip().lower()
        keyword = re.sub(r"\s+", " ", keyword)
        return keyword
    
    def cluster_keywords_hierarchical(
        self,
        keywords: list[str],
        similarity_threshold: float = 0.35,
    ) -> list[list[str]]:
        """
        Hierarchical clustering with refinements.
        """
        
        if not keywords:
            return []
        
        # Normalize and deduplicate
        keywords = [
            self.normalize_keyword(k)
            for k in keywords
        ]
        keywords = list(set(keywords))
        
        # Filter contradictions
        keywords = [
            k for k in keywords
            if not self.contradiction.detect_contradictions(k)
        ]
        
        # Start with each as cluster
        clusters = [[k] for k in keywords]
        
        # Merge similar clusters
        merged = True
        
        while merged:
            merged = False
            new_clusters = []
            used = set()
            
            for i, cluster_a in enumerate(clusters):
                if i in used:
                    continue
                
                merged_cluster = cluster_a.copy()
                
                for j, cluster_b in enumerate(
                    clusters[i+1:]
                ):
                    if (i + j + 1) in used:
                        continue
                    
                    # Calculate average similarity
                    sims = [
                        self.similarity_calc
                        .calculate_weighted_similarity(
                            k_a,
                            k_b,
                        )
                        for k_a in merged_cluster
                        for k_b in cluster_b
                    ]
                    
                    avg_sim = (
                        sum(sims) / len(sims)
                        if sims else 0.0
                    )
                    
                    # Check long-tail preservation
                    should_skip = False
                    
                    if (
                        len(merged_cluster) == 1 and
                        len(cluster_b) == 1
                    ):
                        should_skip = (
                            self.long_tail.should_skip_merge(
                                merged_cluster[0],
                                cluster_b[0],
                                avg_sim,
                            )
                        )
                    
                    if (
                        avg_sim >= similarity_threshold and
                        not should_skip
                    ):
                        merged_cluster.extend(
                            cluster_b
                        )
                        used.add(i + j + 1)
                        merged = True
                
                new_clusters.append(merged_cluster)
                used.add(i)
            
            clusters = new_clusters
        
        return clusters
    
    def analyze_cluster(
        self,
        keywords: list[str],
    ) -> dict[str, Any]:
        """Analyze cluster."""
        
        # Collect properties
        journey_stages = set()
        temporal_classes = set()
        entities = set()
        
        for kw in keywords:
            stage = (
                JourneyStageDetector.detect_stage(kw)
            )
            if stage:
                journey_stages.add(stage)
            
            temporal = (
                TemporalClassifier.classify_temporal(kw)
            )
            temporal_classes.add(temporal)
            
            entity = (
                EntityDetector.detect_entity(kw)
            )
            if entity:
                entities.add(entity)
        
        # Coherence score
        coherence = (
            self.coherence_scorer.score_coherence(
                keywords
            )
        )
        
        # Intent purity
        intent_purity = 1.0 if (
            len(journey_stages) <= 1
        ) else 1.0 / len(journey_stages)
        
        # Temporal consistency
        temporal_consistency = 1.0 if (
            len(temporal_classes) <= 1
        ) else 1.0 / len(temporal_classes)
        
        # Entity consistency
        entity_consistency = 1.0 if (
            len(entities) <= 1
        ) else 1.0 / len(entities)
        
        # Confidence
        confidence = (
            (coherence * 0.35) +
            (intent_purity * 0.25) +
            (temporal_consistency * 0.20) +
            (entity_consistency * 0.20)
        )
        
        # Label
        entity_str = (
            list(entities)[0]
            if entities else None
        )
        
        stage_str = (
            list(journey_stages)[0].value
            if journey_stages else "general"
        )
        
        label = f"{entity_str}_{stage_str}".lstrip("_")
        
        return {
            "name": label,
            "keywords": keywords,
            "size": len(keywords),
            "journey_stages": [
                s.value for s in journey_stages
            ],
            "temporal_classes": list(temporal_classes),
            "entities": list(entities),
            "coherence_score": round(coherence, 2),
            "confidence_score": round(confidence, 2),
            "intent_purity": round(intent_purity, 2),
        }
    
    def cluster_keywords(
        self,
        keywords: list[str],
        similarity_threshold: float = 0.35,
        min_cluster_size: int = 2,
    ) -> dict[str, Any]:
        """Cluster keywords."""
        
        logger.info(
            f"Clustering {len(keywords)} keywords"
        )
        
        if not keywords:
            return {
                "total_keywords": 0,
                "total_clusters": 0,
                "clusters": {},
            }
        
        # Cluster
        raw_clusters = (
            self.cluster_keywords_hierarchical(
                keywords,
                similarity_threshold,
            )
        )
        
        # Filter by size and analyze
        clusters_dict = {}
        
        for cluster in raw_clusters:
            if len(cluster) >= min_cluster_size:
                analysis = self.analyze_cluster(cluster)
                cluster_id = f"{analysis['name']}_{len(clusters_dict)}"
                clusters_dict[cluster_id] = analysis
        
        # Sort by confidence
        clusters_dict = dict(
            sorted(
                clusters_dict.items(),
                key=lambda x: x[1][
                    "confidence_score"
                ],
                reverse=True,
            )
        )
        
        logger.info(
            f"Generated {len(clusters_dict)} clusters"
        )
        
        return {
            "total_keywords": len(keywords),
            "total_clusters": len(clusters_dict),
            "clusters": clusters_dict,
        }


# =====================================================
# PUBLIC API
# =====================================================

class ClusteringService:
    """Production clustering service."""
    
    def __init__(self) -> None:
        self.engine = SEOEcosystemClusteringEngine()
    
    def cluster_keywords(
        self,
        keywords: list[str],
        similarity_threshold: float = 0.35,
        min_cluster_size: int = 2,
    ) -> dict[str, Any]:
        """Cluster keywords."""
        
        return self.engine.cluster_keywords(
            keywords,
            similarity_threshold,
            min_cluster_size,
        )


# =====================================================
# EXAMPLE USAGE
# =====================================================

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    service = ClusteringService()
    
    keywords = [
        # SSC GD Notification
        "ssc gd notification 2025",
        "ssc gd official notification",
        "ssc gd notification pdf",
        
        # SSC GD Admit Card
        "ssc gd admit card 2025",
        "ssc gd admit card download",
        "ssc gd hall ticket pdf",
        
        # SSC GD Answer Key
        "ssc gd answer key official",
        "ssc gd answer key 2025",
        "ssc gd answer key pdf download",
        
        # SSC GD Result
        "ssc gd result 2025",
        "ssc gd result declared",
        "ssc gd marks released",
        
        # UPSC IAS (Different entity)
        "upsc ias notification 2025",
        "upsc ias admit card",
        "upsc ias result",
        
        # GATE (Different entity)
        "gate 2025 notification",
        "gate admit card download",
        "gate answer key official",
    ]
    
    result = service.cluster_keywords(keywords)
    
    print(f"\n{'='*70}")
    print(f"Total Keywords: {result['total_keywords']}")
    print(f"Total Clusters: {result['total_clusters']}")
    print(f"{'='*70}")
    
    for cluster_id, cluster_data in (
        result['clusters'].items()
    ):
        print(f"\n{cluster_data['name']}")
        print(
            f"  Confidence: {cluster_data['confidence_score']:.2f}"
        )
        print(
            f"  Coherence: {cluster_data['coherence_score']:.2f}"
        )
        print(f"  Size: {cluster_data['size']}")
        
        if cluster_data['entities']:
            print(f"  Entities: {cluster_data['entities']}")
        
        print(f"  Keywords: {', '.join(cluster_data['keywords'][:3])}")