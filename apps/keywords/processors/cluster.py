"""
Keyword clustering processor.
"""

import logging
import re


logger = logging.getLogger(__name__)


class KeywordClusterProcessor:

    """
    Semantic keyword clustering engine.
    """

    # ==================================================
    # NORMALIZE
    # ==================================================

    def normalize(
        self,
        keyword,
    ):

        """
        Normalize keyword.
        """

        keyword = (
            keyword
            .strip()
            .lower()
        )

        keyword = re.sub(
            r"\s+",
            " ",
            keyword,
        )

        return keyword

    # ==================================================
    # TOKENIZE
    # ==================================================

    def tokenize(
        self,
        keyword,
    ):

        """
        Split keyword into tokens.
        """

        keyword = (
            self.normalize(
                keyword
            )
        )

        return set(
            keyword.split()
        )

    # ==================================================
    # SIMILARITY
    # ==================================================

    def similarity_score(
        self,
        keyword1,
        keyword2,
    ):

        """
        Calculate token similarity.
        """

        tokens1 = (
            self.tokenize(
                keyword1
            )
        )

        tokens2 = (
            self.tokenize(
                keyword2
            )
        )

        if not tokens1 or not tokens2:

            return 0

        intersection = (
            tokens1.intersection(
                tokens2
            )
        )

        union = (
            tokens1.union(
                tokens2
            )
        )

        score = (
            len(intersection)
            / len(union)
        )

        return round(
            score,
            2,
        )

    # ==================================================
    # CLUSTER
    # ==================================================

    def cluster_keywords(
        self,
        keywords,
        threshold=0.4,
    ):

        """
        Group semantic keywords.
        """

        logger.warning(
            f"CLUSTER START: "
            f"{len(keywords)} keywords"
        )

        clusters = []

        used = set()

        for keyword in keywords:

            keyword = (
                self.normalize(
                    keyword
                )
            )

            if keyword in used:

                continue

            cluster = [keyword]

            used.add(
                keyword
            )

            for other in keywords:

                other = (
                    self.normalize(
                        other
                    )
                )

                if other in used:

                    continue

                similarity = (
                    self.similarity_score(
                        keyword,
                        other,
                    )
                )

                if similarity >= threshold:

                    cluster.append(
                        other
                    )

                    used.add(
                        other
                    )

            clusters.append(
                {

                    "main_keyword": (
                        keyword
                    ),

                    "keywords": (
                        cluster
                    ),

                    "count": (
                        len(cluster)
                    ),
                }
            )

        logger.warning(
            f"TOTAL CLUSTERS: "
            f"{len(clusters)}"
        )

        return clusters

    # ==================================================
    # BEST CLUSTER
    # ==================================================

    def best_cluster(
        self,
        keywords,
    ):

        """
        Return largest keyword cluster.
        """

        clusters = (
            self.cluster_keywords(
                keywords
            )
        )

        if not clusters:

            return {}

        best = max(

            clusters,

            key=lambda item: item.get(
                "count",
                0,
            ),
        )

        logger.warning(
            f"BEST CLUSTER: {best}"
        )

        return best