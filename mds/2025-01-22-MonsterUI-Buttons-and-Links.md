# MonsterUI Buttons and Links

Iterating through the ButtonT enum to show all MonsterUI button types visually.


```python
from fastcore.utils import *
from fasthtml.common import *
from monsterui.all import *
```


```python
tags = ["MonsterUI"]
```

## Setup


```python
Button()
```




```html
<button type="submit" class="uk-button uk-button-default"></button>
```




```python
show(Button("Click me"))
```


<button type="submit" class="uk-button uk-button-default">Click me</button>



```python
show(A("My link", href="example.com", cls=AT.muted))
```


<a href="example.com" class="uk-link-muted">My link</a>



```python
show(NavBar(title="MySite", nav_links=(A("Link 1"), A("Link 2"))))
```


<div>
  <div class="uk-container mt-5 uk-container-xlarge">
    <div class="md:flex md:relative">
      <div class="uk-navbar-left ">
        <h1 class="uk-h1 ">MySite</h1>
<uk-icon icon="menu" height="30" width="30" hx-on-click="htmx.find('#_S_0fkn7ATy2jXQuJL72PNg').classList.toggle('hidden')" class="md:hidden"></uk-icon>      </div>
      <div id="_S_0fkn7ATy2jXQuJL72PNg" class="uk-navbar-right hidden md:flex md:justify-between">
        <nav class="uk-navbar-nav w-full flex-col md:flex-row">
<a href="#">Link 1</a><a href="#">Link 2</a>        </nav>
      </div>
    </div>
  </div>
</div>




```python
show(Button("Hey",cls=ButtonT.primary))
```


<button type="submit" class="uk-button uk-button-primary">Hey</button>



```python
ButtonT
```




    <enum 'ButtonT'>




```python
[t.name for t in ButtonT]
```




    ['default', 'primary', 'secondary', 'danger', 'text', 'link', 'ghost']



**AI Prompt**

Is there a convenience function in enum to list all these?

**AI Response**

Yes! The `Enum` class in Python has a built-in method called `__members__`. You can use it like this:

```python
ButtonT.__members__
```

Would you like me to explain more about what this returns and how it differs from the list comprehension approach you used?


```python
ButtonT.__members__
```




    mappingproxy({'default': <ButtonT.default: 'uk-button-default'>,
                  'primary': <ButtonT.primary: 'uk-button-primary'>,
                  'secondary': <ButtonT.secondary: 'uk-button-secondary'>,
                  'danger': <ButtonT.danger: 'uk-button-danger'>,
                  'text': <ButtonT.text: 'uk-button-text'>,
                  'link': <ButtonT.link: 'uk-button-link'>,
                  'ghost': <ButtonT.ghost: 'uk-button-ghost'>})




