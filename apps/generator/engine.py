"""
Enterprise SEO Orchestration Generator Engine
---------------------------------------------

FINAL OPTIMIZED ENTERPRISE EDITION

Major Improvements:
-------------------
✓ Removed aggressive regeneration loops
✓ Reduced Gemini API waste
✓ Faster orchestration flow
✓ Relaxed SEO validation
✓ Semantic-first validation
✓ Reduced retry storms
✓ Removed blocking sleep delays
✓ Better production stability
✓ Lower 503 probability
✓ OCI optimized
✓ Enterprise-grade validation flow
"""

from __future__ import annotations

import logging
import time

from apps.dashboard.services.feature_service import (
    FeatureService,
)

from apps.generator.services.orchestration_service import (
    OrchestrationService,
)

from apps.generator.models import (
    GeneratorConfig,
)

from apps.generator.response_cleaner import (
    ResponseCleaner,
)

from apps.generator.content_scorer import (
    ContentScorer,
)

from apps.keywords.engine import (
    KeywordEngine,
)

from apps.keywords.processors.density import (
    KeywordDensityProcessor,
)

from apps.monitoring.models import (
    EngineExecution,
)

from utils.content_formatter import (
    ContentFormatter,
)


logger = logging.getLogger(
    __name__
)


class GeneratorEngine:

    """
    Enterprise AI generation engine.
    """

    # =====================================================
    # OPTIMIZED THRESHOLDS
    # =====================================================

    MAX_RETRIES = 1

    MIN_CONTENT_LENGTH = 500

    MIN_SEO_SCORE = 45

    MIN_OVERALL_SCORE = 55

    MAX_AI_RISK_SCORE = 55

    BLOCKED_PATTERNS = [

        "ignore previous instructions",

        "system prompt",

        "developer instructions",

        "reveal hidden prompt",
    ]

    # =====================================================
    # INIT
    # =====================================================

    def __init__(
        self
    ):

        self.orchestrator = (
            OrchestrationService()
        )

        self.cleaner = (
            ResponseCleaner()
        )

        self.scorer = (
            ContentScorer()
        )

        self.keyword_engine = (
            KeywordEngine()
        )

        self.density_processor = (
            KeywordDensityProcessor()
        )

    # =====================================================
    # ACTIVE CONFIG
    # =====================================================

    def active_config(
        self,
    ):

        return (

            GeneratorConfig.objects
            .filter(
                is_active=True
            )
            .first()
        )

    # =====================================================
    # SAFE TEXT
    # =====================================================

    def safe_text(
        self,
        text,
    ):

        if not text:

            return False

        lowered = (
            str(text)
            .lower()
        )

        for pattern in (
            self.BLOCKED_PATTERNS
        ):

            if pattern in lowered:

                return False

        return True

    # =====================================================
    # NORMALIZE KEYWORD
    # =====================================================

    def normalize_keyword(
        self,
        keyword,
    ):

        if not keyword:

            return ""

        keyword = str(
            keyword
        ).strip()

        return keyword[:300]

    # =====================================================
    # VALIDATE RESPONSE
    # =====================================================

    def validate_response(
        self,
        response,
    ):

        if not response:

            raise Exception(
                "Empty response"
            )

        if not isinstance(
            response,
            dict,
        ):

            raise Exception(
                "Invalid response format"
            )

        content = response.get(
            "content",
            ""
        )

        if not content:

            raise Exception(
                "Content missing"
            )

        if len(
            content.strip()
        ) < self.MIN_CONTENT_LENGTH:

            raise Exception(
                "Generated content too short"
            )

        return True

    # =====================================================
    # ENTERPRISE QUALITY VALIDATION
    # =====================================================

    def validate_quality(
        self,
        scores,
        density_analysis,
    ):

        seo_score = scores.get(
            "seo_score",
            0,
        )

        overall_score = scores.get(
            "overall_score",
            0,
        )

        ai_risk_score = scores.get(
            "ai_risk_score",
            0,
        )

        density = density_analysis.get(
            "density",
            0,
        )

        seo_status = density_analysis.get(
            "seo_status",
            "low",
        )

        semantic_coverage = (

            density_analysis.get(
                "semantic_analysis",
                {}
            ).get(
                "semantic_coverage",
                0
            )
        )

        keyword_count = (
            density_analysis.get(
                "keyword_count",
                0
            )
        )

        word_count = (
            density_analysis.get(
                "total_words",
                0
            )
        )

        # =============================================
        # ENTERPRISE SEMANTIC-FIRST VALIDATION
        # =============================================

        if (

            semantic_coverage >= 80

            and

            word_count >= 800

        ):

            logger.info(

                "Semantic SEO validation passed."
            )

            return True

        # =============================================
        # RELAXED SEO VALIDATION
        # =============================================

        if seo_score < self.MIN_SEO_SCORE:

            logger.warning(

                f"Low SEO score accepted: "
                f"{seo_score}"
            )

        if overall_score < self.MIN_OVERALL_SCORE:

            logger.warning(

                f"Low overall score accepted: "
                f"{overall_score}"
            )

        # =============================================
        # ONLY BLOCK CRITICAL AI RISK
        # =============================================

        if ai_risk_score > self.MAX_AI_RISK_SCORE:

            raise Exception(
                "AI risk score too high"
            )

        # =============================================
        # ONLY BLOCK ACTUAL STUFFING
        # =============================================

        if seo_status == "keyword_stuffing":

            raise Exception(
                "Keyword stuffing detected"
            )

        # =============================================
        # RELAXED DENSITY LOGIC
        # =============================================

        if (

            density < 0.05

            and

            semantic_coverage < 40

            and

            keyword_count < 2

        ):

            logger.warning(

                "Low keyword density accepted."
            )

        # =============================================
        # LONG-FORM SEO PASS
        # =============================================

        if (

            word_count > 1200

            and

            semantic_coverage >= 70

        ):

            logger.info(

                "Long-form semantic SEO passed."
            )

        return True

    # =====================================================
    # SEO TITLE
    # =====================================================

    def seo_title(
        self,
        keyword,
    ):

        return (
            f"Complete Guide About "
            f"{keyword}"
        )

    # =====================================================
    # META DESCRIPTION
    # =====================================================

    def meta_description(
        self,
        keyword,
    ):

        return (

            f"Learn everything about "
            f"{keyword} including "
            f"tips, strategies, "
            f"benefits, examples, "
            f"and expert guidance."
        )

    # =====================================================
    # EXTRACT NUMERIC SCORE
    # =====================================================

    def extract_numeric_score(
        self,
        score_data,
    ):

        if isinstance(
            score_data,
            dict,
        ):

            return float(

                score_data.get(
                    "overall_score",
                    0
                )
            )

        try:

            return float(
                score_data
            )

        except Exception:

            return 0.0

    # =====================================================
    # GENERATE
    # =====================================================

    def generate(
        self,
        keyword_data,
    ):

        """
        Enterprise orchestration pipeline.
        """

        start_time = time.time()

        # =========================================
        # FEATURE CHECK
        # =========================================

        if not FeatureService.is_enabled(
            "generator_enabled"
        ):

            logger.warning(
                "Generator disabled."
            )

            return {

                "success": False,

                "error": (
                    "Generator disabled"
                ),
            }

        keyword = (
            self.normalize_keyword(

                keyword_data.get(
                    "keyword"
                )
            )
        )

        if not keyword:

            raise Exception(
                "Keyword required"
            )

        if not self.safe_text(
            keyword
        ):

            raise Exception(
                "Unsafe keyword detected"
            )

        logger.info(

            f"GENERATOR STARTED: "
            f"{keyword}"
        )

        # =========================================
        # SEO DATA REUSE
        # =========================================

        existing_seo_data = (
            keyword_data.get(
                "seo_data"
            )
        )

        if existing_seo_data:

            logger.info(
                "Using existing SEO data."
            )

            keyword_data.update({

                "search_intent": (

                    existing_seo_data.get(
                        "intent",
                        "informational"
                    )
                ),
            })

        # =========================================
        # FALLBACK SEO ANALYSIS
        # =========================================

        else:

            logger.warning(

                "SEO data missing. "
                "Running fallback analysis."
            )

            try:

                seo_data = (

                    self.keyword_engine
                    .analyze_keyword(
                        keyword
                    )
                )

                keyword_data.update({

                    "seo_data":
                    seo_data,

                    "search_intent": (

                        seo_data.get(
                            "intent",
                            "informational"
                        )
                    ),
                })

            except Exception as error:

                logger.warning(

                    f"SEO analysis failed: "
                    f"{str(error)}"
                )

        # =========================================
        # CONFIG
        # =========================================

        config = self.active_config()

        if config:

            keyword_data.update({

                "provider": (
                    config.active_provider
                ),

                "model": (
                    config.default_model
                ),

                "temperature": (
                    config.temperature
                ),

                "max_tokens": (
                    config.max_tokens
                ),

                "tone": (
                    config.tone
                ),

                "content_type": (
                    config.content_type
                ),

                "target_word_count": (
                    config.target_word_count
                ),
            })

        # =========================================
        # GENERATION LOOP
        # =========================================

        last_error = None

        generated_response = None

        for attempt in range(
            self.MAX_RETRIES
        ):

            try:

                logger.info(

                    f"Generation attempt: "
                    f"{attempt + 1}"
                )

                orchestration_result = (

                    self.orchestrator.execute(
                        keyword_data
                    )
                )

                if not orchestration_result.get(
                    "success",
                    False,
                ):

                    raise Exception(

                        orchestration_result.get(
                            "error",
                            "Unknown orchestration error",
                        )
                    )

                content = (

                    orchestration_result.get(
                        "content",
                        ""
                    )
                )

                cleaned_content = (

                    self.cleaner.clean(
                        content
                    )
                )

                cleaned_content = (

                    ContentFormatter.clean_markdown(
                        cleaned_content
                    )
                )

                html_content = (

                    ContentFormatter.to_html(
                        cleaned_content
                    )
                )

                quality_breakdown = (

                    self.scorer.score(
                        cleaned_content
                    )
                )

                density_analysis = (

                    self.density_processor
                    .analyze(

                        cleaned_content,

                        keyword,
                    )
                )

                # =====================================
                # OPTIMIZED VALIDATION
                # =====================================

                self.validate_quality(

                    quality_breakdown,

                    density_analysis,
                )

                seo_score = (

                    self.extract_numeric_score(
                        quality_breakdown
                    )
                )

                generated_response = {

                    "success": True,

                    "keyword": keyword,

                    "title": (
                        self.seo_title(
                            keyword
                        )
                    ),

                    "meta_description": (

                        self.meta_description(
                            keyword
                        )
                    ),

                    "content": (
                        cleaned_content
                    ),

                    "content_html": (
                        html_content
                    ),

                    "seo_score": (
                        seo_score
                    ),

                    "quality_breakdown": (
                        quality_breakdown
                    ),

                    "density_analysis": (
                        density_analysis
                    ),

                    "verified": True,

                    "engine_metadata": {

                        "engine":
                        "generator_engine",

                        "version":
                        "8.0.0",

                        "provider": (

                            orchestration_result.get(
                                "provider",
                                "unknown",
                            )
                        ),

                        "execution_time": round(

                            time.time()
                            - start_time,

                            2,
                        ),

                        "attempts": (
                            attempt + 1
                        ),
                    },
                }

                self.validate_response(
                    generated_response
                )

                logger.info(
                    "Generation successful."
                )

                break

            except Exception as error:

                last_error = error

                logger.warning(

                    f"Generation failed: "
                    f"{str(error)}"
                )

                # =====================================
                # NO BLOCKING SLEEP
                # =====================================

                continue

        # =========================================
        # FINAL FAILURE
        # =========================================

        if not generated_response:

            try:

                EngineExecution.objects.create(

                    engine_name=(
                        "generator_engine"
                    ),

                    keyword=keyword,

                    provider="unknown",

                    model_name="unknown",

                    execution_time=round(

                        time.time()
                        - start_time,

                        2,
                    ),

                    score=0,

                    status="failed",

                    error_message=str(
                        last_error
                    ),
                )

            except Exception:

                logger.exception(
                    "Monitoring save failed."
                )

            raise Exception(

                f"Generation failed: "
                f"{str(last_error)}"
            )

        # =========================================
        # SUCCESS MONITORING
        # =========================================

        try:

            EngineExecution.objects.create(

                engine_name=(
                    "generator_engine"
                ),

                keyword=keyword,

                provider=(

                    generated_response[
                        "engine_metadata"
                    ][
                        "provider"
                    ]
                ),

                model_name="orchestrated",

                execution_time=(

                    generated_response[
                        "engine_metadata"
                    ][
                        "execution_time"
                    ]
                ),

                score=float(

                    generated_response.get(
                        "seo_score",
                        0
                    )
                ),

                status="success",
            )

        except Exception:

            logger.exception(
                "Success monitoring failed."
            )

        logger.info(

            f"GENERATOR COMPLETED: "
            f"{keyword}"
        )

        return generated_response