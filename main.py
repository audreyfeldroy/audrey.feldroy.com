from pathlib import Path
from fasthtml.common import *
from nb2fasthtml.core import *
import regex
from importlib.metadata import distributions

css = ':root {font-family: system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", sans-serif;} p {line-height: 1.5;}'
s = Style(css)

hdrs = (
    MarkdownJS(),
    HighlightJS(langs=['python', 'javascript', 'html', 'css',]),
)

app,rt = fast_app(hdrs=hdrs, pico=False)

def get_date_from_fname(fname):
    try:
        year, month, day = L(regex.findall(r"\d+", fname))[0:3]
    except Exception:
        year, month, day = 0,0,0
    return f"{year}-{month}-{day}"

# HACK: I changed 11 to 14 to chop off the 'nbs/' part of the path
def get_title_from_fname(fname): return fname[14:][:-6].replace('-', ' ').replace('_', ' ')

def Card(fname):
    date = get_date_from_fname(fname)
    title = get_title_from_fname(fname)
    style = """
        border: 1px solid #e2e8f0;
        padding: 1.25rem;
        border-radius: 0.5rem;
        background: white;
        box-shadow: 0 1px 3px rgba(0,0,0,0.12);
        transition: transform 0.2s ease;
        cursor: pointer;
        text-decoration: none;
        color: inherit;
        display: block;
    """
    header_style = "margin-bottom: 0.5rem; font-weight: 600;"
    date_style = "color: #666; font-size: 0.875rem;"
    
    c = A(
        Header(H2(title, style=header_style)),
        I(date, style=date_style),
        style=style,
        href=f'/nbs/{fname[4:][:-6]}',
        onmouseover="this.style.transform='translateY(-2px)';this.style.boxShadow='0 4px 6px rgba(0,0,0,0.1)'",
        onmouseout="this.style.transform='none';this.style.boxShadow='0 1px 3px rgba(0,0,0,0.12)'"
    )
    return c

# Card container - TODO refactor into a component maybe
container_style = """
    margin: 2em auto;
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(220px,1fr));
    grid-gap: 1.5rem;
    padding: 1rem;
    max-width: 1200px;
"""

def Note(c): return Div(H3("Note"), c, style="padding:10px;border:1px lightblue solid; border-left:6px lightblue solid;")

@rt
def index():
    nb_dir = Path('nbs')
    nbs = L(sorted(nb_dir.glob('*.ipynb'), reverse=True)).map(str)
    return Titled("audrey.feldroy.com",
        Style(css),
        P("The notebooks of Audrey M. Roy Greenfeld"),
        Note(P("Happy new year! All notebooks should be displaying correctly now. If you find any problems, message me. I'm ", A("@audreyfeldroy.bsky.social on Bluesky", href="https://bsky.app/profile/audreyfeldroy.bsky.social"))),
        Div(*L(nbs).map(Card), style=container_style),
        style="padding: 1em"
    )

@rt('/nbs/{name}')
def notebook(name: str):
    nb = Path(f'nbs/{name}.ipynb')
    # name is like '2021-01-01-foo-bar'
    # Chop off the date part
    return (
        Title(name[11:].replace('-', ' ').replace('_', ' ')),
        Style(css),
        render_nb(nb, wrapper=Div),
    )

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
