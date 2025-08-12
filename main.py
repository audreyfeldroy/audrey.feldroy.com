import air
import json
import logging
import re
from typing import Iterable, Generator, List, Dict, Any
from listo import listo as L
from pathlib import Path
from datetime import datetime
from mistletoe import markdown
from mistletoe.html_renderer import HtmlRenderer
from pygments import highlight
from pygments.lexers import get_lexer_by_name, PythonLexer, JsonLexer, BashLexer
from pygments.formatters import HtmlFormatter

app = air.Air()

STYLE = "monokai"
FORMATTER = HtmlFormatter(style=STYLE, cssclass=STYLE, prestyles="padding:10px 0;")
STYLE_DEFINITION = FORMATTER.get_style_defs(f".{STYLE}")

NBS_DIR = Path("nbs/")


def get_notebook_paths():
    return L(NBS_DIR.glob("*.ipynb")).sorted(reverse=True)


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


def page_header(is_index=False):
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


def page_footer():
    return air.P(f"© 2024-{datetime.now().year} Audrey M. Roy Greenfeld")


def tailwind_layout(*content):
    """Custom layout function using Tailwind CSS instead of Pico.css"""
    return air.Html(
        air.Head(
            air.Meta(charset="utf-8"),
            air.Meta(name="viewport", content="width=device-width, initial-scale=1"),
            air.Script(src="https://cdn.tailwindcss.com"),
        ),
        air.Body(
            air.Main(
                *content,
                class_="container mx-auto px-4 py-8 max-w-4xl"
            )
        )
    )


def notebook_card(notebook_path: Path):
    notebook = get_notebook_cells(notebook_path=notebook_path)
    date = get_date_from_filename(notebook_path.name) or datetime.now()
    return air.Article(
        air.Header(
            air.H3(
                air.A(
                    notebook[0]["content"],
                    href=f"/nbs/{notebook_path.stem}",
                )
            ),
            air.P(f"{date:%a, %b %-d, %Y}"),
            air.P(notebook[1]["content"]),
        )
    )


@app.page
def index():
    nb_paths = get_notebook_paths()
    return tailwind_layout(
        air.Title("audrey.feldroy.com"),
        *page_header(is_index=True),
        air.Div(
            *nb_paths.map(notebook_card),
            # *get_nb_paths().map(notebook_card),
            # class_="grid",
        ),
        page_footer(),
    )


def StyledCell(cell):
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


@app.get("/nbs/{name}")
def notebook(name: str):
    path = NBS_DIR / f"{name}.ipynb"
    notebook = get_notebook_cells(path)
    date = get_date_from_filename(name)
    return tailwind_layout(
        air.Title(notebook[0]["content"]),
        *page_header(),
        air.Br(),
        air.H2(notebook[0]["content"]),
        air.Style(STYLE_DEFINITION),
        air.P(f"by Audrey M. Roy Greenfeld | {date:%a, %b %-d, %Y}"),
        air.P(notebook[1]["content"]),
        air.Hr(),
        air.Div(*L(notebook[2:]).map(StyledCell)),
        page_footer(),
    )
