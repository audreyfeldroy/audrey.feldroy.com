# This Site Is Now Powered by This Notebook

Here in this Jupyter notebook I rewrite audrey.feldroy.com and use nb_export to export it as my new main.py for arg-blog-fasthtml.


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
tags = ["Python", "Jupyter"]
```

## Background

Before this notebook, the code for my blog was a main.py that I maintained by editing it in VS Code. The index page and notebooks were rendered without MonsterUI. I wanted to keep it minimal because sometimes I do crazy CSS experiments.

Yesterday in [Customizing FastHTML Headers From Notebook Contents](https://audrey.feldroy.com/nbs/2025-01-22-Customizing-FastHTML-Headers-From-Notebook-Contents) I discovered that different routes can have different HTML headers thanks to `_xt_cts`. I then modified my notebook detail view to include MonsterUI headers only when I tag the notebook with "MonsterUI".

Today I was inspired by [Solve It With Code](https://solveit.fast.ai/) Lesson 11 to try rewriting more of my blog in MonsterUI. 

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


## Notebook Index: Cards


```python
def NBCard(t,d):
    return franken.Card(d, header=franken.H3(t))
```


```python
NBCard("First Post", "This is a description of what my post is about")
```




```html
<div class="uk-card ">
  <div class="uk-card-header ">
    <h3 class="uk-h3 ">First Post</h3>
  </div>
  <div class="uk-card-body space-y-6">This is a description of what my post is about</div>
</div>

```




```python
show(NBCard("First Post", "This is a description of what my post is about"))
```


<div class="uk-card ">
  <div class="uk-card-header ">
    <h3 class="uk-h3 ">First Post</h3>
  </div>
  <div class="uk-card-body space-y-6">This is a description of what my post is about</div>
</div>
<script>if (window.htmx) htmx.process(document.body)</script>



```python
#| export
def get_nb_paths(): return L(sorted(Path().glob("nbs/*.ipynb"), reverse=True))
```

Note: change to `glob("*.ipynb")` to run this from the notebook


```python
nb_paths = get_nb_paths()
nb_paths
```




    (#0) []




```python
read_nb(nb_paths[0]).cells[0].source.lstrip("# ")
```




    'Using My Blog to Rewrite Itself'



This is the title of the first notebook.


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




    ('Using My Blog to Rewrite Itself',
     'Here I use my blog made of Jupyter notebooks to rewrite itself.')




```python
show(NBCard(*get_title_and_desc(nb_paths[0])))
```


<div class="uk-card ">
  <div class="uk-card-header ">
    <h3 class="uk-h3 ">Using My Blog to Rewrite Itself</h3>
  </div>
  <div class="uk-card-body space-y-6">Here I use my blog made of Jupyter notebooks to rewrite itself.</div>
</div>
<script>if (window.htmx) htmx.process(document.body)</script>



```python
def mk_nbcard_from_nb_path(nb_path):
    return NBCard(*get_title_and_desc(nb_path))
```


```python
mk_nbcard_from_nb_path(nb_paths[0])
```




```html
<div class="uk-card ">
  <div class="uk-card-header ">
    <h3 class="uk-h3 ">Using My Blog to Rewrite Itself</h3>
  </div>
  <div class="uk-card-body space-y-6">Here I use my blog made of Jupyter notebooks to rewrite itself.</div>
</div>

```




```python
nb_paths.map(mk_nbcard_from_nb_path)[:2]
```




    (#2) [div((div((h3(('Using My Blog to Rewrite Itself',),{'class': 'uk-h3 '}),),{'class': 'uk-card-header '}), div(('Here I use my blog made of Jupyter notebooks to rewrite itself.',),{'class': 'uk-card-body space-y-6'})),{'class': 'uk-card '}),div((div((h3(('Troubleshooting MonsterUI on This Site',),{'class': 'uk-h3 '}),),{'class': 'uk-card-header '}), div(("My first MonsterUI notebook isn't rendering correctly. Here I debug it.",),{'class': 'uk-card-body space-y-6'})),{'class': 'uk-card '})]




```python
show(*nb_paths.map(mk_nbcard_from_nb_path)[:2])
```


<div class="uk-card ">
  <div class="uk-card-header ">
    <h3 class="uk-h3 ">Using My Blog to Rewrite Itself</h3>
  </div>
  <div class="uk-card-body space-y-6">Here I use my blog made of Jupyter notebooks to rewrite itself.</div>
</div>
<div class="uk-card ">
  <div class="uk-card-header ">
    <h3 class="uk-h3 ">Troubleshooting MonsterUI on This Site</h3>
  </div>
  <div class="uk-card-body space-y-6">My first MonsterUI notebook isn&#x27;t rendering correctly. Here I debug it.</div>
</div>
<script>if (window.htmx) htmx.process(document.body)</script>


## Notebook Index: Add Dates to Cards


```python
#| export
def get_date_from_iso8601_prefix(fname):
    "Gets date from first 10 chars YYYY-MM-DD of `fname`, where `fname` is like `2025-01-12-Get-Date-From-This.whatever"
    try:
        return datetime.fromisoformat(str(fname)[4:14])
    except ValueError: return None
```


```python
nb_paths[0]
```




    Path('2025-01-23-Using-My-Blog-to-Rewrite-Itself.ipynb')




```python
date = get_date_from_iso8601_prefix(nb_paths[0])
```


```python
Div(f"{date:%a, %b %-d, %Y}", style="font-size: 0.875rem;color:#666;")
```




```html
<div style="font-size: 0.875rem;color:#666;">Thu, Jan 23, 2025</div>

```




```python
franken.PSmall(f"{date:%a, %b %-d, %Y}", cls="uk-text-muted")
```




```html
<p class="uk-text-small uk-text-muted">Thu, Jan 23, 2025</p>

```




```python
def NBCard(t,d):
    return franken.Card(
        franken.CardTitle(franken.H3(t)), 
        franken.PSmall(f"{date:%a, %b %-d, %Y}", cls="uk-text-muted"),
        franken.P(d),
        body_cls='space-y-2'
    )
```


```python
c = mk_nbcard_from_nb_path(nb_paths[0])
c
```




```html
<div class="uk-card ">
  <div class="uk-card-body space-y-2">
    <div class="uk-card-title ">
      <h3 class="uk-h3 ">Using My Blog to Rewrite Itself</h3>
    </div>
    <p class="uk-text-small uk-text-muted">Thu, Jan 23, 2025</p>
    <p>Here I use my blog made of Jupyter notebooks to rewrite itself.</p>
  </div>
</div>

```




```python
show(c)
```


<div class="uk-card ">
  <div class="uk-card-body space-y-2">
    <div class="uk-card-title ">
      <h3 class="uk-h3 ">Using My Blog to Rewrite Itself</h3>
    </div>
    <p class="uk-text-small uk-text-muted">Thu, Jan 23, 2025</p>
    <p>Here I use my blog made of Jupyter notebooks to rewrite itself.</p>
  </div>
</div>
<script>if (window.htmx) htmx.process(document.body)</script>


## Notebook Index: Linkify Cards


```python
#| export
def NBCard(title,desc,href,date):
    return A(
        franken.Card(
        franken.CardTitle(franken.H3(title)), 
        franken.PSmall(f"{date:%a, %b %-d, %Y}", cls="uk-text-muted"),
        franken.P(desc),
        body_cls='space-y-2'
    ), href=href)
```


```python
#| export
def mk_nbcard_from_nb_path(nb_path):
    date = get_date_from_iso8601_prefix(nb_path)
    return NBCard(*get_title_and_desc(nb_path), href=f'/nbs/{nb_path.name[:-6]}', date=date)
```


```python
c = mk_nbcard_from_nb_path(nb_paths[1])
c
```




```html
<a href="/nbs/2025-01-23-Troubleshooting-MonsterUI-on-This-Site">  <div class="uk-card ">
    <div class="uk-card-body space-y-2">
      <div class="uk-card-title ">
        <h3 class="uk-h3 ">Troubleshooting MonsterUI on This Site</h3>
      </div>
      <p class="uk-text-small uk-text-muted">Thu, Jan 23, 2025</p>
      <p>My first MonsterUI notebook isn&#x27;t rendering correctly. Here I debug it.</p>
    </div>
  </div>
</a>
```




```python
show(c)
```


<a href="/nbs/2025-01-23-Troubleshooting-MonsterUI-on-This-Site">  <div class="uk-card ">
    <div class="uk-card-body space-y-2">
      <div class="uk-card-title ">
        <h3 class="uk-h3 ">Troubleshooting MonsterUI on This Site</h3>
      </div>
      <p class="uk-text-small uk-text-muted">Thu, Jan 23, 2025</p>
      <p>My first MonsterUI notebook isn&#x27;t rendering correctly. Here I debug it.</p>
    </div>
  </div>
</a><script>if (window.htmx) htmx.process(document.body)</script>


## Notebook Index Page


```python
#| export
@rt
def index():
    nb_paths = get_nb_paths()
    return (
        Theme.blue.headers(),
        franken.Container(
            Div(
                franken.H1('audrey.feldroy.com'), franken.PParagraph("The experimental Jupyter notebooks of Audrey M. Roy Greenfeld. This website and all its notebooks are open-source at ", franken.A("github.com/audreyfeldroy/arg-blog-fasthtml", href="https://github.com/audreyfeldroy/arg-blog-fasthtml"), cls="mb-6"),
            ),
            franken.Grid(*nb_paths.map(mk_nbcard_from_nb_path), cols_sm=1, cols_md=1, cols_lg=2, cols_xl=3)
        )
    )
