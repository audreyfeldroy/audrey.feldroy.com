# Constructing SQLite Tables for Notebooks and Search

SQLite full text search setup via APSW for all the notebooks on this website, inspired by the [APSW FTS5 Tour]((https://rogerbinns.github.io/apsw/example-fts.html)).

## Setup


```python
from typing import Optional, Iterator, Any

from pprint import pprint
import re
import functools

import apsw
import apsw.ext
import apsw.fts5
import apsw.fts5aux
import apsw.fts5query

from execnb.nbio import read_nb
from fastcore.all import *
from pathlib import Path, PosixPath
```


```python
print("FTS5 available:", "ENABLE_FTS5" in apsw.compile_options)
```

    FTS5 available: True


## Create a Notebooks Database

Until now I haven't had a SQLite database for anything on this site. Let's create one.


```python
connection = apsw.Connection("notebooks.db")
connection
```




    <apsw.Connection at 0x10b282110>



## Create and Populate Table `notebooks`


```python
nbs = L(Path(".").glob("*.ipynb")).sorted(reverse=True)
nbs
```




    (#38) [Path('2025-01-16-Cosine-Similarity-Breakdown-in-LaTeX.ipynb'),Path('2025-01-14-Constructing-SQLite-Tables-for-Notebooks-and-Search.ipynb'),Path('2025-01-13-SQLite-FTS5-Tokenizers-unicode61-and-ascii.ipynb'),Path('2025-01-12-A-Better-Notebook-Index-Page.ipynb'),Path('2025-01-11-NBClassic-Keyboard-Shortcuts-in-Command-and-Dual-Mode.ipynb'),Path('2025-01-10-Understanding-FastHTML-Routes-Requests-and-Redirects.ipynb'),Path('2025-01-09-Reading-and-Writing-Jupyter-Notebooks-With-Python.ipynb'),Path('2025-01-08-HTML-Title-Tag-in-FastHTML.ipynb'),Path('2025-01-07-Verifying-Bluesky-Domain-in-FastHTML.ipynb'),Path('2025-01-06-Understanding-FastHTML-Headers.ipynb'),Path('2025-01-05-SSH-Agent-to-Save-Passphrase-Typing.ipynb'),Path('2025-01-04-Claude-Artifacts-in-Notebooks.ipynb'),Path('2025-01-03-Using-zip.ipynb'),Path('2025-01-02-FastHTML-Piano-Part-3.ipynb'),Path('2025-01-02-FastHTML-Piano-Part-2.ipynb'),Path('2025-01-01-FastHTML-Piano-Part-1.ipynb'),Path('2025-01-01-Command-Substitution-in-Bash.ipynb'),Path('2024-12-31-Note-Box-FastTag.ipynb'),Path('2024-12-30-Images-In-Every-Way-In-Notebooks.ipynb'),Path('2024-12-29-Bash-in-Jupyter-Notebooks.ipynb')...]



All notebooks, sorted from newest to oldest.


```python
nb = read_nb(nbs[0])
nb.cells[0]
```




```json
{ 'cell_type': 'markdown',
  'id': 'e865206a',
  'idx_': 0,
  'metadata': {},
  'source': '# Cosine Similarity Breakdown in LaTeX'}
```



A Markdown cell looks like this.


```python
connection.execute("""CREATE TABLE IF NOT EXISTS notebooks (
    id INTEGER PRIMARY KEY,
    path TEXT NOT NULL,
    markdown_content TEXT)""")
```




    <apsw.Cursor at 0x10a42e560>



We create a table to put notebooks' paths and Markdown content into. (At this point we skip code cells to make things simple.)


```python
def is_md_cell(c): return c.cell_type == 'markdown'
md_cells = L(nb.cells).filter(is_md_cell)
md_cells
```




    (#18) [{'cell_type': 'markdown', 'id': 'e865206a', 'metadata': {}, 'source': '# Cosine Similarity Breakdown in LaTeX', 'idx_': 0},{'cell_type': 'markdown', 'id': '5dc1aea0', 'metadata': {}, 'source': 'A mathematical breakdown of cosine similarity, with copy-pastable LaTeX.', 'idx_': 1},{'cell_type': 'markdown', 'id': '1bbf957e', 'metadata': {}, 'source': '## Overview', 'idx_': 2},{'cell_type': 'markdown', 'id': 'faad9583', 'metadata': {}, 'source': "After hearing so much about cosine similarity, I thought it was something extremely difficult to understand. It turns out it's just the similarity of 2 word vectors, calculated as the cosine of the angle between them.\n\nThe result ranges from -1 to 1, where:\n\n* 1 means the vectors point in the same direction (most similar)\n* 0 means they're perpendicular (totally unrelated)\n* -1 means they point in opposite directions (complete opposites)\n\nSimilarity is just about the angle. The vectors are typically normalized to make comparisons make more sense intuitively, and to avoid having to deal with magnitudes as well.\n\nNote: I'm reading that the range used with word vectors is usually [0,1] because word vectors typically are non-negative.", 'idx_': 3},{'cell_type': 'markdown', 'id': 'f5b4b6e0', 'metadata': {}, 'source': '## The Cosine Similarity Formula', 'idx_': 4},{'cell_type': 'markdown', 'id': '11d974a5', 'metadata': {}, 'source': 'The cosine similarity formula in LaTeX:', 'idx_': 5},{'cell_type': 'markdown', 'id': '1932bca7', 'metadata': {}, 'source': '## Dot Product', 'idx_': 7},{'cell_type': 'markdown', 'id': '83e774a9', 'metadata': {}, 'source': "If you're wondering why it looks so familiar, it's probably because you can get it by rewriting the definition of the dot product:", 'idx_': 8},{'cell_type': 'markdown', 'id': '148fa3a6', 'metadata': {}, 'source': '## Expanding Dot Product Sum', 'idx_': 10},{'cell_type': 'markdown', 'id': 'dd419125', 'metadata': {}, 'source': 'In the cosine similarity formula, the numerator is the dot product **A** . **B**. Expanding that, you get the sum of all the vector components multiplied together:', 'idx_': 11},{'cell_type': 'markdown', 'id': 'eb3a082d', 'metadata': {}, 'source': '## Magnitude: Sqrt of Sum of Squares', 'idx_': 13},{'cell_type': 'markdown', 'id': 'ff564e70', 'metadata': {}, 'source': 'The magnitude ‖A‖ is the square root of the sum of the squares of its components:', 'idx_': 14},{'cell_type': 'markdown', 'id': '7badf992', 'metadata': {}, 'source': "It's just the length of the vector.", 'idx_': 16},{'cell_type': 'markdown', 'id': '7fbc3d12', 'metadata': {}, 'source': '## Multiplying Vector Magnitudes', 'idx_': 17},{'cell_type': 'markdown', 'id': '69241573', 'metadata': {}, 'source': 'In the cosine similarity formula, the denominator is multiplying magnitudes $\\|\\mathbf{A}\\| \\|\\mathbf{B}\\|$ together:', 'idx_': 18},{'cell_type': 'markdown', 'id': '5d0bc906', 'metadata': {}, 'source': '## Putting It All Together', 'idx_': 20},{'cell_type': 'markdown', 'id': '0c562278', 'metadata': {}, 'source': '## Summary', 'idx_': 22},{'cell_type': 'markdown', 'id': '1260a44f', 'metadata': {}, 'source': "Cosine similarity measures how similar two vectors are by finding the cosine of the angle between them. \n\nThe math is not as bad as it looks: we're just comparing the directions vectors point in, normalized by their lengths.", 'idx_': 23}]



A list of only Markdown cells from a notebook looks like this.


```python
def cell_source(c): return c.source
md = md_cells.map(cell_source)
md
```




    (#18) ['# Cosine Similarity Breakdown in LaTeX','A mathematical breakdown of cosine similarity, with copy-pastable LaTeX.','## Overview',"After hearing so much about cosine similarity, I thought it was something extremely difficult to understand. It turns out it's just the similarity of 2 word vectors, calculated as the cosine of the angle between them.\n\nThe result ranges from -1 to 1, where:\n\n* 1 means the vectors point in the same direction (most similar)\n* 0 means they're perpendicular (totally unrelated)\n* -1 means they point in opposite directions (complete opposites)\n\nSimilarity is just about the angle. The vectors are typically normalized to make comparisons make more sense intuitively, and to avoid having to deal with magnitudes as well.\n\nNote: I'm reading that the range used with word vectors is usually [0,1] because word vectors typically are non-negative.",'## The Cosine Similarity Formula','The cosine similarity formula in LaTeX:','## Dot Product',"If you're wondering why it looks so familiar, it's probably because you can get it by rewriting the definition of the dot product:",'## Expanding Dot Product Sum','In the cosine similarity formula, the numerator is the dot product **A** . **B**. Expanding that, you get the sum of all the vector components multiplied together:','## Magnitude: Sqrt of Sum of Squares','The magnitude ‖A‖ is the square root of the sum of the squares of its components:',"It's just the length of the vector.",'## Multiplying Vector Magnitudes','In the cosine similarity formula, the denominator is multiplying magnitudes $\\|\\mathbf{A}\\| \\|\\mathbf{B}\\|$ together:','## Putting It All Together','## Summary',"Cosine similarity measures how similar two vectors are by finding the cosine of the angle between them. \n\nThe math is not as bad as it looks: we're just comparing the directions vectors point in, normalized by their lengths."]



Map the cells to just their Markdown source. For now we don't care about the rest.


```python
def extract_markdown_content(nbpath):
    """Extract all markdown cell content from a notebook"""
    nb = read_nb(nbpath)
    md_cells = L(nb.cells).filter(is_md_cell)
    return "\n".join(md_cells.map(cell_source))
extract_markdown_content(nbs[0])
```




    "# Cosine Similarity Breakdown in LaTeX\nA mathematical breakdown of cosine similarity, with copy-pastable LaTeX.\n## Overview\nAfter hearing so much about cosine similarity, I thought it was something extremely difficult to understand. It turns out it's just the similarity of 2 word vectors, calculated as the cosine of the angle between them.\n\nThe result ranges from -1 to 1, where:\n\n* 1 means the vectors point in the same direction (most similar)\n* 0 means they're perpendicular (totally unrelated)\n* -1 means they point in opposite directions (complete opposites)\n\nSimilarity is just about the angle. The vectors are typically normalized to make comparisons make more sense intuitively, and to avoid having to deal with magnitudes as well.\n\nNote: I'm reading that the range used with word vectors is usually [0,1] because word vectors typically are non-negative.\n## The Cosine Similarity Formula\nThe cosine similarity formula in LaTeX:\n## Dot Product\nIf you're wondering why it looks so familiar, it's probably because you can get it by rewriting the definition of the dot product:\n## Expanding Dot Product Sum\nIn the cosine similarity formula, the numerator is the dot product **A** . **B**. Expanding that, you get the sum of all the vector components multiplied together:\n## Magnitude: Sqrt of Sum of Squares\nThe magnitude ‖A‖ is the square root of the sum of the squares of its components:\nIt's just the length of the vector.\n## Multiplying Vector Magnitudes\nIn the cosine similarity formula, the denominator is multiplying magnitudes $\\|\\mathbf{A}\\| \\|\\mathbf{B}\\|$ together:\n## Putting It All Together\n## Summary\nCosine similarity measures how similar two vectors are by finding the cosine of the angle between them. \n\nThe math is not as bad as it looks: we're just comparing the directions vectors point in, normalized by their lengths."



Join all the Markdown cells' content for a notebook together, separated by 1 new line between each pair of cells.


```python
def populate_notebooks_table():
    connection.execute("DELETE FROM notebooks")
    
    for nb_path in nbs:
        markdown_text = extract_markdown_content(nb_path)
        connection.execute(
            "INSERT INTO notebooks (path, markdown_content) VALUES (?, ?)",
            (str(nb_path), markdown_text)
        )
populate_notebooks_table()
```


```python
connection.execute("SELECT count(*) FROM notebooks").get
```




    38



Now we have notebook paths and their contents in a SQLite table.

## Create Search Table


```python
if not connection.table_exists("main", "search"):
    search_table = apsw.fts5.Table.create(
        connection,
        "search",
        content="notebooks",
        columns=None,
        generate_triggers=True,
        tokenize=["unicode61"])
else:
    search_table = apsw.fts5.Table(connection, "search")
```

Here we check if a table named `search` already exists in the `main` database of `connection`. If it doesn't exist, we create it.

`search` is a virtual table pointing at the `notebooks` table. It doesn't actually store any data! It contains indexes on that table, as well as a table-like interface for searching it.

## Check the Tables


```python
print("quoted name", search_table.quoted_table_name)
```

    quoted name "main"."search"


This verifies that the database schema `main` and table name `search have been set up.

The notebooks' content:


```python
print(connection.execute(
        "SELECT sql FROM sqlite_schema WHERE name='notebooks'"
    ).get)
```

    CREATE TABLE notebooks (
        id INTEGER PRIMARY KEY,
        path TEXT NOT NULL,
        markdown_content TEXT)



```python
pprint(search_table.structure)
```

    FTS5TableStructure(name='search',
                       columns=('id', 'path', 'markdown_content'),
                       unindexed=set(),
                       tokenize=('unicode61',),
                       prefix=set(),
                       content='notebooks',
                       content_rowid='_ROWID_',
                       contentless_delete=None,
                       contentless_unindexed=None,
                       columnsize=True,
                       tokendata=False,
                       locale=False,
                       detail='full')



```python
print(f"{search_table.config_rank()=}")
```

    search_table.config_rank()='bm25()'



```python
print(f"{search_table.row_count=}")
```

    search_table.row_count=38



```python
print(f"{search_table.tokens_per_column=}")
```

    search_table.tokens_per_column=[38, 302, 10334]


## Optional Cleanup

At one point I had to run this to drop the search table, so I could recreate it with a different tokenizer:


```python
connection.execute("DROP TABLE IF EXISTS search")
```




    <apsw.Cursor at 0x1093dfa00>



## What Next?

To be continued...
