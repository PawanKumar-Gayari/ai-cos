"""
Advanced AI SEO content generation service — God-level edition.
"""

from __future__ import annotations

import json
import logging
import re
import time
from dataclasses import dataclass, field
from typing import Any

from django.utils.text import slugify

from apps.generator.clients.router import AIRouter

# =========================
# LOGGER
# =========================

logger = logging.getLogger(__name__)


# =========================
# CONSTANTS
# =========================

MIN_CONTENT_LENGTH = 300
MIN_WORD_TARGET   = 1200
MAX_RETRIES       = 3
RETRY_BASE_DELAY  = 1.0          # seconds (doubles each attempt)
SEO_TITLE_LIMIT   = 60           # characters
META_DESC_LIMIT   = 160          # characters


# =========================
# DATA SCHEMAS
# =========================

@dataclass
class KeywordData:
    keyword:    str
    intent:     str  = "informational"
    difficulty: str  = "medium"
    volume:     int  = 0

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "KeywordData":
        keyword = data.get("keyword", "").strip()
        if not keyword:
            raise ValueError("keyword is required and must not be blank.")
        return cls(
            keyword    = keyword,
            intent     = data.get("intent",     "informational"),
            difficulty = data.get("difficulty", "medium"),
            volume     = int(data.get("volume", 0)),
        )


@dataclass
class GeneratedArticle:
    title:            str
    slug:             str
    meta_description: str
    content:          str
    faq:              str
    conclusion:       str
    seo_score:        int
    word_count:       int
    verified:         bool

    def to_dict(self) -> dict[str, Any]:
        return {
            "title":            self.title,
            "slug":             self.slug,
            "meta_description": self.meta_description,
            "content":          self.content,
            "faq":              self.faq,
            "conclusion":       self.conclusion,
            "seo_score":        self.seo_score,
            "word_count":       self.word_count,
            "verified":         self.verified,
        }


# =========================
# PROMPT BUILDER
# =========================

class SEOPromptBuilder:
    """Builds structured SEO generation prompts."""

    _TEMPLATE = """
You are a senior SEO content strategist and copywriter.

Write a comprehensive, human-like, SEO-optimised article.

── KEYWORD ──────────────────────
{keyword}

── SEARCH INTENT ────────────────
{intent}

── SEO DIFFICULTY ───────────────
{difficulty}

── MONTHLY SEARCH VOLUME ────────
{volume}

── CONTENT REQUIREMENTS ─────────
• SEO-optimised title (≤ {title_limit} chars)
• Compelling meta description (≤ {meta_limit} chars)
• Minimum {min_words} words of body content
• Natural use of keyword + semantic variations
• Clear H1 → H2 → H3 heading hierarchy
• Practical tips, real-world examples, data points
• Dedicated FAQ section (≥ 5 Q&A pairs)
• Strong conclusion with a clear call-to-action
• Engaging, conversational, human tone — no AI filler phrases
• Bullet points and numbered lists where appropriate

── OUTPUT FORMAT ─────────────────
Return ONLY valid JSON — no markdown fences, no preamble.

{{
    "title":            "<SEO title string>",
    "meta_description": "<meta description string>",
    "content":          "<full article body in Markdown>",
    "faq":              "<FAQ section in Markdown>",
    "conclusion":       "<conclusion paragraph>"
}}
""".strip()

    @classmethod
    def build(cls, kw: KeywordData) -> str:
        return cls._TEMPLATE.format(
            keyword    = kw.keyword,
            intent     = kw.intent,
            difficulty = kw.difficulty,
            volume     = f"{kw.volume:,}",
            title_limit = SEO_TITLE_LIMIT,
            meta_limit  = META_DESC_LIMIT,
            min_words   = MIN_WORD_TARGET,
        )


# =========================
# FALLBACK CONTENT FACTORY
# =========================

class FallbackContentFactory:
    """Returns a minimal safe article when all AI attempts fail."""

    @staticmethod
    def build(kw: KeywordData) -> dict[str, str]:
        k = kw.keyword
        return {
            "title": f"Complete Guide to {k}",
            "meta_description": (
                f"Discover everything you need to know about {k}. "
                f"Tips, benefits, FAQs, and expert advice."
            ),
            "content": f"""# Complete Guide to {k}

## Introduction

{k} is a subject that attracts growing interest across industries.
This guide breaks down what you need to know — clearly and concisely.

## Why {k} Matters

- Helps you make informed decisions
- Saves time through structured knowledge
- Keeps you ahead of the curve

## Key Principles of {k}

1. **Research** — understand the landscape before acting.
2. **Compare** — evaluate your options objectively.
3. **Apply** — put best practices into action.
4. **Iterate** — measure results and refine your approach.

## Frequently Asked Questions

### What is {k}?
{k} refers to a widely-discussed topic with applications across many fields.

### Is {k} suitable for beginners?
Yes — with the right guidance, anyone can grasp the fundamentals quickly.

### How do I get started with {k}?
Begin with foundational research, then apply small-scale experiments.

## Conclusion

Mastering {k} is within reach. Start with the basics, stay consistent,
and you'll see measurable progress.
""",
            "faq": f"### What is {k}?\n{k} is a popular topic with broad applications.",
            "conclusion": (
                f"Understanding {k} empowers better decisions "
                f"and long-term success."
            ),
        }


