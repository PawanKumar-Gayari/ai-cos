"""
Production-Grade Multi-Intent SEO Intelligence Engine v2.1
=========================================================

FINAL REFINEMENT PASS:
1. Token-aware phrase boundary matching (no substrings)
2. Improved weighted aggregation (strong signals, diminishing returns)
3. Spam/modifier penalties (stuffing detection)
4. Query realism scoring (human-like phrasing)
5. Advanced confidence calibration (multi-factor)
6. Dynamic SERP ecosystem (urgency + official influence)

Pure deterministic heuristics - no ML, embeddings, or vectors.
"""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Final, Any
from math import log

logger = logging.getLogger(__name__)

# =====================================================
# INTENT TYPE DEFINITIONS
# =====================================================

class IntentType(str, Enum):
    """All supported intent types."""
    
    INFORMATIONAL = "informational"
    NAVIGATIONAL = "navigational"
    COMMERCIAL = "commercial"
    TRANSACTIONAL = "transactional"
    COMPARISON = "comparison"
    LOCAL = "local"
    
    SYLLABUS = "syllabus"
    ADMIT_CARD = "admit_card"
    RESULT = "result"
    ANSWER_KEY = "answer_key"
    CUTOFF = "cutoff"
    NOTIFICATION = "notification"
    EXAM_DATE = "exam_date"
    EXAM_PATTERN = "exam_pattern"
    ELIGIBILITY = "eligibility"
    
    RECRUITMENT = "recruitment"
    APPLICATION = "application"
    SELECTION = "selection"
    MERIT_LIST = "merit_list"
    
    PDF_DOWNLOAD = "pdf_download"
    DOCUMENT_DOWNLOAD = "document_download"
    OFFICIAL_DOCUMENT = "official_document"


# =====================================================
# ENTITY DEFINITIONS
# =====================================================

class ExamEntity(str, Enum):
    """Major exam entities."""
    
    GATE = "gate"
    UPSC = "upsc"
    SSC = "ssc"
    UGC_NET = "ugc_net"
    RPSC = "rpsc"
    REET = "reet"
    DRDO = "drdo"
    NTA = "nta"
    IBPS = "ibps"
    NEET = "neet"
    JEE = "jee"


# =====================================================
# TOKEN BOUNDARY MATCHER (New)
# =====================================================

class TokenBoundaryMatcher:
    """
    Match phrases with proper token boundaries.
    Prevents substring matches like "hall" in "shallow".
    """
    
    @staticmethod
    def matches_phrase(
        keyword: str,
        phrase: str,
    ) -> bool:
        """
        Check if phrase matches with word boundaries.
        
        Examples:
        - "answer key" matches in "answer key pdf" ✓
        - "answer" does NOT match in "unanswer" ✗
        - "pdf" matches in "answer key pdf" ✓
        """
        
        keyword_lower = keyword.lower()
        phrase_lower = phrase.lower()
        
        # Create regex with word boundaries
        escaped_phrase = re.escape(phrase_lower)
        pattern = rf"\b{escaped_phrase}\b"
        
        return bool(
            re.search(
                pattern,
                keyword_lower,
            )
        )
    
    @staticmethod
    def tokenize(keyword: str) -> list[str]:
        """Tokenize keyword into words."""
        return keyword.lower().split()
    
    @staticmethod
    def analyze_token_order(
        tokens: list[str],
    ) -> dict[str, Any]:
        """
        Analyze token order for naturalness.
        
        Returns:
        - modifier_first: bool
        - entity_position: int or -1
        - has_temporal: bool
        - has_action: bool
        """
        
        if not tokens:
            return {
                "modifier_first": False,
                "entity_position": -1,
                "has_temporal": False,
                "has_action": False,
            }
        
        modifiers = {
            "best", "top", "latest", "official",
            "new", "free", "easy", "complete",
        }
        
        temporal = {"2024", "2025", "2026"}
        
        actions = {
            "download", "pdf", "get", "find",
            "check", "see", "view",
        }
        
        modifier_first = tokens[0] in modifiers
        
        entity_position = -1
        for i, token in enumerate(tokens):
            if token in {
                "gate", "upsc", "ssc", "neet",
                "jee", "ibps", "net",
            }:
                entity_position = i
                break
        
        has_temporal = any(
            t in temporal for t in tokens
        )
        
        has_action = any(
            t in actions for t in tokens
        )
        
        return {
            "modifier_first": modifier_first,
            "entity_position": entity_position,
            "has_temporal": has_temporal,
            "has_action": has_action,
        }


