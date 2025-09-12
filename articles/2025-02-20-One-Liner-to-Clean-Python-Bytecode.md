# One-Liner to Clean Python Bytecode

How to remove stale .pyc files and __pycache__ directories, using uvx + pyclean.

## Overview

I like to use the [PyClean](https://github.com/bittner/pyclean) tool by [Peter Bittner](https://peter.bittner.it/) like this:

```sh
uvx pyclean .
```

This one-liner:

1. Creates an ephemeral virtualenv with `uvx`
2. Installs pyclean from PyPI into it
3. Runs it to remove all Python bytecode files from the current dir, recursively
4. Auto-deletes the venv, including pyclean

## Example

Here I run it on several of my git repos:

```sh
(uv) fun % uvx pyclean .
Cleaning directory .
Total 93 files, 34 directories removed.
```

## uvx and the uv Tool Interface

`uvx` is an alias for `uv tool run`, part of the [uv Python package manager](https://github.com/astral-sh/uv). 

It creates a single-use disposable virtualenv for whatever tool you install and run with it. Here the tool name matches the PyPI package name, but it does also support uvx `<package-name>:<command-name>`.
