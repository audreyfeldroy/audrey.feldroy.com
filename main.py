import air
import io
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
from PIL import Image, ImageDraw, ImageFont
from starlette.responses import Response

app = air.Air()
app.mount("/static", air.StaticFiles(directory="static"), name="static")

jinja = air.JinjaRenderer("templates")

STYLE = "monokai"
FORMATTER = HtmlFormatter(style=STYLE, cssclass=STYLE, prestyles="padding:10px; white-space: pre-wrap; word-break: break-word; overflow-x: auto;")
STYLE_DEFINITION = FORMATTER.get_style_defs(f".{STYLE}")


STATIC_DIR = Path(__file__).parent / "static"
FONTS_DIR = STATIC_DIR / "fonts"
OG_BASE = Image.open(STATIC_DIR / "og-base.png")
SCALE = OG_BASE.width / 1200  # 2x for retina screenshots

FONT_TITLE = ImageFont.truetype(str(FONTS_DIR / "SourceSerif4-Bold.ttf"), int(48 * SCALE))
FONT_DATE = ImageFont.truetype(str(FONTS_DIR / "Inter-SemiBold.ttf"), int(13 * SCALE))
FONT_SUBTITLE = ImageFont.truetype(str(FONTS_DIR / "SourceSerif4-Regular.ttf"), int(20 * SCALE))

COLOR_TITLE = "#1a1a1a"
COLOR_DATE = "#c85d3b"
COLOR_SUBTITLE = "#6b6b6b"

# Content area matches the CSS: top 56px, left 72px, right 80px, bottom 68px
OG_CONTENT_LEFT = int(72 * SCALE)
OG_CONTENT_RIGHT = int((1200 - 80) * SCALE)
OG_TITLE_MAX_WIDTH = int(900 * SCALE)
OG_SUBTITLE_MAX_WIDTH = int(740 * SCALE)


def wrap_text(text: str, font: ImageFont.FreeTypeFont, max_width: int) -> list[str]:
    """Word-wrap text to fit within max_width pixels."""
    words = text.split()
    lines = []
    current = ""
    for word in words:
        test = f"{current} {word}".strip()
        bbox = font.getbbox(test)
        if bbox[2] - bbox[0] <= max_width:
            current = test
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines or [""]


def generate_og_jpg(title: str, meta: str, description: str) -> bytes:
    """Render title, date, and description onto the OG base image, return JPEG bytes."""
    img = OG_BASE.copy()
    draw = ImageDraw.Draw(img)

    # Vertically center the text block in the content area (top=56, bottom=68, total height=630)
    content_top = int(56 * SCALE)
    content_bottom = int((630 - 68) * SCALE)

    # Measure all text blocks to center vertically
    date_text = meta.upper()
    title_lines = wrap_text(title, FONT_TITLE, OG_TITLE_MAX_WIDTH)
    desc_lines = wrap_text(description, FONT_SUBTITLE, OG_SUBTITLE_MAX_WIDTH)[:3]

    line_height_title = int(48 * SCALE * 1.15)
    line_height_subtitle = int(20 * SCALE * 1.55)
    date_height = int(13 * SCALE)
    gap_date_title = int(20 * SCALE)
    gap_title_desc = int(20 * SCALE)

    total_height = (
        date_height + gap_date_title
        + line_height_title * len(title_lines)
        + gap_title_desc
        + line_height_subtitle * len(desc_lines)
    )

    y = content_top + (content_bottom - content_top - total_height) // 2

    # Date (uppercase, tracked)
    draw.text((OG_CONTENT_LEFT, y), date_text, fill=COLOR_DATE, font=FONT_DATE)
    y += date_height + gap_date_title

    # Title
    for line in title_lines:
        draw.text((OG_CONTENT_LEFT, y), line, fill=COLOR_TITLE, font=FONT_TITLE)
        y += line_height_title
    y += gap_title_desc

    # Description
    for line in desc_lines:
        draw.text((OG_CONTENT_LEFT, y), line, fill=COLOR_SUBTITLE, font=FONT_SUBTITLE)
        y += line_height_subtitle

    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=90)
    return buf.getvalue()


