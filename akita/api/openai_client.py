from typing import Optional
from openai import OpenAI
from akita.utils.console import console
from rich.console import Console


class OpenAIClient:
    def __init__(
        self,
        openai_client: Optional[OpenAI] = None,
        rich_console: Optional[Console] = None,
    ) -> None:
        self.openai_client = openai_client if openai_client is not None else OpenAI()
        self.console = rich_console if rich_console is not None else console

    def call_openai_api(
        self, prompt: str, max_tokens: int, model: str = "gpt-4-0125-preview"
    ) -> Optional[str]:
        try:
            with self.console.status("Processing...", spinner="dots"):
                response = self.openai_client.chat.completions.create(
                    model=model,
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=max_tokens,
                )
                if response.choices and response.choices[0].message:
                    return response.choices[0].message.content.strip()
                else:
                    print("Invalid response structure from OpenAI API")
                    return None
        except Exception as e:
            print(f"Error in OpenAI API call: {e}")
            return None
