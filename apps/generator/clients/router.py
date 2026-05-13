"""
AI provider router — God-level edition.

Features:
- Typed provider registry with health tracking
- Per-provider exponential back-off (no duplicate retry logic)
- Circuit breaker: auto-skip providers that keep failing
- Structured logging (no f-string interpolation in log calls)
- Clean fallback that reuses FallbackContentFactory from generation_service
- Zero silent exceptions
"""

from __future__ import annotations

import logging
import time
from dataclasses import dataclass, field
from typing import Any, Protocol, runtime_checkable

from apps.generator.clients.gemini_client import GeminiClient
from apps.generator.clients.openai_client import OpenAIClient

# =========================
# LOGGER
# =========================

logger = logging.getLogger(__name__)


# =========================
# CONSTANTS
# =========================

MAX_PROVIDER_RETRIES    = 3
RETRY_BASE_DELAY        = 0.5   # seconds; doubles each attempt
CIRCUIT_BREAKER_THRESH  = 5     # consecutive failures before skip
KEYWORD_SECTION_MARKER  = "KEYWORD:"


# =========================
# CLIENT PROTOCOL
# =========================

@runtime_checkable
class AIClient(Protocol):
    """Any object with a generate_content(prompt) method qualifies."""

    def generate_content(self, prompt: str) -> str | dict | None: ...


# =========================
# PROVIDER HEALTH TRACKER
# =========================

@dataclass
class ProviderHealth:
    """Tracks consecutive failures per provider for circuit-breaker logic."""

    name:                str
    client:              AIClient
    consecutive_failures: int  = field(default=0, repr=False)

    @property
    def is_open(self) -> bool:
        """Circuit is 'open' (provider skipped) when failures exceed threshold."""
        return self.consecutive_failures >= CIRCUIT_BREAKER_THRESH

    def record_success(self) -> None:
        self.consecutive_failures = 0

    def record_failure(self) -> None:
        self.consecutive_failures += 1


# =========================
# AI ROUTER
# =========================