# =====================================================
# SPAM/MODIFIER PENALTY (New)
# =====================================================

class SpamDetector:
    """
    Detect and penalize spam patterns.
    """
    
    @staticmethod
    def detect_modifier_spam(
        keyword: str,
    ) -> tuple[float, list[str]]:
        """
        Detect repeated or stacked modifiers.
        
        Returns:
        (penalty_score, detected_patterns)
        """
        
        tokens = keyword.lower().split()
        modifiers = {
            "best", "top", "latest", "official",
            "new", "free", "easy", "simple",
        }
        
        modifier_tokens = [
            t for t in tokens if t in modifiers
        ]
        
        patterns = []
        penalty = 0.0
        
        # =============================================
        # Repeated modifiers
        # =============================================
        
        from collections import Counter
        modifier_counts = Counter(modifier_tokens)
        
        for modifier, count in (
            modifier_counts.items()
        ):
            if count > 1:
                # Penalty: 0.05 per extra occurrence
                penalty += 0.05 * (count - 1)
                patterns.append(
                    f"repeated_{modifier}_{count}x"
                )
                logger.debug(
                    f"Spam: '{modifier}' repeated {count} times"
                )
        
        # =============================================
        # Modifier stacking (3+ modifiers in short window)
        # =============================================
        
        if len(modifier_tokens) >= 3:
            # Check for clustering
            windows = [
                tokens[i:i+3]
                for i in range(len(tokens) - 2)
            ]
            
            for window in windows:
                window_modifiers = sum(
                    1 for w in window
                    if w in modifiers
                )
                
                if window_modifiers >= 2:
                    penalty += 0.08
                    patterns.append("modifier_stacking")
                    logger.debug(
                        "Spam: Modifier stacking detected"
                    )
                    break
        
        # =============================================
        # Keyword stuffing pattern
        # =============================================
        
        if len(modifier_tokens) / len(tokens) > 0.4:
            # More than 40% modifiers = stuffing
            excess_ratio = (
                (len(modifier_tokens) / len(tokens))
                - 0.4
            )
            penalty += excess_ratio * 0.15
            patterns.append("keyword_stuffing")
            logger.debug(
                f"Spam: Keyword stuffing "
                f"({len(modifier_tokens)}/{len(tokens)})"
            )
        
        return min(0.3, penalty), patterns


# =====================================================
# QUERY REALISM SCORER (New)
# =====================================================

class QueryRealismScorer:
    """
    Score how human-like and natural the query is.
    """
    
    @staticmethod
    def score_realism(
        keyword: str,
        tokens: list[str],
    ) -> tuple[float, str]:
        """
        Score query realism (0-1).
        
        Returns:
        (realism_score, reason)
        """
        
        score = 0.5
        reasons = []
        
        # =============================================
        # Token order naturalness
        # =============================================
        
        token_analysis = (
            TokenBoundaryMatcher.analyze_token_order(
                tokens
            )
        )
        
        # Modifier first is natural
        if token_analysis["modifier_first"]:
            score += 0.15
            reasons.append("modifier_first_natural")
        
        # Entity position (earlier is better)
        if token_analysis["entity_position"] >= 0:
            entity_pos = token_analysis["entity_position"]
            if entity_pos <= 1:
                score += 0.20
            elif entity_pos <= 2:
                score += 0.10
            reasons.append(
                f"entity_position_{entity_pos}"
            )
        
        # =============================================
        # Semantic flow
        # =============================================
        
        # Question format is very natural
        question_starters = {
            "how", "what", "where", "when",
            "why", "which", "can", "does",
        }
        
        if tokens and tokens[0] in question_starters:
            score += 0.15
            reasons.append("question_format")
        
        # =============================================
        # Avoid unnatural sequences
        # =============================================
        
        keyword_lower = keyword.lower()
        
        unnatural_patterns = [
            r"\bpdf\s+pdf\b",      # "pdf pdf"
            r"\bdownload\s+download\b",  # "download download"
            r"\s{2,}",             # Multiple spaces
        ]
        
        for pattern in unnatural_patterns:
            if re.search(pattern, keyword_lower):
                score -= 0.10
                reasons.append(
                    f"unnatural_{pattern}"
                )
        
        # =============================================
        # Length penalty (very long/short)
        # =============================================
        
        if len(tokens) < 2:
            score -= 0.15
            reasons.append("too_short")
        elif len(tokens) > 8:
            score -= 0.10
            reasons.append("too_long")
        elif 3 <= len(tokens) <= 5:
            score += 0.10
            reasons.append("optimal_length")
        
        return max(0.0, min(1.0, score)), " + ".join(
            reasons
        )


