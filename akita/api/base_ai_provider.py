from abc import ABC, abstractmethod
from typing import Optional, Any


class AIProvider(ABC):
    @abstractmethod
    def __init__(self, client, console):
        pass

    @abstractmethod
    def call_api(self, prompt: str, max_tokens: int, model: str) -> Optional[str]:
        pass

    @abstractmethod
    def get_langchain_provider(self) -> Any:
        """Returns a LangChain provider compatible with the AI provider."""
        pass

    @abstractmethod
    def get_langchain_embeddings(self) -> Any:
        """Returns LangChain embeddings compatible with the AI provider."""
        pass
