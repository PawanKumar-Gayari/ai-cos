"""
Global enterprise AI model manager.
"""

import logging
import threading

from sentence_transformers import (
    SentenceTransformer
)

from apps.llm.ollama_provider import (
    OllamaProvider
)


logger = logging.getLogger(
    __name__
)


class ModelManager:

    EMBEDDING_MODEL_NAME = (
        "all-MiniLM-L6-v2"
    )

    OLLAMA_MODEL_NAME = (
        "tinyllama"
    )

    # ==========================================
    # SHARED INSTANCES
    # ==========================================

    _embedding_model = None

    _ollama_provider = None

    # ==========================================
    # THREAD LOCKS
    # ==========================================

    _embedding_lock = (
        threading.Lock()
    )

    _ollama_lock = (
        threading.Lock()
    )

    # ==================================================
    # EMBEDDING MODEL
    # ==================================================

    @classmethod
    def embedding_model(
        cls
    ):

        """
        Shared singleton embedding model.
        """

        if (
            cls._embedding_model
            is not None
        ):

            return (
                cls._embedding_model
            )

        with cls._embedding_lock:

            if (
                cls._embedding_model
                is None
            ):

                logger.info(

                    f"Loading embedding model: "
                    f"{cls.EMBEDDING_MODEL_NAME}"
                )

                cls._embedding_model = (
                    SentenceTransformer(

                        cls.EMBEDDING_MODEL_NAME
                    )
                )

                logger.info(
                    "Embedding model loaded."
                )

        return (
            cls._embedding_model
        )

    # ==================================================
    # OLLAMA PROVIDER
    # ==================================================

    @classmethod
    def ollama_provider(
        cls
    ):

        """
        Shared singleton Ollama provider.
        """

        if (
            cls._ollama_provider
            is not None
        ):

            return (
                cls._ollama_provider
            )

        with cls._ollama_lock:

            if (
                cls._ollama_provider
                is None
            ):

                logger.info(

                    f"Loading Ollama provider: "
                    f"{cls.OLLAMA_MODEL_NAME}"
                )

                cls._ollama_provider = (
                    OllamaProvider(

                        model=(
                            cls.OLLAMA_MODEL_NAME
                        )
                    )
                )

                logger.info(
                    "Ollama provider loaded."
                )

        return (
            cls._ollama_provider
        )

    # ==================================================
    # WARMUP
    # ==================================================

    @classmethod
    def warmup(
        cls
    ):

        """
        Preload core AI models.
        """

        logger.info(
            "Starting model warmup."
        )

        embedding_loaded = False

        ollama_loaded = False

        try:

            cls.embedding_model()

            embedding_loaded = True

        except Exception as error:

            logger.exception(

                f"Embedding warmup failed: "
                f"{str(error)}"
            )

        try:

            cls.ollama_provider()

            ollama_loaded = True

        except Exception as error:

            logger.exception(

                f"Ollama warmup failed: "
                f"{str(error)}"
            )

        logger.info(
            "Model warmup completed."
        )

        return {

            "status": "ready",

            "embedding_loaded": (
                embedding_loaded
            ),

            "ollama_loaded": (
                ollama_loaded
            ),

            "embedding_model": (
                cls.EMBEDDING_MODEL_NAME
            ),

            "ollama_model": (
                cls.OLLAMA_MODEL_NAME
            ),
        }

    # ==================================================
    # EMBEDDING HEALTH
    # ==================================================

    @classmethod
    def embedding_health(
        cls
    ):

        """
        Validate embedding runtime.
        """

        try:

            model = (
                cls.embedding_model()
            )

            vector = (
                model.encode(
                    "health check"
                )
            )

            return {

                "healthy": (
                    vector is not None
                ),

                "vector_size": (
                    len(vector)
                ),

                "model": (
                    cls.EMBEDDING_MODEL_NAME
                ),
            }

        except Exception as error:

            logger.exception(

                f"Embedding health failed: "
                f"{str(error)}"
            )

            return {

                "healthy": False,

                "error": str(error),
            }

    # ==================================================
    # OLLAMA HEALTH
    # ==================================================

    @classmethod
    def ollama_health(
        cls
    ):

        """
        Validate Ollama runtime.
        """

        try:

            provider = (
                cls.ollama_provider()
            )

            return {

                "healthy": (
                    provider.health_check()
                ),

                "model": (
                    cls.OLLAMA_MODEL_NAME
                ),
            }

        except Exception as error:

            logger.exception(

                f"Ollama health failed: "
                f"{str(error)}"
            )

            return {

                "healthy": False,

                "error": str(error),
            }

    # ==================================================
    # SYSTEM STATUS
    # ==================================================

    @classmethod
    def system_status(
        cls
    ):

        """
        Return runtime model status.
        """

        return {

            "embedding_loaded": (

                cls._embedding_model
                is not None
            ),

            "ollama_loaded": (

                cls._ollama_provider
                is not None
            ),

            "embedding_model": (
                cls.EMBEDDING_MODEL_NAME
            ),

            "ollama_model": (
                cls.OLLAMA_MODEL_NAME
            ),

            "embedding_health": (
                cls.embedding_health()
            ),

            "ollama_health": (
                cls.ollama_health()
            ),
        }

    # ==================================================
    # UNLOAD MODELS
    # ==================================================

    @classmethod
    def unload_models(
        cls
    ):

        """
        Release shared models.
        """

        logger.warning(
            "Unloading AI models."
        )

        cls._embedding_model = None

        cls._ollama_provider = None

        return {

            "status": "unloaded"
        }