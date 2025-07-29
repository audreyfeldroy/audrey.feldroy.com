import marimo

__generated_with = "0.14.13"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""# Exploring Marimo""")
    return


@app.cell
def _(mo):
    mo.md(r"""This is an experiment to see if I like blogging with Marimo enough to migrate my Jupyter notebook-powered blog over entirely.""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## Setup""")
    return


@app.cell
def _():
    import marimo as mo
    import math
    return math, mo


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## Plan""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    1. Play around in here with blogging about something interesting and tiny, and not too far off from the topic of this post.
    2. Create an Air view in my site that renders a Marimo blog post as HTML

    Um, so we haven't officially launched Air yet, so I'll gloss over that for now, but big announcement forthcoming.
    """
    )
    return


@app.cell
def _(mo):
    mo.md(r"""## Marimo Interactivity""")
    return


@app.cell
def _(mo):
    mo.md(r"""I love the reactive UI components in Marimo! I didn't realize until now how much I missed this similar thing from Observable notebooks.""")
    return


@app.cell
def _(mo):
    x = mo.ui.slider(1,9)
    x
    return (x,)


@app.cell
def _(math, mo, x):
    mo.md(f"""$e^{x.value} = {math.exp(x.value):0.3f}$""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## Exporting Marimo to HTML""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    I guess the easiest way for me to publish this as a blog post is to just export this notebook as HTML with:

    ```sh
    marimo export html notebook.py -o notebook.html
    ```

    and then add a view to show HTML pages on this site.

    Specifically for this notebook, I created an `html` directory at the same level as `nbs` and then ran:

    ```sh
    marimo export html 2025-07-28-Exploring-Marimo.py -o ../html/2025-07-28-Exploring-Marimo.html
    ```
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## Final Thoughts""")
    return


@app.cell
def _(mo):
    mo.md(
        r"""
    This will work for now, but for optimal workflow I wouldn't want to export posts manually. Ideas I'm considering:

    - Dynamically generate the HTML in an Air view
    - Create an Air Tag for it
    - Put the Marimo-generated HTML or a subset of it into my main site layout via a Jinja template
    - Use a GitHub action to auto-export new posts
    - Revisit Air static site generation
    """
    )
    return


if __name__ == "__main__":
    app.run()
