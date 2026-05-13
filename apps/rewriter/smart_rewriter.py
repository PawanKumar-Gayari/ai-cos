"""
Smart autonomous rewriter.
"""

from apps.rewriter.engine import (
    RewriteEngine,
)

from apps.rewriter.analyzer import (
    RewriteAnalyzer,
)

from apps.rewriter.cache import (
    RewriteCache,
)

from apps.rewriter.constants import (
    MAX_REWRITE_LOOPS,
)

from apps.rewriter.exceptions import (
    RewriteException,
)


class SmartRewriter:

    def __init__(self):

        # =========================
        # REWRITE ENGINE
        # =========================

        self.rewrite_engine = (
            RewriteEngine()
        )

        # =========================
        # ANALYZER
        # =========================

        self.analyzer = (
            RewriteAnalyzer()
        )

        # =========================
        # CACHE
        # =========================

        self.cache = (
            RewriteCache()
        )

    def optimize(
        self,
        content,
        target_score=85,
        use_cache=True,
    ):

        # =========================
        # VALIDATE CONTENT
        # =========================

        if not content:

            raise RewriteException(
                "Content is required"
            )

        # =========================
        # CHECK CACHE
        # =========================

        if use_cache:

            cached_result = (
                self.cache.get(
                    content
                )
            )

            if cached_result:

                cached_result[
                    "cache_hit"
                ] = True

                return cached_result

        # =========================
        # INITIAL CONTENT
        # =========================

        optimized_content = (
            content
        )

        # =========================
        # INITIAL ANALYSIS
        # =========================

        analysis = (
            self.analyzer.analyze(
                optimized_content
            )
        )

        best_score = analysis[
            "final_score"
        ]

        best_content = (
            optimized_content
        )

        # =========================
        # OPTIMIZATION LOOP
        # =========================

        for loop in range(
            MAX_REWRITE_LOOPS
        ):

            # =====================
            # TARGET REACHED
            # =====================

            if best_score >= target_score:

                break

            # =====================
            # REWRITE CONTENT
            # =====================

            optimized_content = (

                self.rewrite_engine.process(
                    optimized_content
                )
            )

            # =====================
            # ANALYZE AGAIN
            # =====================

            analysis = (
                self.analyzer.analyze(
                    optimized_content
                )
            )

            current_score = analysis[
                "final_score"
            ]

            # =====================
            # SAVE BEST CONTENT
            # =====================

            if current_score > best_score:

                best_score = (
                    current_score
                )

                best_content = (
                    optimized_content
                )

        # =========================
        # FINAL ANALYSIS
        # =========================

        final_analysis = (
            self.analyzer.analyze(
                best_content
            )
        )

        # =========================
        # FINAL RESULT
        # =========================

        result = {

            "content": (
                best_content
            ),

            "analysis": (
                final_analysis
            ),

            "score": (
                final_analysis[
                    "final_score"
                ]
            ),

            "quality_status": (
                final_analysis[
                    "quality_status"
                ]
            ),

            "cache_hit": False,
        }

        # =========================
        # SAVE CACHE
        # =========================

        if use_cache:

            self.cache.set(

                content=content,

                data=result,
            )

        # =========================
        # RETURN RESULT
        # =========================

        return result