"""
Rewrite service.
"""

from apps.rewriter.local_rewriter import (
    LocalRewriter,
)

from apps.rewriter.cache import (
    RewriteCache,
)

from apps.rewriter.strategies import (
    HUMANIZE,
    SEO,
    READABILITY,
    ENGAGEMENT,
)

from apps.rewriter.exceptions import (
    RewriteException,
)


class RewriteService:

    def __init__(
        self,
    ):

        # ======================================
        # LOCAL REWRITER
        # ======================================

        self.local_rewriter = (
            LocalRewriter()
        )

        # ======================================
        # CACHE
        # ======================================

        self.cache = (
            RewriteCache()
        )

    # ==================================================
    # REWRITE
    # ==================================================

    def rewrite(
        self,
        content,
        strategy=HUMANIZE,
    ):

        # ==============================================
        # VALIDATE CONTENT
        # ==============================================

        if not content:

            raise RewriteException(
                "Content is required"
            )

        # ==============================================
        # CACHE HIT
        # ==============================================

        cache_key = (
            f"{strategy}:{content}"
        )

        cached = (
            self.cache.get(
                cache_key
            )
        )

        if cached:

            return cached

        # ==============================================
        # LOCAL REWRITE
        # ==============================================

        rewritten_content = (

            self.local_rewriter.rewrite(
                content
            )
        )

        # ==============================================
        # STRATEGY OPTIMIZATION
        # ==============================================

        rewritten_content = (

            self.apply_strategy(
                rewritten_content,
                strategy,
            )
        )

        # ==============================================
        # VALIDATE OUTPUT
        # ==============================================

        if not rewritten_content:

            raise RewriteException(
                "Rewrite failed"
            )

        # ==============================================
        # CLEAN RESPONSE
        # ==============================================

        rewritten_content = (
            self.clean_response(
                rewritten_content
            )
        )

        # ==============================================
        # SAVE CACHE
        # ==============================================

        self.cache.set(

            cache_key,

            rewritten_content,
        )

        # ==============================================
        # RETURN CONTENT
        # ==============================================

        return rewritten_content

    # ==================================================
    # APPLY STRATEGY
    # ==================================================

    def apply_strategy(
        self,
        content,
        strategy,
    ):

        # ==============================================
        # HUMANIZE
        # ==============================================

        if strategy == HUMANIZE:

            return content

        # ==============================================
        # SEO
        # ==============================================

        if strategy == SEO:

            return self.optimize_seo(
                content
            )

        # ==============================================
        # READABILITY
        # ==============================================

        if strategy == READABILITY:

            return self.improve_readability(
                content
            )

        # ==============================================
        # ENGAGEMENT
        # ==============================================

        if strategy == ENGAGEMENT:

            return self.improve_engagement(
                content
            )

        return content

    # ==================================================
    # SEO OPTIMIZATION
    # ==================================================

    def optimize_seo(
        self,
        content,
    ):

        # ==============================================
        # ADD SEO HEADING
        # ==============================================

        if "## Benefits" not in content:

            content += (

                "\n\n## Benefits\n\n"

                "This topic provides "
                "valuable insights "
                "and practical knowledge."
            )

        return content

    # ==================================================
    # READABILITY
    # ==================================================

    def improve_readability(
        self,
        content,
    ):

        # ==============================================
        # SHORTEN LONG SENTENCES
        # ==============================================

        content = (
            content.replace(
                ", and",
                ". And",
            )
        )

        return content

    # ==================================================
    # ENGAGEMENT
    # ==================================================

    def improve_engagement(
        self,
        content,
    ):

        hooks = [

            "Did you know?",

            "Here's something important:",

            "Let's understand this:",

            "This matters because:",
        ]

        # ==============================================
        # ALREADY HAS HOOK
        # ==============================================

        if any(

            hook.lower()
            in
            content.lower()

            for hook in hooks
        ):

            return content

        # ==============================================
        # ADD HOOK
        # ==============================================

        return (

            hooks[0]

            + "\n\n"

            + content
        )

    # ==================================================
    # CLEAN RESPONSE
    # ==================================================

    def clean_response(
        self,
        content,
    ):

        # ==============================================
        # HANDLE DICT RESPONSE
        # ==============================================

        if isinstance(
            content,
            dict,
        ):

            content = (
                content.get(
                    "content",
                    ""
                )
            )

        # ==============================================
        # REMOVE CODE BLOCKS
        # ==============================================

        content = (
            content
            .replace(
                "```markdown",
                ""
            )
            .replace(
                "```",
                ""
            )
            .strip()
        )

        # ==============================================
        # REMOVE EXTRA SPACES
        # ==============================================

        content = (
            " ".join(
                content.split()
            )
        )

        return content