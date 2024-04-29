import openai
from rich.console import Console
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from akita.api.base_ai_provider import AIProvider
from typing import Optional
import os


class OpenAIProvider(AIProvider):
    def __init__(
        self, api_key: Optional[str] = None, model_name: str = "gpt-4-0125-preview"
    ):
        if not api_key:
            api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError(
                "API key is required for OpenAIProvider. Please set the OPENAI_API_KEY environment variable."
            )
        if not model_name:
            raise ValueError("Model name is required but was not provided.")

        super().__init__(api_key, model_name)
        openai.api_key = api_key
        self.model_name = model_name
        self.model = model_name
        self.console = Console()

    def call_api(self, prompt: str, max_tokens: int, **kwargs) -> Optional[str]:
        try:
            with self.console.status("Processing...", spinner="dots"):
                response = openai.chat.completions.create(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=max_tokens,
                    **kwargs,
                )
                if response.choices and response.choices[0].message:
                    return response.choices[0].message.content.strip()
                else:
                    print("Invalid response structure from OpenAI API")
                    return None
        except Exception as e:
            print(f"Error in OpenAI API call: {e}")
            return None

    def get_langchain_provider(self) -> ChatOpenAI:
        return ChatOpenAI(model_name=self.model_name)

    def get_langchain_embeddings(self) -> OpenAIEmbeddings:
        return OpenAIEmbeddings(disallowed_special=())
