from abc import ABC, abstractmethod


class BaseAIProvider(ABC):

    @abstractmethod
    def generate(self, prompt: str, **kwargs):
        pass

    @abstractmethod
    def embeddings(self, text: str):
        pass