"""
Enterprise SEO Scoring Service v2.4-ADVANCED
=============================================

Production-grade multi-signal SEO keyword scoring with:
1. Cross-signal intelligence (synergies & penalties)
2. Temporal SEO awareness (exam cycles, trending)
3. Semantic-role specificity (document types, years)
4. SERP diversity analysis (format mix, competition)
5. Advanced autocomplete realism (phrase chains, flow)

All lightweight heuristics - no ML, embeddings, or vectors.
"""

import logging
import math
import re
from collections import Counter
from dataclasses import dataclass, field
from typing import Any

logger = logging.getLogger(__name__)

# =====================================================
# TEMPORAL INTENT MARKERS
# =====================================================

TEMPORAL_MARKERS = {
    # Year references
    "year_future": {"2025", "2026", "2027", "2028"},
    "year_current": {"2024", "2023"},
    "year_past": {"2022", "2021", "2020"},
    
    # Freshness indicators
    "freshness_high": {
        "latest", "new", "today", "now", "recent",
        "breaking", "update", "announced", "released",
        "just", "right now", "this week", "this month",
    },
    
    # Exam/education cycle
    "exam_admit": {
        "admit card", "admission card", "admit",
        "hall ticket", "entry pass",
    },
    "exam_answer": {
        "answer key", "official answer", "solution",
        "key", "answers",
    },
    "exam_result": {
        "result", "scorecard", "score card", "marks",
        "declared", "announced",
    },
    "exam_syllabus": {
        "syllabus", "curriculum", "pattern", "exam pattern",
    },
    "exam_date": {
        "exam date", "test date", "schedule",
        "when", "notification",
    },
    "exam_phase": {
        "prelims", "mains", "interview", "cutoff",
        "merit list", "selection",
    },
    
    # Notification markers
    "notification": {
        "notification", "notification pdf",
        "official notification", "alert",
    },
}

# Semantic role templates
SEMANTIC_ROLE_PATTERNS = {
    "document_type": {
        r"pdf$": ("document", 1.2),
        r"book$": ("document", 1.1),
        r"guide$": ("document", 1.0),
        r"tutorial$": ("document", 0.9),
        r"course$": ("document", 0.85),
    },
    "content_scope": {
        r"^full": ("comprehensive", 1.3),
        r"complete": ("comprehensive", 1.25),
        r"detailed": ("comprehensive", 1.2),
        r"chapter": ("modular", 0.95),
        r"part": ("modular", 0.9),
    },
    "target_audience": {
        r"beginners": ("audience", 1.0),
        r"advanced": ("audience", 1.05),
        r"professionals": ("audience", 1.1),
        r"kids": ("audience", 0.9),
    },
}

# SERP format diversity types
SERP_FORMAT_TYPES = {
    "official": {"official site", "government", "gov.in"},
    "blog": {"blog", "article", "post"},
    "pdf": {".pdf", "pdf download"},
    "video": {"youtube", "video"},
    "forum": {"reddit", "quora", "stackoverflow"},
    "news": {"news", "breaking"},
    "shopping": {"price", "buy", "shop"},
}

# Common suffix chains for autocomplete
SUFFIX_CHAINS = {
    # After exam keywords
    "exam": {
        "syllabus": 0.95,
        "date": 0.94,
        "pattern": 0.92,
        "notification": 0.90,
        "answer key": 0.93,
    },
    # After education keywords
    "course": {
        "fees": 0.90,
        "duration": 0.85,
        "eligibility": 0.88,
        "admission": 0.87,
    },
    # After "how to"
    "how to": {
        "learn": 0.95,
        "get": 0.92,
        "prepare": 0.90,
        "pass": 0.91,
    },
}

# =====================================================
# DATA CLASSES FOR ADVANCED ANALYSIS
# =====================================================

@dataclass
class TemporalAnalysis:
    """Temporal intent analysis results."""
    temporal_markers_found: dict[str, list[str]]
    temporal_confidence: float
    freshness_score: float
    exam_cycle_phase: str | None
    time_sensitivity_score: float
    boost_factor: float


@dataclass
class SemanticRoleAnalysis:
    """Semantic role and document type analysis."""
    primary_entity: str | None
    qualifiers: list[str]
    document_types: list[str]
    years_mentioned: list[str]
    semantic_roles: dict[str, float]
    role_specificity_score: float
    completeness_score: float


@dataclass
class SERPDiversityAnalysis:
    """SERP ecosystem diversity analysis."""
    format_distribution: dict[str, float]
    diversity_score: float
    saturation_score: float
    opportunity_gap: float
    ecosystem_health: str


@dataclass
class CrossSignalInteraction:
    """Result of cross-signal interaction analysis."""
    synergy_pairs: dict[str, float]
    penalty_pairs: dict[str, float]
    compound_adjustments: dict[str, float]
    total_adjustment: float
    interaction_details: dict[str, str]


@dataclass
class AdvancedScoringResult:
    """Complete advanced scoring result."""
    seo_score: int
    signals: dict[str, float]
    base_composition: float
    interactions: CrossSignalInteraction
    temporal_analysis: TemporalAnalysis
    semantic_roles: SemanticRoleAnalysis
    serp_diversity: SERPDiversityAnalysis
    query_flow: dict[str, float]


# =====================================================
# NORMALIZER & BASIC COMPONENTS (Keep from v2.3)
# =====================================================

class SignalNormalizer:
    """Normalize signals to 0-1 range."""

    def normalize(
        self,
        value: float,
        min_val: float = 0.0,
        max_val: float = 1.0,
    ) -> float:
        """Normalize value to 0-1 range."""
        if max_val == min_val:
            return 0.5
        return (value - min_val) / (max_val - min_val)

    def clamp(self, value: float) -> float:
        """Clamp value to 0-1."""
        return max(0.0, min(1.0, value))


# =====================================================
# 1. TEMPORAL SEO INTELLIGENCE
# =====================================================

