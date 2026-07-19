"""
Enterprise Topic Validator
--------------------------

Production-grade topical consistency validator.

Features:
- cross-topic contamination detection
- unrelated niche detection
- semantic topic validation
- SEO topical purity enforcement
- hallucination reduction
- AI output quality protection
"""

from __future__ import annotations

import logging
import re


logger = logging.getLogger(
    __name__
)


# =========================================================
# TOPIC VALIDATOR
# =========================================================

class TopicValidator:

    """
    Validate topical consistency.
    """

    # =====================================================
    # CROSS-TOPIC PATTERNS
    # =====================================================

    CROSS_TOPIC_RULES = {

        "study": [

            "dog food",

            "pet nutrition",

            "dog breeds",

            "puppy food",

            "pet shampoo",
        ],

        "seo": [

            "dog vaccine",

            "pet nutrition",

            "cat food",

            "pet grooming",
        ],

        "dog": [

            "stock market",

            "crypto trading",

            "loan approval",

            "forex signals",
        ],
    }

    # =====================================================
    # GENERIC NOISE PATTERNS
    # =====================================================

    NOISE_PATTERNS = [

        r"\bjhbd\w*",

        r"\bkjhv\w*",

        r"\basdf\w*",

        r"\bqwerty\w*",

        r"\bzxcv\w*",
    ]

    # =====================================================
    # NORMALIZE TEXT
    # =====================================================

    @classmethod
    def normalize(
        cls,
        text,
    ):

        return str(
            text
        ).lower()

    # =====================================================
    # DETECT PRIMARY TOPIC
    # =====================================================

    @classmethod
    def detect_primary_topic(
        cls,
        query,
    ):

        query = cls.normalize(
            query
        )

        if any(

            word in query

            for word in [

                "study",

                "exam",

                "student",

                "gate",

                "neet",

                "jee",
            ]
        ):

            return "study"

        if any(

            word in query

            for word in [

                "seo",

                "blogging",

                "website",

                "wordpress",

                "ranking",
            ]
        ):

            return "seo"

        if any(

            word in query

            for word in [

                "dog",

                "puppy",

                "pet",

                "labrador",

                "german shepherd",
            ]
        ):

            return "dog"

        return "general"

    # =====================================================
    # CHECK CROSS-TOPIC CONTAMINATION
    # =====================================================

    @classmethod
    def detect_cross_topic_content(
        cls,
        query,
        content,
    ):

        topic = cls.detect_primary_topic(
            query
        )

        if topic == "general":

            return []

        content = cls.normalize(
            content
        )

        violations = []

        blocked_terms = (
            cls.CROSS_TOPIC_RULES.get(
                topic,
                []
            )
        )

        for term in blocked_terms:

            if term in content:

                violations.append(
                    term
                )

        return violations

    # =====================================================
    # DETECT NOISE
    # =====================================================

    @classmethod
    def detect_noise_patterns(
        cls,
        content,
    ):

        violations = []

        for pattern in (
            cls.NOISE_PATTERNS
        ):

            matches = re.findall(

                pattern,

                content,

                re.IGNORECASE,
            )

            if matches:

                violations.extend(
                    matches
                )

        return violations

    # =====================================================
    # VALIDATE CONTENT
    # =====================================================

    @classmethod
    def validate(
        cls,
        query,
        content,
    ):

        result = {

            "valid": True,

            "topic": None,

            "cross_topic_violations": [],

            "noise_violations": [],

            "warnings": [],
        }

        try:

            topic = cls.detect_primary_topic(
                query
            )

            result["topic"] = (
                topic
            )

            # =========================================
            # CROSS TOPIC CHECK
            # =========================================

            cross_topic = (
                cls.detect_cross_topic_content(
                    query,
                    content,
                )
            )

            if cross_topic:

                result[
                    "cross_topic_violations"
                ] = cross_topic

                result[
                    "warnings"
                ].append(

                    "Cross-topic contamination detected."
                )

                result["valid"] = False

            # =========================================
            # NOISE CHECK
            # =========================================

            noise = (
                cls.detect_noise_patterns(
                    content
                )
            )

            if noise:

                result[
                    "noise_violations"
                ] = noise

                result[
                    "warnings"
                ].append(

                    "Hallucinated or noisy text detected."
                )

                result["valid"] = False

            logger.info(

                f"Topic validation complete | "
                f"topic={topic} | "
                f"valid={result['valid']}"
            )

            return result

        except Exception as error:

            logger.exception(

                f"Topic validation failed: "
                f"{str(error)}"
            )

            return {

                "valid": False,

                "topic": "unknown",

                "cross_topic_violations": [],

                "noise_violations": [],

                "warnings": [
                    str(error)
                ],
            }