class CustomHTMLRenderer(HtmlRenderer):
    def render_block_code(self, token):
        code = token.children[0].content
        language = token.language
        if language:
            try:
                lexer = get_lexer_by_name(language)
            except:
                lexer = get_lexer_by_name('python')  # fallback to Python
        else:
            lexer = get_lexer_by_name('python')  # default to Python
        highlighted = highlight(code, lexer, FORMATTER)
        # Ensure long lines are wrapped properly
        return highlighted

def layout(title, *content):
    return air.Html(
        air.Head(
            title,
        ),
        air.Body(*content)
    )

ARTICLES_DIR = Path(__file__).parent / "articles"

def get_article_paths() -> List[Path]:
    "Returns a sorted list of markdown paths in the ARTICLES_DIR directory."
    return L(list(ARTICLES_DIR.glob("*.md"))).sorted(reverse=True)

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


def extract_first_image(text: str) -> str:
    """Extracts the first markdown image URL from text, or returns empty string."""
    match = re.search(r'!\[[^\]]*\]\(([^)]+)\)', text)
    return match.group(1) if match else ""


def strip_markdown(text: str) -> str:
    """Strips markdown syntax for plain-text display (links, bold, italic, code)."""
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)  # [text](url) -> text
    text = re.sub(r'`([^`]+)`', r'\1', text)  # `code` -> code
    return text


def get_post_dict(path: Path) -> dict:
    """
    Extracts title, formatted date, and summary from a notebook or markdown path.
    """
    date = get_date_from_filename(path.name)
    formatted_date = f"{date:%a, %b %-d, %Y}"
    # Articles are markdown files. Use the first non-empty line as the title
    # and the second line (if present) as a short tease/summary.
    try:
        text = path.read_text(encoding="utf-8")
        lines = [l for l in text.splitlines()]
        raw_title = lines[0] if lines else "Untitled"
        # strip leading markdown heading markers like '# '
        title = re.sub(r"^\s*#+\s*", "", raw_title).strip() or "Untitled"
        summary = next((l for l in lines[1:] if l.strip()), "")
        image = extract_first_image(text)
    except Exception:
        title = "Untitled"
        summary = ""
        image = ""
    return {"title": title, "date": date, "meta": formatted_date, "tease": strip_markdown(summary), "image": image, "url": f"/articles/{path.stem}"}




def page_footer() -> Any:
    """
    Returns the page footer element.
    """
    return air.P(f"© 2024-{datetime.now().year} Audrey M. Roy Greenfeld")


@app.page
def index(request: air.Request) -> Any:
    post_paths = get_article_paths()
    posts = L(post_paths).map(get_post_dict)
    return jinja(request, "index.html", {
        "posts": posts
    })

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
        # Render full content minus first line (title)
        content = markdown("\n".join(text.splitlines()[1:]), CustomHTMLRenderer)
        # Extract the first line as the title and strip leading '#' (markdown heading)
        lines = text.splitlines()
        raw_title = lines[0] if lines else "Untitled"
        # Remove leading hashes and surrounding whitespace, then trim
        title = re.sub(r"^\s*#+\s*", "", raw_title).strip()
        # Summary/description: first non-empty line after title
        summary = next((l for l in lines[1:] if l.strip()), "")
    else:
        raise air.HTTPException(status_code=404)
    
    return jinja(request, "article.html", {
        "title": title,
        "meta": f"{date:%a, %b %-d, %Y}",
        "description": summary,
        "content": content,
        "pygments_css": STYLE_DEFINITION,
    })

@app.get("/og/{name}.jpg")
def og_image_jpg(name: str) -> Any:
    """Returns a dynamically generated JPEG OG image for a given article."""
    md_path = ARTICLES_DIR / f"{name}.md"
    if not md_path.exists():
        raise air.HTTPException(status_code=404)
    post = get_post_dict(md_path)
    jpg_bytes = generate_og_jpg(post["title"], post["meta"], post["tease"])
    return Response(content=jpg_bytes, media_type="image/jpeg")


@app.get("/og/{name}")
def og_image(request: air.Request, name: str) -> Any:
    """Renders an OG image page for a given article, designed to be screenshotted at 1200x630."""
    md_path = ARTICLES_DIR / f"{name}.md"
    if not md_path.exists():
        raise air.HTTPException(status_code=404)
    post = get_post_dict(md_path)
    return jinja(request, "og-image.html", {
        "title": post["title"],
        "meta": post["meta"],
        "description": post["tease"],
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
