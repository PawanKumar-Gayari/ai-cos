"""
Local rewrite engine — God-level edition.

What's new vs v1:
- AI-powered fact verification layer (dates, salaries, exam info, stats, etc.)
- Fact extractor with typed FactClaim dataclass
- Verification result attached to each claim (verified / unverified / flagged)
- Rewrite output annotated with [⚠ Unverified] inline warnings
- Duplicate fact protection (same placeholder never reused)
- Shared LocalHumanizer — no duplicate phrase removal
- Fully typed, structured logging, zero silent failures
"""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Any

from apps.rewriter.local_humanizer import LocalHumanizer

logger = logging.getLogger(__name__)


# =========================
# CONSTANTS
# =========================

LONG_PARAGRAPH_WORD_LIMIT = 120
FACT_PLACEHOLDER_PREFIX   = "__FACT_"
FACT_PLACEHOLDER_SUFFIX   = "__"


# =========================
# FACT TYPES
# =========================

class FactType(str, Enum):
    DATE        = "date"
    EXAM_DATE   = "exam_date"
    SALARY      = "salary"
    PERCENTAGE  = "percentage"
    STATISTIC   = "statistic"
    URL         = "url"
    EMAIL       = "email"
    YEAR        = "year"
    LARGE_NUM   = "large_number"
    MONEY       = "money"
    DEADLINE    = "deadline"
    VERSION     = "version"


# =========================
# VERIFICATION SOURCE
# =========================

@dataclass
class VerificationSource:
    """
    Tracks WHERE a fact was verified from and HOW confident we are.

    Confidence tiers:
      1.0  — official .gov.in / .nic.in / .ac.in source (web-scraped)
      0.8  — reputed news source (ndtv, thehindu, indianexpress, etc.)
      0.6  — AI knowledge base (LLM — may be outdated)
      0.0  — unverified / unknown
    """
    url:        str   = ""     # source URL if available
    title:      str   = ""     # page/document title
    confidence: float = 0.0    # 0.0 – 1.0
    method:     str   = ""     # "web_official" | "web_news" | "ai_knowledge" | "none"

    @property
    def is_official(self) -> bool:
        official_tlds = (".gov.in", ".nic.in", ".ac.in", ".edu.in", ".gov")
        return any(tld in self.url for tld in official_tlds)

    @property
    def label(self) -> str:
        if self.confidence >= 1.0:  return "✅ Official"
        if self.confidence >= 0.8:  return "🟡 Reputed"
        if self.confidence >= 0.6:  return "🔵 AI Knowledge"
        return                             "❓ Unverified"


# =========================
# FACT CLAIM
# =========================

# How many years before a time-sensitive fact is considered stale
_STALE_YEAR_THRESHOLD = 1

@dataclass
class FactClaim:
    """A single verifiable fact extracted from content."""

    raw:         str                    # original text matched
    fact_type:   FactType
    placeholder: str                    # token used in protected content
    start:       int        = 0         # char offset in original (span tracking)
    end:         int        = 0         # char offset in original (span tracking)
    context:     str        = ""        # surrounding sentence for AI context
    verified:    bool | None = None     # None = not yet checked
    flagged:     bool        = False    # True = AI says this looks wrong
    note:        str         = ""       # AI explanation if flagged
    source:      VerificationSource = field(
                                 default_factory=VerificationSource
                             )
    freshness:   str        = "unknown" # "fresh" | "stale" | "unknown"

    def mark_stale(self, current_year: int) -> None:
        """
        If the claim contains a year older than _STALE_YEAR_THRESHOLD,
        mark it stale — useful for exam dates, salary bands, versions.
        """
        import re as _re
        year_match = _re.search(r"\b(19|20)(\d{2})\b", self.raw)
        if year_match:
            fact_year = int(year_match.group())
            if current_year - fact_year > _STALE_YEAR_THRESHOLD:
                self.freshness = "stale"
                return
        self.freshness = "fresh"


# =========================
# VERIFICATION STATUS
# =========================