class TemporalIntentAnalyzer:
    """
    Analyze temporal intent and time-sensitivity.
    
    Detects:
    - Year references (2024, 2025, 2026)
    - Freshness intent (latest, new, today)
    - Exam cycles (admit card, answer key, results)
    - Educational calendar awareness
    """

    def __init__(self) -> None:
        self.normalizer = SignalNormalizer()

    def analyze_temporal_intent(
        self,
        keyword: str,
        keyword_data: dict[str, Any] | None = None,
    ) -> TemporalAnalysis:
        """Analyze temporal aspects of keyword."""

        keyword_lower = keyword.lower()
        tokens = keyword.split()

        # =============================================
        # Find temporal markers
        # =============================================

        markers_found = {}

        for marker_type, marker_set in (
            TEMPORAL_MARKERS.items()
        ):
            found = [
                token for token in tokens
                if token.lower() in marker_set
            ]

            if found:
                markers_found[marker_type] = found

            # Also check multi-word phrases
            for phrase in marker_set:
                if phrase in keyword_lower:
                    if marker_type not in markers_found:
                        markers_found[marker_type] = []
                    markers_found[marker_type].append(
                        phrase
                    )

        # =============================================
        # Temporal confidence scoring
        # =============================================

        temporal_confidence = (
            self._calculate_temporal_confidence(
                markers_found
            )
        )

        # =============================================
        # Freshness intent scoring
        # =============================================

        freshness_score = (
            self._calculate_freshness_score(
                markers_found
            )
        )

        # =============================================
        # Exam cycle phase detection
        # =============================================

        exam_phase = (
            self._detect_exam_phase(
                markers_found
            )
        )

        # =============================================
        # Time sensitivity
        # =============================================

        time_sensitivity = (
            self._calculate_time_sensitivity(
                markers_found,
                exam_phase,
            )
        )

        # =============================================
        # Boost factor (how much to boost score)
        # =============================================

        boost_factor = (
            self._calculate_boost_factor(
                temporal_confidence,
                time_sensitivity,
            )
        )

        logger.debug(
            f"Temporal analysis: "
            f"confidence={temporal_confidence:.2f}, "
            f"freshness={freshness_score:.2f}, "
            f"phase={exam_phase}, "
            f"sensitivity={time_sensitivity:.2f}, "
            f"boost={boost_factor:.2f}"
        )

        return TemporalAnalysis(
            temporal_markers_found=markers_found,
            temporal_confidence=temporal_confidence,
            freshness_score=freshness_score,
            exam_cycle_phase=exam_phase,
            time_sensitivity_score=time_sensitivity,
            boost_factor=boost_factor,
        )

    def _calculate_temporal_confidence(
        self,
        markers: dict[str, list[str]],
    ) -> float:
        """Calculate confidence in temporal relevance."""

        if not markers:
            return 0.4  # No temporal markers

        # Count marker types found
        marker_type_count = len(markers)

        # Year markers boost confidence
        year_markers = [
            k for k in markers.keys()
            if k.startswith("year_")
        ]

        freshness_markers = [
            k for k in markers.keys()
            if k.startswith("freshness_")
        ]

        exam_markers = [
            k for k in markers.keys()
            if k.startswith("exam_")
        ]

        confidence = 0.4

        if year_markers:
            confidence += 0.25
        if freshness_markers:
            confidence += 0.15
        if exam_markers:
            confidence += 0.20

        return self.normalizer.clamp(confidence)

    def _calculate_freshness_score(
        self,
        markers: dict[str, list[str]],
    ) -> float:
        """Calculate freshness intent score."""

        if "freshness_high" not in markers:
            return 0.5

        # High freshness markers present
        return 0.85

    def _detect_exam_phase(
        self,
        markers: dict[str, list[str]],
    ) -> str | None:
        """Detect which phase of exam cycle."""

        exam_markers = {
            k: v for k, v in markers.items()
            if k.startswith("exam_")
        }

        if not exam_markers:
            return None

        # Priority-based phase detection
        if "exam_admit" in exam_markers:
            return "admit_card_phase"
        elif "exam_answer" in exam_markers:
            return "answer_key_phase"
        elif "exam_result" in exam_markers:
            return "result_phase"
        elif "exam_date" in exam_markers:
            return "date_announcement_phase"
        elif "exam_notification" in exam_markers:
            return "notification_phase"
        else:
            return "general_exam_phase"

    def _calculate_time_sensitivity(
        self,
        markers: dict[str, list[str]],
        exam_phase: str | None,
    ) -> float:
        """Calculate time sensitivity (0-1)."""

        # Very time-sensitive keywords
        if exam_phase:
            return 0.9

        # Check for freshness
        if "freshness_high" in markers:
            return 0.85

        # Check for future years
        if "year_future" in markers:
            return 0.75

        return 0.3  # Low time sensitivity

    def _calculate_boost_factor(
        self,
        temporal_confidence: float,
        time_sensitivity: float,
    ) -> float:
        """
        Calculate score boost factor.
        
        Time-sensitive keywords get boosted in scoring
        because they have less competition and higher intent.
        """

        # Boost = confidence * sensitivity
        # Clamped to max 1.15x (15% boost)
        boost = 1.0 + (
            (temporal_confidence * 0.1) +
            (time_sensitivity * 0.05)
        )

        return min(1.15, boost)


# =====================================================
# 2. SEMANTIC-ROLE SPECIFICITY ANALYZER
# =====================================================

