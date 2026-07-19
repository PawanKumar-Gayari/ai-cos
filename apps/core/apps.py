from django.apps import AppConfig

import logging
import sys


logger = logging.getLogger(
    __name__
)


class CoreConfig(AppConfig):

    default_auto_field = (
        "django.db.models.BigAutoField"
    )

    name = "apps.core"

    verbose_name = (
        "Core System"
    )

    # ==================================================
    # STARTUP
    # ==================================================

    def ready(
        self
    ):

        try:

            # ==========================================
            # SAFE COMMAND DETECTION
            # ==========================================

            running_commands = (

                " ".join(
                    sys.argv
                ).lower()
            )

            # ==========================================
            # SKIP HEAVY AI PRELOAD
            # ==========================================

            skip_ai_preload = [

                "celery",
                "migrate",
                "makemigrations",
                "collectstatic",
                "shell",
                "check",
                "createsuperuser",
                "test",
            ]

            # ==========================================
            # SKIP FOR LIGHTWEIGHT COMMANDS
            # ==========================================

            if any(

                command in running_commands

                for command in (
                    skip_ai_preload
                )
            ):

                logger.info(

                    "Skipping AI preload "
                    f"for command: "
                    f"{running_commands}"
                )

                return

            # ==========================================
            # AI PRELOAD
            # ==========================================

            from apps.core.model_manager import (
                ModelManager
            )

            logger.info(
                "Starting AI model preload."
            )

            ModelManager.warmup()

            logger.info(
                "AI model preload completed."
            )

        except Exception as error:

            logger.exception(

                f"AI preload failed: "
                f"{str(error)}"
            )