@dataclass
class VerificationReport:
    total:        int
    verified:     int
    flagged:      int
    skipped:      int
    stale:        int = 0
    claims:       list[FactClaim] = field(default_factory=list)

    @property
    def has_issues(self) -> bool:
        return self.flagged > 0 or self.stale > 0

    def summary(self) -> str:
        return (
            f"Facts: {self.total} total | "
            f"{self.verified} verified | "
            f"{self.flagged} flagged | "
            f"{self.stale} stale | "
            f"{self.skipped} skipped"
        )


# =========================
# FACT PATTERNS
# =========================

# Each entry: (compiled regex, FactType)
_FACT_PATTERNS: list[tuple[re.Pattern, FactType]] = [
    # URLs
    (re.compile(r"https?://[^\s\]>\"']+"),                                FactType.URL),
    # Emails
    (re.compile(r"\b[\w.+-]+@[\w-]+\.[a-z]{2,}\b", re.IGNORECASE),       FactType.EMAIL),
    # Exam dates (e.g. "UPSC 2024", "JEE Main 2025", "NEET exam date")
    (re.compile(
        r"\b(?:UPSC|IAS|IPS|JEE|NEET|CAT|GATE|SSC|IBPS|RRB|CLAT|AIIMS)"
        r"[\w\s]*(?:exam|date|result|notification|cutoff)[\w\s,]*\d{4}\b",
        re.IGNORECASE,
    ),                                                                     FactType.EXAM_DATE),
    # Deadlines (e.g. "last date: 15 March 2025", "apply by 31 Jan")
    (re.compile(
        r"\b(?:last date|deadline|apply by|closing date|due date)"
        r"[\w\s:,]*\d{1,2}[\s/-]\w+[\s/-]\d{2,4}\b",
        re.IGNORECASE,
    ),                                                                     FactType.DEADLINE),
    # Salary / CTC (e.g. "₹45,000", "$120k", "15 LPA", "CTC of 8 lakhs")
    (re.compile(
        r"(?:₹|Rs\.?|INR|USD|\$)\s?\d[\d,\.]*"
        r"|\b\d+(?:\.\d+)?\s*(?:LPA|lpa|lakhs?|crore|k|K)\b"
        r"|\bCTC\s+of\s+\d[\d,.]*\s*(?:lakhs?|LPA|crore)?\b",
        re.IGNORECASE,
    ),                                                                     FactType.SALARY),
    # Percentages
    (re.compile(r"\b\d+(?:\.\d+)?%"),                                     FactType.PERCENTAGE),
    # Versions (e.g. "Python 3.12", "v2.4.1")
    (re.compile(r"\bv?\d+\.\d+(?:\.\d+)?\b"),                            FactType.VERSION),
    # Standalone years
    (re.compile(r"\b(19|20)\d{2}\b"),                                     FactType.YEAR),
    # Dates (DD/MM/YYYY, DD-MM-YYYY)
    (re.compile(r"\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b"),                  FactType.DATE),
    # Large numbers (3+ digits, not already matched)
    (re.compile(r"\b\d{3,}\b"),                                           FactType.LARGE_NUM),
]


# =========================
# ENGAGEMENT HOOKS
# =========================

_HOOKS: list[str] = [
    "Here's something worth double-checking:",
    "This one detail matters a lot:",
    "Keep this in mind as you continue:",
    "Many people miss this point:",
    "A small detail with big consequences:",
]


# =========================
# LOCAL REWRITER
# =========================