# =========================
# CONTENT PARSER
# =========================

class ContentParser:
    """
    Converts raw AI output (JSON string or plain text)
    into a normalised dict.
    """

    # Strip common markdown code-fence wrappers
    _FENCE_RE = re.compile(r"^```(?:json)?\s*|\s*```$", re.MULTILINE)

    @classmethod
    def parse(cls, raw: str, keyword: str) -> dict[str, str]:
        cleaned = cls._FENCE_RE.sub("", raw).strip()

        # ── Attempt 1: strict JSON ──────────────────────
        try:
            data = json.loads(cleaned)
            if isinstance(data, dict):
                return data
        except json.JSONDecodeError:
            pass

        # ── Attempt 2: extract first JSON object ───────
        brace_match = re.search(r"\{.*\}", cleaned, re.DOTALL)
        if brace_match:
            try:
                data = json.loads(brace_match.group())
                if isinstance(data, dict):
                    return data
            except json.JSONDecodeError:
                pass

        # ── Attempt 3: regex field extraction ──────────
        logger.warning(
            "JSON parse failed for keyword=%r; falling back to regex extraction.",
            keyword,
        )
        return cls._extract_fields(cleaned, keyword)

    # ── helpers ──────────────────────────────────────────

    @staticmethod
    def _extract_fields(text: str, keyword: str) -> dict[str, str]:
        def _grab(pattern: str) -> str:
            m = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
            return m.group(1).strip() if m else ""

        return {
            "title":            _grab(r"(?:seo\s+)?title\s*:\s*(.+)"),
            "meta_description": _grab(r"meta\s+description\s*:\s*(.+)"),
            "content":          text,   # treat the whole blob as content
            "faq":              _grab(r"(##\s*faq.*?)(?=##|\Z)"),
            "conclusion":       _grab(r"(##\s*conclusion.*?)(?=##|\Z)"),
        }


# =========================
# SEO SCORER
# =========================

class SEOScorer:
    """
    Heuristic SEO quality scorer (0–100).
    Replaces the hardcoded 90.
    """

    @staticmethod
    def score(article: dict[str, str], kw: KeywordData) -> int:
        keyword   = kw.keyword.lower()
        content   = (article.get("content") or "").lower()
        title     = (article.get("title") or "").lower()
        meta      = (article.get("meta_description") or "").lower()
        faq       = (article.get("faq") or "").lower()
        word_count = len(content.split())

        pts = 0

        # Title checks (25 pts)
        if keyword in title:                          pts += 15
        if len(title) <= SEO_TITLE_LIMIT:             pts += 10

        # Meta checks (20 pts)
        if keyword in meta:                           pts += 10
        if 50 <= len(meta) <= META_DESC_LIMIT:        pts += 10

        # Content depth (30 pts)
        if word_count >= MIN_WORD_TARGET:             pts += 15
        if word_count >= MIN_WORD_TARGET * 1.5:       pts += 10
        heading_count = len(re.findall(r"^#{1,3}\s", content, re.MULTILINE))
        if heading_count >= 5:                        pts += 5

        # FAQ presence (10 pts)
        if faq and len(faq) > 100:                    pts += 10

        # Keyword density (15 pts)
        occurrences = content.count(keyword)
        density     = occurrences / max(word_count, 1) * 100
        if 0.5 <= density <= 2.5:                     pts += 15
        elif density > 0:                             pts += 5

        return min(pts, 100)


# =========================
# GENERATION SERVICE
# =========================

