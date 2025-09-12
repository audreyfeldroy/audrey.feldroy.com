# How to Turn a Jupyter Notebook Into a Python Script

Here I turn this Jupyter notebook into a Python script, using nbdev's nb_export function from the notebook itself.

## Name the Module

First, I add the `default_exp` directive with the module name I want created from this notebook:


```python
#| default_exp rename_nbs
```

## Bring Over Code

In this section, I copy over just the important cells from [Auto-Renaming My Untitled.ipynb Files With Gemini 1.5 Flash](https://audrey.feldroy.com/nbs/2025-02-01-Auto-Renaming-My-Untitled-ipynb-Files-With-Gemini)

I also define function `get_untitled_nbs`.

I add the export directive to each cell, so that it gets added to my script.


```python
#| export
from datetime import datetime
from fastcore.utils import *
import google.generativeai as genai
from nbdev.export import nb_export
from pathlib import Path
```


```python
#| export
def generate_title_part(nb):
    prompt = f"""Given this Jupyter notebook, create a filename following these EXACT steps:
1. Extract the title from the first cell if it starts with '#'. In this case it's: "FastHTML By Example, Part 2"
2. Convert to the format: Words-In-Title-Case-With-Hyphens.ipynb
3. Remove any special characters (like commas)
4. If the filename sounds repetitive, simplify it.
5. If the first cell does not contain a title, create one based on the entire notebook's contents.

<notebook>
{nb}
</notebook>

Return ONLY the filename, nothing else."""
    safety_settings = [
        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE",},
        {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE",},
        {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE",},
        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE",},
    ]
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
    response = model.generate_content(prompt, safety_settings=safety_settings, request_options = {"timeout": 1000})
    try:
        return response.text
    except Exception as ex:
        raise ex
```


```python
#| export
def rename_notebook(nb_path):
    """Rename an untitled notebook based on its contents and modification date"""
    date = datetime.fromtimestamp(Path(nb_path).stat().st_mtime).strftime('%Y-%m-%d')
    with open(nb_path) as f: nb = f.read()
    
    title_part = generate_title_part(nb)
    
    new_name = f"{date}-{title_part.strip()}"
    new_path = Path(new_name)
    
    if new_path.exists():
        print(f"Warning: {new_path} already exists")
        return nb_path
    else:
        nb_path.rename(new_path)
        print(f"Renamed {nb_path} to {new_path}")
        return new_path
```


```python
#| export
def get_untitled_nbs(nbs_path): return L(Path(nbs_path).expanduser().glob("Untitled*.ipynb"))
```


```python
#| export
if __name__ == '__main__':
    nbs = get_untitled_nbs("~/fun/arg-drafts")
    new_paths = nbs.map(rename_notebook)
```

## Export It

Here I export `rename_nbs.py` from this notebook to a new `scripts/` directory where I'm going to put all my Python scripts:


```python
nb_export("2025-02-04-Using-nb_export-to-Export-a-Python-Module-From-a-Notebook.ipynb", lib_path="../scripts")
```


```python
!ls ../scripts/
```

    rename_nbs.py


It's amazing to call `nb_export` as a function in notebooks! I often use the nb_export command in my terminal, which is nice, but in-notebook use is even nicer.
