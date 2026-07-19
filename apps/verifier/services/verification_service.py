"""
Central verification service for AI content.
"""

from apps.verifier.parsers.content_parser import (
    ContentParser,
)

from apps.verifier.validators.seo_validator import (
    SEOValidator,
)

from apps.verifier.validators.readability_validator import (
    ReadabilityValidator,
)


class VerificationService:

    def __init__(self):

        # =========================
        # COMPONENTS
        # =========================

        self.content_parser = (
            ContentParser()
        )

        self.seo_validator = (
            SEOValidator()
        )

        self.readability_validator = (
            ReadabilityValidator()
        )

    def verify(
        self,
        content_data
    ):

        # =========================
        # EXTRACT RAW CONTENT
        # =========================

        raw_content = content_data.get(
            "content",
            ""
        )

        keyword = content_data.get(
            "title",
            ""
        )

        # =========================
        # PARSE CONTENT
        # =========================

        parsed_content = (
            self.content_parser.parse(
                raw_content
            )
        )

        # =========================
        # SEO VALIDATION
        # =========================

        seo_result = (
            self.seo_validator.validate(

                parsed_content,

                keyword
            )
        )

        # =========================
        # READABILITY VALIDATION
        # =========================

        readability_result = (
            self.readability_validator.validate(

                parsed_content.get(
                    "article",
                    ""
                )
            )
        )

        # =========================
        # FINAL CONTENT
        # =========================

        final_content = f"""

# {parsed_content.get('seo_title')}

## Meta Description

{parsed_content.get('meta_description')}

---

{parsed_content.get('article')}

---

## FAQ

{parsed_content.get('faq')}

---

## Conclusion

{parsed_content.get('conclusion')}
"""

        # =========================
        # FINAL SCORE
        # =========================

        final_score = int(

            (
                seo_result.get(
                    "seo_score",
                    0
                )

                +

                readability_result.get(
                    "readability_score",
                    0
                )
            ) / 2
        )

        # =========================
        # RETURN VERIFIED DATA
        # =========================

        return {

            "title": parsed_content.get(
                "seo_title"
            ),

            "slug": parsed_content.get(
                "slug"
            ),

            "meta_description": parsed_content.get(
                "meta_description"
            ),

            "content": final_content,

            "faq": parsed_content.get(
                "faq"
            ),

            "conclusion": parsed_content.get(
                "conclusion"
            ),

            "seo_score": final_score,

            "seo_validation": seo_result,

            "readability_validation": (
                readability_result
            ),

            "verified": True,
        }