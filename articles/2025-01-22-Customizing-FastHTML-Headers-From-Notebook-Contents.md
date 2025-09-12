# Customizing FastHTML Headers From Notebook Contents

Can we customize a FastHTML app to set different headers when rendering notebooks with nb2fasthtml, based on what the notebook actually needs for its headers?


```python
from fasthtml.common import *
from monsterui.all import *
from nb2fasthtml.core import *
from pathlib import Path
import json, yaml
from execnb.nbio import *
from execnb.shell import render_outputs
from typing import Callable
from functools import partial
from IPython.display import display,HTML
```


```python
tags = ["Python", "Markdown"]
```


```python
hdrs = (MarkdownJS(), HighlightJS(langs=['python', 'javascript', 'html', 'css']))
```

Here I define what is essentially blog post frontmatter, but in multiple cells that are Markdown or Python depending on their purpose. You'll see more about this frontmatter later in the *My Multi-Cell Frontmatter Format* section.

## Warning

This notebook doesn't render well on https://audrey.feldroy.com/nbs/2025-01-22-Customizing-FastHTML-Headers-Per-Route-From-Notebook-Contents and I haven't figured out why. 

To see it a little better, download https://github.com/audreyfeldroy/arg-blog-fasthtml/blob/main/nbs/2025-01-22-Customizing-FastHTML-Headers-Per-Route-From-Notebook-Contents.ipynb
    
