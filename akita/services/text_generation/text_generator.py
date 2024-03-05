from typing import Any, Dict, List, Optional, Union
from akita.services.text_generation.prompt_builder import PromptBuilder
from akita.services.text_generation.file_handler import FileHandler
from akita.api.openai_client import OpenAIClient
from .settings import Settings
from .utils import load_model_config
import os


class TextGenerator:
    """
    Generates various types of text content using OpenAI's GPT models,
    based on the provided code content.

    Attributes:
        model_config (Dict[str, Any]): Configuration for the models
                                       used in generating text.
        file_handler (FileHandler): Handles file operations,
                                    like reading files to get their content.
        chatgpt_client (OpenAIClient): Client for calling OpenAI's API to generate text.
        prompt_builder (PromptBuilder): Builds prompts for the AI based on templates.
    """

    def __init__(self) -> None:
        self.model_config: Dict[str, Any] = load_model_config(
            Settings.MODEL_CONFIG_FILE
        )
        self.file_handler: FileHandler = FileHandler()
        self.chatgpt_client: OpenAIClient = OpenAIClient()
        self.prompt_builder: PromptBuilder = PromptBuilder(
            prompts_dir=Settings.DEFAULT_PROMPT_DIR
        )

    def generate_docstring(
        self,
        input_data: Union[str, List[str]],
        model: str = "default",
        verbosity: Optional[str] = None,
        language: Optional[str] = None,
    ) -> Any:
        self._prepare_prompt_builder(verbosity, language)
        code_content: str = self._process_input(input_data)
        prompt: str = self.prompt_builder.get_prompt("docstring", code_content)
        return self.chatgpt_client.call_openai_api(
            prompt, max_tokens=3000, model=self.model_config[model]
        )

    def generate_inline_comments(
        self,
        input_data: Union[str, List[str]],
        model: str = "default",
        verbosity: Optional[str] = None,
        language: Optional[str] = None,
    ) -> Any:
        self._prepare_prompt_builder(verbosity, language)
        code_content: str = self._process_input(input_data)
        prompt: str = self.prompt_builder.get_prompt("inline_comments", code_content)
        return self.chatgpt_client.call_openai_api(
            prompt, max_tokens=4000, model=self.model_config[model]
        )

    def generate_description_files(
        self,
        input_data: Union[str, List[str]],
        model: str = "default",
        verbosity: Optional[str] = None,
        language: Optional[str] = None,
    ) -> Any:
        self._prepare_prompt_builder(verbosity, language)
        code_content: str = self._process_input(input_data)
        prompt: str = self.prompt_builder.get_prompt("describe_files", code_content)
        return self.chatgpt_client.call_openai_api(
            prompt, max_tokens=4000, model=self.model_config[model]
        )

    def generate_description_code_diff(
        self,
        input_data: Union[str, List[str]],
        model: str = "default",
        verbosity: Optional[str] = None,
        language: Optional[str] = None,
    ) -> Any:
        self._prepare_prompt_builder(verbosity, language)
        code_content: str = self._process_input(input_data)
        prompt: str = self.prompt_builder.get_prompt("describe_code_diff", code_content)
        return self.chatgpt_client.call_openai_api(
            prompt, max_tokens=500, model=self.model_config[model]
        )

    def generate_commit_message(
        self,
        input_data: Union[str, List[str]],
        model: str = "default",
        verbosity: Optional[str] = None,
        language: Optional[str] = None,
    ) -> Any:
        self._prepare_prompt_builder(verbosity, language)
        code_content: str = self._process_input(input_data)
        prompt: str = self.prompt_builder.get_prompt("commit_message", code_content)
        return self.chatgpt_client.call_openai_api(
            prompt, max_tokens=60, model=self.model_config[model]
        )

    def generate_readme(
        self,
        input_data: Union[str, List[str]],
        model: str = "default",
        verbosity: Optional[str] = None,
        language: Optional[str] = None,
    ) -> Any:
        self._prepare_prompt_builder(verbosity, language)
        code_content: str = self._process_input(input_data)
        prompt: str = self.prompt_builder.get_prompt("readme", code_content)
        return self.chatgpt_client.call_openai_api(
            prompt, max_tokens=3000, model=self.model_config[model]
        )

    def generate_review(
        self,
        input_data: Union[str, List[str]],
        model: str = "default",
        verbosity: Optional[str] = None,
        language: Optional[str] = None,
    ) -> Any:
        self._prepare_prompt_builder(verbosity, language)
        code_content: str = self._process_input(input_data)
        prompt: str = self.prompt_builder.get_prompt("review", code_content)
        return self.chatgpt_client.call_openai_api(
            prompt, max_tokens=3000, model=self.model_config[model]
        )

    def generate_tests(
        self,
        input_data: Union[str, List[str]],
        model: str = "default",
        verbosity: Optional[str] = None,
        language: Optional[str] = None,
    ) -> Any:
        self._prepare_prompt_builder(verbosity, language)
        code_content: str = self._process_input(input_data)
        prompt: str = self.prompt_builder.get_prompt("tests", code_content)
        return self.chatgpt_client.call_openai_api(
            prompt, max_tokens=3000, model=self.model_config[model]
        )

    def _prepare_prompt_builder(
        self, verbosity: Optional[str], language: Optional[str]
    ) -> None:
        self.prompt_builder.verbosity = (
            verbosity if verbosity else Settings.DEFAULT_VERBOSITY
        )
        self.prompt_builder.language = (
            language if language else Settings.DEFAULT_LANGUAGE
        )

    def _process_input(self, input_data: Union[str, List[str]]) -> str:
        if isinstance(input_data, list):
            valid_files: List[str] = [
                item
                for item in input_data
                if isinstance(item, str) and os.path.isfile(item)
            ]
            return self.file_handler.read_files(valid_files)
        elif isinstance(input_data, str):
            return input_data
        else:
            raise ValueError("Input data must be a list of file paths or a string")
