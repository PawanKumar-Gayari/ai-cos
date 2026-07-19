"""
Enterprise Async AI Generation Tasks
------------------------------------

Production-grade async orchestration tasks.

Optimized Features:
- duplicate SEO analysis prevention
- async-safe orchestration
- lower CPU usage
- reduced embedding inference
- production-safe retries
- monitoring integration
- scalable Celery execution
- OCI optimized workload
- lightweight generation flow
"""

from __future__ import annotations

import logging
import time
import traceback

from celery import shared_task

from apps.dashboard.services.feature_service import (
    FeatureService,
)

from apps.history.models import (
    GenerationHistory,
)

from apps.generator.engine import (
    GeneratorEngine,
)

from apps.monitoring.models import (
    EngineExecution,
)

from apps.decision_engine.models import (
    DecisionLog,
)

from apps.keywords.engine import (
    KeywordEngine,
)


logger = logging.getLogger(
    __name__
)


# =====================================================
# TASK CONFIG
# =====================================================

class TaskConfig:

    MAX_RETRIES = 3

    RETRY_DELAY = 10

    SOFT_TIME_LIMIT = 300

    HARD_TIME_LIMIT = 360

    MAX_CONTENT_LENGTH = 50000

    DEFAULT_WORD_COUNT = 2000


# =====================================================
# SAFE CONTENT
# =====================================================

def safe_content(content):

    if content is None:

        return ""

    return str(content)[
        :TaskConfig.MAX_CONTENT_LENGTH
    ]


# =====================================================
# SAVE HISTORY
# =====================================================

def save_history(

    task_id,

    task_type,

    query,

    provider,

    content,

    status,
):

    try:

        GenerationHistory.objects.create(

            task_id=task_id,

            task_type=task_type,

            query=str(query)[:1000],

            generated_content=(
                safe_content(content)
            ),

            provider=provider,

            status=status,
        )

    except Exception as error:

        logger.exception(
            "History save failed | error=%s",
            str(error),
        )


# =====================================================
# SAVE FAILURE ANALYTICS
# =====================================================

def save_failure_analytics(

    query,

    error_message,

    execution_time,
):

    try:

        DecisionLog.objects.create(

            keyword=query,

            provider="unknown",

            model_name="unknown",

            seo_score=0,

            competition_score=0,

            quality_score=0,

            publish_score=0,

            ai_quality_score=0,

            should_generate=False,

            rewrite_required=False,

            generation_success=False,

            execution_time=execution_time,

            response_time=execution_time,

            provider_latency=execution_time,

            token_usage=0,

            estimated_cost=0,

            status="failed",

            error_message=error_message,
        )

    except Exception as error:

        logger.exception(
            "Decision analytics failed | error=%s",
            str(error),
        )


# =====================================================
# PREPARE PAYLOAD
# =====================================================

def prepare_payload(

    query,

    seo_data=None,
):

    """
    Prepare optimized generation payload.
    """

    # =============================================
    # USE EXISTING SEO DATA
    # =============================================

    if seo_data:

        logger.info(
            "Using existing SEO data."
        )

        final_seo_data = {

            "primary_keyword":
            seo_data.get(
                "primary_keyword",
                query
            ),

            "secondary_keywords":
            seo_data.get(
                "secondary_keywords",
                []
            ),

            "semantic_keywords":
            seo_data.get(
                "semantic_keywords",
                []
            ),

            "entities":
            seo_data.get(
                "entities",
                []
            ),

            "intent":
            seo_data.get(
                "intent",
                "informational"
            ),
        }

        suggestions = (
            final_seo_data[
                "secondary_keywords"
            ]
        )

    # =============================================
    # FALLBACK SEO ANALYSIS
    # =============================================

    else:

        logger.warning(
            "SEO data missing. "
            "Running fallback keyword analysis."
        )

        keyword_engine = (
            KeywordEngine()
        )

        engine_seo_data = (
            keyword_engine
            .analyze_keyword(
                query
            )
        )

        suggestions = (
            engine_seo_data.get(
                "suggestions",
                []
            )
        )

        final_seo_data = {

            "primary_keyword":
            query,

            "secondary_keywords":
            suggestions[1:10],

            "semantic_keywords":
            engine_seo_data.get(
                "semantic_keywords",
                []
            ),

            "entities":
            engine_seo_data.get(
                "entities",
                []
            ),

            "intent":
            engine_seo_data.get(
                "intent",
                "informational"
            ),
        }

    logger.info(
        "SEO DATA READY | %s",
        str(final_seo_data),
    )

    return {

        "keyword": query,

        "seo_keywords": (
            suggestions[:15]
        ),

        "secondary_keywords": (
            final_seo_data[
                "secondary_keywords"
            ]
        ),

        "semantic_keywords": (
            final_seo_data[
                "semantic_keywords"
            ]
        ),

        "entities": (
            final_seo_data[
                "entities"
            ]
        ),

        "search_intent": (
            final_seo_data[
                "intent"
            ]
        ),

        "content_type": "article",

        "tone": "humanized",

        "target_word_count": (
            TaskConfig.DEFAULT_WORD_COUNT
        ),

        "seo_data": final_seo_data,
    }


# =====================================================
# SAVE MONITORING
# =====================================================

def save_monitoring(

    query,

    provider,

    execution_time,

    score,

    status,

    error_message="",
):

    try:

        EngineExecution.objects.create(

            engine_name=(
                "generation_task"
            ),

            keyword=query,

            provider=provider,

            model_name="async_worker",

            execution_time=(
                execution_time
            ),

            score=score,

            status=status,

            error_message=(
                error_message
            ),
        )

    except Exception as error:

        logger.exception(
            "Monitoring save failed | error=%s",
            str(error),
        )


