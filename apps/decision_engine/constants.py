"""
Decision engine constants.
"""

# ======================================================
# ENGINE
# ======================================================

ENGINE_NAME = (
    "decision_engine"
)

ENGINE_VERSION = (
    "1.0.0"
)

# ======================================================
# PROVIDERS
# ======================================================

PROVIDER_OLLAMA = (
    "ollama"
)

PROVIDER_OPENAI = (
    "openai"
)

PROVIDER_GEMINI = (
    "gemini"
)

SUPPORTED_PROVIDERS = [

    PROVIDER_OLLAMA,

    PROVIDER_OPENAI,

    PROVIDER_GEMINI,
]

# ======================================================
# STATUS
# ======================================================

STATUS_SUCCESS = (
    "success"
)

STATUS_FAILED = (
    "failed"
)

STATUS_PENDING = (
    "pending"
)

STATUS_PROCESSING = (
    "processing"
)

# ======================================================
# SEARCH INTENT
# ======================================================

INTENT_INFORMATIONAL = (
    "informational"
)

INTENT_COMMERCIAL = (
    "commercial"
)

INTENT_GENERAL = (
    "general"
)

SUPPORTED_INTENTS = [

    INTENT_INFORMATIONAL,

    INTENT_COMMERCIAL,

    INTENT_GENERAL,
]

# ======================================================
# ARTICLE TYPES
# ======================================================

ARTICLE_GUIDE = (
    "guide"
)

ARTICLE_LISTICLE = (
    "listicle"
)

ARTICLE_BLOG = (
    "blog"
)

# ======================================================
# CONTENT DEPTH
# ======================================================

DEPTH_LOW = (
    "low"
)

DEPTH_MEDIUM = (
    "medium"
)

DEPTH_HIGH = (
    "high"
)

# ======================================================
# SCORE LIMITS
# ======================================================

MAX_SCORE = 100

MIN_SCORE = 0

SEO_SCORE_THRESHOLD = 50

QUALITY_SCORE_THRESHOLD = 60

HIGH_COMPETITION_THRESHOLD = 80

MEDIUM_COMPETITION_THRESHOLD = 50

# ======================================================
# WORD TARGETS
# ======================================================

LOW_DEPTH_WORDS = 1000

MEDIUM_DEPTH_WORDS = 2000

HIGH_DEPTH_WORDS = 3500