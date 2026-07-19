"""
Pipeline execution manager.
"""

from apps.engine.constants import (
    STEP_GENERATION,
    STEP_KEYWORD,
    STEP_PUBLISHING,
    STEP_VERIFICATION,
)


class Pipeline:

    def __init__(self):

        self.steps = [
            STEP_KEYWORD,
            STEP_GENERATION,
            STEP_VERIFICATION,
            STEP_PUBLISHING,
        ]

    def get_steps(self):

        return self.steps

    def execute(self, orchestrator, keyword):

        keyword_data = orchestrator.process_keyword(
            keyword
        )

        content = orchestrator.generate_content(
            keyword_data
        )

        verified_content = orchestrator.verify_content(
            content
        )

        published_result = orchestrator.publish_content(
            verified_content
        )

        return {
            "keyword": keyword_data,
            "content": content,
            "verified_content": verified_content,
            "published_result": published_result,
        }