class SemanticRoleAnalyzer:
    """
    Analyze semantic roles and document types.
    
    Detects:
    - Primary entity (exam name, course, etc.)
    - Qualifiers (year, phase, level)
    - Document types (PDF, guide, syllabus)
    - Semantic specificity
    """

    def __init__(self) -> None:
        self.normalizer = SignalNormalizer()

    def analyze_semantic_roles(
        self,
        keyword: str,
        entities: dict[str, list[str]] | None = None,
    ) -> SemanticRoleAnalysis:
        """Analyze semantic roles in keyword."""

        tokens = keyword.lower().split()
        keyword_lower = keyword.lower()

        # =============================================
        # Extract primary entity
        # =============================================

        primary_entity = self._extract_primary_entity(
            tokens,
            entities,
        )

        # =============================================
        # Extract qualifiers
        # =============================================

        qualifiers = self._extract_qualifiers(tokens)

        # =============================================
        # Detect document types
        # =====================================================

        document_types = (
            self._detect_document_types(
                keyword_lower
            )
        )

        # =============================================
        # Extract years
        # =============================================

        years = self._extract_years(tokens)

        # =============================================
        # Semantic role scoring
        # =============================================

        role_scores = (
            self._score_semantic_roles(
                keyword_lower
            )
        )

        # =============================================
        # Specificity calculation
        # =============================================

        specificity = (
            self._calculate_role_specificity(
                primary_entity,
                qualifiers,
                document_types,
                years,
                role_scores,
            )
        )

        # =============================================
        # Completeness
        # =============================================

        completeness = (
            self._calculate_completeness(
                primary_entity,
                qualifiers,
                len(tokens),
            )
        )

        logger.debug(
            f"Semantic roles: "
            f"entity={primary_entity}, "
            f"qualifiers={qualifiers}, "
            f"docs={document_types}, "
            f"specificity={specificity:.2f}"
        )

        return SemanticRoleAnalysis(
            primary_entity=primary_entity,
            qualifiers=qualifiers,
            document_types=document_types,
            years_mentioned=years,
            semantic_roles=role_scores,
            role_specificity_score=specificity,
            completeness_score=completeness,
        )

    def _extract_primary_entity(
        self,
        tokens: list[str],
        entities: dict[str, list[str]] | None = None,
    ) -> str | None:
        """Extract primary entity (exam name, course, etc.)."""

        # Proper nouns are primary entities
        for token in tokens:
            if token and token[0].isupper():
                return token

        # Check custom entities
        if entities:
            for entity_type, entity_list in (
                entities.items()
            ):
                for entity in entity_list:
                    if entity.lower() in [
                        t.lower() for t in tokens
                    ]:
                        return entity

        # Common exam/course names
        exam_names = {
            "gate", "ugc", "net", "ssc", "ibps",
            "upsc", "neet", "jee", "ias", "ips",
        }

        for token in tokens:
            if token.lower() in exam_names:
                return token

        return None

    def _extract_qualifiers(
        self,
        tokens: list[str],
    ) -> list[str]:
        """Extract qualifiers (year, phase, level)."""

        qualifiers = []

        qualifier_patterns = {
            r"\d{4}": "year",  # 2024, 2025
            r"(preliminary|prelim|mains|final|round)": "phase",
            r"(advanced|beginner|intermediate)": "level",
            r"(pdf|book|guide|tutorial)": "type",
        }

        for token in tokens:
            for pattern, qual_type in (
                qualifier_patterns.items()
            ):
                if re.match(pattern, token.lower()):
                    qualifiers.append(token)
                    break

        return qualifiers

    def _detect_document_types(
        self,
        keyword_lower: str,
    ) -> list[str]:
        """Detect document types (PDF, guide, etc.)."""

        doc_types = []

        for doc_type, pattern in (
            SEMANTIC_ROLE_PATTERNS[
                "document_type"
            ].items()
        ):
            if re.search(doc_type, keyword_lower):
                doc_types.append(pattern[0])

        return doc_types

    def _extract_years(
        self,
        tokens: list[str],
    ) -> list[str]:
        """Extract year references."""

        years = []

        for token in tokens:
            if re.match(r"^\d{4}$", token):
                year_int = int(token)
                if 2000 <= year_int <= 2030:
                    years.append(token)

        return years

    def _score_semantic_roles(
        self,
        keyword_lower: str,
    ) -> dict[str, float]:
        """Score each semantic role type."""

        scores = {}

        for role_type, patterns in (
            SEMANTIC_ROLE_PATTERNS.items()
        ):
            score = 0.0

            for pattern, (role, weight) in (
                patterns.items()
            ):
                if re.search(pattern, keyword_lower):
                    score = max(score, weight)

            scores[role_type] = (
                self.normalizer.clamp(
                    score / 1.3
                )
            )

        return scores

    def _calculate_role_specificity(
        self,
        primary_entity: str | None,
        qualifiers: list[str],
        document_types: list[str],
        years: list[str],
        role_scores: dict[str, float],
    ) -> float:
        """Calculate specificity from semantic roles."""

        specificity = 0.4  # Base

        if primary_entity:
            specificity += 0.25
        if qualifiers:
            specificity += 0.15 * min(len(qualifiers), 2)
        if document_types:
            specificity += 0.15
        if years:
            specificity += 0.10

        return self.normalizer.clamp(specificity)

    def _calculate_completeness(
        self,
        primary_entity: str | None,
        qualifiers: list[str],
        token_count: int,
    ) -> float:
        """Calculate semantic completeness."""

        completeness = 0.3

        if primary_entity:
            completeness += 0.25
        if qualifiers:
            completeness += 0.20
        if 3 <= token_count <= 6:
            completeness += 0.15
        elif token_count > 6:
            completeness += 0.05

        return self.normalizer.clamp(completeness)


# =====================================================
# 3. SERP DIVERSITY ANALYZER
# =====================================================

