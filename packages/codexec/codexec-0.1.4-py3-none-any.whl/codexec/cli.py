"""Console script for codexec.

This script provides a command-line interface (CLI) for executing code files
using the `codexec` package.

The user can specify the file path of the code to execute and an optional input
file for programs that require input.
"""

from codexec import exec_code
import typer
from rich.console import Console

app = typer.Typer()
console = Console()


@app.command()
def main(
    file_path: str = typer.Argument(
        ..., help="The path to the code file you want to execute."
    ),
    input_path: str = typer.Option(
        None, help="The path to the input file for the code (optional)."
    ),
):
    """
    Executes code from a file and optionally takes an input file.

    Parameters
    ----------
    file_path : str
        The path to the source code file to be executed.
    input_path : str, optional
        The path to the input file for the code (optional).

    Raises
    ------
    Exception
        If there is an error during the code execution process.
    """
    try:
        output = exec_code(file_path, input_path)
        typer.echo(output)
    except Exception as e:
        if str(e) != "":
            console.print(f"[red]error:[/red] {str(e)}")


if __name__ == "__main__":
    app()
