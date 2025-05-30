# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/2025-02-07-This-Site-Is-Now-Powered-by-This-Notebook-Part-6.ipynb.

# %% auto 0
__all__ = ['app', 'rt', 'get_nb_paths', 'get_title_and_desc', 'get_date_from_iso8601_prefix', 'NBCard', 'mk_nbcard_from_nb_path',
           'InLi', 'InlineNav', 'index', 'StyledCode', 'MonsterHtmlRenderer', 'StyledMd', 'StyledCell', 'notebook',
           'versions', 'wellknown']

# %% nbs/2025-02-07-This-Site-Is-Now-Powered-by-This-Notebook-Part-6.ipynb 3
from datetime import datetime
from execnb.nbio import read_nb
from nb2fasthtml.core import render_code_output
from fastcore.utils import *
from fasthtml.common import *
from fasthtml.jupyter import *
from importlib.metadata import distributions
from IPython.display import display, HTML
from monsterui import franken
from monsterui.all import Theme
from mistletoe import markdown
from mistletoe.html_renderer import block_token, HtmlRenderer
import pygments
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter

# %% nbs/2025-02-07-This-Site-Is-Now-Powered-by-This-Notebook-Part-6.ipynb 6
app,rt = fast_app(pico=False)

# %% nbs/2025-02-07-This-Site-Is-Now-Powered-by-This-Notebook-Part-6.ipynb 10
def get_nb_paths(): 
    root = Path() if IN_NOTEBOOK else Path("nbs/")
    return L(root.glob("*.ipynb")).sorted(reverse=True)

# %% nbs/2025-02-07-This-Site-Is-Now-Powered-by-This-Notebook-Part-6.ipynb 12
def get_title_and_desc(fpath):
    nb = read_nb(fpath)
    title = nb.cells[0].source.lstrip("# ")
    desc = nb.cells[1].source
    return title,desc

# %% nbs/2025-02-07-This-Site-Is-Now-Powered-by-This-Notebook-Part-6.ipynb 14
def get_date_from_iso8601_prefix(fname):
    "Gets date from first 10 chars YYYY-MM-DD of `fname`, where `fname` is like `2025-01-12-Get-Date-From-This.whatever"
    try:
        return datetime.fromisoformat(str(fname)[0:10])
    except ValueError: return datetime.now()

# %% nbs/2025-02-07-This-Site-Is-Now-Powered-by-This-Notebook-Part-6.ipynb 18
def NBCard(title,desc,href,date):
    return A(
        franken.Card(
        franken.CardTitle(franken.H3(title)), 
        franken.P(f"{date:%a, %b %-d, %Y}", cls=franken.TextPresets.muted_sm),
        franken.P(desc),
        body_cls='space-y-2'
    ), href=href)

# %% nbs/2025-02-07-This-Site-Is-Now-Powered-by-This-Notebook-Part-6.ipynb 19
def mk_nbcard_from_nb_path(nb_path):
    date = get_date_from_iso8601_prefix(nb_path.name) or datetime.now()
    return NBCard(*get_title_and_desc(nb_path), href=f'/nbs/{nb_path.name[:-6]}', date=date)

# %% nbs/2025-02-07-This-Site-Is-Now-Powered-by-This-Notebook-Part-6.ipynb 21
def InLi(linktuple):
    txt, href = linktuple
    return Li(A(txt, href=href), style="display:inline;margin-right:1em")

# %% nbs/2025-02-07-This-Site-Is-Now-Powered-by-This-Notebook-Part-6.ipynb 22
def InlineNav():
    nls = L(
        ("audrey.feldroy.com", "https://audrey.feldroy.com/"),
        ("GitHub repo for this site", "https://github.com/audreyfeldroy/audrey.feldroy.com")
    )
    return Nav(
        Ul(
            *nls.map(InLi),
            style="list-style:none;padding-left:0"
        ),
        aria_label="Main navigation",
        role="navigation"
    )

# %% nbs/2025-02-07-This-Site-Is-Now-Powered-by-This-Notebook-Part-6.ipynb 24
@rt
def index():
    nb_paths = get_nb_paths()
    return (
        Theme.blue.headers(),
        Title("audrey.feldroy.com"),
        franken.Container(
#             InlineNav(),  # TODO: Fix incompatibilities with MonsterUI
            Div(
                franken.H1('audrey.feldroy.com'), franken.P("The experimental Jupyter notebooks of Audrey M. Roy Greenfeld. This website and all its notebooks are open-source at ", franken.A("github.com/audreyfeldroy/audrey.feldroy.com", href="https://github.com/audreyfeldroy/arg-blog-fasthtml"), cls="mb-6"),
            ),
            franken.Grid(*nb_paths.map(mk_nbcard_from_nb_path), cols_sm=1, cols_md=1, cols_lg=2, cols_xl=3)
        )
    )

