from datetime import datetime
from execnb.nbio import read_nb
from pathlib import Path
from fasthtml.common import *
from functools import cache
from monsterui.all import Theme
from nb2fasthtml.core import *
from importlib.metadata import distributions

hdrs = (
    MarkdownJS(),
    HighlightJS(langs=['python', 'javascript', 'html', 'css',]),
)

app,rt = fast_app(hdrs=hdrs, pico=False)

@cache
def get_date_from_iso8601_prefix(fname):
    "Gets date from first 10 chars YYYY-MM-DD of `fname`, where `fname` is like `2025-01-12-Get-Date-From-This.whatever"
    try:
        return datetime.fromisoformat(str(fname)[:10])
    except ValueError: return None

def get_title(nb):
    "Get title from `fname` notebook's cell 0 source by stripping '# ' prefix"
    nb = nb.cells[0].source.lstrip('# ')
    if '\n' in nb:
        return first(nb.split('\n'))
    return nb

@cache
def Card(fname):
    date = get_date_from_iso8601_prefix(fname.name)
    nb = read_nb(fname)
    title = get_title(nb)
    return A(
        Header(H2(title, style="margin:0 0 0.5rem 0;font-size:1.25rem;font-weight:500;")),
        Div(f"{date:%a, %b %-d, %Y}", style="font-size: 0.875rem;color:#666;"),
        href=f'/nbs/{fname.name[:-6]}',
        onmouseover="this.style.transform='translateY(-2px)';this.style.boxShadow='0 4px 6px rgba(0,0,0,0.1)'",
        onmouseout="this.style.transform='none';this.style.boxShadow='0 1px 3px rgba(0,0,0,0.12)'",
        style="border:1px solid #e2e8f0;padding:1rem;border-radius:0.5rem;background:light-dark(#ffffff, #1a1a1a);color:light-dark(#1a1a1a, #ffffff);box-shadow:0 1px 3px rgba(0,0,0,0.12);transition:transform 0.2s ease;cursor:pointer;text-decoration:none;display:block;")

light = "#f8f9fa"
dark = "#343a40"

def Note(c): return Div(H3("Note"), c, style="padding:10px;border:1px lightblue solid; border-left:6px lightblue solid;")

@rt
def index():
    nb_dir = Path('nbs')
    nbs = L(sorted(nb_dir.glob('*.ipynb'), reverse=True))
    return Titled("audrey.feldroy.com",
        Style(':root {font-family: system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", sans-serif; color-scheme: light dark;} body {background-color: light-dark(#ffffff, #1a1a1a); color: light-dark(#1a1a1a, #ffffff);} p {line-height: 1.5;}'),
        P("The notebooks of Audrey M. Roy Greenfeld"),
        Div(*L(nbs).map(Card), style="margin:2em auto;display:grid;grid-template-columns:repeat(auto-fill, minmax(220px,1fr));grid-gap: 1.5rem;padding:1rem;max-width:1200px;"),
        A("@audrey.feldroy.com on Bluesky", href="https://bsky.app/profile/audrey.feldroy.com"),
        style="padding:1em;"
    )

@rt('/nbs/{name}')
def notebook(name: str):
    fpath = Path(f'nbs/{name}.ipynb')
    nb = read_nb(fpath)
    if "MonsterUI" in nb.cells[3].source:
        return (
            *hdrs,
            *Theme.blue.headers(),
            Title(get_title(nb)),
            render_nb(fpath, wrapper=Div)
        )

    # Otherwise use default style
    return (
        Title(get_title(nb)),
        Style(':root {font-family: system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", sans-serif; color-scheme: light dark;} body {background-color: light-dark(#ffffff, #1a1a1a); color: light-dark(#1a1a1a, #ffffff);} p {line-height: 1.5;}'),
        render_nb(fpath, wrapper=Div),
    )

@rt('/experiments/{name}')
def notebook_old(name: str):
    return Redirect(f"/nbs/{name}")

@rt
def versions():
    dists = L([NS(name=dist.metadata['Name'], version=dist.version) for dist in distributions()]).sorted('name')
    dists = [Li(f'{d.name}: {d.version}') for d in dists]
    return (Title('Package Versions'),
        Style(css),    
        Div(
            H1('Package versions'),
            Ul(*dists)          
        )       
    )

@rt('/.well-known/{fname}')
def wellknown(fname: str):
    return Path(f'.well-known/{fname}').read_text()

serve()
