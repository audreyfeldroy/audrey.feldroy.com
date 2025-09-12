# Creating an Accessible Inline Nav FastTag

I make a lightweight vanilla InlineNav FT with FastHTML, using the HTML nav element and as minimal styling as I can get away with.

## References

* [MDN nav examples](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/nav#examples)
* [HTML spec nav element - multipage](https://html.spec.whatwg.org/multipage/sections.html#the-nav-element)
* [Should I use `<ul>`s and `<li>`s inside my `<nav>`s?](https://stackoverflow.com/questions/5544885/should-i-use-uls-and-lis-inside-my-navs)

## Setup


```python
from fastcore.utils import *
from fasthtml.common import *
from fasthtml.jupyter import *
```

## Basic HTML Elements

This generates an HTML nav element:


```python
Nav()
```




```html
<nav></nav>

```



Within a nav element, screen readers handle lists best. 


```python
nv = Nav(
    Ul(
        Li(A("audrey.feldroy.com", href="https://audrey.feldroy.com/")),
        Li(A("Source", href="https://github.com/audreyfeldroy/audrey.feldroy.com"))
    ))
nv
```




```html
<nav>
  <ul>
    <li>
<a href="https://audrey.feldroy.com/">audrey.feldroy.com</a>    </li>
    <li>
<a href="https://github.com/audreyfeldroy/audrey.feldroy.com">Source</a>    </li>
  </ul>
</nav>

```




```python
show(nv)
```


<nav>
  <ul>
    <li>
<a href="https://audrey.feldroy.com/">audrey.feldroy.com</a>    </li>
    <li>
<a href="https://github.com/audreyfeldroy/audrey.feldroy.com">Source</a>    </li>
  </ul>
</nav>
<script>if (window.htmx) htmx.process(document.body)</script>


## Custom FastTags to Add Minimal CSS Styles

I often see Jeremy and Isaac simply overriding the existing FTs. I tried that at first, but it didn't feel right to me. Maybe in the future I'll switch to that pattern. Here I'll name them differently. 

Mainly I didn't want to have `style="display:inline"` twice.


```python
def InLi(*c): return Li(*c, style="display:inline")
```

Then it felt natural to do one for the parent Ul, but not really necessary. Rather, it felt awkward not to give it a partner element.


```python
def InUl(*c): return Ul(*c, style="list-style:none")
```

But now it feels awkward to not have an inline version of the main nav element. Hmm.


```python
nv = Nav(
    InUl(
        InLi(A("audrey.feldroy.com", href="https://audrey.feldroy.com/")),
        InLi(A("Source", href="https://github.com/audreyfeldroy/audrey.feldroy.com"))
    )
)
show(nv)
```


<nav>
  <ul style="list-style:none">
    <li style="display:inline">
<a href="https://audrey.feldroy.com/">audrey.feldroy.com</a>    </li>
    <li style="display:inline">
<a href="https://github.com/audreyfeldroy/audrey.feldroy.com">Source</a>    </li>
  </ul>
</nav>
<script>if (window.htmx) htmx.process(document.body)</script>


I guess I could do it this way:


```python
nv = Nav(
    Ul(
        InLi(A("audrey.feldroy.com", href="https://audrey.feldroy.com/")),
        InLi(A("Source", href="https://github.com/audreyfeldroy/audrey.feldroy.com")),
        style="list-style:none"
    )
)
show(nv)
```


<nav>
  <ul style="list-style:none">
    <li style="display:inline;margin-right:1em">
<a href="https://audrey.feldroy.com/">audrey.feldroy.com</a>    </li>
    <li style="display:inline;margin-right:1em">
<a href="https://github.com/audreyfeldroy/audrey.feldroy.com">Source</a>    </li>
  </ul>
</nav>
<script>if (window.htmx) htmx.process(document.body)</script>


Or maybe this way:


```python
def InlineNav():
    return Ul(
        InLi(A("audrey.feldroy.com", href="https://audrey.feldroy.com/")),
        InLi(A("Source", href="https://github.com/audreyfeldroy/audrey.feldroy.com")),
        style="list-style:none"
    )
nv = InlineNav()
show(nv)
```


<ul style="list-style:none">
  <li style="display:inline;margin-right:1em">
<a href="https://audrey.feldroy.com/">audrey.feldroy.com</a>  </li>
  <li style="display:inline;margin-right:1em">
<a href="https://github.com/audreyfeldroy/audrey.feldroy.com">Source</a>  </li>
</ul>
<script>if (window.htmx) htmx.process(document.body)</script>


Let's refactor to pull out the parts that matter:


```python
navlinks = L(
    ("audrey.feldroy.com", "https://audrey.feldroy.com/"),
    ("GitHub repo for this site", "https://github.com/audreyfeldroy/audrey.feldroy.com")
)
```


```python
def InLi(linktuple):
    txt, href = linktuple
    return Li(A(txt, href=href), style="display:inline")
```


```python
navlinks.map(InLi)
```




    (#2) [li((a(('audrey.feldroy.com',),{'href': 'https://audrey.feldroy.com/'}),),{'style': 'display:inline'}),li((a(('GitHub repo for this site',),{'href': 'https://github.com/audreyfeldroy/audrey.feldroy.com'}),),{'style': 'display:inline'})]




```python
def InlineNav(navlinks):
    return Nav(Ul(
        *navlinks.map(InLi),
        style="list-style:none"
    ))
nv = InlineNav(navlinks)
show(nv)
```


<nav>
  <ul style="list-style:none">
    <li style="display:inline">
<a href="https://audrey.feldroy.com/">audrey.feldroy.com</a>    </li>
    <li style="display:inline">
<a href="https://github.com/audreyfeldroy/audrey.feldroy.com">GitHub repo for this site</a>    </li>
  </ul>
</nav>
<script>if (window.htmx) htmx.process(document.body)</script>


## Improve Accessibility

To follow accessibility best practices, including making this useful to screen readers:

1. Descriptive `aria-label` on `Nav`
2. Visual space between inline list items
3. `role="navigation"` (redundant with `<nav>` but helps old assistive tech)


```python
def InLi(linktuple):
    txt, href = linktuple
    return Li(A(txt, href=href), style="display:inline;margin-right:1em")
```


```python
def InlineNav(navlinks):
    return Nav(
        Ul(
            *navlinks.map(InLi),
            style="list-style:none;padding-left:0"
        ),
        aria_label="Main navigation",
        role="navigation"
    )
nv = InlineNav(navlinks)
show(nv)
```


<nav aria-label="Main navigation" role="navigation">
  <ul style="list-style:none;padding-left:0">
    <li style="display:inline;margin-right:1em">
<a href="https://audrey.feldroy.com/">audrey.feldroy.com</a>    </li>
    <li style="display:inline;margin-right:1em">
<a href="https://github.com/audreyfeldroy/audrey.feldroy.com">GitHub repo for this site</a>    </li>
  </ul>
</nav>
<script>if (window.htmx) htmx.process(document.body)</script>

