"""
Main orchestration engine for AI COS.
"""

from __future__ import annotations

import logging
from time import perf_counter

from django.utils.text import slugify

from apps.analytics.engine import (
    AnalyticsEngine,
)

from apps.engine.constants import (
    STEP_GENERATION,
    STEP_KEYWORD,
    STEP_PUBLISHING,
    STEP_VERIFICATION,
)

from apps.engine.exceptions import (
    PipelineException,
)

from apps.engine.handlers.generation_handler import (
    GenerationHandler,
)

from apps.engine.handlers.keyword_handler import (
    KeywordHandler,
)

from apps.engine.handlers.verification_handler import (
    VerificationHandler,
)

from apps.engine.models import (
    Article,
    GenerationLog,
    Keyword,
)

from apps.engine.state_manager import (
    StateManager,
)

from apps.publisher.services.publish_service import (
    PublishService,
)

from apps.rewriter.manager import (
    RewriteManager,
)


logger = logging.getLogger(
    __name__
)


class Orchestrator:

    # ==================================================
    # INIT
    # ==================================================

    def __init__(
        self,
    ):

        # ==========================================
        # STATE
        # ==========================================

        self.state_manager = (
            StateManager()
        )

        # ==========================================
        # HANDLERS
        # ==========================================

        self.keyword_handler = (
            KeywordHandler()
        )

        self.generation_handler = (
            GenerationHandler()
        )

        self.verification_handler = (
            VerificationHandler()
        )

        # ==========================================
        # REWRITER
        # ==========================================

        self.rewrite_manager = (
            RewriteManager()
        )

        # ==========================================
        # ANALYTICS
        # ==========================================

        self.analytics = (
            AnalyticsEngine()
        )

        # ==========================================
        # PUBLISHER
        # ==========================================

        self.publish_service = (
            PublishService()
        )

    # ==================================================
    # MAIN PIPELINE
    # ==================================================

    def run(
        self,
        keyword: str,
    ):

        start_time = perf_counter()

        try:

            # ==========================================
            # START
            # ==========================================

            self.state_manager.start_pipeline()

            logger.info(

                "Pipeline started "
                "| keyword=%r",

                keyword,
            )

            # ==================================================
            # STEP 1 — KEYWORD
            # ==================================================

            self.state_manager.set_step(
                STEP_KEYWORD
            )

            keyword_data = (

                self.keyword_handler.execute(
                    keyword
                )
            )

            self.state_manager.update_data(

                "keyword",

                keyword_data,
            )

            # ==================================================
            # SAVE KEYWORD
            # ==================================================

            keyword_object, _ = (

                Keyword.objects.get_or_create(

                    keyword=keyword_data[
                        "keyword"
                    ],

                    defaults={

                        "intent": (
                            keyword_data.get(
                                "intent"
                            )
                        ),

                        "difficulty": (
                            keyword_data.get(
                                "difficulty"
                            )
                        ),

                        "volume": (
                            keyword_data.get(
                                "volume",
                                0,
                            )
                        ),
                    },
                )
            )

            # ==================================================
            # STEP 2 — GENERATION
            # ==================================================

            self.state_manager.set_step(
                STEP_GENERATION
            )

            content = None

            for attempt in range(3):

                try:

                    logger.info(

                        "Generation attempt=%d",

                        attempt + 1,
                    )

                    content = (

                        self.generation_handler.execute(
                            keyword_data
                        )
                    )

                    if content:

                        logger.info(
                            "Content generation succeeded."
                        )

                        break

                except Exception as error:

                    logger.warning(

                        "Generation failed: %s",

                        error,
                    )

            if not content:

                raise Exception(
                    "Content generation failed"
                )

            self.state_manager.update_data(
                "content",
                content,
            )

            logger.info(

                "Generated article "
                "| words=%d",

                len(
                    content.get(
                        "content",
                        ""
                    ).split()
                ),
            )

            # ==================================================
            # STEP 3 — VERIFICATION
            # ==================================================

            self.state_manager.set_step(
                STEP_VERIFICATION
            )

            verification_result = (

                self.verification_handler.execute(
                    content
                )
            )

            # ==================================================
            # MERGE ORIGINAL CONTENT
            # ==================================================

            verification_result[
                "title"
            ] = content.get(
                "title"
            )

            verification_result[
                "content"
            ] = content.get(
                "content"
            )

            verification_result[
                "meta_description"
            ] = content.get(
                "meta_description"
            )

            verification_result[
                "faq"
            ] = content.get(
                "faq"
            )

            verification_result[
                "conclusion"
            ] = content.get(
                "conclusion"
            )

            self.state_manager.update_data(

                "verified_content",

                verification_result,
            )

            # ==================================================
            # STEP 4 — REWRITE
            # ==================================================

            rewritten_content = (

                self.rewrite_manager.process(
                    verification_result
                )
            )

            self.state_manager.update_data(

                "rewritten_content",

                rewritten_content,
            )

            # ==================================================
            # EXTRACT DATA
            # ==================================================

            title = rewritten_content.get(
                "title"
            )

            content_body = rewritten_content.get(
                "content"
            )

            meta_description = (

                rewritten_content.get(
                    "meta_description"
                )
            )

            faq = rewritten_content.get(
                "faq"
            )

            conclusion = rewritten_content.get(
                "conclusion"
            )

            # ==================================================
            # FALLBACKS
            # ==================================================

            if not title:

                title = (
                    f"Complete Guide About {keyword}"
                )

            if not content_body:

                logger.warning(

                    "Rewrite returned empty "
                    "content. Using original."
                )

                content_body = content.get(
                    "content"
                )

            if not meta_description:

                meta_description = (

                    content_body[:160]
                )

            # ==================================================
            # VALIDATE
            # ==================================================

            word_count = len(
                content_body.split()
            )

            logger.info(

                "Final content "
                "| words=%d",

                word_count,
            )

            minimum_words = 500

            if word_count < minimum_words:

                logger.warning(

                    "Rewrite reduced content "
                    "too much. Using original."
                )

                content_body = content.get(
                    "content"
                )

                word_count = len(
                    content_body.split()
                )

            if word_count < minimum_words:

                raise Exception(

                    f"Generated content too short "
                    f"({word_count} words)."
                )

            # ==================================================
            # SAVE ARTICLE
            # ==================================================

            article = Article.objects.create(

                keyword=keyword_object,

                title=title,

                slug=slugify(title),

                meta_description=(
                    meta_description
                ),

                content=content_body,

                faq=faq,

                conclusion=conclusion,

                seo_score=(
                    rewritten_content.get(
                        "seo_score",
                        0,
                    )
                ),

                rewrite_score=(
                    rewritten_content.get(
                        "rewrite_score",
                        0,
                    )
                ),

                rewrite_quality_status=(

                    rewritten_content.get(
                        "rewrite_quality_status",
                        "",
                    )
                ),

                is_verified=(
                    rewritten_content.get(
                        "verified",
                        False,
                    )
                ),

                is_published=False,

                ai_provider="AI Router",
            )

            logger.info(

                "Article saved "
                "| article_id=%s",

                article.id,
            )

            # ==================================================
            # EXECUTION TIME
            # ==================================================

            execution_time = (
                perf_counter()
                - start_time
            )

            # ==================================================
            # GENERATION LOG
            # ==================================================

            GenerationLog.objects.create(

                article=article,

                provider="AI Router",

                status="success",

                response_time=(
                    execution_time
                ),
            )

            # ==================================================
            # ANALYTICS
            # ==================================================

            rewrite_analysis = (

                rewritten_content.get(
                    "rewrite_analysis",
                    {},
                )
            )

            self.analytics.track_article(

                article=article,

                provider="AI Router",

                generation_time=(
                    execution_time
                ),

                rewrite_score=(
                    rewritten_content.get(
                        "rewrite_score",
                        0,
                    )
                ),

                readability_score=(

                    rewrite_analysis.get(
                        "readability",
                        {},
                    ).get(
                        "score",
                        0,
                    )
                ),

                engagement_score=(

                    rewrite_analysis.get(
                        "engagement",
                        {},
                    ).get(
                        "score",
                        0,
                    )
                ),

                ai_detection_score=(

                    rewrite_analysis.get(
                        "ai_detection",
                        {},
                    ).get(
                        "score",
                        0,
                    )
                ),

                verification_score=(

                    verification_result.get(
                        "verification_score",
                        0,
                    )
                ),

                verified_claims=(

                    verification_result.get(
                        "verified_claims",
                        0,
                    )
                ),

                flagged_claims=(

                    verification_result.get(
                        "flagged_claims",
                        0,
                    )
                ),

                seo_score=(
                    article.seo_score
                ),

                used_fallback=False,

                final_quality_score=(

                    rewritten_content.get(
                        "rewrite_score",
                        0,
                    )
                ),

                quality_status=(

                    rewritten_content.get(
                        "rewrite_quality_status",
                        "unknown",
                    )
                ),
            )

            logger.info(
                "Analytics tracked."
            )

            # ==================================================
            # PROVIDER ANALYTICS
            # ==================================================

            self.analytics.track_provider(

                provider_name="AI Router",

                success=True,

                response_time=(
                    execution_time
                ),

                quality_score=(

                    rewritten_content.get(
                        "rewrite_score",
                        0,
                    )
                ),

                fallback_used=False,
            )

            logger.info(
                "Provider analytics updated."
            )

            # ==================================================
            # STEP 5 — PUBLISHING
            # ==================================================

            self.state_manager.set_step(
                STEP_PUBLISHING
            )

            logger.info(
                "Starting publishing step."
            )

            published_result = (

                self.publish_service.create_draft(
                    article
                )
            )

            self.state_manager.update_data(

                "published_result",

                published_result,
            )

            if published_result.get(
                "success"
            ):

                logger.info(

                    "Draft published "
                    "| article_id=%s "
                    "| url=%s",

                    article.id,

                    published_result.get(
                        "url"
                    ),
                )

            else:

                logger.warning(

                    "Publishing failed "
                    "| article_id=%s "
                    "| error=%s",

                    article.id,

                    published_result.get(
                        "error"
                    ),
                )

            # ==================================================
            # SAVE ARTICLE ID
            # ==================================================

            self.state_manager.update_data(

                "article_id",

                article.id,
            )

            # ==================================================
            # COMPLETE
            # ==================================================

            self.state_manager.complete_pipeline()

            logger.info(
                "Pipeline completed successfully."
            )

            return self.state_manager.get_state()

        except Exception as error:

            logger.exception(
                "Pipeline failed: %s",
                error,
            )

            self.state_manager.fail_pipeline(
                error
            )

            raise PipelineException(
                str(error)
            )