```

## Notebook Detail: Frontmatter


```python
t,d = get_title_and_desc(nb_paths[1])
t,d
```




    ('Troubleshooting MonsterUI on This Site',
     "My first MonsterUI notebook isn't rendering correctly. Here I debug it.")




```python
mistletoe.markdown(d)
```




    "<p>My first MonsterUI notebook isn't rendering correctly. Here I debug it.</p>\n"



## Notebook Detail: Non-Frontmatter


```python
nb_paths[1]
```




    Path('2025-01-23-Troubleshooting-MonsterUI-on-This-Site.ipynb')



### Use StyledCode (Pygments) for Code Cells


```python
nb = read_nb(nb_paths[1])
```


```python
nb.cells[5]
```




```json
{ 'cell_type': 'code',
  'execution_count': 3,
  'id': 'cb344dfb',
  'idx_': 5,
  'metadata': {},
  'outputs': [ { 'data': { 'text/markdown': [ '```html\n',
                                              '<h1 class="uk-h1 ">Hi</h1>\n',
                                              '\n',
                                              '```'],
                           'text/plain': ["h1(('Hi',),{'class': 'uk-h1 '})"]},
                 'execution_count': 3,
                 'metadata': {},
                 'output_type': 'execute_result'}],
  'source': 'H1("Hi")'}
```




```python
#| export
def StyledCode(c, style='monokai'):
    fm = HtmlFormatter(style=style, cssclass=style)
    h = highlight(c, PythonLexer(), fm)
    sd = fm.get_style_defs(f".{style}")
    return Div(Style(sd), NotStr(h), id=style)
```


```python
HTML(to_xml(StyledCode(nb.cells[2].source)))
```




<div id="monokai">
  <style>pre { line-height: 125%; }
td.linenos .normal { color: inherit; background-color: transparent; padding-left: 5px; padding-right: 5px; }
span.linenos { color: inherit; background-color: transparent; padding-left: 5px; padding-right: 5px; }
td.linenos .special { color: #000000; background-color: #ffffc0; padding-left: 5px; padding-right: 5px; }
span.linenos.special { color: #000000; background-color: #ffffc0; padding-left: 5px; padding-right: 5px; }
.monokai .hll { background-color: #49483e }
.monokai { background: #272822; color: #F8F8F2 }
.monokai .c { color: #959077 } /* Comment */
.monokai .err { color: #ED007E; background-color: #1E0010 } /* Error */
.monokai .esc { color: #F8F8F2 } /* Escape */
.monokai .g { color: #F8F8F2 } /* Generic */
.monokai .k { color: #66D9EF } /* Keyword */
.monokai .l { color: #AE81FF } /* Literal */
.monokai .n { color: #F8F8F2 } /* Name */
.monokai .o { color: #FF4689 } /* Operator */
.monokai .x { color: #F8F8F2 } /* Other */
.monokai .p { color: #F8F8F2 } /* Punctuation */
.monokai .ch { color: #959077 } /* Comment.Hashbang */
.monokai .cm { color: #959077 } /* Comment.Multiline */
.monokai .cp { color: #959077 } /* Comment.Preproc */
.monokai .cpf { color: #959077 } /* Comment.PreprocFile */
.monokai .c1 { color: #959077 } /* Comment.Single */
.monokai .cs { color: #959077 } /* Comment.Special */
.monokai .gd { color: #FF4689 } /* Generic.Deleted */
.monokai .ge { color: #F8F8F2; font-style: italic } /* Generic.Emph */
.monokai .ges { color: #F8F8F2; font-weight: bold; font-style: italic } /* Generic.EmphStrong */
.monokai .gr { color: #F8F8F2 } /* Generic.Error */
.monokai .gh { color: #F8F8F2 } /* Generic.Heading */
.monokai .gi { color: #A6E22E } /* Generic.Inserted */
.monokai .go { color: #66D9EF } /* Generic.Output */
.monokai .gp { color: #FF4689; font-weight: bold } /* Generic.Prompt */
.monokai .gs { color: #F8F8F2; font-weight: bold } /* Generic.Strong */
.monokai .gu { color: #959077 } /* Generic.Subheading */
.monokai .gt { color: #F8F8F2 } /* Generic.Traceback */
.monokai .kc { color: #66D9EF } /* Keyword.Constant */
.monokai .kd { color: #66D9EF } /* Keyword.Declaration */
.monokai .kn { color: #FF4689 } /* Keyword.Namespace */
.monokai .kp { color: #66D9EF } /* Keyword.Pseudo */
.monokai .kr { color: #66D9EF } /* Keyword.Reserved */
.monokai .kt { color: #66D9EF } /* Keyword.Type */
.monokai .ld { color: #E6DB74 } /* Literal.Date */
.monokai .m { color: #AE81FF } /* Literal.Number */
.monokai .s { color: #E6DB74 } /* Literal.String */
.monokai .na { color: #A6E22E } /* Name.Attribute */
.monokai .nb { color: #F8F8F2 } /* Name.Builtin */
.monokai .nc { color: #A6E22E } /* Name.Class */
.monokai .no { color: #66D9EF } /* Name.Constant */
.monokai .nd { color: #A6E22E } /* Name.Decorator */
.monokai .ni { color: #F8F8F2 } /* Name.Entity */
.monokai .ne { color: #A6E22E } /* Name.Exception */
.monokai .nf { color: #A6E22E } /* Name.Function */
.monokai .nl { color: #F8F8F2 } /* Name.Label */
.monokai .nn { color: #F8F8F2 } /* Name.Namespace */
.monokai .nx { color: #A6E22E } /* Name.Other */
.monokai .py { color: #F8F8F2 } /* Name.Property */
.monokai .nt { color: #FF4689 } /* Name.Tag */
.monokai .nv { color: #F8F8F2 } /* Name.Variable */
.monokai .ow { color: #FF4689 } /* Operator.Word */
.monokai .pm { color: #F8F8F2 } /* Punctuation.Marker */
.monokai .w { color: #F8F8F2 } /* Text.Whitespace */
.monokai .mb { color: #AE81FF } /* Literal.Number.Bin */
.monokai .mf { color: #AE81FF } /* Literal.Number.Float */
.monokai .mh { color: #AE81FF } /* Literal.Number.Hex */
.monokai .mi { color: #AE81FF } /* Literal.Number.Integer */
.monokai .mo { color: #AE81FF } /* Literal.Number.Oct */
.monokai .sa { color: #E6DB74 } /* Literal.String.Affix */
.monokai .sb { color: #E6DB74 } /* Literal.String.Backtick */
.monokai .sc { color: #E6DB74 } /* Literal.String.Char */
.monokai .dl { color: #E6DB74 } /* Literal.String.Delimiter */
.monokai .sd { color: #E6DB74 } /* Literal.String.Doc */
.monokai .s2 { color: #E6DB74 } /* Literal.String.Double */
.monokai .se { color: #AE81FF } /* Literal.String.Escape */
.monokai .sh { color: #E6DB74 } /* Literal.String.Heredoc */
.monokai .si { color: #E6DB74 } /* Literal.String.Interpol */
.monokai .sx { color: #E6DB74 } /* Literal.String.Other */
.monokai .sr { color: #E6DB74 } /* Literal.String.Regex */
.monokai .s1 { color: #E6DB74 } /* Literal.String.Single */
.monokai .ss { color: #E6DB74 } /* Literal.String.Symbol */
.monokai .bp { color: #F8F8F2 } /* Name.Builtin.Pseudo */
.monokai .fm { color: #A6E22E } /* Name.Function.Magic */
.monokai .vc { color: #F8F8F2 } /* Name.Variable.Class */
.monokai .vg { color: #F8F8F2 } /* Name.Variable.Global */
.monokai .vi { color: #F8F8F2 } /* Name.Variable.Instance */
.monokai .vm { color: #F8F8F2 } /* Name.Variable.Magic */
.monokai .il { color: #AE81FF } /* Literal.Number.Integer.Long */</style>
<div class="monokai"><pre><span></span><span class="kn">from</span><span class="w"> </span><span class="nn">fasthtml.common</span><span class="w"> </span><span class="kn">import</span> <span class="o">*</span>
<span class="kn">from</span><span class="w"> </span><span class="nn">monsterui.all</span><span class="w"> </span><span class="kn">import</span> <span class="o">*</span>
</pre></div>
</div>





```python
HTML(to_xml(StyledCode(nb.cells[5].source)))
```




<div id="monokai">
  <style>pre { line-height: 125%; }
td.linenos .normal { color: inherit; background-color: transparent; padding-left: 5px; padding-right: 5px; }
span.linenos { color: inherit; background-color: transparent; padding-left: 5px; padding-right: 5px; }
td.linenos .special { color: #000000; background-color: #ffffc0; padding-left: 5px; padding-right: 5px; }
span.linenos.special { color: #000000; background-color: #ffffc0; padding-left: 5px; padding-right: 5px; }
.monokai .hll { background-color: #49483e }
.monokai { background: #272822; color: #F8F8F2 }
.monokai .c { color: #959077 } /* Comment */
.monokai .err { color: #ED007E; background-color: #1E0010 } /* Error */
.monokai .esc { color: #F8F8F2 } /* Escape */
.monokai .g { color: #F8F8F2 } /* Generic */
.monokai .k { color: #66D9EF } /* Keyword */
.monokai .l { color: #AE81FF } /* Literal */
.monokai .n { color: #F8F8F2 } /* Name */
.monokai .o { color: #FF4689 } /* Operator */
.monokai .x { color: #F8F8F2 } /* Other */
.monokai .p { color: #F8F8F2 } /* Punctuation */
.monokai .ch { color: #959077 } /* Comment.Hashbang */
.monokai .cm { color: #959077 } /* Comment.Multiline */
.monokai .cp { color: #959077 } /* Comment.Preproc */
.monokai .cpf { color: #959077 } /* Comment.PreprocFile */
.monokai .c1 { color: #959077 } /* Comment.Single */
.monokai .cs { color: #959077 } /* Comment.Special */
.monokai .gd { color: #FF4689 } /* Generic.Deleted */
.monokai .ge { color: #F8F8F2; font-style: italic } /* Generic.Emph */
.monokai .ges { color: #F8F8F2; font-weight: bold; font-style: italic } /* Generic.EmphStrong */
.monokai .gr { color: #F8F8F2 } /* Generic.Error */
.monokai .gh { color: #F8F8F2 } /* Generic.Heading */
.monokai .gi { color: #A6E22E } /* Generic.Inserted */
.monokai .go { color: #66D9EF } /* Generic.Output */
.monokai .gp { color: #FF4689; font-weight: bold } /* Generic.Prompt */
.monokai .gs { color: #F8F8F2; font-weight: bold } /* Generic.Strong */
.monokai .gu { color: #959077 } /* Generic.Subheading */
.monokai .gt { color: #F8F8F2 } /* Generic.Traceback */
.monokai .kc { color: #66D9EF } /* Keyword.Constant */
.monokai .kd { color: #66D9EF } /* Keyword.Declaration */
.monokai .kn { color: #FF4689 } /* Keyword.Namespace */
.monokai .kp { color: #66D9EF } /* Keyword.Pseudo */
.monokai .kr { color: #66D9EF } /* Keyword.Reserved */
.monokai .kt { color: #66D9EF } /* Keyword.Type */
.monokai .ld { color: #E6DB74 } /* Literal.Date */
.monokai .m { color: #AE81FF } /* Literal.Number */
.monokai .s { color: #E6DB74 } /* Literal.String */
.monokai .na { color: #A6E22E } /* Name.Attribute */
.monokai .nb { color: #F8F8F2 } /* Name.Builtin */
.monokai .nc { color: #A6E22E } /* Name.Class */
.monokai .no { color: #66D9EF } /* Name.Constant */
.monokai .nd { color: #A6E22E } /* Name.Decorator */
.monokai .ni { color: #F8F8F2 } /* Name.Entity */
.monokai .ne { color: #A6E22E } /* Name.Exception */
.monokai .nf { color: #A6E22E } /* Name.Function */
.monokai .nl { color: #F8F8F2 } /* Name.Label */
.monokai .nn { color: #F8F8F2 } /* Name.Namespace */
.monokai .nx { color: #A6E22E } /* Name.Other */
.monokai .py { color: #F8F8F2 } /* Name.Property */
.monokai .nt { color: #FF4689 } /* Name.Tag */
.monokai .nv { color: #F8F8F2 } /* Name.Variable */
.monokai .ow { color: #FF4689 } /* Operator.Word */
.monokai .pm { color: #F8F8F2 } /* Punctuation.Marker */
.monokai .w { color: #F8F8F2 } /* Text.Whitespace */
.monokai .mb { color: #AE81FF } /* Literal.Number.Bin */
.monokai .mf { color: #AE81FF } /* Literal.Number.Float */
.monokai .mh { color: #AE81FF } /* Literal.Number.Hex */
.monokai .mi { color: #AE81FF } /* Literal.Number.Integer */
.monokai .mo { color: #AE81FF } /* Literal.Number.Oct */
.monokai .sa { color: #E6DB74 } /* Literal.String.Affix */
.monokai .sb { color: #E6DB74 } /* Literal.String.Backtick */
.monokai .sc { color: #E6DB74 } /* Literal.String.Char */
.monokai .dl { color: #E6DB74 } /* Literal.String.Delimiter */
.monokai .sd { color: #E6DB74 } /* Literal.String.Doc */
.monokai .s2 { color: #E6DB74 } /* Literal.String.Double */
.monokai .se { color: #AE81FF } /* Literal.String.Escape */
.monokai .sh { color: #E6DB74 } /* Literal.String.Heredoc */
.monokai .si { color: #E6DB74 } /* Literal.String.Interpol */
.monokai .sx { color: #E6DB74 } /* Literal.String.Other */
.monokai .sr { color: #E6DB74 } /* Literal.String.Regex */
.monokai .s1 { color: #E6DB74 } /* Literal.String.Single */
.monokai .ss { color: #E6DB74 } /* Literal.String.Symbol */
.monokai .bp { color: #F8F8F2 } /* Name.Builtin.Pseudo */
.monokai .fm { color: #A6E22E } /* Name.Function.Magic */
.monokai .vc { color: #F8F8F2 } /* Name.Variable.Class */
.monokai .vg { color: #F8F8F2 } /* Name.Variable.Global */
.monokai .vi { color: #F8F8F2 } /* Name.Variable.Instance */
.monokai .vm { color: #F8F8F2 } /* Name.Variable.Magic */
.monokai .il { color: #AE81FF } /* Literal.Number.Integer.Long */</style>
<div class="monokai"><pre><span></span><span class="n">H1</span><span class="p">(</span><span class="s2">&quot;Hi&quot;</span><span class="p">)</span>
</pre></div>
</div>




### Use Mistletoe for Markdown Cells


```python
nb.cells[4]
```




```json
{ 'cell_type': 'markdown',
  'id': 'b91fdff1',
  'idx_': 4,
  'metadata': {},
  'source': '[MonsterUI Buttons and '
            'Links](https://audrey.feldroy.com/nbs/2025-01-22-MonsterUI-Buttons-and-Links) '
            'is the notebook with the problem.\n'
            '\n'
            'Let\'s start with a subset of the problem: the H1 text "MonsterUI '
            'Buttons and Links" is showing up as normal text.'}
