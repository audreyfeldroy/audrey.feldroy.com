# How I Fixed CSS Scope Leakage in Pygments Syntax Highlighting

This notebook shows how to:

* Get and use Pygments styles programmatically
* Extract and display the source code from Python functions
* Apply different Pygments syntax highlighting to different cells of the same notebook with proper CSS scoping
* Use Pygments-highlighted code in a FastHTML FastTag


```python
from execnb.nbio import *
from fastcore.all import *
from fasthtml.common import *
from inspect import getsource
from IPython.display import display, HTML
import pygments
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter
```

## Pygments Styles

I was getting all Pygments styles the hard way in [my previous notebooks](https://github.com/audreyfeldroy/arg-blog-fasthtml/tree/main/nbs). There's a method for getting the highlight style names via Python:


```python
styles = L(pygments.styles.get_all_styles())
print(styles)
```

## Inspect and `getsource`

Let's grab a function to highlight. How about `read_nb` from execnb:


```python
rn = getsource(read_nb)
rn
```

We have to print it to see it nicely:


```python
print(rn)
```

## Pygments `highlight`

As in previous posts, we call `highlight` to highlight a Python code block like this:


```python
h = highlight(rn, PythonLexer(), HtmlFormatter(style='tango'))
h
```

Then to display that in a notebook:


```python
HTML(h)
```

## Highlighting Code In-Notebook

Putting `highlight` and `HTML` into a function together, building up from above:


```python
def show(c): return HTML(highlight(c, PythonLexer(), HtmlFormatter(style='tango')))
```


```python
show(rn)
```

## Function Getting Its Own Source

To get some source code to highlight without having to read a notebook:


```python
def get_myself(): return getsource(get_myself)
```


```python
get_myself()
```

## Function Highlighting Itself

Putting together `highlight`, `HTML`, and `getsource`:


```python
def show(c=None): 
    if not c: c = getsource(show)
    return HTML(highlight(c, PythonLexer(), HtmlFormatter(style='tango')))
```


```python
show()
```

## Adding a `style` Arg

I wanted to show my code with a particular Pygments style:


```python
def show(c=None, style='tango'): 
    if not c: c = getsource(show)
    return HTML(highlight(c, PythonLexer(), HtmlFormatter(style=style)))
```


```python
show(style='zenburn')
```

Something's not right here. That showed no colors.

## Understanding Pygments Style Defs

In Pygments, style defs are CSS style definitions:


```python
sd = HtmlFormatter(style='zenburn').get_style_defs()
sd[:200]
```


```python
s = L(sd.splitlines())
s
```


```python
s[0]
```


```python
s[6]
```


```python
s[10]
```

## Looking at Hex Colors With FastTags

In style `zenburn`, comments are colored in `#7f9f7f`. Let's see what this looks like with a `Div` FastTag:


```python
cdiv = Div('#7f9f7f', style="background-color:#7f9f7f;")
cdiv
```


```python
HTML(to_xml(cdiv))
```


```python
def show_color(c): return HTML(to_xml(Div(c, style=f"background-color:{c};")))
```

Keywords in `zenburn` are colored with `#efdcbc`:


```python
show_color("#efdcbc")
```

## Pygments Styles in FastHTML FastTags

Putting `zenburn` comment and keyword styles in a `Style` FastTag:


```python
Style(s[6], s[10])
```

## Pygments Highlighting in FastTags

Recall Pygments `highlight` from earlier generates a `div` containing `pre` full of `span` tags: 


```python
h = highlight(rn, PythonLexer(), HtmlFormatter(style='tango'))
print(h)
```

This is a nice string of HTML to use with FastTags. I use `NotStr` to make it work well with a `Div` FastTag:


```python
Div(NotStr(h), id="container")
```

Adding style:


```python
styled_container = Div(Style(s[6], s[10]), NotStr(h), id="container")
styled_container
```

To display it in-notebook here:


```python
HTML(to_xml(styled_container))
```

## Pygments Background Color

The Pygments [`get_style_defs` docs](https://pygments.org/docs/api/#pygments.formatter.Formatter.get_style_defs) say you can specify a CSS selector to prefix styles with:


```python
sd = HtmlFormatter(style='zenburn').get_style_defs('.highlight')
sd[:500]
```

I see all the zenburn style defs with background colors are early on:


```python
Style(sd[:600])
```


```python
show_color("#484848")
```


```python
show_color("#353535")
```


```python
styled_container = Div(Style(sd), NotStr(h), id="container")
HTML(to_xml(styled_container))
```

## Combining Everything Into `show`

Let's combine everything we've learned into a function:


```python
def show(c=None, style='monokai'): 
    if not c: c = getsource(show)
    fm = HtmlFormatter(style=style)
    h = highlight(c, PythonLexer(), fm)
    sd = fm.get_style_defs('.highlight')
    styled_container = Div(Style(sd), NotStr(h), id="container")
    return HTML(to_xml(styled_container))
```


```python
show(style='monokai')
```


```python
show(style='lightbulb')
```

## Fixing CSS Scope Leakage

Let's see if we can customize the `highlight` class


```python
fm = HtmlFormatter(style='monokai')
h = highlight("print('Hi')", PythonLexer(), fm)
h
```


```python
def show(c=None, style='monokai'): 
    if not c: c = getsource(show)
    fm = HtmlFormatter(style=style)
    h = highlight(c, PythonLexer(), fm)
    sd = fm.get_style_defs(f'#{style}')
    styled_container = Div(Style(sd), NotStr(h), id=style)
    return HTML(to_xml(styled_container))
```


```python
show(style='monokai')
```


```python
show(style='lightbulb')
```

The above 2 appeared to work correctly, but this didn't, so something's wrong:


```python
show(style='paraiso-light')
```


```python
print(HtmlFormatter(style='paraiso-light').get_style_defs('#paraiso-light')[:1000])
```

The background color is supposed to be:


```python
show_color("#a39e9b")
```

I think `get_style_defs('#paraiso-light')` where that ID is on the parent div is too hacky here. I feel like `<div class="highlight">` itself should get the ID.


```python
print(HtmlFormatter(style='paraiso-light').get_background_style_defs('#paraiso-light')[:1000])
```


```python
c = 'print("Hi")'
fm = HtmlFormatter(style='paraiso-light', cssclass='audrey')
h = highlight(c, PythonLexer(), fm)
h
```


```python
def show(c=None, style='monokai'): 
    if not c: c = getsource(show)
    fm = HtmlFormatter(style=style, cssclass=style)
    h = highlight(c, PythonLexer(), fm)
    sd = fm.get_style_defs(f".{style}")
    styled_container = Div(Style(sd), NotStr(h), id=style)
    return HTML(to_xml(styled_container))
```


```python
show(style='paraiso-light')
```


```python
show(c="print('Hey')", style="dracula")
```


```python
show(style="dracula")
```


```python
show(style="gruvbox-dark")
```


```python
show(style="solarized-dark")
```

Success! The cells above are syntax-highlighted without their CSS interfering with each other.

## Summary

I've created a function for displaying Pygments syntax-highlighted code in Jupyter notebooks with properly-scoped CSS. To do this, I discovered I could:

1. Use Pygments' `HtmlFormatter`'s `cssclass` parameter to change the name of the outer `highlight` div to the Pygments style name.
2. Use `get_style_defs` to scope style definitions to that name, to prevent CSS conflicts
3. Combine it into a tiny `show` function for use in future notebooks


```python
def show(c=None, style='monokai'): 
    if not c: c = getsource(show)
    fm = HtmlFormatter(style=style, cssclass=style)
    h = highlight(c, PythonLexer(), fm)
    sd = fm.get_style_defs(f".{style}")
    styled_container = Div(Style(sd), NotStr(h), id=style)
    return HTML(to_xml(styled_container))
```

You can use this to show code blocks in Jupyter notebooks, allowing different Pygments syntax highlighting themes in the same notebook. All without CSS leaking between Pygments styles.
