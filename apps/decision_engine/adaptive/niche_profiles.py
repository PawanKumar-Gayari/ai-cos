"""
Niche Profiles

This module defines contextual editorial behavior
for different niches.

Goal:
Avoid hardcoded logic spread across the system.

Instead of:
    if niche == "jobs"

Use:
    profile = get_niche_profile(niche)

Then:
    profile.freshness_required
    profile.official_sources_required
"""

from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class NicheProfile:

    # =========================================================
    # CORE
    # =========================================================

    name: str

    description: str

    # =========================================================
    # CONTENT BEHAVIOR
    # =========================================================

    faq_priority: bool = False

    tables_priority: bool = False

    comparison_priority: bool = False

    listicle_priority: bool = False

    expert_tone: bool = False

    conversational_tone: bool = False

    # =========================================================
    # FRESHNESS + TRUST
    # =========================================================

    freshness_required: bool = False

    official_sources_required: bool = False

    authority_required: bool = False

    verification_strictness: str = "medium"

    # =========================================================
    # ARTICLE DEPTH
    # =========================================================

    article_depth: str = "medium"

    semantic_depth: str = "medium"

    # =========================================================
    # SCORING PRIORITIES
    # =========================================================

    seo_weight: float = 1.0

    quality_weight: float = 1.0

    freshness_weight: float = 1.0

    authority_weight: float = 1.0

    engagement_weight: float = 1.0

    trust_weight: float = 1.0

    # =========================================================
    # SEO + STRUCTURE
    # =========================================================

    internal_linking_priority: bool = True

    entity_coverage_required: bool = True

    schema_markup_priority: bool = False

    # =========================================================
    # SOURCE TYPES
    # =========================================================

    preferred_sources: List[str] = field(
        default_factory=list
    )

    # =========================================================
    # NOTES
    # =========================================================

    notes: List[str] = field(
        default_factory=list
    )


# =============================================================
# DEFAULT NICHE PROFILES
# =============================================================

