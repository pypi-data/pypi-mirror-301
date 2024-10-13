""" CodePilot CLI """

import typer
from code_pilot_cli.commands import command_list


# CLI
code_pilot = typer.Typer(
    name="code-pilot",
    no_args_is_help=True,
    rich_markup_mode="rich",
    help="CodePilot CLI, an advanced AI-powered customizable coding assistant.",
)

for command in command_list:
    code_pilot.command(no_args_is_help=True)(command)


if __name__ == "__main__":
    code_pilot()