```




```python
#| export
def StyledMd(m):
    return Safe(mistletoe.markdown(m))
```


```python
HTML(StyledMd(nb.cells[4].source))
```




<p><a href="https://audrey.feldroy.com/nbs/2025-01-22-MonsterUI-Buttons-and-Links">MonsterUI Buttons and Links</a> is the notebook with the problem.</p>
<p>Let's start with a subset of the problem: the H1 text "MonsterUI Buttons and Links" is showing up as normal text.</p>




### Use Mistletoe for Output Data of Code Cells


```python
HTML(to_xml(StyledMd(nb.cells[5].outputs[0].data["text/markdown"])))
```




<pre><code class="language-html">&lt;h1 class="uk-h1 "&gt;Hi&lt;/h1&gt;

</code></pre>





```python
#| export
def StyledCell(c):
    if c.cell_type == "markdown": return StyledMd(c.source)
    if c.cell_type == "code": 
        if not c.outputs: return StyledCode(c.source)
        return StyledCode(c.source), render_code_output(c)
```


```python
L(nb.cells).map(StyledCell)
```




    (#7) ['<h1>Troubleshooting MonsterUI on This Site</h1>\n',"<p>My first MonsterUI notebook isn't rendering correctly. Here I debug it.</p>\n",div((style(('pre { line-height: 125%; }\ntd.linenos .normal { color: inherit; background-color: transparent; padding-left: 5px; padding-right: 5px; }\nspan.linenos { color: inherit; background-color: transparent; padding-left: 5px; padding-right: 5px; }\ntd.linenos .special { color: #000000; background-color: #ffffc0; padding-left: 5px; padding-right: 5px; }\nspan.linenos.special { color: #000000; background-color: #ffffc0; padding-left: 5px; padding-right: 5px; }\n.monokai .hll { background-color: #49483e }\n.monokai { background: #272822; color: #F8F8F2 }\n.monokai .c { color: #959077 } /* Comment */\n.monokai .err { color: #ED007E; background-color: #1E0010 } /* Error */\n.monokai .esc { color: #F8F8F2 } /* Escape */\n.monokai .g { color: #F8F8F2 } /* Generic */\n.monokai .k { color: #66D9EF } /* Keyword */\n.monokai .l { color: #AE81FF } /* Literal */\n.monokai .n { color: #F8F8F2 } /* Name */\n.monokai .o { color: #FF4689 } /* Operator */\n.monokai .x { color: #F8F8F2 } /* Other */\n.monokai .p { color: #F8F8F2 } /* Punctuation */\n.monokai .ch { color: #959077 } /* Comment.Hashbang */\n.monokai .cm { color: #959077 } /* Comment.Multiline */\n.monokai .cp { color: #959077 } /* Comment.Preproc */\n.monokai .cpf { color: #959077 } /* Comment.PreprocFile */\n.monokai .c1 { color: #959077 } /* Comment.Single */\n.monokai .cs { color: #959077 } /* Comment.Special */\n.monokai .gd { color: #FF4689 } /* Generic.Deleted */\n.monokai .ge { color: #F8F8F2; font-style: italic } /* Generic.Emph */\n.monokai .ges { color: #F8F8F2; font-weight: bold; font-style: italic } /* Generic.EmphStrong */\n.monokai .gr { color: #F8F8F2 } /* Generic.Error */\n.monokai .gh { color: #F8F8F2 } /* Generic.Heading */\n.monokai .gi { color: #A6E22E } /* Generic.Inserted */\n.monokai .go { color: #66D9EF } /* Generic.Output */\n.monokai .gp { color: #FF4689; font-weight: bold } /* Generic.Prompt */\n.monokai .gs { color: #F8F8F2; font-weight: bold } /* Generic.Strong */\n.monokai .gu { color: #959077 } /* Generic.Subheading */\n.monokai .gt { color: #F8F8F2 } /* Generic.Traceback */\n.monokai .kc { color: #66D9EF } /* Keyword.Constant */\n.monokai .kd { color: #66D9EF } /* Keyword.Declaration */\n.monokai .kn { color: #FF4689 } /* Keyword.Namespace */\n.monokai .kp { color: #66D9EF } /* Keyword.Pseudo */\n.monokai .kr { color: #66D9EF } /* Keyword.Reserved */\n.monokai .kt { color: #66D9EF } /* Keyword.Type */\n.monokai .ld { color: #E6DB74 } /* Literal.Date */\n.monokai .m { color: #AE81FF } /* Literal.Number */\n.monokai .s { color: #E6DB74 } /* Literal.String */\n.monokai .na { color: #A6E22E } /* Name.Attribute */\n.monokai .nb { color: #F8F8F2 } /* Name.Builtin */\n.monokai .nc { color: #A6E22E } /* Name.Class */\n.monokai .no { color: #66D9EF } /* Name.Constant */\n.monokai .nd { color: #A6E22E } /* Name.Decorator */\n.monokai .ni { color: #F8F8F2 } /* Name.Entity */\n.monokai .ne { color: #A6E22E } /* Name.Exception */\n.monokai .nf { color: #A6E22E } /* Name.Function */\n.monokai .nl { color: #F8F8F2 } /* Name.Label */\n.monokai .nn { color: #F8F8F2 } /* Name.Namespace */\n.monokai .nx { color: #A6E22E } /* Name.Other */\n.monokai .py { color: #F8F8F2 } /* Name.Property */\n.monokai .nt { color: #FF4689 } /* Name.Tag */\n.monokai .nv { color: #F8F8F2 } /* Name.Variable */\n.monokai .ow { color: #FF4689 } /* Operator.Word */\n.monokai .pm { color: #F8F8F2 } /* Punctuation.Marker */\n.monokai .w { color: #F8F8F2 } /* Text.Whitespace */\n.monokai .mb { color: #AE81FF } /* Literal.Number.Bin */\n.monokai .mf { color: #AE81FF } /* Literal.Number.Float */\n.monokai .mh { color: #AE81FF } /* Literal.Number.Hex */\n.monokai .mi { color: #AE81FF } /* Literal.Number.Integer */\n.monokai .mo { color: #AE81FF } /* Literal.Number.Oct */\n.monokai .sa { color: #E6DB74 } /* Literal.String.Affix */\n.monokai .sb { color: #E6DB74 } /* Literal.String.Backtick */\n.monokai .sc { color: #E6DB74 } /* Literal.String.Char */\n.monokai .dl { color: #E6DB74 } /* Literal.String.Delimiter */\n.monokai .sd { color: #E6DB74 } /* Literal.String.Doc */\n.monokai .s2 { color: #E6DB74 } /* Literal.String.Double */\n.monokai .se { color: #AE81FF } /* Literal.String.Escape */\n.monokai .sh { color: #E6DB74 } /* Literal.String.Heredoc */\n.monokai .si { color: #E6DB74 } /* Literal.String.Interpol */\n.monokai .sx { color: #E6DB74 } /* Literal.String.Other */\n.monokai .sr { color: #E6DB74 } /* Literal.String.Regex */\n.monokai .s1 { color: #E6DB74 } /* Literal.String.Single */\n.monokai .ss { color: #E6DB74 } /* Literal.String.Symbol */\n.monokai .bp { color: #F8F8F2 } /* Name.Builtin.Pseudo */\n.monokai .fm { color: #A6E22E } /* Name.Function.Magic */\n.monokai .vc { color: #F8F8F2 } /* Name.Variable.Class */\n.monokai .vg { color: #F8F8F2 } /* Name.Variable.Global */\n.monokai .vi { color: #F8F8F2 } /* Name.Variable.Instance */\n.monokai .vm { color: #F8F8F2 } /* Name.Variable.Magic */\n.monokai .il { color: #AE81FF } /* Literal.Number.Integer.Long */',),{}), '<div class="monokai"><pre><span></span><span class="kn">from</span><span class="w"> </span><span class="nn">fasthtml.common</span><span class="w"> </span><span class="kn">import</span> <span class="o">*</span>\n<span class="kn">from</span><span class="w"> </span><span class="nn">monsterui.all</span><span class="w"> </span><span class="kn">import</span> <span class="o">*</span>\n</pre></div>\n'),{'id': 'monokai'}),'<h2>Understand the Problem</h2>\n','<p><a href="https://audrey.feldroy.com/nbs/2025-01-22-MonsterUI-Buttons-and-Links">MonsterUI Buttons and Links</a> is the notebook with the problem.</p>\n<p>Let\'s start with a subset of the problem: the H1 text "MonsterUI Buttons and Links" is showing up as normal text.</p>\n',(div((style(('pre { line-height: 125%; }\ntd.linenos .normal { color: inherit; background-color: transparent; padding-left: 5px; padding-right: 5px; }\nspan.linenos { color: inherit; background-color: transparent; padding-left: 5px; padding-right: 5px; }\ntd.linenos .special { color: #000000; background-color: #ffffc0; padding-left: 5px; padding-right: 5px; }\nspan.linenos.special { color: #000000; background-color: #ffffc0; padding-left: 5px; padding-right: 5px; }\n.monokai .hll { background-color: #49483e }\n.monokai { background: #272822; color: #F8F8F2 }\n.monokai .c { color: #959077 } /* Comment */\n.monokai .err { color: #ED007E; background-color: #1E0010 } /* Error */\n.monokai .esc { color: #F8F8F2 } /* Escape */\n.monokai .g { color: #F8F8F2 } /* Generic */\n.monokai .k { color: #66D9EF } /* Keyword */\n.monokai .l { color: #AE81FF } /* Literal */\n.monokai .n { color: #F8F8F2 } /* Name */\n.monokai .o { color: #FF4689 } /* Operator */\n.monokai .x { color: #F8F8F2 } /* Other */\n.monokai .p { color: #F8F8F2 } /* Punctuation */\n.monokai .ch { color: #959077 } /* Comment.Hashbang */\n.monokai .cm { color: #959077 } /* Comment.Multiline */\n.monokai .cp { color: #959077 } /* Comment.Preproc */\n.monokai .cpf { color: #959077 } /* Comment.PreprocFile */\n.monokai .c1 { color: #959077 } /* Comment.Single */\n.monokai .cs { color: #959077 } /* Comment.Special */\n.monokai .gd { color: #FF4689 } /* Generic.Deleted */\n.monokai .ge { color: #F8F8F2; font-style: italic } /* Generic.Emph */\n.monokai .ges { color: #F8F8F2; font-weight: bold; font-style: italic } /* Generic.EmphStrong */\n.monokai .gr { color: #F8F8F2 } /* Generic.Error */\n.monokai .gh { color: #F8F8F2 } /* Generic.Heading */\n.monokai .gi { color: #A6E22E } /* Generic.Inserted */\n.monokai .go { color: #66D9EF } /* Generic.Output */\n.monokai .gp { color: #FF4689; font-weight: bold } /* Generic.Prompt */\n.monokai .gs { color: #F8F8F2; font-weight: bold } /* Generic.Strong */\n.monokai .gu { color: #959077 } /* Generic.Subheading */\n.monokai .gt { color: #F8F8F2 } /* Generic.Traceback */\n.monokai .kc { color: #66D9EF } /* Keyword.Constant */\n.monokai .kd { color: #66D9EF } /* Keyword.Declaration */\n.monokai .kn { color: #FF4689 } /* Keyword.Namespace */\n.monokai .kp { color: #66D9EF } /* Keyword.Pseudo */\n.monokai .kr { color: #66D9EF } /* Keyword.Reserved */\n.monokai .kt { color: #66D9EF } /* Keyword.Type */\n.monokai .ld { color: #E6DB74 } /* Literal.Date */\n.monokai .m { color: #AE81FF } /* Literal.Number */\n.monokai .s { color: #E6DB74 } /* Literal.String */\n.monokai .na { color: #A6E22E } /* Name.Attribute */\n.monokai .nb { color: #F8F8F2 } /* Name.Builtin */\n.monokai .nc { color: #A6E22E } /* Name.Class */\n.monokai .no { color: #66D9EF } /* Name.Constant */\n.monokai .nd { color: #A6E22E } /* Name.Decorator */\n.monokai .ni { color: #F8F8F2 } /* Name.Entity */\n.monokai .ne { color: #A6E22E } /* Name.Exception */\n.monokai .nf { color: #A6E22E } /* Name.Function */\n.monokai .nl { color: #F8F8F2 } /* Name.Label */\n.monokai .nn { color: #F8F8F2 } /* Name.Namespace */\n.monokai .nx { color: #A6E22E } /* Name.Other */\n.monokai .py { color: #F8F8F2 } /* Name.Property */\n.monokai .nt { color: #FF4689 } /* Name.Tag */\n.monokai .nv { color: #F8F8F2 } /* Name.Variable */\n.monokai .ow { color: #FF4689 } /* Operator.Word */\n.monokai .pm { color: #F8F8F2 } /* Punctuation.Marker */\n.monokai .w { color: #F8F8F2 } /* Text.Whitespace */\n.monokai .mb { color: #AE81FF } /* Literal.Number.Bin */\n.monokai .mf { color: #AE81FF } /* Literal.Number.Float */\n.monokai .mh { color: #AE81FF } /* Literal.Number.Hex */\n.monokai .mi { color: #AE81FF } /* Literal.Number.Integer */\n.monokai .mo { color: #AE81FF } /* Literal.Number.Oct */\n.monokai .sa { color: #E6DB74 } /* Literal.String.Affix */\n.monokai .sb { color: #E6DB74 } /* Literal.String.Backtick */\n.monokai .sc { color: #E6DB74 } /* Literal.String.Char */\n.monokai .dl { color: #E6DB74 } /* Literal.String.Delimiter */\n.monokai .sd { color: #E6DB74 } /* Literal.String.Doc */\n.monokai .s2 { color: #E6DB74 } /* Literal.String.Double */\n.monokai .se { color: #AE81FF } /* Literal.String.Escape */\n.monokai .sh { color: #E6DB74 } /* Literal.String.Heredoc */\n.monokai .si { color: #E6DB74 } /* Literal.String.Interpol */\n.monokai .sx { color: #E6DB74 } /* Literal.String.Other */\n.monokai .sr { color: #E6DB74 } /* Literal.String.Regex */\n.monokai .s1 { color: #E6DB74 } /* Literal.String.Single */\n.monokai .ss { color: #E6DB74 } /* Literal.String.Symbol */\n.monokai .bp { color: #F8F8F2 } /* Name.Builtin.Pseudo */\n.monokai .fm { color: #A6E22E } /* Name.Function.Magic */\n.monokai .vc { color: #F8F8F2 } /* Name.Variable.Class */\n.monokai .vg { color: #F8F8F2 } /* Name.Variable.Global */\n.monokai .vi { color: #F8F8F2 } /* Name.Variable.Instance */\n.monokai .vm { color: #F8F8F2 } /* Name.Variable.Magic */\n.monokai .il { color: #AE81FF } /* Literal.Number.Integer.Long */',),{}), '<div class="monokai"><pre><span></span><span class="n">H1</span><span class="p">(</span><span class="s2">&quot;Hi&quot;</span><span class="p">)</span>\n</pre></div>\n'),{'id': 'monokai'}), footer(('<pre><code class="language-html">&lt;h1 class="uk-h1 "&gt;Hi&lt;/h1&gt;\n\n</code></pre>\n',),{})),(div((style(('pre { line-height: 125%; }\ntd.linenos .normal { color: inherit; background-color: transparent; padding-left: 5px; padding-right: 5px; }\nspan.linenos { color: inherit; background-color: transparent; padding-left: 5px; padding-right: 5px; }\ntd.linenos .special { color: #000000; background-color: #ffffc0; padding-left: 5px; padding-right: 5px; }\nspan.linenos.special { color: #000000; background-color: #ffffc0; padding-left: 5px; padding-right: 5px; }\n.monokai .hll { background-color: #49483e }\n.monokai { background: #272822; color: #F8F8F2 }\n.monokai .c { color: #959077 } /* Comment */\n.monokai .err { color: #ED007E; background-color: #1E0010 } /* Error */\n.monokai .esc { color: #F8F8F2 } /* Escape */\n.monokai .g { color: #F8F8F2 } /* Generic */\n.monokai .k { color: #66D9EF } /* Keyword */\n.monokai .l { color: #AE81FF } /* Literal */\n.monokai .n { color: #F8F8F2 } /* Name */\n.monokai .o { color: #FF4689 } /* Operator */\n.monokai .x { color: #F8F8F2 } /* Other */\n.monokai .p { color: #F8F8F2 } /* Punctuation */\n.monokai .ch { color: #959077 } /* Comment.Hashbang */\n.monokai .cm { color: #959077 } /* Comment.Multiline */\n.monokai .cp { color: #959077 } /* Comment.Preproc */\n.monokai .cpf { color: #959077 } /* Comment.PreprocFile */\n.monokai .c1 { color: #959077 } /* Comment.Single */\n.monokai .cs { color: #959077 } /* Comment.Special */\n.monokai .gd { color: #FF4689 } /* Generic.Deleted */\n.monokai .ge { color: #F8F8F2; font-style: italic } /* Generic.Emph */\n.monokai .ges { color: #F8F8F2; font-weight: bold; font-style: italic } /* Generic.EmphStrong */\n.monokai .gr { color: #F8F8F2 } /* Generic.Error */\n.monokai .gh { color: #F8F8F2 } /* Generic.Heading */\n.monokai .gi { color: #A6E22E } /* Generic.Inserted */\n.monokai .go { color: #66D9EF } /* Generic.Output */\n.monokai .gp { color: #FF4689; font-weight: bold } /* Generic.Prompt */\n.monokai .gs { color: #F8F8F2; font-weight: bold } /* Generic.Strong */\n.monokai .gu { color: #959077 } /* Generic.Subheading */\n.monokai .gt { color: #F8F8F2 } /* Generic.Traceback */\n.monokai .kc { color: #66D9EF } /* Keyword.Constant */\n.monokai .kd { color: #66D9EF } /* Keyword.Declaration */\n.monokai .kn { color: #FF4689 } /* Keyword.Namespace */\n.monokai .kp { color: #66D9EF } /* Keyword.Pseudo */\n.monokai .kr { color: #66D9EF } /* Keyword.Reserved */\n.monokai .kt { color: #66D9EF } /* Keyword.Type */\n.monokai .ld { color: #E6DB74 } /* Literal.Date */\n.monokai .m { color: #AE81FF } /* Literal.Number */\n.monokai .s { color: #E6DB74 } /* Literal.String */\n.monokai .na { color: #A6E22E } /* Name.Attribute */\n.monokai .nb { color: #F8F8F2 } /* Name.Builtin */\n.monokai .nc { color: #A6E22E } /* Name.Class */\n.monokai .no { color: #66D9EF } /* Name.Constant */\n.monokai .nd { color: #A6E22E } /* Name.Decorator */\n.monokai .ni { color: #F8F8F2 } /* Name.Entity */\n.monokai .ne { color: #A6E22E } /* Name.Exception */\n.monokai .nf { color: #A6E22E } /* Name.Function */\n.monokai .nl { color: #F8F8F2 } /* Name.Label */\n.monokai .nn { color: #F8F8F2 } /* Name.Namespace */\n.monokai .nx { color: #A6E22E } /* Name.Other */\n.monokai .py { color: #F8F8F2 } /* Name.Property */\n.monokai .nt { color: #FF4689 } /* Name.Tag */\n.monokai .nv { color: #F8F8F2 } /* Name.Variable */\n.monokai .ow { color: #FF4689 } /* Operator.Word */\n.monokai .pm { color: #F8F8F2 } /* Punctuation.Marker */\n.monokai .w { color: #F8F8F2 } /* Text.Whitespace */\n.monokai .mb { color: #AE81FF } /* Literal.Number.Bin */\n.monokai .mf { color: #AE81FF } /* Literal.Number.Float */\n.monokai .mh { color: #AE81FF } /* Literal.Number.Hex */\n.monokai .mi { color: #AE81FF } /* Literal.Number.Integer */\n.monokai .mo { color: #AE81FF } /* Literal.Number.Oct */\n.monokai .sa { color: #E6DB74 } /* Literal.String.Affix */\n.monokai .sb { color: #E6DB74 } /* Literal.String.Backtick */\n.monokai .sc { color: #E6DB74 } /* Literal.String.Char */\n.monokai .dl { color: #E6DB74 } /* Literal.String.Delimiter */\n.monokai .sd { color: #E6DB74 } /* Literal.String.Doc */\n.monokai .s2 { color: #E6DB74 } /* Literal.String.Double */\n.monokai .se { color: #AE81FF } /* Literal.String.Escape */\n.monokai .sh { color: #E6DB74 } /* Literal.String.Heredoc */\n.monokai .si { color: #E6DB74 } /* Literal.String.Interpol */\n.monokai .sx { color: #E6DB74 } /* Literal.String.Other */\n.monokai .sr { color: #E6DB74 } /* Literal.String.Regex */\n.monokai .s1 { color: #E6DB74 } /* Literal.String.Single */\n.monokai .ss { color: #E6DB74 } /* Literal.String.Symbol */\n.monokai .bp { color: #F8F8F2 } /* Name.Builtin.Pseudo */\n.monokai .fm { color: #A6E22E } /* Name.Function.Magic */\n.monokai .vc { color: #F8F8F2 } /* Name.Variable.Class */\n.monokai .vg { color: #F8F8F2 } /* Name.Variable.Global */\n.monokai .vi { color: #F8F8F2 } /* Name.Variable.Instance */\n.monokai .vm { color: #F8F8F2 } /* Name.Variable.Magic */\n.monokai .il { color: #AE81FF } /* Literal.Number.Integer.Long */',),{}), '<div class="monokai"><pre><span></span><span class="n">A</span><span class="p">(</span><span class="s2">&quot;My Blog&quot;</span><span class="p">,</span> <span class="n">href</span><span class="o">=</span><span class="s2">&quot;https://audrey.feldroy.com&quot;</span><span class="p">)</span>\n</pre></div>\n'),{'id': 'monokai'}), footer(('<pre><code class="language-html">&lt;a href="https://audrey.feldroy.com"&gt;My Blog&lt;/a&gt;\n</code></pre>\n',),{}))]




```python
show(*L(nb.cells).map(StyledCell))
```


<h1>Troubleshooting MonsterUI on This Site</h1>
<p>My first MonsterUI notebook isn't rendering correctly. Here I debug it.</p>
<div id="monokai">
  <style>pre { line-height: 125%; }
td.linenos .normal { color: inherit; background-color: transparent; padding-left: 5px; padding-right: 5px; }
span.linenos { color: inherit; background-color: transparent; padding-left: 5px; padding-right: 5px; }
td.linenos .special { color: #000000; background-color: #ffffc0; padding-left: 5px; padding-right: 5px; }
span.linenos.special { color: #000000; background-color: #ffffc0; padding-left: 5px; padding-right: 5px; }
.monokai .hll { background-color: #49483e }
.monokai { background: #272822; color: #F8F8F2 }
.monokai .c { color: #959077 } /* Comment */
.monokai .err { color: #ED007E; background-color: #1E0010 } /* Error */
.monokai .esc { color: #F8F8F2 } /* Escape */
.monokai .g { color: #F8F8F2 } /* Generic */
.monokai .k { color: #66D9EF } /* Keyword */
.monokai .l { color: #AE81FF } /* Literal */
.monokai .n { color: #F8F8F2 } /* Name */
.monokai .o { color: #FF4689 } /* Operator */
.monokai .x { color: #F8F8F2 } /* Other */
.monokai .p { color: #F8F8F2 } /* Punctuation */
.monokai .ch { color: #959077 } /* Comment.Hashbang */
.monokai .cm { color: #959077 } /* Comment.Multiline */
.monokai .cp { color: #959077 } /* Comment.Preproc */
.monokai .cpf { color: #959077 } /* Comment.PreprocFile */
.monokai .c1 { color: #959077 } /* Comment.Single */
.monokai .cs { color: #959077 } /* Comment.Special */
.monokai .gd { color: #FF4689 } /* Generic.Deleted */
.monokai .ge { color: #F8F8F2; font-style: italic } /* Generic.Emph */
.monokai .ges { color: #F8F8F2; font-weight: bold; font-style: italic } /* Generic.EmphStrong */
.monokai .gr { color: #F8F8F2 } /* Generic.Error */
.monokai .gh { color: #F8F8F2 } /* Generic.Heading */
.monokai .gi { color: #A6E22E } /* Generic.Inserted */
.monokai .go { color: #66D9EF } /* Generic.Output */
.monokai .gp { color: #FF4689; font-weight: bold } /* Generic.Prompt */
.monokai .gs { color: #F8F8F2; font-weight: bold } /* Generic.Strong */
.monokai .gu { color: #959077 } /* Generic.Subheading */
.monokai .gt { color: #F8F8F2 } /* Generic.Traceback */
.monokai .kc { color: #66D9EF } /* Keyword.Constant */
.monokai .kd { color: #66D9EF } /* Keyword.Declaration */
.monokai .kn { color: #FF4689 } /* Keyword.Namespace */
.monokai .kp { color: #66D9EF } /* Keyword.Pseudo */
.monokai .kr { color: #66D9EF } /* Keyword.Reserved */
.monokai .kt { color: #66D9EF } /* Keyword.Type */
.monokai .ld { color: #E6DB74 } /* Literal.Date */
.monokai .m { color: #AE81FF } /* Literal.Number */
.monokai .s { color: #E6DB74 } /* Literal.String */
.monokai .na { color: #A6E22E } /* Name.Attribute */
.monokai .nb { color: #F8F8F2 } /* Name.Builtin */
.monokai .nc { color: #A6E22E } /* Name.Class */
.monokai .no { color: #66D9EF } /* Name.Constant */
.monokai .nd { color: #A6E22E } /* Name.Decorator */
.monokai .ni { color: #F8F8F2 } /* Name.Entity */
.monokai .ne { color: #A6E22E } /* Name.Exception */
.monokai .nf { color: #A6E22E } /* Name.Function */
.monokai .nl { color: #F8F8F2 } /* Name.Label */
.monokai .nn { color: #F8F8F2 } /* Name.Namespace */
.monokai .nx { color: #A6E22E } /* Name.Other */
.monokai .py { color: #F8F8F2 } /* Name.Property */
.monokai .nt { color: #FF4689 } /* Name.Tag */
.monokai .nv { color: #F8F8F2 } /* Name.Variable */
.monokai .ow { color: #FF4689 } /* Operator.Word */
.monokai .pm { color: #F8F8F2 } /* Punctuation.Marker */
.monokai .w { color: #F8F8F2 } /* Text.Whitespace */
.monokai .mb { color: #AE81FF } /* Literal.Number.Bin */
.monokai .mf { color: #AE81FF } /* Literal.Number.Float */
.monokai .mh { color: #AE81FF } /* Literal.Number.Hex */
.monokai .mi { color: #AE81FF } /* Literal.Number.Integer */
.monokai .mo { color: #AE81FF } /* Literal.Number.Oct */
.monokai .sa { color: #E6DB74 } /* Literal.String.Affix */
.monokai .sb { color: #E6DB74 } /* Literal.String.Backtick */
.monokai .sc { color: #E6DB74 } /* Literal.String.Char */
.monokai .dl { color: #E6DB74 } /* Literal.String.Delimiter */
.monokai .sd { color: #E6DB74 } /* Literal.String.Doc */
.monokai .s2 { color: #E6DB74 } /* Literal.String.Double */
.monokai .se { color: #AE81FF } /* Literal.String.Escape */
.monokai .sh { color: #E6DB74 } /* Literal.String.Heredoc */
.monokai .si { color: #E6DB74 } /* Literal.String.Interpol */
.monokai .sx { color: #E6DB74 } /* Literal.String.Other */
.monokai .sr { color: #E6DB74 } /* Literal.String.Regex */
.monokai .s1 { color: #E6DB74 } /* Literal.String.Single */
.monokai .ss { color: #E6DB74 } /* Literal.String.Symbol */
.monokai .bp { color: #F8F8F2 } /* Name.Builtin.Pseudo */
.monokai .fm { color: #A6E22E } /* Name.Function.Magic */
.monokai .vc { color: #F8F8F2 } /* Name.Variable.Class */
.monokai .vg { color: #F8F8F2 } /* Name.Variable.Global */
.monokai .vi { color: #F8F8F2 } /* Name.Variable.Instance */
.monokai .vm { color: #F8F8F2 } /* Name.Variable.Magic */
.monokai .il { color: #AE81FF } /* Literal.Number.Integer.Long */</style>
<div class="monokai"><pre><span></span><span class="kn">from</span><span class="w"> </span><span class="nn">fasthtml.common</span><span class="w"> </span><span class="kn">import</span> <span class="o">*</span>
<span class="kn">from</span><span class="w"> </span><span class="nn">monsterui.all</span><span class="w"> </span><span class="kn">import</span> <span class="o">*</span>
</pre></div>
</div>
<h2>Understand the Problem</h2>
<p><a href="https://audrey.feldroy.com/nbs/2025-01-22-MonsterUI-Buttons-and-Links">MonsterUI Buttons and Links</a> is the notebook with the problem.</p>
<p>Let's start with a subset of the problem: the H1 text "MonsterUI Buttons and Links" is showing up as normal text.</p>
<div id="monokai">
  <style>pre { line-height: 125%; }
td.linenos .normal { color: inherit; background-color: transparent; padding-left: 5px; padding-right: 5px; }
span.linenos { color: inherit; background-color: transparent; padding-left: 5px; padding-right: 5px; }
td.linenos .special { color: #000000; background-color: #ffffc0; padding-left: 5px; padding-right: 5px; }
span.linenos.special { color: #000000; background-color: #ffffc0; padding-left: 5px; padding-right: 5px; }
.monokai .hll { background-color: #49483e }
.monokai { background: #272822; color: #F8F8F2 }
.monokai .c { color: #959077 } /* Comment */
.monokai .err { color: #ED007E; background-color: #1E0010 } /* Error */
.monokai .esc { color: #F8F8F2 } /* Escape */
.monokai .g { color: #F8F8F2 } /* Generic */
.monokai .k { color: #66D9EF } /* Keyword */
.monokai .l { color: #AE81FF } /* Literal */
.monokai .n { color: #F8F8F2 } /* Name */
.monokai .o { color: #FF4689 } /* Operator */
.monokai .x { color: #F8F8F2 } /* Other */
.monokai .p { color: #F8F8F2 } /* Punctuation */
.monokai .ch { color: #959077 } /* Comment.Hashbang */
.monokai .cm { color: #959077 } /* Comment.Multiline */
.monokai .cp { color: #959077 } /* Comment.Preproc */
.monokai .cpf { color: #959077 } /* Comment.PreprocFile */
.monokai .c1 { color: #959077 } /* Comment.Single */
.monokai .cs { color: #959077 } /* Comment.Special */
.monokai .gd { color: #FF4689 } /* Generic.Deleted */
.monokai .ge { color: #F8F8F2; font-style: italic } /* Generic.Emph */
.monokai .ges { color: #F8F8F2; font-weight: bold; font-style: italic } /* Generic.EmphStrong */
.monokai .gr { color: #F8F8F2 } /* Generic.Error */
.monokai .gh { color: #F8F8F2 } /* Generic.Heading */
.monokai .gi { color: #A6E22E } /* Generic.Inserted */
.monokai .go { color: #66D9EF } /* Generic.Output */
.monokai .gp { color: #FF4689; font-weight: bold } /* Generic.Prompt */
.monokai .gs { color: #F8F8F2; font-weight: bold } /* Generic.Strong */
.monokai .gu { color: #959077 } /* Generic.Subheading */
.monokai .gt { color: #F8F8F2 } /* Generic.Traceback */
.monokai .kc { color: #66D9EF } /* Keyword.Constant */
.monokai .kd { color: #66D9EF } /* Keyword.Declaration */
.monokai .kn { color: #FF4689 } /* Keyword.Namespace */
.monokai .kp { color: #66D9EF } /* Keyword.Pseudo */
.monokai .kr { color: #66D9EF } /* Keyword.Reserved */
.monokai .kt { color: #66D9EF } /* Keyword.Type */
.monokai .ld { color: #E6DB74 } /* Literal.Date */
.monokai .m { color: #AE81FF } /* Literal.Number */
.monokai .s { color: #E6DB74 } /* Literal.String */
.monokai .na { color: #A6E22E } /* Name.Attribute */
.monokai .nb { color: #F8F8F2 } /* Name.Builtin */
.monokai .nc { color: #A6E22E } /* Name.Class */
.monokai .no { color: #66D9EF } /* Name.Constant */
.monokai .nd { color: #A6E22E } /* Name.Decorator */
.monokai .ni { color: #F8F8F2 } /* Name.Entity */
.monokai .ne { color: #A6E22E } /* Name.Exception */
.monokai .nf { color: #A6E22E } /* Name.Function */
.monokai .nl { color: #F8F8F2 } /* Name.Label */
.monokai .nn { color: #F8F8F2 } /* Name.Namespace */
.monokai .nx { color: #A6E22E } /* Name.Other */
.monokai .py { color: #F8F8F2 } /* Name.Property */
.monokai .nt { color: #FF4689 } /* Name.Tag */
.monokai .nv { color: #F8F8F2 } /* Name.Variable */
.monokai .ow { color: #FF4689 } /* Operator.Word */
.monokai .pm { color: #F8F8F2 } /* Punctuation.Marker */
.monokai .w { color: #F8F8F2 } /* Text.Whitespace */
.monokai .mb { color: #AE81FF } /* Literal.Number.Bin */
.monokai .mf { color: #AE81FF } /* Literal.Number.Float */
.monokai .mh { color: #AE81FF } /* Literal.Number.Hex */
.monokai .mi { color: #AE81FF } /* Literal.Number.Integer */
.monokai .mo { color: #AE81FF } /* Literal.Number.Oct */
.monokai .sa { color: #E6DB74 } /* Literal.String.Affix */
.monokai .sb { color: #E6DB74 } /* Literal.String.Backtick */
.monokai .sc { color: #E6DB74 } /* Literal.String.Char */
.monokai .dl { color: #E6DB74 } /* Literal.String.Delimiter */
.monokai .sd { color: #E6DB74 } /* Literal.String.Doc */
.monokai .s2 { color: #E6DB74 } /* Literal.String.Double */
.monokai .se { color: #AE81FF } /* Literal.String.Escape */
.monokai .sh { color: #E6DB74 } /* Literal.String.Heredoc */
.monokai .si { color: #E6DB74 } /* Literal.String.Interpol */
.monokai .sx { color: #E6DB74 } /* Literal.String.Other */
.monokai .sr { color: #E6DB74 } /* Literal.String.Regex */
.monokai .s1 { color: #E6DB74 } /* Literal.String.Single */
.monokai .ss { color: #E6DB74 } /* Literal.String.Symbol */
.monokai .bp { color: #F8F8F2 } /* Name.Builtin.Pseudo */
.monokai .fm { color: #A6E22E } /* Name.Function.Magic */
.monokai .vc { color: #F8F8F2 } /* Name.Variable.Class */
.monokai .vg { color: #F8F8F2 } /* Name.Variable.Global */
.monokai .vi { color: #F8F8F2 } /* Name.Variable.Instance */
.monokai .vm { color: #F8F8F2 } /* Name.Variable.Magic */
.monokai .il { color: #AE81FF } /* Literal.Number.Integer.Long */</style>
<div class="monokai"><pre><span></span><span class="n">H1</span><span class="p">(</span><span class="s2">&quot;Hi&quot;</span><span class="p">)</span>
</pre></div>
</div>
<footer><pre><code class="language-html">&lt;h1 class="uk-h1 "&gt;Hi&lt;/h1&gt;

</code></pre>
</footer>
<div id="monokai">
  <style>pre { line-height: 125%; }
td.linenos .normal { color: inherit; background-color: transparent; padding-left: 5px; padding-right: 5px; }
span.linenos { color: inherit; background-color: transparent; padding-left: 5px; padding-right: 5px; }
td.linenos .special { color: #000000; background-color: #ffffc0; padding-left: 5px; padding-right: 5px; }
span.linenos.special { color: #000000; background-color: #ffffc0; padding-left: 5px; padding-right: 5px; }
.monokai .hll { background-color: #49483e }
.monokai { background: #272822; color: #F8F8F2 }
.monokai .c { color: #959077 } /* Comment */
.monokai .err { color: #ED007E; background-color: #1E0010 } /* Error */
.monokai .esc { color: #F8F8F2 } /* Escape */
.monokai .g { color: #F8F8F2 } /* Generic */
.monokai .k { color: #66D9EF } /* Keyword */
.monokai .l { color: #AE81FF } /* Literal */
.monokai .n { color: #F8F8F2 } /* Name */
.monokai .o { color: #FF4689 } /* Operator */
.monokai .x { color: #F8F8F2 } /* Other */
.monokai .p { color: #F8F8F2 } /* Punctuation */
.monokai .ch { color: #959077 } /* Comment.Hashbang */
.monokai .cm { color: #959077 } /* Comment.Multiline */
.monokai .cp { color: #959077 } /* Comment.Preproc */
.monokai .cpf { color: #959077 } /* Comment.PreprocFile */
.monokai .c1 { color: #959077 } /* Comment.Single */
.monokai .cs { color: #959077 } /* Comment.Special */
.monokai .gd { color: #FF4689 } /* Generic.Deleted */
.monokai .ge { color: #F8F8F2; font-style: italic } /* Generic.Emph */
.monokai .ges { color: #F8F8F2; font-weight: bold; font-style: italic } /* Generic.EmphStrong */
.monokai .gr { color: #F8F8F2 } /* Generic.Error */
.monokai .gh { color: #F8F8F2 } /* Generic.Heading */
.monokai .gi { color: #A6E22E } /* Generic.Inserted */
.monokai .go { color: #66D9EF } /* Generic.Output */
.monokai .gp { color: #FF4689; font-weight: bold } /* Generic.Prompt */
.monokai .gs { color: #F8F8F2; font-weight: bold } /* Generic.Strong */
.monokai .gu { color: #959077 } /* Generic.Subheading */
.monokai .gt { color: #F8F8F2 } /* Generic.Traceback */
.monokai .kc { color: #66D9EF } /* Keyword.Constant */
.monokai .kd { color: #66D9EF } /* Keyword.Declaration */
.monokai .kn { color: #FF4689 } /* Keyword.Namespace */
.monokai .kp { color: #66D9EF } /* Keyword.Pseudo */
.monokai .kr { color: #66D9EF } /* Keyword.Reserved */
.monokai .kt { color: #66D9EF } /* Keyword.Type */
.monokai .ld { color: #E6DB74 } /* Literal.Date */
.monokai .m { color: #AE81FF } /* Literal.Number */
.monokai .s { color: #E6DB74 } /* Literal.String */
.monokai .na { color: #A6E22E } /* Name.Attribute */
.monokai .nb { color: #F8F8F2 } /* Name.Builtin */
.monokai .nc { color: #A6E22E } /* Name.Class */
.monokai .no { color: #66D9EF } /* Name.Constant */
.monokai .nd { color: #A6E22E } /* Name.Decorator */
.monokai .ni { color: #F8F8F2 } /* Name.Entity */
.monokai .ne { color: #A6E22E } /* Name.Exception */
.monokai .nf { color: #A6E22E } /* Name.Function */
.monokai .nl { color: #F8F8F2 } /* Name.Label */
.monokai .nn { color: #F8F8F2 } /* Name.Namespace */
.monokai .nx { color: #A6E22E } /* Name.Other */
.monokai .py { color: #F8F8F2 } /* Name.Property */
.monokai .nt { color: #FF4689 } /* Name.Tag */
.monokai .nv { color: #F8F8F2 } /* Name.Variable */
.monokai .ow { color: #FF4689 } /* Operator.Word */
.monokai .pm { color: #F8F8F2 } /* Punctuation.Marker */
.monokai .w { color: #F8F8F2 } /* Text.Whitespace */
.monokai .mb { color: #AE81FF } /* Literal.Number.Bin */
.monokai .mf { color: #AE81FF } /* Literal.Number.Float */
.monokai .mh { color: #AE81FF } /* Literal.Number.Hex */
.monokai .mi { color: #AE81FF } /* Literal.Number.Integer */
.monokai .mo { color: #AE81FF } /* Literal.Number.Oct */
.monokai .sa { color: #E6DB74 } /* Literal.String.Affix */
.monokai .sb { color: #E6DB74 } /* Literal.String.Backtick */
.monokai .sc { color: #E6DB74 } /* Literal.String.Char */
.monokai .dl { color: #E6DB74 } /* Literal.String.Delimiter */
.monokai .sd { color: #E6DB74 } /* Literal.String.Doc */
.monokai .s2 { color: #E6DB74 } /* Literal.String.Double */
.monokai .se { color: #AE81FF } /* Literal.String.Escape */
.monokai .sh { color: #E6DB74 } /* Literal.String.Heredoc */
.monokai .si { color: #E6DB74 } /* Literal.String.Interpol */
.monokai .sx { color: #E6DB74 } /* Literal.String.Other */
.monokai .sr { color: #E6DB74 } /* Literal.String.Regex */
.monokai .s1 { color: #E6DB74 } /* Literal.String.Single */
.monokai .ss { color: #E6DB74 } /* Literal.String.Symbol */
.monokai .bp { color: #F8F8F2 } /* Name.Builtin.Pseudo */
.monokai .fm { color: #A6E22E } /* Name.Function.Magic */
.monokai .vc { color: #F8F8F2 } /* Name.Variable.Class */
.monokai .vg { color: #F8F8F2 } /* Name.Variable.Global */
.monokai .vi { color: #F8F8F2 } /* Name.Variable.Instance */
.monokai .vm { color: #F8F8F2 } /* Name.Variable.Magic */
.monokai .il { color: #AE81FF } /* Literal.Number.Integer.Long */</style>
<div class="monokai"><pre><span></span><span class="n">A</span><span class="p">(</span><span class="s2">&quot;My Blog&quot;</span><span class="p">,</span> <span class="n">href</span><span class="o">=</span><span class="s2">&quot;https://audrey.feldroy.com&quot;</span><span class="p">)</span>
</pre></div>
</div>
<footer><pre><code class="language-html">&lt;a href="https://audrey.feldroy.com"&gt;My Blog&lt;/a&gt;
</code></pre>
</footer>
<script>if (window.htmx) htmx.process(document.body)</script>


## Notebook Detail Page


```python
#| export
@rt("/nbs/{name}")
def notebook(name:str):
    fpath = Path(f'nbs/{name}.ipynb')
    nb = read_nb(fpath)
    title = nb.cells[0].source.lstrip("# ")
    desc = nb.cells[1].source
    if "MonsterUI" in title:
        return (
            Theme.slate.headers(),
            franken.Container(
                franken.H1(title), # Title
                franken.P(desc), # Desc
                *L(nb.cells[2:]).map(StyledCell),
                cls="space-y-5"
            )
    )
    return (
        Style(':root {font-family: system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", sans-serif; color-scheme: light dark;} body {background-color: light-dark(#ffffff, #1a1a1a); color: light-dark(#1a1a1a, #ffffff);} p {line-height: 1.5;}'),
        Div(
            H1(title), # Title
            P(desc), # Desc
            *L(nb.cells[2:]).map(StyledCell),
            cls="space-y-5"
        )
    )
