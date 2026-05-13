"""
Enterprise async AI generation tasks.
"""

import asyncio
import logging
import traceback

from celery import shared_task
from celery.exceptions import MaxRetriesExceededError

from apps.generator.intelligent_generator import (
    IntelligentGenerator
)

from apps.history.models import (
    GenerationHistory
)


logger = logging.getLogger(
    __name__
)


class TaskConfig:

    MAX_RETRIES = 3

    RETRY_DELAY = 10

    SOFT_TIME_LIMIT = 300

    HARD_TIME_LIMIT = 360

    MAX_CONTENT_LENGTH = 50000


# ==================================================
# SAFE CONTENT
# ==================================================

def safe_content(
    content
):

    """
    Prevent oversized DB payloads.
    """

    if content is None:

        return ""

    content = str(content)

    return content[
        :TaskConfig.MAX_CONTENT_LENGTH
    ]


# ==================================================
# SAVE HISTORY
# ==================================================

def save_history(

    task_id,
    task_type,
    query,
    provider,
    content,
    status,
):

    """
    Persist generation history safely.
    """

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

            f"History save failed: "
            f"{str(error)}"
        )


# ==================================================
# SAFE ASYNC EXECUTION
# ==================================================

def run_async(
    coroutine
):

    """
    Safe async execution wrapper.
    """

    try:

        return asyncio.run(
            coroutine
        )

    except RuntimeError:

        loop = asyncio.new_event_loop()

        asyncio.set_event_loop(
            loop
        )

        return loop.run_until_complete(
            coroutine
        )


# ==================================================
# BASE TASK EXECUTOR
# ==================================================

def execute_generation(

    task_instance,

    task_type,

    query,

    generator_method,
):

    """
    Shared generation execution pipeline.
    """

    logger.info(

        f"Starting {task_type} "
        f"generation for: {query}"
    )

    try:

        generator = (
            IntelligentGenerator()
        )

        result = run_async(
            generator_method(
                generator
            )
        )

        provider = result.get(
            "provider",
            "unknown",
        )

        generated_content = result.get(
            "generated_content",
            "",
        )

        save_history(

            task_id=(
                task_instance.request.id
            ),

            task_type=task_type,

            query=query,

            provider=provider,

            content=generated_content,

            status="completed",
        )

        logger.info(

            f"{task_type} generation "
            f"completed for: {query}"
        )

        return {

            "success": True,

            "task": task_type,

            "query": query,

            "provider": provider,

            "result": result,
        }

    except Exception as error:

        logger.exception(

            f"{task_type} generation failed: "
            f"{str(error)}"
        )

        save_history(

            task_id=(
                task_instance.request.id
            ),

            task_type=task_type,

            query=query,

            provider="hybrid_router",

            content=traceback.format_exc(),

            status="failed",
        )

        try:

            raise task_instance.retry(
                exc=error
            )

        except MaxRetriesExceededError:

            logger.error(

                f"Max retries exceeded "
                f"for {task_type}: {query}"
            )

            return {

                "success": False,

                "task": task_type,

                "query": query,

                "error": str(error),
            }


# ==================================================
# ARTICLE TASK
# ==================================================

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
):

    """
    Async article generation task.
    """

    return execute_generation(

        task_instance=self,

        task_type="article",

        query=query,

        generator_method=lambda generator: (

            generator.generate(

                query=query,

                session_id=session_id,
            )
        ),
    )


# ==================================================
# OUTLINE TASK
# ==================================================

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
def generate_outline_task(

    self,

    topic,

    session_id=None,
):

    """
    Async outline generation task.
    """

    return execute_generation(

        task_instance=self,

        task_type="outline",

        query=topic,

        generator_method=lambda generator: (

            generator.generate_outline(

                topic=topic,

                session_id=session_id,
            )
        ),
    )


# ==================================================
# KEYWORDS TASK
# ==================================================

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
def generate_keywords_task(

    self,

    topic,

    session_id=None,
):

    """
    Async keyword generation task.
    """

    return execute_generation(

        task_instance=self,

        task_type="keywords",

        query=topic,

        generator_method=lambda generator: (

            generator.generate_keywords(

                topic=topic,

                session_id=session_id,
            )
        ),
    )


# ==================================================
# WORKER HEALTH
# ==================================================

@shared_task
def worker_health():

    """
    Celery worker health check.
    """

    logger.info(
        "Worker health check executed."
    )

    return {

        "worker": "healthy",

        "status": "active",
    }