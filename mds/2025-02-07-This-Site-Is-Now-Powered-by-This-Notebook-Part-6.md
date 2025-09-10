# This Site Is Now Powered by This Notebook, Part 6

I add a mini-nav to the vanilla non-MonsterUI version of notebook detail pages (used for in-depth CSS experiments). I also now export main.py from within this notebook. 


```python
#| default_exp main
```


```python
#| export
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
```


```python
IN_NOTEBOOK
```




    True



## Setup


```python
#| export
app,rt = fast_app(pico=False)
```


```python
server = JupyUvi(app)
```



<script>
document.body.addEventListener('htmx:configRequest', (event) => {
    if(event.detail.path.includes('://')) return;
    htmx.config.selfRequestsOnly=false;
    event.detail.path = `${location.protocol}//${location.hostname}:8000${event.detail.path}`;
});
</script>



```python
# server.stop()
```

## Utilities


```python
#| export
def get_nb_paths(): 
    root = Path() if IN_NOTEBOOK else Path("nbs/")
    return L(root.glob("*.ipynb")).sorted(reverse=True)
```


```python
nb_paths = get_nb_paths()
nb_paths
```




    (#64) [Path('2025-02-07-This-Site-Is-Now-Powered-by-This-Notebook-Part-6.ipynb'),Path('2025-02-06-Creating-an-Accessible-Inline-Nav-FastTag.ipynb'),Path('2025-02-05-FastHTML-Time-Converter-Part-2.ipynb'),Path('2025-02-05-FastHTML-Pattern-List-Page-With-Form.ipynb'),Path('2025-02-05-Create-a-CLI-Tool-With-Fastcore-Script.ipynb'),Path('2025-02-04-How-to-Turn-a-Jupyter-Notebook-Into-a-Python-Script.ipynb'),Path('2025-02-03-FastHTML-and-MonsterUI-Time-Converter.ipynb'),Path('2025-02-02-Text-Embeddings-and-Cosine-Similarity.ipynb'),Path('2025-02-01-Auto-Renaming-My-Untitled-ipynb-Files-With-Gemini.ipynb'),Path('2025-01-31-Performance-Optimization-Moving-HTML-Class-Injection-from-lxml-to-Mistletoe.ipynb'),Path('2025-01-30-This-Site-Is-Now-Powered-by-This-Notebook-Part-5.ipynb'),Path('2025-01-29-This-Site-Is-Now-Powered-by-This-Notebook-Part-4.ipynb'),Path('2025-01-28-Functional-Programming-with-datetime-and-Omni-Timezone-Discord-Timestamps.ipynb'),Path('2025-01-27-This-Site-Is-Now-Powered-by-This-Notebook-Part-3.ipynb'),Path('2025-01-26-Improving-Pygments-Code-Block-Display.ipynb'),Path('2025-01-25-This-Site-Is-Now-Powered-by-This-Notebook-Part-2.ipynb'),Path('2025-01-24-Creating-In-Notebook-Images-for-Social-Media-With-PIL-Pillow.ipynb'),Path('2025-01-23-Troubleshooting-MonsterUI-on-This-Site.ipynb'),Path('2025-01-23-This-Site-Is-Now-Powered-by-This-Notebook.ipynb'),Path('2025-01-22-MonsterUI-Buttons-and-Links.ipynb')...]




```python
#| export
def get_title_and_desc(fpath):
    nb = read_nb(fpath)
    title = nb.cells[0].source.lstrip("# ")
    desc = nb.cells[1].source
    return title,desc
```


```python
get_title_and_desc(nb_paths[0])
```




    ('This Site Is Now Powered by This Notebook, Part 6',
     'I add a mini-nav to the vanilla non-MonsterUI version of notebook detail pages (used for in-depth CSS experiments). I also now export main.py from within this notebook. ')




```python
#| export
def get_date_from_iso8601_prefix(fname):
    "Gets date from first 10 chars YYYY-MM-DD of `fname`, where `fname` is like `2025-01-12-Get-Date-From-This.whatever"
    try:
        return datetime.fromisoformat(str(fname)[0:10])
    except ValueError: return datetime.now()
```


```python
date = get_date_from_iso8601_prefix(nb_paths[0].name)
date
```




    datetime.datetime(2025, 2, 7, 0, 0)




```python
date = get_date_from_iso8601_prefix(None)
date
```




    datetime.datetime(2025, 2, 7, 1, 33, 11, 638223)



## Notebook Cards


```python
#| export
def NBCard(title,desc,href,date):
    return A(
        franken.Card(
        franken.CardTitle(franken.H3(title)), 
        franken.P(f"{date:%a, %b %-d, %Y}", cls=franken.TextPresets.muted_sm),
        franken.P(desc),
        body_cls='space-y-2'
    ), href=href)
```


```python
#| export
def mk_nbcard_from_nb_path(nb_path):
    date = get_date_from_iso8601_prefix(nb_path.name) or datetime.now()
    return NBCard(*get_title_and_desc(nb_path), href=f'/nbs/{nb_path.name[:-6]}', date=date)
```

## Nav


```python
#| export
def InLi(linktuple):
    txt, href = linktuple
    return Li(A(txt, href=href), style="display:inline;margin-right:1em")
```


```python
#| export
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
```

## Index Page


```python
#| export
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
```

## Notebook Cells


```python
#| export
def StyledCode(c, style='monokai'):
    fm = HtmlFormatter(style=style, cssclass=style, prestyles="padding:10px 0;")
    h = highlight(c, PythonLexer(), fm)
    sd = fm.get_style_defs(f".{style}")
    return Style(sd), NotStr(h)
```


```python
#| export
class MonsterHtmlRenderer(HtmlRenderer):
    def render_heading(self, token: block_token.Heading) -> str:
        template = '<h{level} class="uk-h{level}">{inner}</h{level}>'
        inner = self.render_inner(token)
        return template.format(level=token.level, inner=inner)
```


```python
#| export
def StyledMd(m):
    return Safe(markdown(m, MonsterHtmlRenderer))
```


```python
#| export
def StyledCell(c):
    if c.cell_type == "markdown": return StyledMd(c.source)
    if c.cell_type == "code": 
        if not c.outputs: return StyledCode(c.source)
        return StyledCode(c.source), render_code_output(c)
```

## Detail Page


```python
#| export
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
```

## Python Package Versions


```python
#| export
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
```

## .well-known


```python
#| export
@rt('/.well-known/{fname}')
def wellknown(fname: str):
    fpath = f"../.well-known/{fname}" if IN_NOTEBOOK else f".well-known/{fname}"
    return Path(fpath).read_text()
```

## Serve


```python
#| export
serve()
```

## Export

To export this notebook as [audrey.feldroy.com's main.py](https://github.com/audreyfeldroy/audrey.feldroy.com/blob/main/main.py):


```python
from nbdev.export import nb_export
nb_export("2025-02-07-This-Site-Is-Now-Powered-by-This-Notebook-Part-6.ipynb", lib_path="..")
```
