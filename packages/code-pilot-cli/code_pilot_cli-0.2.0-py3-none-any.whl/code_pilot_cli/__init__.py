"""
CodePilot CLI: Your customizable coding assistant for the command line interface (CLI).
"""

from typing import Optional
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel


# Constants
CHAT_LLM = "HuggingFaceH4/starchat2-15b-v0.1"
COMPLETION_LLM = "bigcode/starcoder2-15b"
SYSTEM_MESSAGE = {
    "role": "system",
    "content": "You are CodePilot, an advanced coding assistant powered by "
    "state-of-the-art Large Language Models, and specifically optimized for enhanced "
    "performance in coding tasks. You have the experience and knowledge of senior software"
    "engineer, site reliability engineer and cybersecurity engineer.",
}


# Syntax Highlighting
def print_highlighted(code: str, subtitle: Optional[str] = None) -> None:
    """
    Highlight and print the provided code.

    Args:
        code (str): The code to be highlighted and printed.
        subtitle (str, optional): An optional subtitle for the panel.

    Returns:
        None
    """

    console = Console()
    md = Markdown(code, code_theme="lightbulb")

    console.print(
        Panel(
            md,
            title_align="left",
            title="[bold yellow]CodePilot[/bold yellow]",
            subtitle=subtitle,
            subtitle_align="right",
        )
    )
