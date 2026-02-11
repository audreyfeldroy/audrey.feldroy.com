# execnb's read_nb and nb2fasthtml's render_nb

Exploring how execnb reads notebooks and nb2fasthtml renders them, to understand the tools I'm building on.

## Setup

```python
import glob
from pathlib import Path
from fastcore.all import *
from nb2fasthtml.core import *
from execnb.nbio import *
```


```python
nbs = L(Path('../nbs').glob('*.ipynb'))
nbs
```




    (#11) [Path('../nbs/2024-07-29-Delegates-Decorator.ipynb'),Path('../nbs/2024-07-16_Xtend_Pico.ipynb'),Path('../nbs/2024-08-05-Claudette-FastHTML.ipynb'),Path('../nbs/2024-12-23-nb2fasthtml.ipynb'),Path('../nbs/2024-07-29-Auth.ipynb'),Path('../nbs/2024-12-23-Daddys_Snowman_Card.ipynb'),Path('../nbs/2024-07-15-Printing_Components.ipynb'),Path('../nbs/2024-07-14_SemanticUI_Cards.ipynb'),Path('../nbs/2024-07-29-FH-by-Example.ipynb'),Path('../nbs/2023-07-29-nbdev.ipynb'),Path('../nbs/2024-08-04-Claudette.ipynb')]




```python
nbs = sorted(nbs)
nbs
```




    [Path('../nbs/2023-07-29-nbdev.ipynb'),
     Path('../nbs/2024-07-14_SemanticUI_Cards.ipynb'),
     Path('../nbs/2024-07-15-Printing_Components.ipynb'),
     Path('../nbs/2024-07-16_Xtend_Pico.ipynb'),
     Path('../nbs/2024-07-29-Auth.ipynb'),
     Path('../nbs/2024-07-29-Delegates-Decorator.ipynb'),
     Path('../nbs/2024-07-29-FH-by-Example.ipynb'),
     Path('../nbs/2024-08-04-Claudette.ipynb'),
     Path('../nbs/2024-08-05-Claudette-FastHTML.ipynb'),
     Path('../nbs/2024-12-23-Daddys_Snowman_Card.ipynb'),
     Path('../nbs/2024-12-23-nb2fasthtml.ipynb')]




```python
x = nbs[-2]
x
```




    Path('../nbs/2024-12-23-Daddys_Snowman_Card.ipynb')




```python
read_nb(x)
```




```json
{ 'cells': [ { 'cell_type': 'markdown',
               'idx_': 0,
               'metadata': {},
               'source': "# Daddy's Snowman Card"},
             { 'cell_type': 'markdown',
               'idx_': 1,
               'metadata': {},
               'source': "Here we are checking the numbers from our daughter's "
                         'snowman card to Daddy. She gave him math problems to '
                         'solve and a snowman joke.'},
             { 'cell_type': 'code',
               'execution_count': None,
               'idx_': 2,
               'metadata': {},
               'outputs': [ { 'data': {'text/plain': ['200000']},
                              'execution_count': None,
                              'metadata': {},
                              'output_type': 'execute_result'}],
               'source': '200000'},
             { 'cell_type': 'markdown',
               'idx_': 3,
               'metadata': {},
               'source': '**AI Prompt**\n'
                         '\n'
                         'What is 200000 (2 followed by 5 zeroes)?'},
             { 'cell_type': 'markdown',
               'idx_': 4,
               'metadata': {},
               'source': "**AI Response**\n\nThat's two hundred thousand."},
             { 'cell_type': 'code',
               'execution_count': None,
               'idx_': 5,
               'metadata': {},
               'outputs': [ { 'data': {'text/plain': ['200100']},
                              'execution_count': None,
                              'metadata': {},
                              'output_type': 'execute_result'}],
               'source': '100+200000'}],
  'metadata': { 'kernelspec': { 'display_name': '.venv',
                                'language': 'python',
                                'name': 'python3'},
                'language_info': { 'codemirror_mode': { 'name': 'ipython',
                                                        'version': 3},
                                   'file_extension': '.py',
                                   'mimetype': 'text/x-python',
                                   'name': 'python',
                                   'nbconvert_exporter': 'python',
                                   'pygments_lexer': 'ipython3',
                                   'version': '3.12.7'}},
  'nbformat': 4,
  'nbformat_minor': 4,
  'path_': '../nbs/2024-12-23-Daddys_Snowman_Card.ipynb'}
```




```python
render_nb(x)
```




```html
<main class="container">  <div class="frontmatter">
    <h1>Daddy&#x27;s Snowman Card</h1>
  </div>
  <div>
    <div class="marked">Here we are checking the numbers from our daughter&#x27;s snowman card to Daddy. She gave him math problems to solve and a snowman joke.</div>
  </div>
  <article>
    <div class="marked">
```python
200000
```
</div>
    <footer><pre ><code>200000</code></pre></footer>
  </article>
  <div>
    <div class="marked">**AI Prompt**

What is 200000 (2 followed by 5 zeroes)?</div>
  </div>
  <div>
    <div class="marked">**AI Response**

That&#x27;s two hundred thousand.</div>
  </div>
  <article>
    <div class="marked">
```python
100+200000
```
</div>
    <footer><pre ><code>200100</code></pre></footer>
  </article>
</main>
```




```python

```
