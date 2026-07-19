"""
Central rule engine orchestration service.
"""

import logging

from apps.decision_engine.rules.seo_rules import (
    SEORules,
)

from apps.decision_engine.rules.quality_rules import (
    QualityRules,
)

from apps.decision_engine.rules.rewrite_rules import (
    RewriteRules,
)

from apps.decision_engine.rules.publish_rules import (
    PublishRules,
)


logger = logging.getLogger(
    __name__
)


class RuleEngineService:

    """
    Central rule evaluation engine.
    """

    def __init__(
        self
    ):

        self.seo_rules = (
            SEORules()
        )

        self.quality_rules = (
            QualityRules()
        )

        self.rewrite_rules = (
            RewriteRules()
        )

        self.publish_rules = (
            PublishRules()
        )

    # ==================================================
    # MAIN RULE PIPELINE
    # ==================================================

    def evaluate_rules(
        self,
        scores,
    ):

        """
        Evaluate all decision rules.
        """

        seo_score = scores.get(
            "seo_score",
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

        # ==========================================
        # RULE EVALUATION
        # ==========================================

        seo_result = (

            self.seo_rules.evaluate(
                seo_score
            )
        )

        quality_result = (

            self.quality_rules.evaluate(
                quality_score
            )
        )

        rewrite_result = (

            self.rewrite_rules.evaluate(
                quality_score
            )
        )

        publish_result = (

            self.publish_rules.evaluate(
                publish_score
            )
        )

        # ==========================================
        # FINAL RULE OUTPUT
        # ==========================================

        rules = {

            "seo": (
                seo_result
            ),

            "quality": (
                quality_result
            ),

            "rewrite": (
                rewrite_result
            ),

            "publish": (
                publish_result
            ),
        }

        logger.info(
            "Rule engine evaluation completed."
        )

        return rules