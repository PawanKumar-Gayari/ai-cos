"""
Discovery engine for keyword opportunity system.
"""

from apps.discovery.services.discovery_service import (
    DiscoveryService,
)


class DiscoveryEngine:

    def __init__(self):

        # =========================
        # DISCOVERY SERVICE
        # =========================

        self.discovery_service = (
            DiscoveryService()
        )

    def discover(
        self,
        seed_keyword
    ):

        # =========================
        # RUN DISCOVERY
        # =========================

        return (
            self.discovery_service.discover(
                seed_keyword
            )
        )