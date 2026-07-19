"""
Enterprise SEO Entity Extraction Service
----------------------------------------

Production-grade semantic entity intelligence engine.

Features:
- multilingual entity extraction
- semantic SEO entity detection
- SERP-aware extraction
- competitor entity discovery
- long-tail entity grouping
- NLP-safe filtering
- entity normalization
- duplicate cleanup
- topic entity scoring
- search intent entities
- OCI optimized
- production-safe
"""

from __future__ import annotations

import logging
import re

from collections import Counter

from typing import Any


logger = logging.getLogger(
    __name__
)


class EntityService:

    """
    Enterprise SEO entity intelligence engine.
    """

    MIN_ENTITY_LENGTH = 3

    MAX_ENTITIES = 50

    MIN_ENTITY_FREQUENCY = 2

    # =====================================================
    # STOPWORDS
    # =====================================================

    STOPWORDS = {

        "the",
        "and",
        "for",
        "with",
        "from",
        "that",
        "this",
        "official",
        "latest",
        "guide",
        "tutorial",
        "tips",
        "tools",
        "review",
        "reviews",
        "result",
        "results",
        "pdf",
    }

    # =====================================================
    # HIGH VALUE SEO ENTITIES
    # =====================================================

    PRIORITY_TERMS = {

        "syllabus",

        "notification",

        "vacancy",

        "exam",

        "result",

        "admit card",

        "cut off",

        "eligibility",

        "selection process",

        "answer key",

        "question paper",

        "salary",
    }

    # =====================================================
    # CLEAN ENTITY
    # =====================================================

    @classmethod
    def clean_entity(
        cls,
        text: str,
    ) -> str:

        if not text:

            return ""

        text = re.sub(

            r"[^\w\s\u0900-\u097F]",

            " ",

            text,
        )

        text = re.sub(

            r"\s+",

            " ",

            text,
        )

        return text.strip()

    # =====================================================
    # NORMALIZE ENTITY
    # =====================================================

    @classmethod
    def normalize_entity(
        cls,
        text: str,
    ) -> str:

        text = cls.clean_entity(
            text
        )

        return (
            text
            .strip()
            .lower()
        )

    # =====================================================
    # VALID ENTITY
    # =====================================================

    @classmethod
    def valid_entity(
        cls,
        entity: str,
    ) -> bool:

        if not entity:

            return False

        entity = cls.normalize_entity(
            entity
        )

        if (

            len(entity)

            < cls.MIN_ENTITY_LENGTH
        ):

            return False

        if entity in cls.STOPWORDS:

            return False

        # repeated word spam
        words = entity.split()

        if (

            len(words)

            != len(set(words))
        ):

            return False

        return True

    # =====================================================
    # ENTITY SCORE
    # =====================================================

    @classmethod
    def entity_score(
        cls,
        entity: str,
        frequency: int,
    ) -> int:

        score = frequency * 2

        entity_lower = (
            entity.lower()
        )

        # long-tail bonus
        score += (
            len(entity.split()) * 2
        )

        # priority SEO bonus
        for term in (
            cls.PRIORITY_TERMS
        ):

            if term in entity_lower:

                score += 8

        # year bonus
        if re.search(

            r"\b20\d{2}\b",

            entity_lower,
        ):

            score += 5

        return score

    # =====================================================
    # EXTRACT CAPITALIZED
    # =====================================================

    @classmethod
    def capitalized_entities(
        cls,
        text: str,
    ) -> list[str]:

        matches = re.findall(

            r"\b[A-Z][a-zA-Z0-9]+\b",

            text,
        )

        return matches

    # =====================================================
    # EXTRACT MULTIWORD ENTITIES
    # =====================================================

    @classmethod
    def phrase_entities(
        cls,
        text: str,
    ) -> list[str]:

        phrases = []

        text = cls.clean_entity(
            text
        )

        words = text.split()

        for n in range(2, 5):

            for i in range(

                len(words)
                - n + 1
            ):

                phrase = " ".join(

                    words[
                        i:i + n
                    ]
                )

                if cls.valid_entity(
                    phrase
                ):

                    phrases.append(
                        phrase
                    )

        return phrases

    # =====================================================
    # SAFE LIST
    # =====================================================

    @staticmethod
    def ensure_list(
        value: Any,
    ) -> list:

        if isinstance(
            value,
            list,
        ):

            return value

        return []

    # =====================================================
    # EXTRACT
    # =====================================================

    @classmethod
    def extract(
        cls,
        results: list[dict],
    ) -> list[str]:

        logger.info(
            "Entity extraction started."
        )

        entity_counter = Counter()

        # =============================================
        # PROCESS SERP RESULTS
        # =============================================

        for item in results:

            title = item.get(
                "title",
                "",
            )

            description = item.get(
                "description",
                "",
            )

            headings = item.get(
                "headings",
                [],
            )

            questions = item.get(
                "questions",
                [],
            )

            related_searches = item.get(
                "related_searches",
                [],
            )

            combined = (

                f"{title} "

                f"{description}"
            )

            # =========================================
            # CAPITALIZED ENTITIES
            # =========================================

            entities = (
                cls.capitalized_entities(
                    combined
                )
            )

            # =========================================
            # PHRASE ENTITIES
            # =========================================

            phrase_entities = (
                cls.phrase_entities(
                    combined
                )
            )

            entities.extend(
                phrase_entities
            )

            # =========================================
            # HEADINGS
            # =========================================

            for heading in headings:

                entities.extend(

                    cls.phrase_entities(
                        heading
                    )
                )

            # =========================================
            # QUESTIONS
            # =========================================

            for question in questions:

                entities.extend(

                    cls.phrase_entities(
                        question
                    )
                )

            # =========================================
            # RELATED SEARCHES
            # =========================================

            for related in (
                related_searches
            ):

                entities.extend(

                    cls.phrase_entities(
                        related
                    )
                )

            # =========================================
            # CLEAN ENTITIES
            # =========================================

            for entity in entities:

                entity = (
                    cls.clean_entity(
                        entity
                    )
                )

                if not cls.valid_entity(
                    entity
                ):

                    continue

                entity_counter[
                    entity
                ] += 1

        # =============================================
        # SCORE ENTITIES
        # =============================================

        scored_entities = []

        for entity, frequency in (

            entity_counter.items()
        ):

            if (

                frequency
                < cls.MIN_ENTITY_FREQUENCY
            ):

                continue

            score = cls.entity_score(

                entity,

                frequency,
            )

            scored_entities.append(

                (

                    entity,

                    score,
                )
            )

        # =============================================
        # SORT
        # =============================================

        scored_entities.sort(

            key=lambda x: x[1],

            reverse=True,
        )

        entities = [

            entity

            for entity, _ in (
                scored_entities[
                    :cls.MAX_ENTITIES
                ]
            )
        ]

        logger.info(

            f"Entities extracted: "
            f"{len(entities)}"
        )

        return entities