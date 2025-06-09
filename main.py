

__all__ = ['app', 'rt', 'get_nb_paths', 'get_title_and_desc', 'get_date_from_iso8601_prefix', 'NBCard', 'mk_nbcard_from_nb_path',
           'InLi', 'InlineNav', 'index', 'StyledCode', 'MonsterHtmlRenderer', 'StyledMd', 'StyledCell', 'notebook',
           'versions', 'wellknown']


from datetime import datetime
from execnb.nbio import read_nb
from execnb.shell import render_outputs
from fastcore.utils import *
from fasthtml.common import *
from fasthtml.jupyter import *
from importlib.metadata import distributions
from monsterui import franken
from monsterui.all import Theme
from mistletoe import markdown
from mistletoe.html_renderer import block_token, HtmlRenderer
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter

app,rt = fast_app(pico=False)

def get_nb_paths(): 
    root = Path() if IN_NOTEBOOK else Path("nbs/")
    return L(root.glob("*.ipynb")).sorted(reverse=True)

def get_title_and_desc(fpath):
    nb = read_nb(fpath)
    title = nb.cells[0].source.lstrip("# ")
    desc = nb.cells[1].source
    return title,desc

def get_date_from_iso8601_prefix(fname):
    "Gets date from first 10 chars YYYY-MM-DD of `fname`, where `fname` is like `2025-01-12-Get-Date-From-This.whatever"
    try:
        return datetime.fromisoformat(str(fname)[0:10])
    except ValueError: return datetime.now()

def NBCard(title,desc,href,date):
    return A(
        franken.Card(
        franken.CardTitle(franken.H3(title)), 
        franken.P(f"{date:%a, %b %-d, %Y}", cls=franken.TextPresets.muted_sm),
        franken.P(desc),
        body_cls='space-y-2'
    ), href=href)

def mk_nbcard_from_nb_path(nb_path):
    date = get_date_from_iso8601_prefix(nb_path.name) or datetime.now()
    return NBCard(*get_title_and_desc(nb_path), href=f'/nbs/{nb_path.name[:-6]}', date=date)

def InLi(linktuple):
    txt, href = linktuple
    return Li(A(txt, href=href), style="display:inline;margin-right:1em")

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

@rt
def index():
    nb_paths = get_nb_paths()
    return (
        Theme.blue.headers(),
        Title("audrey.feldroy.com"),
        franken.Container(
#             InlineNav(),  # TODO: Fix incompatibilities with MonsterUI
            Div(
                franken.H1('audrey.feldroy.com'), franken.P("The experimental Jupyter notebooks of Audrey M. Roy Greenfeld. This website and all its notebooks are open-source at ", franken.A("github.com/audreyfeldroy/audrey.feldroy.com", href="https://github.com/audreyfeldroy/audrey.feldroy.com"), cls="mb-6"),
            ),
            franken.Grid(*nb_paths.map(mk_nbcard_from_nb_path), cols_sm=1, cols_md=1, cols_lg=2, cols_xl=3)
        )
    )

def StyledCode(c, style='monokai'):
    fm = HtmlFormatter(style=style, cssclass=style, prestyles="padding:10px 0;")
    h = highlight(c, PythonLexer(), fm)
    sd = fm.get_style_defs(f".{style}")
    return Style(sd), NotStr(h)

class MonsterHtmlRenderer(HtmlRenderer):
    def render_heading(self, token: block_token.Heading) -> str:
        template = '<h{level} class="uk-h{level}">{inner}</h{level}>'
        inner = self.render_inner(token)
        return template.format(level=token.level, inner=inner)

def StyledMd(m):
    return Safe(markdown(m, MonsterHtmlRenderer))

def StyledCell(c):
    if c.cell_type == "markdown": return StyledMd(c.source)
    if c.cell_type == "code": 
        if not c.outputs: return StyledCode(c.source)
        # Directly incorporate render_code_output functionality
        res = render_outputs(c.outputs, pygments=False)
        output = Footer(NotStr(res)) if res else ''
        return StyledCode(c.source), output

@rt("/nbs/{name}")
def notebook(name:str):
    fname = f"nbs/{name}.ipynb"
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
            cls="container mx-auto space-y-5"
        )
    )

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

@rt('/.well-known/{fname}')
def wellknown(fname: str):
    fpath = f"../.well-known/{fname}" if IN_NOTEBOOK else f".well-known/{fname}"
    return Path(fpath).read_text()

serve()
