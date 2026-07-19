"""
Readability scorer.
"""

import re


class ReadabilityScorer:

    def calculate(
        self,
        content,
    ):

        # =========================
        # VALIDATE CONTENT
        # =========================

        if not content:

            return 0

        # =========================
        # WORD COUNT
        # =========================

        words = (
            content.split()
        )

        word_count = len(
            words
        )

        # =========================
        # SENTENCE COUNT
        # =========================

        sentences = re.split(

            r"[.!?]+",

            content
        )

        sentences = [

            sentence.strip()

            for sentence in sentences

            if sentence.strip()
        ]

        sentence_count = len(
            sentences
        )

        # =========================
        # PARAGRAPH COUNT
        # =========================

        paragraphs = [

            paragraph.strip()

            for paragraph in content.split(
                "\n\n"
            )

            if paragraph.strip()
        ]

        paragraph_count = len(
            paragraphs
        )

        # =========================
        # AVERAGE WORDS PER SENTENCE
        # =========================

        avg_words_per_sentence = 0

        if sentence_count > 0:

            avg_words_per_sentence = (

                word_count /
                sentence_count
            )

        # =========================
        # AVERAGE SENTENCES PER PARAGRAPH
        # =========================

        avg_sentences_per_paragraph = 0

        if paragraph_count > 0:

            avg_sentences_per_paragraph = (

                sentence_count /
                paragraph_count
            )

        # =========================
        # INITIAL SCORE
        # =========================

        score = 100

        # =========================
        # LONG SENTENCES PENALTY
        # =========================

        if avg_words_per_sentence > 25:

            score -= 20

        elif avg_words_per_sentence > 20:

            score -= 10

        # =========================
        # LARGE PARAGRAPH PENALTY
        # =========================

        if avg_sentences_per_paragraph > 6:

            score -= 20

        elif avg_sentences_per_paragraph > 4:

            score -= 10

        # =========================
        # VERY SHORT CONTENT
        # =========================

        if word_count < 300:

            score -= 20

        # =========================
        # LIMIT SCORE
        # =========================

        score = max(
            0,
            min(score, 100)
        )

        # =========================
        # RETURN RESULT
        # =========================

        return {

            "score": score,

            "word_count": word_count,

            "sentence_count": sentence_count,

            "paragraph_count": paragraph_count,

            "avg_words_per_sentence": round(
                avg_words_per_sentence,
                2
            ),

            "avg_sentences_per_paragraph": round(
                avg_sentences_per_paragraph,
                2
            ),
        }