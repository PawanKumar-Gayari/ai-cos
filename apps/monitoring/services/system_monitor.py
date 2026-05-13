"""
Enterprise system monitoring service.
"""

import os
import time
import logging
import platform

from datetime import datetime

from django.conf import settings
from django.core.cache import cache

from apps.history.models import (
    GenerationHistory
)

from apps.memory.storage.memory_repository import (
    MemoryRepository
)

from apps.llm.router import (
    LLMRouter
)


logger = logging.getLogger(
    __name__
)


class SystemMonitor:

    def __init__(
        self
    ):

        self.memory_repository = (
            MemoryRepository()
        )

        self.router = (
            LLMRouter()
        )

    # ==================================================
    # TIMESTAMP
    # ==================================================

    def timestamp(
        self
    ):

        return (
            datetime.utcnow()
            .isoformat()
        )

    # ==================================================
    # SYSTEM INFO
    # ==================================================

    def system_info(
        self
    ):

        """
        Basic runtime information.
        """

        return {

            "platform": (
                platform.system()
            ),

            "platform_version": (
                platform.version()
            ),

            "python_version": (
                platform.python_version()
            ),

            "hostname": (
                platform.node()
            ),

            "timestamp": (
                self.timestamp()
            ),
        }

    # ==================================================
    # MEMORY METRICS
    # ==================================================

    def memory_metrics(
        self
    ):

        """
        Semantic memory statistics.
        """

        try:

            total_memories = (
                self.memory_repository.count()
            )

            latest_memories = (
                self.memory_repository.latest(
                    limit=5
                )
            )

            return {

                "total_memories": (
                    total_memories
                ),

                "latest_memories": len(
                    latest_memories
                ),
            }

        except Exception as error:

            logger.exception(

                f"Memory metrics failed: "
                f"{str(error)}"
            )

            return {}

    # ==================================================
    # GENERATION METRICS
    # ==================================================

    def generation_metrics(
        self
    ):

        """
        AI generation statistics.
        """

        try:

            total_generations = (
                GenerationHistory.objects.count()
            )

            completed = (

                GenerationHistory.objects.filter(
                    status="completed"
                ).count()
            )

            failed = (

                GenerationHistory.objects.filter(
                    status="failed"
                ).count()
            )

            success_rate = 0

            if total_generations > 0:

                success_rate = round(

                    (
                        completed
                        / total_generations
                    ) * 100,

                    2,
                )

            return {

                "total_generations": (
                    total_generations
                ),

                "completed": completed,

                "failed": failed,

                "success_rate": (
                    success_rate
                ),
            }

        except Exception as error:

            logger.exception(

                f"Generation metrics failed: "
                f"{str(error)}"
            )

            return {}

    # ==================================================
    # PROVIDER HEALTH
    # ==================================================

    def provider_health(
        self
    ):

        """
        AI provider status.
        """

        providers = {}

        try:

            available = (
                self.router.available_models()
            )

            providers[
                "available_models"
            ] = available

            providers[
                "provider_count"
            ] = len(
                available
            )

            providers[
                "healthy"
            ] = len(
                available
            ) > 0

            return providers

        except Exception as error:

            logger.exception(

                f"Provider health failed: "
                f"{str(error)}"
            )

            return {

                "healthy": False
            }

    # ==================================================
    # CACHE METRICS
    # ==================================================

    def cache_metrics(
        self
    ):

        """
        Cache statistics.
        """

        try:

            cache.set(
                "monitor_test",
                "ok",
                timeout=10,
            )

            value = cache.get(
                "monitor_test"
            )

            return {

                "cache_working": (
                    value == "ok"
                ),

                "backend": str(
                    cache.__class__.__name__
                ),
            }

        except Exception as error:

            logger.exception(

                f"Cache metrics failed: "
                f"{str(error)}"
            )

            return {

                "cache_working": False
            }

    # ==================================================
    # ENVIRONMENT INFO
    # ==================================================

    def environment_info(
        self
    ):

        """
        Runtime environment settings.
        """

        return {

            "debug": (
                settings.DEBUG
            ),

            "timezone": (
                settings.TIME_ZONE
            ),

            "redis_enabled": getattr(

                settings,

                "ENABLE_REDIS",

                False,
            ),

            "celery_enabled": getattr(

                settings,

                "ENABLE_CELERY",

                False,
            ),
        }

    # ==================================================
    # FULL SYSTEM REPORT
    # ==================================================

    def full_report(
        self
    ):

        """
        Complete monitoring report.
        """

        start = time.time()

        report = {

            "timestamp": (
                self.timestamp()
            ),

            "system": (
                self.system_info()
            ),

            "memory": (
                self.memory_metrics()
            ),

            "generation": (
                self.generation_metrics()
            ),

            "providers": (
                self.provider_health()
            ),

            "cache": (
                self.cache_metrics()
            ),

            "environment": (
                self.environment_info()
            ),
        }

        report[
            "execution_time"
        ] = round(

            time.time() - start,

            4,
        )

        logger.info(
            "System monitoring report generated."
        )

        return report