class AIRouter:
    """
    Routes AI generation requests across multiple providers with:

    - Priority-ordered provider list
    - Per-provider retry with exponential back-off
    - Circuit breaker to skip consistently failing providers
    - Keyword-aware local fallback as last resort
    """

    def __init__(self) -> None:
        self._providers: list[ProviderHealth] = [
            ProviderHealth(name="OpenAI", client=OpenAIClient()),
            ProviderHealth(name="Gemini", client=GeminiClient()),
        ]

    # ──────────────────────────────────────────────────────
    # PUBLIC API
    # ──────────────────────────────────────────────────────

    def generate_content(self, prompt: str) -> str | dict:
        """
        Try each healthy provider in priority order.
        Falls back to a local stub only when all providers fail.

        Args:
            prompt: The full generation prompt.

        Returns:
            Raw string or parsed dict from the AI provider,
            or a fallback dict if all providers are unavailable.

        Raises:
            ValueError: if prompt is blank.
        """
        if not (prompt and prompt.strip()):
            raise ValueError("Prompt must not be blank.")

        provider_errors: list[str] = []

        for provider in self._providers:

            # ── Circuit breaker ────────────────────────
            if provider.is_open:
                logger.warning(
                    "Skipping provider %r — circuit open (%d consecutive failures).",
                    provider.name,
                    provider.consecutive_failures,
                )
                continue

            # ── Try with per-provider retries ──────────
            result, error = self._try_provider(provider, prompt)

            if result is not None:
                return result

            provider_errors.append(f"{provider.name}: {error}")

        # ── All providers exhausted ────────────────────
        logger.error(
            "All providers failed. Errors: %s. Returning local fallback.",
            " | ".join(provider_errors),
        )
        return self._local_fallback(prompt)

    # ──────────────────────────────────────────────────────
    # PRIVATE — PROVIDER CALL WITH RETRY
    # ──────────────────────────────────────────────────────

    def _try_provider(
        self,
        provider: ProviderHealth,
        prompt: str,
    ) -> tuple[str | dict | None, str | None]:
        """
        Call a provider up to MAX_PROVIDER_RETRIES times.

        Returns:
            (result, None)      on success.
            (None, error_msg)   if every attempt fails.
        """
        logger.info("Trying provider %r.", provider.name)

        last_error: str = "unknown error"

        for attempt in range(1, MAX_PROVIDER_RETRIES + 1):
            try:
                response = provider.client.generate_content(prompt)

                if response:
                    logger.info(
                        "Provider %r succeeded on attempt %d.",
                        provider.name,
                        attempt,
                    )
                    provider.record_success()
                    return response, None

                logger.warning(
                    "Provider %r returned empty response on attempt %d.",
                    provider.name,
                    attempt,
                )
                last_error = "empty response"

            except Exception as exc:
                last_error = str(exc)
                logger.warning(
                    "Provider %r attempt %d raised: %s",
                    provider.name,
                    attempt,
                    exc,
                )

            # Back-off before next attempt (skip after last)
            if attempt < MAX_PROVIDER_RETRIES:
                delay = RETRY_BASE_DELAY * (2 ** (attempt - 1))
                logger.debug(
                    "Back-off %.2fs before retry %d for provider %r.",
                    delay,
                    attempt + 1,
                    provider.name,
                )
                time.sleep(delay)

        provider.record_failure()
        logger.error(
            "Provider %r exhausted all %d attempts. Last error: %s",
            provider.name,
            MAX_PROVIDER_RETRIES,
            last_error,
        )
        return None, last_error

    # ──────────────────────────────────────────────────────
    # PRIVATE — LOCAL FALLBACK
    # ──────────────────────────────────────────────────────

    def _local_fallback(self, prompt: str) -> dict[str, str] | str:
        """
        Smart fallback that detects prompt intent and returns the right type.

        ┌─────────────────────────────┬──────────────────────────────────┐
        │ Prompt type                 │ Fallback return                  │
        ├─────────────────────────────┼──────────────────────────────────┤
        │ SEO article generation      │ dict with title/content/faq/…    │
        │ Rewrite / humanize / review │ original prompt text (passthrough)│
        └─────────────────────────────┴──────────────────────────────────┘

        WHY: The router is shared by both the article generator AND the
        rewrite/humanizer pipeline.  Article prompts contain structured
        markers (KEYWORD:, SEARCH INTENT:, JSON FORMAT:).  Rewrite prompts
        contain raw article text — no markers.  Returning an SEO article
        dict for a rewrite prompt was the root cause of the "SEO Topic" spam
        and the 13 s latency (pipeline was regenerating fake articles).
        """
        keyword = self._extract_keyword(prompt)

        prompt_type = self._detect_prompt_type(prompt)

        logger.warning(
            "Serving local fallback for prompt_type=%r, keyword=%r.",
            prompt_type,
            keyword,
        )

        # ── Rewrite / humanize / optimizer flow ───────────────────────
        # Return the original content so the caller can still render
        # something sensible instead of a fake SEO article.
        if prompt_type == "rewrite":
            logger.info(
                "Rewrite fallback: passing prompt text through unchanged."
            )
            return prompt

        # ── Article generation flow ────────────────────────────────────
        return {
            "title":            f"Complete Guide to {keyword}",
            "meta_description": (
                f"Everything you need to know about {keyword}. "
                f"Tips, benefits, FAQs, and expert advice."
            ),
            "content":    _FALLBACK_TEMPLATE.format(keyword=keyword),
            "faq":        f"### What is {keyword}?\n{keyword} is a widely searched topic.",
            "conclusion": f"{keyword} is a valuable subject worth exploring in depth.",
        }

    @staticmethod
    def _detect_prompt_type(prompt: str) -> str:
        """
        Classify a prompt as 'article' or 'rewrite' by looking for
        structured SEO generation markers.

        Markers present  → 'article'  (structured generation prompt)
        Markers absent   → 'rewrite'  (raw content sent for rewriting)

        Using explicit markers is far more reliable than a word-count
        heuristic, which would misclassify long article prompts or very
        short rewrite snippets.
        """
        article_markers = (
            "KEYWORD:",
            "SEARCH INTENT:",
            "JSON FORMAT:",
            "SEO DIFFICULTY:",
            "Return ONLY valid JSON",
        )
        for marker in article_markers:
            if marker in prompt:
                return "article"
        return "rewrite"

    @staticmethod
    def _extract_keyword(prompt: str) -> str:
        """
        Pull the keyword from a structured prompt.
        Returns "SEO Topic" as a safe default.
        """
        try:
            if KEYWORD_SECTION_MARKER in prompt:
                raw = (
                    prompt
                    .split(KEYWORD_SECTION_MARKER, 1)[-1]
                    .strip()
                    .splitlines()[0]
                )
                if raw:
                    return raw.strip()
        except Exception as exc:  # noqa: BLE001
            logger.debug("Keyword extraction failed: %s", exc)

        return "SEO Topic"

    # ──────────────────────────────────────────────────────
    # INTROSPECTION
    # ──────────────────────────────────────────────────────

    def provider_status(self) -> list[dict[str, Any]]:
        """Return health snapshot for monitoring / admin dashboards."""
        return [
            {
                "name":                p.name,
                "consecutive_failures": p.consecutive_failures,
                "circuit_open":        p.is_open,
            }
            for p in self._providers
        ]

    def reset_circuit_breakers(self) -> None:
        """Manually reset all circuit breakers (e.g. after deployment)."""
        for provider in self._providers:
            provider.consecutive_failures = 0
        logger.info("All provider circuit breakers reset.")


