import air
import ast
import json
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

style = "monokai"
formatter = HtmlFormatter(style=style, cssclass=style, prestyles="padding:10px 0;")
style_definition = formatter.get_style_defs(f".{style}")


def get_notebook_paths():
    root = Path("nbs/")
    return L(root.glob("*.ipynb")).sorted(reverse=True)


def get_date_from_iso8601_prefix(fname):
    "Gets date from first 10 chars YYYY-MM-DD of `fname`, where `fname` is like `2025-01-12-Get-Date-From-This.whatever"
    try:
        return datetime.fromisoformat(str(fname)[0:10])
    except ValueError:
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

        return cells

    except (FileNotFoundError, json.JSONDecodeError, KeyError) as e:
        print(f"Error reading notebook {notebook_path}: {e}")
        return []


def notebook_card(notebook_path: Path):
    notebook = get_notebook_cells(notebook_path=notebook_path)
    date = get_date_from_iso8601_prefix(notebook_path.name) or datetime.now()
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
    return air.layouts.picocss(
        air.Title("audrey.feldroy.com"),
        air.H1("audrey.feldroy.com"),
        air.P(
            "The experimental notebooks of Audrey M. Roy Greenfeld. This website and all its notebooks are open-source at ",
            air.A(
                "github.com/audreyfeldroy/audrey.feldroy.com",
                href="https://github.com/audreyfeldroy/audrey.feldroy.com",
            ),
        ),
        air.Div(
            *nb_paths.map(notebook_card),
            # *get_nb_paths().map(notebook_card),
            # class_="grid",
        ),
        air.P(f"© 2024-{datetime.now().year} Audrey M. Roy Greenfeld"),
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

        highlighted_text = highlight(cell["content"], lexer, formatter)
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

    return "blarg"


@app.get("/nbs/{name}")
def notebook(name: str):
    path = Path(f"nbs/{name}.ipynb")
    notebook = get_notebook_cells(path)
    date = get_date_from_iso8601_prefix(name)
    return air.layouts.picocss(
        air.Title(notebook[0]["content"]),
        air.A(
            air.H1("audrey.feldroy.com"),
            href="/",
        ),
        air.P(
            "The experimental notebooks of Audrey M. Roy Greenfeld. This website and all its notebooks are open-source at ",
            air.A(
                "github.com/audreyfeldroy/audrey.feldroy.com",
                href="https://github.com/audreyfeldroy/audrey.feldroy.com",
            ),
        ),
        air.Br(),
        air.H2(notebook[0]["content"]),
        air.Style(style_definition),
        air.P(f"by Audrey M. Roy Greenfeld | {date:%a, %b %-d, %Y}"),
        air.P(notebook[1]["content"]),
        air.Hr(),
        air.Div(*L(notebook[2:]).map(StyledCell)),
    )


def get_marimo_cells(path: Path) -> List[Dict[str, Any]]:
    """
    Read a Marimo notebook file and return all cells as a list of dictionaries.
    """
    try:
        source = path.read_text(encoding="utf-8")
        tree = ast.parse(source, filename=path.name)
        cells = []

        for node in tree.body:
            if isinstance(node, ast.FunctionDef):
                is_marimo_cell = False
                hide_code = False
                for decorator in node.decorator_list:
                    decorator_name = ""
                    if (
                        isinstance(decorator, ast.Call)
                        and isinstance(decorator.func, ast.Attribute)
                        and isinstance(decorator.func.value, ast.Name)
                    ):
                        decorator_name = (
                            f"{decorator.func.value.id}.{decorator.func.attr}"
                        )

                    if decorator_name == "app.cell":
                        is_marimo_cell = True
                        for keyword in decorator.keywords:
                            if (
                                keyword.arg == "hide_code"
                                and isinstance(keyword.value, ast.Constant)
                                and keyword.value.value is True
                            ):
                                hide_code = True
                        break

                if is_marimo_cell:
                    cell_type = "code"
                    content = ""

                    # Simple case: single mo.md("...") call
                    if (
                        len(node.body) == 1
                        and isinstance(node.body[0], ast.Expr)
                        and isinstance(node.body[0].value, ast.Call)
                        and isinstance(node.body[0].value.func, ast.Attribute)
                        and node.body[0].value.func.attr == "md"
                        and node.body[0].value.args
                        and isinstance(node.body[0].value.args[0], ast.Constant)
                    ):
                        content = node.body[0].value.args[0].s
                        cell_type = "markdown"
                    else:
                        # Otherwise, treat the whole function body as code
                        content = "\n".join(
                            ast.get_source_segment(source, n) for n in node.body
                        )

                    cells.append(
                        {
                            "content": content,
                            "cell_type": cell_type,
                            "hide_code": hide_code,
                        }
                    )
        return cells
    except Exception as e:
        print(f"Error reading marimo notebook {path}: {e}")
        return []


def StyledMarimoCell(cell):
    if cell["hide_code"] and cell["cell_type"] == "code":
        return ""

    if cell["cell_type"] == "markdown":
        return air.Raw(markdown(cell["content"], HtmlRenderer))
    elif cell["cell_type"] == "code":
        highlighted_text = highlight(cell["content"], PythonLexer(), formatter)
        return air.Raw(highlighted_text)

    return ""


@app.get("/marimo/{name}")
def marimo_notebook(name: str):
    path = Path(f"nbs/{name}.py")
    cells = get_marimo_cells(path)
    date = get_date_from_iso8601_prefix(name)

    title = "Marimo Notebook"
    description = ""

    md_cells = [c["content"] for c in cells if c["cell_type"] == "markdown"]
    if len(md_cells) > 0:
        # Remove markdown heading characters from title
        title = md_cells[0].lstrip("# ").strip()
    if len(md_cells) > 1:
        description = md_cells[1]

    return air.layouts.picocss(
        air.Title(title),
        air.A(
            air.H1("audrey.feldroy.com"),
            href="/",
        ),
        air.P(
            "The experimental notebooks of Audrey M. Roy Greenfeld. This website and all its notebooks are open-source at ",
            air.A(
                "github.com/audreyfeldroy/audrey.feldroy.com",
                href="https://github.com/audreyfeldroy/audrey.feldroy.com",
            ),
        ),
        air.Br(),
        air.H2(title),
        air.Style(style_definition),
        air.P(f"by Audrey M. Roy Greenfeld | {date:%a, %b %-d, %Y}"),
        air.P(description),
        air.Hr(),
        air.Div(*L(cells).map(StyledMarimoCell)),
    )
