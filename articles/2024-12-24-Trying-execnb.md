# What Can `execnb` do?

This notebook is a [SolveIt](https://solveit.fast.ai/)-style exploration of [https://github.com/AnswerDotAI/execnb/](https://github.com/AnswerDotAI/execnb/). Here I am following the SolveIt process in a Jupyter notebook to learn new things.

## Understand the Problem

I've been interested in learning what the open-source `execnb` package does and how it works. I don't have a particular use case, other than wanting to know more so I can contribute to it or to code that uses it.

## Devise a Plan

* Study the examples defined in the `execnb` notebooks
* Create my own examples patterning them after those examples
* Use literate programming in this notebook to write about my findings

## Carry Out the Plan

Let's see what execnb can do!


```python
from execnb.nbio import *
from execnb.shell import *
from fastcore.all import *
from fasthtml.common import *
from IPython.display import HTML, Markdown
from pathlib import Path
```

## Setup: Let's Grab Some Jupyter Notebooks

We have notebooks in `nbs/` in this repo which we can look at.


```python
root = Path('../nbs').parent
nb_dir = root/'nbs'
nb_dir
```

Yay for fastcore `L` lists and chainable operations like `sorted`:


```python
nbs = L(nb_dir.glob('*.ipynb')).sorted()
nbs
```

## Reading a Jupyter Notebook with `read_nb`

`read_nb` comes from `execnb.nbio`:


```python
nb = read_nb(nbs[9])
L(nb['cells'])[1]
```

That's nice that we can get any cell, and get its info!

## Jupyter Notebook Cells

Okay, let's grab the source of cells:


```python
def get_source(cell): return cell['source']
```


```python
cells = L(nb['cells']).map(get_source)
cells
```

Let's see if those are AttrDicts:


```python
nb.cells[0]
```

Yes!

Let's use this nice AttrDict to get the source of a cell:


```python
L(nb.cells)[1].source
```


```python
def get_source(cell): return cell.source
cells = L(nb.cells).map(get_source)
cells
```

Yes, did it!

## Jupyter Notebook Metadata

Sooo...besides cells there's metadata, right?


```python
nb.metadata
```

Seems useful. Might be worth printing the Python version at least:


```python
nb.metadata.language_info.version
```

I feel like I'd want to print the Python version for every notebook I'm publishing.

The version of each imported package would be nice too. Looks like that's beyond the scope of execnb most likely. Or is it?

## CaptureShell

Looks like we can run a Jupyter notebook cell:


```python
s = CaptureShell(mpl_format='retina')
s
```


```python
s.run_cell('print("hi")')
```

Printing didn't have a result. How about a Python expression:


```python
s.run_cell('1+1+1')
```

Ah, so we can see the result of evaluating it.

What about a Markdown cell?


```python
s.run_cell('# Hi')
```


```python
s.run('# Hi')
```

Looking at `execnb.shell`, I think it's just for Python code right now.


```python
s.run("print(1)")
```

## Rendering cell outputs

I'm offline and can't install dependencies, but I can see that `render_outputs` can render some outputs of executed cells like matplotlib plots.

What about a simple Python expression?


```python
o = s.run("1+2+3")
o
```


```python
render_outputs(o)
```

What about some FastHTML?


```python
o = s.run("""from fasthtml.common import *
P("Hi")""")
o
```


```python
render_outputs(o)
```

The `HTML` function from `IPython.display` looks useful here:


```python
HTML(render_outputs(o))
```

## Completions

`SmartCompleter` extends `IPCompleter` from `IPython.core.completer`. We can try instantiating one and seeing what it does:


```python
cc = SmartCompleter(get_ipython())
cc
```


```python
cc("pr")
```

This is quite interesting!

I'm currently offline and feel like I need to read the IPython docs and source to understand more.

## Putting Pieces Together

Let's revisit a simple notebook and put these pieces together.


```python
nb = read_nb(nbs[9])
cells = L(nb['cells'])
cells[0]
```


```python
cells[0].source
```


```python
Markdown(cells[0].source)
```


```python
cells[1]
```


```python
Markdown(cells[1].source)
```


```python
cells[2]
```


```python
HTML(cells[2].source)
```


```python
s = CaptureShell(mpl_format='retina')
s
```


```python
render_outputs(cells[2].outputs)
```


```python
HTML(render_outputs(cells[2].outputs))
```


```python
s.cell(cells[2])
```


```python
cells[2].outputs
```


```python
find_output(cells[2].outputs)['data']
```


```python
out_exec(cells[2].outputs)
```


```python
def get_type_and_source(cell): return cell.cell_type, cell.source
```


```python
cells = L(nb.cells).map(get_type_and_source)
cells
```


```python
def render_cell(c):
    if c.cell_type == 'markdown': return Markdown(c.source)
    # TODO: render both source and outputs for code cells
    elif c.cell_type == 'code': return HTML(c.source)
```


```python
cells = L(nb.cells).map(render_cell)
cells
```


```python
cells[0]
```


```python
cells[1]
```


```python
cells[5]
```

## Reflect

I've studied the 2 notebooks in `execnb`: `nbio` and `shell`

I created examples to explore:

* `read_nb`'s returned nb cells and metadata
* `CaptureShell` and its `run_cell()` and `run()` methods
* `render_outputs()` and `HTML()`
* `SmartCompleter`

I reviewed the examples I created, putting them together using a larger portion of a sample notebook. 

* In doing so, I discovered I had missed `CaptureShell.cell()`

Next steps:

* I plan to understand `IPython.core.display` objects better. I'm not sure how to use fastcore to combine them into a big displayable object.
* I wonder how Quarto renders a Jupyter notebook, and if I can explore that code similarly.
