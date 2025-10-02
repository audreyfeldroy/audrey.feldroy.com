# Run Any Python CLI Instantly — No Install, No Virtualenv (uvx)

If you need to run Python applications from PyPI without installing them permanently, `uvx` provides a convenient way to execute Python tools without having to manage dependencies manually.

**TL;DR:** Run PyPI CLI tools on-demand in an ephemeral virtualenv — no permanent installs, no virtualenv management. Quick try: `uvx pyclean .` or `uvx ruff@latest check`. Great for one-offs, CI, demos, and reproducible one-line workflows.

## What is uvx?

`uvx` is a command-line tool from the `uv` package manager that allows you to run Python CLI tools from PyPI directly, without installing them permanently on your system. 

A quick note on how uvx fits into the ecosystem: unlike `pipx` (which installs and keeps isolated apps around), `uvx` creates a disposable environment for each run so you don't accumulate installed CLI tools. That makes it ideal for ad-hoc tasks, CI steps, and scripts where you want a clean environment every time.

## Using uvx

To run any Python tool from PyPI, you would run:

```sh
uvx tool_name [tool-options]
```

## Example: pyclean

For example, to run `pyclean` on the current directory to clean up your `*.pyc` files and `__pycache__` dirs:

```sh
uvx pyclean .
```

## Example: Instaloader

To download an Instagram post with shortcode `DPIzsnAEvNX`, you run:

```sh
uvx instaloader -- -DPIzsnAEvNX
```

Instaloader then creates a directory called -DPIzsnAEvNX containing:

* The .jpg from that Instagram post
* Its accompanying text
* A .json.xz file - compressed JSON metadata about the post

## Example: Cookiecutter

Or to run Cookiecutter, if the current directory is a Cookiecutter template that you want to generate starting project boilerplate from:

```sh
uvx cookiecutter .
```

## Example: Latest Version of Ruff

I thought by default `uvx <tool>` would always install the latest version of the tool, but it seems to cache the first version it installs. So if you want to ensure you always get the latest version, you can specify `@latest` like:

```sh
uvx ruff@latest check
```

This runs the latest version of `ruff` to check your code for linting issues.

## Better Living With uvx

In short, it makes your Python CLI tools work better:

- No need to create a virtual env
- No need to install tools permanently
- Clean execution environment for each run, with auto-cleanup after
- Easy access to any Python CLI tool on PyPI
- Avoids dependency conflicts with existing packages

## Security & Tradeoffs

A few things to keep in mind:

- Running code directly from PyPI executes arbitrary code. Do your due diligence knowing what you run, and be careful where you run unknown code!
- `uvx` caches the first version it installs for a package; use `@latest` when you explicitly want the newest release.
- Ephemeral runs mean a small startup latency compared to a permanently installed binary, and you need network access for first-run installs. I'm fine with it honestly.

## Cool Uses

I don't do all this yet, but AI tells me `uvx` is great for:

- In CI to keep build images small and avoid baking in lots of CLI tools.
- In Justfiles and deploy scripts for reproducible commands without installing system-wide tools.
