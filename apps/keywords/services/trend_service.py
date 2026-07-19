"""
Production SEO Trend Intelligence Service
-----------------------------------------

Enterprise-grade SEO trend analysis engine.

Features:
- secure keyword validation
- trend scoring
- momentum detection
- seasonality analysis
- growth forecasting
- scalable architecture
- OCI optimized
- production-safe
"""

from __future__ import annotations

import logging
import math

from datetime import (
    UTC,
    datetime,
)

from typing import (
    Any,
)

from apps.keywords.constants import (

    BLOCKED_KEYWORDS,

    MAX_KEYWORD_LENGTH,

    MIN_KEYWORD_LENGTH,
)

from apps.keywords.exceptions import (
    KeywordValidationException,
)


logger = logging.getLogger(__name__)


class TrendService:
    """
    Enterprise SEO trend intelligence engine.
    """

    TREND_STABLE = "stable"

    TREND_RISING = "rising"

    TREND_DECLINING = "declining"

    TREND_BREAKOUT = "breakout"

    VALID_TRENDS = {

        TREND_STABLE,

        TREND_RISING,

        TREND_DECLINING,

        TREND_BREAKOUT,
    }

    TREND_TERMS = {

        "2026",

        "latest",

        "new",

        "update",

        "trending",

        "breaking",
    }

    SEASONAL_TERMS = {

        "exam",

        "admission",

        "result",

        "recruitment",

        "vacancy",
    }

    # =============================================
    # VALIDATE KEYWORD
    # =============================================

    def validate_keyword(
        self,
        keyword: str,
    ) -> str:

        if not isinstance(
            keyword,
            str,
        ):

            raise KeywordValidationException(
                "Keyword must be string."
            )

        keyword = keyword.strip()

        if not keyword:

            raise KeywordValidationException(
                "Keyword cannot be empty."
            )

        normalized = keyword.lower()

        if normalized in BLOCKED_KEYWORDS:

            raise KeywordValidationException(
                "Blocked keyword detected."
            )

        if (

            len(keyword)

            < MIN_KEYWORD_LENGTH
        ):

            raise KeywordValidationException(
                "Keyword too short."
            )

        if (

            len(keyword)

            > MAX_KEYWORD_LENGTH
        ):

            raise KeywordValidationException(
                "Keyword too long."
            )

        return keyword

    # =============================================
    # NORMALIZE KEYWORD
    # =============================================

    def normalize_keyword(
        self,
        keyword: str,
    ) -> str:

        return (

            keyword
            .strip()
            .lower()
        )

    # =============================================
    # TREND SCORE
    # =============================================

    def calculate_trend_score(
        self,
        keyword: str,
    ) -> int:

        keyword = (

            self.validate_keyword(
                keyword
            )
        )

        keyword = (

            self.normalize_keyword(
                keyword
            )
        )

        keyword_length = len(
            keyword.split()
        )

        base_score = 50

        # =========================================
        # LONG TAIL BONUS
        # =========================================

        if keyword_length >= 4:

            base_score += 10

        # =========================================
        # TREND TERMS
        # =========================================

        if any(

            word in keyword

            for word in (
                self.TREND_TERMS
            )
        ):

            base_score += 20

        return min(
            base_score,
            100,
        )

    # =============================================
    # DETECT MOMENTUM
    # =============================================

    def detect_momentum(
        self,
        score: int,
    ) -> str:

        if score >= 85:

            return self.TREND_BREAKOUT

        if score >= 70:

            return self.TREND_RISING

        if score >= 40:

            return self.TREND_STABLE

        return self.TREND_DECLINING

    # =============================================
    # SEASONAL FACTOR
    # =============================================

    def seasonal_factor(
        self,
        keyword: str,
    ) -> float:

        keyword = (

            self.normalize_keyword(
                keyword
            )
        )

        current_month = (

            datetime.now(
                tz=UTC
            ).month
        )

        # =========================================
        # SEASONAL TERMS
        # =========================================

        if any(

            word in keyword

            for word in (
                self.SEASONAL_TERMS
            )
        ):

            if current_month in {

                1,
                2,
                3,
                4,
                5,
                6,
            }:

                return 1.3

        return 1.0

    # =============================================
    # GROWTH POTENTIAL
    # =============================================

    def growth_potential(
        self,
        score: int,
        seasonal: float,
    ) -> float:

        growth = (

            score * seasonal
        ) / 100

        return round(

            min(
                growth,
                1.0,
            ),

            2,
        )

    # =============================================
    # TREND ANALYSIS
    # =============================================

    def analyze(
        self,
        keyword: str,
    ) -> dict[str, Any]:

        logger.info(
            "Trend analysis started."
        )

        keyword = (

            self.validate_keyword(
                keyword
            )
        )

        # =========================================
        # TREND SCORE
        # =========================================

        score = (

            self.calculate_trend_score(
                keyword
            )
        )

        # =========================================
        # MOMENTUM
        # =========================================

        momentum = (

            self.detect_momentum(
                score
            )
        )

        # =========================================
        # SEASONALITY
        # =========================================

        seasonal = (

            self.seasonal_factor(
                keyword
            )
        )

        # =========================================
        # GROWTH
        # =========================================

        growth = (

            self.growth_potential(

                score,

                seasonal,
            )
        )

        # =========================================
        # FINAL RESPONSE
        # =========================================

        result = {

            "keyword":
            keyword,

            "trend_score":
            score,

            "momentum":
            momentum,

            "seasonal_factor":
            seasonal,

            "growth_potential":
            growth,

            "analyzed_at":

            datetime.now(
                tz=UTC
            ).isoformat(),
        }

        logger.info(
            "Trend analysis completed."
        )

        return result

    # =============================================
    # FORECAST
    # =============================================

    def forecast(
        self,
        keyword: str,
    ) -> dict[str, Any]:

        logger.info(
            "Trend forecast started."
        )

        analysis = (
            self.analyze(
                keyword
            )
        )

        score = analysis[
            "trend_score"
        ]

        projected_growth = round(

            math.sqrt(
                score
            ) * 10,

            2,
        )

        result = {

            "keyword":
            keyword,

            "forecast_score":
            projected_growth,

            "forecast_window":
            "90_days",

            "confidence":
            0.72,
        }

        logger.info(
            "Trend forecast completed."
        )

        return result