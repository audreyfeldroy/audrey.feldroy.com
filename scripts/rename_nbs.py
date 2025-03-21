#!/usr/bin/env python

# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/2025-02-04-How-to-Turn-a-Jupyter-Notebook-Into-a-Python-Script.ipynb.

# %% auto 0
__all__ = ['generate_title_part', 'rename_notebook', 'get_untitled_nbs']

# %% ../nbs/2025-02-04-How-to-Turn-a-Jupyter-Notebook-Into-a-Python-Script.ipynb 7
from datetime import datetime
from fastcore.utils import *
import google.generativeai as genai
from nbdev.export import nb_export
from pathlib import Path

# %% ../nbs/2025-02-04-How-to-Turn-a-Jupyter-Notebook-Into-a-Python-Script.ipynb 8
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

# %% ../nbs/2025-02-04-How-to-Turn-a-Jupyter-Notebook-Into-a-Python-Script.ipynb 9
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

# %% ../nbs/2025-02-04-How-to-Turn-a-Jupyter-Notebook-Into-a-Python-Script.ipynb 10
def get_untitled_nbs(nbs_path): return L(Path(nbs_path).expanduser().glob("Untitled*.ipynb"))

# %% ../nbs/2025-02-04-How-to-Turn-a-Jupyter-Notebook-Into-a-Python-Script.ipynb 11
if __name__ == '__main__':
    nbs = get_untitled_nbs("~/fun/arg-drafts")
    new_paths = nbs.map(rename_notebook)
