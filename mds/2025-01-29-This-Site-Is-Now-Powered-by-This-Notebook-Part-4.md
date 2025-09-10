# This Site Is Now Powered by This Notebook, Part 4

Here I update audrey.feldroy.com with some of the latest MonsterUI text presets.


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


    ERROR:    Exception in ASGI application
    Traceback (most recent call last):
      File "/Users/arg/.venv/lib/python3.12/site-packages/uvicorn/protocols/http/httptools_impl.py", line 409, in run_asgi
        result = await app(  # type: ignore[func-returns-value]
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
      File "/Users/arg/.venv/lib/python3.12/site-packages/uvicorn/middleware/proxy_headers.py", line 60, in __call__
        return await self.app(scope, receive, send)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
      File "/Users/arg/.venv/lib/python3.12/site-packages/starlette/applications.py", line 112, in __call__
        await self.middleware_stack(scope, receive, send)
      File "/Users/arg/.venv/lib/python3.12/site-packages/starlette/middleware/errors.py", line 187, in __call__
        raise exc
      File "/Users/arg/.venv/lib/python3.12/site-packages/starlette/middleware/errors.py", line 165, in __call__
        await self.app(scope, receive, _send)
      File "/Users/arg/.venv/lib/python3.12/site-packages/starlette/middleware/cors.py", line 85, in __call__
        await self.app(scope, receive, send)
      File "/Users/arg/.venv/lib/python3.12/site-packages/starlette/middleware/sessions.py", line 85, in __call__
        await self.app(scope, receive, send_wrapper)
      File "/Users/arg/.venv/lib/python3.12/site-packages/starlette/middleware/exceptions.py", line 62, in __call__
        await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
      File "/Users/arg/.venv/lib/python3.12/site-packages/starlette/_exception_handler.py", line 53, in wrapped_app
        raise exc
      File "/Users/arg/.venv/lib/python3.12/site-packages/starlette/_exception_handler.py", line 42, in wrapped_app
        await app(scope, receive, sender)
      File "/Users/arg/.venv/lib/python3.12/site-packages/starlette/routing.py", line 715, in __call__
        await self.middleware_stack(scope, receive, send)
      File "/Users/arg/.venv/lib/python3.12/site-packages/starlette/routing.py", line 735, in app
        await route.handle(scope, receive, send)
      File "/Users/arg/.venv/lib/python3.12/site-packages/starlette/routing.py", line 288, in handle
        await self.app(scope, receive, send)
      File "/Users/arg/.venv/lib/python3.12/site-packages/starlette/routing.py", line 76, in app
        await wrap_app_handling_exceptions(app, request)(scope, receive, send)
      File "/Users/arg/.venv/lib/python3.12/site-packages/starlette/_exception_handler.py", line 53, in wrapped_app
        raise exc
      File "/Users/arg/.venv/lib/python3.12/site-packages/starlette/_exception_handler.py", line 42, in wrapped_app
        await app(scope, receive, sender)
      File "/Users/arg/.venv/lib/python3.12/site-packages/starlette/routing.py", line 73, in app
        response = await f(request)
                   ^^^^^^^^^^^^^^^^
      File "/Users/arg/git/fasthtml/fasthtml/core.py", line 568, in _f
        if not resp: resp = await _wrap_call(f, req, sig.parameters)
                            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
      File "/Users/arg/git/fasthtml/fasthtml/core.py", line 434, in _wrap_call
        return await _handle(f, wreq)
               ^^^^^^^^^^^^^^^^^^^^^^
      File "/Users/arg/git/fasthtml/fasthtml/core.py", line 225, in _handle
        return (await f(*args, **kwargs)) if is_async_callable(f) else await run_in_threadpool(f, *args, **kwargs)
                                                                       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
      File "/Users/arg/.venv/lib/python3.12/site-packages/starlette/concurrency.py", line 37, in run_in_threadpool
        return await anyio.to_thread.run_sync(func)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
      File "/Users/arg/.venv/lib/python3.12/site-packages/anyio/to_thread.py", line 56, in run_sync
        return await get_async_backend().run_sync_in_worker_thread(
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
      File "/Users/arg/.venv/lib/python3.12/site-packages/anyio/_backends/_asyncio.py", line 2461, in run_sync_in_worker_thread
        return await future
               ^^^^^^^^^^^^
      File "/Users/arg/.venv/lib/python3.12/site-packages/anyio/_backends/_asyncio.py", line 962, in run
        result = context.run(func, *args)
                 ^^^^^^^^^^^^^^^^^^^^^^^^
      File "/var/folders/hw/jnc2s63n6g5d42c_9xl8lcwc0000gn/T/ipykernel_22043/456424634.py", line 18, in notebook
        franken.P(f"by Audrey M. Roy Greenfeld | {date:%a, %b %-d, %Y}", cls=TextFont.muted_sm),
                                                                             ^^^^^^^^
    NameError: name 'TextFont' is not defined
    ERROR:    Exception in ASGI application
    Traceback (most recent call last):
      File "/Users/arg/.venv/lib/python3.12/site-packages/uvicorn/protocols/http/httptools_impl.py", line 409, in run_asgi
        result = await app(  # type: ignore[func-returns-value]
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
      File "/Users/arg/.venv/lib/python3.12/site-packages/uvicorn/middleware/proxy_headers.py", line 60, in __call__
        return await self.app(scope, receive, send)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
      File "/Users/arg/.venv/lib/python3.12/site-packages/starlette/applications.py", line 112, in __call__
        await self.middleware_stack(scope, receive, send)
      File "/Users/arg/.venv/lib/python3.12/site-packages/starlette/middleware/errors.py", line 187, in __call__
        raise exc
      File "/Users/arg/.venv/lib/python3.12/site-packages/starlette/middleware/errors.py", line 165, in __call__
        await self.app(scope, receive, _send)
      File "/Users/arg/.venv/lib/python3.12/site-packages/starlette/middleware/cors.py", line 85, in __call__
        await self.app(scope, receive, send)
      File "/Users/arg/.venv/lib/python3.12/site-packages/starlette/middleware/sessions.py", line 85, in __call__
        await self.app(scope, receive, send_wrapper)
      File "/Users/arg/.venv/lib/python3.12/site-packages/starlette/middleware/exceptions.py", line 62, in __call__
        await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
      File "/Users/arg/.venv/lib/python3.12/site-packages/starlette/_exception_handler.py", line 53, in wrapped_app
        raise exc
      File "/Users/arg/.venv/lib/python3.12/site-packages/starlette/_exception_handler.py", line 42, in wrapped_app
        await app(scope, receive, sender)
      File "/Users/arg/.venv/lib/python3.12/site-packages/starlette/routing.py", line 715, in __call__
        await self.middleware_stack(scope, receive, send)
      File "/Users/arg/.venv/lib/python3.12/site-packages/starlette/routing.py", line 735, in app
        await route.handle(scope, receive, send)
      File "/Users/arg/.venv/lib/python3.12/site-packages/starlette/routing.py", line 288, in handle
        await self.app(scope, receive, send)
      File "/Users/arg/.venv/lib/python3.12/site-packages/starlette/routing.py", line 76, in app
        await wrap_app_handling_exceptions(app, request)(scope, receive, send)
      File "/Users/arg/.venv/lib/python3.12/site-packages/starlette/_exception_handler.py", line 53, in wrapped_app
        raise exc
      File "/Users/arg/.venv/lib/python3.12/site-packages/starlette/_exception_handler.py", line 42, in wrapped_app
        await app(scope, receive, sender)
      File "/Users/arg/.venv/lib/python3.12/site-packages/starlette/routing.py", line 73, in app
        response = await f(request)
                   ^^^^^^^^^^^^^^^^
      File "/Users/arg/git/fasthtml/fasthtml/core.py", line 568, in _f
        if not resp: resp = await _wrap_call(f, req, sig.parameters)
                            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
      File "/Users/arg/git/fasthtml/fasthtml/core.py", line 434, in _wrap_call
        return await _handle(f, wreq)
               ^^^^^^^^^^^^^^^^^^^^^^
      File "/Users/arg/git/fasthtml/fasthtml/core.py", line 225, in _handle
        return (await f(*args, **kwargs)) if is_async_callable(f) else await run_in_threadpool(f, *args, **kwargs)
                                                                       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
      File "/Users/arg/.venv/lib/python3.12/site-packages/starlette/concurrency.py", line 37, in run_in_threadpool
        return await anyio.to_thread.run_sync(func)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
      File "/Users/arg/.venv/lib/python3.12/site-packages/anyio/to_thread.py", line 56, in run_sync
        return await get_async_backend().run_sync_in_worker_thread(
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
      File "/Users/arg/.venv/lib/python3.12/site-packages/anyio/_backends/_asyncio.py", line 2461, in run_sync_in_worker_thread
        return await future
               ^^^^^^^^^^^^
      File "/Users/arg/.venv/lib/python3.12/site-packages/anyio/_backends/_asyncio.py", line 962, in run
        result = context.run(func, *args)
                 ^^^^^^^^^^^^^^^^^^^^^^^^
      File "/var/folders/hw/jnc2s63n6g5d42c_9xl8lcwc0000gn/T/ipykernel_22043/456424634.py", line 18, in notebook
        franken.P(f"by Audrey M. Roy Greenfeld | {date:%a, %b %-d, %Y}", cls=TextFont.muted_sm),
                                                                             ^^^^^^^^
    NameError: name 'TextFont' is not defined
    ERROR:    Exception in ASGI application
    Traceback (most recent call last):
      File "/Users/arg/.venv/lib/python3.12/site-packages/uvicorn/protocols/http/httptools_impl.py", line 409, in run_asgi
        result = await app(  # type: ignore[func-returns-value]
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
      File "/Users/arg/.venv/lib/python3.12/site-packages/uvicorn/middleware/proxy_headers.py", line 60, in __call__
        return await self.app(scope, receive, send)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
      File "/Users/arg/.venv/lib/python3.12/site-packages/starlette/applications.py", line 112, in __call__
        await self.middleware_stack(scope, receive, send)
      File "/Users/arg/.venv/lib/python3.12/site-packages/starlette/middleware/errors.py", line 187, in __call__
        raise exc
      File "/Users/arg/.venv/lib/python3.12/site-packages/starlette/middleware/errors.py", line 165, in __call__
        await self.app(scope, receive, _send)
      File "/Users/arg/.venv/lib/python3.12/site-packages/starlette/middleware/cors.py", line 85, in __call__
        await self.app(scope, receive, send)
      File "/Users/arg/.venv/lib/python3.12/site-packages/starlette/middleware/sessions.py", line 85, in __call__
        await self.app(scope, receive, send_wrapper)
      File "/Users/arg/.venv/lib/python3.12/site-packages/starlette/middleware/exceptions.py", line 62, in __call__
        await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
      File "/Users/arg/.venv/lib/python3.12/site-packages/starlette/_exception_handler.py", line 53, in wrapped_app
        raise exc
      File "/Users/arg/.venv/lib/python3.12/site-packages/starlette/_exception_handler.py", line 42, in wrapped_app
        await app(scope, receive, sender)
      File "/Users/arg/.venv/lib/python3.12/site-packages/starlette/routing.py", line 715, in __call__
        await self.middleware_stack(scope, receive, send)
      File "/Users/arg/.venv/lib/python3.12/site-packages/starlette/routing.py", line 735, in app
        await route.handle(scope, receive, send)
      File "/Users/arg/.venv/lib/python3.12/site-packages/starlette/routing.py", line 288, in handle
        await self.app(scope, receive, send)
      File "/Users/arg/.venv/lib/python3.12/site-packages/starlette/routing.py", line 76, in app
        await wrap_app_handling_exceptions(app, request)(scope, receive, send)
      File "/Users/arg/.venv/lib/python3.12/site-packages/starlette/_exception_handler.py", line 53, in wrapped_app
        raise exc
      File "/Users/arg/.venv/lib/python3.12/site-packages/starlette/_exception_handler.py", line 42, in wrapped_app
        await app(scope, receive, sender)
      File "/Users/arg/.venv/lib/python3.12/site-packages/starlette/routing.py", line 73, in app
        response = await f(request)
                   ^^^^^^^^^^^^^^^^
      File "/Users/arg/git/fasthtml/fasthtml/core.py", line 568, in _f
        if not resp: resp = await _wrap_call(f, req, sig.parameters)
                            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
      File "/Users/arg/git/fasthtml/fasthtml/core.py", line 434, in _wrap_call
        return await _handle(f, wreq)
               ^^^^^^^^^^^^^^^^^^^^^^
      File "/Users/arg/git/fasthtml/fasthtml/core.py", line 225, in _handle
        return (await f(*args, **kwargs)) if is_async_callable(f) else await run_in_threadpool(f, *args, **kwargs)
                                                                       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
      File "/Users/arg/.venv/lib/python3.12/site-packages/starlette/concurrency.py", line 37, in run_in_threadpool
        return await anyio.to_thread.run_sync(func)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
      File "/Users/arg/.venv/lib/python3.12/site-packages/anyio/to_thread.py", line 56, in run_sync
        return await get_async_backend().run_sync_in_worker_thread(
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
      File "/Users/arg/.venv/lib/python3.12/site-packages/anyio/_backends/_asyncio.py", line 2461, in run_sync_in_worker_thread
        return await future
               ^^^^^^^^^^^^
      File "/Users/arg/.venv/lib/python3.12/site-packages/anyio/_backends/_asyncio.py", line 962, in run
        result = context.run(func, *args)
                 ^^^^^^^^^^^^^^^^^^^^^^^^
      File "/var/folders/hw/jnc2s63n6g5d42c_9xl8lcwc0000gn/T/ipykernel_22043/3262860527.py", line 18, in notebook
        franken.P(f"by Audrey M. Roy Greenfeld | {date:%a, %b %-d, %Y}", cls=franken.TextFont.muted_sm),
                                                                             ^^^^^^^^^^^^^^^^
    AttributeError: module 'monsterui.franken' has no attribute 'TextFont'


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




    (#53) [Path('2025-01-29-This-Site-Is-Now-Powered-by-This-Notebook-Part-4.ipynb'),Path('2025-01-28-Time-Conversion-and-Discord-Timestamps-in-Python.ipynb'),Path('2025-01-27-This-Site-Is-Now-Powered-by-This-Notebook-Part-3.ipynb'),Path('2025-01-26-Improving-Pygments-Code-Block-Display.ipynb'),Path('2025-01-25-This-Site-Is-Now-Powered-by-This-Notebook-Part-2.ipynb'),Path('2025-01-24-Creating-In-Notebook-Images-for-Social-Media-With-PIL-Pillow.ipynb'),Path('2025-01-23-Troubleshooting-MonsterUI-on-This-Site.ipynb'),Path('2025-01-23-This-Site-Is-Now-Powered-by-This-Notebook.ipynb'),Path('2025-01-22-MonsterUI-Buttons-and-Links.ipynb'),Path('2025-01-22-Customizing-FastHTML-Headers-From-Notebook-Contents.ipynb'),Path('2025-01-21-SVG-Animation-in-FastHTML.ipynb'),Path('2025-01-20-Dark-and-Light-Mode-in-FastHTML.ipynb'),Path('2025-01-19-Genanki-and-fastcore.ipynb'),Path('2025-01-18-Alarm-Sounds-App.ipynb'),Path('2025-01-17-Alarm-Clock-Sounds.ipynb'),Path('2025-01-16-Cosine-Similarity-Breakdown-in-LaTeX.ipynb'),Path('2025-01-14-Constructing-SQLite-Tables-for-Notebooks-and-Search.ipynb'),Path('2025-01-13-SQLite-FTS5-Tokenizers-unicode61-and-ascii.ipynb'),Path('2025-01-12-A-Better-Notebook-Index-Page.ipynb'),Path('2025-01-11-NBClassic-Keyboard-Shortcuts-in-Command-and-Dual-Mode.ipynb')...]




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




    ('This Site Is Now Powered by This Notebook, Part 4',
     'Here I update audrey.feldroy.com with some of the latest MonsterUI text presets.')




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




    datetime.datetime(2025, 1, 29, 0, 0)




```python
date = get_date_from_iso8601_prefix(None)
date
```




    datetime.datetime(2025, 1, 29, 11, 16, 27, 931964)



## Notebook Cards


```python
#| export
def NBCard(title,desc,href,date):
    return A(
        franken.Card(
        franken.CardTitle(franken.H3(title)), 
        franken.P(f"{date:%a, %b %-d, %Y}", cls=franken.TextPresetsT.caption),
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
                franken.H1('audrey.feldroy.com'), franken.P("The experimental Jupyter notebooks of Audrey M. Roy Greenfeld. This website and all its notebooks are open-source at ", franken.A("github.com/audreyfeldroy/arg-blog-fasthtml", href="https://github.com/audreyfeldroy/arg-blog-fasthtml"), cls="mb-6"),
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
                Header(
                    franken.H1(title),
                    franken.P(f"by Audrey M. Roy Greenfeld | {date:%a, %b %-d, %Y}", cls=(franken.TextPresetsT.subheading, franken.PaddingT.lg, "m-b-10")),
                    franken.P(desc),
                    Hr()
                ),
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
nb_export nbs/2025-01-29-This-Site-Is-Now-Powered-by-This-Notebook-Part-4.ipynb --lib_path .
```
