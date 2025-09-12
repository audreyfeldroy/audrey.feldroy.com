# Understanding FastHTML xtend

My early exploration of the xtend notebook in FastHTML.

Current FastHTML Pico Card: https://github.com/AnswerDotAI/fasthtml/blob/main/fasthtml/xtend.py#L76


```python
from fasthtml.common import *
```


```python
Card
```




    <function fasthtml.xtend.Card(*c, header=None, footer=None, target_id=None, id=None, cls=None, title=None, style=None, accesskey=None, contenteditable=None, dir=None, draggable=None, enterkeyhint=None, hidden=None, inert=None, inputmode=None, lang=None, popover=None, spellcheck=None, tabindex=None, translate=None, hx_get=None, hx_post=None, hx_put=None, hx_delete=None, hx_patch=None, hx_trigger=None, hx_target=None, hx_swap=None, hx_include=None, hx_select=None, hx_indicator=None, hx_push_url=None, hx_confirm=None, hx_disable=None, hx_replace_url=None, hx_on=None, **kwargs) -> fastcore.xml.FT>



What interesting things can we find out about the Card function?


```python
help(Card)
```

    Help on function Card in module fasthtml.xtend:
    
    Card(*c, header=None, footer=None, target_id=None, id=None, cls=None, title=None, style=None, accesskey=None, contenteditable=None, dir=None, draggable=None, enterkeyhint=None, hidden=None, inert=None, inputmode=None, lang=None, popover=None, spellcheck=None, tabindex=None, translate=None, hx_get=None, hx_post=None, hx_put=None, hx_delete=None, hx_patch=None, hx_trigger=None, hx_target=None, hx_swap=None, hx_include=None, hx_select=None, hx_indicator=None, hx_push_url=None, hx_confirm=None, hx_disable=None, hx_replace_url=None, hx_on=None, **kwargs) -> fastcore.xml.FT
        A PicoCSS Card, implemented as an Article with optional Header and Footer
    



```python
dir(Card)
```




    ['__annotations__',
     '__builtins__',
     '__call__',
     '__class__',
     '__closure__',
     '__code__',
     '__defaults__',
     '__delattr__',
     '__dict__',
     '__dir__',
     '__doc__',
     '__eq__',
     '__format__',
     '__ge__',
     '__get__',
     '__getattribute__',
     '__getstate__',
     '__globals__',
     '__gt__',
     '__hash__',
     '__init__',
     '__init_subclass__',
     '__kwdefaults__',
     '__le__',
     '__lt__',
     '__module__',
     '__name__',
     '__ne__',
     '__new__',
     '__qualname__',
     '__reduce__',
     '__reduce_ex__',
     '__repr__',
     '__setattr__',
     '__signature__',
     '__sizeof__',
     '__str__',
     '__subclasshook__',
     '__type_params__']




```python
import inspect

print(inspect.getsource(Card))
```

    @delegates(ft_hx, keep=True)
    def Card(*c, header=None, footer=None, **kwargs)->FT:
        "A PicoCSS Card, implemented as an Article with optional Header and Footer"
        if header: c = (Header(header),) + c
        if footer: c += (Footer(footer),)
        return Article(*c, **kwargs)
    


@delegates(xt_hx, keep=True) means it can accept and pass along any arguments that the xt_hx function accepts.

It's defined in https://github.com/fastai/fastcore/blob/005ffd986df737cfc46c7cb1eadec5d214d08da7/fastcore/meta.py#L109

Not sure what xt_hx is, probably a function that does something with the XML tree and HTMX attributes.

I'll run 02_xtend.ipynb to try and learn more.


```python
from functools import partial
from fasthtml.components import ft_hx
my_a = partial(ft_hx, "A")
my_a
```




    functools.partial(<function ft_hx>, 'A')




```python
my_a()
```




```xml
<a></a>

```




```python
my_a('Hi')
```




```xml
<a>Hi</a>

```




```python
my_a("Hi", cls='linky')
```




```xml
<a class="linky">Hi</a>

```




```python
my_b = partial(ft_hx, "B")
my_b("Hello")
```




```xml
<b>Hello</b>

```




```python
C = partial(ft_hx, "C")
C("Hee hee")
```




```xml
<c>Hee hee</c>

```




```python
Uma = partial(ft_hx, "Uma")
Uma("Hi mommy", cls='cute', mood='happy', id="UmaTheKid")
```




```xml
<uma mood="happy" id="UmaTheKid" class="cute">Hi mommy</uma>

```




```python
Mommy = partial(ft_hx, "Mommy")
Mommy("Hi Uma", cls='mom', hx_trigger="mouseenter", hx_get="/inbox")
```




```xml
<mommy hx-trigger="mouseenter" hx-get="/inbox" class="mom">Hi Uma</mommy>

```




```python
Daddy = partial(ft_hx, "Daddy")
Daddy("Hi fam", cls="dad", hx_target="#UmaTheKid")
```




```xml
<daddy hx-target="#UmaTheKid" class="dad">Hi fam</daddy>

```




```python
from fastcore.meta import delegates
```


```python
@delegates(ft_hx, keep=True)
def Mom(*c, title, description, **kwargs) -> FT:
    print(f"Type of c: {type(c)}")
    if title: c = H1(title, 1) + list(c)
    if description: c += P(description)
    return Mommy(*c, **kwargs)
```


```python
Mom("Hi Uma", title="Mother", description="Director of Motherhood", cls="ma", hx_trigger="mouseenter", hx_get="/inbox")
```

    Type of c: <class 'tuple'>





```xml
<mommy hx-trigger="mouseenter" hx-get="/inbox" class="ma">
h1
Mother

1
{}
Hi Uma
p
Director of Motherhood
{}
</mommy>

```




```python
type(H1("Hi"))
```




    fastcore.xml.FT




```python
@delegates(ft_hx, keep=True)
def Card(*c, header=None, footer=None, **kwargs) -> FT:
    "A PicoCSS Card, implemented as an Article with optional Header and Footer"
    if header:
        c = (Header(header),) + c
    if footer:
        c += (Footer(footer),)
    return Article(*c, **kwargs)
```


```python
Card("Hi Uma", header="Mother", footer="Director of Motherhood", cls="ma", hx_trigger="mouseenter", hx_get="/inbox")
```




```xml
<article hx-trigger="mouseenter" hx-get="/inbox" class="ma">
  <header>Mother</header>
Hi Uma
  <footer>Director of Motherhood</footer>
</article>

```


