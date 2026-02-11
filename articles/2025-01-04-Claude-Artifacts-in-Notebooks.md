# Showing Claude Artifacts in Jupyter Notebooks

I prompted Claude 3.5 Sonnet to make an HTML and vanilla JS birthday app for my daughter who just turned six. Then I figured out how to show the artifact inline in a Jupyter notebook.

## Setup

```python
from fastcore.all import *
from fasthtml.common import *
from fasthtml.jupyter import *
from IPython.display import IFrame
from pathlib import *
```

## Prompt for HTML and Vanilla JS

I prompted Claude 3.5 Sonnet with:

> Make an HTML and vanilla JS birthday app for my daughter who just turned six

The `HTML and vanilla JS` part is important. Otherwise it'll make React artifacts which I don't want.

Then I downloaded the artifact it generated to https://github.com/audreyfeldroy/arg-static/tree/main/artifacts-html/2025-01-04

## Inline Display in an IFrame

To show the artifact in a Jupyter notebook iframe:


```python
IFrame(src="https://audreyfeldroy.github.io/arg-static/artifacts-html/2025-01-04/birthday-app.html", width=700, height=600)
```





<iframe
    width="700"
    height="600"
    src="https://audreyfeldroy.github.io/arg-static/artifacts-html/2025-01-04/birthday-app.html"
    frameborder="0"
    allowfullscreen

></iframe>




## New Artifact: 3D Shape Coloring App

She then asked me to make her a coloring app. Yesterday she asked me how it was possible to draw 3D shapes, so I prompted:

> Create a simple HTML and vanilla JS coloring app for my daughter. Show 3D shapes that she can use the paint bucket to color.


```python
IFrame(src="https://audreyfeldroy.github.io/arg-static/artifacts-html/2025-01-04/3D-shape-coloring-app.html", width=800, height=700)
```





<iframe
    width="800"
    height="700"
    src="https://audreyfeldroy.github.io/arg-static/artifacts-html/2025-01-04/3D-shape-coloring-app.html"
    frameborder="0"
    allowfullscreen

></iframe>



