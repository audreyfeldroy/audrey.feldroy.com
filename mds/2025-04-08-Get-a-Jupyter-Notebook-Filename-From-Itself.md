# Get a Jupyter Notebook Filename From Itself

When working in notebooks, you'll occasionally need to access the notebook's own filename. Here's code to do it, which I've verified works in Jupyter Notebook Classic.


```python
import IPython
```

## The Trick: JS to Python Bridge

You can't get the notebook's name from Python. But you can get it from JavaScript, and then execute Python code to store it into a Python variable:


```javascript
%%javascript
IPython.notebook.kernel.execute('nbname = "' + IPython.notebook.notebook_name + '"')
```


    <IPython.core.display.Javascript object>


`IPython.notebook.kernel.execute()` is a JS method that tells the Jupyter kernel to execute a string of Python.

## Verify It Worked

Let's print the Python variable we set via JS:


```python
nbname
```




    '2025-04-08-Get-a-Jupyter-Notebook-Filename-From-Itself.ipynb'


