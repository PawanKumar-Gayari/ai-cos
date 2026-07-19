"""
Analytics engine.
"""

from __future__ import annotations

import logging

from apps.analytics.insights import (
    AnalyticsInsights,
)

from apps.analytics.tracker import (
    AnalyticsTracker,
)


logger = logging.getLogger(
    __name__
)


class AnalyticsEngine:

    def __init__(
        self,
    ):

        # ======================================
        # TRACKER
        # ======================================

        self.tracker = (
            AnalyticsTracker()
        )

        # ======================================
        # INSIGHTS
        # ======================================

        self.insights = (
            AnalyticsInsights()
        )

    # ==================================================
    # TRACK ARTICLE
    # ==================================================

    def track_article(
        self,
        **kwargs,
    ):

        logger.info(

            "Tracking article analytics."
        )

        return (
            self.tracker.track_article(
                **kwargs
            )
        )

    # ==================================================
    # TRACK PROVIDER
    # ==================================================

    def track_provider(
        self,
        **kwargs,
    ):

        logger.info(

            "Tracking provider analytics."
        )

        return (
            self.tracker.track_provider(
                **kwargs
            )
        )

    # ==================================================
    # SYSTEM OVERVIEW
    # ==================================================

    def system_overview(
        self,
    ):

        logger.info(

            "Generating system overview."
        )

        return (
            self.insights.system_overview()
        )

    # ==================================================
    # PROVIDER PERFORMANCE
    # ==================================================

    def provider_performance(
        self,
    ):

        logger.info(

            "Generating provider performance report."
        )

        return (
            self.insights.provider_performance()
        )

    # ==================================================
    # QUALITY REPORT
    # ==================================================

    def quality_report(
        self,
    ):

        logger.info(

            "Generating quality report."
        )

        return (
            self.insights.quality_report()
        )

    # ==================================================
    # VERIFICATION REPORT
    # ==================================================

    def verification_report(
        self,
    ):

        logger.info(

            "Generating verification report."
        )

        return (
            self.insights.verification_report()
        )

    # ==================================================
    # TOP ARTICLES
    # ==================================================

    def top_articles(
        self,
        limit: int = 10,
    ):

        logger.info(

            "Generating top articles report."
        )

        return (
            self.insights.top_articles(
                limit=limit
            )
        )

    # ==================================================
    # WARNING REPORT
    # ==================================================

    def warning_report(
        self,
    ):

        logger.info(

            "Generating warning report."
        )

        return (
            self.insights.warning_report()
        )

    # ==================================================
    # SYSTEM HEALTH
    # ==================================================

    def system_health(
        self,
    ):

        logger.info(

            "Generating system health report."
        )

        return (
            self.insights.system_health()
        )

    # ==================================================
    # FULL REPORT
    # ==================================================

    def full_report(
        self,
    ):

        logger.info(

            "Generating full analytics report."
        )

        return (
            self.insights.full_report()
        )