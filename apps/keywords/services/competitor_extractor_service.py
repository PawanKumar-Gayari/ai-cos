"""
Enterprise Competitor Extractor Service v4
==========================================

Production-grade SEO competitor intelligence engine.

Features:
---------
✓ Redis cache support
✓ Parallel extraction
✓ Session pooling
✓ Trafilatura fallback parser
✓ Reduced CPU usage
✓ Low-latency networking
✓ Multi-user scalability
✓ Production-safe architecture
✓ SEO semantic extraction
✓ Fail-fast crawling
"""

from __future__ import annotations

import json
import logging
import re

from collections import Counter
from concurrent.futures import (
    ThreadPoolExecutor,
)
from urllib.parse import urlparse

import requests
import trafilatura

from bs4 import BeautifulSoup
from django.core.cache import cache


logger = logging.getLogger(__name__)

# =========================================================
# GLOBAL SESSION POOL
# =========================================================

SESSION = requests.Session()


class CompetitorExtractorService:

    """
    Production-grade competitor intelligence service.
    """

    REQUEST_TIMEOUT = (2, 3)

    MAX_URLS = 3

    MAX_HEADINGS = 50

    MAX_KEYWORDS = 20

    MAX_LIST_ITEMS = 50

    MAX_CONTENT_PHRASES = 100

    MAX_HTML_SIZE = 500000

    MAX_CONTENT_LENGTH = 15000

    MIN_KEYWORD_LENGTH = 5

    MIN_PHRASE_WORDS = 2

    CACHE_TIMEOUT = (
        60 * 60 * 12
    )

    USER_AGENT = (
        "Mozilla/5.0 "
        "(Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 "
        "(KHTML, like Gecko) "
        "Chrome/137.0 Safari/537.36"
    )

    BLOCKED_DOMAINS = {
        "youtube.com",
        "facebook.com",
        "instagram.com",
        "twitter.com",
        "x.com",
        "linkedin.com",
        "pinterest.com",
    }

    BLOCKED_EXTENSIONS = {
        ".pdf",
        ".jpg",
        ".jpeg",
        ".png",
        ".gif",
        ".svg",
        ".zip",
        ".rar",
    }

    NOISE_PHRASES = {
        "opens in new window",
        "download pdf",
        "view pdf",
        "save save",
        "download now",
        "click here",
        "read more",
        "show more",
        "load more",
        "sign in",
        "log in",
        "register now",
        "this document",
        "uploaded by",
        "share this",
        "copied successfully",
        "free trial",
        "buy now",
        "limited offer",
        "undefined",
        "null null",
    }

    WEAK_TERMS = {
        "document",
        "window",
        "click",
        "share",
        "upload",
        "download",
        "save",
        "login",
        "signup",
    }

    VALID_SEO_TERMS = {
        "recruitment",
        "vacancy",
        "salary",
        "notification",
        "apply",
        "application",
        "syllabus",
        "result",
        "cutoff",
        "exam",
        "answer key",
        "admit card",
        "guide",
        "tutorial",
        "tips",
        "best",
        "top",
        "review",
        "pdf",
        "course",
        "college",
        "university",
    }

    # =====================================================
    # CLEAN TEXT
    # =====================================================

    @classmethod
    def clean_text(
        cls,
        text,
    ) -> str:

        if not text:
            return ""

        text = str(text)

        text = re.sub(
            r"[^\w\s\u0900-\u097F]",
            " ",
            text,
        )

        text = re.sub(
            r"\s+",
            " ",
            text,
        )

        return text.strip()

    # =====================================================
    # NORMALIZE
    # =====================================================

    @classmethod
    def normalize(
        cls,
        text,
    ) -> str:

        return cls.clean_text(
            text
        ).lower()

    # =====================================================
    # VALID URL
    # =====================================================

    @classmethod
    def valid_url(
        cls,
        url,
    ) -> bool:

        if not url:
            return False

        url = str(url).lower()

        parsed = urlparse(url)

        domain = parsed.netloc

        for blocked in cls.BLOCKED_DOMAINS:

            if blocked in domain:
                return False

        for ext in cls.BLOCKED_EXTENSIONS:

            if url.endswith(ext):
                return False

        return True

    # =====================================================
    # FETCH HTML
    # =====================================================

    @classmethod
    def fetch_html(
        cls,
        url,
    ) -> str:

        try:

            response = SESSION.get(

                url,

                headers={
                    "User-Agent":
                    cls.USER_AGENT,
                },

                timeout=cls.REQUEST_TIMEOUT,
            )

            response.raise_for_status()

            return response.text[
                :cls.MAX_HTML_SIZE
            ]

        except Exception:

            logger.warning(
                "Competitor fetch failed | url=%s",
                url,
            )

            return ""

    # =====================================================
    # MAIN CONTENT EXTRACTION
    # =====================================================

    @classmethod
    def extract_main_content(
        cls,
        html,
    ) -> str:

        try:

            html = html[
                :cls.MAX_HTML_SIZE
            ]

            try:

                extracted = trafilatura.extract(

                    html,

                    include_links=False,
                    include_images=False,
                    include_tables=False,

                    favor_precision=True,
                    deduplicate=True,

                    output_format="txt",
                )

            except Exception:

                logger.warning(
                    "Trafilatura failed, using fallback parser"
                )

                extracted = ""

            # =========================================
            # FALLBACK PARSER
            # =========================================

            if not extracted:

                soup = BeautifulSoup(

                    html[:100000],

                    "lxml",
                )

                extracted = soup.get_text(

                    " ",

                    strip=True,
                )

            return cls.clean_text(
                extracted
            )[
                :cls.MAX_CONTENT_LENGTH
            ]

        except Exception:

            logger.warning(
                "Main content extraction failed"
            )

            return ""

    # =====================================================
    # NOISE FILTER
    # =====================================================

    @classmethod
    def is_noise(
        cls,
        text,
    ) -> bool:

        if not text:
            return True

        normalized = cls.normalize(
            text
        )

        if len(normalized) < 5:
            return True

        if normalized in cls.NOISE_PHRASES:
            return True

        for phrase in cls.NOISE_PHRASES:

            if phrase in normalized:
                return True

        words = normalized.split()

        weak_count = sum(
            1
            for w in words
            if w in cls.WEAK_TERMS
        )

        if words:

            weak_ratio = (
                weak_count / len(words)
            )

            if weak_ratio >= 0.6:
                return True

        return False

    # =====================================================
    # VALID SEO PHRASE
    # =====================================================

    @classmethod
    def is_valid_seo_phrase(
        cls,
        phrase,
    ) -> bool:

        if not phrase:
            return False

        phrase = cls.normalize(
            phrase
        )

        if cls.is_noise(
            phrase
        ):
            return False

        words = phrase.split()

        if (
            len(words)
            < cls.MIN_PHRASE_WORDS
        ):
            return False

        if len(set(words)) < (
            len(words) * 0.5
        ):
            return False

        if any(
            term in phrase
            for term in (
                cls.VALID_SEO_TERMS
            )
        ):
            return True

        return len(words) >= 3

    # =====================================================
    # HEADINGS
    # =====================================================

    @classmethod
    def extract_headings(
        cls,
        soup,
    ) -> list[str]:

        headings = []

        for tag in ["h1", "h2", "h3"]:

            for item in soup.find_all(tag):

                text = cls.clean_text(
                    item.get_text()
                )

                if cls.is_noise(text):
                    continue

                if len(text) < 5:
                    continue

                headings.append(text)

        return headings[
            :cls.MAX_HEADINGS
        ]

    # =====================================================
    # FAQ EXTRACTION
    # =====================================================

    @classmethod
    def extract_faq(
        cls,
        soup,
    ) -> list[str]:

        questions = []

        scripts = soup.find_all(

            "script",

            type="application/ld+json",
        )

        for script in scripts:

            try:

                if not script.string:
                    continue

                data = json.loads(
                    script.string
                )

                datasets = (
                    data
                    if isinstance(data, list)
                    else [data]
                )

                for entry in datasets:

                    if not isinstance(
                        entry,
                        dict,
                    ):
                        continue

                    if (
                        entry.get("@type")
                        != "FAQPage"
                    ):
                        continue

                    entities = entry.get(
                        "mainEntity",
                        [],
                    )

                    for item in entities:

                        question = (
                            cls.clean_text(
                                item.get(
                                    "name",
                                    ""
                                )
                            )
                        )

                        if cls.is_noise(
                            question
                        ):
                            continue

                        if len(question) > 5:

                            questions.append(
                                question
                            )

            except Exception:
                continue

        return questions

    # =====================================================
    # LIST EXTRACTION
    # =====================================================

    @classmethod
    def extract_lists(
        cls,
        soup,
    ) -> list[str]:

        items = []

        for ul in soup.find_all(
            ["ul", "ol"]
        ):

            for li in ul.find_all("li"):

                text = cls.clean_text(
                    li.get_text()
                )

                if cls.is_noise(text):
                    continue

                if len(text) < 5:
                    continue

                items.append(text)

        return items[
            :cls.MAX_LIST_ITEMS
        ]

    # =====================================================
    # SEMANTIC KEYWORDS
    # =====================================================

    @classmethod
    def semantic_keywords(
        cls,
        phrases,
    ) -> list[str]:

        if not phrases:
            return []

        counter = Counter()

        for phrase in phrases:

            normalized = cls.normalize(
                phrase
            )

            if cls.is_noise(
                normalized
            ):
                continue

            words = normalized.split()

            for n in range(2, 4):

                for i in range(
                    len(words)
                    - n + 1
                ):

                    keyword = " ".join(
                        words[
                            i:i + n
                        ]
                    )

                    if (
                        len(keyword)
                        < cls.MIN_KEYWORD_LENGTH
                    ):
                        continue

                    if not (
                        cls.is_valid_seo_phrase(
                            keyword
                        )
                    ):
                        continue

                    counter[keyword] += 1

        results = []

        seen = set()

        for keyword, count in (
            counter.most_common(
                cls.MAX_KEYWORDS * 2
            )
        ):

            if count < 2:
                continue

            if keyword in seen:
                continue

            seen.add(keyword)

            results.append(
                keyword
            )

            if (
                len(results)
                >= cls.MAX_KEYWORDS
            ):
                break

        return results

    # =====================================================
    # EXTRACT URL
    # =====================================================

    @classmethod
    def extract_url(
        cls,
        url,
    ) -> dict:

        cache_key = (
            f"competitor_extract:{url}"
        )

        cached = cache.get(
            cache_key
        )

        if cached:

            logger.info(
                "Competitor cache hit | url=%s",
                url,
            )

            return cached

        if not cls.valid_url(
            url
        ):
            return {}

        html = cls.fetch_html(
            url
        )

        if not html:
            return {}

        soup = BeautifulSoup(

            html[:300000],

            "lxml",
        )

        main_content = (
            cls.extract_main_content(
                html
            )
        )

        headings = (
            cls.extract_headings(
                soup
            )
        )

        faq = cls.extract_faq(
            soup
        )

        lists = cls.extract_lists(
            soup
        )

        content_phrases = []

        for line in (
            main_content.split("\n")
        ):

            if len(content_phrases) >= (
                cls.MAX_CONTENT_PHRASES
            ):
                break

            line = cls.clean_text(
                line
            )

            if cls.is_noise(
                line
            ):
                continue

            if len(line.split()) >= 3:

                content_phrases.append(
                    line
                )

        combined = (
            headings
            + faq
            + lists
            + content_phrases
        )

        semantic_keywords = (
            cls.semantic_keywords(
                combined
            )
        )

        result = {

            "url":
            url,

            "headings":
            headings,

            "faq":
            faq,

            "lists":
            lists,

            "semantic_keywords":
            semantic_keywords,

            "content_length":
            len(main_content),

            "content_preview":
            main_content[:500],
        }

        cache.set(

            cache_key,

            result,

            timeout=cls.CACHE_TIMEOUT,
        )

        logger.info(
            "Competitor extraction complete | url=%s",
            url,
        )

        return result

    # =====================================================
    # EXTRACT MULTIPLE URLS
    # =====================================================

    @classmethod
    def extract_urls(
        cls,
        urls,
    ) -> list[dict]:

        results = []

        seen_domains = set()

        filtered_urls = []

        urls = urls[
            :cls.MAX_URLS
        ]

        # =============================================
        # REMOVE DUPLICATE DOMAINS
        # =============================================

        for url in urls:

            try:

                if not cls.valid_url(
                    url
                ):
                    continue

                domain = (
                    urlparse(url)
                    .netloc
                )

                if domain in seen_domains:
                    continue

                seen_domains.add(
                    domain
                )

                filtered_urls.append(
                    url
                )

            except Exception:
                continue

        # =============================================
        # PARALLEL EXTRACTION
        # =============================================

        with ThreadPoolExecutor(

            max_workers=3

        ) as executor:

            futures = [

                executor.submit(

                    cls.extract_url,

                    url,
                )

                for url in filtered_urls
            ]

            for future in futures:

                try:

                    data = (
                        future.result()
                    )

                    if data:

                        results.append(
                            data
                        )

                except Exception:

                    logger.warning(
                        "Parallel competitor extraction failed"
                    )

        return results