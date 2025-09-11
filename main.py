import air
import json
import logging
import re
from typing import List, Dict, Any
from listo import listo as L
from pathlib import Path
from datetime import datetime
from mistletoe import markdown
from mistletoe.html_renderer import HtmlRenderer
from pygments import highlight
from pygments.lexers import get_lexer_by_name, PythonLexer
from pygments.formatters import HtmlFormatter

app = air.Air()
jinja = air.JinjaRenderer("templates")

STYLE = "monokai"
FORMATTER = HtmlFormatter(style=STYLE, cssclass=STYLE, prestyles="padding:10px 0;")
STYLE_DEFINITION = FORMATTER.get_style_defs(f".{STYLE}")

def layout(title, *content):
    return air.Html(
        air.Head(
            title,
        ),
        air.Body(*content)
    )

ARTICLES_DIR = Path("articles/")


def get_notebook_paths() -> List[Path]:
    """
    Returns a sorted list of post paths in the ARTICLES_DIR directory.
    Accepts both .ipynb and .md files so posts can be notebooks or markdown.
    """
    patterns = ["*.ipynb", "*.md"]
    paths = []
    for pat in patterns:
        paths.extend(list(ARTICLES_DIR.glob(pat)))
    return L(paths).sorted(reverse=True)


def get_date_from_filename(filename: str) -> datetime:
    """
    Extracts the date from a filename string like '2025-01-12-Get-Date-From-This.whatever'.

    Args:
        filename: The name of the file.

    Returns:
        A datetime object if a date is found, otherwise the current time.
    """
    match = re.search(r"^\d{4}-\d{2}-\d{2}", filename)
    if match:
        try:
            return datetime.fromisoformat(match.group(0))
        except ValueError:
            pass
    return datetime.now()


def get_notebook_cells(notebook_path: Path) -> List[Dict[str, Any]]:
    """
    Read a Jupyter notebook file and return all cells as a list of dictionaries.

    Args:
        notebook_path: Path to the .ipynb file

    Returns:
        List of dictionaries, each containing:
        - 'content': The cell's source code/markdown as a string
        - 'cell_type': The type of cell ('code', 'markdown', 'raw', etc.)
        - 'metadata': Any metadata associated with the cell
    """
    try:
        with open(notebook_path, "r", encoding="utf-8") as f:
            notebook_data = json.load(f)

        cells = []
        for cell in notebook_data.get("cells", []):
            try:
                # Join source lines if it's a list, otherwise use as-is
                source = cell.get("source", "")
                if isinstance(source, list):
                    source = "".join(source)

                cells.append(
                    {
                        "content": source,
                        "cell_type": cell.get("cell_type", "unknown"),
                        "metadata": cell.get("metadata", {}),
                        "outputs": cell.get("outputs", []),
                    }
                )
            except KeyError as e:
                logging.warning(
                    f"Skipping cell in {notebook_path} due to missing key: {e}"
                )
                continue

        return cells

    except (FileNotFoundError, json.JSONDecodeError) as e:
        logging.error(f"Error reading notebook {notebook_path}: {e}")
        return []


def get_post_dict(path: Path) -> dict:
    """
    Extracts title, formatted date, and summary from a notebook or markdown path.
    """
    date = get_date_from_filename(path.name)
    formatted_date = f"{date:%a, %b %-d, %Y}"
    if path.suffix == ".ipynb":
        notebook = get_notebook_cells(path)
        title = notebook[0]["content"] if len(notebook) > 0 else "Untitled"
        summary = notebook[1]["content"] if len(notebook) > 1 else ""
    else:
        try:
            text = path.read_text(encoding="utf-8")
            lines = text.splitlines()
            title = lines[0] if lines else "Untitled"
            summary = lines[1] if len(lines) > 1 else ""
        except:
            title = "Untitled"
            summary = ""
    return {"title": title, "date": date, "meta": formatted_date, "tease": summary, "url": f"/articles/{path.stem}"}




def page_footer() -> Any:
    """
    Returns the page footer element.
    """
    return air.P(f"© 2024-{datetime.now().year} Audrey M. Roy Greenfeld")


@app.page
def index(request: air.Request) -> Any:
    post_paths = get_notebook_paths()
    # Ensure nb_paths is a Listo instance so .map() works
    posts = L(post_paths).map(get_post_dict)
    return jinja(request, "index.html", {
        "posts": posts
    })
    # return layout(
    #     air.Title("audrey.feldroy.com"),
    #     *page_header(is_index=True),
    #     air.Div(
    #         *nb_paths.map(notebook_card),
    #         # *get_nb_paths().map(notebook_card),
    #         # class_="grid",
    #     ),
    #     page_footer(),
    # )


# StyledCell removed — rendering of cells is handled inline where needed.


@app.get("/articles/{name}")
def article(request: air.Request, name: str) -> Any:
    """
    Renders an article page by name, showing its title, summary, and cells.
    """
    md_path = ARTICLES_DIR / f"{name}.md"
    if md_path.exists():
        path = md_path
        date = get_date_from_filename(name)
        with open(md_path, "r", encoding="utf-8") as f:
            text = f.read()
        # Render full content
        content = markdown(text, HtmlRenderer)
        # Extract the first line as the title and strip leading '#' (markdown heading)
        lines = text.splitlines()
        raw_title = lines[0] if lines else "Untitled"
        # Remove leading hashes and surrounding whitespace, then trim
        title = re.sub(r"^\s*#+\s*", "", raw_title).strip()
        # Summary/description: second line if present (common pattern)
        summary = lines[1] if len(lines) > 1 else ""
    else:
        return air.Response("Not Found", status_code=404)
    
    return jinja(request, "article.html", {
        "title": title,
        "meta": f"{date:%a, %b %-d, %Y}",
        "description": summary,
        "content": content,
    })

@app.get("/nbs/{name}")
def notebook_compat(name: str) -> Any:
    """Compatibility redirect from old /nbs/<name> URLs to /articles/<name>."""
    # air.redirect may not be available; return a small page that navigates to the new URL
    new_url = f"/articles/{name}"
    return layout(
        air.Title("Moved"),
        air.Raw(f"<meta http-equiv=\"refresh\" content=\"0; url={new_url}\">"),
        air.P("This post has moved to ", air.A(new_url, href=new_url)),
        page_footer(),
    )
