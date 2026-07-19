from django.apps import AppConfig


class DecisionEngineConfig(
    AppConfig
):

    default_auto_field = (
        "django.db.models.BigAutoField"
    )

    name = (
        "apps.decision_engine"
    )

    label = (
        "decision_engine"
    )

    verbose_name = (
        "AI Decision Engine"
    )

    def ready(
        self
    ):

        """
        Initialize decision engine.
        """

        try:

            import apps.decision_engine.services  # noqa

        except Exception:

            pass