class LocalRewriter:
    """
    Rewrites AI-generated content with:

    1. Fact extraction   — pulls out all verifiable claims
    2. Fact protection   — replaces claims with placeholders
    3. Humanization      — delegates to LocalHumanizer
    4. AI verification   — checks each fact claim via AIRouter
    5. Fact restoration  — puts facts back, flagged ones get ⚠ inline
    6. Cleanup           — whitespace, punctuation, paragraph rhythm
    """

    def __init__(
        self,
        ai_router:    Any | None = None,
        web_searcher: Any | None = None,
    ) -> None:
        """
        Args:
            ai_router:    AIRouter instance — used for AI-knowledge verification.
            web_searcher: Any object with .search(query, max_results) → list[dict].
                          Each result dict: {"url": str, "title": str, "snippet": str}
                          Pass your DuckDuckGo / Google / SerpAPI wrapper here.
                          If None, Tier-1 web verification is skipped gracefully.
        """
        self.humanizer   = LocalHumanizer()
        self.ai_router   = ai_router
        self.web_searcher = web_searcher

    # ──────────────────────────────────────────────────────
    # PUBLIC API
    # ──────────────────────────────────────────────────────

    def rewrite(self, content: str) -> str:
        result, _ = self.rewrite_detailed(content)
        return result

    def rewrite_detailed(
        self,
        content: str,
    ) -> tuple[str, VerificationReport]:
        """
        Full pipeline with verification report.

        Returns:
            (rewritten_content, VerificationReport)
        """
        if not content or not content.strip():
            return "", VerificationReport(total=0, verified=0, flagged=0, skipped=0)

        # Step 1 — extract and protect facts
        protected, claims = self._protect_facts(content)
        logger.info("Extracted %d fact claims.", len(claims))

        # Step 2 — humanize (phrase replacement, sentence splitting, etc.)
        protected = self.humanizer.humanize(protected)

        # Step 3 — paragraph splitting
        protected = self._split_long_paragraphs(protected)

        # Step 4 — engagement hooks (only if none already present)
        protected = self._inject_hook_if_needed(protected)

        # Step 5 — verify facts via AI (if router available)
        report = self._verify_facts(claims, content)

        # Step 6 — restore facts with inline warnings for flagged ones
        restored = self._restore_facts(protected, claims)

        # Step 7 — final cleanup
        restored = self._cleanup(restored)

        logger.info(
            "Rewrite done — facts=%d | verified=%d | flagged=%d",
            report.total,
            report.verified,
            report.flagged,
        )

        return restored, report

    # ──────────────────────────────────────────────────────
    # STEP 1 — FACT PROTECTION  (span-safe, offset-indexed)
    # ──────────────────────────────────────────────────────

    def _protect_facts(
        self,
        content: str,
    ) -> tuple[str, list[FactClaim]]:
        """
        Extract all fact spans using char offsets to prevent overlap.

        Algorithm:
        1. Run every pattern over the ORIGINAL content and collect
           (start, end, raw, fact_type) tuples.
        2. Sort by start offset, then greedily pick non-overlapping spans.
        3. Substitute from right-to-left so earlier offsets stay valid.
        4. Attach surrounding sentence as context for AI verification.
        5. Score temporal freshness (year-bearing facts only).
        """
        import datetime

        current_year = datetime.date.today().year
        sentences    = re.split(r"(?<=[.!?])\s+", content)

        # ── Collect all raw spans ──────────────────────────────────────
        raw_spans: list[tuple[int, int, str, FactType]] = []

        for pattern, fact_type in _FACT_PATTERNS:
            for match in pattern.finditer(content):
                raw_spans.append(
                    (match.start(), match.end(), match.group(), fact_type)
                )

        # ── Sort by start; greedy non-overlap selection ────────────────
        raw_spans.sort(key=lambda x: x[0])
        selected: list[tuple[int, int, str, FactType]] = []
        last_end = -1

        for start, end, raw, fact_type in raw_spans:
            if start >= last_end:           # no overlap with previous span
                selected.append((start, end, raw, fact_type))
                last_end = end
            # else: overlapping → skip (higher-priority pattern already covered it)

        # ── Build claims + substitute right-to-left ───────────────────
        claims:  list[FactClaim] = []
        counter  = len(selected) - 1        # build placeholders in order 0..N

        for idx, (start, end, raw, fact_type) in enumerate(selected):
            placeholder = f"{FACT_PLACEHOLDER_PREFIX}{idx}{FACT_PLACEHOLDER_SUFFIX}"
            context     = next((s for s in sentences if raw in s), "")

            claim = FactClaim(
                raw         = raw,
                fact_type   = fact_type,
                placeholder = placeholder,
                start       = start,
                end         = end,
                context     = context,
            )
            claim.mark_stale(current_year)
            claims.append(claim)

        # Substitute right-to-left (highest offset first) so slices stay valid
        for claim in reversed(claims):
            content = (
                content[: claim.start]
                + claim.placeholder
                + content[claim.end :]
            )

        counter = len(claims)
        logger.debug("Span-safe extraction: %d claims, 0 overlaps.", counter)
        return content, claims

    # ──────────────────────────────────────────────────────
    # STEP 5 — VERIFICATION  (web-first → AI fallback)
    # ──────────────────────────────────────────────────────

    def _verify_facts(
        self,
        claims: list[FactClaim],
        original_content: str,
    ) -> VerificationReport:
        """
        Two-tier verification pipeline:

        Tier 1 — Web search (official .gov.in / reputed news)
            • Only for high-stakes FactTypes: EXAM_DATE, DEADLINE, SALARY
            • Requires self.web_searcher (optional dependency)
            • Confidence ≥ 0.8, with real source URL + title

        Tier 2 — AI knowledge base (for anything not resolved by Tier 1)
            • Batched single call via self.ai_router
            • Confidence = 0.6, source = "ai_knowledge"
            • Explicitly warns: AI may be outdated

        Skipped — URL, EMAIL, LARGE_NUM (not meaningfully verifiable)
        """
        SKIP_TYPES       = {FactType.URL, FactType.EMAIL, FactType.LARGE_NUM}
        WEB_PRIORITY     = {FactType.EXAM_DATE, FactType.DEADLINE, FactType.SALARY}

        verifiable = [c for c in claims if c.fact_type not in SKIP_TYPES]
        skipped    = len(claims) - len(verifiable)

        if not verifiable:
            return self._make_report(claims, skipped)

        # ── Tier 1: Web verification for high-stakes facts ────────────
        unresolved: list[FactClaim] = []

        for claim in verifiable:
            if claim.fact_type in WEB_PRIORITY and self.web_searcher is not None:
                self._web_verify_claim(claim)
            else:
                unresolved.append(claim)

        # Claims partially resolved by web; only send unresolved to AI
        still_unresolved = [
            c for c in verifiable if c.verified is None and not c.flagged
        ]

        # ── Tier 2: AI batch verification for remaining claims ─────────
        if still_unresolved:
            if self.ai_router is not None:
                prompt = self._build_verification_prompt(
                    still_unresolved, original_content
                )
                try:
                    raw_response = self.ai_router.generate_content(prompt)
                    self._parse_verification_response(raw_response, still_unresolved)
                    # Mark AI-verified claims with correct source + confidence
                    for claim in still_unresolved:
                        if claim.verified is True and not claim.source.url:
                            claim.source = VerificationSource(
                                url        = "",
                                title      = "AI Knowledge Base",
                                confidence = 0.6,
                                method     = "ai_knowledge",
                            )
                except Exception as exc:
                    logger.error("AI fact verification failed: %s", exc)
                    for claim in still_unresolved:
                        claim.verified = None
            else:
                logger.warning(
                    "No AI router — %d claims left unverified.", len(still_unresolved)
                )

        return self._make_report(claims, skipped)

    def _web_verify_claim(self, claim: FactClaim) -> None:
        """
        Attempt to verify a single high-stakes claim via web search.

        Priority order:
          1. Official government/exam body domains (.gov.in, .nic.in, nta.ac.in, etc.)
          2. Reputed news outlets (thehindu, ndtv, indianexpress, livemint)

        Sets claim.verified, claim.flagged, claim.note, claim.source in-place.
        """
        OFFICIAL_DOMAINS = (
            ".gov.in", ".nic.in", ".ac.in", ".edu.in",
            "nta.ac.in", "upsc.gov.in", "ssc.nic.in",
            "ibps.in", "railwayrecruitment.in",
        )
        NEWS_DOMAINS = (
            "thehindu.com", "ndtv.com", "indianexpress.com",
            "livemint.com", "timesofindia.indiatimes.com",
        )

        query = f"{claim.raw} {claim.context[:80]} official"

        try:
            results: list[dict] = self.web_searcher.search(query, max_results=5)
        except Exception as exc:
            logger.warning("Web search failed for %r: %s", claim.raw, exc)
            return

        for result in results:
            url   = result.get("url", "")
            title = result.get("title", "")
            snippet = result.get("snippet", "")

            is_official = any(d in url for d in OFFICIAL_DOMAINS)
            is_news     = any(d in url for d in NEWS_DOMAINS)

            if not (is_official or is_news):
                continue

            # Simple heuristic: if the raw fact text appears in the snippet → verified
            if claim.raw.lower() in snippet.lower():
                claim.verified = True
                claim.source   = VerificationSource(
                    url        = url,
                    title      = title,
                    confidence = 1.0 if is_official else 0.8,
                    method     = "web_official" if is_official else "web_news",
                )
                logger.info(
                    "Web-verified [%s] %r via %s (conf=%.1f)",
                    claim.fact_type.value, claim.raw,
                    claim.source.method, claim.source.confidence,
                )
                return

            # Snippet exists but fact not found → possible mismatch
            if is_official and snippet:
                claim.flagged = True
                claim.note    = (
                    f"Official source found but fact not confirmed: {title}"
                )
                claim.source  = VerificationSource(
                    url        = url,
                    title      = title,
                    confidence = 0.0,
                    method     = "web_official",
                )
                logger.warning(
                    "Web-flagged [%s] %r — %s",
                    claim.fact_type.value, claim.raw, claim.note,
                )
                return

    @staticmethod
    def _build_verification_prompt(
        claims: list[FactClaim],
        article_content: str,
    ) -> str:
        """
        Build a batched fact-check prompt.

        Explicitly tells the AI:
        - To say UNKNOWN if unsure (reduces hallucinated VERIFIED responses)
        - To flag stale-looking years
        - To include the source it's drawing from, if known
        """
        import datetime
        current_year = datetime.date.today().year

        claims_list = "\n".join(
            f'{i+1}. [{c.fact_type.value.upper()}] "{c.raw}"'
            f'{" 🕐stale-year" if c.freshness == "stale" else ""}'
            f' — context: "{c.context[:120]}"'
            for i, c in enumerate(claims)
        )

        return f"""
You are a strict fact-checking assistant. Current year: {current_year}.

ARTICLE CONTEXT (first 400 chars):
{article_content[:400]}

CLAIMS TO VERIFY:
{claims_list}

RULES:
- VERIFIED  → you are confident this fact is correct based on known data.
- FLAGGED   → fact appears wrong, outdated, or contradicts what you know.
- UNKNOWN   → you cannot confirm either way. DO NOT guess VERIFIED.
- If a claim has a year ≥ 2 years old and is time-sensitive (exam, salary, cutoff),
  mark it FLAGGED with a note like "Data from 2022 — may be outdated by {current_year}."
- Include the source of your knowledge in the note where possible
  (e.g. "As per NTA official schedule...", "Based on 7th Pay Commission data...").
- IMPORTANT: Prefer UNKNOWN over VERIFIED when uncertain.
  A wrong VERIFIED is worse than an honest UNKNOWN.

Return ONLY valid JSON:
{{
  "results": [
    {{"id": 1, "status": "VERIFIED", "note": "Per NTA, NEET 2024 was held on 5 May 2024."}},
    {{"id": 2, "status": "FLAGGED",  "note": "SSC CGL 2023 Tier-1 cutoff was ~145, not 180."}},
    {{"id": 3, "status": "UNKNOWN",  "note": "Cannot confirm this specific salary figure."}}
  ]
}}
""".strip()

    @staticmethod
    def _parse_verification_response(
        response: str | dict | None,
        claims: list[FactClaim],
    ) -> None:
        """Parse AI verification JSON and annotate claims in-place."""
        import json

        if not response:
            return

        try:
            if isinstance(response, str):
                cleaned = re.sub(r"```(?:json)?|```", "", response).strip()
                data    = json.loads(cleaned)
            else:
                data = response

            results: list[dict] = data.get("results", [])

            for entry in results:
                idx    = entry.get("id", 0) - 1   # 1-indexed → 0-indexed
                status = entry.get("status", "UNKNOWN").upper()
                note   = entry.get("note", "")

                if 0 <= idx < len(claims):
                    claim          = claims[idx]
                    claim.note     = note
                    claim.verified = status == "VERIFIED"
                    claim.flagged  = status == "FLAGGED"

        except (json.JSONDecodeError, KeyError, TypeError) as exc:
            logger.warning("Could not parse verification response: %s", exc)

    # ──────────────────────────────────────────────────────
    # STEP 6 — FACT RESTORATION  (with source badges)
    # ──────────────────────────────────────────────────────

    def _restore_facts(
        self,
        content: str,
        claims: list[FactClaim],
    ) -> str:
        """
        Restore placeholders → original text with inline annotations:

        ✅ Official    — web-verified from gov/official domain
        🟡 Reputed     — web-verified from reputed news outlet
        🔵 AI Knowledge — verified by LLM (may be outdated)
        ⚠️ Flagged     — likely wrong, with explanation
        🕐 Stale       — fact contains a year older than threshold
        """
        for claim in claims:
            if claim.flagged:
                note_text = f": {claim.note}" if claim.note else ""
                source_ref = (
                    f" [Source: {claim.source.url}]"
                    if claim.source.url else ""
                )
                restored = (
                    f"~~{claim.raw}~~ "
                    f"⚠️ *Possibly incorrect{note_text}{source_ref}*"
                )
                logger.warning(
                    "Flagged [%s] %r — %s",
                    claim.fact_type.value, claim.raw, claim.note,
                )

            elif claim.freshness == "stale":
                restored = (
                    f"{claim.raw} "
                    f"🕐 *[May be outdated — please verify]*"
                )
                logger.info(
                    "Stale fact [%s]: %r", claim.fact_type.value, claim.raw
                )

            elif claim.verified and claim.source.url:
                badge    = claim.source.label
                restored = f"{claim.raw} {badge}"

            elif claim.verified and claim.source.method == "ai_knowledge":
                restored = f"{claim.raw} 🔵"

            else:
                restored = claim.raw

            content = content.replace(claim.placeholder, restored, 1)

        return content

    # ──────────────────────────────────────────────────────
    # HELPER — BUILD REPORT
    # ──────────────────────────────────────────────────────

    @staticmethod
    def _make_report(
        claims: list[FactClaim],
        skipped: int,
    ) -> VerificationReport:
        return VerificationReport(
            total    = len(claims),
            verified = sum(1 for c in claims if c.verified is True),
            flagged  = sum(1 for c in claims if c.flagged),
            stale    = sum(1 for c in claims if c.freshness == "stale"),
            skipped  = skipped,
            claims   = claims,
        )

    # ──────────────────────────────────────────────────────
    # PIPELINE HELPERS
    # ──────────────────────────────────────────────────────

    @staticmethod
    def _split_long_paragraphs(content: str) -> str:
        """Split paragraphs exceeding LONG_PARAGRAPH_WORD_LIMIT words."""
        paragraphs = content.split("\n\n")
        result: list[str] = []

        for para in paragraphs:
            words = para.split()
            if len(words) > LONG_PARAGRAPH_WORD_LIMIT:
                mid   = len(words) // 2
                left  = " ".join(words[:mid])
                right = " ".join(words[mid:])
                result.append(f"{left}\n\n{right}")
            else:
                result.append(para)

        return "\n\n".join(result)

    @staticmethod
    def _inject_hook_if_needed(content: str) -> str:
        """Prepend an engagement hook if none already present."""
        if any(hook.lower() in content.lower() for hook in _HOOKS):
            return content
        return f"**{_HOOKS[0]}**\n\n{content}"

    @staticmethod
    def _cleanup(content: str) -> str:
        """Final whitespace and punctuation cleanup."""
        content = re.sub(r"\n{3,}", "\n\n", content)     # excess blank lines
        content = re.sub(r" {2,}", " ", content)          # double spaces
        content = re.sub(r"\s+([,.!?])", r"\1", content)  # space before punct
        content = re.sub(r"\.{2,}", ".", content)          # ellipsis collapse
        content = re.sub(r"!{2,}", "!", content)           # repeated !
        return content.strip()