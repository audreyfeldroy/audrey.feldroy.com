# Minimal Typography for FastHTML Apps

When using `pico=False` and no CSS framework, a FastHTML page doesn't look great. Can we use minimal typography to make it look decent, without dependencies?

## Setup


```python
from fasthtml.common import *
from fasthtml.jupyter import *
```

## Styling the Bare Minimum

I style `:root` because it's the highest-level CSS selector. The bare minimum to make a page look decent is `font-family`:


```python
css = ':root {font-family: system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", sans-serif;} p {line-height: 1.5;}'
s = Style(css)
s
```


```python
d = Div(s, H1("Typography Experiment"), P("Here's a paragraph of text for testing. "*20))
show(d)
```

## Constraining Width

The only thing remaining to make the text look good is to constrain the width. Best to do that in a container div.


```python
css = ':root {font-family: system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", sans-serif;} p {line-height: 1.5;} #container {width: 800px; margin: 0 auto;}'
s = Style(css)
d = Div(s, H1("Typography Experiment"), P("Here's a paragraph of text for testing. "*20), id="container")
show(d)
```

## FastHTML App

Putting it into a page in a FastHTML app:


```python
app, rt = fast_app(pico=False)
```

Here I run Uvicorn from this notebook. Replace this with `serve()` at the bottom if you are using this in a main.py:


```python
server = JupyUvi(app)
```


```python
@rt
def index():
    return Div(
        Style(css),
        H1("Typography Experiment"),
        P("Here's a paragraph of some text. "*20),
        id="container"
    )
```

## Stop Server

Run this cell to stop Uvicorn:


```python
if 'server' in globals: server.stop()
```
