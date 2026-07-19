"""
SERP content parser.
"""

import requests
import trafilatura

from urllib.parse import urlparse

from bs4 import BeautifulSoup

from utils.logger import (
    competitor_logger,
)

from utils.text_cleaner import (
    TextCleaner,
)


class SERPParser:

    DEFAULT_TIMEOUT = 8

    MIN_WORD_COUNT = 300

    HEADING_TAGS = [

        "h1",

        "h2",

        "h3",
    ]

    BLOCKED_DOMAINS = [

        "reddit.com",

        "youtube.com",

        "amazon.",

        "bestbuy.",

        "facebook.com",

        "instagram.com",

        "twitter.com",

        "x.com",
    ]

    DEFAULT_HEADERS = {

        "User-Agent": (

            "Mozilla/5.0 "
            "(Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 "
            "(KHTML, like Gecko) "
            "Chrome/136.0.0.0 "
            "Safari/537.36"
        ),

        "Accept": (

            "text/html,"
            "application/xhtml+xml,"
            "application/xml;q=0.9,"
            "image/avif,"
            "image/webp,*/*;q=0.8"
        ),

        "Accept-Language": (
            "en-US,en;q=0.9"
        ),

        "Connection": "keep-alive",
    }

    # ==================================================
    # SAFE CLEAN
    # ==================================================

    def safe_clean(
        self,
        value,
    ):

        if not value:

            return ""

        return TextCleaner.clean(
            str(value)
        )

    # ==================================================
    # DOMAIN FILTER
    # ==================================================

    def should_skip_domain(
        self,
        url,
    ):

        """
        Skip noisy or blocked domains.
        """

        parsed = urlparse(url)

        domain = (
            parsed.netloc.lower()
        )

        for blocked in (
            self.BLOCKED_DOMAINS
        ):

            if blocked in domain:

                competitor_logger.warning(

                    f"[DOMAIN SKIPPED] "
                    f"{domain}"
                )

                return True

        return False

    # ==================================================
    # EXTRACT HEADINGS
    # ==================================================

    def extract_headings(
        self,
        soup,
    ):

        headings = []

        seen = set()

        for tag in self.HEADING_TAGS:

            elements = soup.find_all(tag)

            for element in elements:

                text = self.safe_clean(
                    element.get_text(
                        separator=" ",
                        strip=True,
                    )
                )

                if not text:

                    continue

                normalized = (
                    text.lower()
                )

                if normalized in seen:

                    continue

                seen.add(
                    normalized
                )

                headings.append(
                    text
                )

        return headings

    # ==================================================
    # WORD COUNT
    # ==================================================

    def calculate_word_count(
        self,
        text,
    ):

        cleaned = self.safe_clean(
            text
        )

        return len(
            cleaned.split()
        )

    # ==================================================
    # FETCH HTML
    # ==================================================

    def fetch_html(
        self,
        url,
    ):

        """
        Fetch page HTML safely.
        """

        response = requests.get(

            url,

            timeout=(
                self.DEFAULT_TIMEOUT
            ),

            headers=(
                self.DEFAULT_HEADERS
            ),

            allow_redirects=True,
        )

        response.raise_for_status()

        return response.text

    # ==================================================
    # PRIMARY EXTRACTION
    # ==================================================

    def extract_main_content(
        self,
        html,
    ):

        """
        Extract clean article content.
        """

        extracted = (
            trafilatura.extract(

                html,

                include_comments=False,

                include_tables=True,

                no_fallback=False,
            )
        )

        if not extracted:

            return ""

        return extracted

    # ==================================================
    # FALLBACK PARSER
    # ==================================================

    def fallback_extract(
        self,
        html,
    ):

        """
        BeautifulSoup fallback extraction.
        """

        soup = BeautifulSoup(

            html,

            "lxml",
        )

        return soup.get_text(
            separator=" ",
            strip=True,
        )

    # ==================================================
    # PARSE URL
    # ==================================================

    def parse_url(
        self,
        url,
    ):

        competitor_logger.info(

            f"[PARSER START] "
            f"URL={url}"
        )

        try:

            # ==========================================
            # DOMAIN FILTER
            # ==========================================

            if self.should_skip_domain(
                url
            ):

                return {

                    "headings": [],

                    "word_count": 0,
                }

            # ==========================================
            # FETCH HTML
            # ==========================================

            html = self.fetch_html(
                url
            )

            # ==========================================
            # PRIMARY EXTRACTION
            # ==========================================

            extracted_text = (
                self.extract_main_content(
                    html
                )
            )

            # ==========================================
            # FALLBACK EXTRACTION
            # ==========================================

            if not extracted_text:

                competitor_logger.warning(

                    "[TRAFILATURA FAILED] "
                    "Using BeautifulSoup fallback"
                )

                extracted_text = (
                    self.fallback_extract(
                        html
                    )
                )

            # ==========================================
            # WORD COUNT
            # ==========================================

            word_count = (
                self.calculate_word_count(
                    extracted_text
                )
            )

            # ==========================================
            # LOW QUALITY FILTER
            # ==========================================

            if word_count < (
                self.MIN_WORD_COUNT
            ):

                competitor_logger.warning(

                    f"[LOW QUALITY CONTENT] "
                    f"WORDS={word_count}"
                )

                return {

                    "headings": [],

                    "word_count": 0,
                }

            # ==========================================
            # HEADINGS
            # ==========================================

            soup = BeautifulSoup(

                html,

                "lxml",
            )

            headings = (
                self.extract_headings(
                    soup
                )
            )

            competitor_logger.info(

                f"[PARSER SUCCESS] "
                f"HEADINGS={len(headings)} "
                f"WORDS={word_count}"
            )

            return {

                "headings": headings,

                "word_count": (
                    word_count
                ),
            }

        except Exception as error:

            competitor_logger.exception(

                f"[PARSER FAILED] "
                f"URL={url} | "
                f"ERROR={str(error)}"
            )

            return {

                "headings": [],

                "word_count": 0,
            }