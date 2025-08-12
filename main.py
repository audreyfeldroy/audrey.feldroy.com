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
FORMATTER = HtmlFormatter(style=STYLE, cssclass=STYLE, prestyles="padding:1rem 0;")
STYLE_DEFINITION = FORMATTER.get_style_defs(f".{STYLE}")

# Tailwind CSS configuration
TAILWIND_CONFIG = """
<script src="https://cdn.tailwindcss.com"></script>
<script>
    tailwind.config = {
        theme: {
            extend: {
                fontFamily: {
                    'serif': ['Georgia', 'Times New Roman', 'serif'],
                    'sans': ['Inter', '-apple-system', 'BlinkMacSystemFont', 'sans-serif']
                },
                maxWidth: {
                    'reading': '65ch'
                }
            }
        }
    }
</script>
<style>
    .monokai {
        background: #2d2d2d !important;
        border-radius: 8px;
        padding: 1rem;
        overflow-x: auto;
        margin: 1.5rem 0;
    }
    .monokai pre {
        margin: 0 !important;
        padding: 0 !important;
        background: transparent !important;
        color: #f8f8f2;
        font-size: 0.875rem;
        line-height: 1.5;
    }
</style>
"""

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


def tailwind_layout(*children, title="audrey.feldroy.com"):
    """Custom layout using Tailwind CSS instead of Pico.css"""
    return air.Html(
        air.Head(
            air.Meta(charset="UTF-8"),
            air.Meta(name="viewport", content="width=device-width, initial-scale=1.0"),
            air.Title(title),
            air.Raw(TAILWIND_CONFIG),
            air.Style(STYLE_DEFINITION),
        ),
        air.Body(
            *children,
            class_="bg-white text-gray-900 font-sans antialiased"
        ),
        lang="en"
    )

def page_header(is_index=False):
    """Clean, minimal header with improved typography"""
    if is_index:
        h1 = air.H1(
            "audrey.feldroy.com",
            class_="text-2xl font-bold text-gray-900"
        )
    else:
        h1 = air.H1(
            air.A(
                "audrey.feldroy.com",
                href="/",
                class_="text-xl font-semibold text-gray-900 hover:text-blue-600 transition-colors"
            )
        )
    
    description = air.P(
        "The experimental notebooks of Audrey M. Roy Greenfeld. This website and all its notebooks are open-source at ",
        air.A(
            "github.com/audreyfeldroy/audrey.feldroy.com",
            href="https://github.com/audreyfeldroy/audrey.feldroy.com",
            class_="text-blue-600 hover:text-blue-800 underline"
        ),
        class_="text-gray-600 mt-2 text-sm leading-relaxed"
    )
    
    return air.Header(
        air.Div(
            h1,
            description if is_index else None,
            class_="max-w-4xl mx-auto px-4 py-6" if is_index else "max-w-3xl mx-auto px-4 py-6"
        ),
        class_="border-b border-gray-200 bg-white"
    )


def page_footer():
    """Clean, minimal footer"""
    return air.Footer(
        air.Div(
            air.P(
                f"© 2024-{datetime.now().year} Audrey M. Roy Greenfeld",
                class_="text-gray-500 text-sm"
            ),
            class_="max-w-4xl mx-auto px-4 py-6"
        ),
        class_="border-t border-gray-200 mt-16"
    )


def notebook_card(notebook_path: Path):
    """Modern card design for notebook entries"""
    notebook = get_notebook_cells(notebook_path=notebook_path)
    date = get_date_from_filename(notebook_path.name) or datetime.now()
    
    # Get title and description from first two cells
    title = notebook[0]["content"].strip() if notebook else "Untitled"
    description = notebook[1]["content"].strip() if len(notebook) > 1 else ""
    
    return air.Article(
        air.Header(
            air.H2(
                air.A(
                    title,
                    href=f"/nbs/{notebook_path.stem}",
                    class_="hover:text-blue-600 transition-colors"
                ),
                class_="text-xl font-bold text-gray-900 mb-2 leading-tight"
            ),
            air.Div(
                air.Time(
                    f"{date:%a, %b %-d, %Y}",
                    datetime=date.isoformat()[:10],
                    class_="text-sm text-gray-500"
                ),
                class_="flex items-center mb-3"
            ),
            air.P(
                description,
                class_="text-gray-700 leading-relaxed text-base"
            ) if description else None,
            class_="mb-4"
        ),
        class_="border-b border-gray-100 pb-8 last:border-b-0"
    )


@app.page
def index():
    """Homepage with modern Tailwind design"""
    nb_paths = get_notebook_paths()
    return tailwind_layout(
        page_header(is_index=True),
        air.Main(
            air.Div(
                *nb_paths.map(notebook_card),
                class_="space-y-8"
            ),
            class_="max-w-4xl mx-auto px-4 py-8"
        ),
        page_footer(),
        title="audrey.feldroy.com"
    )


def StyledCell(cell):
    """Render notebook cells with improved styling"""
    if cell["cell_type"] == "markdown":
        return air.Div(
            air.Raw(markdown(cell["content"], HtmlRenderer)),
            class_="text-gray-800 leading-relaxed"
        )
    elif cell["cell_type"] == "raw":
        return air.Pre(
            cell["content"],
            class_="bg-gray-50 p-4 rounded-lg text-sm overflow-x-auto"
        )
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

        return air.Div(
            air.Raw(highlighted_text),
            *L(outputs).map(lambda x: air.Div(
                air.Raw(x) if isinstance(x, str) and x.strip().startswith('<') else air.Pre(x, class_="bg-gray-50 p-4 rounded-lg text-sm mt-4"),
                class_="mt-4"
            )) if outputs else [],
            class_="space-y-4"
        )

    logging.warning(f"Unknown cell type: {cell['cell_type']}")
    return ""


@app.get("/nbs/{name}")
def notebook(name: str):
    """Individual notebook page with improved typography and layout"""
    path = NBS_DIR / f"{name}.ipynb"
    notebook = get_notebook_cells(path)
    date = get_date_from_filename(name)
    
    title = notebook[0]["content"].strip() if notebook else "Untitled"
    description = notebook[1]["content"].strip() if len(notebook) > 1 else ""
    
    return tailwind_layout(
        page_header(is_index=False),
        air.Main(
            # Article Header
            air.Header(
                air.H1(
                    title,
                    class_="text-3xl font-bold text-gray-900 mb-4 leading-tight"
                ),
                air.Div(
                    air.Span("by Audrey M. Roy Greenfeld", class_="text-sm text-gray-500"),
                    air.Span("•", class_="mx-2 text-sm text-gray-500"),
                    air.Time(
                        f"{date:%a, %b %-d, %Y}",
                        datetime=date.isoformat()[:10],
                        class_="text-sm text-gray-500"
                    ),
                    class_="flex items-center mb-4"
                ),
                air.P(
                    description,
                    class_="text-lg text-gray-700 leading-relaxed"
                ) if description else None,
                class_="mb-8 pb-8 border-b border-gray-100"
            ),
            # Article Content
            air.Article(
                air.Div(
                    *L(notebook[2:]).map(StyledCell),
                    class_="space-y-6"
                ),
                class_="prose prose-lg max-w-none"
            ),
            class_="max-w-3xl mx-auto px-4 py-8"
        ),
        page_footer(),
        title=f"{title} - audrey.feldroy.com"
    )
