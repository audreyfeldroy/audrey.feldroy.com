# Showing Components in Notebooks

## Understand the Problem

I currently have trouble following the SolveIt process while building FastHTML apps. I am able to build up an app's pieces as strings of HTML and think about if the strings are correct, but showing those pieces as rendered components in a notebook always trips me up.

## Devise Plan

* Use this notebook to create a sample component
* Display it in this notebook
    * Look at other projects to see ways of rendering components in-notebook
    * Play with different ways and see what works best for me

## Carry Out Plan

### Setup


```python
from fasthtml.common import *
from fasthtml.jupyter import *
from IPython.display import display, HTML, IFrame
```


```python
app, rt = fast_app()
```


```python
server = JupyUvi(app)
```


```python
if 'server' in globals(): server.stop()
```

### Sample Component: P With a Little Style


```python
def RectP(c):
    return P(c, style="border: 1px gray solid")
```


```python
RectP("Hi")
```

### Studying In-Notebook Component Rendering

Starting with the canonical docs:

* https://docs.fastht.ml/tutorials/jupyter_and_fasthtml.html
* https://docs.fastht.ml/api/jupyter.html

### Using render_ft

> After importing fasthtml.jupyter and calling render_ft(), FT components render directly in the notebook.


```python
# render_ft()
```


```python
RectP("Hi")
```

That worked! Though how do I view the string version of it now?


```python
to_xml(RectP("Hello"))
```

That worked too!

### Rendering Without render_ft

It feels a bit weird to change what `RectP` does. Ideally I can render the component only when I want to, not always. For now I am commenting out `render_ft` above, so that I can restart this notebook's kernel and continue without it.

Let's explore what `render_ft` does.


```python
def render_ft():
    @patch
    def _repr_markdown_(self:FT): return to_xml(Div(self, Script('if (window.htmx) htmx.process(document.body)')))
```

I asked AI: Wait so it patches a FT component's _repr_markdown_ method?

Yes - it patches the `_repr_markdown_` method of the `FT` class, which is what Jupyter uses to determine how to display objects. The patch wraps the component in a `Div` with an HTMX processing script, and converts it to XML. This is why components automatically render as HTML after calling `render_ft()`.

That's also why `to_xml()` still works to see the string version - it's a different method that isn't affected by the patch.

`htmx.process()` tells HTMX to scan the given element (in this case `document.body`) and initialize any HTMX attributes it finds. This is necessary when HTML is dynamically added to the page, as HTMX only automatically processes elements when the page first loads. Without this call, any HTMX attributes (like `hx-get`, `hx-post`, etc.) in dynamically rendered components wouldn't be activated.

Since Jupyter dynamically inserts our component's HTML into the notebook after the page has loaded, we need `htmx.process()` to ensure any HTMX functionality in the component gets initialized. Even if our current simple `RectP` component doesn't use HTMX features, the script is included by default since FastHTML components often do use HTMX attributes and we want them to work properly when rendered in the notebook.


```python
def show_ft(c):
    html = to_xml(Div(c, Script('if (window.htmx) htmx.process(document.body)')))
    display(HTML(html))
```


```python
show_ft(RectP("Hi"))
```

### IPython Display and HTML

Let's take a step back to understand IPython display, not worrying about JS for now.


```python
display(HTML('<p style="border: 1px red solid">Hi</p>'))
```


```python
RectP("Uma")
```


```python
uma = RectP("Uma")
uma
```


```python
display(HTML(to_xml(uma)))
```


```python
display(HTML(to_xml(RectP("Uma"))))
```

### Defining a `show` Function


```python
def show(c): return display(HTML(to_xml(c)))
```


```python
show(RectP("Uma is a girl who loves crafts, science, and magic. "*20))
```

### Complex `show` Output: MonsterUI


```python
from monsterui.all import Card
```


```python
c = Card("I'm a card. "*20, header="Prepare yourself, it's coming", footer="Thank you for your attention")
c
```


```python
show(c)
```

I guess it would be nice to grab the card CSS without all of MonsterUI here, and put it into `Style()`. I don't think MonsterUI has that feature, but Pygments does. I'll try that.

### Complex `show` Output: Pygments


```python
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter
```


```python
fm = HtmlFormatter(style='paraiso-light')
```


```python
c = highlight('print("Hey")', lexer=PythonLexer(), formatter=fm)
c
```


```python
NotStr(c)
```


```python
Div(c)
```


```python
Div(NotStr(c))
```

Working examples directly below


```python
display(HTML(to_xml(Div(NotStr(c),Style(fm.get_style_defs())))))
```

Note: the following cell only works when the previous cell works:


```python
display(HTML(c))
```


```python
def show_highlight(c): return display(HTML(to_xml(Div(NotStr(c),Style(fm.get_style_defs())))))
```


```python
c = highlight('styles = L(pygments.styles.STYLES.items()).itemgot(1).itemgot(1)', lexer=PythonLexer(), formatter=fm)
show_highlight(c)
```


```python
def show_highlight(c): return display(HTML(to_xml(Div(NotStr(c),Style(fm.get_style_defs())))))
```

To be continued with scoped CSS...

### Complex `show` Output: My Own


```python
def RectP(c):
    return P(c, style="border:1px lightgray solid;padding:6px;margin:0;")
```


```python
show(RectP("Hi, I'm Audrey. Danny and Uma are sleeping. "*20))
```

To be continued...


```python

```
