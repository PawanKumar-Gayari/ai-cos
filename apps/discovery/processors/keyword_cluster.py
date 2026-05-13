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

    def cluster(
        self,
        keywords
    ):

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
            # SPLIT WORDS
            # =====================

            words = keyword.split()

            # =====================
            # SKIP INVALID
            # =====================

            if not words:

                continue

            # =====================
            # MAIN TOPIC
            # =====================

            main_topic = words[0]

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
            ].append(keyword)

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

                    cluster_size * 15
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

            key=lambda item: item[
                "total_keywords"
            ],

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