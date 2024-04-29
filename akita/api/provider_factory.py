import os
from typing import Dict, Type, Optional
from akita.api.base_ai_provider import AIProvider
from akita.api.openai_provider import OpenAIProvider
from akita.api.google_genai_provider import GoogleGenAIProvider
from akita.api.utils.config_loader import ConfigLoader


class ProviderFactory:
    _providers: Dict[str, Type[AIProvider]] = {
        "openai": OpenAIProvider,
        "google": GoogleGenAIProvider,
    }

    @staticmethod
    def get_provider(
        provider: str = None, model_overwrite: Optional[str] = None
    ) -> AIProvider:
        provider_name, provider_config = ConfigLoader.get_provider_config(provider)
        if provider_name not in ProviderFactory._providers:
            raise ValueError(
                f"Unsupported AI client type '{provider_name}'. Available types: {list(ProviderFactory._providers.keys())}"
            )

        api_key_env = provider_config.get("api_key_env")
        api_key = os.getenv(api_key_env)
        if not api_key:
            raise EnvironmentError(
                f"API key not found. Please set the {api_key_env} environment variable."
            )

        model = (
            model_overwrite
            if model_overwrite and model_overwrite in provider_config.get("options", [])
            else provider_config.get("model")
        )

        return ProviderFactory._providers[provider_name](
            api_key=api_key, model_name=model
        )
