"""
Enterprise Feature Flag Service
-------------------------------

Production-grade runtime feature management.

Features:
- runtime feature flags
- emergency kill switches
- AI engine toggles
- SEO system toggles
- provider controls
- cached feature lookup
- dashboard integration
- production-safe controls
- performance optimization toggles
- lightweight generation controls
- async-safe database access
"""

from __future__ import annotations

import logging

from django.core.cache import cache

from django.db import (
    close_old_connections,
)

from apps.dashboard.models import (
    SystemFeature,
)


logger = logging.getLogger(
    __name__
)


# =========================================================
# FEATURE SERVICE
# =========================================================

class FeatureService:

    """
    Enterprise runtime feature manager.
    """

    CACHE_TIMEOUT = 60

    # =====================================================
    # DEFAULT FEATURES
    # =====================================================

    DEFAULT_FEATURES = {

        # =============================================
        # CORE SYSTEM
        # =============================================

        "generator_enabled": True,

        "publisher_enabled": True,

        "dashboard_enabled": True,

        "monitoring_enabled": True,

        # =============================================
        # PROVIDERS
        # =============================================

        "gemini_enabled": True,

        "openai_enabled": False,

        "ollama_enabled": False,

        # =============================================
        # AI FEATURES
        # =============================================

        "competitor_engine": False,

        "hallucination_validator": True,

        "topic_validator": True,

        "memory_indexing": False,

        "seo_scoring": True,

        "density_analysis": True,

        # =============================================
        # PERFORMANCE
        # =============================================

        "lightweight_mode": True,

        "heavy_generation_mode": False,

        # =============================================
        # SAFETY
        # =============================================

        "maintenance_mode": False,

        "emergency_shutdown": False,
    }

    # =====================================================
    # CACHE KEY
    # =====================================================

    @classmethod
    def cache_key(
        cls,
        key,
    ):

        return (
            f"feature_flag:{key}"
        )

    # =====================================================
    # GET FEATURES
    # =====================================================

    @classmethod
    def get_features(
        cls,
    ):

        try:

            close_old_connections()

            queryset = (
                SystemFeature.objects.all()
            )

            return list(

                queryset.values(

                    "id",

                    "key",

                    "name",

                    "description",

                    "category",

                    "enabled",

                    "cpu_intensive",

                    "experimental",

                    "created_at",

                    "updated_at",
                )
            )

        except Exception as error:

            logger.exception(

                f"Feature fetch failed: "
                f"{str(error)}"
            )

            return []

    # =====================================================
    # GET FEATURE
    # =====================================================

    @classmethod
    def get_feature(
        cls,
        key,
    ):

        try:

            close_old_connections()

            return (
                SystemFeature.objects.filter(
                    key=key
                ).first()
            )

        except Exception as error:

            logger.exception(

                f"Feature fetch failed: "
                f"{str(error)}"
            )

            return None

    # =====================================================
    # ENSURE DEFAULT FEATURES
    # =====================================================

    @classmethod
    def ensure_defaults(
        cls,
    ):

        for key, enabled in (

            cls.DEFAULT_FEATURES.items()
        ):

            SystemFeature.objects.get_or_create(

                key=key,

                defaults={

                    "name": (
                        key.replace(
                            "_",
                            " "
                        ).title()
                    ),

                    "enabled": enabled,
                }
            )

        logger.info(
            "Default features ensured."
        )

    # =====================================================
    # IS ENABLED
    # =====================================================

    @classmethod
    def is_enabled(
        cls,
        key,
        default=False,
    ):

        # =============================================
        # CACHE
        # =============================================

        try:

            cached = cache.get(
                cls.cache_key(key)
            )

            if cached is not None:

                return bool(cached)

        except Exception as error:

            logger.warning(

                f"Cache lookup failed: "
                f"{str(error)}"
            )

        # =============================================
        # DATABASE
        # =============================================

        try:

            close_old_connections()

            feature = (
                SystemFeature.objects.filter(
                    key=key
                ).first()
            )

            # =========================================
            # FEATURE EXISTS
            # =========================================

            if feature is not None:

                enabled = bool(
                    feature.enabled
                )

                try:

                    cache.set(

                        cls.cache_key(key),

                        enabled,

                        timeout=(
                            cls.CACHE_TIMEOUT
                        ),
                    )

                except Exception:

                    pass

                return enabled

            # =========================================
            # DEFAULT FALLBACK
            # =========================================

            fallback = (
                cls.DEFAULT_FEATURES.get(
                    key,
                    default,
                )
            )

            try:

                cache.set(

                    cls.cache_key(key),

                    fallback,

                    timeout=(
                        cls.CACHE_TIMEOUT
                    ),
                )

            except Exception:

                pass

            logger.warning(

                f"Feature missing: "
                f"{key}"
            )

            return bool(
                fallback
            )

        except Exception as error:

            logger.exception(

                f"Feature lookup failed: "
                f"{str(error)}"
            )

            # =========================================
            # SAFE FALLBACKS
            # =========================================

            if key == "generator_enabled":

                return True

            if key == "ollama_enabled":

                return False

            if key == "gemini_enabled":

                return False

            return bool(default)

    # =====================================================
    # ENABLE FEATURE
    # =====================================================

    @classmethod
    def enable(
        cls,
        key,
    ):

        close_old_connections()

        feature, _ = (
            SystemFeature.objects.get_or_create(
                key=key
            )
        )

        feature.enabled = True

        feature.save()

        cache.delete(
            cls.cache_key(key)
        )

        logger.info(

            f"Feature enabled: "
            f"{key}"
        )

        return True

    # =====================================================
    # DISABLE FEATURE
    # =====================================================

    @classmethod
    def disable(
        cls,
        key,
    ):

        close_old_connections()

        feature, _ = (
            SystemFeature.objects.get_or_create(
                key=key
            )
        )

        feature.enabled = False

        feature.save()

        cache.delete(
            cls.cache_key(key)
        )

        logger.warning(

            f"Feature disabled: "
            f"{key}"
        )

        return True

    # =====================================================
    # TOGGLE FEATURE
    # =====================================================

    @classmethod
    def toggle(
        cls,
        key,
    ):

        close_old_connections()

        feature, _ = (
            SystemFeature.objects.get_or_create(
                key=key
            )
        )

        feature.enabled = (
            not feature.enabled
        )

        feature.save()

        cache.delete(
            cls.cache_key(key)
        )

        logger.info(

            f"Feature toggled: "
            f"{key} -> "
            f"{feature.enabled}"
        )

        return feature.enabled

    # =====================================================
    # CLEAR CACHE
    # =====================================================

    @classmethod
    def clear_cache(
        cls,
    ):

        for key in (
            cls.DEFAULT_FEATURES
        ):

            cache.delete(
                cls.cache_key(key)
            )

        logger.info(
            "Feature cache cleared."
        )

        return True

    # =====================================================
    # SYSTEM STATUS
    # =====================================================

    @classmethod
    def system_status(
        cls,
    ):

        return {

            # =========================================
            # CORE
            # =========================================

            "generator": (
                cls.is_enabled(
                    "generator_enabled"
                )
            ),

            "publisher": (
                cls.is_enabled(
                    "publisher_enabled"
                )
            ),

            "dashboard": (
                cls.is_enabled(
                    "dashboard_enabled"
                )
            ),

            "monitoring": (
                cls.is_enabled(
                    "monitoring_enabled"
                )
            ),

            # =========================================
            # PROVIDERS
            # =========================================

            "gemini": (
                cls.is_enabled(
                    "gemini_enabled"
                )
            ),

            "openai": (
                cls.is_enabled(
                    "openai_enabled"
                )
            ),

            "ollama": (
                cls.is_enabled(
                    "ollama_enabled"
                )
            ),

            # =========================================
            # AI FEATURES
            # =========================================

            "competitor_engine": (
                cls.is_enabled(
                    "competitor_engine"
                )
            ),

            "hallucination_validator": (
                cls.is_enabled(
                    "hallucination_validator"
                )
            ),

            "topic_validator": (
                cls.is_enabled(
                    "topic_validator"
                )
            ),

            "memory_indexing": (
                cls.is_enabled(
                    "memory_indexing"
                )
            ),

            "seo_scoring": (
                cls.is_enabled(
                    "seo_scoring"
                )
            ),

            "density_analysis": (
                cls.is_enabled(
                    "density_analysis"
                )
            ),

            # =========================================
            # PERFORMANCE
            # =========================================

            "lightweight_mode": (
                cls.is_enabled(
                    "lightweight_mode"
                )
            ),

            "heavy_generation_mode": (
                cls.is_enabled(
                    "heavy_generation_mode"
                )
            ),

            # =========================================
            # SAFETY
            # =========================================

            "maintenance_mode": (
                cls.is_enabled(
                    "maintenance_mode"
                )
            ),

            "emergency_shutdown": (
                cls.is_enabled(
                    "emergency_shutdown"
                )
            ),
        }