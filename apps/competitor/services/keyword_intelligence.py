"""
Keyword intelligence integration service.
"""

from utils.logger import (
    competitor_logger,
)

from utils.text_cleaner import (
    TextCleaner,
)

from utils.helpers import (
    Helpers,
)

# ==================================================
# IMPORT KEYWORD ENGINE
# ==================================================

try:

    from apps.keywords.engine import (
        KeywordEngine,
    )

except Exception:

    KeywordEngine = None


class KeywordIntelligenceService:

    DEFAULT_LIMIT = 25

    def __init__(
        self
    ):

        self.keyword_engine = None

        if KeywordEngine:

            try:

                self.keyword_engine = (
                    KeywordEngine()
                )

            except Exception as error:

                competitor_logger.exception(

                    f"[KEYWORD ENGINE INIT FAILED] "
                    f"{str(error)}"
                )

    # ==================================================
    # SAFE CLEAN
    # ==================================================

    def safe_clean(
        self,
        value,
    ):

        if not value:

            return ""

        return TextCleaner.clean(
            str(value)
        )

    # ==================================================
    # NORMALIZE KEYWORDS
    # ==================================================

    def normalize_keywords(
        self,
        keywords,
    ):

        normalized = []

        for keyword in keywords:

            cleaned = (
                self.safe_clean(
                    keyword
                )
                .strip()
                .lower()
            )

            if not cleaned:

                continue

            normalized.append(
                cleaned
            )

        return Helpers.unique_list(
            normalized
        )

    # ==================================================
    # EXTRACT SEMANTIC KEYWORDS
    # ==================================================

    def extract_semantic_keywords(
        self,
        keyword_data,
    ):

        """
        Extract semantic keyword intelligence.
        """

        semantic_keywords = []

        # ==========================================
        # RELATED KEYWORDS
        # ==========================================

        related_keywords = (
            keyword_data.get(
                "related_keywords",
                []
            )
        )

        semantic_keywords.extend(
            related_keywords
        )

        # ==========================================
        # LONG TAIL KEYWORDS
        # ==========================================

        long_tail_keywords = (
            keyword_data.get(
                "long_tail_keywords",
                []
            )
        )

        semantic_keywords.extend(
            long_tail_keywords
        )

        # ==========================================
        # NLP KEYWORDS
        # ==========================================

        nlp_keywords = (
            keyword_data.get(
                "nlp_keywords",
                []
            )
        )

        semantic_keywords.extend(
            nlp_keywords
        )

        # ==========================================
        # ENTITIES
        # ==========================================

        entities = (
            keyword_data.get(
                "entities",
                []
            )
        )

        semantic_keywords.extend(
            entities
        )

        return self.normalize_keywords(
            semantic_keywords
        )

    # ==================================================
    # EXTRACT TOPICAL CLUSTERS
    # ==================================================

    def extract_topic_clusters(
        self,
        keyword_data,
    ):

        """
        Extract topical clusters.
        """

        clusters = (
            keyword_data.get(
                "clusters",
                []
            )
        )

        normalized_clusters = []

        for cluster in clusters:

            if isinstance(
                cluster,
                dict,
            ):

                cluster_name = (
                    cluster.get(
                        "name",
                        ""
                    )
                )

                cleaned = (
                    self.safe_clean(
                        cluster_name
                    )
                )

                if cleaned:

                    normalized_clusters.append(
                        cleaned
                    )

            else:

                cleaned = (
                    self.safe_clean(
                        cluster
                    )
                )

                if cleaned:

                    normalized_clusters.append(
                        cleaned
                    )

        return Helpers.unique_list(
            normalized_clusters
        )

    # ==================================================
    # FETCH KEYWORD INTELLIGENCE
    # ==================================================

    def fetch(
        self,
        keyword,
    ):

        """
        Fetch keyword intelligence.
        """

        competitor_logger.info(

            f"[KEYWORD INTELLIGENCE START] "
            f"KEYWORD={keyword}"
        )

        # ==========================================
        # ENGINE SAFETY
        # ==========================================

        if not self.keyword_engine:

            competitor_logger.warning(

                "Keyword engine unavailable."
            )

            return {

                "semantic_keywords": [],

                "topic_clusters": [],

                "entities": [],
            }

        try:

            # ==========================================
            # RUN KEYWORD ENGINE
            # ==========================================

            keyword_data = (
                self.keyword_engine.analyze(
                    keyword
                )
            )

            # ==========================================
            # SEMANTIC KEYWORDS
            # ==========================================

            semantic_keywords = (
                self.extract_semantic_keywords(
                    keyword_data
                )
            )

            # ==========================================
            # TOPIC CLUSTERS
            # ==========================================

            topic_clusters = (
                self.extract_topic_clusters(
                    keyword_data
                )
            )

            # ==========================================
            # ENTITIES
            # ==========================================

            entities = (
                keyword_data.get(
                    "entities",
                    []
                )
            )

            entities = (
                self.normalize_keywords(
                    entities
                )
            )

            competitor_logger.info(

                f"[KEYWORD INTELLIGENCE SUCCESS] "
                f"SEMANTIC={len(semantic_keywords)} "
                f"CLUSTERS={len(topic_clusters)} "
                f"ENTITIES={len(entities)}"
            )

            return {

                "semantic_keywords": (
                    semantic_keywords[
                        : self.DEFAULT_LIMIT
                    ]
                ),

                "topic_clusters": (
                    topic_clusters[
                        : self.DEFAULT_LIMIT
                    ]
                ),

                "entities": (
                    entities[
                        : self.DEFAULT_LIMIT
                    ]
                ),
            }

        except Exception as error:

            competitor_logger.exception(

                f"[KEYWORD INTELLIGENCE FAILED] "
                f"{str(error)}"
            )

            return {

                "semantic_keywords": [],

                "topic_clusters": [],

                "entities": [],
            }