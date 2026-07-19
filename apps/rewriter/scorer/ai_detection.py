"""
AI detection scorer.
"""

import re


class AIDetectionScorer:

    def calculate(
        self,
        content,
    ):

        # =========================
        # VALIDATE CONTENT
        # =========================

        if not content:

            return {

                "score": 100,

                "ai_probability": 100,
            }

        # =========================
        # LOWERCASE CONTENT
        # =========================

        lower_content = (
            content.lower()
        )

        # =========================
        # AI PHRASES
        # =========================

        ai_phrases = [

            "in conclusion",

            "it is important to note",

            "in today's world",

            "overall",

            "furthermore",

            "moreover",

            "additionally",

            "delve into",

            "navigate the complexities",

            "unlock the potential",

            "enhance your understanding",

            "this article explores",

            "whether you are",

            "in this guide",

            "let us explore",
        ]

        # =========================
        # DETECT AI PHRASES
        # =========================

        ai_phrase_matches = 0

        for phrase in ai_phrases:

            if phrase in lower_content:

                ai_phrase_matches += 1

        # =========================
        # REPETITIVE SENTENCE CHECK
        # =========================

        sentences = re.split(

            r"[.!?]+",

            lower_content
        )

        cleaned_sentences = [

            sentence.strip()

            for sentence in sentences

            if sentence.strip()
        ]

        unique_sentences = set(
            cleaned_sentences
        )

        duplicate_ratio = 0

        if cleaned_sentences:

            duplicate_ratio = 1 - (

                len(unique_sentences) /
                len(cleaned_sentences)
            )

        # =========================
        # INITIAL SCORE
        # =========================

        score = 100

        # =========================
        # AI PHRASE PENALTY
        # =========================

        score -= (
            ai_phrase_matches * 5
        )

        # =========================
        # DUPLICATE PENALTY
        # =========================

        score -= int(
            duplicate_ratio * 50
        )

        # =========================
        # LIMIT SCORE
        # =========================

        score = max(
            0,
            min(score, 100)
        )

        # =========================
        # AI PROBABILITY
        # =========================

        ai_probability = (
            100 - score
        )

        # =========================
        # RETURN RESULT
        # =========================

        return {

            "score": score,

            "ai_probability": (
                ai_probability
            ),

            "ai_phrase_matches": (
                ai_phrase_matches
            ),

            "duplicate_ratio": round(
                duplicate_ratio,
                2
            ),
        }