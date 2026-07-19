"""
Experience injection service.
"""

import random

from utils.logger import (
    competitor_logger,
)


class ExperienceService:

    EXPERIENCE_PATTERNS = [

        (
            "installation",
            (
                "One common mistake beginners make "
                "during installation is skipping "
                "dependency updates before adding "
                "external repositories."
            ),
        ),

        (
            "server",
            (
                "On production servers, enabling "
                "automatic service startup is "
                "strongly recommended to avoid "
                "downtime after system reboots."
            ),
        ),

        (
            "docker",
            (
                "In real-world environments, Docker "
                "logs can silently consume large "
                "amounts of disk space if log "
                "rotation is not configured properly."
            ),
        ),

        (
            "ubuntu",
            (
                "Ubuntu LTS releases are generally "
                "the safest choice for Docker-based "
                "development and production systems."
            ),
        ),

        (
            "permissions",
            (
                "Permission-related Docker errors "
                "are extremely common when users "
                "forget to join the docker group."
            ),
        ),

        (
            "compose",
            (
                "For multi-container applications, "
                "Docker Compose simplifies "
                "management significantly compared "
                "to running containers manually."
            ),
        ),
    ]

    MAX_INSERTIONS = 5

    # ==================================================
    # SAFE LOWER
    # ==================================================

    def safe_lower(
        self,
        value,
    ):

        if not value:

            return ""

        return str(value).lower()

    # ==================================================
    # FIND MATCHING EXPERIENCES
    # ==================================================

    def find_matching_experiences(
        self,
        article,
    ):

        article_lower = (
            self.safe_lower(article)
        )

        matches = []

        for keyword, text in (

            self.EXPERIENCE_PATTERNS

        ):

            if keyword in article_lower:

                matches.append(text)

        return matches

    # ==================================================
    # SPLIT PARAGRAPHS
    # ==================================================

    def split_paragraphs(
        self,
        article,
    ):

        return [

            paragraph.strip()

            for paragraph in (

                article.split("\n\n")
            )

            if paragraph.strip()
        ]

    # ==================================================
    # INJECT EXPERIENCES
    # ==================================================

    def inject_experiences(
        self,
        article,
    ):

        """
        Inject practical human-like
        experience notes into article.
        """

        try:

            paragraphs = (
                self.split_paragraphs(
                    article
                )
            )

            experiences = (
                self.find_matching_experiences(
                    article
                )
            )

            if not experiences:

                competitor_logger.info(

                    "[EXPERIENCE ENGINE] "
                    "No matching patterns found"
                )

                return article

            random.shuffle(
                experiences
            )

            insertions = 0

            enhanced = []

            for index, paragraph in enumerate(
                paragraphs
            ):

                enhanced.append(
                    paragraph
                )

                # ======================================
                # INSERT EXPERIENCE EVERY FEW PARAGRAPHS
                # ======================================

                if (

                    insertions < (
                        self.MAX_INSERTIONS
                    )

                    and index % 4 == 0

                    and experiences
                ):

                    experience = (
                        experiences.pop(0)
                    )

                    enhanced.append(
                        f"> {experience}"
                    )

                    insertions += 1

            competitor_logger.info(

                f"[EXPERIENCE ENGINE] "
                f"INSERTIONS={insertions}"
            )

            return "\n\n".join(
                enhanced
            )

        except Exception as error:

            competitor_logger.exception(

                f"[EXPERIENCE ENGINE FAILED] "
                f"{str(error)}"
            )

            return article