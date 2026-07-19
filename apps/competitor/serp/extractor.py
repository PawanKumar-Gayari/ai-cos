"""
SERP extractor for competitor intelligence engine.
"""

from urllib.parse import (
    urlparse,
)

from apps.competitor.serp.fetcher import (
    SERPFetcher,
)

from apps.competitor.serp.parser import (
    SERPParser,
)

from utils.keyword_normalizer import (
    KeywordNormalizer,
)

from utils.text_cleaner import (
    TextCleaner,
)

from utils.seo_helpers import (
    SEOHelpers,
)

from utils.helpers import (
    Helpers,
)

from utils.logger import (
    competitor_logger,
)


class SERPExtractor:

    MIN_WORD_COUNT = 300

    MAX_RESULTS = 10

    BLOCKED_DOMAINS = [

        "reddit.com",

        "youtube.com",

        "amazon.",

        "flipkart.",

        "bestbuy.",

        "facebook.com",

        "instagram.com",

        "twitter.com",

        "x.com",

        "smartprix.com",
    ]

    BLOCKED_URL_PATTERNS = [

        "/product/",

        "/products/",

        "/shop/",

        "/store/",

        "/buy/",

        "/cart/",

        "/watch",

        "/video/",
    ]

    HIGH_QUALITY_KEYWORDS = [

        "best",

        "guide",

        "review",

        "comparison",

        "tutorial",

        "tips",

        "top",

        "vs",

        "how to",
    ]

    def __init__(
        self
    ):

        self.fetcher = (
            SERPFetcher()
        )

        self.parser = (
            SERPParser()
        )

    # ==================================================
    # CLEAN TITLE
    # ==================================================

    def clean_title(
        self,
        title,
    ):

        return TextCleaner.clean(
            title
        )

    # ==================================================
    # DOMAIN FILTER
    # ==================================================

    def is_blocked_domain(
        self,
        url,
    ):

        parsed = urlparse(url)

        domain = (
            parsed.netloc.lower()
        )

        for blocked in (
            self.BLOCKED_DOMAINS
        ):

            if blocked in domain:

                return True

        return False

    # ==================================================
    # URL PATTERN FILTER
    # ==================================================

    def is_blocked_pattern(
        self,
        url,
    ):

        lowered = url.lower()

        for pattern in (
            self.BLOCKED_URL_PATTERNS
        ):

            if pattern in lowered:

                return True

        return False

    # ==================================================
    # HIGH QUALITY TITLE
    # ==================================================

    def is_high_quality_title(
        self,
        title,
    ):

        lowered = title.lower()

        for keyword in (
            self.HIGH_QUALITY_KEYWORDS
        ):

            if keyword in lowered:

                return True

        return False

    # ==================================================
    # QUALITY FILTER
    # ==================================================

    def is_high_quality_result(
        self,
        result,
    ):

        """
        Determine if SERP result
        is useful for SEO analysis.
        """

        url = result.get(
            "url",
            ""
        )

        title = result.get(
            "title",
            ""
        )

        if not url:

            return False

        # ==========================================
        # BLOCK DOMAINS
        # ==========================================

        if self.is_blocked_domain(
            url
        ):

            competitor_logger.warning(

                f"[FILTERED DOMAIN] "
                f"{url}"
            )

            return False

        # ==========================================
        # BLOCK URL PATTERNS
        # ==========================================

        if self.is_blocked_pattern(
            url
        ):

            competitor_logger.warning(

                f"[FILTERED URL PATTERN] "
                f"{url}"
            )

            return False

        # ==========================================
        # TITLE QUALITY
        # ==========================================

        if not self.is_high_quality_title(
            title
        ):

            competitor_logger.warning(

                f"[LOW QUALITY TITLE] "
                f"{title}"
            )

            return False

        return True

    # ==================================================
    # BUILD REAL RESULT
    # ==================================================

    def build_real_result(
        self,
        result,
    ):

        """
        Build normalized real SERP result.
        """

        url = result.get(
            "url",
            ""
        )

        parsed_data = (
            self.parser.parse_url(
                url
            )
        )

        headings = (
            parsed_data.get(
                "headings",
                []
            )
        )

        word_count = (
            parsed_data.get(
                "word_count",
                0
            )
        )

        # ==========================================
        # LOW QUALITY CONTENT
        # ==========================================

        if word_count < (
            self.MIN_WORD_COUNT
        ):

            competitor_logger.warning(

                f"[FILTERED LOW WORD COUNT] "
                f"{word_count} | "
                f"{url}"
            )

            return None

        return {

            "position": result.get(
                "position",
                0
            ),

            "title": TextCleaner.clean(
                result.get(
                    "title",
                    ""
                )
            ),

            "url": url,

            "meta_description": TextCleaner.clean(
                result.get(
                    "snippet",
                    ""
                )
            ),

            "word_count": (
                word_count
            ),

            "content_type": (
                "article"
            ),

            "seo_signals": {

                "has_faq": (
                    any(
                        "faq" in heading.lower()
                        for heading in headings
                    )
                ),

                "has_comparison": (
                    any(
                        "comparison" in heading.lower()
                        for heading in headings
                    )
                ),

                "has_buying_guide": (
                    any(
                        "buying guide" in heading.lower()
                        for heading in headings
                    )
                ),

                "internal_links": 0,

                "external_links": 0,
            },

            "headings": headings,
        }

    # ==================================================
    # REMOVE DUPLICATES
    # ==================================================

    def remove_duplicates(
        self,
        results,
    ):

        unique_results = []

        seen_titles = set()

        for result in results:

            if not result:

                continue

            title = (
                result.get(
                    "title",
                    ""
                )
                .strip()
                .lower()
            )

            if not title:

                continue

            if title in seen_titles:

                continue

            seen_titles.add(
                title
            )

            unique_results.append(
                result
            )

        return unique_results

    # ==================================================
    # FILTER SERP RESULTS
    # ==================================================

    def filter_serp_results(
        self,
        results,
    ):

        """
        Filter low-quality SERP results.
        """

        filtered = []

        for result in results:

            if not self.is_high_quality_result(
                result
            ):

                continue

            filtered.append(
                result
            )

        return filtered

    # ==================================================
    # EXTRACT
    # ==================================================

    def extract(
        self,
        keyword,
    ):

        keyword = (
            KeywordNormalizer.normalize(
                keyword
            )
        )

        competitor_logger.info(

            f"Running SERP extraction "
            f"for keyword: {keyword}"
        )

        # ==========================================
        # FETCH REAL RESULTS
        # ==========================================

        real_results = (
            self.fetcher.fetch_google_results(
                keyword
            )
        )

        serp_results = []

        # ==========================================
        # USE REAL RESULTS
        # ==========================================

        if real_results:

            competitor_logger.info(

                f"Using real SERP results "
                f"for keyword: {keyword}"
            )

            # ==========================================
            # FILTER RESULTS
            # ==========================================

            filtered_results = (
                self.filter_serp_results(
                    real_results
                )
            )

            competitor_logger.info(

                f"[FILTERED RESULTS] "
                f"{len(filtered_results)} "
                f"remaining"
            )

            # ==========================================
            # BUILD RESULTS
            # ==========================================

            for result in filtered_results[

                : self.MAX_RESULTS

            ]:

                parsed_result = (
                    self.build_real_result(
                        result
                    )
                )

                if not parsed_result:

                    continue

                serp_results.append(
                    parsed_result
                )

        # ==========================================
        # FINAL CLEANUP
        # ==========================================

        unique_results = (
            self.remove_duplicates(
                serp_results
            )
        )

        competitor_logger.info(

            f"SERP extraction completed "
            f"with {len(unique_results)} "
            f"high-quality results"
        )

        return {

            "keyword": keyword,

            "total_results": len(
                unique_results
            ),

            "results": (
                unique_results
            ),
        }