# Images in Jupyter Notebooks, in Every Way

This notebook uses images in every possible way. 


```python
from fasthtml.common import *
from IPython.display import Image
from IPython.core.display import HTML
```

## Image from `IPython.display`

This works well, but if the image later changes, it doesn't update:


```python
Image(url="https://audreyfeldroy.github.io/arg-static/img/2024-12-30-Images-in-Jupyter-Notebooks.webp", width=300, height=171)
```




<img src="https://audreyfeldroy.github.io/arg-static/img/2024-12-30-Images-in-Jupyter-Notebooks.webp" width="300" height="171"/>




```python
Image(url="https://audreyfeldroy.github.io/arg-static/img/2024-12-30-Images-in-Jupyter-Notebooks.webp", width=150, height=85)
```




<img src="https://audreyfeldroy.github.io/arg-static/img/2024-12-30-Images-in-Jupyter-Notebooks.webp" width="150" height="85"/>



## HTML

Interestingly this shows the old image from above rather than getting it fresh:


```python
%%html
<img src="https://audreyfeldroy.github.io/arg-static/img/2024-12-30-Images-in-Jupyter-Notebooks.webp" width="150" height="85" />
```


<img src="https://audreyfeldroy.github.io/arg-static/img/2024-12-30-Images-in-Jupyter-Notebooks.webp" width="150" height="85" />



## HTML Image Cache Busting

Note: I've since updated this post and don't have the old version around anymore, but the `?t=123` trick is still valid.

Let's try busting its image cache:


```python
%%html
<img src="https://audreyfeldroy.github.io/arg-static/img/2024-12-30-Images-in-Jupyter-Notebooks.webp?t=4534" width="150" height="85" />
```


<img src="https://audreyfeldroy.github.io/arg-static/img/2024-12-30-Images-in-Jupyter-Notebooks.webp?t=4534" width="150" height="85" />



That updated it!

This still shows the old version:


```python
%%html
<img src="https://audreyfeldroy.github.io/arg-static/img/2024-12-30-Images-in-Jupyter-Notebooks.webp" width="150" height="85" />
```


<img src="https://audreyfeldroy.github.io/arg-static/img/2024-12-30-Images-in-Jupyter-Notebooks.webp" width="150" height="85" />



## Markdown Image Embedded in Notebook

Create a cell, convert it to Markdown, and drag the image in. It creates a Markdown image with the image as an attachment.

![2024-12-30-Images-in-Jupyter-Notebooks-150x85.webp](2024-12-30-Images-In-Every-Way-In-Notebooks_files/2024-12-30-Images-in-Jupyter-Notebooks-150x85.webp)

The Markdown for the cell above looks like: 

`![2024-12-30-Images-in-Jupyter-Notebooks-150x85.webp](attachment:2024-12-30-Images-in-Jupyter-Notebooks-150x85.webp)`

## Markdown Image From Local Dir in Repo

Here I use Markdown to show an image from the img directory of this repo, like this:

`![My test image for use in Jupyter Notebooks](../img/2024-12-30-Images-in-Jupyter-Notebooks-150x85.webp)`

![My test image for use in Jupyter Notebooks](../img/2024-12-30-Images-in-Jupyter-Notebooks-150x85.webp)

## No Markdown Remote URL to Image

Markdown with a remote image URL doesn't seem to work:

`![title]("https://audreyfeldroy.github.io/arg-static/img/2024-12-30-Images-in-Jupyter-Notebooks.webp")`

![title]("https://audreyfeldroy.github.io/arg-static/img/2024-12-30-Images-in-Jupyter-Notebooks.webp")

(Message me if you know how to get that working.)

## FastHTML Image

Here I use the `Img` FastTag from FastHTML:


```python
i = Img(src="https://audreyfeldroy.github.io/arg-static/img/2024-12-30-Images-in-Jupyter-Notebooks.webp?t=312")
i
```




```html
<img src="https://audreyfeldroy.github.io/arg-static/img/2024-12-30-Images-in-Jupyter-Notebooks.webp?t=312">
```



I call `show` to display a FastTag in a notebook:


```python
show(i)
```


<img src="https://audreyfeldroy.github.io/arg-static/img/2024-12-30-Images-in-Jupyter-Notebooks.webp?t=312">


## Learn More

If you're as interested in this as I am, read [StackOverflow: How to embed image or picture in jupyter notebook, either from a local machine or from a web resource?](https://stackoverflow.com/q/32370281/271697)
