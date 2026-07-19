"""
Base LLM provider interface.
"""


class BaseProvider:

    def generate(
        self,
        prompt,
        **kwargs,
    ):

        raise NotImplementedError(
            "LLM provider must implement generate()"
        )