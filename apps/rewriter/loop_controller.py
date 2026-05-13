"""
Rewrite loop controller.
"""

from apps.rewriter.engine import (
    RewriteEngine,
)

from apps.rewriter.constants import (
    MAX_REWRITE_LOOPS,
)

from apps.rewriter.exceptions import (
    RewriteException,
)


class RewriteLoopController:

    def __init__(self):

        # =========================
        # REWRITE ENGINE
        # =========================

        self.rewrite_engine = (
            RewriteEngine()
        )

    def optimize(
        self,
        content,
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

        optimized_content = (
            content
        )

        # =========================
        # REWRITE LOOP
        # =========================

        for loop in range(
            MAX_REWRITE_LOOPS
        ):

            # =====================
            # PROCESS REWRITE
            # =====================

            optimized_content = (
                self.rewrite_engine.process(
                    optimized_content
                )
            )

            # =====================
            # VALIDATE OUTPUT
            # =====================

            if not optimized_content:

                raise RewriteException(
                    "Optimization failed"
                )

        # =========================
        # RETURN FINAL CONTENT
        # =========================

        return optimized_content