"""
SEO content verification and parsing service.
"""

import re


class VerificationService:

    def verify(self, content_data):

        # =========================
        # EXTRACT CONTENT
        # =========================

        title = content_data.get(
            "title",
            ""
        )

        content = content_data.get(
            "content",
            ""
        )

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
        # BUILD FINAL CONTENT
        # =========================

        final_content = f"""

# {seo_title}

## Meta Description

{meta_description}

---

{article}

---

## FAQ

{faq}

---

## Conclusion

{conclusion}

"""

        # =========================
        # SEO SCORE
        # =========================

        seo_score = self.calculate_seo_score(
            content
        )

        # =========================
        # RETURN VERIFIED DATA
        # =========================

        return {

            "title": seo_title or title,

            "slug": slug,

            "meta_description": meta_description,

            "content": final_content,

            "faq": faq,

            "conclusion": conclusion,

            "seo_score": seo_score,

            "verified": True,
        }

    def extract_section(
        self,
        text,
        start,
        end=None
    ):

        try:

            if end:

                pattern = (
                    rf"{re.escape(start)}(.*?){re.escape(end)}"
                )

            else:

                pattern = (
                    rf"{re.escape(start)}(.*)"
                )

            match = re.search(

                pattern,

                text,

                re.DOTALL
            )

            if match:

                return (
                    match.group(1)
                    .strip()
                )

        except Exception:

            pass

        return ""

    def calculate_seo_score(
        self,
        content
    ):

        score = 50

        checks = [

            "SEO Title:",
            "Meta Description:",
            "FAQ:",
            "Conclusion:",
            "H1",
            "H2",
        ]

        for item in checks:

            if item.lower() in content.lower():

                score += 8

        return min(score, 100)