class SERPDiversityAnalyzer:
    """
    Analyze SERP ecosystem diversity.
    
    Evaluates:
    - Format distribution (official, blog, PDF, video)
    - Content diversity
    - Saturation levels
    - Opportunity gaps
    """

    def __init__(self) -> None:
        self.normalizer = SignalNormalizer()

    def analyze_serp_diversity(
        self,
        keyword_data: dict[str, Any] | None = None,
    ) -> SERPDiversityAnalysis:
        """Analyze SERP ecosystem diversity."""

        if not keyword_data:
            # Default analysis
            return self._create_default_analysis()

        # =============================================
        # Extract format distribution
        # =============================================

        format_dist = (
            self._analyze_format_distribution(
                keyword_data
            )
        )

        # =============================================
        # Diversity score (content mix health)
        # =============================================

        diversity_score = (
            self._calculate_diversity_score(
                format_dist
            )
        )

        # =============================================
        # Saturation score
        # =============================================

        saturation = self._calculate_saturation(
            keyword_data
        )

        # =============================================
        # Opportunity gap
        # =============================================

        opportunity_gap = (
            self._calculate_opportunity_gap(
                format_dist,
                diversity_score,
            )
        )

        # =============================================
        # Ecosystem health assessment
        # =============================================

        ecosystem_health = (
            self._assess_ecosystem_health(
                diversity_score,
                saturation,
            )
        )

        logger.debug(
            f"SERP diversity: "
            f"formats={len(format_dist)}, "
            f"diversity={diversity_score:.2f}, "
            f"saturation={saturation:.2f}, "
            f"health={ecosystem_health}"
        )

        return SERPDiversityAnalysis(
            format_distribution=format_dist,
            diversity_score=diversity_score,
            saturation_score=saturation,
            opportunity_gap=opportunity_gap,
            ecosystem_health=ecosystem_health,
        )

    def _analyze_format_distribution(
        self,
        keyword_data: dict[str, Any],
    ) -> dict[str, float]:
        """Analyze format distribution in SERP."""

        competitor_data = keyword_data.get(
            "competitor_data",
            [],
        )

        if not competitor_data:
            return {}

        format_counts = {
            "official": 0,
            "blog": 0,
            "pdf": 0,
            "video": 0,
            "forum": 0,
            "news": 0,
            "other": 0,
        }

        for page in competitor_data:
            domain = page.get("domain", "").lower()
            title = page.get("title", "").lower()

            # Detect format
            detected = False

            for format_type, patterns in (
                SERP_FORMAT_TYPES.items()
            ):
                for pattern in patterns:
                    if (
                        pattern in domain or
                        pattern in title
                    ):
                        format_counts[
                            format_type
                        ] += 1
                        detected = True
                        break

                if detected:
                    break

            if not detected:
                format_counts["other"] += 1

        # Convert to ratios
        total = sum(format_counts.values())

        if total == 0:
            return {}

        return {
            fmt: count / total
            for fmt, count in format_counts.items()
            if count > 0
        }

    def _calculate_diversity_score(
        self,
        format_dist: dict[str, float],
    ) -> float:
        """
        Calculate diversity score.
        
        Ideal: evenly distributed across 3-5 formats
        Bad: all same format
        """

        if not format_dist:
            return 0.5

        format_count = len(format_dist)

        # Entropy-like calculation
        entropy = -sum(
            p * math.log(p + 0.0001)
            for p in format_dist.values()
        )

        # Normalize to 0-1
        # Ideal entropy for 5 formats: ~1.6
        diversity = min(entropy / 1.6, 1.0)

        logger.debug(
            f"Format diversity: "
            f"formats={format_count}, "
            f"entropy={entropy:.2f}, "
            f"score={diversity:.2f}"
        )

        return diversity

    def _calculate_saturation(
        self,
        keyword_data: dict[str, Any],
    ) -> float:
        """Calculate market saturation."""

        competitor_count = len(
            keyword_data.get("competitor_data", [])
        )

        # Saturation scoring
        if competitor_count <= 2:
            saturation = 0.2
        elif competitor_count <= 5:
            saturation = 0.4
        elif competitor_count <= 10:
            saturation = 0.6
        elif competitor_count <= 20:
            saturation = 0.8
        else:
            saturation = 0.95

        return saturation

    def _calculate_opportunity_gap(
        self,
        format_dist: dict[str, float],
        diversity_score: float,
    ) -> float:
        """
        Calculate opportunity gap.
        
        Low diversity = high opportunity
        Missing formats = opportunity
        """

        if not format_dist:
            return 0.5

        # Gap = 1 - diversity
        format_gap = 1.0 - diversity_score

        # Check for missing high-opportunity formats
        missing_formats = 0

        high_opportunity = {"pdf", "video"}

        for fmt in high_opportunity:
            if fmt not in format_dist:
                missing_formats += 1

        missing_bonus = missing_formats * 0.15

        opportunity = (
            (format_gap * 0.7) +
            (missing_bonus * 0.3)
        )

        return min(1.0, opportunity)

    def _assess_ecosystem_health(
        self,
        diversity: float,
        saturation: float,
    ) -> str:
        """Assess overall SERP ecosystem health."""

        # Health assessment matrix
        if diversity >= 0.7 and saturation <= 0.5:
            return "healthy_opportunity_rich"
        elif diversity >= 0.6 and saturation <= 0.6:
            return "healthy_moderate"
        elif diversity >= 0.5 and saturation <= 0.7:
            return "balanced_competitive"
        elif saturation > 0.8:
            return "saturated_difficult"
        else:
            return "fragmented_niche"

    def _create_default_analysis(
        self,
    ) -> SERPDiversityAnalysis:
        """Create default analysis when no data."""

        return SERPDiversityAnalysis(
            format_distribution={},
            diversity_score=0.5,
            saturation_score=0.5,
            opportunity_gap=0.5,
            ecosystem_health="unknown",
        )


# =====================================================
# 4. CROSS-SIGNAL INTELLIGENCE
# =====================================================

