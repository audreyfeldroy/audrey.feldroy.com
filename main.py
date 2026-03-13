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
try:
    FONT_EMOJI = ImageFont.truetype(str(FONTS_DIR / "NotoColorEmoji.ttf"), 109)  # only valid size
except OSError:
    FONT_EMOJI = None

# Regex matching emoji characters (including variation selectors and ZWJ sequences)
_EMOJI_RE = re.compile(
    "(["
    "\U0001f600-\U0001f64f"  # emoticons
    "\U0001f300-\U0001f5ff"  # symbols & pictographs
    "\U0001f680-\U0001f6ff"  # transport & map
    "\U0001f1e0-\U0001f1ff"  # flags
    "\U0001f900-\U0001f9ff"  # supplemental symbols
    "\U0001fa00-\U0001fa6f"  # chess symbols
    "\U0001fa70-\U0001faff"  # symbols extended-A
    "\U00002702-\U000027b0"  # dingbats
    "\U0000fe0f"             # variation selector
    "\U0000200d"             # ZWJ
    "\U00002600-\U000026ff"  # misc symbols
    "]+)"
)

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


def draw_text_with_emoji(
    img: Image.Image,
    draw: ImageDraw.Draw,
    xy: tuple[int, int],
    text: str,
    fill: str,
    font: ImageFont.FreeTypeFont,
) -> None:
    """Draw text, substituting color emoji from a fallback font where needed."""
    x, y = xy
    # Target emoji height matches the text cap height
    text_bbox = font.getbbox("A")
    text_h = text_bbox[3] - text_bbox[1]
    if FONT_EMOJI is None:
        # No emoji font available, draw everything with the text font
        draw.text((x, y), text, fill=fill, font=font)
        return
    segments = _EMOJI_RE.split(text)
    for seg in segments:
        if not seg:
            continue
        if _EMOJI_RE.fullmatch(seg):
            # Render emoji at native 109px, then scale to match text size
            bbox = FONT_EMOJI.getbbox(seg)
            w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
            tmp = Image.new("RGBA", (w, h), (0, 0, 0, 0))
            tmp_draw = ImageDraw.Draw(tmp)
            tmp_draw.text((-bbox[0], -bbox[1]), seg, font=FONT_EMOJI, embedded_color=True)
            target_h = int(text_h * 1.1)
            target_w = int(w * target_h / h)
            tmp = tmp.resize((target_w, target_h), Image.LANCZOS)
            y_offset = (text_h - target_h) // 2 + int(target_h * 0.55)
            img.paste(tmp, (x, y + y_offset), tmp)
            x += target_w
        else:
            draw.text((x, y), seg, fill=fill, font=font)
            bbox = font.getbbox(seg)
            x += bbox[2] - bbox[0]


def generate_og_jpg(title: str, meta: str, description: str) -> bytes:
    """Render title, date, and description onto the OG base image, return JPEG bytes."""
    img = OG_BASE.copy().convert("RGBA")
    draw = ImageDraw.Draw(img)

    # Vertically center the text block in the content area (top=56, bottom=68, total height=630)
    content_top = int(56 * SCALE)
    content_bottom = int((630 - 68) * SCALE)

    # Measure all text blocks to center vertically
    date_text = meta.upper()
    title_lines = wrap_text(title, FONT_TITLE, OG_TITLE_MAX_WIDTH)
    desc_lines = wrap_text(description, FONT_SUBTITLE, OG_SUBTITLE_MAX_WIDTH)[:5]

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
        draw_text_with_emoji(img, draw, (OG_CONTENT_LEFT, y), line, COLOR_TITLE, FONT_TITLE)
        y += line_height_title
    y += gap_title_desc

    # Description
    for line in desc_lines:
        draw_text_with_emoji(img, draw, (OG_CONTENT_LEFT, y), line, COLOR_SUBTITLE, FONT_SUBTITLE)
        y += line_height_subtitle

    buf = io.BytesIO()
    img.convert("RGB").save(buf, format="JPEG", quality=90)
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


def truncate_description(text: str, max_len: int = 155) -> str:
    """Truncate text to max_len chars, breaking at sentence or word boundary."""
    if len(text) <= max_len:
        return text
    # Try to break at a sentence boundary
    for end in ". ! ?".split():
        idx = text.rfind(end, 0, max_len)
        if idx > 0:
            return text[:idx + 1]
    # Fall back to word boundary
    truncated = text[:max_len].rsplit(" ", 1)[0]
    return truncated + "..."


