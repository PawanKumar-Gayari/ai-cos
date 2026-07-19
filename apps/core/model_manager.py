"""
Enterprise AI Model Manager
---------------------------

Production-grade global AI runtime manager.

Final Optimizations:
- singleton embedding model
- thread-safe loading
- offline HuggingFace runtime
- low-memory architecture
- cached health validation
- zero-inference health checks
- OCI optimized deployment
- reduced startup latency
- lower CPU spikes
- production-safe runtime
"""

from __future__ import annotations

import logging
import os
import threading
import time

from django.core.cache import cache

from sentence_transformers import (
    SentenceTransformer,
)


# =========================================================
# OFFLINE HF OPTIMIZATION
# =========================================================

os.environ.setdefault(
    "HF_HUB_OFFLINE",
    "1",
)

os.environ.setdefault(
    "TRANSFORMERS_OFFLINE",
    "1",
)


logger = logging.getLogger(
    __name__
)


# =========================================================
# MODEL MANAGER
# =========================================================

class ModelManager:

    """
    Enterprise singleton AI model manager.
    """

    EMBEDDING_MODEL_NAME = (
        "sentence-transformers/all-MiniLM-L6-v2"
    )

    HEALTH_CACHE_TIMEOUT = 3600

    _embedding_model = None

    _embedding_lock = (
        threading.Lock()
    )

    # =====================================================
    # EMBEDDING MODEL
    # =====================================================

    @classmethod
    def embedding_model(
        cls,
    ):

        """
        Shared singleton embedding model.
        """

        # =============================================
        # REUSE EXISTING MODEL
        # =============================================

        if (
            cls._embedding_model
            is not None
        ):

            return (
                cls._embedding_model
            )

        # =============================================
        # THREAD SAFE LOAD
        # =============================================

        with cls._embedding_lock:

            if (
                cls._embedding_model
                is None
            ):

                started = time.time()

                logger.info(

                    f"Loading embedding model: "
                    f"{cls.EMBEDDING_MODEL_NAME}"
                )

                cls._embedding_model = (
                    SentenceTransformer(

                        cls.EMBEDDING_MODEL_NAME,

                        device="cpu",

                        local_files_only=True,
                    )
                )

                duration = round(

                    time.time()
                    - started,

                    2,
                )

                logger.info(

                    f"Embedding model loaded "
                    f"in {duration}s"
                )

        return (
            cls._embedding_model
        )

    # =====================================================
    # WARMUP
    # =====================================================

    @classmethod
    def warmup(
        cls,
    ):

        """
        Preload AI runtime.
        """

        if (
            cls._embedding_model
            is not None
        ):

            logger.info(
                "Embedding model already warmed."
            )

            return {

                "status":
                "already_warmed",

                "embedding_model":
                cls.EMBEDDING_MODEL_NAME,
            }

        logger.info(
            "Starting AI warmup."
        )

        started = time.time()

        embedding_loaded = False

        try:

            cls.embedding_model()

            embedding_loaded = True

        except Exception as error:

            logger.exception(

                f"Embedding warmup failed: "
                f"{str(error)}"
            )

        duration = round(

            time.time()
            - started,

            2,
        )

        logger.info(

            f"AI warmup completed "
            f"in {duration}s"
        )

        return {

            "status": "ready",

            "embedding_loaded":
            embedding_loaded,

            "embedding_model":
            cls.EMBEDDING_MODEL_NAME,

            "warmup_time":
            duration,
        }

    # =====================================================
    # EMBEDDING HEALTH
    # =====================================================

    @classmethod
    def embedding_health(
        cls,
    ):

        """
        Lightweight runtime validation.
        """

        try:

            cache_key = (
                "embedding_health_status"
            )

            cached = cache.get(
                cache_key
            )

            if cached:

                return cached

            # =========================================
            # VALIDATE MODEL LOAD ONLY
            # =========================================

            cls.embedding_model()

            result = {

                "healthy": True,

                "model":
                cls.EMBEDDING_MODEL_NAME,

                "loaded":
                (
                    cls._embedding_model
                    is not None
                ),
            }

            cache.set(

                cache_key,

                result,

                timeout=(
                    cls.HEALTH_CACHE_TIMEOUT
                ),
            )

            return result

        except Exception as error:

            logger.exception(

                f"Embedding health failed: "
                f"{str(error)}"
            )

            return {

                "healthy": False,

                "error": str(error),
            }

    # =====================================================
    # SYSTEM STATUS
    # =====================================================

    @classmethod
    def system_status(
        cls,
    ):

        """
        Global AI runtime status.
        """

        return {

            "embedding_loaded": (

                cls._embedding_model
                is not None
            ),

            "embedding_model":
            cls.EMBEDDING_MODEL_NAME,

            "embedding_health":
            cls.embedding_health(),
        }

    # =====================================================
    # UNLOAD
    # =====================================================

    @classmethod
    def unload_models(
        cls,
    ):

        """
        Release shared runtime.
        """

        logger.warning(
            "Unloading AI models."
        )

        cls._embedding_model = None

        cache.delete(
            "embedding_health_status"
        )

        return {

            "status": "unloaded"
        }