# =====================================================
# ADVANCED CONFIDENCE CALIBRATOR (New)
# =====================================================

class ConfidenceCalibrator:
    """
    Calibrate confidence based on multiple factors.
    """
    
    @staticmethod
    def calibrate(
        signal_count: int,
        signal_quality: float,
        synergy_bonus: float,
        ambiguity: float,
        entity_certainty: float,
    ) -> float:
        """
        Calculate calibrated confidence.
        
        Factors:
        - signal_count: Number of matching signals (0-5)
        - signal_quality: Average weight of signals (0-1)
        - synergy_bonus: Interaction bonus (-0.3 to 0.3)
        - ambiguity: Ambiguity score (0-1)
        - entity_certainty: Entity match certainty (0-1)
        """
        
        # =============================================
        # Signal quality factor
        # =============================================
        
        # More signals = higher confidence, but with diminishing returns
        signal_factor = (
            min(signal_count, 5) / 5.0 *
            signal_quality
        )
        
        # Use logarithmic scaling for diminishing returns
        if signal_count > 1:
            signal_factor *= (
                1.0 + log(signal_count) * 0.1
            )
        
        # =============================================
        # Synergy factor
        # =============================================
        
        # Strong synergies increase confidence
        synergy_factor = 1.0 + (synergy_bonus * 0.2)
        synergy_factor = max(0.7, synergy_factor)
        
        # =============================================
        # Ambiguity factor (inverse)
        # =============================================
        
        # High ambiguity = low confidence
        ambiguity_factor = 1.0 - (ambiguity * 0.5)
        
        # =============================================
        # Entity certainty factor
        # =============================================
        
        # Known entity = higher confidence
        entity_factor = 0.5 + (entity_certainty * 0.5)
        
        # =============================================
        # Composite confidence
        # =============================================
        
        confidence = (
            (signal_factor * 0.40) +
            (synergy_factor * 0.25) +
            (ambiguity_factor * 0.20) +
            (entity_factor * 0.15)
        )
        
        return max(0.0, min(1.0, confidence))


# =====================================================
# DYNAMIC SERP PREDICTOR (Refined)
# =====================================================

