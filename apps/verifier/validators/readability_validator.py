"""
Readability validation engine.
"""

import re


class ReadabilityValidator:

    def validate(
        self,
        content
    ):

        # =========================
        # CLEAN CONTENT
        # =========================

        cleaned_content = (
            content.replace("\n", " ")
        )

        # =========================
        # SENTENCES
        # =========================

        sentences = re.split(

            r"[.!?]+",

            cleaned_content
        )

        sentences = [

            sentence.strip()

            for sentence in sentences

            if sentence.strip()
        ]

        # =========================
        # WORDS
        # =========================

        words = cleaned_content.split()

        # =========================
        # PARAGRAPHS
        # =========================

        paragraphs = [

            paragraph.strip()

            for paragraph in content.split(
                "\n\n"
            )

            if paragraph.strip()
        ]

        # =========================
        # COUNTS
        # =========================

        sentence_count = len(
            sentences
        )

        word_count = len(
            words
        )

        paragraph_count = len(
            paragraphs
        )

        # =========================
        # AVERAGE SENTENCE LENGTH
        # =========================

        avg_sentence_length = 0

        if sentence_count > 0:

            avg_sentence_length = (
                word_count / sentence_count
            )

        # =========================
        # SCORE
        # =========================

        score = 100

        checks = []

        # =========================
        # SENTENCE LENGTH CHECK
        # =========================

        if avg_sentence_length <= 20:

            checks.append(
                "Sentence length excellent"
            )

        elif avg_sentence_length <= 30:

            score -= 10

            checks.append(
                "Sentence length acceptable"
            )

        else:

            score -= 25

            checks.append(
                "Sentence length too long"
            )

        # =========================
        # PARAGRAPH CHECK
        # =========================

        if paragraph_count >= 5:

            checks.append(
                "Paragraph structure good"
            )

        else:

            score -= 10

            checks.append(
                "Paragraph structure weak"
            )

        # =========================
        # CONTENT LENGTH CHECK
        # =========================

        if word_count >= 1000:

            checks.append(
                "Content length strong"
            )

        elif word_count >= 500:

            score -= 5

            checks.append(
                "Content length moderate"
            )

        else:

            score -= 20

            checks.append(
                "Content length weak"
            )

        # =========================
        # FINAL SCORE
        # =========================

        score = max(
            min(score, 100),
            0
        )

        # =========================
        # RETURN RESULT
        # =========================

        return {

            "readability_score": score,

            "sentence_count": sentence_count,

            "word_count": word_count,

            "paragraph_count": paragraph_count,

            "average_sentence_length": round(
                avg_sentence_length,
                2
            ),

            "checks": checks,
        }