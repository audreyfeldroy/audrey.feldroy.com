# 2023-07-29-Blogging-With-nbdev

# Setting Up a Blog With nbdev
I feel like Jupyter notebooks would be really nice for blogging or publishing "Today I Learned" posts. I had heard about Fastpages before via Jeremy Howard's blog or YouTube videos, but seeing that it was deprecated in favor of nbdev, I decided to try nbdev.
I followed the [End-to-End Walkthrough nbdev tutorial](https://nbdev.fast.ai/tutorials/tutorial.html).
## Things I Learned

### Best for Python Packages

nbdev works best out-of-the-box for the use case where you want to create a Python package out of auto-exporting Jupyter notebooks.

For regular blogging you have to experiment a bit to make that work. I'm still figuring that out.

The nbdev docs point to Quarto which appears to be something like Jekyll. I believe it would be good to use nbdev with Quatro in order to publish Jupyter notebook-based blog posts, but I haven't tried that yet.

### Make the Package and Repository Name the Same

It's hard to configure the package name to be different from the repository name. I tried this in settings.ini:

```
lib_name = tilly
```

And I tried various combinations of running the notebooks to export a new package, but the package directory generated was always `til`.

I don't actually want to release a package named `til` or `tilly` to PyPI, or at all for that matter, but I like the name `til` for this repo.

### What Now?

This isn't actually my blog, but more my playground for learning. I'm keeping nbdev in order to practice creating notebooks that are exportable as Python packages.

My main blog is at [audrey.feldroy.com](https://audrey.feldroy.com/), but I'll continue playing in notebooks here.