class GenerationService:
    """
    Orchestrates AI-powered SEO article generation with:
    - Input validation via KeywordData
    - Structured prompt building
    - Retry logic with exponential back-off
    - Graceful fallback on total failure
    - Real SEO scoring
    - Fully typed output
    """

    def __init__(self) -> None:
        self.ai_router = AIRouter()

    # ──────────────────────────────────────────────────────
    # PUBLIC API
    # ──────────────────────────────────────────────────────

    def generate(self, keyword_data: dict[str, Any]) -> dict[str, Any]:
        """
        Generate an SEO article for the given keyword data.

        Args:
            keyword_data: dict with keys: keyword, intent, difficulty, volume

        Returns:
            Serialised GeneratedArticle dict.

        Raises:
            ValueError: if keyword is missing or blank.
            RuntimeError: if generated content is empty or too short.
        """
        kw     = KeywordData.from_dict(keyword_data)
        prompt = SEOPromptBuilder.build(kw)

        raw = self._generate_with_retry(prompt, kw)
        article_dict = (
            ContentParser.parse(raw, kw.keyword)
            if isinstance(raw, str)
            else raw
        )

        return self._build_article(article_dict, kw).to_dict()

    # ──────────────────────────────────────────────────────
    # PRIVATE — RETRY LOGIC
    # ──────────────────────────────────────────────────────

    def _generate_with_retry(
        self,
        prompt: str,
        kw: KeywordData,
    ) -> str | dict:
        """
        Call AIRouter up to MAX_RETRIES times with exponential back-off.
        Returns fallback content dict if all attempts fail.
        """
        last_error: Exception | None = None

        for attempt in range(1, MAX_RETRIES + 1):
            try:
                result = self.ai_router.generate_content(prompt)
                if result:
                    logger.info(
                        "AI generation succeeded on attempt %d for keyword=%r.",
                        attempt, kw.keyword,
                    )
                    return result

                logger.warning(
                    "Attempt %d returned empty result for keyword=%r.",
                    attempt, kw.keyword,
                )

            except Exception as exc:
                last_error = exc
                logger.warning(
                    "Attempt %d failed for keyword=%r: %s",
                    attempt, kw.keyword, exc,
                )

            if attempt < MAX_RETRIES:
                delay = RETRY_BASE_DELAY * (2 ** (attempt - 1))
                logger.debug("Waiting %.1fs before retry %d.", delay, attempt + 1)
                time.sleep(delay)

        logger.error(
            "All %d attempts failed for keyword=%r. Last error: %s. "
            "Using fallback content.",
            MAX_RETRIES, kw.keyword, last_error,
        )
        return FallbackContentFactory.build(kw)

    # ──────────────────────────────────────────────────────
    # PRIVATE — ARTICLE ASSEMBLY
    # ──────────────────────────────────────────────────────

    def _build_article(
        self,
        data: dict[str, Any],
        kw: KeywordData,
    ) -> GeneratedArticle:
        """
        Validate, enrich, and assemble the final GeneratedArticle.

        Raises:
            RuntimeError: if content is empty or below MIN_CONTENT_LENGTH.
        """
        title            = (data.get("title") or "").strip()
        meta_description = (data.get("meta_description") or "").strip()
        content          = (data.get("content") or "").strip()
        faq              = (data.get("faq") or "").strip()
        conclusion       = (data.get("conclusion") or "").strip()

        # ── Fallback values ────────────────────────────
        if not title:
            title = f"Complete Guide to {kw.keyword}"
            logger.debug("Title missing; using fallback.")

        if not meta_description:
            meta_description = (
                f"Learn everything about {kw.keyword} "
                f"in this detailed, expert guide."
            )
            logger.debug("Meta description missing; using fallback.")

        # ── Content validation ─────────────────────────
        if not content:
            raise RuntimeError(
                f"Generated content is empty for keyword={kw.keyword!r}."
            )

        if len(content) < MIN_CONTENT_LENGTH:
            raise RuntimeError(
                f"Generated content too short ({len(content)} chars) "
                f"for keyword={kw.keyword!r}. "
                f"Minimum is {MIN_CONTENT_LENGTH} chars."
            )

        # ── Truncate oversized SEO fields ─────────────
        if len(title) > SEO_TITLE_LIMIT:
            logger.warning(
                "Title exceeds %d chars; truncating.", SEO_TITLE_LIMIT
            )
            title = title[:SEO_TITLE_LIMIT].rsplit(" ", 1)[0]

        if len(meta_description) > META_DESC_LIMIT:
            logger.warning(
                "Meta description exceeds %d chars; truncating.", META_DESC_LIMIT
            )
            meta_description = (
                meta_description[:META_DESC_LIMIT - 1].rsplit(" ", 1)[0] + "…"
            )

        # ── Score ──────────────────────────────────────
        seo_score  = SEOScorer.score(data, kw)
        word_count = len(content.split())

        logger.info(
            "Article built: keyword=%r | words=%d | seo_score=%d",
            kw.keyword, word_count, seo_score,
        )

        return GeneratedArticle(
            title            = title,
            slug             = slugify(title),
            meta_description = meta_description,
            content          = content,
            faq              = faq,
            conclusion       = conclusion,
            seo_score        = seo_score,
            word_count       = word_count,
            verified         = True,
        )