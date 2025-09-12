# Improving Pygments Code Block Display

Using Pygments, CSS and Ruff to improve how code blocks are displayed on my daily notebook blog.


```python
from execnb.nbio import read_nb
from fasthtml.common import *
from fasthtml.jupyter import JupyUvi
from fastcore.utils import L
import pygments
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter
```

## Listing My Notebooks' File Paths

My new favorite way of grabbing all my notebooks:

* Set `root` based on if I'm in a notebook or not. (`IN_NOTEBOOK` comes from `fasthtml.common`)
* Get a fastcore `L` list of my notebook paths sorted from newest to oldest


```python
root = Path() if IN_NOTEBOOK else Path("nbs/")
nb_paths = L(root.glob("*.ipynb")).sorted(reverse=True)
nb_paths
```




    (#50) [Path('2025-01-26-Improving-Pygments-Code-Block-Display.ipynb'),Path('2025-01-25-This-Site-Is-Now-Powered-by-This-Notebook-Part-2.ipynb'),Path('2025-01-24-Creating-In-Notebook-Images-for-Social-Media-With-PIL-Pillow.ipynb'),Path('2025-01-23-Troubleshooting-MonsterUI-on-This-Site.ipynb'),Path('2025-01-23-This-Site-Is-Now-Powered-by-This-Notebook.ipynb'),Path('2025-01-22-MonsterUI-Buttons-and-Links.ipynb'),Path('2025-01-22-Customizing-FastHTML-Headers-From-Notebook-Contents.ipynb'),Path('2025-01-21-SVG-Animation-in-FastHTML.ipynb'),Path('2025-01-20-Dark-and-Light-Mode-in-FastHTML.ipynb'),Path('2025-01-19-Genanki-and-fastcore.ipynb'),Path('2025-01-18-Alarm-Sounds-App.ipynb'),Path('2025-01-17-Alarm-Clock-Sounds.ipynb'),Path('2025-01-16-Cosine-Similarity-Breakdown-in-LaTeX.ipynb'),Path('2025-01-14-Constructing-SQLite-Tables-for-Notebooks-and-Search.ipynb'),Path('2025-01-13-SQLite-FTS5-Tokenizers-unicode61-and-ascii.ipynb'),Path('2025-01-12-A-Better-Notebook-Index-Page.ipynb'),Path('2025-01-11-NBClassic-Keyboard-Shortcuts-in-Command-and-Dual-Mode.ipynb'),Path('2025-01-10-Understanding-FastHTML-Routes-Requests-and-Redirects.ipynb'),Path('2025-01-09-Reading-and-Writing-Jupyter-Notebooks-With-Python.ipynb'),Path('2025-01-08-HTML-Title-Tag-in-FastHTML.ipynb')...]



## Get Sample Cells to Work With

Here I grab a specific cell of a notebook that looks good to play with.


```python
nb = read_nb(nb_paths[10])
```


```python
def is_code(c): return c.cell_type=='code'
c = L(nb.cells).filter(is_code)[3]
c
```




```json
{ 'cell_type': 'code',
  'execution_count': 16,
  'id': '00540ad9',
  'idx_': 10,
  'metadata': {},
  'outputs': [ { 'data': { 'text/plain': [ "(#3) [['Magandang hapon', 'Good "
                                           "afternoon'],['Magandang gabi', "
                                           "'Good evening'],['Paalam', "
                                           "'Goodbye']]"]},
                 'execution_count': 16,
                 'metadata': {},
                 'output_type': 'execute_result'}],
  'source': "notes = L(['Magandang hapon', 'Good afternoon'],\n"
            "    ['Magandang gabi', 'Good evening'],\n"
            "    ['Paalam', 'Goodbye'])\n"
            'notes'}
```



## Style the Cell

My FT function for styling cells that I built up to in [How I Fixed CSS Scope Leakage in Pygments Syntax Highlighting](https://audrey.feldroy.com/nbs/2024-12-27-CSS-Scope-Leakage-Pygments):


```python
def StyledCode(c, style='monokai'):
    "A notebook cell styled as code, with style name as its css class for scope limiting"
    fm = HtmlFormatter(style=style, cssclass=style)
    h = highlight(c, PythonLexer(), fm)
    sd = fm.get_style_defs(f".{style}")
    return Div(Style(sd), NotStr(h), id=style)
```


```python
show(StyledCode(c.source))
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
<div class="monokai"><pre><span></span><span class="n">notes</span> <span class="o">=</span> <span class="n">L</span><span class="p">([</span><span class="s1">&#39;Magandang hapon&#39;</span><span class="p">,</span> <span class="s1">&#39;Good afternoon&#39;</span><span class="p">],</span>
    <span class="p">[</span><span class="s1">&#39;Magandang gabi&#39;</span><span class="p">,</span> <span class="s1">&#39;Good evening&#39;</span><span class="p">],</span>
    <span class="p">[</span><span class="s1">&#39;Paalam&#39;</span><span class="p">,</span> <span class="s1">&#39;Goodbye&#39;</span><span class="p">])</span>
<span class="n">notes</span>
</pre></div>
</div>



## Pad the Cell

I just want to pad the top and bottom with 10 pixels here.


```python
def StyledCode(c, style='monokai'):
    "A notebook cell styled as code, with style name as its css class for scope limiting"
    fm = HtmlFormatter(style=style, cssclass=f"my-{style}", prestyles="padding:10px 0;")
    h = highlight(c, PythonLexer(), fm)
    sd = fm.get_style_defs(f".my-{style}")
    return Style(sd), NotStr(h)
```

Pygments lets you add inline styles to `<pre>`. That's nice.


```python
st, sc = StyledCode(c.source)
```


```python
Div(sc)
```




```html
<div><div class="my-monokai"><pre style="padding:10px 0;"><span></span><span class="n">notes</span> <span class="o">=</span> <span class="n">L</span><span class="p">([</span><span class="s1">&#39;Magandang hapon&#39;</span><span class="p">,</span> <span class="s1">&#39;Good afternoon&#39;</span><span class="p">],</span>
    <span class="p">[</span><span class="s1">&#39;Magandang gabi&#39;</span><span class="p">,</span> <span class="s1">&#39;Good evening&#39;</span><span class="p">],</span>
    <span class="p">[</span><span class="s1">&#39;Paalam&#39;</span><span class="p">,</span> <span class="s1">&#39;Goodbye&#39;</span><span class="p">])</span>
<span class="n">notes</span>
</pre></div>
</div>

```




```python
show(StyledCode(c.source))
```


<style>pre { line-height: 125%; }
td.linenos .normal { color: inherit; background-color: transparent; padding-left: 5px; padding-right: 5px; }
span.linenos { color: inherit; background-color: transparent; padding-left: 5px; padding-right: 5px; }
td.linenos .special { color: #000000; background-color: #ffffc0; padding-left: 5px; padding-right: 5px; }
span.linenos.special { color: #000000; background-color: #ffffc0; padding-left: 5px; padding-right: 5px; }
.my-monokai .hll { background-color: #49483e }
.my-monokai { background: #272822; color: #F8F8F2 }
.my-monokai .c { color: #959077 } /* Comment */
.my-monokai .err { color: #ED007E; background-color: #1E0010 } /* Error */
.my-monokai .esc { color: #F8F8F2 } /* Escape */
.my-monokai .g { color: #F8F8F2 } /* Generic */
.my-monokai .k { color: #66D9EF } /* Keyword */
.my-monokai .l { color: #AE81FF } /* Literal */
.my-monokai .n { color: #F8F8F2 } /* Name */
.my-monokai .o { color: #FF4689 } /* Operator */
.my-monokai .x { color: #F8F8F2 } /* Other */
.my-monokai .p { color: #F8F8F2 } /* Punctuation */
.my-monokai .ch { color: #959077 } /* Comment.Hashbang */
.my-monokai .cm { color: #959077 } /* Comment.Multiline */
.my-monokai .cp { color: #959077 } /* Comment.Preproc */
.my-monokai .cpf { color: #959077 } /* Comment.PreprocFile */
.my-monokai .c1 { color: #959077 } /* Comment.Single */
.my-monokai .cs { color: #959077 } /* Comment.Special */
.my-monokai .gd { color: #FF4689 } /* Generic.Deleted */
.my-monokai .ge { color: #F8F8F2; font-style: italic } /* Generic.Emph */
.my-monokai .ges { color: #F8F8F2; font-weight: bold; font-style: italic } /* Generic.EmphStrong */
.my-monokai .gr { color: #F8F8F2 } /* Generic.Error */
.my-monokai .gh { color: #F8F8F2 } /* Generic.Heading */
.my-monokai .gi { color: #A6E22E } /* Generic.Inserted */
.my-monokai .go { color: #66D9EF } /* Generic.Output */
.my-monokai .gp { color: #FF4689; font-weight: bold } /* Generic.Prompt */
.my-monokai .gs { color: #F8F8F2; font-weight: bold } /* Generic.Strong */
.my-monokai .gu { color: #959077 } /* Generic.Subheading */
.my-monokai .gt { color: #F8F8F2 } /* Generic.Traceback */
.my-monokai .kc { color: #66D9EF } /* Keyword.Constant */
.my-monokai .kd { color: #66D9EF } /* Keyword.Declaration */
.my-monokai .kn { color: #FF4689 } /* Keyword.Namespace */
.my-monokai .kp { color: #66D9EF } /* Keyword.Pseudo */
.my-monokai .kr { color: #66D9EF } /* Keyword.Reserved */
.my-monokai .kt { color: #66D9EF } /* Keyword.Type */
.my-monokai .ld { color: #E6DB74 } /* Literal.Date */
.my-monokai .m { color: #AE81FF } /* Literal.Number */
.my-monokai .s { color: #E6DB74 } /* Literal.String */
.my-monokai .na { color: #A6E22E } /* Name.Attribute */
.my-monokai .nb { color: #F8F8F2 } /* Name.Builtin */
.my-monokai .nc { color: #A6E22E } /* Name.Class */
.my-monokai .no { color: #66D9EF } /* Name.Constant */
.my-monokai .nd { color: #A6E22E } /* Name.Decorator */
.my-monokai .ni { color: #F8F8F2 } /* Name.Entity */
.my-monokai .ne { color: #A6E22E } /* Name.Exception */
.my-monokai .nf { color: #A6E22E } /* Name.Function */
.my-monokai .nl { color: #F8F8F2 } /* Name.Label */
.my-monokai .nn { color: #F8F8F2 } /* Name.Namespace */
.my-monokai .nx { color: #A6E22E } /* Name.Other */
.my-monokai .py { color: #F8F8F2 } /* Name.Property */
.my-monokai .nt { color: #FF4689 } /* Name.Tag */
.my-monokai .nv { color: #F8F8F2 } /* Name.Variable */
.my-monokai .ow { color: #FF4689 } /* Operator.Word */
.my-monokai .pm { color: #F8F8F2 } /* Punctuation.Marker */
.my-monokai .w { color: #F8F8F2 } /* Text.Whitespace */
.my-monokai .mb { color: #AE81FF } /* Literal.Number.Bin */
.my-monokai .mf { color: #AE81FF } /* Literal.Number.Float */
.my-monokai .mh { color: #AE81FF } /* Literal.Number.Hex */
.my-monokai .mi { color: #AE81FF } /* Literal.Number.Integer */
.my-monokai .mo { color: #AE81FF } /* Literal.Number.Oct */
.my-monokai .sa { color: #E6DB74 } /* Literal.String.Affix */
.my-monokai .sb { color: #E6DB74 } /* Literal.String.Backtick */
.my-monokai .sc { color: #E6DB74 } /* Literal.String.Char */
.my-monokai .dl { color: #E6DB74 } /* Literal.String.Delimiter */
.my-monokai .sd { color: #E6DB74 } /* Literal.String.Doc */
.my-monokai .s2 { color: #E6DB74 } /* Literal.String.Double */
.my-monokai .se { color: #AE81FF } /* Literal.String.Escape */
.my-monokai .sh { color: #E6DB74 } /* Literal.String.Heredoc */
.my-monokai .si { color: #E6DB74 } /* Literal.String.Interpol */
.my-monokai .sx { color: #E6DB74 } /* Literal.String.Other */
.my-monokai .sr { color: #E6DB74 } /* Literal.String.Regex */
.my-monokai .s1 { color: #E6DB74 } /* Literal.String.Single */
.my-monokai .ss { color: #E6DB74 } /* Literal.String.Symbol */
.my-monokai .bp { color: #F8F8F2 } /* Name.Builtin.Pseudo */
.my-monokai .fm { color: #A6E22E } /* Name.Function.Magic */
.my-monokai .vc { color: #F8F8F2 } /* Name.Variable.Class */
.my-monokai .vg { color: #F8F8F2 } /* Name.Variable.Global */
.my-monokai .vi { color: #F8F8F2 } /* Name.Variable.Instance */
.my-monokai .vm { color: #F8F8F2 } /* Name.Variable.Magic */
.my-monokai .il { color: #AE81FF } /* Literal.Number.Integer.Long */</style>
<div class="my-monokai"><pre style="padding:10px 0;"><span></span><span class="n">notes</span> <span class="o">=</span> <span class="n">L</span><span class="p">([</span><span class="s1">&#39;Magandang hapon&#39;</span><span class="p">,</span> <span class="s1">&#39;Good afternoon&#39;</span><span class="p">],</span>
    <span class="p">[</span><span class="s1">&#39;Magandang gabi&#39;</span><span class="p">,</span> <span class="s1">&#39;Good evening&#39;</span><span class="p">],</span>
    <span class="p">[</span><span class="s1">&#39;Paalam&#39;</span><span class="p">,</span> <span class="s1">&#39;Goodbye&#39;</span><span class="p">])</span>
<span class="n">notes</span>
</pre></div>



Success: the code is padded on top and bottom with 10px now.

## Limiting Line Length on Mobile Devices

On my phone I counted that 52 characters is the maximum I can read on a line of code, before having to scroll. Let's see if Ruff's textwrap breaks lines in a way that keeps Python code valid.


```python
def wrap_text(text, width=52):
    wrapper = textwrap.TextWrapper(width=width)
    wrapped_text = wrapper.fill(text)
    return wrapped_text
```


```python
wrapped_text = wrap_text(c.source)
print(wrapped_text)
```

    notes = L(['Magandang hapon', 'Good afternoon'],
    ['Magandang gabi', 'Good evening'],     ['Paalam',
    'Goodbye']) notes



```python
wrapped_text = wrap_text(c.source, width=43)
print(wrapped_text)
```

    notes = L(['Magandang hapon', 'Good
    afternoon'],     ['Magandang gabi', 'Good
    evening'],     ['Paalam', 'Goodbye']) notes


## Next Steps

If I continue this approach, the next steps will be:

* Find another way to wrap lines while ensuring they're still valid Python after wrapping
* Choose line length to return based on User-Agent header
* Put it all together

Or I may just implement the padding and move on. We'll see.
