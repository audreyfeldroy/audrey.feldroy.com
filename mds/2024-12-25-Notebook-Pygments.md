# Converting Jupyter Notebook Cells to Pygments Syntax-Highlighted HTML

## Understand the Problem

Can a Jupyter notebook be converted to syntax-highlighted HTML easily with Pygments?

Side note: Highlight.js is what Danny and Isaac use for syntax highlighting in FastHTML apps. I'll try that in another notebook later. I started this on a plane where I only had Pygments installed.

## Devise a Plan

* Get the code cells of a sample notebook
* Convert one to syntax-highlighted HTML
* View it
* Convert all to syntax-highlighted HTML

## Carry Out Plan


```python
from execnb.nbio import *
from fastcore.all import *
from fasthtml.common import *
from fasthtml.jupyter import *
from IPython.display import HTML, Markdown
from mistletoe import markdown, HTMLRenderer
from mistletoe.contrib.pygments_renderer import PygmentsRenderer
from nb2fasthtml.core import *
from pathlib import Path
import pygments
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter
from random import choice
```


```python
nb = read_nb(Path("../nbs/2024-12-24-deck-the-halls.ipynb"))
nb.metadata
```


```python
nb.cells
```


```python
sources = L(nb.cells).itemgot('source')
sources
```


```python
sources.map(Div)
```


```python
code_cells = L(nb.cells).filter(lambda x: x.cell_type == 'code')
code_cells[:4]
```


```python
code_cells[2]
```

## Code Highlighting With Pygments


```python
fm = HtmlFormatter(style='colorful')
pl = PythonLexer()
```


```python
highlight("print('Hi')", lexer=pl, formatter=fm)
```


```python
highlight(code_cells[2].source, lexer=pl, formatter=fm)
```


```python
HTML(highlight(code_cells[2].source, lexer=pl, formatter=fm))
```

The previous cell should show colors but doesn't. Not sure how to show them here in this notebook.


```python
def colorize(c): return highlight(c.source, lexer=pl, formatter=fm)
```


```python
colorized = code_cells.map(colorize).map(NotStr)
colorized[:2]
```


```python
def colorized_cells(cells): return cells.map(colorize).map(NotStr)
```

## Formatter Styles


```python
L(pygments.styles.STYLES.items())
```


```python
L(pygments.styles.STYLES.items()).itemgot(1)
```


```python
styles = L(pygments.styles.STYLES.items()).itemgot(1).itemgot(1)
styles
```


```python
%%aip
Get a random style from that list
```


```python
style = choice(styles)
style
```

## CSS Styles


```python
fm = HtmlFormatter(style='stata-dark')
```


```python
fm.get_style_defs()[:100]
```

## FastHTML app


```python
app,rt = fast_app()
```


```python
server = JupyUvi(app)
```


```python
@rt
def index():
    nb = read_nb(Path("../nbs/2024-12-24-deck-the-halls.ipynb"))
    code_cells = L(nb.cells).filter(lambda x: x.cell_type == 'code')
    style = choice(styles)
    fm = HtmlFormatter(style=style)
    return (
        H1(f"Random style: {style}"),
        P("This page gets a random ",
            A("Pygments", href="https://pygments.org/"),
            " HtmlFormatter style and applies it to ",
            A("my Deck the Halls Jupyter notebook", href="https://nbsanity.com/static/a426287f3fbfc5a38c99291beadc77d3/2024-12-24-deck-the-halls.html")),
        Style(fm.get_style_defs()),
        Style(".highlight{border:1px solid gray;margin:10px;}"),
        Div(*colorized_cells(code_cells))
    )
```

## Stopping the Server


```python
if 'server' in globals(): server.stop()
```


```python

```
