"""
Generator prompt modules.
"""

from apps.generator.prompts.prompt_builder import (
    PromptBuilder
)

from apps.generator.prompts.seo_prompt import (
    SEOPrompt
)

from apps.generator.prompts.competitor_prompt import (
    CompetitorPrompt
)

from apps.generator.prompts.article_prompt import (
    ARTICLE_MARKDOWN_RULES
)

from apps.generator.prompts.language_rules import (
    LANGUAGE_RULES
)

from apps.generator.prompts.quality_rules import (
    QUALITY_RULES
)

__all__ = [

    "PromptBuilder",

    "SEOPrompt",

    "CompetitorPrompt",

    "ARTICLE_MARKDOWN_RULES",

    "LANGUAGE_RULES",

    "QUALITY_RULES",
]