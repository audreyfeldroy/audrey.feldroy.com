# This Site Is Now Powered by This Notebook, Part 3

Here I improve audrey.feldroy.com in small, subtle ways.


```python
#| default_exp main
```


```python
#| export
from datetime import datetime
from execnb.nbio import read_nb
from nb2fasthtml.core import render_code_output
from fasthtml.common import *
from fasthtml.jupyter import *
from importlib.metadata import distributions
from IPython.display import display, HTML
from monsterui import franken
from monsterui.all import Theme
import mistletoe
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




    (#51) [Path('2025-01-27-This-Site-Is-Now-Powered-by-This-Notebook-Part-3.ipynb'),Path('2025-01-26-Improving-Pygments-Code-Block-Display.ipynb'),Path('2025-01-25-This-Site-Is-Now-Powered-by-This-Notebook-Part-2.ipynb'),Path('2025-01-24-Creating-In-Notebook-Images-for-Social-Media-With-PIL-Pillow.ipynb'),Path('2025-01-23-Troubleshooting-MonsterUI-on-This-Site.ipynb'),Path('2025-01-23-This-Site-Is-Now-Powered-by-This-Notebook.ipynb'),Path('2025-01-22-MonsterUI-Buttons-and-Links.ipynb'),Path('2025-01-22-Customizing-FastHTML-Headers-From-Notebook-Contents.ipynb'),Path('2025-01-21-SVG-Animation-in-FastHTML.ipynb'),Path('2025-01-20-Dark-and-Light-Mode-in-FastHTML.ipynb'),Path('2025-01-19-Genanki-and-fastcore.ipynb'),Path('2025-01-18-Alarm-Sounds-App.ipynb'),Path('2025-01-17-Alarm-Clock-Sounds.ipynb'),Path('2025-01-16-Cosine-Similarity-Breakdown-in-LaTeX.ipynb'),Path('2025-01-14-Constructing-SQLite-Tables-for-Notebooks-and-Search.ipynb'),Path('2025-01-13-SQLite-FTS5-Tokenizers-unicode61-and-ascii.ipynb'),Path('2025-01-12-A-Better-Notebook-Index-Page.ipynb'),Path('2025-01-11-NBClassic-Keyboard-Shortcuts-in-Command-and-Dual-Mode.ipynb'),Path('2025-01-10-Understanding-FastHTML-Routes-Requests-and-Redirects.ipynb'),Path('2025-01-09-Reading-and-Writing-Jupyter-Notebooks-With-Python.ipynb')...]




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




    ('This Site Is Now Powered by This Notebook, Part 3',
     'Here I improve audrey.feldroy.com in small, subtle ways.')




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




    datetime.datetime(2025, 1, 27, 0, 0)




```python
date = get_date_from_iso8601_prefix(None)
date
```




    datetime.datetime(2025, 1, 27, 0, 59, 24, 184133)



## Notebook Cards


```python
#| export
def NBCard(title,desc,href,date):
    return A(
        franken.Card(
        franken.CardTitle(franken.H3(title)), 
        franken.PSmall(f"{date:%a, %b %-d, %Y}", cls="uk-text-muted"),
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
            Div(
                franken.H1('audrey.feldroy.com'), franken.PParagraph("The experimental Jupyter notebooks of Audrey M. Roy Greenfeld. This website and all its notebooks are open-source at ", franken.A("github.com/audreyfeldroy/arg-blog-fasthtml", href="https://github.com/audreyfeldroy/arg-blog-fasthtml"), cls="mb-6"),
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
def StyledMd(m):
    return Safe(mistletoe.markdown(m))
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
#     root = Path() if IN_NOTEBOOK else Path("nbs/")
    fname = f"{name}.ipynb" if IN_NOTEBOOK else f"nbs/{name}.ipynb"
    fpath = Path(fname)
    nb = read_nb(fpath)
    title = nb.cells[0].source.lstrip("# ")
    date = get_date_from_iso8601_prefix(fname.lstrip("nbs/"))
    desc = nb.cells[1].source
    if "MonsterUI" in title:
        return (
            Theme.slate.headers(),
            Title(title),
            franken.Container(
                franken.H1(title),
                franken.PSmall(f"by Audrey M. Roy Greenfeld | {date:%a, %b %-d, %Y}", cls="uk-text-muted"),
                franken.P(desc), # Desc
                *L(nb.cells[2:]).map(StyledCell),
                cls="space-y-5"
            )
    )
    return (
        Style(':root {font-family: system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", sans-serif; color-scheme: light dark;} body {background-color: light-dark(#ffffff, #1a1a1a); color: light-dark(#1a1a1a, #ffffff);} p {line-height: 1.5;}'),
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


```python
server.stop()
```

## Export

To export this notebook as arg-blog-fasthtml's main.py:

```bash
nb_export nbs/2025-01-27-This-Site-Is-Now-Powered-by-This-Notebook-Part-3.ipynb --lib_path .
```
