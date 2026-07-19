"""
Keyword clustering engine for discovery system.
"""

from utils.keyword_normalizer import (
    KeywordNormalizer,
)

from utils.helpers import (
    Helpers,
)

from utils.scoring_helpers import (
    ScoringHelpers,
)

from utils.logger import (
    logger,
)


class KeywordCluster:

    # =========================
    # CLUSTER IGNORE WORDS
    # =========================

    IGNORE_WORDS = {

        "best",

        "top",

        "cheap",

        "free",

        "professional",

        "guide",

        "tutorial",

        "review",

        "comparison",

        "alternatives",

        "tips",

        "strategy",
    }

    def _extract_topic(
        self,
        keyword
    ):

        words = keyword.split()

        if not words:

            return "general"

        # =========================
        # FIND FIRST VALID TOPIC
        # =========================

        for word in words:

            if word not in (
                self.IGNORE_WORDS
            ):

                return word

        return words[0]

    def cluster(
        self,
        keywords
    ):

        # =========================
        # VALIDATE INPUT
        # =========================

        if not keywords:

            logger.warning(
                "No keywords received for clustering"
            )

            return {

                "total_clusters": 0,

                "clusters": [],
            }

        logger.info(

            f"Starting keyword clustering "
            f"for {len(keywords)} keywords"
        )

        # =========================
        # CLUSTER STORAGE
        # =========================

        clusters = {}

        # =========================
        # PROCESS KEYWORDS
        # =========================

        for keyword in keywords:

            try:

                # =====================
                # SKIP EMPTY
                # =====================

                if not keyword:

                    continue

                # =====================
                # NORMALIZE KEYWORD
                # =====================

                keyword = (
                    KeywordNormalizer.normalize(
                        keyword
                    )
                )

                # =====================
                # SKIP INVALID
                # =====================

                if not keyword:

                    continue

                # =====================
                # EXTRACT TOPIC
                # =====================

                main_topic = (
                    self._extract_topic(
                        keyword
                    )
                )

                # =====================
                # CREATE CLUSTER
                # =====================

                if main_topic not in clusters:

                    clusters[
                        main_topic
                    ] = []

                # =====================
                # ADD KEYWORD
                # =====================

                clusters[
                    main_topic
                ].append(
                    keyword
                )

            except Exception as error:

                logger.warning(

                    f"Failed to cluster keyword: "
                    f"{keyword} | "
                    f"{str(error)}"
                )

                continue

        # =========================
        # BUILD FINAL DATA
        # =========================

        cluster_data = []

        for topic, topic_keywords in (
            clusters.items()
        ):

            # =====================
            # REMOVE DUPLICATES
            # =====================

            topic_keywords = (
                Helpers.unique_list(
                    topic_keywords
                )
            )

            # =====================
            # SORT KEYWORDS
            # =====================

            topic_keywords.sort()

            # =====================
            # CLUSTER SIZE
            # =====================

            cluster_size = len(
                topic_keywords
            )

            # =====================
            # CLUSTER SCORE
            # =====================

            cluster_score = (
                ScoringHelpers.normalize_score(

                    min(
                        cluster_size * 15,
                        100
                    )
                )
            )

            # =====================
            # CLUSTER LEVEL
            # =====================

            cluster_level = (
                ScoringHelpers.confidence_level(
                    cluster_score
                )
            )

            # =====================
            # BUILD CLUSTER
            # =====================

            cluster_data.append({

                "topic": topic,

                "total_keywords": (
                    cluster_size
                ),

                "cluster_score": (
                    cluster_score
                ),

                "cluster_level": (
                    cluster_level
                ),

                "keywords": (
                    topic_keywords
                ),
            })

        # =========================
        # SORT CLUSTERS
        # =========================

        cluster_data.sort(

            key=lambda item: (

                item["total_keywords"],

                item["cluster_score"]
            ),

            reverse=True
        )

        logger.info(

            f"Keyword clustering completed "
            f"with {len(cluster_data)} "
            f"clusters"
        )

        # =========================
        # RETURN RESULT
        # =========================

        return {

            "total_clusters": len(
                cluster_data
            ),

            "clusters": (
                cluster_data
            ),
        }