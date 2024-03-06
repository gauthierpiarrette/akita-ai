import os


class Settings:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    AKITA_DIR = ".akita"
    DEFAULT_VERBOSITY = "moderate"
    DEFAULT_LANGUAGE = "en"
    DEFAULT_PROMPT_DIR = os.path.join(BASE_DIR, "prompts")
    MODEL_CONFIG_FILE = os.path.join(BASE_DIR, "models.json")
