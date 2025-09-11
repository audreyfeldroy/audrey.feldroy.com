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

POSTS_DIR = Path("posts/")


def get_notebook_paths() -> List[Path]:
    """
    Returns a sorted list of post paths in the POSTS_DIR directory.
    Accepts both .ipynb and .md files so posts can be notebooks or markdown.
    """
    patterns = ["*.ipynb", "*.md"]
    paths = []
    for pat in patterns:
        paths.extend(list(POSTS_DIR.glob(pat)))
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


def page_header(is_index: bool = False) -> List[Any]:
    """
    Returns the page header elements. If not index, wraps the title in a link.
    """
    h1 = air.H1("audrey.feldroy.com")
    if not is_index:
        h1 = air.A(h1, href="/")
    return [
        h1,
        air.P(
            "The experimental notebooks of Audrey M. Roy Greenfeld. This website and all its notebooks are open-source at ",
            air.A(
                "github.com/audreyfeldroy/audrey.feldroy.com",
                href="https://github.com/audreyfeldroy/audrey.feldroy.com",
            ),
        ),
    ]


def page_footer() -> Any:
    """
    Returns the page footer element.
    """
    return air.P(f"© 2024-{datetime.now().year} Audrey M. Roy Greenfeld")


def notebook_card(notebook_path: Path) -> Any:
    """
    Returns a card element for a notebook, showing its title, date, and summary.
    """
    # for listing/summary we only render the first two cells/lines
    if notebook_path.suffix == ".ipynb":
        notebook = get_notebook_cells(notebook_path=notebook_path)
    else:
        # simple markdown file: read first two lines as title/summary
        try:
            text = notebook_path.read_text(encoding="utf-8")
            lines = text.splitlines()
        except Exception:
            lines = ["Untitled", ""]
        notebook = [{"content": lines[0] if lines else "Untitled", "cell_type": "markdown"},
                    {"content": lines[1] if len(lines) > 1 else "", "cell_type": "markdown"}]
    date = get_date_from_filename(notebook_path.name) or datetime.now()
    # Defensive: check notebook has at least 2 cells
    title = notebook[0]["content"] if len(notebook) > 0 else "Untitled"
    summary = notebook[1]["content"] if len(notebook) > 1 else ""
    return air.Article(
        air.Header(
            air.H3(
                air.A(
                    title,
                    href=f"/posts/{notebook_path.stem}",
                )
            ),
            air.P(f"{date:%a, %b %-d, %Y}"),
            air.P(summary),
        )
    )


@app.page
def index():
    nb_paths = get_notebook_paths()
    # Ensure nb_paths is a Listo instance so .map() works
    nb_paths = L(nb_paths)
    return layout(
        air.Title("audrey.feldroy.com"),
        *page_header(is_index=True),
        air.Div(
            *nb_paths.map(notebook_card),
            # *get_nb_paths().map(notebook_card),
            # class_="grid",
        ),
        page_footer(),
    )


def StyledCell(cell: Dict[str, Any]) -> Any:
    """
    Renders a notebook cell as HTML, styled according to its type.
    """
    if cell["cell_type"] == "markdown":
        return air.Raw(markdown(cell["content"], HtmlRenderer))
    elif cell["cell_type"] == "raw":
        return air.Pre(cell["content"])
    elif cell["cell_type"] == "code":
        # Get the language from the cell's metadata, default to python
        language = (
            cell.get("metadata", {}).get("language_info", {}).get("name", "python")
        )
        try:
            lexer = get_lexer_by_name(language)
        except ValueError:
            lexer = PythonLexer()

        highlighted_text = highlight(cell["content"], lexer, FORMATTER)
        outputs = []
        for output in cell["outputs"]:
            for typ, value in output.get("data", {}).items():
                if typ == "text/markdown":
                    content = "\n".join(value)
                    outputs.append(markdown(content, HtmlRenderer))
                else:
                    content = "\n".join(value)
                    outputs.append(content)

        return air.Article(
            air.Header(air.Raw(highlighted_text)), *L(outputs).map(air.Raw)
        )

    logging.warning(f"Unknown cell type: {cell['cell_type']}")
    return ""


@app.get("/posts/{name}")
def notebook(name: str) -> Any:
    """
    Renders a notebook page by name, showing its title, summary, and cells.
    """
    # prefer .ipynb, fall back to .md
    ipynb_path = POSTS_DIR / f"{name}.ipynb"
    md_path = POSTS_DIR / f"{name}.md"
    if ipynb_path.exists():
        path = ipynb_path
        notebook = get_notebook_cells(path)
        date = get_date_from_filename(name)
        title = notebook[0]["content"] if len(notebook) > 0 else "Untitled"
        summary = notebook[1]["content"] if len(notebook) > 1 else ""
        cells = notebook[2:]
    elif md_path.exists():
        path = md_path
        date = get_date_from_filename(name)
        text = md_path.read_text(encoding="utf-8")
        lines = text.splitlines()
        title = lines[0] if lines else "Untitled"
        summary = lines[1] if len(lines) > 1 else ""
        # treat remaining lines as a single markdown cell
        cells = [{"content": "\n".join(lines[2:]), "cell_type": "markdown"}]
    else:
        return layout(air.Title("Not Found"), air.H1("Not Found"), page_footer())
    return layout(
        air.Title(title),
        *page_header(),
        air.Br(),
        air.H2(title),
        air.Style(STYLE_DEFINITION),
        air.P(f"by Audrey M. Roy Greenfeld | {date:%a, %b %-d, %Y}"),
        air.P(summary),
        air.Hr(),
    air.Div(*L(cells).map(StyledCell)),
        page_footer(),
    )


@app.get("/nbs/{name}")
def notebook_compat(name: str) -> Any:
    """Compatibility redirect from old /nbs/<name> URLs to /posts/<name>."""
    # air.redirect may not be available; return a small page that navigates to the new URL
    new_url = f"/posts/{name}"
    return layout(
        air.Title("Moved"),
        air.Raw(f"<meta http-equiv=\"refresh\" content=\"0; url={new_url}\">"),
        air.P("This post has moved to ", air.A(new_url, href=new_url)),
        page_footer(),
    )
