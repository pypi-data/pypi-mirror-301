""" Command to generate shell commands """

from typing import Annotated, Optional
import typer
from huggingface_hub import InferenceClient
from rich import print
from code_pilot_cli import COMPLETION_LLM, print_highlighted


def completions(
    code: Annotated[
        Optional[str],
        typer.Option(
            "--code",
            "-c",
            help="Code snippet to complete.",
        ),
    ] = None,
    file: Annotated[
        Optional[typer.FileText],
        typer.Option(
            "--file",
            "-f",
            help="File to read the code snippet from.",
            encoding="utf-8",
        ),
    ] = None,
    language: Annotated[
        Optional[str],
        typer.Option(
            "--lang",
            "-l",
            help="Programming language of the code snippet.",
        ),
    ] = None,
    output: Annotated[
        Optional[typer.FileTextWrite],
        typer.Option(
            "--output",
            "-o",
            help="Output file to write the response to.",
            encoding="utf-8",
        ),
    ] = None,
    model: Annotated[
        Optional[str],
        typer.Option(
            "--model",
            "-m",
            help="The model to run inference with. Can be a model id hosted on the "
            "Hugging Face Hub, e.g. meta-llama/Meta-Llama-3-8B-Instruct or a URL "
            "to a deployed Inference Endpoint.",
        ),
    ] = COMPLETION_LLM,
) -> None:
    """
    Generate code completions based on the provided code snippet.

    Args:
        code (str): The code to complete.
        file (typer.FileText, optional): The file to read the code snippet from.
        language (str, optional): The programming language of the code snippet.
        output (typer.FileTextWrite, optional): The file to write the response to.
        model (str, optional): The model to run inference with.

    Returns:
        None

    Examples:
    ```shell
    # Generate code completions
    code-pilot completions "const greet = (name: string) =>"
    code-pilot completions -f main.rs

    # Generate code completions with a specific language
    code-pilot completions "fn say_hello(name: String) -> String:" -l rust

    # Save the output to a markdown file
    code-pilot completions "def list_files() -> List[str]:" -o code-completions.md

    # Change the model
    code-pilot completions "def list_files() -> List[str]:" -m meta-llama/Llama-3.2-3B-Instruct
    ```
    """

    # Input
    input = code if code else file.read() if file else ""

    if input == "":
        typer.Abort("No code snippet provided.")

    client = InferenceClient(model)

    try:
        response = client.text_generation(
            f"```{language if language else ''}\n{input}",
            max_new_tokens=512,
        )

        if output:
            with output as file:
                file.write(f"```{language if language else ''}\n{input + response}")

            print(f"Output [bold green]saved[/bold green] to {output.name}.")

        else:
            print_highlighted(f"```{language if language else ''}\n{input + response}")

    except Exception as error:
        print(f"[bold red]Error[/bold red]: {error}")