class DynamicSerpPredictor:
    """
    Predict SERP ecosystem with dynamic adjustments.
    """
    
    # Base patterns (from original)
    BASE_PATTERNS: Final[
        dict[IntentType, dict[str, float]]
    ] = {
        IntentType.ANSWER_KEY: {
            "official": 0.40,
            "pdfs": 0.35,
            "blogs": 0.15,
            "videos": 0.05,
            "forums": 0.05,
        },
        IntentType.ADMIT_CARD: {
            "official": 0.50,
            "pdfs": 0.25,
            "blogs": 0.15,
            "forums": 0.05,
            "videos": 0.05,
        },
        IntentType.RESULT: {
            "official": 0.45,
            "news": 0.20,
            "blogs": 0.20,
            "pdfs": 0.10,
            "forums": 0.05,
        },
        IntentType.NOTIFICATION: {
            "official": 0.60,
            "pdfs": 0.20,
            "blogs": 0.10,
            "news": 0.05,
            "forums": 0.05,
        },
        IntentType.SYLLABUS: {
            "blogs": 0.35,
            "videos": 0.25,
            "pdfs": 0.20,
            "official": 0.15,
            "forums": 0.05,
        },
        IntentType.INFORMATIONAL: {
            "blogs": 0.35,
            "videos": 0.25,
            "official": 0.15,
            "forums": 0.15,
            "pdfs": 0.10,
        },
    }
    
    @staticmethod
    def predict_with_dynamics(
        intent_type: IntentType,
        urgency_level: str,
        has_official_marker: bool,
        has_pdf_marker: bool,
    ) -> dict[str, float]:
        """
        Predict SERP ecosystem with dynamic adjustments.
        
        Critical urgency + official signals → boost official/pdfs
        """
        
        pattern = (
            DynamicSerpPredictor.BASE_PATTERNS.get(
                intent_type,
                DynamicSerpPredictor.BASE_PATTERNS[
                    IntentType.INFORMATIONAL
                ],
            )
        ).copy()
        
        # =============================================
        # Urgency adjustment
        # =============================================
        
        if urgency_level == "critical":
            # Critical urgency = more official content
            pattern["official"] = min(
                pattern.get("official", 0.2) + 0.15,
                0.75,
            )
            pattern["blogs"] = max(
                pattern.get("blogs", 0.3) - 0.10,
                0.0,
            )
            pattern["videos"] = max(
                pattern.get("videos", 0.2) - 0.05,
                0.0,
            )
            logger.debug(
                "SERP: Critical urgency boost to official"
            )
        
        elif urgency_level == "high":
            pattern["official"] = min(
                pattern.get("official", 0.2) + 0.08,
                0.65,
            )
            pattern["blogs"] = max(
                pattern.get("blogs", 0.3) - 0.05,
                0.0,
            )
        
        # =====================================================
        # Official marker adjustment
        # =====================================================
        
        if has_official_marker:
            pattern["official"] = min(
                pattern.get("official", 0.2) + 0.10,
                0.80,
            )
            logger.debug(
                "SERP: Official marker boost"
            )
        
        # =====================================================
        # PDF marker adjustment
        # =====================================================
        
        if has_pdf_marker:
            pattern["pdfs"] = min(
                pattern.get("pdfs", 0.15) + 0.12,
                0.50,
            )
            pattern["blogs"] = max(
                pattern.get("blogs", 0.3) - 0.05,
                0.0,
            )
            logger.debug("SERP: PDF marker boost")
        
        # =====================================================
        # Normalize (ensure sum = 1.0)
        # =====================================================
        
        total = sum(pattern.values())
        if total > 0:
            pattern = {
                k: v / total for k, v in pattern.items()
            }
        
        return pattern


# =====================================================
# WEIGHTED AGGREGATOR (Refined)
# =====================================================

class WeightedSignalAggregator:
    """
    Aggregate weighted signals with diminishing returns.
    """
    
    @staticmethod
    def aggregate_signals(
        signals: list[tuple[float, float]],
    ) -> float:
        """
        Aggregate signals (value, weight) tuples.
        
        Features:
        - Preserve strong signals (weight > 0.8)
        - Reduce weak-signal dilution
        - Support diminishing returns
        
        Returns:
        aggregated score (0-1)
        """
        
        if not signals:
            return 0.0
        
        strong_signals = [
            (v, w) for v, w in signals if w > 0.8
        ]
        
        weak_signals = [
            (v, w) for v, w in signals if w <= 0.8
        ]
        
        # =============================================
        # Strong signal contribution
        # =============================================
        
        if strong_signals:
            # Average strong signals directly
            strong_contribution = sum(
                v * w for v, w in strong_signals
            ) / len(strong_signals)
        else:
            strong_contribution = 0.0
        
        # =============================================
        # Weak signal contribution (diminished)
        # =============================================
        
        if weak_signals:
            # Weak signals get discounted
            weak_contribution = (
                sum(v * w for v, w in weak_signals) /
                len(weak_signals)
            )
            
            # Logarithmic diminishing returns
            # More weak signals don't help as much
            weak_count_factor = (
                1.0 / (1.0 + log(len(weak_signals)))
            )
            
            weak_contribution *= weak_count_factor
        else:
            weak_contribution = 0.0
        
        # =============================================
        # Composite aggregation
        # =============================================
        
        # Strong signals dominate
        if strong_signals:
            score = (
                (strong_contribution * 0.8) +
                (weak_contribution * 0.2)
            )
        else:
            score = weak_contribution
        
        return max(0.0, min(1.0, score))


