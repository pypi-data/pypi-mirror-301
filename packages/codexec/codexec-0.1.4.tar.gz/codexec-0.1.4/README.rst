================
codexec
================

codexec is a Python package that allows you to execute code written in various programming languages
(C, C++, Java, Python, and JavaScript) by making API calls to a server. The package takes code files
and optional input files, executes the code, and returns the output.

Features
========

- Execute code in multiple languages: C, C++, Java, Python, and JavaScript.
- Simple command-line interface (CLI) for executing code files.
- Supports optional input files for code that requires input.
- Easy integration with environment variables for configuration.

.. Installation
.. ============
..
.. You can install codexec by running the following command::
..
..     pip install codexec
..
.. Usage
.. =====
..
.. To execute a code file, run the following command::
..
..     codexec run path_to_code_file
..
.. For example::
..
..     codexec run main.py
..
.. If your code requires input, you can also provide an input file::
..
..     codexec run main.py --input input.txt
..
.. Configuration
.. =============
..
.. Set up your `.env` file with the following variable::
..
..     CODE_ENGINE_URL=https://your-api-url
..
.. This URL is used to make API calls to execute the code.

