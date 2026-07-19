"""
Enterprise AI Orchestration Pipeline
Production Safe Edition
"""

from __future__ import annotations

import asyncio
import logging
import time

from apps.decision_engine.decision import (
    DecisionEngine,
)

from apps.generator.intelligent_generator import (
    IntelligentGenerator,
)

from apps.generator.response_cleaner import (
    ResponseCleaner,
)

from apps.generator.content_scorer import (
    ContentScorer,
)

from apps.keywords.processors.density import (
    KeywordDensityProcessor,
)

from apps.monitoring.models import (
    EngineExecution,
)

from apps.decision_engine.models import (
    DecisionLog,
)

logger = logging.getLogger(
    __name__
)


class OrchestrationService:

    """
    Enterprise orchestration pipeline.
    """

    MAX_RETRIES = 2

    MIN_QUALITY_SCORE = 60

    MAX_AI_RISK_SCORE = 45

    # =============================================
    # INIT
    # =============================================

    def __init__(
        self
    ):

        self.decision_engine = (
            DecisionEngine()
        )

        self.generator = (
            IntelligentGenerator()
        )

        self.cleaner = (
            ResponseCleaner()
        )

        self.scorer = (
            ContentScorer()
        )

        self.density_processor = (
            KeywordDensityProcessor()
        )

    # =============================================
    # ASYNC WRAPPER
    # =============================================

    def run_generation(
        self,
        payload,
    ):

        try:

            return self.generator.generate(
                payload
            )

        except RuntimeError:

            loop = asyncio.new_event_loop()

            asyncio.set_event_loop(
                loop
            )

            try:

                result = (
                    loop.run_until_complete(

                        self.generator.generate(
                            payload
                        )
                    )
                )

            finally:

                loop.close()

            return result

    # =============================================
    # SAFE SCORE EXTRACTION
    # =============================================

    def extract_quality_score(
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
                    0,
                )
            )

        try:

            return float(
                score_data
            )

        except Exception:

            return 0.0

    # =============================================
    # VALIDATE CONTENT
    # =============================================

    def validate_content(
        self,
        keyword,
        content,
        score_data,
    ):

        if not content:

            raise Exception(
                "Generated content empty"
            )

        if len(content.split()) < 100:

            raise Exception(
                "Generated content too short"
            )

        overall_score = (

            score_data.get(
                "overall_score",
                0,
            )
        )

        ai_risk_score = (

            score_data.get(
                "ai_risk_score",
                0,
            )
        )

        if (

            overall_score
            < self.MIN_QUALITY_SCORE
        ):

            raise Exception(
                "Content quality too low"
            )

        if (

            ai_risk_score
            > self.MAX_AI_RISK_SCORE
        ):

            raise Exception(
                "AI risk too high"
            )

        density_analysis = (

            self.density_processor
            .analyze(

                content,

                keyword,
            )
        )

        if (

            density_analysis.get(
                "seo_status"
            )
            == "keyword_stuffing"
        ):

            raise Exception(
                "Keyword stuffing detected"
            )

        return density_analysis

    # =============================================
    # CLEAN CONTENT
    # =============================================

    def clean_content(
        self,
        content,
    ):

        cleaned = (
            self.cleaner.clean(
                content
            )
        )

        return cleaned.strip()

    # =============================================
    # UPDATE ANALYTICS
    # =============================================

    def update_decision_log(
        self,
        keyword,
        ai_quality_score,
        execution_time,
    ):

        try:

            latest_log = (

                DecisionLog.objects.filter(
                    keyword=keyword
                )

                .order_by(
                    "-created_at"
                )

                .first()
            )

            if latest_log:

                latest_log.ai_quality_score = (
                    ai_quality_score
                )

                latest_log.response_time = (
                    execution_time
                )

                latest_log.provider_latency = (
                    execution_time
                )

                latest_log.generation_success = True

                latest_log.save()

        except Exception:

            logger.exception(
                "Decision log update failed."
            )

    # =============================================
    # MONITORING SUCCESS
    # =============================================

    def monitoring_success(
        self,
        keyword,
        provider,
        execution_time,
        score,
    ):

        try:

            EngineExecution.objects.create(

                engine_name=(
                    "orchestration_engine"
                ),

                keyword=keyword,

                provider=provider,

                model_name="orchestrator",

                execution_time=(
                    execution_time
                ),

                score=score,

                status="success",
            )

        except Exception:

            logger.exception(
                "Monitoring success save failed."
            )

    # =============================================
    # MONITORING FAILURE
    # =============================================

    def monitoring_failure(
        self,
        keyword,
        execution_time,
        error,
    ):

        try:

            EngineExecution.objects.create(

                engine_name=(
                    "orchestration_engine"
                ),

                keyword=keyword,

                provider="unknown",

                model_name="orchestrator",

                execution_time=(
                    execution_time
                ),

                score=0,

                status="failed",

                error_message=str(error),
            )

        except Exception:

            logger.exception(
                "Monitoring failure save failed."
            )

    # =============================================
    # SHOULD STOP RETRY
    # =============================================

    def should_stop_retry(
        self,
        error,
    ):

        error_text = str(
            error
        ).lower()

        fatal_patterns = [

            "all providers failed",

            "quota",

            "cooldown",

            "resource_exhausted",

            "rate limit",

            "429",

            "provider unavailable",
        ]

        for pattern in fatal_patterns:

            if pattern in error_text:

                return True

        return False

    # =============================================
    # EXECUTE
    # =============================================

    def execute(
        self,
        payload,
    ):

        """
        Execute enterprise orchestration workflow.
        """

        start_time = time.time()

        keyword = str(

            payload.get(
                "keyword",
                "",
            )
        )

        logger.info(

            f"ORCHESTRATION STARTED: "
            f"{keyword}"
        )

        last_error = None

        for attempt in range(
            self.MAX_RETRIES
        ):

            try:

                logger.info(

                    f"Orchestration attempt "
                    f"{attempt + 1}"
                )

                # =================================
                # DECISION ENGINE
                # =================================

                decision_result = (

                    self.decision_engine
                    .execute(
                        payload
                    )
                )

                if not decision_result.get(
                    "success",
                    False,
                ):

                    raise Exception(
                        "Decision engine failed"
                    )

                decision_data = (
                    decision_result.get(
                        "decision",
                        {}
                    )
                )

                recommended_provider = (

                    decision_data.get(
                        "decision",
                        {}
                    ).get(
                        "recommended_provider",
                        "ollama",
                    )
                )

                # =================================
                # PROVIDER INJECTION
                # =================================

                payload.setdefault(

                    "provider",

                    recommended_provider,
                )

                logger.info(

                    f"Recommended provider: "
                    f"{recommended_provider}"
                )

                # =================================
                # GENERATION
                # =================================

                generation_result = (

                    self.run_generation(
                        payload
                    )
                )

                if not isinstance(
                    generation_result,
                    dict,
                ):

                    raise Exception(
                        "Invalid generation response"
                    )

                if not generation_result.get(
                    "success",
                    False,
                ):

                    raise Exception(

                        generation_result.get(
                            "error",
                            "Generation failed",
                        )
                    )

                raw_content = (

                    generation_result.get(
                        "content",
                        ""
                    )
                )

                provider_used = (

                    generation_result.get(
                        "provider",
                        recommended_provider,
                    )
                )

                # =================================
                # CLEAN CONTENT
                # =================================

                cleaned_content = (
                    self.clean_content(
                        raw_content
                    )
                )

                # =================================
                # QUALITY SCORING
                # =================================

                content_score = (

                    self.scorer.score(
                        cleaned_content
                    )
                )

                ai_quality_score = (

                    self.extract_quality_score(
                        content_score
                    )
                )

                # =================================
                # VALIDATION
                # =================================

                density_analysis = (

                    self.validate_content(

                        keyword,

                        cleaned_content,

                        content_score,
                    )
                )

                execution_time = round(

                    time.time()
                    - start_time,

                    4,
                )

                # =================================
                # ANALYTICS
                # =================================

                self.update_decision_log(

                    keyword,

                    ai_quality_score,

                    execution_time,
                )

                # =================================
                # MONITORING
                # =================================

                self.monitoring_success(

                    keyword,

                    provider_used,

                    execution_time,

                    ai_quality_score,
                )

                logger.info(

                    f"ORCHESTRATION COMPLETE | "
                    f"provider={provider_used} | "
                    f"time={execution_time}s"
                )

                # =================================
                # FINAL RESPONSE
                # =================================

                return {

                    "success": True,

                    "keyword": keyword,

                    "provider": provider_used,

                    "content": (
                        cleaned_content
                    ),

                    "content_score": (
                        ai_quality_score
                    ),

                    "quality_breakdown": (
                        content_score
                    ),

                    "density_analysis": (
                        density_analysis
                    ),

                    "decision": (
                        decision_result
                    ),

                    "execution_time": (
                        execution_time
                    ),

                    "attempts": (
                        attempt + 1
                    ),
                }

            except Exception as error:

                last_error = error

                logger.exception(

                    f"Orchestration failed: "
                    f"{str(error)}"
                )

                # =================================
                # STOP RETRY STORM
                # =================================

                if self.should_stop_retry(
                    error
                ):

                    logger.warning(

                        "Stopping retries due "
                        "to provider exhaustion."
                    )

                    break

                time.sleep(
                    1 + attempt
                )

        # =========================================
        # FINAL FAILURE
        # =========================================

        execution_time = round(

            time.time()
            - start_time,

            4,
        )

        self.monitoring_failure(

            keyword,

            execution_time,

            last_error,
        )

        return {

            "success": False,

            "error": str(
                last_error
            ),

            "execution_time": (
                execution_time
            ),
        }