# =====================================================
# MAIN ANALYZER ENGINE (Refined)
# =====================================================

class WeightedBehavioralIntentAnalyzer:
    """
    Production-grade intent analyzer with refinements.
    """
    
    def __init__(self) -> None:
        self.token_matcher = TokenBoundaryMatcher()
        self.spam_detector = SpamDetector()
        self.realism_scorer = QueryRealismScorer()
        self.confidence_calibrator = (
            ConfidenceCalibrator()
        )
        self.serp_predictor = (
            DynamicSerpPredictor()
        )
        self.signal_aggregator = (
            WeightedSignalAggregator()
        )
    
    def normalize_keyword(
        self,
        keyword: str,
    ) -> str:
        """Normalize keyword."""
        keyword = keyword.strip().lower()
        keyword = re.sub(r"\s+", " ", keyword)
        return keyword
    
    def detect_entity(
        self,
        keyword: str,
    ) -> tuple[ExamEntity | None, float]:
        """
        Detect exam entity with certainty.
        
        Returns:
        (entity, certainty_score)
        """
        
        keyword_lower = keyword.lower()
        tokens = self.token_matcher.tokenize(keyword)
        
        entity_patterns: dict[
            ExamEntity,
            set[str]
        ] = {
            ExamEntity.GATE: {"gate"},
            ExamEntity.UPSC: {"upsc", "ias", "ips"},
            ExamEntity.SSC: {"ssc", "ssc gd", "ssc cgl"},
            ExamEntity.UGC_NET: {"ugc net", "net exam"},
            ExamEntity.RPSC: {"rpsc"},
            ExamEntity.REET: {"reet"},
            ExamEntity.DRDO: {"drdo"},
            ExamEntity.NTA: {"nta"},
            ExamEntity.IBPS: {"ibps"},
            ExamEntity.NEET: {"neet"},
            ExamEntity.JEE: {"jee", "jee main"},
        }
        
        best_entity = None
        best_certainty = 0.0
        
        for entity, patterns in (
            entity_patterns.items()
        ):
            for pattern in patterns:
                if self.token_matcher.matches_phrase(
                    keyword_lower,
                    pattern,
                ):
                    # Longer pattern = higher certainty
                    certainty = (
                        len(pattern.split()) / 2.0
                    )
                    certainty = min(1.0, certainty)
                    
                    if certainty > best_certainty:
                        best_entity = entity
                        best_certainty = certainty
        
        return best_entity, best_certainty
    
    def extract_temporal_markers(
        self,
        keyword: str,
    ) -> dict[str, list[str]]:
        """Extract temporal markers."""
        
        keyword_lower = keyword.lower()
        temporal_found = {}
        
        temporal_patterns = {
            "2026": 0.9,
            "2025": 0.85,
            "2024": 0.7,
            "latest": 0.85,
            "new": 0.6,
            "today": 0.85,
        }
        
        for marker, _ in temporal_patterns.items():
            if self.token_matcher.matches_phrase(
                keyword_lower,
                marker,
            ):
                temporal_found[marker] = [marker]
        
        return temporal_found
    
    def calculate_intent_score_refined(
        self,
        keyword: str,
        intent_type: IntentType,
        entity: ExamEntity | None,
        entity_certainty: float,
        temporal_markers: dict[str, list[str]],
    ) -> tuple[float, float, float]:
        """
        Calculate refined intent score.
        
        Returns:
        (base_score, confidence, realism)
        """
        
        keyword_lower = keyword.lower()
        tokens = self.token_matcher.tokenize(keyword)
        
        # =============================================
        # Detect spam patterns
        # =============================================
        
        spam_penalty, spam_patterns = (
            self.spam_detector.detect_modifier_spam(
                keyword
            )
        )
        
        logger.debug(f"Spam penalty: {spam_penalty:.2f}")
        
        # =============================================
        # Query realism
        # =============================================
        
        realism_score, realism_reasons = (
            self.realism_scorer.score_realism(
                keyword,
                tokens,
            )
        )
        
        logger.debug(
            f"Realism: {realism_score:.2f} "
            f"({realism_reasons})"
        )
        
        # =============================================
        # Token boundary matching (no substrings)
        # =============================================
        
        signals = []  # (value, weight)
        
        # Match intent-specific patterns
        intent_keywords = self._get_intent_keywords(
            intent_type
        )
        
        for keyword_pattern, weight in (
            intent_keywords.items()
        ):
            if self.token_matcher.matches_phrase(
                keyword_lower,
                keyword_pattern,
            ):
                signals.append((1.0, weight))
        
        # =============================================
        # Aggregate signals with refinements
        # =============================================
        
        base_score = (
            self.signal_aggregator.aggregate_signals(
                signals
            )
        )
        
        # =============================================
        # Apply penalties
        # =============================================
        
        base_score -= spam_penalty
        base_score = max(0.0, base_score)
        
        # =============================================
        # Apply realism boost
        # =============================================
        
        base_score *= (0.8 + realism_score * 0.2)
        
        # =============================================
        # Calibrate confidence
        # =============================================
        
        synergy_bonus = 0.0  # Simplified for now
        ambiguity = 0.5  # Placeholder
        
        confidence = (
            ConfidenceCalibrator.calibrate(
                signal_count=len(signals),
                signal_quality=(
                    sum(w for _, w in signals) /
                    len(signals)
                    if signals else 0.0
                ),
                synergy_bonus=synergy_bonus,
                ambiguity=ambiguity,
                entity_certainty=entity_certainty,
            )
        )
        
        return (
            min(1.0, base_score),
            confidence,
            realism_score,
        )
    
    def _get_intent_keywords(
        self,
        intent_type: IntentType,
    ) -> dict[str, float]:
        """Get intent-specific keywords with weights."""
        
        keywords_map = {
            IntentType.ANSWER_KEY: {
                "answer key": 1.0,
                "official answer key": 1.1,
                "answer key pdf": 1.15,
                "answer key download": 1.15,
            },
            IntentType.ADMIT_CARD: {
                "admit card": 1.0,
                "admit card pdf": 1.1,
                "admit card download": 1.1,
                "download admit card": 1.15,
            },
            IntentType.RESULT: {
                "result": 0.8,
                "result declared": 1.0,
                "result announced": 0.95,
                "results out": 1.05,
                "official result": 1.05,
            },
            IntentType.NOTIFICATION: {
                "notification": 0.75,
                "official notification": 0.95,
                "notification pdf": 0.9,
                "latest notification": 1.0,
            },
        }
        
        return keywords_map.get(intent_type, {})
    
    def analyze(
        self,
        keyword: str,
    ) -> dict[str, Any]:
        """
        Comprehensive refined analysis.
        """
        
        logger.info(
            f"Refined intent analysis: {keyword}"
        )
        
        # =============================================
        # Normalize
        # =============================================
        
        normalized = self.normalize_keyword(keyword)
        
        # =============================================
        # Detect entity with certainty
        # =============================================
        
        entity, entity_certainty = (
            self.detect_entity(normalized)
        )
        
        # =============================================
        # Extract temporal markers
        # =============================================
        
        temporal = self.extract_temporal_markers(
            normalized
        )
        
        # =============================================
        # Determine urgency level
        # =============================================
        
        urgency_level = self._determine_urgency(
            normalized,
            temporal,
        )
        
        # =============================================
        # Calculate scores for key intents
        # =============================================
        
        key_intents = [
            IntentType.ANSWER_KEY,
            IntentType.ADMIT_CARD,
            IntentType.RESULT,
            IntentType.NOTIFICATION,
        ]
        
        intent_scores = {}
        
        for intent_type in key_intents:
            score, confidence, realism = (
                self.calculate_intent_score_refined(
                    normalized,
                    intent_type,
                    entity,
                    entity_certainty,
                    temporal,
                )
            )
            
            intent_scores[intent_type.value] = {
                "score": score,
                "confidence": confidence,
                "realism": realism,
            }
        
        # Find primary
        primary_intent = max(
            intent_scores.items(),
            key=lambda x: x[1]["score"],
        )
        
        # =============================================
        # Predict SERP with dynamics
        # =============================================
        
        has_official = any(
            self.token_matcher.matches_phrase(
                normalized,
                phrase,
            )
            for phrase in ["official", "government"]
        )
        
        has_pdf = any(
            self.token_matcher.matches_phrase(
                normalized,
                phrase,
            )
            for phrase in ["pdf", "download"]
        )
        
        serp_pattern = (
            DynamicSerpPredictor.predict_with_dynamics(
                IntentType[
                    primary_intent[0].upper()
                    .replace(" ", "_")
                ],
                urgency_level,
                has_official,
                has_pdf,
            )
        )
        
        # =============================================
        # Build output
        # =============================================
        
        return {
            "keyword": keyword,
            "normalized": normalized,
            "primary_intent": primary_intent[0],
            "score": primary_intent[1]["score"],
            "confidence": primary_intent[1][
                "confidence"
            ],
            "realism": primary_intent[1]["realism"],
            "all_intents": intent_scores,
            "entity": entity.value if entity else None,
            "entity_certainty": entity_certainty,
            "urgency": urgency_level,
            "temporal": temporal,
            "serp_prediction": serp_pattern,
        }
    
    def _determine_urgency(
        self,
        keyword: str,
        temporal: dict[str, list[str]],
    ) -> str:
        """Determine urgency level."""
        
        if any(
            phrase in keyword
            for phrase in [
                "result",
                "declared",
                "admit card",
            ]
        ):
            return "critical"
        
        if any(
            phrase in keyword
            for phrase in [
                "answer key",
                "latest",
                "notification",
            ]
        ):
            return "high"
        
        if temporal:
            return "normal"
        
        return "low"


