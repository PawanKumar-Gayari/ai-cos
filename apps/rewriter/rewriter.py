"""
Main rewriter module.
"""

from apps.rewriter.services.rewrite_service import (
    RewriteService,
)

from apps.rewriter.strategies import (
    HUMANIZE,
)

from apps.rewriter.exceptions import (
    RewriteException,
)


class Rewriter:

    def __init__(self):

        # =========================
        # REWRITE SERVICE
        # =========================

        self.rewrite_service = (
            RewriteService()
        )

    def rewrite(
        self,
        content,
        strategy=HUMANIZE,
    ):

        # =========================
        # VALIDATE CONTENT
        # =========================

        if not content:

            raise RewriteException(
                "Content is required"
            )

        # =========================
        # RUN REWRITE
        # =========================

        rewritten_content = (
            self.rewrite_service.rewrite(

                content=content,

                strategy=strategy,
            )
        )

        # =========================
        # VALIDATE OUTPUT
        # =========================

        if not rewritten_content:

            raise RewriteException(
                "Rewritten content is empty"
            )

        # =========================
        # RETURN CONTENT
        # =========================

        return rewritten_content

    def humanize(
        self,
        content,
    ):

        return self.rewrite(

            content=content,

            strategy=HUMANIZE,
        )