"""
AI planning orchestration service.
"""

import logging

from apps.decision_engine.planner.article_planner import (
    ArticlePlanner,
)

from apps.decision_engine.planner.publish_planner import (
    PublishPlanner,
)

from apps.decision_engine.planner.update_planner import (
    UpdatePlanner,
)


logger = logging.getLogger(
    __name__
)


class PlanningService:

    """
    Central planning orchestration.
    """

    def __init__(
        self
    ):

        self.article_planner = (
            ArticlePlanner()
        )

        self.publish_planner = (
            PublishPlanner()
        )

        self.update_planner = (
            UpdatePlanner()
        )

    # ==================================================
    # MAIN PLANNING PIPELINE
    # ==================================================

    def build_plan(
        self,
        payload,
    ):

        """
        Generate full AI content plan.
        """

        keyword = payload.get(
            "keyword",
            "",
        )

        scores = payload.get(
            "scores",
            {},
        )

        intent = self.detect_intent(
            keyword
        )

        article_type = (
            self.article_type(
                intent
            )
        )

        content_depth = (
            self.content_depth(
                keyword
            )
        )

        estimated_words = (
            self.estimated_words(
                content_depth
            )
        )

        # ==========================================
        # MODULAR PLANNERS
        # ==========================================

        article_plan = (

            self.article_planner.build(

                keyword,

                intent,
            )
        )

        publish_plan = (

            self.publish_planner.build(
                scores
            )
        )

        update_plan = (

            self.update_planner.build(
                keyword
            )
        )

        # ==========================================
        # FINAL PLAN
        # ==========================================

        plan = {

            "keyword": keyword,

            "intent": intent,

            "article_type": (
                article_type
            ),

            "content_depth": (
                content_depth
            ),

            "estimated_words": (
                estimated_words
            ),

            "article_plan": (
                article_plan
            ),

            "publish_plan": (
                publish_plan
            ),

            "update_plan": (
                update_plan
            ),
        }

        logger.info(

            f"Planning completed "
            f"for keyword: {keyword}"
        )

        return plan

    # ==================================================
    # SEARCH INTENT
    # ==================================================

    def detect_intent(
        self,
        keyword,
    ):

        keyword = keyword.lower()

        commercial_terms = [

            "best",

            "top",

            "review",

            "buy",
        ]

        informational_terms = [

            "guide",

            "how",

            "tutorial",

            "what",
        ]

        for term in commercial_terms:

            if term in keyword:

                return "commercial"

        for term in informational_terms:

            if term in keyword:

                return "informational"

        return "general"

    # ==================================================
    # ARTICLE TYPE
    # ==================================================

    def article_type(
        self,
        intent,
    ):

        mapping = {

            "commercial": (
                "listicle"
            ),

            "informational": (
                "guide"
            ),

            "general": (
                "blog"
            ),
        }

        return mapping.get(
            intent,
            "blog",
        )

    # ==================================================
    # CONTENT DEPTH
    # ==================================================

    def content_depth(
        self,
        keyword,
    ):

        keyword_length = len(
            keyword.split()
        )

        if keyword_length >= 5:

            return "high"

        if keyword_length >= 3:

            return "medium"

        return "low"

    # ==================================================
    # WORD ESTIMATION
    # ==================================================

    def estimated_words(
        self,
        content_depth,
    ):

        mapping = {

            "low": 1000,

            "medium": 2000,

            "high": 3500,
        }

        return mapping.get(
            content_depth,
            1500,
        )