class CrossSignalIntelligence:
    """
    Analyze interactions between signals.
    
    Models:
    - Positive synergies (signals that enhance each other)
    - Negative synergies (signals that hurt together)
    - Compound effects
    """

    def __init__(self) -> None:
        self.normalizer = SignalNormalizer()

    def analyze_interactions(
        self,
        signals: dict[str, float],
        temporal_analysis: TemporalAnalysis,
        semantic_roles: SemanticRoleAnalysis,
    ) -> CrossSignalInteraction:
        """
        Analyze signal interactions and create adjustments.
        """

        # =============================================
        # Positive synergies
        # =============================================

        synergy_pairs = (
            self._calculate_synergies(
                signals,
                temporal_analysis,
                semantic_roles,
            )
        )

        # =============================================
        # Negative synergies (penalties)
        # =============================================

        penalty_pairs = (
            self._calculate_penalties(
                signals
            )
        )

        # =============================================
        # Compound adjustments
        # =============================================

        compound_adjustments = (
            self._calculate_compound_effects(
                signals,
                synergy_pairs,
                penalty_pairs,
            )
        )

        # =============================================
        # Total adjustment
        # =============================================

        total_adjustment = (
            sum(synergy_pairs.values()) -
            sum(penalty_pairs.values())
        )

        total_adjustment = self.normalizer.clamp(
            total_adjustment / 100.0
        )

        # =============================================
        # Interaction details
        # =============================================

        interaction_details = (
            self._build_interaction_details(
                synergy_pairs,
                penalty_pairs,
            )
        )

        logger.debug(
            f"Signal interactions: "
            f"synergies={len(synergy_pairs)}, "
            f"penalties={len(penalty_pairs)}, "
            f"total_adjustment={total_adjustment:.2f}"
        )

        return CrossSignalInteraction(
            synergy_pairs=synergy_pairs,
            penalty_pairs=penalty_pairs,
            compound_adjustments=compound_adjustments,
            total_adjustment=total_adjustment,
            interaction_details=interaction_details,
        )

    def _calculate_synergies(
        self,
        signals: dict[str, float],
        temporal: TemporalAnalysis,
        semantic: SemanticRoleAnalysis,
    ) -> dict[str, float]:
        """Calculate positive signal synergies."""

        synergies = {}

        # =============================================
        # Synergy 1: Intent + Coherence
        # =============================================
        # Strong intent + clear query = better ranking
        if (
            signals.get("intent_clarity", 0) > 0.8 and
            signals.get("query_coherence", 0) > 0.75
        ):
            synergy_score = (
                (signals["intent_clarity"] +
                 signals["query_coherence"]) / 2 * 0.15
            )
            synergies["intent_coherence"] = (
                synergy_score
            )

        # =============================================
        # Synergy 2: Autocomplete + Specificity
        # =============================================
        # Realistic autocomplete + specific keyword = strong
        if (
            signals.get("autocomplete_alignment", 0) > 0.7 and
            signals.get("specificity", 0) > 0.7
        ):
            synergy_score = (
                (signals["autocomplete_alignment"] +
                 signals["specificity"]) / 2 * 0.12
            )
            synergies["autocomplete_specificity"] = (
                synergy_score
            )

        # =============================================
        # Synergy 3: Source Confidence + Authority
        # =============================================
        # Strong SERP data + competitive landscape clarity
        if (
            signals.get("source_confidence", 0) > 0.7 and
            signals.get("authority", 0) > 0.65
        ):
            synergy_score = (
                (signals["source_confidence"] +
                 signals["authority"]) / 2 * 0.10
            )
            synergies["source_authority"] = (
                synergy_score
            )

        # =============================================
        # Synergy 4: Temporal + Entity Specificity
        # =============================================
        # Time-sensitive + specific entity = high value
        if (
            temporal.time_sensitivity_score > 0.7 and
            semantic.role_specificity_score > 0.7
        ):
            synergy_score = (
                (temporal.time_sensitivity_score +
                 semantic.role_specificity_score) / 2 * 0.12
            )
            synergies["temporal_specificity"] = (
                synergy_score
            )

        # =============================================
        # Synergy 5: Completeness + Modifier Quality
        # =============================================
        # Complete keyword + good modifiers = balanced
        if (
            signals.get("completeness", 0) > 0.75 and
            signals.get("modifier_quality", 0) > 0.7
        ):
            synergy_score = (
                (signals["completeness"] +
                 signals["modifier_quality"]) / 2 * 0.08
            )
            synergies["completeness_modifiers"] = (
                synergy_score
            )

        return synergies

    def _calculate_penalties(
        self,
        signals: dict[str, float],
    ) -> dict[str, float]:
        """Calculate negative signal interactions."""

        penalties = {}

        # =============================================
        # Penalty 1: Modifier Spam + Low Readability
        # =============================================
        # Multiple bad modifiers + hard to read = bad
        if (
            signals.get("modifier_quality", 0) < 0.5 and
            signals.get("naturalness", 0) < 0.5
        ):
            penalty_score = (
                (1.0 - signals["modifier_quality"]) *
                (1.0 - signals["naturalness"]) * 0.15
            )
            penalties["modifier_spam_naturalness"] = (
                penalty_score
            )

        # =============================================
        # Penalty 2: Low Coherence + Low Specificity
        # =============================================
        # Incoherent + vague = very bad
        if (
            signals.get("query_coherence", 0) < 0.5 and
            signals.get("specificity", 0) < 0.5
        ):
            penalty_score = (
                (1.0 - signals["query_coherence"]) *
                (1.0 - signals["specificity"]) * 0.18
            )
            penalties["coherence_specificity"] = (
                penalty_score
            )

        # =============================================
        # Penalty 3: Keyword Stuffing Pattern
        # =============================================
        # Low coherence + high modifier spam = stuffing
        if (
            signals.get("query_coherence", 0) < 0.5 and
            signals.get("modifier_quality", 0) < 0.4
        ):
            penalty_score = (
                (1.0 - signals["query_coherence"]) *
                (1.0 - signals["modifier_quality"]) * 0.12
            )
            penalties["stuffing_pattern"] = (
                penalty_score
            )

        # =============================================
        # Penalty 4: Poor Autocomplete + Low Authority
        # =============================================
        # Unrealistic keyword + weak SERP = hard to rank
        if (
            signals.get("autocomplete_alignment", 0) < 0.5 and
            signals.get("authority", 0) < 0.55
        ):
            penalty_score = (
                (1.0 - signals["autocomplete_alignment"]) *
                (1.0 - signals["authority"]) * 0.10
            )
            penalties["unrealistic_weak_serp"] = (
                penalty_score
            )

        return penalties

    def _calculate_compound_effects(
        self,
        signals: dict[str, float],
        synergies: dict[str, float],
        penalties: dict[str, float],
    ) -> dict[str, float]:
        """Calculate compound effects of multiple factors."""

        compound = {}

        # High signal variance can be bad (imbalanced keyword)
        signal_values = list(signals.values())

        if signal_values:
            mean = sum(signal_values) / len(signal_values)
            variance = sum(
                (x - mean) ** 2 for x in signal_values
            ) / len(signal_values)

            # High variance penalty
            if variance > 0.05:
                compound["signal_variance_penalty"] = (
                    min(variance * 0.5, 0.1)
                )

        # Synergy concentration bonus (multiple synergies)
        if len(synergies) >= 2:
            compound["synergy_concentration_bonus"] = (
                min(len(synergies) * 0.02, 0.06)
            )

        return compound

    def _build_interaction_details(
        self,
        synergies: dict[str, float],
        penalties: dict[str, float],
    ) -> dict[str, str]:
        """Build human-readable interaction details."""

        details = {}

        for name, score in synergies.items():
            details[f"synergy_{name}"] = (
                f"Positive interaction boost: {score*100:.1f}%"
            )

        for name, score in penalties.items():
            details[f"penalty_{name}"] = (
                f"Negative interaction penalty: {score*100:.1f}%"
            )

        return details


# =====================================================
# 5. ADVANCED AUTOCOMPLETE REALISM
# =====================================================

