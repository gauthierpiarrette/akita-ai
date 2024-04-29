from typing import Any, List, Optional, Union
import os
from akita.services.text_generation.prompt_builder import PromptBuilder
from akita.services.text_generation.file_handler import FileHandler
from akita.api.base_ai_provider import AIProvider
from akita.api.provider_factory import ProviderFactory
from .settings import Settings


class TextGenerator:
    """
    Generates various types of text content using AI models,
    based on the provided code content.

    Attributes:
        file_handler (FileHandler): Handles file operations,
                                    like reading files to get their content.
        ai_provider (AIProvider): An AI provider conforming to the AIProvider interface,
                              used to generate text.
        prompt_builder (PromptBuilder): Builds prompts for the AI based on templates.
    """

    def __init__(self) -> None:
        self.file_handler: FileHandler = FileHandler()
        self.ai_provider: AIProvider = ProviderFactory.get_provider()
        self.prompt_builder: PromptBuilder = PromptBuilder(
            prompts_dir=Settings.DEFAULT_PROMPT_DIR
        )

    def generate_docstring(
        self,
        input_data: Union[str, List[str]],
        verbosity: Optional[str] = None,
        language: Optional[str] = None,
    ) -> Any:
        self._prepare_prompt_builder(verbosity, language)
        code_content: str = self._process_input(input_data)
        prompt: str = self.prompt_builder.get_prompt("docstring", code_content)
        return self.ai_provider.call_api(prompt, max_tokens=3000)

    def generate_inline_comments(
        self,
        input_data: Union[str, List[str]],
        verbosity: Optional[str] = None,
        language: Optional[str] = None,
    ) -> Any:
        self._prepare_prompt_builder(verbosity, language)
        code_content: str = self._process_input(input_data)
        prompt: str = self.prompt_builder.get_prompt("inline_comments", code_content)
        return self.ai_provider.call_api(prompt, max_tokens=4000)

    def generate_description_files(
        self,
        input_data: Union[str, List[str]],
        verbosity: Optional[str] = None,
        language: Optional[str] = None,
    ) -> Any:
        self._prepare_prompt_builder(verbosity, language)
        code_content: str = self._process_input(input_data)
        prompt: str = self.prompt_builder.get_prompt("describe_files", code_content)
        return self.ai_provider.call_api(prompt, max_tokens=4000)

    def generate_description_code_diff(
        self,
        input_data: Union[str, List[str]],
        verbosity: Optional[str] = None,
        language: Optional[str] = None,
    ) -> Any:
        self._prepare_prompt_builder(verbosity, language)
        code_content: str = self._process_input(input_data)
        prompt: str = self.prompt_builder.get_prompt("describe_code_diff", code_content)
        return self.ai_provider.call_api(prompt, max_tokens=500)

    def generate_commit_message(
        self,
        input_data: Union[str, List[str]],
        verbosity: Optional[str] = None,
        language: Optional[str] = None,
    ) -> Any:
        self._prepare_prompt_builder(verbosity, language)
        code_content: str = self._process_input(input_data)
        prompt: str = self.prompt_builder.get_prompt("commit_message", code_content)
        return self.ai_provider.call_api(prompt, max_tokens=60)

    def generate_readme(
        self,
        input_data: Union[str, List[str]],
        verbosity: Optional[str] = None,
        language: Optional[str] = None,
    ) -> Any:
        self._prepare_prompt_builder(verbosity, language)
        code_content: str = self._process_input(input_data)
        prompt: str = self.prompt_builder.get_prompt("readme", code_content)
        return self.ai_provider.call_api(prompt, max_tokens=3000)

    def generate_review(
        self,
        input_data: Union[str, List[str]],
        verbosity: Optional[str] = None,
        language: Optional[str] = None,
    ) -> Any:
        self._prepare_prompt_builder(verbosity, language)
        code_content: str = self._process_input(input_data)
        prompt: str = self.prompt_builder.get_prompt("review", code_content)
        return self.ai_provider.call_api(prompt, max_tokens=3000)

    def generate_tests(
        self,
        input_data: Union[str, List[str]],
        verbosity: Optional[str] = None,
        language: Optional[str] = None,
    ) -> Any:
        self._prepare_prompt_builder(verbosity, language)
        code_content: str = self._process_input(input_data)
        prompt: str = self.prompt_builder.get_prompt("tests", code_content)
        return self.ai_provider.call_api(prompt, max_tokens=3000)

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
