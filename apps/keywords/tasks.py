"""
Enterprise SEO Background Tasks v1.1
------------------------------------

Production-grade async SEO processing system.

Version: 1.1

Features:
- Celery async pipeline
- competitor crawling
- SERP processing
- progress tracking
- failure recovery
- dashboard-ready jobs
- OCI optimized
- production-safe
"""

from __future__ import annotations

import logging
import traceback

from celery import shared_task

from django.utils import timezone

from apps.keywords.models import (
    KeywordAnalysis,
    KeywordResearchJob,
)

from apps.keywords.services.pipeline_service import (
    KeywordPipelineService,
)


logger = logging.getLogger(
    __name__
)


# =========================================================
# UPDATE JOB
# =========================================================

def update_job(

    job,

    status=None,

    progress=None,

    result=None,

    error_message=None,
):

    if status:

        job.status = status

    if progress is not None:

        job.progress = progress

    if result is not None:

        job.result = result

    if error_message:

        job.error_message = (
            error_message
        )

    if status == (
        KeywordResearchJob
        .STATUS_RUNNING
    ):

        if not job.started_at:

            job.started_at = (
                timezone.now()
            )

    if status in [

        KeywordResearchJob
        .STATUS_COMPLETED,

        KeywordResearchJob
        .STATUS_FAILED,
    ]:

        job.completed_at = (
            timezone.now()
        )

    job.save()


# =========================================================
# SAVE ANALYSIS
# =========================================================

def save_keyword_analysis(
    pipeline_result,
):

    keyword = pipeline_result.get(
        "keyword",
        ""
    )

    if not keyword:

        return None

    keyword_obj, _ = (

        KeywordAnalysis.objects
        .get_or_create(
            keyword=keyword
        )
    )

    # =====================================================
    # BASIC SEO
    # =====================================================

    keyword_obj.search_intent = (
        pipeline_result.get(
            "intent",
            "informational",
        )
    )

    difficulty = (
        pipeline_result.get(
            "difficulty",
            {}
        )
    )

    if isinstance(
        difficulty,
        dict,
    ):

        keyword_obj.seo_difficulty = (

            difficulty.get(
                "difficulty",
                "medium",
            )
        )

        keyword_obj.search_volume = (

            difficulty.get(
                "volume",
                0,
            )
        )

        keyword_obj.keyword_score = (

            difficulty.get(
                "score",
                0,
            )
        )

    # =====================================================
    # SEO INTELLIGENCE
    # =====================================================

    keyword_obj.related_keywords = (

        pipeline_result.get(
            "suggestions",
            []
        )
    )

    keyword_obj.semantic_keywords = (

        pipeline_result.get(
            "semantic_keywords",
            []
        )
    )

    keyword_obj.entities = (
        pipeline_result.get(
            "entities",
            []
        )
    )

    keyword_obj.people_also_ask = (

        pipeline_result.get(
            "people_also_ask",
            []
        )
    )

    keyword_obj.related_searches = (

        pipeline_result.get(
            "related_searches",
            []
        )
    )

    keyword_obj.competitor_data = (

        pipeline_result.get(
            "competitor_data",
            []
        )
    )

    keyword_obj.recommendation_data = (

        pipeline_result.get(
            "recommendations",
            {}
        )
    )

    keyword_obj.outline_data = (
        pipeline_result.get(
            "outline",
            {}
        )
    )

    keyword_obj.cluster_data = (
        pipeline_result.get(
            "clusters",
            {}
        )
    )

    # =====================================================
    # CONTENT STRATEGY
    # =====================================================

    recommendations = (
        pipeline_result.get(
            "recommendations",
            {}
        )
    )

    if isinstance(
        recommendations,
        dict,
    ):

        keyword_obj.recommended_word_count = (

            recommendations.get(
                "recommended_word_count",
                2500,
            )
        )

    keyword_obj.last_analyzed_at = (
        timezone.now()
    )

    keyword_obj.save()

    return keyword_obj


# =========================================================
# MAIN PIPELINE TASK
# =========================================================

@shared_task(
    bind=True,
    max_retries=3,
    default_retry_delay=60,
)
def run_keyword_pipeline(
    self,
    job_id,
):

    logger.info(

        f"SEO pipeline task started "
        f"| job_id={job_id}"
    )

    try:

        # =================================================
        # FETCH JOB
        # =================================================

        job = (
            KeywordResearchJob.objects
            .get(id=job_id)
        )

        update_job(

            job,

            status=(
                KeywordResearchJob
                .STATUS_RUNNING
            ),

            progress=5,
        )

        # =================================================
        # PIPELINE
        # =================================================

        pipeline = (
            KeywordPipelineService()
        )

        update_job(
            job,
            progress=15,
        )

        # =================================================
        # RUN PIPELINE
        # =================================================

        result = pipeline.run(
            job.keyword
        )

        update_job(
            job,
            progress=70,
        )

        # =================================================
        # SAVE ANALYSIS
        # =================================================

        keyword_obj = (
            save_keyword_analysis(
                result
            )
        )

        update_job(
            job,
            progress=90,
        )

        # =================================================
        # FINAL RESULT
        # =================================================

        final_result = {

            "success": True,

            "version": result.get(
                "version",
                "1.1",
            ),

            "keyword": result.get(
                "keyword",
                "",
            ),

            "keyword_id":

            getattr(
                keyword_obj,
                "id",
                None,
            ),

            "data": result,
        }

        update_job(

            job,

            status=(
                KeywordResearchJob
                .STATUS_COMPLETED
            ),

            progress=100,

            result=final_result,
        )

        logger.info(

            f"SEO pipeline task completed "
            f"| job_id={job_id}"
        )

        return final_result

    # =====================================================
    # RETRY
    # =====================================================

    except Exception as error:

        logger.exception(

            f"SEO pipeline task failed "
            f"| job_id={job_id}"
        )

        try:

            job = (
                KeywordResearchJob.objects
                .get(id=job_id)
            )

            update_job(

                job,

                status=(
                    KeywordResearchJob
                    .STATUS_FAILED
                ),

                progress=100,

                error_message=(
                    str(error)
                ),

                result={

                    "success": False,

                    "error":
                    str(error),

                    "traceback":

                    traceback.format_exc(),
                },
            )

        except Exception:

            logger.exception(
                "Job update failed."
            )

        raise self.retry(
            exc=error
        )


# =========================================================
# HEALTH CHECK TASK
# =========================================================

@shared_task
def seo_pipeline_health_check():

    logger.info(
        "SEO pipeline health check."
    )

    return {

        "status": "healthy",

        "service":
        "seo_pipeline",

        "time":
        str(
            timezone.now()
        ),
    }