import marimo

__generated_with = "0.14.13"
app = marimo.App(width="medium")


@app.cell
def _(mo):
    mo.md(r"""# Parsing Marimo Notebooks_Programmatically_With_Python""")
    return


@app.cell
def _(mo):
    mo.md(r"""How to get each cell and its type from a Marimo notebook via Python code.""")
    return


@app.cell
def _(mo):
    mo.md(r"""## Setup""")
    return


@app.cell
def _():
    import importlib
    import importlib.util
    import marimo as mo
    from pathlib import Path
    import sys
    return Path, importlib, mo


@app.cell
def _(mo):
    mo.md(r"""## Using importlib With a Marimo Notebook""")
    return


@app.cell
def _(mo):
    mo.md(r"""There appears to be no library for Marimo analogous to nbformat, which lets you read/write Jupyter notebooks from Python. I suppose because Marimo notebooks are already Python code. So let's try importlib.""")
    return


@app.cell
def _(importlib):
    importlib
    return


@app.cell
def _():
    return


@app.cell
def _():
    return


@app.cell
def _(Path, importlib):
    nb = Path("2025_07_28_Exploring_Marimo.py")
    spec = importlib.util.spec_from_file_location("exmo", nb)
    spec
    return (spec,)


@app.cell
def _(importlib, spec):
    module = importlib.util.module_from_spec(spec=spec)
    module
    return (module,)


@app.cell
def _(module):
    vars(module)
    return


@app.cell
def _(module):
    cells = {name: attr for name, attr in vars(module).items() if hasattr(attr, 'run')}
    cells
    return


@app.cell
def _(module, spec):
    spec.loader.exec_module(module)
    return


@app.cell
def _(module):
    vars(module)
    return


@app.cell
def _(module):
    cells2 = {name: attr for name, attr in vars(module).items() if hasattr(attr, 'run')}
    cells2
    return (cells2,)


@app.cell
def _(cells2):
    cells2.keys()
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
