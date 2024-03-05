from rich.console import Console
from rich.markdown import Markdown
from rich.theme import Theme


custom_theme = Theme(
    {
        "info": "#6c7a89",
        "success": "#2ecc71",
        "error": "#e74c3c",
        "warning": "yellow",
        "path": "underline",
        "duration": "dim",
        "accent": "#3498db",
    }
)

console = Console(theme=custom_theme)


def print_error(message: str):
    console.print(f"[bold red]Error:[/bold red] {message}")


def print_success(message: str):
    console.print(f"[bold green]{message}[/bold green]")


def print_markdown(md_text: str):
    markdown = Markdown(md_text)
    console.print(markdown)
