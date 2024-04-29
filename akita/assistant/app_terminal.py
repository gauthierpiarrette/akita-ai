import asyncio
from rich.console import Console
from prompt_toolkit import PromptSession
from rich.panel import Panel
from prompt_toolkit.styles import Style
from prompt_toolkit.history import InMemoryHistory
from akita.assistant.config import SEARCH_TYPE, SEARCH_K, HELP_MESSAGE
from akita.assistant.rag_chain import RAGChain
from akita.api.provider_factory import ProviderFactory
from typing import NoReturn
from langchain.schema.runnable import RunnablePassthrough


console = Console()

# Define a custom style for the prompt
custom_style = Style.from_dict({"prompt": "#248542"})


class TerminalChat:
    """A terminal-based chat interface for interacting with the Akita Assistant.

    This class provides an interactive command-line interface for users to interact
    with the Akita Assistant.

    Attributes:
        session (PromptSession): A prompt session for capturing user input.
        rag_chain (RAGChain): The conversational retrieval chain
            responsible for processing user queries and generating responses.
    """

    def __init__(self) -> None:
        """Initializes the TerminalChat with a custom prompt session
        and setups up the assistant."""
        self.session: PromptSession = PromptSession(
            history=InMemoryHistory(), style=custom_style
        )
        self.setup()

    def setup(self) -> None:
        """Sets up the conversational components and the QA chain for the assistant.

        Loads documents, splits texts, creates the database, and initializes the
        conversational retrieval chain.
        """
        ai_provider = ProviderFactory.get_provider()
        self.rag_chain: RunnablePassthrough = RAGChain(
            ai_provider, SEARCH_TYPE, SEARCH_K
        ).create_runnable()

    def process_answer(self, response: str) -> str:
        """Processes the response from the QA chain to generate a human-readable answer.

        Args:
            response (str): The response from the QA chain.

        Returns:
            str: The processed answer ready to be displayed to the user.
        """
        answer: str = response
        return answer

    async def handle_user_input(self, user_input: str) -> NoReturn:
        """Asynchronously handles user input, processing it
           through the QA chain and displaying the response.

        Args:
            user_input (str): The user's input string to be processed.

        Raises:
            NoReturn: This function is designed to run indefinitely,
            handling user input.
        """
        with console.status("Thinking...", spinner="dots"):
            response = self.rag_chain.invoke(user_input)

        answer = self.process_answer(response)
        chat_response = f"[blue]Akita:[/blue] {answer}"
        console.print(chat_response)

    def display_help(self) -> None:
        """Displays help information about using the Akita Assistant."""
        help_panel: Panel = Panel(HELP_MESSAGE, title="Help", expand=False)
        console.print(help_panel)

    def run(self) -> NoReturn:
        """Runs the main event loop, displaying the welcome message and processing user inputs.

        This method sets up the event loop, captures user inputs, and handles clean-up
        and exit procedures.
        """
        console.print("Welcome to the Akita Assistant!", style="blue")
        self.display_help()

        loop = asyncio.get_event_loop()

        while True:
            try:
                user_input: str = self.session.prompt("You: ")
                if user_input.lower() in ["exit", "quit"]:
                    console.print("Exiting...", style="red")
                    break
                loop.run_until_complete(self.handle_user_input(user_input))
            except KeyboardInterrupt:
                console.print("\nExiting...", style="red")
                break
            except Exception as e:
                console.print(f"Error: {e}", style="red")

        loop.close()
