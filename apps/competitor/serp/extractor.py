"""
SERP extractor for competitor intelligence engine.
"""

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

    MOCK_DOMAINS = [

        "example.com",

        "sampleblog.com",

        "techsite.com",

        "contenthub.com",

        "smartseo.com",
    ]

    def clean_title(
        self,
        title,
    ):

        """
        Clean SEO title.
        """

        return TextCleaner.clean(
            title
        )

    def build_result(
        self,
        position,
        title,
        url,
        meta_description,
        word_count,
        headings,
        content_type,
    ):

        """
        Build SERP result structure.
        """

        cleaned_headings = [

            TextCleaner.clean(
                heading
            )

            for heading in headings
        ]

        return {

            "position": position,

            "title": (
                self.clean_title(
                    title
                )
            ),

            "url": url,

            "meta_description": (
                TextCleaner.clean(
                    meta_description
                )
            ),

            "word_count": (
                word_count
            ),

            "content_type": (
                content_type
            ),

            "seo_signals": {

                "has_faq": (
                    "FAQ" in headings
                ),

                "has_comparison": (
                    "Comparison" in headings
                ),

                "has_buying_guide": (
                    "Buying Guide" in headings
                ),

                "internal_links": (
                    10 + position
                ),

                "external_links": (
                    3 + position
                ),
            },

            "headings": (
                cleaned_headings
            ),
        }

    def generate_mock_results(
        self,
        keyword,
        keyword_slug,
    ):

        """
        Generate mock SERP results.
        """

        title_1 = (
            f"{KeywordNormalizer.add_prefix(keyword, 'best')} "
            f"in 2026"
        )

        title_2 = (
            f"Top 10 {keyword}"
        )

        title_3 = (
            f"{keyword.title()} "
            f"Review and Comparison"
        )

        serp_results = [

            self.build_result(

                position=1,

                title=title_1,

                url=(

                    f"https://example.com/"
                    f"{keyword_slug}"
                ),

                meta_description=(

                    f"Complete guide about "
                    f"{keyword} with reviews, "
                    f"tips, and comparisons."
                ),

                word_count=3200,

                headings=[

                    "Introduction",

                    "Features",

                    "Pros and Cons",

                    "Buying Guide",

                    "Conclusion",
                ],

                content_type="guide",
            ),

            self.build_result(

                position=2,

                title=title_2,

                url=(

                    f"https://sampleblog.com/"
                    f"top-{keyword_slug}"
                ),

                meta_description=(

                    f"Discover the top "
                    f"{keyword} options "
                    f"available right now."
                ),

                word_count=2500,

                headings=[

                    "Overview",

                    "Best Picks",

                    "Comparison",

                    "FAQ",
                ],

                content_type="listicle",
            ),

            self.build_result(

                position=3,

                title=title_3,

                url=(

                    f"https://techsite.com/"
                    f"{keyword_slug}-review"
                ),

                meta_description=(

                    f"Detailed {keyword} review "
                    f"with pricing and "
                    f"performance analysis."
                ),

                word_count=2800,

                headings=[

                    "Review",

                    "Specifications",

                    "Performance",

                    "Verdict",
                ],

                content_type="review",
            ),
        ]

        return serp_results

    def remove_duplicates(
        self,
        results,
    ):

        """
        Remove duplicate SERP titles.
        """

        unique_results = []

        seen_titles = set()

        for result in results:

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

    def extract(
        self,
        keyword,
    ):

        """
        Run SERP extraction.
        """

        # ==========================================
        # NORMALIZE KEYWORD
        # ==========================================

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
        # SEO SLUG
        # ==========================================

        keyword_slug = (
            SEOHelpers.generate_slug(
                keyword
            )
        )

        # ==========================================
        # GENERATE MOCK RESULTS
        # ==========================================

        serp_results = (
            self.generate_mock_results(

                keyword,

                keyword_slug,
            )
        )

        # ==========================================
        # REMOVE DUPLICATES
        # ==========================================

        unique_results = (
            self.remove_duplicates(
                serp_results
            )
        )

        competitor_logger.info(

            f"SERP extraction completed "
            f"with {len(unique_results)} "
            f"results"
        )

        # ==========================================
        # RETURN RESULT
        # ==========================================

        return {

            "keyword": keyword,

            "total_results": len(
                unique_results
            ),

            "results": (
                unique_results
            ),
        }