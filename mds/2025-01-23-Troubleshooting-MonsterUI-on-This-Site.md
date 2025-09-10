# Troubleshooting MonsterUI on This Site

My first MonsterUI notebook wasn't rendering correctly. I started to debug it in this notebook, but ended up just using this as a test notebook for the next one.


```python
from fasthtml.common import *
from monsterui.all import *
```

## Understand the Problem

[MonsterUI Buttons and Links](https://audrey.feldroy.com/nbs/2025-01-22-MonsterUI-Buttons-and-Links) is the notebook with the problem.

Let's start with a subset of the problem: the H1 text "MonsterUI Buttons and Links" is showing up as normal text.


```python
H1("Hi")
```




```html
<h1 class="uk-h1 ">Hi</h1>

```




```python
show(H1("Hi"))
```


<h1 class="uk-h1 ">Hi</h1>




```python
A("My Blog", href="https://audrey.feldroy.com")
```




```html
<a href="https://audrey.feldroy.com">My Blog</a>
```



## Solution in Next Notebook

I ended up rewriting the MonsterUI rendering part of main.py from scratch in https://audrey.feldroy.com/nbs/2025-01-23-This-Site-Is-Now-Powered-by-This-Blog-Post

Sometimes it's just easier to rewrite than debug.

## Update 2025-01-30

I'm using this notebook again to troubleshoot MonsterUI as I update my site.


```python
c = Card("This is a plain Card")
c
```




```html
<div class="uk-card ">
  <div class="uk-card-body space-y-6">This is a plain Card</div>
</div>

```




```python
show(c)
```


<div class="uk-card ">
  <div class="uk-card-body space-y-6">This is a plain Card</div>
</div>




```python
c2 = Card("This is a Card with added Tailwind background styles to make it greeen", cls="bg-green-500 dark:bg-green-400")
```


```python
show(c2)
```


<div class="uk-card bg-green-500 dark:bg-green-400">
  <div class="uk-card-body space-y-6">This is a Card with added Tailwind background styles to make it greeen</div>
</div>




```python

```
