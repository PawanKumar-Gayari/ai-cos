"""
Enterprise AI Decision Engine
-----------------------------

Production-grade orchestration decision engine.

Features:
- intelligent provider selection
- SEO-aware routing
- publish scoring
- rewrite intelligence
- quality-aware planning
- provider optimization
- production-safe orchestration
"""

from __future__ import annotations

import logging
import time

from apps.decision_engine.services.decision_service import (
    DecisionService,
)

from apps.decision_engine.services.planning_service import (
    PlanningService,
)

from apps.decision_engine.services.rule_engine_service import (
    RuleEngineService,
)


logger = logging.getLogger(
    __name__
)


class DecisionEngine:

    """
    Enterprise orchestration decision engine.
    """

    MIN_SEO_SCORE = 45

    MIN_QUALITY_SCORE = 50

    MIN_PUBLISH_SCORE = 50

    # ==================================================
    # INIT
    # ==================================================

    def __init__(
        self
    ):

        self.decision_service = (
            DecisionService()
        )

        self.planning_service = (
            PlanningService()
        )

        self.rule_engine = (
            RuleEngineService()
        )

    # ==================================================
    # SAFE SCORE
    # ==================================================

    def safe_score(
        self,
        value,
        default=0,
    ):

        try:

            return float(value)

        except Exception:

            return float(default)

    # ==================================================
    # PROVIDER SELECTION
    # ==================================================

    def select_provider(
        self,
        scores,
    ):

        seo_score = (
            self.safe_score(

                scores.get(
                    "seo_score",
                    0,
                )
            )
        )

        competition_score = (
            self.safe_score(

                scores.get(
                    "competition_score",
                    0,
                )
            )
        )

        quality_score = (
            self.safe_score(

                scores.get(
                    "quality_score",
                    0,
                )
            )
        )

        # ==============================================
        # PREMIUM SEO
        # ==============================================

        if (

            seo_score >= 80

            or

            quality_score >= 80
        ):

            return "gemini"

        # ==============================================
        # HIGH COMPETITION
        # ==============================================

        if competition_score >= 70:

            return "openai"

        # ==============================================
        # DEFAULT FAST LOCAL
        # ==============================================

        return "ollama"

    # ==================================================
    # PUBLISH DECISION
    # ==================================================

    def publish_decision(
        self,
        scores,
    ):

        seo_score = (
            self.safe_score(

                scores.get(
                    "seo_score",
                    0,
                )
            )
        )

        quality_score = (
            self.safe_score(

                scores.get(
                    "quality_score",
                    0,
                )
            )
        )

        publish_score = (
            self.safe_score(

                scores.get(
                    "publish_score",
                    0,
                )
            )
        )

        if seo_score < self.MIN_SEO_SCORE:

            return False

        if quality_score < (
            self.MIN_QUALITY_SCORE
        ):

            return False

        if publish_score < (
            self.MIN_PUBLISH_SCORE
        ):

            return False

        return True

    # ==================================================
    # REWRITE DECISION
    # ==================================================

    def rewrite_required(
        self,
        scores,
    ):

        ai_quality_score = (
            self.safe_score(

                scores.get(
                    "ai_quality_score",
                    0,
                )
            )
        )

        quality_score = (
            self.safe_score(

                scores.get(
                    "quality_score",
                    0,
                )
            )
        )

        seo_score = (
            self.safe_score(

                scores.get(
                    "seo_score",
                    0,
                )
            )
        )

        if ai_quality_score > 60:

            return True

        if quality_score < 60:

            return True

        if seo_score < 50:

            return True

        return False

    # ==================================================
    # BUILD EXECUTION STRATEGY
    # ==================================================

    def build_strategy(
        self,
        scores,
    ):

        provider = (
            self.select_provider(
                scores
            )
        )

        should_publish = (
            self.publish_decision(
                scores
            )
        )

        rewrite_needed = (
            self.rewrite_required(
                scores
            )
        )

        return {

            "recommended_provider":
            provider,

            "should_publish":
            should_publish,

            "rewrite_required":
            rewrite_needed,

            "priority": (

                "high"

                if should_publish

                else "medium"
            ),
        }

    # ==================================================
    # MAIN EXECUTION
    # ==================================================

    def execute(
        self,
        payload,
    ):

        """
        Execute enterprise AI strategy pipeline.
        """

        started = time.time()

        keyword = payload.get(
            "keyword",
            "",
        )

        logger.info(

            f"Decision engine started "
            f"for keyword: {keyword}"
        )

        try:

            # ==========================================
            # DECISION EVALUATION
            # ==========================================

            decision_result = (

                self.decision_service
                .evaluate(
                    payload
                )
            )

            if not decision_result.get(
                "success",
                False,
            ):

                return {

                    "success": False,

                    "stage": "decision",

                    "error": (
                        decision_result.get(
                            "error"
                        )
                    ),
                }

            # ==========================================
            # SCORES
            # ==========================================

            scores = (
                decision_result.get(
                    "scores",
                    {}
                )
            )

            # ==========================================
            # RULE ENGINE
            # ==========================================

            rules = (

                self.rule_engine
                .evaluate_rules(
                    scores
                )
            )

            # ==========================================
            # STRATEGY
            # ==========================================

            strategy = (
                self.build_strategy(
                    scores
                )
            )

            # ==========================================
            # PLANNING PAYLOAD
            # ==========================================

            planning_payload = {

                **payload,

                "scores": scores,

                "strategy": strategy,
            }

            # ==========================================
            # PLANNING
            # ==========================================

            planning_result = (

                self.planning_service
                .build_plan(
                    planning_payload
                )
            )

            execution_time = round(

                time.time()
                - started,

                3,
            )

            # ==========================================
            # FINAL RESPONSE
            # ==========================================

            response = {

                "success": True,

                "keyword": keyword,

                "decision": {

                    **decision_result,

                    "strategy":
                    strategy,
                },

                "rules": (
                    rules
                ),

                "planning": (
                    planning_result
                ),

                "execution_time": (
                    execution_time
                ),

                "engine_metadata": {

                    "engine": (
                        "decision_engine"
                    ),

                    "version": "6.0.0",

                    "provider": (

                        strategy.get(
                            "recommended_provider"
                        )
                    ),
                },
            }

            logger.info(

                f"Decision engine completed "
                f"for keyword: {keyword}"
            )

            return response

        except Exception as error:

            logger.exception(

                f"Decision engine failed: "
                f"{str(error)}"
            )

            return {

                "success": False,

                "keyword": keyword,

                "error": str(error),

                "stage": "decision_engine",
            }