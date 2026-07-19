"""
Enterprise Prompt Builder
-------------------------

Production-grade modular prompt assembly engine.

Features:
- modular prompt composition
- multilingual support
- SEO-first prompting
- hallucination protection
- topical isolation
- competitor enrichment
- EEAT-oriented prompting
- production-ready architecture
"""

from __future__ import annotations

import logging

from apps.generator.prompts.language_rules import (
    LANGUAGE_RULES,
)

from apps.generator.prompts.quality_rules import (
    QUALITY_RULES,
)

from apps.generator.prompts.article_prompt import (
    ARTICLE_MARKDOWN_RULES,
)

from apps.generator.prompts.seo_prompt import (
    SEOPrompt,
)


logger = logging.getLogger(
    __name__
)


# =========================================================
# PROMPT BUILDER
# =========================================================

class PromptBuilder:

    """
    Enterprise modular prompt builder.
    """

    # =====================================================
    # BUILD COMPETITOR SECTION
    # =====================================================

    @classmethod
    def build_competitor_section(
        cls,
        competitor_context,
    ):

        if not competitor_context:

            return []

        return [

            "COMPETITOR INSIGHTS:",

            competitor_context,

            "",
        ]

    # =====================================================
    # BUILD QUALITY SECTION
    # =====================================================

    @classmethod
    def build_quality_section(
        cls,
    ):

        lines = [

            "ARTICLE QUALITY RULES:",
        ]

        for rule in (
            QUALITY_RULES
        ):

            lines.append(
                rule
            )

        lines.append("")

        return lines

    # =====================================================
    # BUILD MARKDOWN SECTION
    # =====================================================

    @classmethod
    def build_markdown_section(
        cls,
    ):

        lines = [

            "STRICT MARKDOWN RULES:",
        ]

        for rule in (
            ARTICLE_MARKDOWN_RULES
        ):

            lines.append(
                rule
            )

        lines.append("")

        return lines

    # =====================================================
    # BUILD FINAL TASK
    # =====================================================

    @classmethod
    def build_task_section(
        cls,
        user_query,
        language,
    ):

        lines = [

            f"TASK: {user_query}",

            "",
        ]

        if language == "hindi":

            lines.append(
                "Final article सीधे लिखें।"
            )

        else:

            lines.append(
                "Write the final SEO-optimized article directly."
            )

        return lines

    # =====================================================
    # BUILD FULL PROMPT
    # =====================================================

    @classmethod
    def build(
        cls,
        user_query,
        language,
        seo_data=None,
        competitor_context=None,
    ):

        try:

            sections = []

            # =========================================
            # LANGUAGE
            # =========================================

            language_rule = (
                LANGUAGE_RULES.get(
                    language,
                    LANGUAGE_RULES[
                        "english"
                    ]
                )
            )

            sections.append(
                language_rule
            )

            sections.append("")

            # =========================================
            # SEO FIRST
            # =========================================

            sections.extend(
                SEOPrompt.build(

                    seo_data,

                    user_query,
                )
            )

            # =========================================
            # COMPETITOR
            # =========================================

            sections.extend(
                cls.build_competitor_section(
                    competitor_context
                )
            )

            # =========================================
            # QUALITY
            # =========================================

            sections.extend(
                cls.build_quality_section()
            )

            # =========================================
            # MARKDOWN
            # =========================================

            sections.extend(
                cls.build_markdown_section()
            )

            # =========================================
            # TASK
            # =========================================

            sections.extend(
                cls.build_task_section(

                    user_query,

                    language,
                )
            )

            # =========================================
            # FINAL PROMPT
            # =========================================

            prompt = "\n".join(
                sections
            )

            logger.info(
                "Prompt build complete."
            )

            return prompt

        except Exception as error:

            logger.exception(

                f"Prompt build failed: "
                f"{str(error)}"
            )

            raise