class AdvancedAutocompleteAnalyzer:
    """
    Advanced autocomplete and query-flow realism.
    
    Models:
    - Common suffix chains (what comes after words)
    - Phrase continuation quality
    - Query-flow naturalness
    - Modifier ordering
    - Entity-first patterns
    - Education niche patterns
    """

    def __init__(self) -> None:
        self.normalizer = SignalNormalizer()

    def analyze_autocomplete_realism(
        self,
        keyword: str,
        keyword_data: dict[str, Any] | None = None,
    ) -> dict[str, float]:
        """
        Advanced autocomplete and phrase-flow analysis.
        """

        keyword_lower = keyword.lower()
        tokens = keyword.split()

        # =============================================
        # Suffix chain analysis
        # =============================================

        suffix_score = (
            self._analyze_suffix_chains(
                tokens
            )
        )

        # =============================================
        # Phrase continuation quality
        # =============================================

        continuation_score = (
            self._analyze_phrase_continuation(
                tokens
            )
        )

        # =============================================
        # Modifier ordering quality
        # =============================================

        modifier_order_score = (
            self._analyze_modifier_ordering(
                tokens
            )
        )

        # =============================================
        # Entity-first patterns
        # =============================================

        entity_first_score = (
            self._analyze_entity_first_pattern(
                tokens
            )
        )

        # =============================================
        # Education niche patterns
        # =============================================

        education_pattern_score = (
            self._analyze_education_patterns(
                keyword_lower
            )
        )

        # =============================================
        # Composite realism score
        # =============================================

        realism_score = (
            (suffix_score * 0.2) +
            (continuation_score * 0.2) +
            (modifier_order_score * 0.2) +
            (entity_first_score * 0.2) +
            (education_pattern_score * 0.2)
        )

        logger.debug(
            f"Autocomplete realism: "
            f"suffix={suffix_score:.2f}, "
            f"continuation={continuation_score:.2f}, "
            f"modifier_order={modifier_order_score:.2f}, "
            f"composite={realism_score:.2f}"
        )

        return {
            "suffix_chain_score": suffix_score,
            "phrase_continuation_score": (
                continuation_score
            ),
            "modifier_ordering_score": (
                modifier_order_score
            ),
            "entity_first_score": entity_first_score,
            "education_pattern_score": (
                education_pattern_score
            ),
            "composite_realism_score": realism_score,
        }

    def _analyze_suffix_chains(
        self,
        tokens: list[str],
    ) -> float:
        """
        Analyze suffix chains.
        
        E.g., after "exam" people search:
        - "exam syllabus"
        - "exam date"
        - "exam notification"
        """

        if len(tokens) < 2:
            return 0.5

        score = 0.5  # Base

        for i in range(len(tokens) - 1):
            current = tokens[i].lower()
            next_token = tokens[i + 1].lower()

            # Check if this is a common suffix
            if current in SUFFIX_CHAINS:
                common_suffixes = SUFFIX_CHAINS[
                    current
                ]

                if next_token in common_suffixes:
                    chain_score = (
                        common_suffixes[next_token]
                    )
                    score = max(score, chain_score)

        return self.normalizer.clamp(score)

    def _analyze_phrase_continuation(
        self,
        tokens: list[str],
    ) -> float:
        """
        Analyze phrase continuation quality.
        
        Natural phrases have smooth word transitions.
        """

        if len(tokens) < 2:
            return 0.75

        # Check for natural continuations
        natural_patterns = [
            # Exam patterns
            (r"^(gate|ugc|net|ssc|ibps)\s+(exam|test|recruitment)", 0.95),
            # Education patterns
            (r"^(learn|study|understand)\s+\w+\s+(for|in|from)", 0.90),
            # How-to patterns
            (r"^how\s+(to|do)\s+\w+\s+(in|for)", 0.92),
            # Temporal patterns
            (r"^\w+\s+(2024|2025|2026)", 0.85),
        ]

        keyword_str = " ".join(tokens)
        keyword_lower = keyword_str.lower()

        max_score = 0.6

        for pattern, pattern_score in natural_patterns:
            if re.match(pattern, keyword_lower):
                max_score = max(max_score, pattern_score)

        return max_score

    def _analyze_modifier_ordering(
        self,
        tokens: list[str],
    ) -> float:
        """
        Analyze modifier ordering quality.
        
        Best: modifier-entity-qualifier
        E.g., "best python tutorial 2024"
        """

        if len(tokens) < 2:
            return 0.6

        score = 0.5

        # Modifiers first is ideal
        first_token = tokens[0].lower()

        modifiers = {
            "best", "top", "latest", "official",
            "free", "easy", "new", "complete",
        }

        if first_token in modifiers:
            score += 0.20

        # Qualifiers last is good (years, editions)
        if len(tokens) > 1:
            last_token = tokens[-1].lower()

            if re.match(r"\d{4}", last_token):
                score += 0.10

        return self.normalizer.clamp(score)

    def _analyze_entity_first_pattern(
        self,
        tokens: list[str],
    ) -> float:
        """
        Analyze entity-first patterns.
        
        In education/exams, entity first is common:
        - "GATE chemistry"
        - "JEE maths"
        - "UPSC history"
        """

        if len(tokens) < 2:
            return 0.5

        first_token = tokens[0].lower()

        # Common entities that go first
        first_entities = {
            "gate", "jee", "neet", "upsc",
            "ugc", "net", "ssc", "ibps",
            "python", "java", "javascript",
        }

        if first_token in first_entities:
            return 0.85

        # Proper noun first is good
        if tokens[0] and tokens[0][0].isupper():
            return 0.75

        return 0.5

    def _analyze_education_patterns(
        self,
        keyword_lower: str,
    ) -> float:
        """
        Analyze education-specific patterns.
        
        Common in education SERPs:
        - exam names + date/syllabus/admit
        - course + duration/fees/eligibility
        - subject + chapter/topic
        """

        score = 0.5

        # Exam + time-sensitive keywords
        exam_keywords = {
            "gate", "upsc", "neet", "jee",
            "ugc", "net", "ssc", "ibps",
        }

        time_keywords = {
            "syllabus", "date", "admit", "answer",
            "result", "notification", "pattern",
            "eligibility", "fees", "duration",
        }

        exam_found = any(
            exam in keyword_lower
            for exam in exam_keywords
        )

        time_found = any(
            time in keyword_lower
            for time in time_keywords
        )

        if exam_found and time_found:
            score = 0.92  # Perfect education pattern

        elif exam_found or time_found:
            score = 0.80  # Good education signal

        return score


