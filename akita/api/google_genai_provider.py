import google.generativeai as genai
from rich.console import Console
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from akita.api.base_ai_provider import AIProvider
from typing import Optional
import os


class GoogleGenAIProvider(AIProvider):
    def __init__(self, api_key: Optional[str] = None, model_name: str = "gemini-pro"):
        api_key = api_key or os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError(
                "API key is not provided. \
                Please set the GOOGLE_API_KEY environment variable."
            )
        if not model_name:
            raise ValueError("Model name is required but was not provided.")

        super().__init__(api_key, model_name)
        genai.configure(api_key=api_key)
        self.model_name = model_name
        self.model = genai.GenerativeModel(model_name=model_name)
        self.console = Console()

    def call_api(self, prompt: str, max_tokens: int, **kwargs) -> Optional[str]:
        try:
            with self.console.status("Processing...", spinner="dots"):
                generation_config = genai.types.GenerationConfig(
                    candidate_count=1,
                    stop_sequences=["x"],
                    max_output_tokens=max_tokens,
                    temperature=1.0,
                )
                response = self.model.generate_content(
                    prompt, generation_config=generation_config, **kwargs
                )
                if response and response.candidates:
                    return response.candidates[0].content.parts[0].text.strip()
                else:
                    self.console.print("Invalid or empty response from API.")
                    return None
        except Exception as e:
            self.console.print(f"Error during API call: {e}")
            return None

    def get_langchain_provider(self) -> ChatGoogleGenerativeAI:
        return ChatGoogleGenerativeAI(
            model="gemini-pro",
            temperature=0.7,
            top_p=0.85,
            convert_system_message_to_human=True,
        )

    def get_langchain_embeddings(self) -> GoogleGenerativeAIEmbeddings:
        return GoogleGenerativeAIEmbeddings(model="models/embedding-001")
