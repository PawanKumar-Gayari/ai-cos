"""
Enterprise System Monitoring Service
------------------------------------

Production-grade infrastructure monitoring.

Features:
- OCI resource monitoring
- AI provider analytics
- Redis/Celery detection
- generation analytics
- cache monitoring
- infrastructure health
- dashboard-safe metrics
- production-safe observability
"""

from __future__ import annotations

import logging
import platform
import socket
import time

from datetime import datetime

import psutil

from django.conf import settings

from django.core.cache import cache

from apps.history.models import (
    GenerationHistory,
)

from apps.memory.storage.memory_repository import (
    MemoryRepository,
)

from apps.llm.router import (
    LLMRouter,
)


logger = logging.getLogger(
    __name__
)


# =====================================================
# SYSTEM MONITOR
# =====================================================

class SystemMonitor:

    """
    Enterprise infrastructure monitor.
    """

    CACHE_TIMEOUT = 30

    # =================================================
    # INIT
    # =================================================

    def __init__(
        self
    ):

        self.memory_repository = (
            MemoryRepository()
        )

        self.router = (
            LLMRouter()
        )

    # =================================================
    # TIMESTAMP
    # =================================================

    def timestamp(
        self
    ):

        return (

            datetime.utcnow()
            .isoformat()
        )

    # =================================================
    # SYSTEM INFO
    # =================================================

    def system_info(
        self
    ):

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

    # =================================================
    # RESOURCE METRICS
    # =================================================

    def resource_metrics(
        self
    ):

        try:

            memory = (
                psutil.virtual_memory()
            )

            disk = (
                psutil.disk_usage("/")
            )

            cpu_percent = (
                psutil.cpu_percent(
                    interval=1
                )
            )

            load_avg = (0, 0, 0)

            try:

                load_avg = (
                    psutil.getloadavg()
                )

            except Exception:

                pass

            return {

                "cpu_percent": (
                    cpu_percent
                ),

                "cpu_count": (
                    psutil.cpu_count()
                ),

                "load_average": {

                    "1min": (
                        load_avg[0]
                    ),

                    "5min": (
                        load_avg[1]
                    ),

                    "15min": (
                        load_avg[2]
                    ),
                },

                "memory_percent": (
                    memory.percent
                ),

                "memory_used_gb": round(

                    memory.used / (
                        1024 ** 3
                    ),

                    2,
                ),

                "memory_total_gb": round(

                    memory.total / (
                        1024 ** 3
                    ),

                    2,
                ),

                "disk_percent": (
                    disk.percent
                ),

                "disk_used_gb": round(

                    disk.used / (
                        1024 ** 3
                    ),

                    2,
                ),

                "disk_total_gb": round(

                    disk.total / (
                        1024 ** 3
                    ),

                    2,
                ),

                "uptime_hours": round(

                    (
                        time.time()
                        - psutil.boot_time()
                    ) / 3600,

                    2,
                ),
            }

        except Exception as error:

            logger.exception(

                f"Resource metrics failed: "
                f"{str(error)}"
            )

            return {}

    # =================================================
    # MEMORY METRICS
    # =================================================

    def memory_metrics(
        self
    ):

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

    # =================================================
    # GENERATION METRICS
    # =================================================

    def generation_metrics(
        self
    ):

        try:

            total = (
                GenerationHistory
                .objects
                .count()
            )

            completed = (

                GenerationHistory
                .objects
                .filter(
                    status="completed"
                )
                .count()
            )

            failed = (

                GenerationHistory
                .objects
                .filter(
                    status="failed"
                )
                .count()
            )

            pending = (

                GenerationHistory
                .objects
                .filter(
                    status="pending"
                )
                .count()
            )

            success_rate = 0

            if total > 0:

                success_rate = round(

                    (
                        completed
                        / total
                    ) * 100,

                    2,
                )

            return {

                "total_generations":
                total,

                "completed":
                completed,

                "failed":
                failed,

                "pending":
                pending,

                "success_rate":
                success_rate,
            }

        except Exception as error:

            logger.exception(

                f"Generation metrics failed: "
                f"{str(error)}"
            )

            return {}

    # =================================================
    # PROVIDER HEALTH
    # =================================================

    def provider_health(
        self
    ):

        try:

            router_status = (
                self.router
                .router_status()
            )

            providers = (
                router_status.get(
                    "provider_health",
                    {}
                )
            )

            healthy_count = sum(

                1

                for item in providers.values()

                if (

                    item.get(
                        "failures",
                        0
                    ) < 5
                )
            )

            return {

                "healthy": (
                    healthy_count > 0
                ),

                "provider_count": len(
                    providers
                ),

                "healthy_providers": (
                    healthy_count
                ),

                "providers": providers,
            }

        except Exception as error:

            logger.exception(

                f"Provider health failed: "
                f"{str(error)}"
            )

            return {

                "healthy": False,

                "providers": {},
            }

    # =================================================
    # CACHE METRICS
    # =================================================

    def cache_metrics(
        self
    ):

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

    # =================================================
    # ENVIRONMENT
    # =================================================

    def environment_info(
        self
    ):

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

    # =================================================
    # SERVICE STATUS
    # =================================================

    def service_status(
        self
    ):

        try:

            redis_online = False

            celery_online = False

            # =====================================
            # REDIS
            # =====================================

            for connection in (

                psutil.net_connections()
            ):

                try:

                    if (

                        hasattr(
                            connection,
                            "laddr"
                        )

                        and connection.laddr

                        and connection.laddr.port == 6379
                    ):

                        redis_online = True

                        break

                except Exception:

                    continue

            # =====================================
            # CELERY
            # =====================================

            for process in (

                psutil.process_iter(
                    ["cmdline"]
                )
            ):

                try:

                    cmdline = " ".join(

                        process.info.get(
                            "cmdline",
                            []
                        )
                    )

                    if "celery" in (
                        cmdline.lower()
                    ):

                        celery_online = True

                        break

                except Exception:

                    continue

            return {

                "redis": (

                    "Online"

                    if redis_online

                    else "Offline"
                ),

                "celery": (

                    "Online"

                    if celery_online

                    else "Offline"
                ),

                "hostname": (
                    socket.gethostname()
                ),
            }

        except Exception as error:

            logger.exception(

                f"Service detection failed: "
                f"{str(error)}"
            )

            return {

                "redis": "Offline",

                "celery": "Offline",

                "hostname": "Unknown",
            }

    # =================================================
    # DASHBOARD STATS
    # =================================================

    @classmethod
    def get_system_stats(
        cls
    ):

        cache_key = (
            "dashboard_stats"
        )

        cached = cache.get(
            cache_key
        )

        if cached:

            return cached

        try:

            monitor = cls()

            resources = (
                monitor.resource_metrics()
            )

            providers = (
                monitor.provider_health()
            )

            services = (
                monitor.service_status()
            )

            generations = (
                monitor.generation_metrics()
            )

            provider_name = "Unavailable"

            if providers.get(
                "healthy"
            ):

                provider_name = (
                    "Active"
                )

            result = {

                "cpu": resources.get(
                    "cpu_percent",
                    0,
                ),

                "ram": resources.get(
                    "memory_percent",
                    0,
                ),

                "disk": resources.get(
                    "disk_percent",
                    0,
                ),

                "cpu_count": resources.get(
                    "cpu_count",
                    0,
                ),

                "uptime_hours": (

                    resources.get(
                        "uptime_hours",
                        0,
                    )
                ),

                "queue": "Running",

                "provider": (
                    provider_name
                ),

                "redis": services.get(
                    "redis"
                ),

                "celery": services.get(
                    "celery"
                ),

                "hostname": services.get(
                    "hostname"
                ),

                "generations": (

                    generations.get(
                        "total_generations",
                        0,
                    )
                ),

                "success_rate": (

                    generations.get(
                        "success_rate",
                        0,
                    )
                ),
            }

            cache.set(

                cache_key,

                result,

                timeout=(
                    cls.CACHE_TIMEOUT
                ),
            )

            return result

        except Exception:

            return {

                "cpu": 0,

                "ram": 0,

                "disk": 0,

                "cpu_count": 0,

                "uptime_hours": 0,

                "queue": "Offline",

                "provider": "Unavailable",

                "redis": "Offline",

                "celery": "Offline",

                "hostname": "Unknown",

                "generations": 0,

                "success_rate": 0,
            }

    # =================================================
    # FULL REPORT
    # =================================================

    def full_report(
        self
    ):

        started = time.time()

        report = {

            "timestamp": (
                self.timestamp()
            ),

            "system": (
                self.system_info()
            ),

            "resources": (
                self.resource_metrics()
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

            "services": (
                self.service_status()
            ),
        }

        report[
            "execution_time"
        ] = round(

            time.time()
            - started,

            4,
        )

        logger.info(
            "Monitoring report generated."
        )

        return report