```python
L(ButtonT.__members__)
```




    (#7) ['default','primary','secondary','danger','text','link','ghost']




```python
def _Button(t): return Button(f"{t} button",cls=t)
btns = L(ButtonT.__members__).map(_Button)
btns
```




    (#7) [button(('default button',),{'type': 'submit', 'class': 'uk-button default'}),button(('primary button',),{'type': 'submit', 'class': 'uk-button primary'}),button(('secondary button',),{'type': 'submit', 'class': 'uk-button secondary'}),button(('danger button',),{'type': 'submit', 'class': 'uk-button danger'}),button(('text button',),{'type': 'submit', 'class': 'uk-button text'}),button(('link button',),{'type': 'submit', 'class': 'uk-button link'}),button(('ghost button',),{'type': 'submit', 'class': 'uk-button ghost'})]




```python
to_xml(Div(*btns))
```




    '<div>\n<button type="submit" class="uk-button default">default button</button><button type="submit" class="uk-button primary">primary button</button><button type="submit" class="uk-button secondary">secondary button</button><button type="submit" class="uk-button danger">danger button</button><button type="submit" class="uk-button text">text button</button><button type="submit" class="uk-button link">link button</button><button type="submit" class="uk-button ghost">ghost button</button></div>\n'




```python
show(to_xml(Div(*btns)))
```


<div>
<button type="submit" class="uk-button default">default button</button><button type="submit" class="uk-button primary">primary button</button><button type="submit" class="uk-button secondary">secondary button</button><button type="submit" class="uk-button danger">danger button</button><button type="submit" class="uk-button text">text button</button><button type="submit" class="uk-button link">link button</button><button type="submit" class="uk-button ghost">ghost button</button></div>



**AI Prompt**

Why don't the buttons look right?

**AI Response**

Looking at the button classes in the HTML output, I notice the classes are missing the `uk-button-` prefix that we saw in the `ButtonT` enum values. Instead, they just have `uk-button default`, `uk-button primary`, etc.

Let's check what's happening by looking at one button directly:

```python
show(Button("test", cls=ButtonT.primary))
```

This should help us see if the issue is in how we're passing the enum values to the Button constructor.

**AI Prompt**

def _Button(t): return Button(f"{t} button",cls=ButtonT.t)
btns = L(ButtonT.__members__).map(_Button)
btns

**AI Response**

Ah, I see the issue in your code. `ButtonT.t` isn't correct - you're trying to access a property `t` on `ButtonT`, but `t` is actually the variable in your function containing the member name.

Instead, you should use `ButtonT[t]` or `getattr(ButtonT, t)` to look up the enum member by name. Would you like to try fixing this?


```python
def _Button(t): return Button(f"{t} button",cls=ButtonT[t])
btns = L(ButtonT.__members__).map(_Button)
show(Div(*btns))
```


<div>
<button type="submit" class="uk-button uk-button-default">default button</button><button type="submit" class="uk-button uk-button-primary">primary button</button><button type="submit" class="uk-button uk-button-secondary">secondary button</button><button type="submit" class="uk-button uk-button-danger">danger button</button><button type="submit" class="uk-button uk-button-text">text button</button><button type="submit" class="uk-button uk-button-link">link button</button><button type="submit" class="uk-button uk-button-ghost">ghost button</button></div>



## Improvements 

This part is from SolveIt office hours with Isaac Flath.

**AI Prompt**

Is there any other way to get `ButtonT.__members__` in enum or otherwise?

**AI Response**

Yes! There are a few other ways to get enum members:

1. Using `list(ButtonT)` - this gives you the values
2. Using `ButtonT._member_names_` - this gives you just the names
3. Using `ButtonT._member_map_` - similar to `__members__` but returns a regular dict

Would you like to try any of these to see how they differ?


```python
list(ButtonT)[0].value
```




    'uk-button-default'




```python
Div(*[Button(v,cls=v) for v in list(ButtonT)])
```




```html
<div>
<button type="submit" class="uk-button uk-button-default">uk-button-default</button><button type="submit" class="uk-button uk-button-primary">uk-button-primary</button><button type="submit" class="uk-button uk-button-secondary">uk-button-secondary</button><button type="submit" class="uk-button uk-button-danger">uk-button-danger</button><button type="submit" class="uk-button uk-button-text">uk-button-text</button><button type="submit" class="uk-button uk-button-link">uk-button-link</button><button type="submit" class="uk-button uk-button-ghost">uk-button-ghost</button></div>

```




```python
show(Div(*[Button(v,cls=v) for v in list(ButtonT)]))
```


<div>
<button type="submit" class="uk-button uk-button-default">uk-button-default</button><button type="submit" class="uk-button uk-button-primary">uk-button-primary</button><button type="submit" class="uk-button uk-button-secondary">uk-button-secondary</button><button type="submit" class="uk-button uk-button-danger">uk-button-danger</button><button type="submit" class="uk-button uk-button-text">uk-button-text</button><button type="submit" class="uk-button uk-button-link">uk-button-link</button><button type="submit" class="uk-button uk-button-ghost">uk-button-ghost</button></div>




```python
show(DivLAligned(*[Button(v,cls=v) for v in list(ButtonT)]))
```


<div class="uk-flex uk-flex-left uk-flex-middle space-x-4">
<button type="submit" class="uk-button uk-button-default">uk-button-default</button><button type="submit" class="uk-button uk-button-primary">uk-button-primary</button><button type="submit" class="uk-button uk-button-secondary">uk-button-secondary</button><button type="submit" class="uk-button uk-button-danger">uk-button-danger</button><button type="submit" class="uk-button uk-button-text">uk-button-text</button><button type="submit" class="uk-button uk-button-link">uk-button-link</button><button type="submit" class="uk-button uk-button-ghost">uk-button-ghost</button></div>




```python
show(Grid(*[Button(v,cls=v) for v in list(ButtonT)]))
```


<div class="grid grid-cols-1 sm:grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
<button type="submit" class="uk-button uk-button-default">uk-button-default</button><button type="submit" class="uk-button uk-button-primary">uk-button-primary</button><button type="submit" class="uk-button uk-button-secondary">uk-button-secondary</button><button type="submit" class="uk-button uk-button-danger">uk-button-danger</button><button type="submit" class="uk-button uk-button-text">uk-button-text</button><button type="submit" class="uk-button uk-button-link">uk-button-link</button><button type="submit" class="uk-button uk-button-ghost">uk-button-ghost</button></div>


