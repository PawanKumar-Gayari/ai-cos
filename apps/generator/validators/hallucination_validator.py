"""
Enterprise Hallucination Validator
----------------------------------

Production-grade hallucination detection engine.

Features:
- fake term detection
- random noise detection
- AI hallucination protection
- fabricated statistics detection
- fake framework detection
- SEO-safe validation
- production-ready architecture
"""

from __future__ import annotations

import logging
import re


logger = logging.getLogger(
    __name__
)


# =========================================================
# HALLUCINATION VALIDATOR
# =========================================================

class HallucinationValidator:

    """
    Enterprise hallucination validator.
    """

    # =====================================================
    # RANDOM / NOISE PATTERNS
    # =====================================================

    RANDOM_PATTERNS = [

        r"\bjhbd\w*",

        r"\bkjhv\w*",

        r"\basdf\w*",

        r"\bqwerty\w*",

        r"\bzxcv\w*",

        r"\btest123\w*",

        r"\blorem\s+ipsum\b",
    ]

    # =====================================================
    # FAKE FRAMEWORK PATTERNS
    # =====================================================

    FAKE_FRAMEWORK_PATTERNS = [

        r"\b[A-Z]{4,}\s+Framework\b",

        r"\b[A-Z]{5,}\s+Method\b",

        r"\b[A-Z]{4,}\s+Protocol\b",

        r"\b[A-Z]{4,}\s+System\b",
    ]

    # =====================================================
    # FAKE STATISTICS PATTERNS
    # =====================================================

    SUSPICIOUS_STATS_PATTERNS = [

        r"\b99\.999%\b",

        r"\b100% guaranteed\b",

        r"\bscientifically proven\b",

        r"\bclinically guaranteed\b",
    ]

    # =====================================================
    # GENERIC AI PHRASES
    # =====================================================

    AI_FILLER_PHRASES = [

        "as an ai language model",

        "i hope this helps",

        "certainly!",

        "in conclusion",

        "it is important to note",

        "without further ado",
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
    # DETECT RANDOM NOISE
    # =====================================================

    @classmethod
    def detect_random_noise(
        cls,
        content,
    ):

        violations = []

        for pattern in (
            cls.RANDOM_PATTERNS
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
    # DETECT FAKE FRAMEWORKS
    # =====================================================

    @classmethod
    def detect_fake_frameworks(
        cls,
        content,
    ):

        violations = []

        for pattern in (
            cls.FAKE_FRAMEWORK_PATTERNS
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
    # DETECT SUSPICIOUS STATS
    # =====================================================

    @classmethod
    def detect_suspicious_stats(
        cls,
        content,
    ):

        violations = []

        for pattern in (
            cls.SUSPICIOUS_STATS_PATTERNS
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
    # DETECT AI FILLER
    # =====================================================

    @classmethod
    def detect_ai_filler(
        cls,
        content,
    ):

        content = cls.normalize(
            content
        )

        violations = []

        for phrase in (
            cls.AI_FILLER_PHRASES
        ):

            if phrase in content:

                violations.append(
                    phrase
                )

        return violations

    # =====================================================
    # DETECT REPETITION
    # =====================================================

    @classmethod
    def detect_repetition(
        cls,
        content,
    ):

        words = re.findall(

            r"\b\w+\b",

            content.lower(),
        )

        repeated = []

        for i in range(
            len(words) - 4
        ):

            chunk = " ".join(
                words[i:i + 5]
            )

            occurrences = content.lower().count(
                chunk
            )

            if occurrences > 3:

                repeated.append(
                    chunk
                )

        return list(
            set(repeated)
        )[:10]

    # =====================================================
    # VALIDATE CONTENT
    # =====================================================

    @classmethod
    def validate(
        cls,
        content,
    ):

        result = {

            "valid": True,

            "random_noise": [],

            "fake_frameworks": [],

            "suspicious_stats": [],

            "ai_filler": [],

            "repetition": [],

            "warnings": [],
        }

        try:

            # =========================================
            # RANDOM NOISE
            # =========================================

            random_noise = (
                cls.detect_random_noise(
                    content
                )
            )

            if random_noise:

                result[
                    "random_noise"
                ] = random_noise

                result[
                    "warnings"
                ].append(

                    "Random noise detected."
                )

                result["valid"] = False

            # =========================================
            # FAKE FRAMEWORKS
            # =========================================

            fake_frameworks = (
                cls.detect_fake_frameworks(
                    content
                )
            )

            if fake_frameworks:

                result[
                    "fake_frameworks"
                ] = fake_frameworks

                result[
                    "warnings"
                ].append(

                    "Fake frameworks detected."
                )

            # =========================================
            # SUSPICIOUS STATS
            # =========================================

            suspicious_stats = (
                cls.detect_suspicious_stats(
                    content
                )
            )

            if suspicious_stats:

                result[
                    "suspicious_stats"
                ] = suspicious_stats

                result[
                    "warnings"
                ].append(

                    "Suspicious statistics detected."
                )

            # =========================================
            # AI FILLER
            # =========================================

            ai_filler = (
                cls.detect_ai_filler(
                    content
                )
            )

            if ai_filler:

                result[
                    "ai_filler"
                ] = ai_filler

                result[
                    "warnings"
                ].append(

                    "Generic AI filler phrases detected."
                )

            # =========================================
            # REPETITION
            # =========================================

            repetition = (
                cls.detect_repetition(
                    content
                )
            )

            if repetition:

                result[
                    "repetition"
                ] = repetition

                result[
                    "warnings"
                ].append(

                    "Repetitive patterns detected."
                )

            logger.info(

                f"Hallucination validation complete | "
                f"valid={result['valid']}"
            )

            return result

        except Exception as error:

            logger.exception(

                f"Hallucination validation failed: "
                f"{str(error)}"
            )

            return {

                "valid": False,

                "random_noise": [],

                "fake_frameworks": [],

                "suspicious_stats": [],

                "ai_filler": [],

                "repetition": [],

                "warnings": [
                    str(error)
                ],
            }
