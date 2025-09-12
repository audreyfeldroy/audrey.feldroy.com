# Understanding FastHTML Headers

FastHTML provides default headers for every page, which are also fully customizable. This notebook explores how this works.


```python
from fasthtml.common import *
from fasthtml.jupyter import *
from IPython.display import display,HTML
```

## Default Headers

In [00_core](https://github.com/AnswerDotAI/fasthtml/blob/main/nbs/api/00_core.ipynb) there is a `def_hdrs` function that returns the "default headers for a FastHTML app":


```python
def_hdrs()
```

JS files for these libraries are included by default:

* [HTMX](https://htmx.org/): For interactivity! Allows any HTML attribute to have actions, handlers, etc. providing dynamic behavior via DOM element AJAX swaps and modification
* [fasthtml-js](https://github.com/answerdotai/fasthtml-js): JS for FastHTML apps
* [Surreal](https://github.com/gnat/surreal): Inline Locality of Behavior (LoB) for JS + tiny jQuery alternative
* [CSS Scope Inline](https://github.com/gnat/css-scope-inline/): Inline LoB for CSS

### How They're Defined

In that same 00_core notebook each of the default script headers above is defined with `Script`, like:


```python
htmxsrc   = Script(src="https://unpkg.com/htmx.org@2.0.4/dist/htmx.min.js")
htmxsrc
```

The meta headers are defined with `Meta` like:


```python
viewport  = Meta(name="viewport", content="width=device-width, initial-scale=1, viewport-fit=cover")
viewport
```

## In the FastHTML app instance

Later in 00_core when `FastHTML` is defined, these are the relevant lines related to headers:
    
```python
class FastHTML(Starlette):
    def __init__(self, ..., hdrs=None)
        ...
        if default_hdrs: hdrs = def_hdrs(htmx, surreal=surreal) + hdrs
        hdrs += [Script(src=ext) for ext in exts.values()]
        if IN_NOTEBOOK:
            hdrs.append(iframe_scr)
            from IPython.display import display,HTML
            if nb_hdrs: display(HTML(to_xml(tuple(hdrs))))
            middleware.append(cors_allow)
        self.on_startup,self.on_shutdown,self.lifespan,self.hdrs,self.ftrs = on_startup,on_shutdown,lifespan,hdrs,ftrs
        ...
```

## In the app from `fast_app`

If you instantiate `FastHTML` via the [fast_app](https://github.com/AnswerDotAI/fasthtml/blob/main/fasthtml/fastapp.py#L29) convenience function, you can see those same default JS headers here, plus Pico and a `sendmsg` JS function:


```python
app,rt = fast_app()
```


```python
app.hdrs
```

## In-Notebook Behavior

One of the things I love about FastHTML is how it's designed to work in Jupyter notebooks, and built that way from its core. 

The more I use notebooks, the more I realize they're key to writing simple code that you understand thorougly inside and out. That is what makes code truly maintainable and long-lasting.


```python
IN_NOTEBOOK
```

This is defined earlier in 00_core and appended to the in-notebook headers. Here iframes' height is auto-resized to their content, allowing FastHTML pages to be better shown in-notebook:


```python
iframe_scr
```

If you set `nb_hdrs=True`, the line `display(HTML(to_xml(tuple(app.hdrs))))` will add the headers to the notebook.

## Customizing Headers: Adding a JS File

Here we add a simple 1-file JS library, Tone.js:


```python
Script(src="http://unpkg.com/tone")
```

We see the Tone.js header was added after the default FastHTML headers:


```python
app,rt = fast_app(hdrs=(Script(src="https://unpkg.com/tone"),))
app.hdrs
```

This route handler has code from the Tone.js Hello World example:


```python
@rt
def index():
    return Div(
        Script('const synth = new Tone.Synth().toDestination();synth.triggerAttackRelease("C4", "8n");'),
        P("This page should include the Tone.js header and play a tone")
    )

```


```python
server = JupyUvi(app)
```

Uncomment and run this to play a tone:


```python
# HTMX()
```

That works because the Tone.js header file was added.

## Customizing Headers: Adding MonsterUI

MonsterUI has a great [tutorial app](https://monsterui.answer.ai/tutorial_app) showing how to customize FastHTML headers. It starts with adding the MonsterUI headers to `fast_app`.


```python
from monsterui.all import Theme, fast_app
hdrs = Theme.blue.headers()
```

MonsterUI's theme headers include FrankenUI, Tailwind CSS, and theming code:


```python
hdrs
```

MonsterUI is a little different because it comes with its own `fast_app` that extends the one from FastHTML's fastapp.py. That is defined in [monsterui/nbs/01_core.ipynb](https://github.com/AnswerDotAI/MonsterUI/blob/main/nbs/01_core.ipynb) and used here:


```python
app,rt = fast_app(hdrs=hdrs)
app.hdrs
```

The code in MonsterUI for this is:


```python
from fastcore.all import delegates
import fasthtml.common as fh

@delegates(fh.fast_app, but=['pico'])
def fast_app(*args, pico=False, **kwargs):
    "Create a FastHTML or FastHTMLWithLiveReload app with `bg-background text-foreground` to bodykw for frankenui themes"
    if 'bodykw' not in kwargs: kwargs['bodykw'] = {}
    if 'class' not in kwargs['bodykw']: kwargs['bodykw']['class'] = ''
    kwargs['bodykw']['class'] = stringify((kwargs['bodykw']['class'],'bg-background text-foreground'))
    return fh.fast_app(*args, pico=pico, **kwargs)
```


```python
app.bodykw
```
