"""
Content parser for AI generated SEO articles.
"""

import re


class ContentParser:

    def parse(
        self,
        content
    ):

        # =========================
        # PARSE SEO TITLE
        # =========================

        seo_title = self.extract_section(

            content,

            "SEO Title:",
            "Meta Description:"
        )

        # =========================
        # PARSE META DESCRIPTION
        # =========================

        meta_description = self.extract_section(

            content,

            "Meta Description:",
            "Slug:"
        )

        # =========================
        # PARSE SLUG
        # =========================

        slug = self.extract_section(

            content,

            "Slug:",
            "Article:"
        )

        # =========================
        # PARSE ARTICLE
        # =========================

        article = self.extract_section(

            content,

            "Article:",
            "FAQ:"
        )

        # =========================
        # PARSE FAQ
        # =========================

        faq = self.extract_section(

            content,

            "FAQ:",
            "Conclusion:"
        )

        # =========================
        # PARSE CONCLUSION
        # =========================

        conclusion = self.extract_section(

            content,

            "Conclusion:",
            None
        )

        # =========================
        # BUILD STRUCTURED DATA
        # =========================

        return {

            "seo_title": seo_title,

            "meta_description": meta_description,

            "slug": slug,

            "article": article,

            "faq": faq,

            "conclusion": conclusion,
        }

    def extract_section(
        self,
        text,
        start,
        end=None
    ):

        try:

            # =========================
            # BUILD PATTERN
            # =========================

            if end:

                pattern = (
                    rf"{re.escape(start)}(.*?){re.escape(end)}"
                )

            else:

                pattern = (
                    rf"{re.escape(start)}(.*)"
                )

            # =========================
            # SEARCH CONTENT
            # =========================

            match = re.search(

                pattern,

                text,

                re.DOTALL
            )

            # =========================
            # RETURN RESULT
            # =========================

            if match:

                return (
                    match.group(1)
                    .strip()
                )

        except Exception:

            pass

        return ""