def get_tags(path: Path) -> list[str]:
    """Extracts lowercase tags from the 'Tags: ...' line at the end of a markdown file."""
    try:
        text = path.read_text(encoding="utf-8")
    except Exception:
        return []
    for line in reversed(text.splitlines()):
        line = line.strip()
        if line.lower().startswith("tags:"):
            raw = line[len("tags:"):].strip()
            if not raw:
                return []
            return [t.strip().lower() for t in raw.split(",") if t.strip()]
        if line:
            break
    return []


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
    tags = get_tags(path)
    return {"title": title, "date": date, "meta": formatted_date, "tease": strip_markdown(summary), "image": image, "url": f"/articles/{path.stem}", "tags": tags}




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

def get_all_tags() -> list[dict]:
    """Returns all tags with counts, sorted by count descending."""
    from collections import Counter
    counts = Counter()
    for path in get_article_paths():
        for tag in get_tags(path):
            counts[tag] += 1
    return sorted(
        [{"name": name, "count": count} for name, count in counts.items()],
        key=lambda t: (-t["count"], t["name"]),
    )


@app.get("/tags/{tag}")
def tag_page(request: air.Request, tag: str) -> Any:
    """Shows all posts with a given tag."""
    posts = [get_post_dict(p) for p in get_article_paths() if tag.lower() in get_tags(p)]
    return jinja(request, "tag.html", {
        "tag": tag,
        "posts": posts,
        "all_tags": get_all_tags(),
    })


@app.get("/tags")
def tags_page(request: air.Request) -> Any:
    """Shows all tags."""
    all_tags = get_all_tags()
    total_posts = len([p for p in get_article_paths() if get_tags(p)])
    return jinja(request, "tags.html", {
        "all_tags": all_tags,
        "total_posts": total_posts,
    })


@app.get("/articles/{name}")
def article(request: air.Request, name: str) -> Any:
    """
    Renders an article page by name, showing its title, summary, and cells.
    """
    md_path = ARTICLES_DIR / f"{name}.md"
    if md_path.exists():
        date = get_date_from_filename(name)
        with open(md_path, "r", encoding="utf-8") as f:
            text = f.read()
        lines = text.splitlines()
        raw_title = lines[0] if lines else "Untitled"
        title = re.sub(r"^\s*#+\s*", "", raw_title).strip()
        summary = next((l for l in lines[1:] if l.strip()), "")
        tags = get_tags(md_path)
        # Render content minus title line and Tags line
        body_lines = lines[1:]
        if body_lines and body_lines[-1].strip().lower().startswith("tags:"):
            body_lines = body_lines[:-1]
        content = markdown("\n".join(body_lines), CustomHTMLRenderer)
    else:
        raise air.HTTPException(status_code=404)

    base_url = "https://audrey.feldroy.com"
    return jinja(request, "article.html", {
        "title": title,
        "meta": f"{date:%a, %b %-d, %Y}",
        "description": truncate_description(strip_markdown(summary)),
        "content": content,
        "tags": tags,
        "pygments_css": STYLE_DEFINITION,
        "canonical_url": f"{base_url}/articles/{name}",
        "og_image_url": f"{base_url}/og/{name}.jpg",
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


BASE_URL = "https://audrey.feldroy.com"


def get_feed_entries(tag: str) -> list[dict]:
    """Build a list of feed entry dicts for articles matching a tag."""
    entries = []
    for path in get_article_paths():
        if tag.lower() not in get_tags(path):
            continue
        post = get_post_dict(path)
        date_str = post["date"].strftime("%Y-%m-%dT%H:%M:%S+00:00")
        article_url = f"{BASE_URL}/articles/{path.stem}"

        # Render article body as HTML, stripping title and Tags lines
        text = path.read_text(encoding="utf-8")
        body_lines = text.splitlines()[1:]
        if body_lines and body_lines[-1].strip().lower().startswith("tags:"):
            body_lines = body_lines[:-1]
        content_html = markdown("\n".join(body_lines), CustomHTMLRenderer)

        entries.append({
            "url": article_url,
            "title": post["title"],
            "summary": post["tease"],
            "content_html": content_html,
            "date_str": date_str,
            "tags": get_tags(path),
        })
        if len(entries) >= 15:
            break
    return entries


@app.get("/feeds/{tag}.atom.xml")
def tag_feed(request: air.Request, tag: str) -> Any:
    """Returns an Atom feed of articles matching the given tag."""
    entries = get_feed_entries(tag)
    feed_updated = entries[0]["date_str"] if entries else datetime.now().strftime("%Y-%m-%dT%H:%M:%S+00:00")
    xml = jinja(request, "feed.xml", {
        "base_url": BASE_URL,
        "tag": tag,
        "feed_updated": feed_updated,
        "year": datetime.now().year,
        "entries": entries,
    }, as_string=True)
    return Response(content=xml.encode("utf-8"), media_type="application/atom+xml; charset=utf-8")