# =====================================================
# PUBLIC API
# =====================================================

class IntentService:
    """Production intent detection API."""
    
    def __init__(self) -> None:
        self.analyzer = (
            WeightedBehavioralIntentAnalyzer()
        )
    
    def analyze(
        self,
        keyword: str,
    ) -> dict[str, Any]:
        """Analyze keyword intent."""
        return self.analyzer.analyze(keyword)


# =====================================================
# EXAMPLE USAGE
# =====================================================

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    service = IntentService()
    
    test_keywords = [
        "gate 2025 chemistry answer key pdf download",
        "ssc gd admit card 2026 official pdf",
        "upsc ias result 2024 declared official",
        "best best best latest answer key official",  # spam
        "how to prepare for neet exam",
    ]
    
    for keyword in test_keywords:
        print(f"\n{'='*70}")
        print(f"Keyword: {keyword}")
        
        result = service.analyze(keyword)
        
        print(f"\nIntent: {result['primary_intent']}")
        print(f"Score: {result['score']:.2f}")
        print(f"Confidence: {result['confidence']:.2f}")
        print(f"Realism: {result['realism']:.2f}")
        
        if result['entity']:
            print(
                f"Entity: {result['entity']} "
                f"(certainty={result['entity_certainty']:.2f})"
            )
        
        print(f"Urgency: {result['urgency']}")
        
        print(f"\nSERP Prediction:")
        for fmt, ratio in result['serp_prediction'].items():
            if ratio > 0:
                print(f"  {fmt}: {ratio*100:.0f}%")
        
        print(f"{'='*70}")