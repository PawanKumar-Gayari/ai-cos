"""
Main decision orchestration service.
"""

import logging
import time

from django.db import models

from apps.decision_engine.models import (
    DecisionLog,
)

from apps.decision_engine.services.scoring_service import (
    ScoringService,
)

from apps.monitoring.models import (
    EngineExecution,
)


logger = logging.getLogger(
    __name__
)


class DecisionService:

    """
    Central AI decision engine.
    """

    def __init__(
        self
    ):

        self.scoring_service = (
            ScoringService()
        )

    # ==================================================
    # MAIN DECISION PIPELINE
    # ==================================================

    def evaluate(
        self,
        payload,
    ):

        """
        Evaluate AI generation strategy.
        """

        start_time = time.time()

        keyword = payload.get(
            "keyword",
            "",
        )

        try:

            # ======================================
            # SCORING
            # ======================================

            scores = (

                self.scoring_service
                .calculate_scores(
                    payload
                )
            )

            seo_score = scores.get(
                "seo_score",
                0,
            )

            competition_score = scores.get(
                "competition_score",
                0,
            )

            quality_score = scores.get(
                "quality_score",
                0,
            )

            publish_score = scores.get(
                "publish_score",
                0,
            )

            # ======================================
            # DECISION LOGIC
            # ======================================

            should_generate = (
                seo_score >= 50
            )

            rewrite_required = (
                quality_score < 60
            )

            recommended_provider = (
                self.select_provider(
                    competition_score
                )
            )

            execution_time = round(

                time.time()
                - start_time,

                4,
            )

            # ======================================
            # DECISION OBJECT
            # ======================================

            decision = {

                "success": True,

                "keyword": keyword,

                "scores": scores,

                "decision": {

                    "should_generate": (
                        should_generate
                    ),

                    "rewrite_required": (
                        rewrite_required
                    ),

                    "recommended_provider": (
                        recommended_provider
                    ),
                },
            }

            # ======================================
            # DATABASE ANALYTICS
            # ======================================

            DecisionLog.objects.create(

                keyword=keyword,

                provider=(
                    recommended_provider
                ),

                model_name="router",

                seo_score=seo_score,

                competition_score=(
                    competition_score
                ),

                quality_score=(
                    quality_score
                ),

                publish_score=(
                    publish_score
                ),

                should_generate=(
                    should_generate
                ),

                rewrite_required=(
                    rewrite_required
                ),

                execution_time=(
                    execution_time
                ),

                status="success",
            )

            # ======================================
            # MONITORING
            # ======================================

            EngineExecution.objects.create(

                engine_name=(
                    "decision_engine"
                ),

                keyword=keyword,

                provider=(
                    recommended_provider
                ),

                model_name="router",

                execution_time=(
                    execution_time
                ),

                score=seo_score,

                status="success",
            )

            logger.info(

                f"Decision evaluated "
                f"for keyword: {keyword}"
            )

            return decision

        except Exception as error:

            logger.exception(

                f"Decision engine failed: "
                f"{str(error)}"
            )

            execution_time = round(

                time.time()
                - start_time,

                4,
            )

            # ======================================
            # FAILURE ANALYTICS
            # ======================================

            DecisionLog.objects.create(

                keyword=keyword,

                provider="unknown",

                model_name="unknown",

                seo_score=0,

                competition_score=0,

                quality_score=0,

                publish_score=0,

                should_generate=False,

                rewrite_required=False,

                execution_time=(
                    execution_time
                ),

                status="failed",

                error_message=str(error),
            )

            EngineExecution.objects.create(

                engine_name=(
                    "decision_engine"
                ),

                keyword=keyword,

                provider="unknown",

                model_name="unknown",

                execution_time=(
                    execution_time
                ),

                score=0,

                status="failed",

                error_message=str(error),
            )

            return {

                "success": False,

                "error": str(error),
            }

    # ==================================================
    # ADAPTIVE PROVIDER SELECTION
    # ==================================================

    def select_provider(
        self,
        competition_score,
    ):

        """
        Adaptive provider routing
        based on historical analytics.
        """

        try:

            providers = [

                "gemini",

                "openai",
            ]

            provider_scores = {}

            # ======================================
            # HISTORICAL ANALYTICS
            # ======================================

            for provider in providers:

                history = (

                    DecisionLog.objects.filter(
                        provider=provider,
                        status="success",
                    )
                )

                total = history.count()

                if total == 0:

                    provider_scores[
                        provider
                    ] = 0

                    continue

                avg_publish = (

                    history.aggregate(
                        avg=models.Avg(
                            "publish_score"
                        )
                    )["avg"]
                    or 0
                )

                rewrite_penalty = (

                    history.filter(
                        rewrite_required=True
                    ).count()
                )

                success_bonus = (

                    history.filter(
                        should_generate=True
                    ).count()
                )

                final_score = (

                    avg_publish

                    +

                    success_bonus

                    -

                    rewrite_penalty
                )

                provider_scores[
                    provider
                ] = round(
                    final_score,
                    2,
                )

            # ======================================
            # BEST HISTORICAL PROVIDER
            # ======================================

            best_provider = max(

                provider_scores,

                key=provider_scores.get,
            )

            # ======================================
            # FALLBACK LOGIC
            # ======================================

            if all(

                score == 0

                for score in provider_scores.values()
            ):

                if competition_score >= 80:

                    return "openai"

                if competition_score >= 50:

                    return "gemini"

                return "gemini"


            logger.info(

                f"Adaptive routing selected: "
                f"{best_provider}"
            )

            return best_provider

        except Exception as error:

            logger.exception(

                f"Adaptive routing failed: "
                f"{str(error)}"
            )

            # ======================================
            # SAFE FALLBACK
            # ======================================

            if competition_score >= 80:

                return "openai"

            if competition_score >= 50:

                return "gemini"

            return "gemini"
