"""
Rewrite manager.
"""

from __future__ import annotations

import logging

from apps.rewriter.smart_rewriter import (
    SmartRewriter,
)

from apps.rewriter.exceptions import (
    RewriteException,
)


logger = logging.getLogger(
    __name__
)


class RewriteManager:

    # ==================================================
    # INIT
    # ==================================================

    def __init__(
        self,
    ):

        # ==========================================
        # SMART REWRITER
        # ==========================================

        self.smart_rewriter = (
            SmartRewriter()
        )

    # ==================================================
    # PROCESS
    # ==================================================

    def process(
        self,
        article_data,
    ):

        # ==========================================
        # VALIDATE INPUT
        # ==========================================

        if not article_data:

            raise RewriteException(
                "Article data is required"
            )

        # ==========================================
        # EXTRACT CONTENT
        # ==========================================

        original_content = (
            article_data.get(
                "content"
            )
        )

        if not original_content:

            raise RewriteException(
                "Article content is required"
            )

        original_word_count = len(
            original_content.split()
        )

        logger.info(

            "Rewrite started "
            "| original_words=%d",

            original_word_count,
        )

        # ==========================================
        # RUN SMART REWRITER
        # ==========================================

        try:

            optimized_result = (

                self.smart_rewriter.optimize(
                    original_content
                )
            )

        except Exception as error:

            logger.exception(

                "Rewrite failed. "
                "Using original content. "
                "Error=%s",

                error,
            )

            optimized_result = {

                "content": (
                    original_content
                ),

                "analysis": {},

                "score": 0,

                "quality_status": (
                    "fallback"
                ),
            }

        # ==========================================
        # EXTRACT REWRITTEN CONTENT
        # ==========================================

        rewritten_content = (

            optimized_result.get(
                "content"
            )
        )

        # ==========================================
        # EMPTY OUTPUT PROTECTION
        # ==========================================

        if not rewritten_content:

            logger.warning(

                "Rewrite returned empty "
                "content. Using original."
            )

            rewritten_content = (
                original_content
            )

        rewritten_word_count = len(
            rewritten_content.split()
        )

        logger.info(

            "Rewrite completed "
            "| rewritten_words=%d",

            rewritten_word_count,
        )

        # ==========================================
        # CONTENT LOSS PROTECTION
        # ==========================================

        minimum_safe_words = int(

            original_word_count * 0.60
        )

        if rewritten_word_count < minimum_safe_words:

            logger.warning(

                "Rewrite lost too much "
                "content. "
                "| original=%d "
                "| rewritten=%d "
                "| using original",

                original_word_count,

                rewritten_word_count,
            )

            rewritten_content = (
                original_content
            )

            rewritten_word_count = (
                original_word_count
            )

        # ==========================================
        # UPDATE ARTICLE DATA
        # ==========================================

        article_data[
            "content"
        ] = rewritten_content

        article_data[
            "rewrite_analysis"
        ] = optimized_result.get(
            "analysis",
            {},
        )

        article_data[
            "rewrite_score"
        ] = optimized_result.get(
            "score",
            0,
        )

        article_data[
            "rewrite_quality_status"
        ] = optimized_result.get(
            "quality_status",
            "unknown",
        )

        # ==========================================
        # METADATA
        # ==========================================

        article_data[
            "rewritten"
        ] = True

        article_data[
            "original_word_count"
        ] = original_word_count

        article_data[
            "rewritten_word_count"
        ] = rewritten_word_count

        # ==========================================
        # FINAL LOG
        # ==========================================

        logger.info(

            "Rewrite manager finished "
            "| final_words=%d "
            "| rewrite_score=%s",

            rewritten_word_count,

            article_data[
                "rewrite_score"
            ],
        )

        # ==========================================
        # RETURN RESULT
        # ==========================================

        return article_data