```

http://localhost:8000/nbs/2025-01-23-Troubleshooting-MonsterUI-on-This-Site


```python
name = "2025-01-23-Troubleshooting-MonsterUI-on-This-Site"
fpath = Path(f'{name}.ipynb')
fpath.absolute()
```




    Path('/Users/arg/fun/arg-blog-fasthtml/nbs/2025-01-23-Troubleshooting-MonsterUI-on-This-Site.ipynb')



## Troubleshooting the Troubleshooting MonsterUI Notebook


```python
def is_code_cell(c): return c.cell_type == "code"
cells = L(read_nb(nb_paths[1]).cells).filter(is_code_cell)
cells
```




    (#3) [{'cell_type': 'code', 'execution_count': 2, 'id': '8bff65e3', 'metadata': {}, 'outputs': [], 'source': 'from fasthtml.common import *\nfrom monsterui.all import *', 'idx_': 2},{'cell_type': 'code', 'execution_count': 3, 'id': 'cb344dfb', 'metadata': {}, 'outputs': [{'data': {'text/markdown': ['```html\n', '<h1 class="uk-h1 ">Hi</h1>\n', '\n', '```'], 'text/plain': ["h1(('Hi',),{'class': 'uk-h1 '})"]}, 'execution_count': 3, 'metadata': {}, 'output_type': 'execute_result'}], 'source': 'H1("Hi")', 'idx_': 5},{'cell_type': 'code', 'execution_count': 4, 'id': 'b86c1d3c', 'metadata': {}, 'outputs': [{'data': {'text/markdown': ['```html\n', '<a href="https://audrey.feldroy.com">My Blog</a>\n', '```'], 'text/plain': ["a(('My Blog',),{'href': 'https://audrey.feldroy.com'})"]}, 'execution_count': 4, 'metadata': {}, 'output_type': 'execute_result'}], 'source': 'A("My Blog", href="https://audrey.feldroy.com")', 'idx_': 6}]




```python
cells[1]
```




```json
{ 'cell_type': 'code',
  'execution_count': 3,
  'id': 'cb344dfb',
  'idx_': 5,
  'metadata': {},
  'outputs': [ { 'data': { 'text/markdown': [ '```html\n',
                                              '<h1 class="uk-h1 ">Hi</h1>\n',
                                              '\n',
                                              '```'],
                           'text/plain': ["h1(('Hi',),{'class': 'uk-h1 '})"]},
                 'execution_count': 3,
                 'metadata': {},
                 'output_type': 'execute_result'}],
  'source': 'H1("Hi")'}
