"""Main module for codexec.

This module contains the core functionality for executing code in various
languages (C, C++, Java, Python, JavaScript) by making API calls to a server.

Functions:
----------
get_output(lang_code: int, input: str, code: str):
    Sends a POST request to execute code based on the provided language and input.

get_lang_code(file_path: str):
    Returns the language code based on the file extension.

read_code(file_path: str):
    Reads and returns the contents of the given code file.

read_input(input_path: str):
    Reads and returns the contents of the given input file.

exec_code(file_path: str, input_path: str):
    Executes the code from the provided file, with optional input, and returns the output.
"""

import os
import requests
import typer
from typing import Optional
from dotenv import load_dotenv
from rich.console import Console

load_dotenv()
console = Console()


def get_output(lang_code: int, input: str, code: str) -> dict:
    """
    Sends a code execution request to the external code execution API.

    Parameters
    ----------
    lang_code : int
        The code representing the programming language of the file.
    input : str
        The input for the code execution.
    code : str
        The actual code to be executed.

    Returns
    -------
    dict
        The JSON response from the code execution API, or an error message.
    """
    url = os.getenv("CODE_ENGINE_URL")
    payload = {"languageCode": lang_code, "input": input, "code": code}

    with console.status("[bold green]executing code...") as status:
        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}


def get_lang_code(file_path: str) -> int:
    """
    Returns the language code based on the file extension.

    Parameters
    ----------
    file_path : str
        The file path of the source code file.

    Returns
    -------
    int
        The language code corresponding to the file extension.
    """
    lang_code = -1
    _, ext = os.path.splitext(file_path)
    if ext[1:] == "c":
        lang_code = 50
    elif ext[1:] == "cpp":
        lang_code = 76
    elif ext[1:] == "java":
        lang_code = 62
    elif ext[1:] == "py":
        lang_code = 71
    elif ext[1:] == "js":
        lang_code = 63
    return lang_code


def read_code(file_path: str) -> str:
    """
    Reads and returns the contents of a source code file.

    Parameters
    ----------
    file_path : str
        The file path of the source code file.

    Returns
    -------
    str
        The contents of the file as a string.
    """
    with open(file_path, "r") as file:
        return file.read()


def read_input(input_path: str) -> str:
    """
    Reads and returns the contents of an input file.

    Parameters
    ----------
    input_path : str
        The file path of the input file.

    Returns
    -------
    str
        The contents of the input file as a string.
    """
    with open(input_path, "r") as file:
        return file.read()


def exec_code(file_path: str, input_path: Optional[str] = None):
    """
    Executes code based on the provided file path and optional input path.

    Parameters
    ----------
    file_path : str
        The file path of the source code file.
    input_path : str
        The file path of the input file (optional).

    Returns
    -------
    str
        The output from the code execution, or an error message.
    """
    code = ""
    input = ""
    lang_code = -1

    if file_path and file_path != "":
        code = read_code(file_path)
        lang_code = get_lang_code(file_path)
    else:
        typer.echo("please provide a code file.", err=True)
        raise typer.Exit(code=1)

    if lang_code == -1:
        typer.echo("language not supported.", err=True)
        raise typer.Exit(code=1)

    if input_path and input_path != "":
        input = read_input(input_path)

    response = get_output(lang_code, input, code)
    if isinstance(response, dict) and "data" in response:
        output = response["data"].get("stdout", "no output available")
        if output == None:
            output = response["data"].get("compile_output", "no output available")
        return output
    else:
        typer.echo("received unexpected output format.", err=True)
        raise typer.Exit(code=1)
