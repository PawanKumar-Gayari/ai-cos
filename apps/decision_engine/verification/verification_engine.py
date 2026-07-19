from typing import Dict, Any, List

from apps.decision_engine.verification.claims.claim_extractor import (
    ClaimExtractor,
)

from apps.decision_engine.verification.claims.fact_matcher import (
    FactMatcher,
)

from apps.decision_engine.verification.claims.contradiction_detector import (
    ContradictionDetector,
)

from apps.decision_engine.verification.claims.verification_score import (
    VerificationScore,
)

from apps.decision_engine.verification.freshness.freshness_detector import (
    FreshnessDetector,
)

from apps.decision_engine.verification.realtime.live_verifier import (
    LiveVerifier,
)

from apps.decision_engine.verification.realtime.source_monitor import (
    SourceMonitor,
)


# =============================================================
# VERIFICATION ENGINE
# =============================================================

class VerificationEngine:

    """
    Central verification engine.
    """

    # =========================================================
    # INIT
    # =========================================================

    def __init__(self):

        self.claim_extractor = (
            ClaimExtractor()
        )

        self.fact_matcher = (
            FactMatcher()
        )

        self.contradiction_detector = (
            ContradictionDetector()
        )

        self.verification_score = (
            VerificationScore()
        )

        self.freshness_detector = (
            FreshnessDetector()
        )

        self.live_verifier = (
            LiveVerifier()
        )

        self.source_monitor = (
            SourceMonitor()
        )

    # =========================================================
    # VERIFY
    # =========================================================

    def verify(
        self,
        content: str,
        keyword: str = "",
        verified_facts: List[str] | None = None,
        sources: List[str] | None = None,
    ) -> Dict[str, Any]:

        verified_facts = (
            verified_facts or []
        )

        sources = (
            sources or []
        )

        # =====================================================
        # CLAIM EXTRACTION
        # =====================================================

        claim_result = (
            self.claim_extractor.extract(
                content
            )
        )

        claims = [

            item["text"]

            for item
            in claim_result["claims"]
        ]

        # =====================================================
        # FACT MATCHING
        # =====================================================

        fact_result = (
            self.fact_matcher.match(
                claims=claims,
                verified_facts=verified_facts,
            )
        )

        # =====================================================
        # CONTRADICTIONS
        # =====================================================

        contradiction_result = (
            self.contradiction_detector.detect(
                content
            )
        )

        # =====================================================
        # FRESHNESS
        # =====================================================

        freshness_result = (
            self.freshness_detector.detect(
                content=content,
                keyword=keyword,
            )
        )

        # =====================================================
        # LIVE
        # =====================================================

        live_result = (
            self.live_verifier.verify(
                keyword=keyword,
                content=content,
            )
        )

        # =====================================================
        # SOURCES
        # =====================================================

        source_result = (
            self.source_monitor.monitor(
                sources
            )
        )

        # =====================================================
        # FINAL SCORE
        # =====================================================

        verification_result = (
            self.verification_score.calculate(

                factual_accuracy_score=
                fact_result[
                    "factual_accuracy_score"
                ],

                consistency_score=
                contradiction_result[
                    "consistency_score"
                ],

                source_trust_score=
                source_result.get(
                    "monitoring_score",
                    80,
                ),

                contradictions_detected=
                contradiction_result[
                    "contradictions_detected"
                ],

                total_claims=
                claim_result[
                    "total_claims"
                ],

                verified_claims=
                fact_result[
                    "matched_claims"
                ],
            )
        )

        # =====================================================
        # DECISION
        # =====================================================

        decision = (
            self._generate_decision(
                verification_result
            )
        )

        return {

            "decision": decision,

            "claim_result":
            claim_result,

            "fact_result":
            fact_result,

            "contradiction_result":
            contradiction_result,

            "freshness_result":
            freshness_result,

            "live_result":
            live_result,

            "source_result":
            source_result,

            "verification_result":
            verification_result,
        }

    # =========================================================
    # DECISION
    # =========================================================

    def _generate_decision(
        self,
        verification_result: Dict[str, Any],
    ) -> str:

        score = (
            verification_result[
                "overall_verification_score"
            ]
        )

        if score >= 85:

            return "publish"

        if score >= 60:

            return "rewrite"

        return "reject"