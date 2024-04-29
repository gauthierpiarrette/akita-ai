import toml
from typing import Dict
from pathlib import Path


class ConfigLoader:
    _config: Dict = None
    _config_path = Path(__file__).parent.parent / "config.toml"

    @classmethod
    def load_config(cls) -> None:
        if cls._config is None:
            cls._config = toml.load(cls._config_path)

    @classmethod
    def get_provider_config(cls, provider: str = None) -> Dict:
        cls.load_config()
        provider = provider or cls._config["providers"]["default"]
        return provider, cls._config.get(provider, {})
