"""
Enterprise Intelligent SEO Generator
Final Optimized Production Edition
"""

from __future__ import annotations

import logging
import re
import time

from apps.dashboard.services.feature_service import (
    FeatureService,
)

from apps.generator.content_scorer import (
    ContentScorer,
)

from apps.generator.prompts.prompt_builder import (
    PromptBuilder,
)

from apps.generator.response_cleaner import (
    ResponseCleaner,
)

from apps.generator.validators.hallucination_validator import (
    HallucinationValidator,
)

from apps.generator.validators.topic_validator import (
    TopicValidator,
)

from apps.keywords.engine import (
    KeywordEngine,
)

from apps.keywords.processors.density import (
    KeywordDensityProcessor,
)

from apps.llm.router import (
    LLMRouter,
)

from apps.memory.indexer.memory_indexer import (
    MemoryIndexer,
)


logger = logging.getLogger(
    __name__
)


# =========================================================
# INTELLIGENT GENERATOR
# =========================================================

class IntelligentGenerator:

    """
    Enterprise multilingual SEO AI generator.
    """

    # =====================================================
    # INIT
    # =====================================================

    def __init__(
        self,
    ):

        self.router = (
            LLMRouter()
        )

        self.keyword_engine = (
            KeywordEngine()
        )

        self.density_processor = (
            KeywordDensityProcessor()
        )

        self.memory_indexer = (
            MemoryIndexer()
        )

    # =====================================================
    # FEATURE CHECK
    # =====================================================

    def feature_enabled(
        self,
        key,
        default=False,
    ):

        try:

            return FeatureService.is_enabled(

                key,

                default=default,
            )

        except Exception as error:

            logger.warning(

                f"Feature check failed: "
                f"{key} | "
                f"{str(error)}"
            )

            return default

    # =====================================================
    # LANGUAGE DETECTION
    # =====================================================

    def detect_language(
        self,
        text,
    ):

        text = str(
            text
        ).lower()

        if re.search(
            r"[\u0900-\u097F]",
            text,
        ):

            return "hindi"

        roman_hindi_words = [

            "kaise",

            "kya",

            "kyu",

            "karna",

            "kare",

            "likhe",

            "likhen",

            "samjhe",

            "sikhe",

            "hai",

            "hindi",
        ]

        for word in (
            roman_hindi_words
        ):

            if word in text:

                return "hinglish"

        return "english"

    # =====================================================
    # NORMALIZE PAYLOAD
    # =====================================================

    def normalize_payload(
        self,
        query,
    ):

        if isinstance(
            query,
            dict,
        ):

            payload = query

            normalized_query = str(

                payload.get(
                    "query"
                )

                or

                payload.get(
                    "keyword"
                )

                or ""
            )

        else:

            normalized_query = str(
                query
            )

            payload = {

                "query": (
                    normalized_query
                )
            }

        return (

            normalized_query,

            payload,
        )

    # =====================================================
    # TASK TYPE
    # =====================================================

    def detect_task_type(
        self,
        query,
    ):

        query_lower = str(
            query
        ).lower()

        if any(

            word in query_lower

            for word in [

                "outline",

                "toc",

                "structure",
            ]
        ):

            return "outline"

        if any(

            word in query_lower

            for word in [

                "keyword",

                "keywords",
            ]
        ):

            return "keywords"

        return "article"

    # =====================================================
    # PROVIDER ROUTING
    # =====================================================

    def select_provider(
        self,
        payload,
    ):

        manual_provider = (
            payload.get(
                "provider"
            )
        )

        # =============================================
        # MANUAL PROVIDER
        # =============================================

        if manual_provider:

            provider_health = (
                self.router.provider_health()
            )

            provider_data = (
                provider_health.get(
                    manual_provider,
                    {}
                )
            )

            cooldown = (
                provider_data.get(
                    "last_failure"
                )
            )

            if cooldown:

                logger.warning(

                    f"Manual provider "
                    f"{manual_provider} "
                    f"cooldown detected. "
                    f"Using adaptive routing."
                )

            else:

                logger.info(

                    f"Manual provider: "
                    f"{manual_provider}"
                )

                return manual_provider

        # =============================================
        # FEATURE FLAGS
        # =============================================

        gemini_enabled = (
            self.feature_enabled(
                "gemini_enabled",
                default=False,
            )
        )

        openai_enabled = (
            self.feature_enabled(
                "openai_enabled",
                default=False,
            )
        )

        logger.info(

            f"Provider status | "
            f"gemini={gemini_enabled} | "
            f"openai={openai_enabled}"
        )

        # =============================================
        # PRIORITY ORDER
        # =============================================

        if gemini_enabled:

            logger.info(
                "Adaptive routing → Gemini"
            )

            return "gemini"

        if openai_enabled:

            logger.info(
                "Adaptive routing → OpenAI"
            )

            return "openai"

        raise RuntimeError(
            "No AI provider enabled."
        )

    # =====================================================
    # RESPONSE EXTRACTION
    # =====================================================

    def extract_response(
        self,
        response,
    ):

        if isinstance(
            response,
            dict,
        ):

            return {

                "success": response.get(
                    "success",
                    True,
                ),

                "provider": response.get(
                    "provider",
                    "unknown",
                ),

                "content": (

                    response.get(
                        "content"
                    )

                    or

                    response.get(
                        "generated_content"
                    )

                    or ""
                ),

                "errors": response.get(
                    "errors",
                    [],
                ),
            }

        return {

            "success": True,

            "provider": "unknown",

            "content": str(
                response
            ),

            "errors": [],
        }

    # =====================================================
    # MAIN GENERATION
    # =====================================================

    def generate(
        self,
        query,
        session_id=None,
    ):

        started_at = time.time()

        query, payload = (
            self.normalize_payload(
                query
            )
        )

        logger.info(

            f"START GENERATION: "
            f"{query}"
        )

        # =============================================
        # EMERGENCY SHUTDOWN
        # =============================================

        if self.feature_enabled(
            "emergency_shutdown"
        ):

            raise RuntimeError(
                "System temporarily disabled."
            )

        # =============================================
        # GENERATOR ENABLED
        # =============================================

        if not self.feature_enabled(

            "generator_enabled",

            default=True,
        ):

            raise RuntimeError(
                "Generator disabled."
            )

        # =============================================
        # PROVIDER ROUTING
        # =============================================

        selected_provider = (
            self.select_provider(
                payload
            )
        )

        payload.setdefault(

            "provider",

            selected_provider,
        )

        logger.info(

            f"Selected provider: "
            f"{selected_provider}"
        )

        # =============================================
        # TASK + LANGUAGE
        # =============================================

        task_type = (
            self.detect_task_type(
                query
            )
        )

        language = (
            self.detect_language(
                query
            )
        )

        # =============================================
        # LIGHTWEIGHT MODE
        # =============================================

        lightweight_mode = (
            self.feature_enabled(
                "lightweight_mode",
                default=True,
            )
        )

        logger.info(

            f"Language: "
            f"{language} | "
            f"Task: "
            f"{task_type}"
        )

        # =============================================
        # SEO DATA REUSE
        # =============================================

        seo_data = (
            payload.get(
                "seo_data",
                {}
            )
        )

        if seo_data:

            logger.info(
                "Reusing existing SEO data."
            )

        else:

            logger.info(
                "Running fresh SEO analysis."
            )

            try:

                seo_data = (
                    self.keyword_engine
                    .analyze_keyword(
                        query
                    )
                )

                logger.info(
                    "SEO analysis completed."
                )

            except Exception as error:

                logger.warning(

                    f"SEO engine failed: "
                    f"{str(error)}"
                )

                seo_data = {}

        # =============================================
        # PROMPT BUILDING
        # =============================================

        final_prompt = (
            PromptBuilder.build(

                user_query=query,

                language=language,

                seo_data=seo_data,

                competitor_context="",
            )
        )

        logger.info(
            "Prompt assembly complete."
        )

        # =============================================
        # GENERATION
        # =============================================

        response = self.router.generate(

            prompt=final_prompt,

            task_type=task_type,

            provider=payload.get(
                "provider"
            ),
        )

        normalized_response = (
            self.extract_response(
                response
            )
        )

        actual_provider = (

            normalized_response.get(
                "provider",
                selected_provider,
            )
        )

        generated_content = (

            normalized_response.get(
                "content",
                ""
            )
        )

        # =============================================
        # EMPTY CHECK
        # =============================================

        if not generated_content:

            raise RuntimeError(
                "Empty AI response received."
            )

        # =============================================
        # CLEAN RESPONSE
        # =============================================

        generated_content = (
            ResponseCleaner.clean(
                generated_content
            )
        )

        # =============================================
        # VALIDATION
        # =============================================

        hallucination_validation = {}

        topic_validation = {}

        if self.feature_enabled(
            "hallucination_validator"
        ):

            try:

                hallucination_validation = (
                    HallucinationValidator.validate(
                        generated_content
                    )
                )

            except Exception as error:

                logger.warning(

                    f"Hallucination validator failed: "
                    f"{str(error)}"
                )

        if self.feature_enabled(
            "topic_validator"
        ):

            try:

                topic_validation = (
                    TopicValidator.validate(

                        query,

                        generated_content,
                    )
                )

            except Exception as error:

                logger.warning(

                    f"Topic validator failed: "
                    f"{str(error)}"
                )

        # =============================================
        # SEO SCORING
        # =============================================

        content_scores = {}

        if (

            self.feature_enabled(
                "seo_scoring"
            )

            and

            not lightweight_mode
        ):

            try:

                content_scores = (
                    ContentScorer.score(
                        generated_content
                    )
                )

            except Exception as error:

                logger.warning(

                    f"Scoring failed: "
                    f"{str(error)}"
                )

        # =============================================
        # DENSITY ANALYSIS
        # =============================================

        density_analysis = {}

        if (

            self.feature_enabled(
                "density_analysis"
            )

            and

            not lightweight_mode
        ):

            try:

                density_analysis = (
                    self.density_processor.analyze(

                        generated_content,

                        query,
                    )
                )

            except Exception as error:

                logger.warning(

                    f"Density failed: "
                    f"{str(error)}"
                )

        # =============================================
        # MEMORY INDEXING
        # =============================================

        if self.feature_enabled(
            "memory_indexing"
        ):

            try:

                self.memory_indexer.index(

                    query=query,

                    metadata={

                        "title": query,

                        "provider": (
                            actual_provider
                        ),

                        "task_type": (
                            task_type
                        ),

                        "source": (
                            "intelligent_generator"
                        ),
                    }
                )

            except Exception as error:

                logger.warning(

                    f"Memory indexing failed: "
                    f"{str(error)}"
                )

        # =============================================
        # EXECUTION TIME
        # =============================================

        execution_time = round(

            time.time() - started_at,

            2,
        )

        # =============================================
        # FINAL LOGGING
        # =============================================

        if normalized_response.get(
            "success",
            False
        ):

            logger.info(

                f"GENERATION COMPLETE | "
                f"provider={actual_provider} | "
                f"time={execution_time}s"
            )

        else:

            logger.error(

                f"GENERATION FAILED | "
                f"provider={actual_provider}"
            )

        # =============================================
        # FINAL RESPONSE
        # =============================================

        return {

            "success": (
                normalized_response.get(
                    "success",
                    True,
                )
            ),

            "provider": (
                actual_provider
            ),

            "query": query,

            "language": language,

            "task_type": (
                task_type
            ),

            "execution_time": (
                execution_time
            ),

            "lightweight_mode": (
                lightweight_mode
            ),

            "content": (
                generated_content
            ),

            "seo_data": (
                seo_data
            ),

            "scores": (
                content_scores
            ),

            "density_analysis": (
                density_analysis
            ),

            "hallucination_validation": (
                hallucination_validation
            ),

            "topic_validation": (
                topic_validation
            ),

            "errors": (
                normalized_response.get(
                    "errors",
                    [],
                )
            ),
        }