# =====================================================
# MAIN ADVANCED SCORING SERVICE v2.4
# =====================================================

class AdvancedScoringService:
    """
    Production-grade SEO scoring with advanced features.
    
    Features:
    1. Cross-signal intelligence (synergies/penalties)
    2. Temporal SEO awareness
    3. Semantic-role specificity
    4. SERP diversity analysis
    5. Advanced autocomplete realism
    """

    VERSION = "2.4-ADVANCED"

    # Base signal weights
    SIGNAL_WEIGHTS = {
        "query_coherence": 0.09,
        "autocomplete_alignment": 0.08,
        "entity_proximity": 0.07,
        "naturalness": 0.10,
        "completeness": 0.09,
        "specificity": 0.11,
        "intent_clarity": 0.12,
        "modifier_quality": 0.07,
        "authority": 0.06,
        "semantic_realism": 0.09,
        "answer_compatibility": 0.06,
        "source_confidence": 0.07,
        "opportunity": 0.08,
    }

    def __init__(
        self,
        keyword_data: dict[str, Any] | None = None,
    ) -> None:
        self.keyword_data = keyword_data
        self.normalizer = SignalNormalizer()

        # Advanced analyzers
        self.temporal_analyzer = (
            TemporalIntentAnalyzer()
        )
        self.semantic_analyzer = (
            SemanticRoleAnalyzer()
        )
        self.serp_diversity_analyzer = (
            SERPDiversityAnalyzer()
        )
        self.cross_signal = (
            CrossSignalIntelligence()
        )
        self.autocomplete_analyzer = (
            AdvancedAutocompleteAnalyzer()
        )

    def calculate_advanced_score(
        self,
        keyword: str,
        base_signals: dict[str, float] | None = None,
    ) -> AdvancedScoringResult:
        """
        Calculate advanced SEO score with all features.
        """

        logger.info(
            f"Advanced SEO scoring v2.4 started: {keyword}"
        )

        # =============================================
        # Use provided signals or mock them
        # =============================================

        if base_signals is None:
            base_signals = self._generate_mock_signals(
                keyword
            )

        # =============================================
        # 1. TEMPORAL ANALYSIS
        # =============================================

        temporal_analysis = (
            self.temporal_analyzer
            .analyze_temporal_intent(
                keyword,
                self.keyword_data,
            )
        )

        # =============================================
        # 2. SEMANTIC ROLE ANALYSIS
        # =============================================

        entities = (
            self._extract_entities_from_keyword_data()
        )

        semantic_roles = (
            self.semantic_analyzer
            .analyze_semantic_roles(
                keyword,
                entities,
            )
        )

        # =============================================
        # 3. SERP DIVERSITY ANALYSIS
        # =============================================

        serp_diversity = (
            self.serp_diversity_analyzer
            .analyze_serp_diversity(
                self.keyword_data
            )
        )

        # =============================================
        # 4. ADVANCED AUTOCOMPLETE ANALYSIS
        # =============================================

        autocomplete_scores = (
            self.autocomplete_analyzer
            .analyze_autocomplete_realism(
                keyword,
                self.keyword_data,
            )
        )

        # Update base signals with autocomplete realism
        base_signals["autocomplete_realism"] = (
            autocomplete_scores[
                "composite_realism_score"
            ]
        )

        # =============================================
        # 5. CROSS-SIGNAL INTELLIGENCE
        # =============================================

        interactions = (
            self.cross_signal
            .analyze_interactions(
                base_signals,
                temporal_analysis,
                semantic_roles,
            )
        )

        # =============================================
        # COMPOSITE SCORE CALCULATION
        # =============================================

        # Base composition
        base_composition = sum(
            base_signals.get(key, 0) * weight
            for key, weight in (
                self.SIGNAL_WEIGHTS.items()
            )
            if key in base_signals
        )

        logger.debug(
            f"Base composition: {base_composition:.2f}"
        )

        # Apply temporal boost
        temporal_boost = (
            temporal_analysis.boost_factor - 1.0
        )

        # Apply interaction adjustments
        interaction_adjustment = (
            interactions.total_adjustment
        )

        # Apply diversity bonus
        diversity_bonus = (
            serp_diversity.opportunity_gap * 0.05
        )

        # Final score
        final_composite = (
            base_composition +
            (base_composition * temporal_boost) +
            (base_composition * interaction_adjustment) +
            diversity_bonus
        )

        seo_score = int(
            self.normalizer.clamp(final_composite) *
            100
        )

        logger.info(
            f"Advanced scoring completed: "
            f"score={seo_score}, "
            f"temporal_boost={temporal_boost:.2f}, "
            f"interactions={interaction_adjustment:.2f}"
        )

        return AdvancedScoringResult(
            seo_score=seo_score,
            signals=base_signals,
            base_composition=base_composition,
            interactions=interactions,
            temporal_analysis=temporal_analysis,
            semantic_roles=semantic_roles,
            serp_diversity=serp_diversity,
            query_flow=autocomplete_scores,
        )

    def _generate_mock_signals(
        self,
        keyword: str,
    ) -> dict[str, float]:
        """Generate mock signals for testing."""

        tokens = keyword.split()

        return {
            "query_coherence": 0.75,
            "autocomplete_alignment": 0.72,
            "entity_proximity": 0.68,
            "naturalness": 0.78,
            "completeness": 0.74,
            "specificity": 0.76,
            "intent_clarity": 0.82,
            "modifier_quality": 0.71,
            "authority": 0.65,
            "semantic_realism": 0.73,
            "answer_compatibility": 0.69,
            "source_confidence": 0.67,
            "opportunity": 0.72,
        }

    def _extract_entities_from_keyword_data(
        self,
    ) -> dict[str, list[str]]:
        """Extract entities from keyword data."""

        if not self.keyword_data:
            return {}

        entities = {
            "brands": [],
            "products": [],
            "categories": [],
        }

        custom_entities = (
            self.keyword_data.get(
                "entities",
                {},
            )
        )

        entities.update(custom_entities)

        return entities

    def format_output(
        self,
        result: AdvancedScoringResult,
    ) -> dict[str, Any]:
        """Format result for output."""

        return {
            "seo_score": result.seo_score,
            "version": self.VERSION,
            "signals": result.signals,
            "score_composition": {
                "base_score": result.base_composition,
                "temporal_boost": (
                    result.temporal_analysis.boost_factor
                ),
                "interaction_adjustment": (
                    result.interactions.total_adjustment
                ),
            },
            "temporal_intelligence": {
                "markers": (
                    result.temporal_analysis
                    .temporal_markers_found
                ),
                "confidence": (
                    result.temporal_analysis
                    .temporal_confidence
                ),
                "freshness_score": (
                    result.temporal_analysis
                    .freshness_score
                ),
                "exam_phase": (
                    result.temporal_analysis
                    .exam_cycle_phase
                ),
                "time_sensitivity": (
                    result.temporal_analysis
                    .time_sensitivity_score
                ),
            },
            "semantic_intelligence": {
                "primary_entity": (
                    result.semantic_roles.primary_entity
                ),
                "qualifiers": (
                    result.semantic_roles.qualifiers
                ),
                "document_types": (
                    result.semantic_roles
                    .document_types
                ),
                "years": (
                    result.semantic_roles
                    .years_mentioned
                ),
                "specificity": (
                    result.semantic_roles
                    .role_specificity_score
                ),
            },
            "serp_intelligence": {
                "diversity_score": (
                    result.serp_diversity.diversity_score
                ),
                "saturation_score": (
                    result.serp_diversity.saturation_score
                ),
                "opportunity_gap": (
                    result.serp_diversity.opportunity_gap
                ),
                "ecosystem_health": (
                    result.serp_diversity.ecosystem_health
                ),
            },
            "signal_interactions": {
                "synergies": (
                    result.interactions.synergy_pairs
                ),
                "penalties": (
                    result.interactions.penalty_pairs
                ),
                "details": (
                    result.interactions
                    .interaction_details
                ),
            },
            "query_realism": {
                "suffix_chains": (
                    result.query_flow[
                        "suffix_chain_score"
                    ]
                ),
                "phrase_continuation": (
                    result.query_flow[
                        "phrase_continuation_score"
                    ]
                ),
                "modifier_ordering": (
                    result.query_flow[
                        "modifier_ordering_score"
                    ]
                ),
                "entity_first_pattern": (
                    result.query_flow[
                        "entity_first_score"
                    ]
                ),
                "education_patterns": (
                    result.query_flow[
                        "education_pattern_score"
                    ]
                ),
                "composite_realism": (
                    result.query_flow[
                        "composite_realism_score"
                    ]
                ),
            },
        }