# %% nbs/2025-02-07-This-Site-Is-Now-Powered-by-This-Notebook-Part-6.ipynb 26
def StyledCode(c, style='monokai'):
    fm = HtmlFormatter(style=style, cssclass=style, prestyles="padding:10px 0;")
    h = highlight(c, PythonLexer(), fm)
    sd = fm.get_style_defs(f".{style}")
    return Style(sd), NotStr(h)

# %% nbs/2025-02-07-This-Site-Is-Now-Powered-by-This-Notebook-Part-6.ipynb 27
class MonsterHtmlRenderer(HtmlRenderer):
    def render_heading(self, token: block_token.Heading) -> str:
        template = '<h{level} class="uk-h{level}">{inner}</h{level}>'
        inner = self.render_inner(token)
        return template.format(level=token.level, inner=inner)

# %% nbs/2025-02-07-This-Site-Is-Now-Powered-by-This-Notebook-Part-6.ipynb 28
def StyledMd(m):
    return Safe(markdown(m, MonsterHtmlRenderer))

# %% nbs/2025-02-07-This-Site-Is-Now-Powered-by-This-Notebook-Part-6.ipynb 29
def StyledCell(c):
    if c.cell_type == "markdown": return StyledMd(c.source)
    if c.cell_type == "code": 
        if not c.outputs: return StyledCode(c.source)
        return StyledCode(c.source), render_code_output(c)

# %% nbs/2025-02-07-This-Site-Is-Now-Powered-by-This-Notebook-Part-6.ipynb 31
@rt("/nbs/{name}")
def notebook(name:str):
    fname = f"{name}.ipynb" if IN_NOTEBOOK else f"nbs/{name}.ipynb"
    fpath = Path(fname)
    nb = read_nb(fpath)
    title = nb.cells[0].source.lstrip("# ")
    date = get_date_from_iso8601_prefix(fname.lstrip("nbs/"))
    desc = nb.cells[1].source
    if "MonsterUI" in title:
        return (
            Theme.slate.headers(),
#             InlineNav(),  # TODO: Fix incompatibilities with MonsterUI
            Title(title),
            franken.Container(
                Header(
                    # TODO: refactor Tailwind margin classes to use MonsterUI DivVStacked or DivFullySpaced
                    franken.H1(title, cls=("my-6",)),
                    franken.P(f"by Audrey M. Roy Greenfeld | {date:%a, %b %-d, %Y}", cls=(franken.TextT.sm, franken.PaddingT.lg, "mb-6")),
                    franken.P(desc, cls=("mb-6",)),
                    Hr()
                ),
                *L(nb.cells[2:]).map(StyledCell),
                cls="space-y-5"
            )
    )
    return (
        Style(':root {font-family: system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", sans-serif; color-scheme: light dark;} body {background-color: light-dark(#ffffff, #1a1a1a); color: light-dark(#1a1a1a, #ffffff);} p {line-height: 1.5;}'),
        InlineNav(),
        Title(title),
        Div(
            H1(title), # Title
            P(Small(f"by Audrey M. Roy Greenfeld | {date:%a, %b %-d, %Y}")),
            P(desc),
            Hr(),
            *L(nb.cells[2:]).map(StyledCell),
            cls="space-y-5"
        )
    )

# %% nbs/2025-02-07-This-Site-Is-Now-Powered-by-This-Notebook-Part-6.ipynb 33
@rt
def versions():
    dists = L([NS(name=dist.metadata['Name'], version=dist.version) for dist in distributions()]).sorted('name')
    dists = [Li(f'{d.name}: {d.version}') for d in dists]
    return (Title('Python Package Versions'),
        Style(':root {font-family: system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", sans-serif; color-scheme: light dark;} body {background-color: light-dark(#ffffff, #1a1a1a); color: light-dark(#1a1a1a, #ffffff);} p {line-height: 1.5;}'),   
        Div(
            H1('Python Package Versions'),
            Ul(*dists)          
        )       
    )

# %% nbs/2025-02-07-This-Site-Is-Now-Powered-by-This-Notebook-Part-6.ipynb 35
@rt('/.well-known/{fname}')
def wellknown(fname: str):
    fpath = f"../.well-known/{fname}" if IN_NOTEBOOK else f".well-known/{fname}"
    return Path(fpath).read_text()

# %% nbs/2025-02-07-This-Site-Is-Now-Powered-by-This-Notebook-Part-6.ipynb 37
serve()
