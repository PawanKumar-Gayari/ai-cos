"""
SERP Context Engine

This module analyzes SERP intelligence signals.

Goal:
Understand what currently dominates the search results.

This helps the system decide:
- article structure
- FAQ necessity
- table usage
- video competition
- snippet optimization
- freshness dominance
- authority pressure

Future versions can integrate:
- live Google SERP APIs
- vector SERP analysis
- competitor embeddings
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List


# =============================================================
# SERP CONTEXT
# =============================================================

@dataclass
class SerpContext:

    faq_dominant: bool = False

    tables_common: bool = False

    video_heavy: bool = False

    featured_snippet: bool = False

    freshness_dominant: bool = False

    authority_sites_dominant: bool = False

    forum_results_present: bool = False

    ecommerce_dominant: bool = False

    average_content_depth: str = "medium"

    serp_complexity_score: float = 50.0

    notes: List[str] = field(
        default_factory=list
    )


# =============================================================
# SERP CONTEXT ENGINE
# =============================================================

class SerpContextEngine:

    """
    Extracts strategic SERP intelligence.
    """

    # =========================================================
    # MAIN ENTRY
    # =========================================================

    def build(
        self,
        serp_data: Dict[str, Any] = None,
    ) -> Dict[str, Any]:

        serp_data = serp_data or {}

        context = SerpContext()

        self._detect_faq_presence(
            context,
            serp_data,
        )

        self._detect_tables(
            context,
            serp_data,
        )

        self._detect_videos(
            context,
            serp_data,
        )

        self._detect_featured_snippets(
            context,
            serp_data,
        )

        self._detect_freshness_dominance(
            context,
            serp_data,
        )

        self._detect_authority_sites(
            context,
            serp_data,
        )

        self._detect_forum_results(
            context,
            serp_data,
        )

        self._detect_ecommerce_results(
            context,
            serp_data,
        )

        self._estimate_content_depth(
            context,
            serp_data,
        )

        self._calculate_complexity(
            context,
        )

        return self.export(context)

    # =========================================================
    # FAQ
    # =========================================================

    def _detect_faq_presence(
        self,
        context: SerpContext,
        serp_data: Dict[str, Any],
    ) -> None:

        faq_count = serp_data.get(
            "faq_results",
            0,
        )

        if faq_count >= 3:

            context.faq_dominant = True

            context.notes.append(
                "FAQ-heavy SERP detected"
            )

    # =========================================================
    # TABLES
    # =========================================================

    def _detect_tables(
        self,
        context: SerpContext,
        serp_data: Dict[str, Any],
    ) -> None:

        table_count = serp_data.get(
            "table_results",
            0,
        )

        if table_count >= 2:

            context.tables_common = True

            context.notes.append(
                "Table-based SERP structure detected"
            )

    # =========================================================
    # VIDEOS
    # =========================================================

    def _detect_videos(
        self,
        context: SerpContext,
        serp_data: Dict[str, Any],
    ) -> None:

        video_count = serp_data.get(
            "video_results",
            0,
        )

        if video_count >= 2:

            context.video_heavy = True

            context.notes.append(
                "Video-heavy SERP detected"
            )

    # =========================================================
    # FEATURED SNIPPETS
    # =========================================================

    def _detect_featured_snippets(
        self,
        context: SerpContext,
        serp_data: Dict[str, Any],
    ) -> None:

        if serp_data.get(
            "featured_snippet",
            False,
        ):

            context.featured_snippet = True

            context.notes.append(
                "Featured snippet opportunity detected"
            )

    # =========================================================
    # FRESHNESS
    # =========================================================

    def _detect_freshness_dominance(
        self,
        context: SerpContext,
        serp_data: Dict[str, Any],
    ) -> None:

        recent_results = serp_data.get(
            "recent_results",
            0,
        )

        if recent_results >= 5:

            context.freshness_dominant = True

            context.notes.append(
                "Fresh content dominates SERP"
            )

    # =========================================================
    # AUTHORITY SITES
    # =========================================================

    def _detect_authority_sites(
        self,
        context: SerpContext,
        serp_data: Dict[str, Any],
    ) -> None:

        authority_domains = serp_data.get(
            "authority_domains",
            [],
        )

        if len(authority_domains) >= 5:

            context.authority_sites_dominant = True

            context.notes.append(
                "Authority domains dominate rankings"
            )

    # =========================================================
    # FORUM RESULTS
    # =========================================================

    def _detect_forum_results(
        self,
        context: SerpContext,
        serp_data: Dict[str, Any],
    ) -> None:

        forum_count = serp_data.get(
            "forum_results",
            0,
        )

        if forum_count >= 2:

            context.forum_results_present = True

            context.notes.append(
                "Forum/community results present"
            )

    # =========================================================
    # ECOMMERCE
    # =========================================================

    def _detect_ecommerce_results(
        self,
        context: SerpContext,
        serp_data: Dict[str, Any],
    ) -> None:

        ecommerce_count = serp_data.get(
            "ecommerce_results",
            0,
        )

        if ecommerce_count >= 3:

            context.ecommerce_dominant = True

            context.notes.append(
                "E-commerce dominant SERP"
            )

    # =========================================================
    # CONTENT DEPTH
    # =========================================================

    def _estimate_content_depth(
        self,
        context: SerpContext,
        serp_data: Dict[str, Any],
    ) -> None:

        avg_word_count = serp_data.get(
            "average_word_count",
            1500,
        )

        if avg_word_count >= 3000:

            context.average_content_depth = (
                "very_high"
            )

        elif avg_word_count >= 2000:

            context.average_content_depth = (
                "high"
            )

        elif avg_word_count >= 1000:

            context.average_content_depth = (
                "medium"
            )

        else:

            context.average_content_depth = (
                "low"
            )

    # =========================================================
    # COMPLEXITY SCORE
    # =========================================================

    def _calculate_complexity(
        self,
        context: SerpContext,
    ) -> None:

        score = 50

        if context.featured_snippet:
            score += 10

        if context.video_heavy:
            score += 10

        if context.authority_sites_dominant:
            score += 15

        if context.freshness_dominant:
            score += 10

        if context.faq_dominant:
            score += 5

        if context.tables_common:
            score += 5

        if context.ecommerce_dominant:
            score += 10

        context.serp_complexity_score = min(
            score,
            100,
        )

    # =========================================================
    # EXPORT
    # =========================================================

    def export(
        self,
        context: SerpContext,
    ) -> Dict[str, Any]:

        return {
            "faq_dominant": (
                context.faq_dominant
            ),
            "tables_common": (
                context.tables_common
            ),
            "video_heavy": (
                context.video_heavy
            ),
            "featured_snippet": (
                context.featured_snippet
            ),
            "freshness_dominant": (
                context.freshness_dominant
            ),
            "authority_sites_dominant": (
                context.authority_sites_dominant
            ),
            "forum_results_present": (
                context.forum_results_present
            ),
            "ecommerce_dominant": (
                context.ecommerce_dominant
            ),
            "average_content_depth": (
                context.average_content_depth
            ),
            "complexity_score": (
                context.serp_complexity_score
            ),
            "notes": context.notes,
        }