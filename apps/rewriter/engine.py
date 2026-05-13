"""
Rewrite engine.
"""

from apps.rewriter.rewriter import (
    Rewriter,
)

from apps.rewriter.local_humanizer import (
    LocalHumanizer,
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


class RewriteEngine:

    def __init__(self):

        # =========================
        # REWRITER
        # =========================

        self.rewriter = (
            Rewriter()
        )

        # =========================
        # LOCAL HUMANIZER
        # =========================

        self.local_humanizer = (
            LocalHumanizer()
        )

    def process(
        self,
        content,
        humanize=True,
        seo=True,
        readability=True,
        engagement=True,
        use_local_humanizer=True,
    ):

        # =========================
        # VALIDATE CONTENT
        # =========================

        if not content:

            raise RewriteException(
                "Content is required"
            )

        # =========================
        # INITIAL CONTENT
        # =========================

        rewritten_content = (
            content
        )

        # =========================
        # LOCAL HUMANIZER
        # =========================

        if use_local_humanizer:

            rewritten_content = (

                self.local_humanizer.humanize(
                    rewritten_content
                )
            )

        # =========================
        # AI HUMANIZE
        # =========================

        if humanize:

            try:

                rewritten_content = (
                    self.rewriter.rewrite(

                        content=rewritten_content,

                        strategy=HUMANIZE,
                    )
                )

            except Exception:

                # =====================
                # FALLBACK TO LOCAL
                # =====================

                rewritten_content = (

                    self.local_humanizer.humanize(
                        rewritten_content
                    )
                )

        # =========================
        # SEO OPTIMIZATION
        # =========================

        if seo:

            try:

                rewritten_content = (
                    self.rewriter.rewrite(

                        content=rewritten_content,

                        strategy=SEO,
                    )
                )

            except Exception:

                pass

        # =========================
        # READABILITY
        # =========================

        if readability:

            try:

                rewritten_content = (
                    self.rewriter.rewrite(

                        content=rewritten_content,

                        strategy=READABILITY,
                    )
                )

            except Exception:

                rewritten_content = (

                    self.local_humanizer.break_long_sentences(
                        rewritten_content
                    )
                )

        # =========================
        # ENGAGEMENT
        # =========================

        if engagement:

            try:

                rewritten_content = (
                    self.rewriter.rewrite(

                        content=rewritten_content,

                        strategy=ENGAGEMENT,
                    )
                )

            except Exception:

                rewritten_content = (

                    self.local_humanizer.add_engagement(
                        rewritten_content
                    )
                )

        # =========================
        # VALIDATE FINAL OUTPUT
        # =========================

        if not rewritten_content:

            raise RewriteException(
                "Rewrite engine failed"
            )

        # =========================
        # RETURN CONTENT
        # =========================

        return rewritten_content