# =====================================================
# ARTICLE TASK
# =====================================================

@shared_task(
    bind=True,
    max_retries=TaskConfig.MAX_RETRIES,
    default_retry_delay=(
        TaskConfig.RETRY_DELAY
    ),
    soft_time_limit=(
        TaskConfig.SOFT_TIME_LIMIT
    ),
    time_limit=(
        TaskConfig.HARD_TIME_LIMIT
    ),
)
def generate_article_task(

    self,

    query,

    session_id=None,

    seo_data=None,
):

    """
    Enterprise async orchestration task.
    """

    start_time = time.time()

    logger.info(
        "ASYNC GENERATION STARTED | query=%s",
        query,
    )

    self.update_state(

        state="STARTED",

        meta={

            "progress": 5,

            "stage": "initializing",

            "query": str(query),
        },
    )

    if not FeatureService.is_enabled(
        "generator_enabled"
    ):

        raise RuntimeError(
            "Generator disabled."
        )

    try:

        # =============================================
        # PAYLOAD
        # =============================================

        self.update_state(

            state="PROGRESS",

            meta={

                "progress": 20,

                "stage": "payload_preparation",
            },
        )

        payload = prepare_payload(

            query,

            seo_data,
        )

        logger.info(
            "PAYLOAD READY | keyword=%s",
            query,
        )

        # =============================================
        # CONTENT GENERATION
        # =============================================

        self.update_state(

            state="PROGRESS",

            meta={

                "progress": 45,

                "stage": "content_generation",
            },
        )

        logger.info(
            "GENERATOR ENGINE STARTED | query=%s",
            query,
        )

        engine = GeneratorEngine()

        result = engine.generate(
            payload
        )

        logger.info(
            "GENERATOR ENGINE COMPLETED | query=%s",
            query,
        )

        # =============================================
        # VALIDATION
        # =============================================

        if not isinstance(
            result,
            dict,
        ):

            raise RuntimeError(
                "Generator engine returned invalid response."
            )

        content = result.get(
            "content",
            ""
        )

        if not content:

            raise RuntimeError(
                "Generated content is empty."
            )

        execution_time = round(

            time.time()
            - start_time,

            2,
        )

        provider = (

            result.get(
                "engine_metadata",
                {}
            ).get(
                "provider",
                "unknown",
            )
        )

        seo_score = result.get(
            "seo_score",
            0,
        )

        logger.info(
            "ARTICLE GENERATED SUCCESSFULLY | query=%s | seo_score=%s",
            query,
            seo_score,
        )

        # =============================================
        # FINALIZING
        # =============================================

        self.update_state(

            state="PROGRESS",

            meta={

                "progress": 90,

                "stage": "finalizing",
            },
        )

        save_history(

            task_id=self.request.id,

            task_type="article",

            query=query,

            provider=provider,

            content=content,

            status="completed",
        )

        save_monitoring(

            query=query,

            provider=provider,

            execution_time=(
                execution_time
            ),

            score=seo_score,

            status="success",
        )

        logger.info(
            "ASYNC GENERATION COMPLETE | query=%s",
            query,
        )

        return {

            "success": True,

            "task": "article",

            "query": query,

            "provider": provider,

            "execution_time": (
                execution_time
            ),

            "seo_score": (
                seo_score
            ),

            "seo_data": (
                payload[
                    "seo_data"
                ]
            ),

            "result": result,

            "meta": {

                "progress": 100,

                "stage": "completed",
            },
        }

    except Exception as error:

        execution_time = round(

            time.time()
            - start_time,

            2,
        )

        logger.exception(
            "ASYNC GENERATION FAILED | query=%s | error=%s",
            query,
            str(error),
        )

        save_history(

            task_id=self.request.id,

            task_type="article",

            query=query,

            provider="unknown",

            content=traceback.format_exc(),

            status="failed",
        )

        save_failure_analytics(

            query=query,

            error_message=str(error),

            execution_time=(
                execution_time
            ),
        )

        save_monitoring(

            query=query,

            provider="unknown",

            execution_time=(
                execution_time
            ),

            score=0,

            status="failed",

            error_message=str(error),
        )

        if self.request.retries < (
            TaskConfig.MAX_RETRIES
        ):

            logger.warning(
                "Retrying task | query=%s | retry=%s",
                query,
                self.request.retries + 1,
            )

            raise self.retry(
                exc=error
            )

        logger.error(
            "MAX RETRIES EXCEEDED | query=%s",
            query,
        )

        raise RuntimeError(
            str(error)
        ) from error


# =====================================================
# OUTLINE TASK
# =====================================================

@shared_task
def generate_outline_task(

    topic,

    session_id=None,
):

    return {

        "success": True,

        "task": "outline",

        "topic": topic,

        "message": (
            "Outline orchestration ready."
        ),
    }


# =====================================================
# KEYWORDS TASK
# =====================================================

@shared_task
def generate_keywords_task(

    topic,

    session_id=None,
):

    keyword_engine = (
        KeywordEngine()
    )

    result = (
        keyword_engine.analyze_keyword(
            topic
        )
    )

    logger.info(
        "KEYWORD ANALYSIS COMPLETE | topic=%s",
        topic,
    )

    return {

        "success": True,

        "task": "keywords",

        "topic": topic,

        "keywords": result,
    }


# =====================================================
# WORKER HEALTH
# =====================================================

@shared_task
def worker_health():

    logger.info(
        "Worker health check executed."
    )

    return {

        "worker": "healthy",

        "status": "active",
    }