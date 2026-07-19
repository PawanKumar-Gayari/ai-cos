"""
Discovery engine for keyword opportunity system. v1
"""

from apps.discovery.services.discovery_service import (
    DiscoveryService,
)

from utils.logger import (
    logger,
)


class DiscoveryEngine:

    def __init__(
        self,
        discovery_service=None
    ):

        # =========================
        # DEPENDENCY INJECTION
        # =========================

        self.discovery_service = (
            discovery_service
            or DiscoveryService()
        )

        logger.info(
            "DiscoveryEngine initialized"
        )

    def discover(
        self,
        seed_keyword
    ):

        # =========================
        # INPUT VALIDATION
        # =========================

        if not isinstance(
            seed_keyword,
            str
        ):

            raise TypeError(
                "seed_keyword must be string"
            )

        if not seed_keyword.strip():

            raise ValueError(
                "seed_keyword cannot be empty"
            )

        logger.info(

            f"Discovery started for: "
            f"{seed_keyword}"
        )

        # =========================
        # RUN DISCOVERY
        # =========================

        result = (
            self.discovery_service.discover(
                seed_keyword
            )
        )

        logger.info(

            f"Discovery completed for: "
            f"{seed_keyword}"
        )

        return result