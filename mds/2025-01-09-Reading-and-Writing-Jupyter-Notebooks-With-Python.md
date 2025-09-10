# Reading and Writing Jupyter Notebooks With Python


```python
from execnb.nbio import new_nb, mk_cell, read_nb, write_nb
from execnb.shell import exec_nb
from pathlib import Path
```

## Exploring This Snippet

I'm starting with a snippet of code from the bottom of execnb's 01_nbio.ipynb, breaking it down into pieces and seeing each part:

```python
nb = new_nb([mk_cell('print(1)')])
path = Path('test.ipynb')
write_nb(nb, path)
nb2 = read_nb(path)
print(nb2.cells)
path.unlink()
```

Funny, that original notebook built it up one cell at a time to get to that cell. Now I'm breaking down the finished result for myself to understand it better.

It looks clear and understandable enough. But just reading code doesn't build mental muscle memory. To truly learn I find I have to interact, evaluate cells, print things, and see what everything even the obvious does.

## About Post-Cell Explanations

I realize I've been writing before each cell instead of after. I'll try explaining after cells to better emulate Jeremy Howard's style. It's nice in a way because you get to look at the code and try to understand it for yourself first.

## Creating a Jupyter Notebook Programmatically


```python
nb = new_nb([mk_cell('print(1)')])
nb
```




```json
{ 'cells': [ { 'cell_type': 'code',
               'directives_': {},
               'execution_count': 0,
               'idx_': 0,
               'metadata': {},
               'outputs': [],
               'source': 'print(1)'}],
  'metadata': {},
  'nbformat': 4,
  'nbformat_minor': 5}
```



Here I create a new notebook via `new_nb`. The outputs list is empty because this notebook cell hasn't been executed yet - I've only created the notebook structure in memory.

## Creating a Path to Write It To


```python
path = Path('test.ipynb')
path
```




    Path('test.ipynb')



Using standard pathlib here to create a path.


```python
print(path)
```

    test.ipynb


Printing it shows the relative path.


```python
path.absolute()
```




    Path('/Users/arg/fun/arg-blog-fasthtml/nbs/test.ipynb')



Here we can now see we're somewhere fun! So, relax and enjoy the rest of this experience.

## Writing and Rereading `test.ipynb`


```python
write_nb(nb, path)
```


```python
nb2 = read_nb(path)
nb2
```




```json
{ 'cells': [ { 'cell_type': 'code',
               'execution_count': 0,
               'idx_': 0,
               'metadata': {},
               'outputs': [],
               'source': 'print(1)'}],
  'metadata': {},
  'nbformat': 4,
  'nbformat_minor': 5,
  'path_': 'test.ipynb'}
```



Yay, we have written the notebook to test.ipynb and read it back in as nb2 successfully!

## Exploring the Cells


```python
nb2.cells
```




    [{'cell_type': 'code',
      'execution_count': 0,
      'metadata': {},
      'outputs': [],
      'source': 'print(1)',
      'idx_': 0}]



Here we see there's 1 cell, the one we originally created, as expected. This would be `nb2['cells']` if this were a normal dict, but we've got a nice fastcore `AttrDict` here with dot access.


```python
print(nb2.cells)
```

    [{'cell_type': 'code', 'execution_count': 0, 'metadata': {}, 'outputs': [], 'source': 'print(1)', 'idx_': 0}]


Printing the cells shows them on a single line.

## Cleaning Up Our Chef's Station


```python
path.unlink()
```

In pathlib, `unlink` deletes a file or symlink. We just deleted test.ipynb.

Careful with programmatic deletion of files. Keep the code as simple as possible. Here it's super-simple so we're fine.
