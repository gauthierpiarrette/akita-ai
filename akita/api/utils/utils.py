from akita.api.openai_provider import OpenAIProvider
from akita.api.google_genai_provider import GoogleGenAIProvider
from akita.api.base_ai_provider import AIProvider
import os


def get_ai_provider(client_type: str) -> AIProvider:
    if client_type == "openai":
        return OpenAIProvider()
    elif client_type == "google":
        return GoogleGenAIProvider()
    else:
        raise ValueError("Unsupported AI client type")
