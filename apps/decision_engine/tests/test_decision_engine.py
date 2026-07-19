from django.test import (
    TestCase,
)

from apps.decision_engine.decision import (
    DecisionEngine,
)


class DecisionEngineTestCase(
    TestCase
):

    """
    Decision engine tests.
    """

    def setUp(
        self
    ):

        self.engine = (
            DecisionEngine()
        )

    # ==================================================
    # FULL ENGINE TEST
    # ==================================================

    def test_engine_execution(
        self
    ):

        payload = {

            "keyword": (
                "Best AI tools for students"
            )
        }

        result = (
            self.engine.execute(
                payload
            )
        )

        self.assertTrue(
            result["success"]
        )

        self.assertIn(
            "decision",
            result,
        )

        self.assertIn(
            "planning",
            result,
        )

    # ==================================================
    # SEO SCORE TEST
    # ==================================================

    def test_seo_score_exists(
        self
    ):

        payload = {

            "keyword": (
                "SEO guide for beginners"
            )
        }

        result = (
            self.engine.execute(
                payload
            )
        )

        scores = result[
            "decision"
        ][
            "scores"
        ]

        self.assertGreater(

            scores["seo_score"],

            0,
        )

    # ==================================================
    # PROVIDER SELECTION TEST
    # ==================================================

    def test_provider_selection(
        self
    ):

        payload = {

            "keyword": (
                "AI"
            )
        }

        result = (
            self.engine.execute(
                payload
            )
        )

        provider = result[
            "decision"
        ][
            "decision"
        ][
            "recommended_provider"
        ]

        self.assertIn(

            provider,

            [

                "ollama",

                "openai",

                "gemini",
            ],
        )

    # ==================================================
    # PLANNING TEST
    # ==================================================

    def test_article_plan(
        self
    ):

        payload = {

            "keyword": (
                "How to learn SEO"
            )
        }

        result = (
            self.engine.execute(
                payload
            )
        )

        planning = result[
            "planning"
        ]

        self.assertIn(
            "article_plan",
            planning,
        )

        self.assertIn(
            "publish_plan",
            planning,
        )

        self.assertIn(
            "update_plan",
            planning,
        )