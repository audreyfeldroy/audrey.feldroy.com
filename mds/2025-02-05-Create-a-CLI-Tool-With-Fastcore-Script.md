# Create a CLI Tool With fastcore.script

Fastcore's call_parse decorator turns Python functions into CLI tools quickly. It's nowhere near as fancy as Typer or Click, but it's super quick to use.

## Study the Example

From https://fastcore.fast.ai/script.html#example


```python
#| export
from fastcore.script import *
from fastcore.utils import *
from pathlib import Path
import time
```


```python
from nbdev.export import nb_export
```


```python
@call_parse
def main(msg:str,     # The message
         upper:bool): # Convert to uppercase?
    "Print `msg`, optionally converting to uppercase"
    print(msg.upper() if upper else msg)
```

We can use the function right here, which is nice:


```python
main("hey", upper=True)
```

    HEY



```python
main("hey", upper=False)
```

    hey


As for using it as a CLI tool, the docs say "If you copy that info a file and run it, you’ll see:
    
```sh
$ examples/test_fastcore.py --help
usage: test_fastcore.py [-h] [--upper] msg

Print `msg`, optionally converting to uppercase

positional arguments:
  msg          The message

optional arguments:
  -h, --help   show this help message and exit
  --upper      Convert to uppercase? (default: False)
```
"

## Real-World Example: Prepending Notebook Filenames With Dates

I have many notebooks like Docker-Run.ipynb that I'd like prepended with the ISO 8601 date that they were last updated. My script will be prepend_nbs_with_dates.py because of the next line:


```python
#| default_exp prepend_nbs_with_dates
```

I'll define a function to get all of them:


```python
#| export
def get_undated_nbs(): return L(Path().glob('[!0-9]*.ipynb'))
```


```python
nbs = get_undated_nbs()
nbs
```




    (#14) [Path('Publish-Command-for-This-Blog.ipynb'),Path('Title-Generation.ipynb'),Path('ShellSage-Ghostty-and-Tmux.ipynb'),Path('Understanding-Gradient-Descent.ipynb'),Path('SVG-Animation-Via-CSS-Keyframes.ipynb'),Path('AI-Trajectory.ipynb'),Path('asyncio-in-Jupyter-Notebooks.ipynb'),Path('Writing-for-the-AIs.ipynb'),Path('ai_server_load_testing.ipynb'),Path('SVG-Paths-in-FastHTML.ipynb'),Path('fastai-WordTokenizer.ipynb'),Path('Matplotlib-Charts-in-FastHTML.ipynb'),Path('fastcore-and-anki.ipynb'),Path('Docker-Run.ipynb')]




```python
nbs[1]
```




    Path('Title-Generation.ipynb')



Then I'll define a function to prepend a date to a filename:


```python
#| export
def prepend_date(fn):
    "Prepend ISO 8601 date to filename if not already present"
    if fn.stem[0].isdigit(): return  # Already has date
    mtime = fn.stat().st_mtime
    date = time.strftime('%Y-%m-%d', time.localtime(mtime))
    new_name = fn.parent/f"{date}-{fn.name}"
    fn.rename(new_name)
    return new_name
```


```python
# prepend_date(nbs[1])
```

Finally, I'll define a main function that gets all undated notebooks and prepends dates to their filenames:


```python
#| export
@call_parse
def main(dry_run:bool=True): # Don't actually rename if True
    "Prepend dates to notebook filenames"
    fns = get_undated_nbs()
    print(f"Found {len(fns)} undated notebooks")
    if dry_run:
        for f in fns:
            mtime = f.stat().st_mtime
            date = time.strftime('%Y-%m-%d', time.localtime(mtime))
            print(f"{f} -> {date}-{f.name}")
    else:
        for f in fns: prepend_date(f)
```

By default this does a dry run:


```python
main()
```

    Found 14 undated notebooks
    Publish-Command-for-This-Blog.ipynb -> 2025-01-11-Publish-Command-for-This-Blog.ipynb
    Title-Generation.ipynb -> 2025-01-29-Title-Generation.ipynb
    ShellSage-Ghostty-and-Tmux.ipynb -> 2025-01-29-ShellSage-Ghostty-and-Tmux.ipynb
    Understanding-Gradient-Descent.ipynb -> 2025-01-16-Understanding-Gradient-Descent.ipynb
    SVG-Animation-Via-CSS-Keyframes.ipynb -> 2025-01-25-SVG-Animation-Via-CSS-Keyframes.ipynb
    AI-Trajectory.ipynb -> 2025-02-04-AI-Trajectory.ipynb
    asyncio-in-Jupyter-Notebooks.ipynb -> 2025-01-25-asyncio-in-Jupyter-Notebooks.ipynb
    Writing-for-the-AIs.ipynb -> 2025-01-27-Writing-for-the-AIs.ipynb
    ai_server_load_testing.ipynb -> 2024-11-25-ai_server_load_testing.ipynb
    SVG-Paths-in-FastHTML.ipynb -> 2025-01-27-SVG-Paths-in-FastHTML.ipynb
    fastai-WordTokenizer.ipynb -> 2025-01-11-fastai-WordTokenizer.ipynb
    Matplotlib-Charts-in-FastHTML.ipynb -> 2025-01-22-Matplotlib-Charts-in-FastHTML.ipynb
    fastcore-and-anki.ipynb -> 2025-01-19-fastcore-and-anki.ipynb
    Docker-Run.ipynb -> 2025-01-20-Docker-Run.ipynb


Here we run it for real:


```python
main(dry_run=False)
```

    Found 14 undated notebooks


Now there are no more undated notebooks:


```python
get_undated_nbs()
```




    (#0) []



## Export It


```python
nb_export("2025-02-05-Create-a-CLI-Tool-With-Fastcore-Script.ipynb", lib_path="../scripts")
```


```python
!ls ../scripts/
```

    prepend_nbs_with_dates.py prepend_with_dates.py


## Run It

I ran it as a function earlier, so I don't have undated notebooks at the moment!

```sh
% python ../scripts/prepend_nbs_with_dates.py
Found 0 undated notebooks
```

Give me a few hours or days, and I'll update this post...
