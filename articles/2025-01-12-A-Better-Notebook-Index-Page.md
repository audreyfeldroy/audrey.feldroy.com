# A Better Notebook Index Page

I've made good progress on creating a notebook every day. Now I have so many notebooks that my index page needs an overhaul, including:

* Dates with datetime
* Cards with execnb to grab notebook titles
* The cache decorator to make that fast
* Subtle CSS tweaks to increase information density


```python
from datetime import datetime
from execnb.nbio import read_nb
from fasthtml.common import *
from fastcore.all import *
from functools import cache
from pathlib import Path, PosixPath
```

## List Live Posts


```python
nbs = L(Path('../arg-blog-fasthtml/nbs').glob('*.ipynb'))
nbs
```




    (#34) [Path('../arg-blog-fasthtml/nbs/2023-07-29-Blogging-With-nbdev.ipynb'),Path('../arg-blog-fasthtml/nbs/2024-12-31-Note-Box-FastTag.ipynb'),Path('../arg-blog-fasthtml/nbs/2024-07-29-Delegates-Decorator.ipynb'),Path('../arg-blog-fasthtml/nbs/2024-07-29-Auth-in-FastHTML.ipynb'),Path('../arg-blog-fasthtml/nbs/2025-01-09-Reading-and-Writing-Jupyter-Notebooks-With-Python.ipynb'),Path('../arg-blog-fasthtml/nbs/2025-01-06-Understanding-FastHTML-Headers.ipynb'),Path('../arg-blog-fasthtml/nbs/2025-01-10-Understanding-FastHTML-Routes-Requests-and-Redirects.ipynb'),Path('../arg-blog-fasthtml/nbs/2024-07-16_Xtend_Pico.ipynb'),Path('../arg-blog-fasthtml/nbs/2024-12-28-Minimal-Typography-for-FastHTML-Apps.ipynb'),Path('../arg-blog-fasthtml/nbs/2024-12-26-Showing-FTs-in-Jupyter-Notebooks.ipynb'),Path('../arg-blog-fasthtml/nbs/2025-01-04-Claude-Artifacts-in-Notebooks.ipynb'),Path('../arg-blog-fasthtml/nbs/2025-01-05-SSH-Agent-to-Save-Passphrase-Typing.ipynb'),Path('../arg-blog-fasthtml/nbs/2024-12-27-Notebook-Names-to-Cards.ipynb'),Path('../arg-blog-fasthtml/nbs/2025-01-11-NBClassic-Keyboard-Shortcuts-in-Command-and-Dual-Mode.ipynb'),Path('../arg-blog-fasthtml/nbs/2025-01-01-FastHTML-Piano-Part-1.ipynb'),Path('../arg-blog-fasthtml/nbs/2025-01-07-Verifying-Bluesky-Domain-in-FastHTML.ipynb'),Path('../arg-blog-fasthtml/nbs/2024-12-24-Trying-execnb.ipynb'),Path('../arg-blog-fasthtml/nbs/2025-01-01-Command-Substitution-in-Bash.ipynb'),Path('../arg-blog-fasthtml/nbs/2024-08-05-Claudette-FastHTML.ipynb'),Path('../arg-blog-fasthtml/nbs/2024-12-27-CSS-Scope-Leakage-Pygments.ipynb')...]



According to this, I have 34 notebooks in `arg-blog-fasthtml/nbs`, which matches the 34 cards on audrey.feldroy.com.

## Pathlib, User Directory, and PosixPath


```python
PosixPath('~/fun/arg-blog-fasthtml/nbs').expanduser()
```




    Path('/Users/arg/fun/arg-blog-fasthtml/nbs')



To specify the path in terms of my home directory `~`, I use `PosixPath`.


```python
nbs = L(sorted(PosixPath('~/fun/arg-blog-fasthtml/nbs').expanduser().glob('*.ipynb'), reverse=True))
nbs
```




    (#34) [Path('/Users/arg/fun/arg-blog-fasthtml/nbs/2025-01-11-NBClassic-Keyboard-Shortcuts-in-Command-and-Dual-Mode.ipynb'),Path('/Users/arg/fun/arg-blog-fasthtml/nbs/2025-01-10-Understanding-FastHTML-Routes-Requests-and-Redirects.ipynb'),Path('/Users/arg/fun/arg-blog-fasthtml/nbs/2025-01-09-Reading-and-Writing-Jupyter-Notebooks-With-Python.ipynb'),Path('/Users/arg/fun/arg-blog-fasthtml/nbs/2025-01-08-HTML-Title-Tag-in-FastHTML.ipynb'),Path('/Users/arg/fun/arg-blog-fasthtml/nbs/2025-01-07-Verifying-Bluesky-Domain-in-FastHTML.ipynb'),Path('/Users/arg/fun/arg-blog-fasthtml/nbs/2025-01-06-Understanding-FastHTML-Headers.ipynb'),Path('/Users/arg/fun/arg-blog-fasthtml/nbs/2025-01-05-SSH-Agent-to-Save-Passphrase-Typing.ipynb'),Path('/Users/arg/fun/arg-blog-fasthtml/nbs/2025-01-04-Claude-Artifacts-in-Notebooks.ipynb'),Path('/Users/arg/fun/arg-blog-fasthtml/nbs/2025-01-03-Using-zip.ipynb'),Path('/Users/arg/fun/arg-blog-fasthtml/nbs/2025-01-02-FastHTML-Piano-Part-3.ipynb'),Path('/Users/arg/fun/arg-blog-fasthtml/nbs/2025-01-02-FastHTML-Piano-Part-2.ipynb'),Path('/Users/arg/fun/arg-blog-fasthtml/nbs/2025-01-01-FastHTML-Piano-Part-1.ipynb'),Path('/Users/arg/fun/arg-blog-fasthtml/nbs/2025-01-01-Command-Substitution-in-Bash.ipynb'),Path('/Users/arg/fun/arg-blog-fasthtml/nbs/2024-12-31-Note-Box-FastTag.ipynb'),Path('/Users/arg/fun/arg-blog-fasthtml/nbs/2024-12-30-Images-In-Every-Way-In-Notebooks.ipynb'),Path('/Users/arg/fun/arg-blog-fasthtml/nbs/2024-12-29-Bash-in-Jupyter-Notebooks.ipynb'),Path('/Users/arg/fun/arg-blog-fasthtml/nbs/2024-12-28-Minimal-Typography-for-FastHTML-Apps.ipynb'),Path('/Users/arg/fun/arg-blog-fasthtml/nbs/2024-12-27-Notebook-Names-to-Cards.ipynb'),Path('/Users/arg/fun/arg-blog-fasthtml/nbs/2024-12-27-CSS-Scope-Leakage-Pygments.ipynb'),Path('/Users/arg/fun/arg-blog-fasthtml/nbs/2024-12-26-Showing-FTs-in-Jupyter-Notebooks.ipynb')...]



Here I expand `~` into `/Users/arg/`, list files that end in .ipynb, and convert the generator object into a readable list with a fastcore `L` list.

## Display the Notebooks List Nicely


```python
for nb in nbs: print(nb.name)
```

    2025-01-11-NBClassic-Keyboard-Shortcuts-in-Command-and-Dual-Mode.ipynb
    2025-01-10-Understanding-FastHTML-Routes-Requests-and-Redirects.ipynb
    2025-01-09-Reading-and-Writing-Jupyter-Notebooks-With-Python.ipynb
    2025-01-08-HTML-Title-Tag-in-FastHTML.ipynb
    2025-01-07-Verifying-Bluesky-Domain-in-FastHTML.ipynb
    2025-01-06-Understanding-FastHTML-Headers.ipynb
    2025-01-05-SSH-Agent-to-Save-Passphrase-Typing.ipynb
    2025-01-04-Claude-Artifacts-in-Notebooks.ipynb
    2025-01-03-Using-zip.ipynb
    2025-01-02-FastHTML-Piano-Part-3.ipynb
    2025-01-02-FastHTML-Piano-Part-2.ipynb
    2025-01-01-FastHTML-Piano-Part-1.ipynb
    2025-01-01-Command-Substitution-in-Bash.ipynb
    2024-12-31-Note-Box-FastTag.ipynb
    2024-12-30-Images-In-Every-Way-In-Notebooks.ipynb
    2024-12-29-Bash-in-Jupyter-Notebooks.ipynb
    2024-12-28-Minimal-Typography-for-FastHTML-Apps.ipynb
    2024-12-27-Notebook-Names-to-Cards.ipynb
    2024-12-27-CSS-Scope-Leakage-Pygments.ipynb
    2024-12-26-Showing-FTs-in-Jupyter-Notebooks.ipynb
    2024-12-25-Notebook-Pygments.ipynb
    2024-12-24-Trying-execnb.ipynb
    2024-12-24-Deck-the-Halls.ipynb
    2024-12-23-Exploring-execnb-and-nb2fasthtml.ipynb
    2024-12-23-Daddys_Snowman_Card.ipynb
    2024-08-05-Claudette-FastHTML.ipynb
    2024-08-04-Claudette.ipynb
    2024-07-29-FH-by-Example.ipynb
    2024-07-29-Delegates-Decorator.ipynb
    2024-07-29-Auth-in-FastHTML.ipynb
    2024-07-16_Xtend_Pico.ipynb
    2024-07-15-Printing_Components.ipynb
    2024-07-14_SemanticUI_Cards.ipynb
    2023-07-29-Blogging-With-nbdev.ipynb


If we just print the filenames, we can see my current approach of naming them with the date and TitleCase title.

## New Approach

Doing this has given me insight about how to improve my site:

* Keep naming files as before
* Now for the index page, get the titles from the notebooks instead of the filenames

When there were just a few notebooks, these cards were great. Now I want a more information-dense layout with tighter cards, and with titles containing proper punctuation coming from the notebooks themselves.

## Revisit Date Parsing

I'm currently getting dates from ISO 8601-prefixed filenames with this not-great code that I hacked together quickly:


```python
def get_date_from_fname(fname):
    try:
        year, month, day = L(regex.findall(r"\d+", fname))[0:3]
    except Exception:
        year, month, day = 0,0,0
    return f"{year}-{month}-{day}"
```

I talked with Claude 3.5 Sonnet about it. It generated code that looked awesome at first but wasn't my favorite when I experimented with it carefully. But something good resulted: out of that I learned about `datetime.fromisoformat` and looked it up in the [Python datetime docs](https://docs.python.org/3/library/datetime.html#datetime.datetime.fromisoformat).


```python
d = datetime.fromisoformat('2025-01-04')
d
```




    datetime.datetime(2025, 1, 4, 0, 0)



It's actually nice to have `datetime` objects here because I can get the parts like:


```python
d.year, d.month, d.day
```




    (2025, 1, 4)



And print them with f-strings:


```python
print(f"{d:%a, %b %-d, %Y}")
```

    Sat, Jan 4, 2025


I like that combination of readability and abbreviations. I'll try it and see if I still like it later.

## Iterate on ISO 8601 Date Parsing

My improved function:


```python
@cache
def get_date_from_iso8601_prefix(fname):
    "Gets date from first 10 chars YYYY-MM-DD of `fname`, where `fname` is like `2025-01-12-Get-Date-From-This.whatever"
    try:
        return datetime.fromisoformat(str(fname)[:10])
    except ValueError: return None
```

Note: on my first pass writing this notebook, I didn't use the `@cache` decorator. I waited until the end to cache, to make debugging easier for myself. It'll become clear in the next section on notebook titles why caching is good here.

Now let's test it by grabbing a filename and passing it in.


```python
nbs[0]
```




    Path('/Users/arg/fun/arg-blog-fasthtml/nbs/2025-01-11-NBClassic-Keyboard-Shortcuts-in-Command-and-Dual-Mode.ipynb')




```python
nbs[0].name
```




    '2025-01-11-NBClassic-Keyboard-Shortcuts-in-Command-and-Dual-Mode.ipynb'




```python
d = get_date_from_iso8601_prefix(nbs[0].name)
d
```




    datetime.datetime(2025, 1, 11, 0, 0)



## Iterate on Getting Notebook Titles

Instead of parsing filenames, I'm going to grab the first cell of each notebook and remove the `# ` prefix.


```python
nbc = read_nb(nbs[0].name)
nbc.cells[0]
```




```json
{ 'cell_type': 'markdown',
  'id': '7a932161',
  'idx_': 0,
  'metadata': {},
  'source': '# NBClassic Keyboard Shortcuts: Command and Dual-Mode'}
```




```python
nbc.cells[0].source
```




    '# NBClassic Keyboard Shortcuts: Command and Dual-Mode'




```python
nbc.cells[0].source.lstrip('# ')
```




    'NBClassic Keyboard Shortcuts: Command and Dual-Mode'



### Make That a Function


```python
def get_title(fname):
    "Get title from `fname` notebook's cell 0 source by stripping '# ' prefix"
    nbc = read_nb(fname)
    return nbc.cells[0].source.lstrip('# ')
```


```python
get_title(nbs[0])
```




    'NBClassic Keyboard Shortcuts: Command and Dual-Mode'




```python
get_title(nbs[1])
```




    'Understanding FastHTML Routes, Requests, and Redirects'



### Try It on All Titles


```python
print(nbs.map(get_title))
```

    ['NBClassic Keyboard Shortcuts: Command and Dual-Mode', 'Understanding FastHTML Routes, Requests, and Redirects', 'Reading and Writing Jupyter Notebooks With Python', 'HTML Title Tag in FastHTML', 'Verifying a Bluesky Domain Handle on a FastHTML Site', 'Understanding FastHTML Headers', 'Using SSH Agent to Save Passphrase Typing', 'Showing Claude Artifacts in Jupyter Notebooks', 'Using zip', 'FastHTML Piano, Part 3', 'FastHTML Piano, Part 2', 'FastHTML Piano, Part 1', 'Command Substitution in Bash', 'Note Box FastTag', 'Images in Jupyter Notebooks, in Every Way', 'Bash in Jupyter Notebooks', 'Minimal Typography for FastHTML Apps', 'Transforming Notebook Names to Cards', 'How I Fixed CSS Scope Leakage in Pygments Syntax Highlighting', 'Showing Components in Notebooks', 'Converting Jupyter Notebook Cells to Pygments Syntax-Highlighted HTML', 'What Can `execnb` do?', 'Deck the Halls', "execnb's read_nb and nb2fasthtml's render_nb", "Daddy's Snowman Card", 'Using Claudette with FastHTML', 'Claudette', 'FastHTML by Example', 'Delegates Decorator\n\nMy study of the `@delegates` decorator and `GetAttr` from `fastcore`, as described in https://www.fast.ai/posts/2019-08-06-delegation.html', 'Auth in FastHTML\n\nBasic auth:\n\n* https://github.com/AnswerDotAI/fasthtml/blob/main/fasthtml/authmw.py\n* https://github.com/AnswerDotAI/fasthtml/blob/main/nbs/api/00_core.ipynb has some auth tests\n\nOauth:\n\n* https://github.com/AnswerDotAI/fasthtml/blob/main/nbs/incomplete/oauth.ipynb\n', 'Understanding FastHTML xtend\n\nCurrent FastHTML Pico Card: https://github.com/AnswerDotAI/fasthtml/blob/main/fasthtml/xtend.py#L76', 'Printing FastHTML Components', 'SemanticUI FastHTML Cards', 'Setting Up a Blog With nbdev\n\nI feel like Jupyter notebooks would be really nice for blogging or publishing "Today I Learned" posts. I had heard about Fastpages before via Jeremy Howard\'s blog or YouTube videos, but seeing that it was deprecated in favor of nbdev, I decided to try nbdev.\n\nI followed the [End-to-End Walkthrough nbdev tutorial](https://nbdev.fast.ai/tutorials/tutorial.html).']


### Find the Broken Titles


```python
def has_newline(x): return '\n' in x
broken = nbs.map(get_title).filter(has_newline)
broken
```




    (#4) ['Delegates Decorator\n\nMy study of the `@delegates` decorator and `GetAttr` from `fastcore`, as described in https://www.fast.ai/posts/2019-08-06-delegation.html','Auth in FastHTML\n\nBasic auth:\n\n* https://github.com/AnswerDotAI/fasthtml/blob/main/fasthtml/authmw.py\n* https://github.com/AnswerDotAI/fasthtml/blob/main/nbs/api/00_core.ipynb has some auth tests\n\nOauth:\n\n* https://github.com/AnswerDotAI/fasthtml/blob/main/nbs/incomplete/oauth.ipynb\n','Understanding FastHTML xtend\n\nCurrent FastHTML Pico Card: https://github.com/AnswerDotAI/fasthtml/blob/main/fasthtml/xtend.py#L76','Setting Up a Blog With nbdev\n\nI feel like Jupyter notebooks would be really nice for blogging or publishing "Today I Learned" posts. I had heard about Fastpages before via Jeremy Howard\'s blog or YouTube videos, but seeing that it was deprecated in favor of nbdev, I decided to try nbdev.\n\nI followed the [End-to-End Walkthrough nbdev tutorial](https://nbdev.fast.ai/tutorials/tutorial.html).']



### Fix Broken Titles


```python
broken[0]
```




    'Delegates Decorator\n\nMy study of the `@delegates` decorator and `GetAttr` from `fastcore`, as described in https://www.fast.ai/posts/2019-08-06-delegation.html'




```python
broken[0].split('\n')
```




    ['Delegates Decorator',
     '',
     'My study of the `@delegates` decorator and `GetAttr` from `fastcore`, as described in https://www.fast.ai/posts/2019-08-06-delegation.html']




```python
first(broken[0].split('\n'))
```




    'Delegates Decorator'




```python
@cache
def get_title(fname):
    "Get title from `fname` notebook's cell 0 source by stripping '# ' prefix"
    nbc = read_nb(fname)
    nbc = nbc.cells[0].source.lstrip('# ')
    if '\n' in nbc:
        return first(nbc.split('\n'))
    return nbc
```

You can imagine how running this on every notebook would be slow! So we add `@cache`.


```python
nbs[28]
```




    Path('/Users/arg/fun/arg-blog-fasthtml/nbs/2024-07-29-Delegates-Decorator.ipynb')




```python
get_title(nbs[28])
```




    'Delegates Decorator'




```python
print(nbs.map(get_title))
```

    ['NBClassic Keyboard Shortcuts: Command and Dual-Mode', 'Understanding FastHTML Routes, Requests, and Redirects', 'Reading and Writing Jupyter Notebooks With Python', 'HTML Title Tag in FastHTML', 'Verifying a Bluesky Domain Handle on a FastHTML Site', 'Understanding FastHTML Headers', 'Using SSH Agent to Save Passphrase Typing', 'Showing Claude Artifacts in Jupyter Notebooks', 'Using zip', 'FastHTML Piano, Part 3', 'FastHTML Piano, Part 2', 'FastHTML Piano, Part 1', 'Command Substitution in Bash', 'Note Box FastTag', 'Images in Jupyter Notebooks, in Every Way', 'Bash in Jupyter Notebooks', 'Minimal Typography for FastHTML Apps', 'Transforming Notebook Names to Cards', 'How I Fixed CSS Scope Leakage in Pygments Syntax Highlighting', 'Showing Components in Notebooks', 'Converting Jupyter Notebook Cells to Pygments Syntax-Highlighted HTML', 'What Can `execnb` do?', 'Deck the Halls', "execnb's read_nb and nb2fasthtml's render_nb", "Daddy's Snowman Card", 'Using Claudette with FastHTML', 'Claudette', 'FastHTML by Example', 'Delegates Decorator', 'Auth in FastHTML', 'Understanding FastHTML xtend', 'Printing FastHTML Components', 'SemanticUI FastHTML Cards', 'Setting Up a Blog With nbdev']


## Iterate on Cards

My cards were created with this FastTag:


```python
@cache
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
        text-decoration: none;
        color: inherit;
        display: block;
    """
    header_style = "margin-bottom: 0.5rem; font-weight: 600;"
    date_style = "color: #666; font-size: 0.875rem;"
    
    c = A(
        Header(H2(title, style=header_style)),
        I(date, style=date_style),
        style=style,
        href=f'/nbs/{fname[4:][:-6]}',
        onmouseover="this.style.transform='translateY(-2px)';this.style.boxShadow='0 4px 6px rgba(0,0,0,0.1)'",
        onmouseout="this.style.transform='none';this.style.boxShadow='0 1px 3px rgba(0,0,0,0.12)'"
    )
    return c
```

Let's rebuild it from scratch with our new functions.


```python
nbs[0]
```




    Path('/Users/arg/fun/arg-blog-fasthtml/nbs/2025-01-11-NBClassic-Keyboard-Shortcuts-in-Command-and-Dual-Mode.ipynb')




```python
get_title(nbs[0])
```




    'NBClassic Keyboard Shortcuts: Command and Dual-Mode'




```python
def Card(fname):
    date = get_date_from_iso8601_prefix(fname.name)
    title = get_title(fname)
    return A(
        Header(H2(title, style="margin:0 0 0.5rem 0;font-size:1.25rem;")),
        Div(f"{date:%a, %b %-d, %Y}", style="font-size: 0.875rem;color:#666;"),
        href=f'/nbs/{fname.name[4:][:-6]}',
        onmouseover="this.style.transform='translateY(-2px)';this.style.boxShadow='0 4px 6px rgba(0,0,0,0.1)'",
        onmouseout="this.style.transform='none';this.style.boxShadow='0 1px 3px rgba(0,0,0,0.12)'",
        style="""border:1px solid #e2e8f0;
        padding:1rem;
        border-radius: 0.5rem;
        background: white;
        box-shadow: 0 1px 3px rgba(0,0,0,0.12);
        transition: transform 0.2s ease;
        cursor: pointer;
        text-decoration: none;
        color: inherit;
        display: block;
    """)
show(Div(Style(':root {font-family: system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", sans-serif; font-size:16px;} p {line-height: 1.5;}'), Card(nbs[0])))
```


<div>
  <style>:root {font-family: system-ui, -apple-system, &quot;Segoe UI&quot;, Roboto, &quot;Helvetica Neue&quot;, sans-serif; font-size:16px;} p {line-height: 1.5;}</style>
<a href="/nbs/-01-11-NBClassic-Keyboard-Shortcuts-in-Command-and-Dual-Mode" onmouseover="this.style.transform='translateY(-2px)';this.style.boxShadow='0 4px 6px rgba(0,0,0,0.1)'" onmouseout="this.style.transform='none';this.style.boxShadow='0 1px 3px rgba(0,0,0,0.12)'" style="border:1px solid #e2e8f0;
        padding:1rem;
        border-radius: 0.5rem;
        background: white;
        box-shadow: 0 1px 3px rgba(0,0,0,0.12);
        transition: transform 0.2s ease;
        cursor: pointer;
        text-decoration: none;
        color: inherit;
        display: block;
    ">    <header>
      <h2 style="margin:0 0 0.5rem 0;font-size:1.25rem;">NBClassic Keyboard Shortcuts: Command and Dual-Mode</h2>
    </header>
    <div style="font-size: 0.875rem;color:#666;">Sat, Jan 11, 2025</div>
</a></div>



Here I had to set a root element so `rem` font sizes would show correctly here in nbclassic, where I'm working from. There's more to get it to look right here, but I'm getting a bit tired.

You may be wondering about how there's a lot of CSS getting repeated in each card instance. There aren't that many cards right now, and this is still way smaller than a React/Tailwind app. I have some interesting ideas here that I'll save for another day.

## Bringing Changes Over to My Blog App

My blog app [arg-blog-fasthtml](https://github.com/audreyfeldroy/arg-blog-fasthtml) has a `main.py` that isn't notebook-generated. 

Note: At this point, considering how many functions I rewrote in this notebook, it would be nice to move that `main.py` to notebooks. I originally had started writing it in notebooks but had moved to the simple main.py to make troubleshooting deployment on a PaaS easier. 

For now, I've updated `main.py` with all of the above manually. I'm like a manual version of `nbdev_export` and that tells me that I should automate.

## Caching

With `@cache` on all the functions above, the index page is super snappy locally! Yes, that's the unbounded cache, but I have few and small enough things to cache that I won't worry about it for now. I can explore it another time.

## Summary

I've made good progress improving my blog's index page!

1. Better date handling using `datetime.fromisoformat()` instead of regex parsing
2. Getting proper titles from notebook first cells instead of filenames
3. Tighter, more information-dense cards with improved typography
4. Caching with `@cache` to keep things snappy

It's working well locally, and we'll see what happens when I deploy. I manually updated my blog app's `main.py` with these changes, though doing this made me realize I should probably move that code into notebooks and use `nbdev_export` instead of copying by hand.

There's still room for improvement, but I'm happy with my progress!
