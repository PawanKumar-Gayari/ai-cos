"""
Content generation handler.
"""

from apps.generator.engine import (
    GeneratorEngine,
)


class GenerationHandler:

    def __init__(self):

        # =========================
        # GENERATOR ENGINE
        # =========================

        self.generator_engine = (
            GeneratorEngine()
        )

    def execute(
        self,
        keyword_data
    ):

        # =========================
        # EXTRACT KEYWORD
        # =========================

        keyword = keyword_data.get(
            "keyword"
        )

        # =========================
        # VALIDATE KEYWORD
        # =========================

        if not keyword:

            raise Exception(
                "Keyword is required"
            )

        # =========================
        # GENERATE CONTENT
        # =========================

        generated_content = (
            self.generator_engine.generate(
                keyword_data
            )
        )

        # =========================
        # VALIDATE RESPONSE
        # =========================

        if not generated_content:

            raise Exception(
                "Empty content generated"
            )

        # =========================
        # FALLBACK STRUCTURE
        # =========================

        if not isinstance(
            generated_content,
            dict
        ):

            generated_content = {

                "title": (
                    f"Complete Guide About {keyword}"
                ),

                "meta_description": (
                    f"Learn everything about {keyword} "
                    f"in this detailed guide."
                ),

                "content": str(
                    generated_content
                ),

                "faq": "",

                "conclusion": (
                    f"{keyword} is an important topic."
                ),
            }

        # =========================
        # EXTRACT FIELDS
        # =========================

        title = generated_content.get(
            "title"
        )

        content = generated_content.get(
            "content"
        )

        meta_description = (
            generated_content.get(
                "meta_description"
            )
        )

        # =========================
        # FALLBACK TITLE
        # =========================

        if not title:

            generated_content[
                "title"
            ] = (
                f"Complete Guide About {keyword}"
            )

        # =========================
        # FALLBACK META DESCRIPTION
        # =========================

        if not meta_description:

            generated_content[
                "meta_description"
            ] = (
                f"Learn everything about {keyword} "
                f"in this detailed guide."
            )

        # =========================
        # VALIDATE CONTENT
        # =========================

        if not content:

            raise Exception(
                "Generated content is empty"
            )

        if len(content.strip()) < 300:

            raise Exception(
                "Generated content too short"
            )

        # =========================
        # ENSURE REQUIRED FIELDS
        # =========================

        generated_content.setdefault(
            "faq",
            ""
        )

        generated_content.setdefault(
            "conclusion",
            ""
        )

        generated_content.setdefault(
            "seo_score",
            80
        )

        generated_content.setdefault(
            "verified",
            True
        )

        # =========================
        # RETURN CLEAN CONTENT
        # =========================

        return generated_content