NICHE_PROFILES: Dict[str, NicheProfile] = {

    # =========================================================
    # JOBS
    # =========================================================

    "jobs": NicheProfile(

        name="jobs",

        description=(
            "Recruitment, exams, admit cards, results, "
            "government jobs, notifications"
        ),

        faq_priority=True,

        tables_priority=True,

        freshness_required=True,

        official_sources_required=True,

        authority_required=True,

        verification_strictness="high",

        article_depth="medium",

        semantic_depth="medium",

        freshness_weight=1.8,

        trust_weight=1.7,

        authority_weight=1.5,

        schema_markup_priority=True,

        preferred_sources=[
            ".gov.in",
            ".nic.in",
            "official recruitment portals",
        ],

        notes=[
            "Freshness critical",
            "Official notifications mandatory",
            "Dates must be verified",
        ],
    ),

    # =========================================================
    # HEALTH
    # =========================================================

    "health": NicheProfile(

        name="health",

        description=(
            "Medical, healthcare, wellness, disease, "
            "nutrition, treatment content"
        ),

        faq_priority=True,

        expert_tone=True,

        authority_required=True,

        official_sources_required=True,

        freshness_required=True,

        verification_strictness="very_high",

        article_depth="high",

        semantic_depth="high",

        authority_weight=2.0,

        trust_weight=2.0,

        quality_weight=1.6,

        preferred_sources=[
            "WHO",
            "NIH",
            "CDC",
            "PubMed",
        ],

        notes=[
            "Medical accuracy critical",
            "Strong authority signals required",
        ],
    ),

    # =========================================================
    # FINANCE
    # =========================================================

    "finance": NicheProfile(

        name="finance",

        description=(
            "Banking, investing, taxes, loans, "
            "insurance, stock market"
        ),

        faq_priority=True,

        tables_priority=True,

        authority_required=True,

        official_sources_required=True,

        freshness_required=True,

        verification_strictness="very_high",

        article_depth="high",

        trust_weight=2.0,

        authority_weight=1.8,

        freshness_weight=1.5,

        preferred_sources=[
            "RBI",
            "SEBI",
            "official exchanges",
        ],

        notes=[
            "Financial misinformation risk high",
            "Trust signals required",
        ],
    ),

    # =========================================================
    # TECH
    # =========================================================

    "tech": NicheProfile(

        name="tech",

        description=(
            "Technology, AI, gadgets, software, "
            "coding, cybersecurity"
        ),

        comparison_priority=True,

        freshness_required=True,

        article_depth="high",

        semantic_depth="high",

        seo_weight=1.4,

        freshness_weight=1.4,

        engagement_weight=1.3,

        preferred_sources=[
            "official docs",
            "GitHub",
            "vendor blogs",
        ],

        notes=[
            "Freshness moderately important",
            "Comparisons perform well",
        ],
    ),

    # =========================================================
    # EDUCATION
    # =========================================================

    "education": NicheProfile(

        name="education",

        description=(
            "Study material, exams, syllabus, "
            "academic guidance"
        ),

        faq_priority=True,

        tables_priority=True,

        authority_required=True,

        article_depth="high",

        semantic_depth="high",

        quality_weight=1.6,

        authority_weight=1.3,

        preferred_sources=[
            "official universities",
            "educational boards",
        ],

        notes=[
            "Clarity and readability important",
        ],
    ),

    # =========================================================
    # SEO
    # =========================================================

    "seo": NicheProfile(

        name="seo",

        description=(
            "SEO, blogging, digital marketing, "
            "ranking strategies"
        ),

        comparison_priority=True,

        listicle_priority=True,

        article_depth="high",

        semantic_depth="high",

        seo_weight=2.0,

        engagement_weight=1.5,

        preferred_sources=[
            "Google Search Central",
            "Ahrefs",
            "Semrush",
        ],

        notes=[
            "Entity coverage important",
            "SERP analysis critical",
        ],
    ),

    # =========================================================
    # DEFAULT
    # =========================================================

    "default": NicheProfile(

        name="default",

        description="Generic fallback profile",

        article_depth="medium",

        semantic_depth="medium",

        verification_strictness="medium",

        notes=[
            "Fallback profile",
        ],
    ),
}


# =============================================================
# PROFILE HELPERS
# =============================================================

def get_niche_profile(
    niche: str,
) -> NicheProfile:

    """
    Get niche profile safely.
    """

    niche = (niche or "").lower().strip()

    return NICHE_PROFILES.get(
        niche,
        NICHE_PROFILES["default"],
    )


def profile_exists(
    niche: str,
) -> bool:

    return niche.lower() in NICHE_PROFILES


def list_profiles() -> List[str]:

    return list(
        NICHE_PROFILES.keys()
    )


def detect_niche_profile(
    topic: str,
) -> NicheProfile:

    """
    Lightweight topic-based niche detection.
    Future versions should use:
    - ML classification
    - embeddings
    - semantic intent detection
    """

    topic = (topic or "").lower()

    jobs_keywords = [
        "recruitment",
        "vacancy",
        "result",
        "admit card",
        "exam",
        "notification",
    ]

    health_keywords = [
        "disease",
        "treatment",
        "health",
        "medicine",
        "symptoms",
    ]

    tech_keywords = [
        "ai",
        "software",
        "coding",
        "python",
        "technology",
    ]

    finance_keywords = [
        "loan",
        "bank",
        "stock",
        "finance",
        "investment",
    ]

    if any(
        keyword in topic
        for keyword in jobs_keywords
    ):
        return get_niche_profile("jobs")

    if any(
        keyword in topic
        for keyword in health_keywords
    ):
        return get_niche_profile("health")

    if any(
        keyword in topic
        for keyword in tech_keywords
    ):
        return get_niche_profile("tech")

    if any(
        keyword in topic
        for keyword in finance_keywords
    ):
        return get_niche_profile("finance")

    return get_niche_profile("default")