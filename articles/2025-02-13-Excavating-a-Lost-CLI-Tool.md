# Excavating a Lost CLI Tool

I thought I had completely lost my new iteration on my notebook titler tool, but it turns out I'm finding bits and pieces in various places. Here I try to put it together again. 

## Setup


```python
#| default_exp unun
```


```python
#| export
from datetime import datetime
import google.generativeai as genai
import IPython
import json
from nbdev.export import nb_export
from pathlib import Path
import typer
from typing_extensions import Annotated
```

To get better at posting every day, I'm time-boxing from now until 10am. I'm picking up where I left off yesterday at the bottom of [My Self-Analysis of How to Get Back to Posting Every Day](https://audrey.feldroy.com/nbs/2025-02-12-My-Self-Analysis-of-How-to-Get-Back-to-Posting-Every-Day)


```python
datetime.now()
```




    datetime.datetime(2025, 2, 13, 9, 7, 0, 856623)



I would like the time box to include posting to social media, which means I need to finish writing the actual post by 9:40am to give me 20 minutes of social media time. I'm a bit slow at social media, especially because I like to listen to what others are saying at least a little before I post.

## Re-Notebookifying my nbdev-Exported Script

2025-02-10-How-I-Built-an-Ununtitle-CLI-Tool-With-Typer.ipynb is gone, but I found its lost exported script ununtitle.py and brought it back over into this notebook.


```python
#| export
def title_it(nb, nbpath):
    date = datetime.fromtimestamp(Path(nbpath).stat().st_mtime).strftime('%Y-%m-%d')
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
    prompt = f"""Given this Jupyter notebook, create a filename-title pair following these steps:
1. Prefix the filename with `{date}-` but not the title.
2. Think about what would be most compelling about the given notebook if it were published as a blog post.
3. Create a list of 20 compelling titles for it.
4. Pick the top title from the list of 20 titles. 
5. Convert it to the format: {date}-Words-In-Title-Case-With-Hyphens.ipynb
6. Remove any special characters (like commas)
7. If the title and/or filename sound repetitive, simplify them

<notebook>{nb}</notebook>

Return ONLY json like {{"title": "my_title", "filename": "{date}-my_filename.ipynb"}}, nothing else. Do not add a fenced code block. Just the JSON, please."""
    response = model.generate_content(prompt, safety_settings=[], request_options = {"timeout": 1000})
    try:
        return response.text
    except Exception as ex:
        raise ex
```

I started to modify this part but realized I don't have time to finish it because I don't know Typer well enough.


```python
def main(
    prompt: Annotated[bool, typer.Option(help="Confirm each file before renaming.")] = True,
):
    """
    Rename Untitled notebooks with meaningful names based on their content.
    
    If --dry-run is used, show what would be renamed without actually doing it.
    """
    for p in Path('.').glob('Untitled*.ipynb'):
        with open(p) as f: nb = f.read()
        cleaned = title_it(nb, p).replace('```json', '').replace('```', '').strip()
        new_names = json.loads(cleaned)

        if prompt:
            response = typer.confirm(f"Rename {p} to {new_names['filename']}")
        if not response: break
        
        if not dry_run:
            p.rename(new_names['filename'])
            print(f"Renamed {p} to {new_names['filename']}")
```

OK, this definitely doesn't do anything correctly, but I'm publishing it because I'm out of time. It's so embarrassing to publish broken code like this! I mean, I'm not even using the dry_run variable anymore, and there is a way to prompt her input with a default value that's editable probably, but I don't have time to look that up. Oh well. 


```python
#| export
if __name__ == "__main__":
    typer.run(main)
```


<pre style="white-space:pre;overflow-x:auto;line-height:normal;font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace"><span style="color: #808000; text-decoration-color: #808000">Usage: </span>ipykernel_launcher.py [OPTIONS]
</pre>




<pre style="white-space:pre;overflow-x:auto;line-height:normal;font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace"><span style="color: #7f7f7f; text-decoration-color: #7f7f7f">Try </span><span style="color: #7f7fbf; text-decoration-color: #7f7fbf">'ipykernel_launcher.py </span><span style="color: #7f7fbf; text-decoration-color: #7f7fbf; font-weight: bold">--help</span><span style="color: #7f7fbf; text-decoration-color: #7f7fbf">'</span><span style="color: #7f7f7f; text-decoration-color: #7f7f7f"> for help.</span>
</pre>




<pre style="white-space:pre;overflow-x:auto;line-height:normal;font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace"><span style="color: #800000; text-decoration-color: #800000">╭─ Error ─────────────────────────────────────────────────────────────────────────────────────────────────────────╮</span>
<span style="color: #800000; text-decoration-color: #800000">│</span> No such option: <span style="color: #008000; text-decoration-color: #008000; font-weight: bold">-f</span>                                                                                              <span style="color: #800000; text-decoration-color: #800000">│</span>
<span style="color: #800000; text-decoration-color: #800000">╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯</span>
</pre>




    An exception has occurred, use %tb to see the full traceback.


    SystemExit: 2




```python
nb_export("2025-02-13-Excavating-a-Lost-CLI-Tool.ipynb", lib_path="../scripts")
```


```python

```

Oh no, I definitely went over time:


```python
datetime.now()
```




    datetime.datetime(2025, 2, 13, 9, 47, 4, 361120)



## Tomorrow's TODO List


```python
* Copy over the cells with nbdev directives 
* Remove dry_run completely
* When prompting a user, provide the generated file name as the start of the filename prompt value for them to tap backspace and edit. 
```


```python

```