```




```python
cells[1].outputs[0].data
```




```json
{ 'text/markdown': ['```html\n', '<h1 class="uk-h1 ">Hi</h1>\n', '\n', '```'],
  'text/plain': ["h1(('Hi',),{'class': 'uk-h1 '})"]}
```



## Troubleshooting the Cosine Similarity Notebook


```python
def is_code_cell(c): return c.cell_type == "code"
cells = L(read_nb(nb_paths[9]).cells).filter(is_code_cell)
cells[0]
```




```json
{ 'cell_type': 'code',
  'execution_count': 7,
  'id': '06004824',
  'idx_': 6,
  'metadata': {},
  'outputs': [ { 'data': { 'text/latex': [ '$$\\text{cos}(\\theta) = '
                                           '\\frac{\\mathbf{A} \\cdot '
                                           '\\mathbf{B}}{\\|\\mathbf{A}\\| '
                                           '\\|\\mathbf{B}\\|}$$\n'],
                           'text/plain': [ '<IPython.core.display.Latex '
                                           'object>']},
                 'metadata': {},
                 'output_type': 'display_data'}],
  'source': '%%latex\n'
            '$$\\text{cos}(\\theta) = \\frac{\\mathbf{A} \\cdot '
            '\\mathbf{B}}{\\|\\mathbf{A}\\| \\|\\mathbf{B}\\|}$$'}
```



## Rendering Code Outputs With render_code_output


```python
cells = L(read_nb(nb_paths[1]).cells).filter(is_code_cell)
cells[1]
```




```json
{ 'cell_type': 'code',
  'execution_count': 3,
  'id': 'cb344dfb',
  'idx_': 5,
  'metadata': {},
  'outputs': [ { 'data': { 'text/markdown': [ '```html\n',
                                              '<h1 class="uk-h1 ">Hi</h1>\n',
                                              '\n',
                                              '```'],
                           'text/plain': ["h1(('Hi',),{'class': 'uk-h1 '})"]},
                 'execution_count': 3,
                 'metadata': {},
                 'output_type': 'execute_result'}],
  'source': 'H1("Hi")'}
```




```python
render_code_output(cells[1])
```




```html
<footer><pre><code class="language-html">&lt;h1 class="uk-h1 "&gt;Hi&lt;/h1&gt;

</code></pre>
</footer>

```




```python
# show(*L(read_nb(nb_paths[4]).cells).map(StyledCell))
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
nb_export 2025-01-23-This-Site-Is-Now-Powered-by-This-Notebook.ipynb
mv main.py ..
```