# =====================================================
# EXAMPLE USAGE
# =====================================================

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    # Example data
    example_keyword_data = {
        "google_suggestions": [
            "gate 2025 syllabus",
            "gate 2025 exam date",
            "gate 2025 notification",
        ],
        "people_also_ask": [
            {"question": "What is GATE exam?"},
            {"question": "How to prepare for GATE?"},
        ],
        "related_searches": [
            "gate exam pattern",
            "gate admit card",
            "gate answer key",
        ],
        "competitor_data": [
            {
                "domain": "gate.iitg.ac.in",
                "domain_authority": 95,
                "title": "GATE 2025",
            },
            {
                "domain": "gatefullinformation.com",
                "domain_authority": 65,
                "title": "GATE Exam",
            },
        ],
        "entities": {
            "exams": ["GATE", "JEE", "NEET"],
            "subjects": ["Chemistry", "Physics"],
        },
    }

    # Mock base signals
    mock_signals = {
        "query_coherence": 0.85,
        "autocomplete_alignment": 0.80,
        "entity_proximity": 0.78,
        "naturalness": 0.82,
        "completeness": 0.80,
        "specificity": 0.83,
        "intent_clarity": 0.88,
        "modifier_quality": 0.76,
        "authority": 0.72,
        "semantic_realism": 0.79,
        "answer_compatibility": 0.75,
        "source_confidence": 0.78,
        "opportunity": 0.81,
    }

    # Create scorer
    scorer = AdvancedScoringService(
        example_keyword_data
    )

    # Test keywords
    test_keywords = [
        "gate 2025 chemistry syllabus pdf",
        "ugc net exam date 2026",
        "ssc gd admit card notification",
        "how to prepare for upsc ias",
    ]

    for keyword in test_keywords:
        print(f"\n{'='*70}")
        print(f"Keyword: {keyword}")
        print(f"{'='*70}")

        result = scorer.calculate_advanced_score(
            keyword,
            mock_signals,
        )

        output = scorer.format_output(result)

        print(f"\nSEO Score: {output['seo_score']}/100")

        print(f"\nTemporal Intelligence:")
        temporal = output["temporal_intelligence"]
        print(f"  Markers Found: {temporal['markers']}")
        print(
            f"  Confidence: {temporal['confidence']:.2f}"
        )
        print(
            f"  Exam Phase: {temporal['exam_phase']}"
        )
        print(
            f"  Time Sensitivity: "
            f"{temporal['time_sensitivity']:.2f}"
        )

        print(f"\nSemantic Intelligence:")
        semantic = output["semantic_intelligence"]
        print(
            f"  Primary Entity: {semantic['primary_entity']}"
        )
        print(
            f"  Qualifiers: {semantic['qualifiers']}"
        )
        print(
            f"  Specificity: {semantic['specificity']:.2f}"
        )

        print(f"\nSERP Intelligence:")
        serp = output["serp_intelligence"]
        print(
            f"  Diversity: {serp['diversity_score']:.2f}"
        )
        print(
            f"  Saturation: {serp['saturation_score']:.2f}"
        )
        print(
            f"  Opportunity: {serp['opportunity_gap']:.2f}"
        )
        print(f"  Health: {serp['ecosystem_health']}")

        print(f"\nSignal Interactions:")
        interactions = output["signal_interactions"]
        if interactions["synergies"]:
            print("  Synergies:")
            for name, score in (
                interactions["synergies"].items()
            ):
                print(f"    - {name}: {score*100:.1f}%")
        if interactions["penalties"]:
            print("  Penalties:")
            for name, score in (
                interactions["penalties"].items()
            ):
                print(f"    - {name}: {score*100:.1f}%")

        print(f"\nQuery Realism:")
        realism = output["query_realism"]
        print(
            f"  Composite: "
            f"{realism['composite_realism']:.2f}"
        )
        print(
            f"  Education Patterns: "
            f"{realism['education_patterns']:.2f}"
        )

        print(f"{'='*70}")