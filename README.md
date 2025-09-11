# audrey.feldroy.com

Welcome to audrey.feldroy.com! 🌟

This is my blog. I created it this way because I love experimenting with Python in notebooks, and I found blogging platforms using Markdown files or content in databases too limiting.

It's designed to make it as easy and fun as possible for me to blog, by allowing me to:

* Create blog posts as standard .ipynb files
* Render blog posts as beautiful, fast-loading HTML blog posts with the power of [Air, our new Python web framework](https://github.com/feldroy/air) which is built on Starlette, FastAPI, and Pydantic.
* Get right to blogging with no extra front matter to remember. The notebook's title is the blog post title.

## Why This Matters

Jupyter notebooks are such a joy to experiment in! My goal here is to make turning those experiments into blog posts just as effortless. 

## About the Blog Posts

This started off with me copying the notebooks from https://github.com/audreyfeldroy/til/tree/main/nbs to articles/
and then it turned into my real blog.

## Quickstart

Clone this repo, then:

```sh
uv tool install rust-just
uv venv
source .venv/bin/activate
uv sync
just dev
```
