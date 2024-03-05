import os
from typing import Dict


class PromptBuilder:
    def __init__(
        self, prompts_dir: str, verbosity: str = "moderate", language: str = "en"
    ) -> None:
        self.prompts_dir: str = prompts_dir
        self.verbosity: str = verbosity
        self.language: str = language

    def get_prompt(self, prompt_name: str, code_content: str) -> str:
        """Constructs a full prompt based on a template, verbosity, and language settings.

        Args:
            prompt_name: The name of the prompt template to use.
            code_content: The code content to include in the prompt.

        Returns:
            The fully constructed prompt as a string.
        """
        base_prompt: str = self._read_prompt_template(prompt_name)
        prompt: str = self._build_prompt(base_prompt, code_content)
        return prompt

    def _read_prompt_template(self, prompt_name: str) -> str:
        """Reads a prompt template file.

        Args:
            prompt_name: The name of the prompt template to read.

        Returns:
            The content of the prompt template file.

        Raises:
            ValueError: If the prompt template file does not exist.
        """
        prompt_path: str = os.path.join(self.prompts_dir, f"{prompt_name}_prompt.txt")
        try:
            with open(prompt_path, "r", encoding="utf-8") as file:
                return file.read().strip()
        except FileNotFoundError:
            raise ValueError(f"The prompt template for {prompt_name} was not found.")

    def _build_prompt(self, base_prompt: str, content: str) -> str:
        """Builds the full prompt by incorporating verbosity and language settings.

        Args:
            base_prompt: The base prompt template content.
            content: The code content to include in the prompt.

        Returns:
            The full prompt string.
        """
        verbosity_part: str = self._get_verbosity_part()
        language_part: str = self._get_language_part()
        return f"{base_prompt}{verbosity_part}\n\n{content}{language_part}"

    def _get_verbosity_part(self) -> str:
        """Returns the verbosity part of the prompt based on the verbosity setting.

        Returns:
            The verbosity string to append to the prompt.
        """
        verbosity_levels: Dict[str, str] = {
            "high": "\n\nPlease provide a very detailed and specific output,\
                    including technical details if applicable.",
            "low": "\n\nPlease keep the output brief and to the point.",
            "moderate": "",
        }
        return verbosity_levels[self.verbosity]

    def _get_language_part(self) -> str:
        """Returns the language part of the prompt based on the language setting.

        Returns:
            The language string to append to the prompt,\
            or an empty string if the language is English.
        """
        return (
            f"\n\nPlease translate the output to {self.language}."
            if self.language != "en"
            else ""
        )
