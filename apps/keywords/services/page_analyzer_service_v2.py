"""
Production Page Analyzer Service v3
----------------------------------

Advanced SEO competitor analyzer.

Features:
- main content extraction
- sidebar/footer cleanup
- semantic heading extraction
- FAQ detection
- cleaner keyword extraction
- Hindi-safe processing
- blocked-site-safe scraping
- cloudscraper fallback
- OCI optimized
"""

from __future__ import annotations

import logging
import re

import requests
import cloudscraper

from bs4 import BeautifulSoup


logger = logging.getLogger(__name__)


class PageAnalyzerService:

    TIMEOUT = 8

    MAX_HEADINGS = 20

    MAX_FAQS = 10

    USER_AGENT = (
        "Mozilla/5.0 "
        "(Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 "
        "(KHTML, like Gecko) "
        "Chrome/137.0 Safari/537.36"
    )

    FAQ_PATTERNS = [
        "what",
        "why",
        "how",
        "when",
        "where",
        "can",
        "is",
        "does",
        "should",
        "which",
    ]

    GARBAGE_PHRASES = [

        "you may also like",
        "related posts",
        "trending now",
        "click here",
        "read more",
        "advertisement",
        "follow us",
        "popular posts",
        "latest updates",
    ]

    def __init__(self):

        self.scraper = (
            cloudscraper.create_scraper()
        )

    # =============================================
    # HEADERS
    # =============================================

    @classmethod
    def get_headers(
        cls,
    ) -> dict[str, str]:

        return {

            "User-Agent":
            cls.USER_AGENT,

            "Accept":
            "text/html,application/xhtml+xml",

            "Accept-Language":
            "en-US,en;q=0.9",

            "Connection":
            "keep-alive",
        }

    # =============================================
    # CLEAN TEXT
    # =============================================

    @staticmethod
    def clean_text(
        text: str,
    ) -> str:

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

    # =============================================
    # UNIQUE LIST
    # =============================================

    @staticmethod
    def unique_list(
        values: list[str],
    ) -> list[str]:

        seen = set()

        unique = []

        for item in values:

            item = str(item).strip()

            if not item:
                continue

            if item in seen:
                continue

            seen.add(item)

            unique.append(item)

        return unique

    # =============================================
    # REMOVE JUNK HTML
    # =============================================

    def remove_junk_html(
        self,
        soup: BeautifulSoup,
    ) -> None:

        for tag in soup([
            "script",
            "style",
            "noscript",
            "nav",
            "footer",
            "aside",
            "form",
        ]):

            tag.decompose()

        junk_selectors = [

            ".sidebar",
            ".related-posts",
            ".trending",
            ".widget",
            ".ads",
            ".comments",
            ".footer",
            ".navigation",
            ".menu",
            ".recommended",
            ".popular-posts",
            ".share-buttons",
            ".social-share",
        ]

        for selector in junk_selectors:

            for element in soup.select(
                selector
            ):

                element.decompose()

    # =============================================
    # MAIN CONTENT
    # =============================================

    def extract_main_content(
        self,
        soup: BeautifulSoup,
    ):

        main_content = soup.find(
            "article"
        )

        if not main_content:

            main_content = soup.find(
                "main"
            )

        if not main_content:

            main_content = soup.body

        return main_content

    # =============================================
    # HEADINGS
    # =============================================

    def extract_headings(
        self,
        soup: BeautifulSoup,
    ) -> list[str]:

        headings = []

        for heading in soup.find_all([
            "h2",
            "h3",
        ]):

            text = self.clean_text(
                heading.get_text()
            )

            if not text:
                continue

            if len(text.split()) < 2:
                continue

            headings.append(text)

        headings = self.unique_list(
            headings
        )

        return headings[
            :self.MAX_HEADINGS
        ]

    # =============================================
    # H1
    # =============================================

    def extract_h1_tags(
        self,
        soup: BeautifulSoup,
    ) -> list[str]:

        h1_tags = []

        for tag in soup.find_all(
            "h1"
        ):

            text = self.clean_text(
                tag.get_text()
            )

            if not text:
                continue

            h1_tags.append(text)

        return self.unique_list(
            h1_tags
        )

    # =============================================
    # FAQS
    # =============================================

    def extract_faqs(
        self,
        headings: list[str],
    ) -> list[str]:

        faqs = []

        for heading in headings:

            lower = heading.lower()

            if any(

                lower.startswith(
                    pattern
                )

                for pattern in
                self.FAQ_PATTERNS
            ):

                faqs.append(
                    heading
                )

        faqs = self.unique_list(
            faqs
        )

        return faqs[
            :self.MAX_FAQS
        ]

    # =============================================
    # META DESCRIPTION
    # =============================================

    def extract_meta_description(
        self,
        soup: BeautifulSoup,
    ) -> str:

        meta_tag = soup.find(

            "meta",

            attrs={
                "name":
                "description"
            },
        )

        if not meta_tag:
            return ""

        return self.clean_text(

            meta_tag.get(
                "content",
                "",
            )
        )

    # =============================================
    # WORD COUNT
    # =============================================

    def calculate_word_count(
        self,
        soup: BeautifulSoup,
    ) -> int:

        body_text = soup.get_text(
            separator=" ",
            strip=True,
        )

        body_text = self.clean_text(
            body_text
        )

        return len(
            body_text.split()
        )

    # =============================================
    # ANALYZE
    # =============================================

    def analyze(
        self,
        url: str,
    ) -> dict:

        logger.info(
            f"Page analysis started: {url}"
        )

        blocked_response = {

            "url": url,

            "title": "",

            "meta_description": "",

            "h1_tags": [],

            "headings": [],

            "faq_questions": [],

            "word_count": 0,

            "blocked": True,
        }

        try:

            # =====================================
            # PRIMARY REQUEST
            # =====================================

            try:

                response = requests.get(

                    url,

                    headers=self.get_headers(),

                    timeout=self.TIMEOUT,
                )

                # =================================
                # BLOCKED
                # =================================

                if response.status_code in [
                    403,
                    429,
                ]:

                    logger.warning(
                        f"Requests blocked: "
                        f"{url}"
                    )

                    response = (
                        self.scraper.get(

                            url,

                            headers=self.get_headers(),

                            timeout=self.TIMEOUT,
                        )
                    )

                    if response.status_code in [
                        403,
                        429,
                    ]:

                        logger.warning(
                            f"Cloudscraper blocked: "
                            f"{url}"
                        )

                        return blocked_response

            except Exception as error:

                logger.warning(
                    f"Primary request failed: "
                    f"{error}"
                )

                try:

                    response = (
                        self.scraper.get(

                            url,

                            headers=self.get_headers(),

                            timeout=self.TIMEOUT,
                        )
                    )

                    if response.status_code in [
                        403,
                        429,
                    ]:

                        logger.warning(
                            f"Cloudscraper blocked: "
                            f"{url}"
                        )

                        return blocked_response

                except Exception as fallback_error:

                    logger.warning(
                        f"Fallback failed: "
                        f"{fallback_error}"
                    )

                    return blocked_response

            # =====================================
            # PARSER
            # =====================================

            soup = BeautifulSoup(
                response.text,
                "lxml",
            )

            # =====================================
            # REMOVE JUNK HTML
            # =====================================

            self.remove_junk_html(
                soup
            )

            # =====================================
            # MAIN CONTENT
            # =====================================

            main_content = (
                self.extract_main_content(
                    soup
                )
            )

            # =====================================
            # TITLE
            # =====================================

            title = ""

            if soup.title:

                title = self.clean_text(
                    soup.title.text
                )

            # =====================================
            # META
            # =====================================

            meta_description = (
                self.extract_meta_description(
                    soup
                )
            )

            # =====================================
            # H1
            # =====================================

            h1_tags = (
                self.extract_h1_tags(
                    main_content
                )
            )

            # =====================================
            # HEADINGS
            # =====================================

            headings = (
                self.extract_headings(
                    main_content
                )
            )

            # =====================================
            # FAQS
            # =====================================

            faqs = (
                self.extract_faqs(
                    headings
                )
            )

            # =====================================
            # WORD COUNT
            # =====================================

            word_count = (
                self.calculate_word_count(
                    main_content
                )
            )

            logger.info(
                "Page analysis completed."
            )

            return {

                "url":
                url,

                "title":
                title,

                "meta_description":
                meta_description,

                "h1_tags":
                h1_tags,

                "headings":
                headings,

                "faq_questions":
                faqs,

                "word_count":
                word_count,

                "blocked":
                False,
            }

        except Exception as error:

            logger.exception(
                f"Page analysis failed: "
                f"{str(error)}"
            )

            return {

                "url":
                url,

                "error":
                str(error),

                "blocked":
                True,
            }