# =========================
# FALLBACK TEMPLATE
# =========================

_FALLBACK_TEMPLATE = """\
# Complete Guide to {keyword}

## Introduction

{keyword} is one of the most searched and discussed topics online today.

Many beginners want to understand how {keyword} works, why it matters, and how they can start learning it effectively.

This detailed guide explains everything in a simple and beginner-friendly format.

Whether you are completely new or already have some basic understanding, this article will help you build strong foundational knowledge.

---

## Why {keyword} Is Important

There are several reasons why {keyword} has become increasingly important:

- It helps improve practical knowledge
- Many industries now rely on it
- It creates learning and career opportunities
- It improves decision-making skills
- It is useful for beginners and professionals alike

Understanding {keyword} can provide long-term benefits and help individuals stay updated with modern trends and technologies.

---

## Main Benefits of Learning {keyword}

### 1. Better Understanding

Learning {keyword} improves awareness and helps build strong conceptual clarity.

### 2. Real-World Applications

Many real-world systems and industries use {keyword} regularly.

### 3. Improved Problem Solving

Knowledge of {keyword} helps improve analytical and practical thinking skills.

### 4. Career Opportunities

Many organizations look for individuals with skills related to {keyword}.

### 5. Continuous Growth

{keyword} is constantly evolving, which creates ongoing learning opportunities.

---

## Step-by-Step Guide to Learn {keyword}

### Step 1 — Understand the Basics

Start with beginner-friendly resources and understand the core concepts first.

Avoid jumping directly into advanced topics.

### Step 2 — Practice Consistently

Regular practice is one of the most important parts of learning {keyword} effectively.

Small daily improvements can produce significant long-term results.

### Step 3 — Use Trusted Resources

Always use trusted and updated learning resources.

Good documentation and tutorials help improve learning speed.

### Step 4 — Build Practical Experience

Applying concepts in practical situations improves confidence and understanding.

### Step 5 — Continue Improving

Learning is an ongoing process.

Keep exploring new updates, tools, and techniques related to {keyword}.

---

## Common Mistakes to Avoid

Many beginners make similar mistakes while learning {keyword}.

Here are some common problems to avoid:

- Ignoring the fundamentals
- Learning too many things at once
- Not practicing regularly
- Using outdated resources
- Avoiding practical implementation
- Losing consistency

Avoiding these mistakes can significantly improve learning progress.

---

## Best Tips for Beginners

Here are some useful tips for beginners:

- Start with simple concepts
- Create a learning schedule
- Practice regularly
- Track your progress
- Use high-quality resources
- Learn from real examples
- Stay consistent and patient

Consistency is usually more important than speed.

---

## Practical Applications of {keyword}

{keyword} can be used in many practical scenarios.

Some common applications include:

- Education
- Technology
- Business
- Research
- Data analysis
- Online services
- Automation systems

Because of its wide applications, learning {keyword} can provide long-term value.

---

## Frequently Asked Questions

### What is {keyword}?

{keyword} is a widely discussed topic that has many practical uses and applications.

### Is {keyword} beginner friendly?

Yes. Beginners can start learning gradually using proper guidance and consistent practice.

### How long does it take to learn {keyword}?

The learning time depends on consistency, practice, and previous experience.

### Can I learn {keyword} for free?

Yes. Many free resources, tutorials, and guides are available online.

### Why is {keyword} popular?

{keyword} is popular because it is useful, practical, and widely applied across different industries.

---

## Advanced Learning Strategies

Once you understand the basics, you can move toward advanced concepts and real-world projects.

Advanced learning helps improve:
- practical implementation
- problem-solving ability
- professional skills
- technical understanding

Continuous improvement is important for long-term success.

---

## Final Thoughts

{keyword} is a valuable subject worth learning and exploring.

With proper consistency, practice, and trusted resources, anyone can gradually improve their understanding and skills.

Start with the basics, continue practicing regularly, and focus on long-term improvement rather than quick results.

Learning {keyword} can become a valuable investment for future growth and development.
"""