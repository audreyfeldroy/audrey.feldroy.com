# Transforming Notebook Names to Cards

I have Jupyter notebooks in `nbs/`. I want to turn them into cards from the filenames, without having to read the file contents.

I'm on a train without wifi, so I'll make simple cards for now and maybe later convert them to MonsterUI.


```python
from fasthtml.common import *
from IPython.display import display, HTML
from pathlib import Path
import regex
```


```python
nb_dir = Path('.')
nbs = L(sorted(nb_dir.glob('*.ipynb'), reverse=True)).map(str)
nbs
```


```python
nbs[0]
```


```python
x = nbs[0]
x
```


```python
L(regex.findall(r"\d+", x))
```


```python
def get_date_from_fname(fname):
    year, month, day = L(regex.findall(r"\d+", fname))[0:3]
    return f"{year}-{month}-{day}"
```


```python
get_date_from_fname(x)
```


```python
get_date_from_fname('2024-12-23-Exploring-execnb-and-nb2fasthtml.ipynb')
```


```python
L(regex.finditer(r"\d+", x))
```


```python
x[11:][:-6].replace('-', ' ')
```


```python
def get_title_from_fname(fname): return fname[11:][:-6].replace('-', ' ').replace('_', ' ')
```


```python
[get_title_from_fname(x) for x in nbs]
```


```python
L(nbs).map(get_title_from_fname)
```


```python
date = get_date_from_fname(x)
title = get_title_from_fname(x)
a = Div(Header(H2(title)),I(date),style="border:1px lightgray solid;padding:10px;")
a
```


```python
HTML(to_xml(a))
```

I have wifi now! Monster UI cards use FrankenUI Card CSS, which is defined in https://github.com/franken-ui/ui/blob/master/src/lib/shadcn-ui/components/card.ts which apply Tailwind classes like [pt-0](https://tailwindcss.com/docs/padding). It's a bit involved to set up that whole build pipeline to extract and modify card styles, and I have to get off this train in 2 stops, so for now I'll continue with the simple CSS one-liner.


```python
def Card(fname):
    date = get_date_from_fname(fname)
    title = get_title_from_fname(fname)
    c = Div(Header(H2(title)),I(date),style="border:1px lightgray solid;padding:10px;display:grid;grid-template-rows: max-content 30px 1fr;")
    return c
HTML(to_xml(Card(x)))
```


```python
HTML(to_xml(Div(*L(nbs).map(Card), style="margin:1em auto;display:grid;grid-template-columns:repeat(auto-fill, minmax(180px,1fr));grid-gap:20px;")))
```

I asked AI: How to make the cards look better?


```python
def Card(fname):
    date = get_date_from_fname(fname)
    title = get_title_from_fname(fname)
    style = """
        border: 1px solid #e2e8f0;
        padding: 1.25rem;
        border-radius: 0.5rem;
        background: white;
        box-shadow: 0 1px 3px rgba(0,0,0,0.12);
        transition: transform 0.2s ease;
        cursor: pointer;
    """
    header_style = "margin-bottom: 0.5rem; font-weight: 600;"
    date_style = "color: #666; font-size: 0.875rem;"
    
    c = Div(
        Header(H2(title, style=header_style)),
        I(date, style=date_style),
        style=style,
        onmouseover="this.style.transform='translateY(-2px)';this.style.boxShadow='0 4px 6px rgba(0,0,0,0.1)'",
        onmouseout="this.style.transform='none';this.style.boxShadow='0 1px 3px rgba(0,0,0,0.12)'"
    )
    return c
```


```python
# Container style with some padding and max-width
container_style = """
    margin: 2em auto;
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(220px,1fr));
    grid-gap: 1.5rem;
    padding: 1rem;
    max-width: 1200px;
"""

HTML(to_xml(Div(*L(nbs).map(Card), style=container_style)))
```

This adds:
- Softer borders and subtle shadow
- Hover effect with lift animation
- Better spacing and typography
- Rounded corners
- Wider cards and more gap between them
- Container max-width and padding
- Pointer cursor to indicate clickable