Better yet, just look at [my arg-blog-fasthtml main.py's notebook route](https://github.com/audreyfeldroy/arg-blog-fasthtml/blob/main/main.py#L90-L106) for the TL;DR on what I did.

## Background

I like to experiment deeply with different FastHTML headers in different daily notebooks. My use cases include:

* Sometimes I want vanilla CSS and JS, and other times I want the MonsterUI headers.
* If I'm using daily notebooks to explore code cell rendering, sometimes I want to render code cells with HighlightJS, other times with Pygments or another library.
* If I'm playing with Pico or Bootstrap, I want to add it to the headers.
* Maybe I'll start exploring the different HTMX extensions and add them to headers in one-off notebooks.

I definitely don't want all my notebooks rendered on this site with the same FastHTML headers! That's how audrey.feldroy.com started off, but today as a result of this exploration, I now have different headers depending on what the notebook needs.

## Setup


```python
app, rt = fast_app(hdrs=hdrs)
```

## Render NB

This is `render_nb` from `nb2fasthtml.core`:


```python
def render_nb(fpath, # Path to Jupyter Notebook
              wrapper=Main, #Wraps entire rendered NB, default is for pico
              cls='container', # cls to be passed to wrapper, default is for pico
              md_cell_wrapper=Div, # Wraps markdown cell
              md_fn=render_md, # md -> rendered html
              code_cell_wrapper=Card, # Wraps Source Code (body) + Outputs (footer)
              cd_fn=render_code_source, # code cell -> code source rendered html
              out_fn=render_code_output, # code cell -> code output rendered html
              get_fm=get_frontmatter_md, # How to read frontmatter cell
              fm_fn:None|Callable=render_frontmatter, # Frontmatter -> FT components
              **kwargs # Passed to wrapper
             ): 
    nb = read_nb(fpath)
    res, content_start_idx = [], 0
    if fm_fn: 
        content_start_idx = 1
        fm = get_fm(nb.cells[0])
        res.append(fm_fn(fm))
    for cell in nb.cells[content_start_idx:]:
        if   cell['cell_type']=='code'    : res.append(code_cell_wrapper(cd_fn(cell), out_fn(cell)))
        elif cell['cell_type']=='markdown': res.append(md_cell_wrapper(md_fn(cell.source)))
    return wrapper(cls=cls, **kwargs)(*res)
```

### Usage of `render_nb` in my Blog

Currently in the main.py for https://audrey.feldroy.com, I call it from my notebooks detail handler:


```python
@rt('/nbs/{name}')
def notebook(name: str):
    nb = Path(f'nbs/{name}.ipynb')
    return (
        Title(get_title(nb)),
        Style(':root {font-family: system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", sans-serif; color-scheme: light dark;} body {background-color: light-dark(#ffffff, #1a1a1a); color: light-dark(#1a1a1a, #ffffff);} p {line-height: 1.5;}'),
        render_nb(nb, wrapper=Div),
    )
```

## Getting Frontmatter

Here I study all the code in `get_frontmatter`, bringing in everything it depends on.


```python
_RE_FM_BASE=r'''^---\s*
(.*?\S+.*?)
---\s*'''
```


```python
_re_fm_nb = re.compile(_RE_FM_BASE+'$', flags=re.DOTALL)
```

I asked AI to explain this regex:

This regex pattern is designed to match YAML frontmatter at the start of a document:

1. `^---\s*` - Matches start of text (`^`), three dashes, and optional whitespace
2. `(.*?\S+.*?)` - Captures content between dashes:
   - `.*?` - Any chars (non-greedy)
   - `\S+` - At least one non-whitespace char
   - `.*?` - Any chars (non-greedy)
3. `---\s*` - Matches three dashes and optional whitespace
4. `$` - End of text (with `re.DOTALL` flag allowing . to match newlines)

This matches standard YAML frontmatter format like:
```yaml
---
title: My Post
date: 2024-01-22
---
```


```python
def _fm2dict(s:str, nb=True):
    "Load YAML frontmatter into a `dict`"
    re_fm = _re_fm_nb if nb else _re_fm_md
    match = re_fm.search(s.strip())
    return yaml.safe_load(match.group(1)) if match else {}
```

This function is for notebooks with YAML frontmatter.

With `nb2fasthtml` the first notebook or Quarto/Markdown cell is frontmatter, and the function that reads it is customizable. By default it's:


```python
def get_frontmatter(source,     # metatadata source (jupyter cell or md content)
                    nb_file=True,    # Is jupyter nb or qmd file
                    md_fm=False # md or raw style frontmatter
                   ):
    if not nb_file: return _fm2dict(source)
    if md_fm:       return _md2dict(source.source)
    return _fm2dict(source.source, nb_file) 
```

We can see that it works with Quarto .qmd files in addition to Jupyter .ipynb files.

## Trying It on an Example Notebook


```python
nb = read_nb(Path("/Users/arg/fun/arg-blog-fasthtml/nbs/2025-01-22-MonsterUI-Buttons-and-Links.ipynb"))
nb.cells[0]
```




```json
{ 'cell_type': 'markdown',
  'idx_': 0,
  'metadata': {},
  'source': '# MonsterUI Buttons and Links'}
```



This is how `render_nb` calls `get_frontmatter`:`


```python
fm = get_frontmatter(nb.cells[0])
fm
```




    {}




```python
_fm2dict(nb.cells[0].source, nb)
```




    {}



## My Multi-Cell Frontmatter Format

At first I didn't like frontmatter. I realize now that it's just YAML frontmatter that bothers me, creating a bit of mental overhead. I want my daily notebooks to feel like regular Jupyter notebooks, and I can only get into flow with writing if I have nothing bothering me.

This is perhaps a bit ambitious, but I would love my daily notebooks on audrey.feldroy.com to have literate multi-cell frontmatter, inspired by the nicely literate Markdown [llmstxt.org](https://llmstxt.org/) format. My spec for it:

### Cell 0: Title in a Markdown Heading


```python
nb.cells[0]
```




```json
{ 'cell_type': 'markdown',
  'idx_': 0,
  'metadata': {},
  'source': '# MonsterUI Buttons and Links'}
```



### Cell 1: Short Description in a Markdown Paragraph


```python
nb.cells[1]
```




```json
{ 'cell_type': 'markdown',
  'idx_': 1,
  'metadata': {},
  'source': 'Iterating through the `ButtonT` enum to show all MonsterUI button '
            'types visually.'}
```



This would be a separate cell, to allow me to grab it easily on the index page and in self-referential examples in future notebooks. I often use my old notebooks as examples in new notebooks.

I considered keeping it in one cell separated by `\n\n`, but I really do like it in a separate cell for ease of use. It's also nice to have less surface area for errors: sometimes I find myself forgetting if I need 1 line break or 2, and this helps me.

### Cell 2: Imports


```python
nb.cells[2]
```




```json
{ 'cell_type': 'code',
  'execution_count': 4,
  'idx_': 2,
  'metadata': {},
  'outputs': [],
  'source': 'from fastcore.utils import *\n'
            'from fasthtml.common import *\n'
            'from monsterui.all import *'}
```



This is a `code` cell containing the imports for my notebook. I always have at least 1 import. I need them for at least 1 Python frontmatter cell, so I make them my first Python cell.

### Cell 3: Tags


```python
nb.cells[3]
```




```json
{ 'cell_type': 'code',
  'execution_count': 2,
  'idx_': 3,
  'metadata': {},
  'outputs': [],
  'source': 'tags = ["MonsterUI"]'}
```



This is a `code` cell containing a Python list of tags. I would love to play with creating tag components, and this is convenient for me to grab and use.

## Customizing Headers Per Route

Can FastHTML headers be customized differently for different routes?

The typical pattern is to set them at the app level, like `app, rt = fast_app(hdrs=Theme.slate.headers())`. Let's see if I can change this. 

### Cell 4: FastHTML Headers

This is a `code` cell containing a Python definition of my FastHTML headers for the particular page. My use case for this is that I like to experiment deeply with different FastHTML headers in different daily notebooks. 

My use cases include:

* Sometimes I want vanilla CSS and JS, and other times I want the MonsterUI headers.
* If I'm using daily notebooks to explore code cell rendering, sometimes I want to render code cells with HighlightJS, other times with Pygments or another library.

I definitely don't want all my notebooks rendered by nb2fasthtml with the same FastHTML headers!

At the moment I'm not sure I like how I've defined this cell, but let's go with it and see what happens. I may get rid of it later.

## How Do Headers Even Work in `FastHTML()`?


```python
nb.cells[4]
```




```json
{ 'cell_type': 'code',
  'execution_count': 5,
  'idx_': 4,
  'metadata': {},
  'outputs': [],
  'source': 'hdrs = (Theme.blue.headers(), MarkdownJS(), '
            "HighlightJS(langs=['python', 'javascript', 'html', 'css']))"}
```



I see this in `fasthtml.core`:


```python
def def_hdrs(htmx=True, surreal=True):
    "Default headers for a FastHTML app"
    hdrs = []
    if surreal: hdrs = [surrsrc,scopesrc] + hdrs
    if htmx: hdrs = [htmxsrc,fhjsscr] + hdrs
    return [charset, viewport] + hdrs
```


```python
def_hdrs()
```




    [meta((),{'charset': 'utf-8'}),
     meta((),{'name': 'viewport', 'content': 'width=device-width, initial-scale=1, viewport-fit=cover'}),
     script((),{'src': 'https://unpkg.com/htmx.org@2.0.4/dist/htmx.min.js'}),
     script((),{'src': 'https://cdn.jsdelivr.net/gh/answerdotai/fasthtml-js@1.0.12/fasthtml.js'}),
     script((),{'src': 'https://cdn.jsdelivr.net/gh/answerdotai/surreal@main/surreal.js'}),
     script((),{'src': 'https://cdn.jsdelivr.net/gh/gnat/css-scope-inline@main/script.js'})]



I'm breaking down portions of `FastHTML()` here to try and understand better:


```python
hdrs = def_hdrs()
hdrs
```




    [meta((),{'charset': 'utf-8'}),
     meta((),{'name': 'viewport', 'content': 'width=device-width, initial-scale=1, viewport-fit=cover'}),
     script((),{'src': 'https://unpkg.com/htmx.org@2.0.4/dist/htmx.min.js'}),
     script((),{'src': 'https://cdn.jsdelivr.net/gh/answerdotai/fasthtml-js@1.0.12/fasthtml.js'}),
     script((),{'src': 'https://cdn.jsdelivr.net/gh/answerdotai/surreal@main/surreal.js'}),
     script((),{'src': 'https://cdn.jsdelivr.net/gh/gnat/css-scope-inline@main/script.js'})]




```python
ftrs = None
exts = 'head-support'
```


```python
hdrs,ftrs,exts = map(listify, (hdrs,ftrs,exts))
```

### HTMX Extensions in FastHTML Headers


```python
htmx_exts = {
    "head-support": "https://unpkg.com/htmx-ext-head-support@2.0.3/head-support.js",
    "preload": "https://unpkg.com/htmx-ext-preload@2.1.0/preload.js",
    "class-tools": "https://unpkg.com/htmx-ext-class-tools@2.0.1/class-tools.js",
    "loading-states": "https://unpkg.com/htmx-ext-loading-states@2.0.0/loading-states.js",
    "multi-swap": "https://unpkg.com/htmx-ext-multi-swap@2.0.0/multi-swap.js",
    "path-deps": "https://unpkg.com/htmx-ext-path-deps@2.0.0/path-deps.js",
    "remove-me": "https://unpkg.com/htmx-ext-remove-me@2.0.0/remove-me.js",
    "ws": "https://unpkg.com/htmx-ext-ws@2.0.2/ws.js",
    "chunked-transfer": "https://unpkg.com/htmx-ext-transfer-encoding-chunked@0.4.0/transfer-encoding-chunked.js"
}
```

#### Head Support

That's nice that FastHTML makes it easy to add these HTMX extensions. I went back and changed `exts = None` to `exts = 'head-support'` just to see what happens.


```python
exts = {k:htmx_exts[k] for k in exts}
exts
```




    {'head-support': 'https://unpkg.com/htmx-ext-head-support@2.0.3/head-support.js'}



### How Scripts Are Added to Head


```python
hdrs += [Script(src=ext) for ext in exts.values()]
```


```python
hdrs
```




    [meta((),{'charset': 'utf-8'}),
     meta((),{'name': 'viewport', 'content': 'width=device-width, initial-scale=1, viewport-fit=cover'}),
     script((),{'src': 'https://unpkg.com/htmx.org@2.0.4/dist/htmx.min.js'}),
     script((),{'src': 'https://cdn.jsdelivr.net/gh/answerdotai/fasthtml-js@1.0.12/fasthtml.js'}),
     script((),{'src': 'https://cdn.jsdelivr.net/gh/answerdotai/surreal@main/surreal.js'}),
     script((),{'src': 'https://cdn.jsdelivr.net/gh/gnat/css-scope-inline@main/script.js'}),
     script(('',),{'src': 'https://unpkg.com/htmx-ext-head-support@2.0.3/head-support.js'})]



The [htmx Head Tag Support Extension](https://htmx.org/extensions/head-support/) adds support for head tags in responses to htmx requests. That looks cool. I want to explore it another day.

### Extra JS Headers for Notebook-Based FastHTML Apps

Exploring the stuff inside `if IN_NOTEBOOK`:


```python
hdrs.append(iframe_scr)
hdrs
```




    [meta((),{'charset': 'utf-8'}),
     meta((),{'name': 'viewport', 'content': 'width=device-width, initial-scale=1, viewport-fit=cover'}),
     script((),{'src': 'https://unpkg.com/htmx.org@2.0.4/dist/htmx.min.js'}),
     script((),{'src': 'https://cdn.jsdelivr.net/gh/answerdotai/fasthtml-js@1.0.12/fasthtml.js'}),
     script((),{'src': 'https://cdn.jsdelivr.net/gh/answerdotai/surreal@main/surreal.js'}),
     script((),{'src': 'https://cdn.jsdelivr.net/gh/gnat/css-scope-inline@main/script.js'}),
     script(('',),{'src': 'https://unpkg.com/htmx-ext-head-support@2.0.3/head-support.js'}),
     script(("\n    function sendmsg() {\n        window.parent.postMessage({height: document.documentElement.offsetHeight}, '*');\n    }\n    window.onload = function() {\n        sendmsg();\n        document.body.addEventListener('htmx:afterSettle',    sendmsg);\n        document.body.addEventListener('htmx:wsAfterMessage', sendmsg);\n    };",),{}),
     script(("\n    function sendmsg() {\n        window.parent.postMessage({height: document.documentElement.offsetHeight}, '*');\n    }\n    window.onload = function() {\n        sendmsg();\n        document.body.addEventListener('htmx:afterSettle',    sendmsg);\n        document.body.addEventListener('htmx:wsAfterMessage', sendmsg);\n    };",),{})]



Ah, the `HTMX()` `IFrame` uses websockets and the JS is added like this. So much to explore another day!

Inside of `if nb_hdrs` there is:


```python
display(HTML(to_xml(tuple(hdrs))))
```


<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<script src="https://unpkg.com/htmx.org@2.0.4/dist/htmx.min.js"></script><script src="https://cdn.jsdelivr.net/gh/answerdotai/fasthtml-js@1.0.12/fasthtml.js"></script><script src="https://cdn.jsdelivr.net/gh/answerdotai/surreal@main/surreal.js"></script><script src="https://cdn.jsdelivr.net/gh/gnat/css-scope-inline@main/script.js"></script><script src="https://unpkg.com/htmx-ext-head-support@2.0.3/head-support.js"></script><script>
    function sendmsg() {
        window.parent.postMessage({height: document.documentElement.offsetHeight}, '*');
    }
    window.onload = function() {
        sendmsg();
        document.body.addEventListener('htmx:afterSettle',    sendmsg);
        document.body.addEventListener('htmx:wsAfterMessage', sendmsg);
    };</script><script>
    function sendmsg() {
        window.parent.postMessage({height: document.documentElement.offsetHeight}, '*');
    }
    window.onload = function() {
        sendmsg();
        document.body.addEventListener('htmx:afterSettle',    sendmsg);
        document.body.addEventListener('htmx:wsAfterMessage', sendmsg);
    };</script>


Breaking that down:


```python
to_xml(tuple(hdrs))
```




    '<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n<script src="https://unpkg.com/htmx.org@2.0.4/dist/htmx.min.js"></script><script src="https://cdn.jsdelivr.net/gh/answerdotai/fasthtml-js@1.0.12/fasthtml.js"></script><script src="https://cdn.jsdelivr.net/gh/answerdotai/surreal@main/surreal.js"></script><script src="https://cdn.jsdelivr.net/gh/gnat/css-scope-inline@main/script.js"></script><script src="https://unpkg.com/htmx-ext-head-support@2.0.3/head-support.js"></script><script>\n    function sendmsg() {\n        window.parent.postMessage({height: document.documentElement.offsetHeight}, \'*\');\n    }\n    window.onload = function() {\n        sendmsg();\n        document.body.addEventListener(\'htmx:afterSettle\',    sendmsg);\n        document.body.addEventListener(\'htmx:wsAfterMessage\', sendmsg);\n    };</script><script>\n    function sendmsg() {\n        window.parent.postMessage({height: document.documentElement.offsetHeight}, \'*\');\n    }\n    window.onload = function() {\n        sendmsg();\n        document.body.addEventListener(\'htmx:afterSettle\',    sendmsg);\n        document.body.addEventListener(\'htmx:wsAfterMessage\', sendmsg);\n    };</script>'




```python
HTML(to_xml(tuple(hdrs)))
```




<script type="module">import { marked } from "https://cdn.jsdelivr.net/npm/marked/lib/marked.esm.js";
proc_htmx('.marked', e => e.innerHTML = marked.parse(e.textContent));</script>[link((),{'rel': 'stylesheet', 'href': 'https://cdn.jsdelivr.net/gh/highlightjs/cdn-release/build/styles/atom-one-dark.css', 'media': '(prefers-color-scheme: dark)'}), link((),{'rel': 'stylesheet', 'href': 'https://cdn.jsdelivr.net/gh/highlightjs/cdn-release/build/styles/atom-one-light.css', 'media': '(prefers-color-scheme: light)'}), script(('',),{'src': 'https://cdn.jsdelivr.net/gh/highlightjs/cdn-release/build/highlight.min.js'}), script(('',),{'src': 'https://cdn.jsdelivr.net/gh/arronhunt/highlightjs-copy/dist/highlightjs-copy.min.js'}), link((),{'rel': 'stylesheet', 'href': 'https://cdn.jsdelivr.net/gh/arronhunt/highlightjs-copy/dist/highlightjs-copy.min.css'}), script(('',),{'src': 'https://cdn.jsdelivr.net/gh/highlightjs/cdn-release/build/languages/python.min.js'}), script(('',),{'src': 'https://cdn.jsdelivr.net/gh/highlightjs/cdn-release/build/languages/javascript.min.js'}), script(('',),{'src': 'https://cdn.jsdelivr.net/gh/highlightjs/cdn-release/build/languages/html.min.js'}), script(('',),{'src': 'https://cdn.jsdelivr.net/gh/highlightjs/cdn-release/build/languages/css.min.js'}), script(('\nhljs.addPlugin(new CopyButtonPlugin());\nhljs.configure({\'cssSelector\': \'pre code:not([data-highlighted="yes"])\'});\nhtmx.onLoad(hljs.highlightAll);',),{'type': 'module'})]



Ah, I think I see, this is how the headers are added to the Jupyter notebook. I am reading [the IPython.display.HTML docs](https://ipython.readthedocs.io/en/stable/api/generated/IPython.display.html#IPython.display.HTML)

### Exception Handlers

A bit of a tangent, but they use `hdrs` so I'll explore them a little.


```python
def _not_found(req, exc): return Div('nope')
```


```python
exception_handlers={404:_not_found}
```


```python
htmlkw,bodykw,body_wrap = None,None,None
```


```python
def _wrap_ex(f, status_code, hdrs, ftrs, htmlkw, bodykw, body_wrap):
    async def _f(req, exc):
        req.hdrs,req.ftrs,req.htmlkw,req.bodykw = map(deepcopy, (hdrs, ftrs, htmlkw, bodykw))
        req.body_wrap = body_wrap
        res = await _handle(f, (req, exc))
        return _resp(req, res, status_code=status_code)
    return _f
```


```python
excs = {k:_wrap_ex(v, k, hdrs, ftrs, htmlkw, bodykw, body_wrap=body_wrap) for k,v in exception_handlers.items()}
```


```python
excs
```




    {404: <function __main__._wrap_ex.<locals>._f(req, exc)>}



### Headers in FastHTML Routing

I still haven't found the exact spot where headers get added to a FastHTML route handler. Time to look at routing in more detail.

I see that `route` and `_add_route` have a `body_wrap` parameter, and that it also uses `self.body_wrap`. 


```python
%%ai
Where are headers added before the Div or other FT returned by the route handler?
```

Looking at the dialog, I can help trace where headers are added to route responses. The key is in the `_resp` function mentioned in `_wrap_ex`. When a route handler returns, its response goes through `_resp` which combines the headers with the content.

Let me help find the exact mechanism. Looking at your exploration, I see:

1. Headers are stored in the request object: `req.hdrs,req.ftrs,req.htmlkw,req.bodykw = map(deepcopy, (hdrs, ftrs, htmlkw, bodykw))`
2. Route responses go through: `return _resp(req, res, status_code=status_code)`

To find exactly where headers are added, we should look at the `_resp` function in fasthtml.


```python
def _xt_resp(req, resp, status_code):
    cts,http_hdrs,tasks = _xt_cts(req, resp)
    return HTMLResponse(cts, status_code=status_code, headers=http_hdrs, background=tasks)
```


```python
def _is_ft_resp(resp): return isinstance(resp, _iter_typs+(HttpHeader,FT)) or hasattr(resp, '__ft__')
```


```python
def _resp(req, resp, cls=empty, status_code=200):
    if not resp: resp=()
    if hasattr(resp, '__response__'): resp = resp.__response__(req)
    if cls in (Any,FT): cls=empty
    if isinstance(resp, FileResponse) and not os.path.exists(resp.path): raise HTTPException(404, resp.path)
    if cls is not empty: return cls(resp, status_code=status_code)
    if isinstance(resp, Response): return resp # respect manually set status_code
    if _is_ft_resp(resp): return _xt_resp(req, resp, status_code)
    if isinstance(resp, str): cls = HTMLResponse
    elif isinstance(resp, Mapping): cls = JSONResponse
    else:
        resp = str(resp)
        cls = HTMLResponse
    return cls(resp, status_code=status_code)
```


```python
%%ai
Any ideas?
```

Yes - I see that `_xt_resp` is called for FastHTML responses (when `_is_ft_resp` returns True). The key is in `_xt_cts` which we haven't seen yet. Let's look at that function - it's likely where the headers from `req.hdrs` get combined with the response content.

Would you like me to help find `_xt_cts` in the FastHTML source?


```python
def _xt_cts(req, resp):
    resp = flat_tuple(resp)
    resp = resp + tuple(getattr(req, 'injects', ()))
    http_hdrs,resp = partition(resp, risinstance(HttpHeader))
    http_hdrs = {o.k:str(o.v) for o in http_hdrs}
    tasks,resp = partition(resp, risinstance(BackgroundTask))
    ts = BackgroundTasks()
    for t in tasks: ts.tasks.append(t)
    hdr_tags = 'title','meta','link','style','base'
    heads,bdy = partition(resp, lambda o: getattr(o, 'tag', '') in hdr_tags)
    if resp and 'hx-request' not in req.headers and not any(getattr(o, 'tag', '')=='html' for o in resp):
        title = [] if any(getattr(o, 'tag', '')=='title' for o in heads) else [Title(req.app.title)]
        resp = respond(req, [*heads, *title], bdy)
    return _to_xml(req, resp, indent=fh_cfg.indent), http_hdrs, ts
```

Okay! I see clues here. Breaking relevant parts of it down...


```python
hdr_tags = 'title','meta','link','style','base'
heads,bdy = partition(resp, lambda o: getattr(o, 'tag', '') in hdr_tags)
heads
```


    ---------------------------------------------------------------------------

    NameError                                 Traceback (most recent call last)

    Cell In[117], line 2
          1 hdr_tags = 'title','meta','link','style','base'
    ----> 2 heads,bdy = partition(resp, lambda o: getattr(o, 'tag', '') in hdr_tags)
          3 heads


    NameError: name 'resp' is not defined



```python
%%aip
Construct a resp
```


```python
# Let's create a simple response with some header tags and body content
resp = (
    Title("Test Page"),
    Meta(name="description", content="A test page"),
    Link(rel="stylesheet", href="style.css"),
    Style("body { color: blue }"),
    Div("Some content"),
    P("More content")
)
resp
```




    (title(('Test Page',),{}),
     meta((),{'name': 'description', 'content': 'A test page'}),
     link((),{'rel': 'stylesheet', 'href': 'style.css'}),
     style(('body { color: blue }',),{}),
     div(('Some content',),{}),
     p(('More content',),{}))




```python
# Now try partition to see what gets separated into heads vs body
heads, bdy = partition(resp, lambda o: getattr(o, 'tag', '') in ('title','meta','link','style','base'))
print("Headers:", heads)
```

    Headers: (title(('Test Page',),{}), meta((),{'name': 'description', 'content': 'A test page'}), link((),{'rel': 'stylesheet', 'href': 'style.css'}), style(('body { color: blue }',),{}))



```python
print("Body:", bdy)
```

    Body: (div(('Some content',),{}), p(('More content',),{}))



```python
%%ai
What does _xt_cts do?
```

Based on the code and our exploration, `_xt_cts` does several key things:

1. Flattens and processes response tuple:
   ```python
   resp = flat_tuple(resp)
   resp = resp + tuple(getattr(req, 'injects', ()))
   ```

2. Extracts HTTP headers and background tasks:
   ```python
   http_hdrs,resp = partition(resp, risinstance(HttpHeader))
   http_hdrs = {o.k:str(o.v) for o in http_hdrs}
   tasks,resp = partition(resp, risinstance(BackgroundTask))
   ```

3. Separates HTML head tags from body content:
   ```python
   heads,bdy = partition(resp, lambda o: getattr(o.tag, '') in ('title','meta','link','style','base'))
   ```

4. For non-HTMX requests, wraps content in full HTML response:
   ```python
   if resp and 'hx-request' not in req.headers and not any(getattr(o, 'tag', '')=='html' for o in resp):
       title = [] if any(getattr(o, 'tag', '')=='title' for o in heads) else [Title(req.app.title)]
       resp = respond(req, [*heads, *title], bdy)
   ```

5. Returns tuple of:
   - XML-rendered content
   - HTTP headers dict
   - Background tasks

This is where FastHTML route responses get transformed into full HTML documents with proper head/body structure.

Whoa, that's so cool how the response gets partitioned.


```python
%%ai
What could the cts in _xt_cts be short for? XT is like FT I think
```

Given the context and that it's transforming content into XML/HTML, `cts` is most likely short for "contents". So `_xt_cts` would be "transform contents" - where `xt` is like `ft` (FastHTML Transform) and `cts` is contents.

This makes sense since the function is all about transforming and organizing the contents of the response into proper HTML structure with headers, body, etc. before rendering to XML.

## Checking If the Notebook Needs MonsterUI Headers


```python
nb.cells[3].source
```




    'tags = ["MonsterUI"]'




```python
"MonsterUI" in nb.cells[3].source
```




    True



A bit hacky but works for now. Maybe I don't need tags to be a Python list after all, haha. I'll leave it, though.

## Conditionally Including MonsterUI Headers

Modifying the `notebook` handler that calles `render_nb`:


```python
def get_title(nb):
    "Get title from `fname` notebook's cell 0 source by stripping '# ' prefix"
#     nbc = read_nb(fname)
    nb = nb.cells[0].source.lstrip('# ')
    if '\n' in nb:
        return first(nbc.split('\n'))
    return nb
```


```python
@rt('/nbs/{name}')
def notebook(name: str):
    fpath = Path(f'nbs/{name}.ipynb')
    nb = read_nb(fpath)
    if "MonsterUI" in nb.cells[3].source:
        return (
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
```


```python
name = "2025-01-22-MonsterUI-Buttons-and-Links"
fpath = Path(f'nbs/{name}.ipynb')
fpath
```




    Path('nbs/2025-01-22-MonsterUI-Buttons-and-Links.ipynb')




```python
fpath.absolute()
```




    Path('/Users/arg/fun/arg-drafts/nbs/2025-01-22-MonsterUI-Buttons-and-Links.ipynb')




```python
notebook("2025-01-22-MonsterUI-Buttons-and-Links")
```




    (link((),{'rel': 'stylesheet', 'href': 'https://unpkg.com/franken-ui@1.1.0/dist/css/core.min.css'}),
     script(('',),{'type': 'module', 'src': 'https://unpkg.com/franken-ui@1.1.0/dist/js/core.iife.js'}),
     script(('',),{'type': 'module', 'src': 'https://cdn.jsdelivr.net/gh/answerdotai/monsterui@main/monsterui/icon.iife.js'}),
     script(('',),{'src': 'https://cdn.tailwindcss.com'}),
     script(('\n        const htmlElement = document.documentElement;\n        \n            if (\n                localStorage.getItem("mode") === "dark" ||\n                (!("mode" in localStorage) &&\n                window.matchMedia("(prefers-color-scheme: dark)").matches)\n            ) {\n                htmlElement.classList.add("dark");\n            } else {\n                htmlElement.classList.remove("dark");\n            }\n        \n        htmlElement.classList.add(localStorage.getItem("theme") || "uk-theme-blue");\n    ',),{}),
     link((),{'rel': 'stylesheet', 'href': 'https://cdn.jsdelivr.net/npm/daisyui@4.12.22/dist/full.min.css'}),
     style(('\n:root {\n  --p: from hsl(var(--primary)) l c h;\n  --pc: from hsl(var(--primary-foreground)) l c h;\n  --s: from hsl(var(--secondary)) l c h;\n  --sc: from hsl(var(--secondary-foreground)) l c h;\n  --b2: from hsl(var(--card-background)) l c h;\n  --b1: from hsl(var(--background)) l c h;\n  --bc: from hsl(var(--foreground)) l c h;\n  --b3: from hsl(var(--ring)) l c h;\n  --er: from hsl(var(--destructive)) l c h;\n  --erc: from hsl(var(--destructive-foreground)) l c h;\n}\n',),{}),
     title(('MonsterUI Buttons and Links',),{}),
     div((div((h1(('MonsterUI Buttons and Links',),{}),),{'class': 'frontmatter'}), div((div(('Iterating through the `ButtonT` enum to show all MonsterUI button types visually.',),{'class': 'marked'}),),{}), article((div(('\n```python\nfrom fastcore.utils import *\nfrom fasthtml.common import *\nfrom monsterui.all import *\n```\n',),{'class': 'marked'}), ''),{}), article((div(('\n```python\ntags = ["MonsterUI"]\n```\n',),{'class': 'marked'}), ''),{}), article((div(("\n```python\nhdrs = (Theme.blue.headers(), MarkdownJS(), HighlightJS(langs=['python', 'javascript', 'html', 'css']))\n```\n",),{'class': 'marked'}), ''),{}), div((div(('## Setup',),{'class': 'marked'}),),{}), article((div(('\n```python\nButton()\n```\n',),{'class': 'marked'}), footer(('<pre><code class="language-html">&lt;button type="submit" class="uk-button uk-button-default"&gt;&lt;/button&gt;\n</code></pre>\n',),{})),{}), article((div(('\n```python\nshow(Button("Click me"))\n```\n',),{'class': 'marked'}), footer(('<button type="submit" class="uk-button uk-button-default">Click me</button>',),{})),{}), article((div(('\n```python\nshow(A("My link", href="example.com", cls=AT.muted))\n```\n',),{'class': 'marked'}), footer(('<a href="example.com" class="uk-link-muted">My link</a>',),{})),{}), article((div(('\n```python\nshow(NavBar(title="MySite", nav_links=(A("Link 1"), A("Link 2"))))\n```\n',),{'class': 'marked'}), footer(('<div>\n  <div class="uk-container mt-5 uk-container-xlarge">\n    <div class="md:flex md:relative">\n      <div class="uk-navbar-left ">\n        <h1 class="uk-h1 ">MySite</h1>\n<uk-icon icon="menu" height="30" width="30" hx-on-click="htmx.find(\'#_S_0fkn7ATy2jXQuJL72PNg\').classList.toggle(\'hidden\')" class="md:hidden"></uk-icon>      </div>\n      <div id="_S_0fkn7ATy2jXQuJL72PNg" class="uk-navbar-right hidden md:flex md:justify-between">\n        <nav class="uk-navbar-nav w-full flex-col md:flex-row">\n<a href="#">Link 1</a><a href="#">Link 2</a>        </nav>\n      </div>\n    </div>\n  </div>\n</div>\n',),{})),{}), article((div(('\n```python\nshow(Button("Hey",cls=ButtonT.primary))\n```\n',),{'class': 'marked'}), footer(('<button type="submit" class="uk-button uk-button-primary">Hey</button>',),{})),{}), article((div(('\n```python\nButtonT\n```\n',),{'class': 'marked'}), footer(('<pre ><code>&lt;enum &#x27;ButtonT&#x27;&gt;</code></pre>',),{})),{}), article((div(('\n```python\n[t.name for t in ButtonT]\n```\n',),{'class': 'marked'}), footer(('<pre ><code>[&#x27;default&#x27;, &#x27;primary&#x27;, &#x27;secondary&#x27;, &#x27;danger&#x27;, &#x27;text&#x27;, &#x27;link&#x27;, &#x27;ghost&#x27;]</code></pre>',),{})),{}), div((div(('**AI Prompt**\n\nIs there a convenience function in enum to list all these?',),{'class': 'marked'}),),{}), div((div(('**AI Response**\n\nYes! The `Enum` class in Python has a built-in method called `__members__`. You can use it like this:\n\n```python\nButtonT.__members__\n```\n\nWould you like me to explain more about what this returns and how it differs from the list comprehension approach you used?',),{'class': 'marked'}),),{}), article((div(('\n```python\nButtonT.__members__\n```\n',),{'class': 'marked'}), footer(('<pre ><code>mappingproxy({&#x27;default&#x27;: &lt;ButtonT.default: &#x27;uk-button-default&#x27;&gt;,\n              &#x27;primary&#x27;: &lt;ButtonT.primary: &#x27;uk-button-primary&#x27;&gt;,\n              &#x27;secondary&#x27;: &lt;ButtonT.secondary: &#x27;uk-button-secondary&#x27;&gt;,\n              &#x27;danger&#x27;: &lt;ButtonT.danger: &#x27;uk-button-danger&#x27;&gt;,\n              &#x27;text&#x27;: &lt;ButtonT.text: &#x27;uk-button-text&#x27;&gt;,\n              &#x27;link&#x27;: &lt;ButtonT.link: &#x27;uk-button-link&#x27;&gt;,\n              &#x27;ghost&#x27;: &lt;ButtonT.ghost: &#x27;uk-button-ghost&#x27;&gt;})</code></pre>',),{})),{}), article((div(('\n```python\nL(ButtonT.__members__)\n```\n',),{'class': 'marked'}), footer(('<pre ><code>(#7) [&#x27;default&#x27;,&#x27;primary&#x27;,&#x27;secondary&#x27;,&#x27;danger&#x27;,&#x27;text&#x27;,&#x27;link&#x27;,&#x27;ghost&#x27;]</code></pre>',),{})),{}), article((div(('\n```python\ndef _Button(t): return Button(f"{t} button",cls=t)\nbtns = L(ButtonT.__members__).map(_Button)\nbtns\n```\n',),{'class': 'marked'}), footer(('<pre ><code>(#7) [button((&#x27;default button&#x27;,),{&#x27;type&#x27;: &#x27;submit&#x27;, &#x27;class&#x27;: &#x27;uk-button default&#x27;}),button((&#x27;primary button&#x27;,),{&#x27;type&#x27;: &#x27;submit&#x27;, &#x27;class&#x27;: &#x27;uk-button primary&#x27;}),button((&#x27;secondary button&#x27;,),{&#x27;type&#x27;: &#x27;submit&#x27;, &#x27;class&#x27;: &#x27;uk-button secondary&#x27;}),button((&#x27;danger button&#x27;,),{&#x27;type&#x27;: &#x27;submit&#x27;, &#x27;class&#x27;: &#x27;uk-button danger&#x27;}),button((&#x27;text button&#x27;,),{&#x27;type&#x27;: &#x27;submit&#x27;, &#x27;class&#x27;: &#x27;uk-button text&#x27;}),button((&#x27;link button&#x27;,),{&#x27;type&#x27;: &#x27;submit&#x27;, &#x27;class&#x27;: &#x27;uk-button link&#x27;}),button((&#x27;ghost button&#x27;,),{&#x27;type&#x27;: &#x27;submit&#x27;, &#x27;class&#x27;: &#x27;uk-button ghost&#x27;})]</code></pre>',),{})),{}), article((div(('\n```python\nto_xml(Div(*btns))\n```\n',),{'class': 'marked'}), footer(('<pre ><code>&#x27;&lt;div&gt;\\n&lt;button type=&quot;submit&quot; class=&quot;uk-button default&quot;&gt;default button&lt;/button&gt;&lt;button type=&quot;submit&quot; class=&quot;uk-button primary&quot;&gt;primary button&lt;/button&gt;&lt;button type=&quot;submit&quot; class=&quot;uk-button secondary&quot;&gt;secondary button&lt;/button&gt;&lt;button type=&quot;submit&quot; class=&quot;uk-button danger&quot;&gt;danger button&lt;/button&gt;&lt;button type=&quot;submit&quot; class=&quot;uk-button text&quot;&gt;text button&lt;/button&gt;&lt;button type=&quot;submit&quot; class=&quot;uk-button link&quot;&gt;link button&lt;/button&gt;&lt;button type=&quot;submit&quot; class=&quot;uk-button ghost&quot;&gt;ghost button&lt;/button&gt;&lt;/div&gt;\\n&#x27;</code></pre>',),{})),{}), article((div(('\n```python\nshow(to_xml(Div(*btns)))\n```\n',),{'class': 'marked'}), footer(('<div>\n<button type="submit" class="uk-button default">default button</button><button type="submit" class="uk-button primary">primary button</button><button type="submit" class="uk-button secondary">secondary button</button><button type="submit" class="uk-button danger">danger button</button><button type="submit" class="uk-button text">text button</button><button type="submit" class="uk-button link">link button</button><button type="submit" class="uk-button ghost">ghost button</button></div>\n',),{})),{}), div((div(("**AI Prompt**\n\nWhy don't the buttons look right?",),{'class': 'marked'}),),{}), div((div(('**AI Response**\n\nLooking at the button classes in the HTML output, I notice the classes are missing the `uk-button-` prefix that we saw in the `ButtonT` enum values. Instead, they just have `uk-button default`, `uk-button primary`, etc.\n\nLet\'s check what\'s happening by looking at one button directly:\n\n```python\nshow(Button("test", cls=ButtonT.primary))\n```\n\nThis should help us see if the issue is in how we\'re passing the enum values to the Button constructor.',),{'class': 'marked'}),),{}), div((div(('**AI Prompt**\n\ndef _Button(t): return Button(f"{t} button",cls=ButtonT.t)\nbtns = L(ButtonT.__members__).map(_Button)\nbtns',),{'class': 'marked'}),),{}), div((div(("**AI Response**\n\nAh, I see the issue in your code. `ButtonT.t` isn't correct - you're trying to access a property `t` on `ButtonT`, but `t` is actually the variable in your function containing the member name.\n\nInstead, you should use `ButtonT[t]` or `getattr(ButtonT, t)` to look up the enum member by name. Would you like to try fixing this?",),{'class': 'marked'}),),{}), article((div(('\n```python\ndef _Button(t): return Button(f"{t} button",cls=ButtonT[t])\nbtns = L(ButtonT.__members__).map(_Button)\nshow(Div(*btns))\n```\n',),{'class': 'marked'}), footer(('<div>\n<button type="submit" class="uk-button uk-button-default">default button</button><button type="submit" class="uk-button uk-button-primary">primary button</button><button type="submit" class="uk-button uk-button-secondary">secondary button</button><button type="submit" class="uk-button uk-button-danger">danger button</button><button type="submit" class="uk-button uk-button-text">text button</button><button type="submit" class="uk-button uk-button-link">link button</button><button type="submit" class="uk-button uk-button-ghost">ghost button</button></div>\n',),{})),{}), div((div(('## Improvements ',),{'class': 'marked'}),),{}), div((div(('This part is from SolveIt office hours with Isaac Flath.',),{'class': 'marked'}),),{}), div((div(('**AI Prompt**\n\nIs there any other way to get `ButtonT.__members__` in enum or otherwise?',),{'class': 'marked'}),),{}), div((div(('**AI Response**\n\nYes! There are a few other ways to get enum members:\n\n1. Using `list(ButtonT)` - this gives you the values\n2. Using `ButtonT._member_names_` - this gives you just the names\n3. Using `ButtonT._member_map_` - similar to `__members__` but returns a regular dict\n\nWould you like to try any of these to see how they differ?',),{'class': 'marked'}),),{}), article((div(('\n```python\nlist(ButtonT)[0].value\n```\n',),{'class': 'marked'}), footer(('<pre ><code>&#x27;uk-button-default&#x27;</code></pre>',),{})),{}), article((div(('\n```python\nDiv(*[Button(v,cls=v) for v in list(ButtonT)])\n```\n',),{'class': 'marked'}), footer(('<pre><code class="language-html">&lt;div&gt;\n&lt;button type="submit" class="uk-button uk-button-default"&gt;uk-button-default&lt;/button&gt;&lt;button type="submit" class="uk-button uk-button-primary"&gt;uk-button-primary&lt;/button&gt;&lt;button type="submit" class="uk-button uk-button-secondary"&gt;uk-button-secondary&lt;/button&gt;&lt;button type="submit" class="uk-button uk-button-danger"&gt;uk-button-danger&lt;/button&gt;&lt;button type="submit" class="uk-button uk-button-text"&gt;uk-button-text&lt;/button&gt;&lt;button type="submit" class="uk-button uk-button-link"&gt;uk-button-link&lt;/button&gt;&lt;button type="submit" class="uk-button uk-button-ghost"&gt;uk-button-ghost&lt;/button&gt;&lt;/div&gt;\n\n</code></pre>\n',),{})),{}), article((div(('\n```python\nshow(Div(*[Button(v,cls=v) for v in list(ButtonT)]))\n```\n',),{'class': 'marked'}), footer(('<div>\n<button type="submit" class="uk-button uk-button-default">uk-button-default</button><button type="submit" class="uk-button uk-button-primary">uk-button-primary</button><button type="submit" class="uk-button uk-button-secondary">uk-button-secondary</button><button type="submit" class="uk-button uk-button-danger">uk-button-danger</button><button type="submit" class="uk-button uk-button-text">uk-button-text</button><button type="submit" class="uk-button uk-button-link">uk-button-link</button><button type="submit" class="uk-button uk-button-ghost">uk-button-ghost</button></div>\n',),{})),{}), article((div(('\n```python\nshow(DivLAligned(*[Button(v,cls=v) for v in list(ButtonT)]))\n```\n',),{'class': 'marked'}), footer(('<div class="uk-flex uk-flex-left uk-flex-middle space-x-4">\n<button type="submit" class="uk-button uk-button-default">uk-button-default</button><button type="submit" class="uk-button uk-button-primary">uk-button-primary</button><button type="submit" class="uk-button uk-button-secondary">uk-button-secondary</button><button type="submit" class="uk-button uk-button-danger">uk-button-danger</button><button type="submit" class="uk-button uk-button-text">uk-button-text</button><button type="submit" class="uk-button uk-button-link">uk-button-link</button><button type="submit" class="uk-button uk-button-ghost">uk-button-ghost</button></div>\n',),{})),{}), article((div(('\n```python\nshow(Grid(*[Button(v,cls=v) for v in list(ButtonT)]))\n```\n',),{'class': 'marked'}), footer(('<div class="grid grid-cols-1 sm:grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">\n<button type="submit" class="uk-button uk-button-default">uk-button-default</button><button type="submit" class="uk-button uk-button-primary">uk-button-primary</button><button type="submit" class="uk-button uk-button-secondary">uk-button-secondary</button><button type="submit" class="uk-button uk-button-danger">uk-button-danger</button><button type="submit" class="uk-button uk-button-text">uk-button-text</button><button type="submit" class="uk-button uk-button-link">uk-button-link</button><button type="submit" class="uk-button uk-button-ghost">uk-button-ghost</button></div>\n',),{})),{})),{'class': 'container'}))




```python
notebook("2025-01-21-SVG-Animation-in-FastHTML")
```




    (title(('SVG Animations in FastHTML',),{}),
     style((':root {font-family: system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", sans-serif; color-scheme: light dark;} body {background-color: light-dark(#ffffff, #1a1a1a); color: light-dark(#1a1a1a, #ffffff);} p {line-height: 1.5;}',),{}),
     div((div((h1(('SVG Animations in FastHTML',),{}),),{'class': 'frontmatter'}), div((div(('Exploring how to make basic SVG animations work with FastHTML.',),{'class': 'marked'}),),{}), article((div(('\n```python\nfrom fastcore.meta import delegates\nfrom fastcore.utils import snake2camel\nfrom fasthtml.common import *\nfrom fasthtml.svg import *\n```\n',),{'class': 'marked'}), ''),{}), div((div(('## FastHTML SVG Docs Examples',),{'class': 'marked'}),),{}), div((div(('The [FastHTML SVG API Docs](https://docs.fastht.ml/api/svg.html) introduce you to `fasthtml.svg` with this nice circle specified as an SVG string:',),{'class': 'marked'}),),{}), article((div(('\n```python\nsvg = \'<svg width="50" height="50"><circle cx="20" cy="20" r="15" fill="red"></circle></svg>\'\nshow(NotStr(svg))\n```\n',),{'class': 'marked'}), footer(('<svg width="50" height="50"><circle cx="20" cy="20" r="15" fill="red"></circle></svg>',),{})),{}), div((div(("Often you'll just want to paste these strings into your FastHTML apps, and that's fine. However, when you want to construct SVG elements programmatically via Python, you can!",),{'class': 'marked'}),),{}), article((div(('\n```python\ndef demo(el, h=50, w=50): return show(Svg(h=h,w=w)(el))\n```\n',),{'class': 'marked'}), ''),{}), article((div(("\n```python\ndemo(Rect(30, 30, fill='blue', rx=8, ry=8))\n```\n",),{'class': 'marked'}), footer(('<svg xmlns="http://www.w3.org/2000/svg" viewbox="0 0 50 50" height="50" width="50"><rect width="30" height="30" fill="blue" rx="8" ry="8"></rect></svg>',),{})),{}), div((div(('## MDN Example',),{'class': 'marked'}),),{}), div((div(("[MDN's SVG <animate> example](https://developer.mozilla.org/en-US/docs/Web/SVG/Element/animate) is:",),{'class': 'marked'}),),{}), article((div(('\n```python\nsvg = """<svg viewBox="0 0 10 10" xmlns="http://www.w3.org/2000/svg">\n  <rect width="10" height="10">\n    <animate\n      attributeName="rx"\n      values="0;5;0"\n      dur="10s"\n      repeatCount="indefinite" />\n  </rect>\n</svg>\n"""\n```\n',),{'class': 'marked'}), ''),{}), article((div(('\n```python\nshow(NotStr(svg))\n```\n',),{'class': 'marked'}), footer(('<svg viewBox="0 0 10 10" xmlns="http://www.w3.org/2000/svg">\n  <rect width="10" height="10">\n    <animate\n      attributeName="rx"\n      values="0;5;0"\n      dur="10s"\n      repeatCount="indefinite" />\n  </rect>\n</svg>\n',),{})),{}), div((div(("Why is that rectangle so big here? Let's try",),{'class': 'marked'}),),{}), article((div(('\n```python\nsvg2 = """<svg width="100" height="100">\n  <rect width="10" height="10">\n    <animate\n      attributeName="rx"\n      values="0;5;0"\n      dur="10s"\n      repeatCount="indefinite" />\n  </rect>\n</svg>\n"""\nshow(NotStr(svg2))\n```\n',),{'class': 'marked'}), footer(('<svg width="100" height="100">\n  <rect width="10" height="10">\n    <animate\n      attributeName="rx"\n      values="0;5;0"\n      dur="10s"\n      repeatCount="indefinite" />\n  </rect>\n</svg>\n',),{})),{}), div((div(('## MDN Example in FastHTML',),{'class': 'marked'}),),{}), div((div(("Currently `Rect()` doesn't accept an `animate` child. Seeing if I can make that work:",),{'class': 'marked'}),),{}), article((div(('\n```python\ndef Animate(attributeName, values, dur, repeatCount):\n    return Safe(f"<animate {attributeName=} {values=} {dur=} {repeatCount=} />")\n```\n',),{'class': 'marked'}), ''),{}), article((div(('\n```python\nAnimate(attributeName="rx", values="0;5;0", dur="10s", repeatCount="indefinite")\n```\n',),{'class': 'marked'}), footer(('<pre ><code>&quot;&lt;animate attributeName=&#x27;rx&#x27; values=&#x27;0;5;0&#x27; dur=&#x27;10s&#x27; repeatCount=&#x27;indefinite&#x27; /&gt;&quot;</code></pre>',),{})),{}), article((div(('\n```python\n@delegates(ft_svg)\ndef AnimatedRect(animate, width, height, x=0, y=0, fill=None, stroke=None, stroke_width=None, rx=None, ry=None, **kwargs):\n    "An animated standard SVG `rect` element"\n    return ft_svg(\'rect\', animate, width=width, height=height, x=x, y=y, fill=fill,\n                 stroke=stroke, stroke_width=stroke_width, rx=rx, ry=ry, **kwargs)\n```\n',),{'class': 'marked'}), ''),{}), article((div(('\n```python\nshow(Svg(AnimatedRect(\n    Animate(attributeName="rx", values="0;5;0", dur="10s", repeatCount="indefinite"), \n    width=10, height=10), h=10, w=10))\n```\n',),{'class': 'marked'}), footer(('<svg xmlns="http://www.w3.org/2000/svg" viewbox="0 0 10 10" height="10" width="10"><rect width="10" height="10"><animate attributeName=\'rx\' values=\'0;5;0\' dur=\'10s\' repeatCount=\'indefinite\' /></rect></svg>',),{})),{}), article((div(('\n```python\nshow(Svg(AnimatedRect(\n    Animate(attributeName="rx", values="0;50;0", dur="10s", repeatCount="indefinite"), \n    width=100, height=100), h=100, w=100))\n```\n',),{'class': 'marked'}), footer(('<svg xmlns="http://www.w3.org/2000/svg" viewbox="0 0 100 100" height="100" width="100"><rect width="100" height="100"><animate attributeName=\'rx\' values=\'0;50;0\' dur=\'10s\' repeatCount=\'indefinite\' /></rect></svg>',),{})),{}), article((div(('\n```python\ndemo(AnimatedRect(\n        Animate(attributeName="rx", values="0;50;0", dur="1s", repeatCount="indefinite"), \n    width=100, height=100), h=100, w=100)\n```\n',),{'class': 'marked'}), footer(('<svg xmlns="http://www.w3.org/2000/svg" viewbox="0 0 100 100" height="100" width="100"><rect width="100" height="100"><animate attributeName=\'rx\' values=\'0;50;0\' dur=\'1s\' repeatCount=\'indefinite\' /></rect></svg>',),{})),{}), div((div(('## More Complex SVG Animation',),{'class': 'marked'}),),{}), article((div(('\n```python\nsvg4 = """<svg width="100" height="100" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">\n  <!-- Gradient definitions -->\n  <defs>\n    <linearGradient id="gradient1" x1="0%" y1="0%" x2="100%" y2="100%">\n      <stop offset="0%" stop-color="#60a5fa">\n        <animate attributeName="stop-color" \n          values="#60a5fa;#8b5cf6;#ec4899;#60a5fa"\n          dur="8s" repeatCount="indefinite" />\n      </stop>\n      <stop offset="100%" stop-color="#8b5cf6">\n        <animate attributeName="stop-color" \n          values="#8b5cf6;#ec4899;#60a5fa;#8b5cf6"\n          dur="8s" repeatCount="indefinite" />\n      </stop>\n    </linearGradient>\n  </defs>\n\n  <!-- Background star burst -->\n  <g>\n    <circle cx="50" cy="50" r="45" fill="url(#gradient1)">\n      <animate attributeName="opacity"\n        values="0.3;0.5;0.3"\n        dur="3s" repeatCount="indefinite" />\n    </circle>\n  </g>\n\n  <!-- Spinning triangles -->\n  <g transform="translate(50 50)">\n    <path d="M0,-30 L26,15 L-26,15 Z" fill="#fcd34d" opacity="0.8">\n      <animateTransform attributeName="transform"\n        type="rotate"\n        from="0"\n        to="360"\n        dur="8s"\n        repeatCount="indefinite" />\n      <animate attributeName="d"\n        values="M0,-30 L26,15 L-26,15 Z;M0,-20 L35,25 L-35,25 Z;M0,-30 L26,15 L-26,15 Z"\n        dur="4s"\n        repeatCount="indefinite" />\n    </path>\n  </g>\n\n  <!-- Bouncing squares -->\n  <rect x="40" y="40" width="20" height="20" fill="#34d399" opacity="0.8">\n    <animate attributeName="x" \n      values="40;30;50;40"\n      dur="3s"\n      repeatCount="indefinite" />\n    <animate attributeName="y"\n      values="40;50;30;40"\n      dur="3s"\n      repeatCount="indefinite" />\n    <animate attributeName="rx"\n      values="0;10;0"\n      dur="3s"\n      repeatCount="indefinite" />\n  </rect>\n\n  <!-- Orbiting particles -->\n  <g>\n    <circle cx="50" cy="20" r="4" fill="#f472b6">\n      <animateMotion\n        path="M 0,0 a 30,30 0 1,1 0,0"\n        dur="3s"\n        repeatCount="indefinite" />\n      <animate attributeName="r"\n        values="4;6;4"\n        dur="1.5s"\n        repeatCount="indefinite" />\n    </circle>\n    <circle cx="80" cy="50" r="4" fill="#60a5fa">\n      <animateMotion\n        path="M 0,0 a 30,30 0 1,0 0,0"\n        dur="4s"\n        repeatCount="indefinite" />\n      <animate attributeName="r"\n        values="4;6;4"\n        dur="2s"\n        repeatCount="indefinite" />\n    </circle>\n  </g>\n\n  <!-- Dancing dots -->\n  <g>\n    <circle cx="50" cy="50" r="3" fill="#fcd34d">\n      <animateMotion\n        path="M 0,0 q 15,15 0,30 q -15,15 0,0"\n        dur="2.5s"\n        repeatCount="indefinite" />\n    </circle>\n    <circle cx="50" cy="50" r="3" fill="#f472b6">\n      <animateMotion\n        path="M 0,0 q -15,-15 -30,0 q -15,15 0,0"\n        dur="2.5s"\n        repeatCount="indefinite" />\n    </circle>\n  </g>\n\n  <!-- Pulsing rings -->\n  <circle cx="50" cy="50" r="20" fill="none" stroke="#93c5fd" stroke-width="1">\n    <animate attributeName="r"\n      values="20;30;20"\n      dur="4s"\n      repeatCount="indefinite" />\n    <animate attributeName="stroke-opacity"\n      values="1;0;1"\n      dur="4s"\n      repeatCount="indefinite" />\n  </circle>\n  <circle cx="50" cy="50" r="25" fill="none" stroke="#93c5fd" stroke-width="1">\n    <animate attributeName="r"\n      values="25;35;25"\n      dur="4s"\n      repeatCount="indefinite" />\n    <animate attributeName="stroke-opacity"\n      values="0;1;0"\n      dur="4s"\n      repeatCount="indefinite" />\n  </circle>\n</svg>"""\nshow(NotStr(svg4))\n```\n',),{'class': 'marked'}), footer(('<svg width="100" height="100" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">\n  <!-- Gradient definitions -->\n  <defs>\n    <linearGradient id="gradient1" x1="0%" y1="0%" x2="100%" y2="100%">\n      <stop offset="0%" stop-color="#60a5fa">\n        <animate attributeName="stop-color" \n          values="#60a5fa;#8b5cf6;#ec4899;#60a5fa"\n          dur="8s" repeatCount="indefinite" />\n      </stop>\n      <stop offset="100%" stop-color="#8b5cf6">\n        <animate attributeName="stop-color" \n          values="#8b5cf6;#ec4899;#60a5fa;#8b5cf6"\n          dur="8s" repeatCount="indefinite" />\n      </stop>\n    </linearGradient>\n  </defs>\n\n  <!-- Background star burst -->\n  <g>\n    <circle cx="50" cy="50" r="45" fill="url(#gradient1)">\n      <animate attributeName="opacity"\n        values="0.3;0.5;0.3"\n        dur="3s" repeatCount="indefinite" />\n    </circle>\n  </g>\n\n  <!-- Spinning triangles -->\n  <g transform="translate(50 50)">\n    <path d="M0,-30 L26,15 L-26,15 Z" fill="#fcd34d" opacity="0.8">\n      <animateTransform attributeName="transform"\n        type="rotate"\n        from="0"\n        to="360"\n        dur="8s"\n        repeatCount="indefinite" />\n      <animate attributeName="d"\n        values="M0,-30 L26,15 L-26,15 Z;M0,-20 L35,25 L-35,25 Z;M0,-30 L26,15 L-26,15 Z"\n        dur="4s"\n        repeatCount="indefinite" />\n    </path>\n  </g>\n\n  <!-- Bouncing squares -->\n  <rect x="40" y="40" width="20" height="20" fill="#34d399" opacity="0.8">\n    <animate attributeName="x" \n      values="40;30;50;40"\n      dur="3s"\n      repeatCount="indefinite" />\n    <animate attributeName="y"\n      values="40;50;30;40"\n      dur="3s"\n      repeatCount="indefinite" />\n    <animate attributeName="rx"\n      values="0;10;0"\n      dur="3s"\n      repeatCount="indefinite" />\n  </rect>\n\n  <!-- Orbiting particles -->\n  <g>\n    <circle cx="50" cy="20" r="4" fill="#f472b6">\n      <animateMotion\n        path="M 0,0 a 30,30 0 1,1 0,0"\n        dur="3s"\n        repeatCount="indefinite" />\n      <animate attributeName="r"\n        values="4;6;4"\n        dur="1.5s"\n        repeatCount="indefinite" />\n    </circle>\n    <circle cx="80" cy="50" r="4" fill="#60a5fa">\n      <animateMotion\n        path="M 0,0 a 30,30 0 1,0 0,0"\n        dur="4s"\n        repeatCount="indefinite" />\n      <animate attributeName="r"\n        values="4;6;4"\n        dur="2s"\n        repeatCount="indefinite" />\n    </circle>\n  </g>\n\n  <!-- Dancing dots -->\n  <g>\n    <circle cx="50" cy="50" r="3" fill="#fcd34d">\n      <animateMotion\n        path="M 0,0 q 15,15 0,30 q -15,15 0,0"\n        dur="2.5s"\n        repeatCount="indefinite" />\n    </circle>\n    <circle cx="50" cy="50" r="3" fill="#f472b6">\n      <animateMotion\n        path="M 0,0 q -15,-15 -30,0 q -15,15 0,0"\n        dur="2.5s"\n        repeatCount="indefinite" />\n    </circle>\n  </g>\n\n  <!-- Pulsing rings -->\n  <circle cx="50" cy="50" r="20" fill="none" stroke="#93c5fd" stroke-width="1">\n    <animate attributeName="r"\n      values="20;30;20"\n      dur="4s"\n      repeatCount="indefinite" />\n    <animate attributeName="stroke-opacity"\n      values="1;0;1"\n      dur="4s"\n      repeatCount="indefinite" />\n  </circle>\n  <circle cx="50" cy="50" r="25" fill="none" stroke="#93c5fd" stroke-width="1">\n    <animate attributeName="r"\n      values="25;35;25"\n      dur="4s"\n      repeatCount="indefinite" />\n    <animate attributeName="stroke-opacity"\n      values="0;1;0"\n      dur="4s"\n      repeatCount="indefinite" />\n  </circle>\n</svg>',),{})),{}), div((div(('I kind of like this one for representing "a sound is currently playing" for experimental audio apps.',),{'class': 'marked'}),),{})),{'class': 'container'}))



Reading that as best I can, I think the conditional header inclusion worked!

The true test of this is if it actually works when I bring it over to my arg-blog-fasthtml main.py. Let's see what happens.

## Success

Whoa, I can't believe I managed to get that working:

* https://audrey.feldroy.com/nbs/2025-01-22-MonsterUI-Buttons-and-Links shows MonsterUI styles
* https://audrey.feldroy.com/nbs/2025-01-21-SVG-Animation-in-FastHTML shows my vanilla CSS styles without MonsterUI

Go check out the main.py in https://github.com/audreyfeldroy/arg-blog-fasthtml to see how it all fits together.

I suppose we didn't actually customize `render_nb` but rather customized the part before it. Then we left the hard work of header and body partitioning to `_xt_cts`.


```python
from nb2fasthtml.core import *
```
