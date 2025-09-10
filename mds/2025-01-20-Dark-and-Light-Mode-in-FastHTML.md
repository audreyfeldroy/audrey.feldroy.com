# Dark and Light Mode in FastHTML

How to make a website check the user's preferred mode and set the background appropriately.


```python
from fasthtml.common import *
from fasthtml.jupyter import *
from fastcore.utils import *
```

## Compare a Page in Both Modes

Open your website in 2 Chrome profiles, one with light and one with dark mode. For example, in mine I noticed:

* In light mode, the page and code examples correctly had light backgrounds
* In dark mode, the code examples correctly had dark backgrounds, but the page incorrectly had a light background.

This told me that I need to modify the page background styles depending on the preferred mode.

### Try Emulating Preference Manually

In Chrome, go to `Option` `Cmd` `c` to open "Inspect Elements" > Elements > Styles. Click the upside-down paintbrush icon to bring up a menu of:

* `prefers-color-scheme: light`
* `prefers-color-scheme: dark`
* Automatic dark mode (or whatever mode your laptop is in)

## To Update a FastHTML `main.py` With `color-scheme`

### Step 1: Enable light-dark Support

To enable support for the CSS light-dark() color function, you set this on `:root`:


```python
Style(':root {color-scheme: light dark;}')
```




```html
<style>:root {color-scheme: light dark;}</style>

```



This allows your site to respect the user's light or dark mode preference.

### Step 2: Use the light-dark Function

Now wherever you specify CSS colors, you can specify a pair of colors.


```python
Style('body {background-color: light-dark(#ffffff, #1a1a1a); color: light-dark(#1a1a1a, #ffffff);}')
```




```html
<style>body {background-color: light-dark(#ffffff, #1a1a1a); color: light-dark(#1a1a1a, #ffffff);}</style>

```



Here in this example:

* The first color `#ffffff` is `<body>`'s background color in light mode
* The first color `#1a1a1a` is `<body>`'s background color in dark mode

If you use these values a lot, define CSS variables `--light-*` and `--dark-*`

### Step 3: Factor Out CSS Variables (Optional)

If you find yourself repeating color constants a lot, define CSS variables in `:root` and use them in `light-dark()` like:


```python
Style(""":root {color-scheme: light dark; --lightshade: #ffffff; --darkshade: #1a1a1a;}

body {background-color: light-dark(var(--lightshade), var(--darkshade))};""")
```




```html
<style>:root {color-scheme: light dark; --lightshade: #ffffff; --darkshade: #1a1a1a;}

body {background-color: light-dark(var(--lightshade), var(--darkshade))};</style>

```



## Example

Here I create a component with light-dark colors. The component respects light/dark mode preference. I need stuff to put into cards, so I'm grabbing my notebooks:


```python
nbs = L(Path('../arg-blog-fasthtml/nbs').glob('*.ipynb'))
nbs
```




    (#41) [Path('../arg-blog-fasthtml/nbs/2023-07-29-Blogging-With-nbdev.ipynb'),Path('../arg-blog-fasthtml/nbs/2024-12-31-Note-Box-FastTag.ipynb'),Path('../arg-blog-fasthtml/nbs/2024-07-29-Delegates-Decorator.ipynb'),Path('../arg-blog-fasthtml/nbs/2024-07-29-Auth-in-FastHTML.ipynb'),Path('../arg-blog-fasthtml/nbs/2025-01-09-Reading-and-Writing-Jupyter-Notebooks-With-Python.ipynb'),Path('../arg-blog-fasthtml/nbs/2025-01-06-Understanding-FastHTML-Headers.ipynb'),Path('../arg-blog-fasthtml/nbs/2025-01-10-Understanding-FastHTML-Routes-Requests-and-Redirects.ipynb'),Path('../arg-blog-fasthtml/nbs/2024-07-16_Xtend_Pico.ipynb'),Path('../arg-blog-fasthtml/nbs/2024-12-28-Minimal-Typography-for-FastHTML-Apps.ipynb'),Path('../arg-blog-fasthtml/nbs/2024-12-26-Showing-FTs-in-Jupyter-Notebooks.ipynb'),Path('../arg-blog-fasthtml/nbs/2025-01-04-Claude-Artifacts-in-Notebooks.ipynb'),Path('../arg-blog-fasthtml/nbs/2025-01-05-SSH-Agent-to-Save-Passphrase-Typing.ipynb'),Path('../arg-blog-fasthtml/nbs/2024-12-27-Notebook-Names-to-Cards.ipynb'),Path('../arg-blog-fasthtml/nbs/2025-01-11-NBClassic-Keyboard-Shortcuts-in-Command-and-Dual-Mode.ipynb'),Path('../arg-blog-fasthtml/nbs/2025-01-01-FastHTML-Piano-Part-1.ipynb'),Path('../arg-blog-fasthtml/nbs/2025-01-18-Alarm-Sounds-App.ipynb'),Path('../arg-blog-fasthtml/nbs/2025-01-07-Verifying-Bluesky-Domain-in-FastHTML.ipynb'),Path('../arg-blog-fasthtml/nbs/2024-12-24-Trying-execnb.ipynb'),Path('../arg-blog-fasthtml/nbs/2025-01-01-Command-Substitution-in-Bash.ipynb'),Path('../arg-blog-fasthtml/nbs/2024-08-05-Claudette-FastHTML.ipynb')...]




```python
def LightDarkNotebookCard(nb):
    "A card showing notebook info"
    return Div(H3(nb.name), P("Lorem ipsum dolor sit amet."), style="border: 3px solid light-dark(#eaeaea, #111111); padding: 10px; margin: 2px; border-radius: 4px; background-color: light-dark(#eeeeee, #1a1a1a); color: light-dark(#1a1a1a, #eeeeee);")
show(LightDarkNotebookCard(nbs[0]))
```


<div style="border: 3px solid light-dark(#eaeaea, #111111); padding: 10px; margin: 2px; border-radius: 4px; background-color: light-dark(#eeeeee, #1a1a1a); color: light-dark(#1a1a1a, #eeeeee);">
  <h3>2023-07-29-Blogging-With-nbdev.ipynb</h3>
  <p>Lorem ipsum dolor sit amet.</p>
</div>
<script>if (window.htmx) htmx.process(document.body)</script>


It's nice to create a rough component, then use AI to iterate on the design. Here I pasted my code into Claude with the prompt:

> Make these FastHTML cards look better. No React or Tailwind, please.

That gave me this improved card FT component:


```python
def LightDarkNotebookCard(nb):
    "A card showing notebook info with enhanced styling"
    return Div(
        H3(nb.name, style="margin: 0 0 12px 0; font-size: 1.3em;"),
        P("Lorem ipsum dolor sit amet.", 
          style="margin: 0; line-height: 1.5; opacity: 0.9;"),
        style="""
            border: 1px solid light-dark(#e0e0e0, #333333);
            padding: 20px;
            margin: 8px;
            border-radius: 8px;
            background-color: light-dark(#ffffff, #222222);
            color: light-dark(#1a1a1a, #ffffff);
            box-shadow: 0 2px 4px light-dark(rgba(0,0,0,0.05), rgba(0,0,0,0.2));
            transition: all 0.2s ease;
            cursor: pointer;
        """,
        onmouseover="""
            this.style.transform = 'translateY(-2px)';
            this.style.boxShadow = '0 4px 8px light-dark(rgba(0,0,0,0.1), rgba(0,0,0,0.3))';
        """,
        onmouseout="""
            this.style.transform = 'translateY(0)';
            this.style.boxShadow = '0 2px 4px light-dark(rgba(0,0,0,0.05), rgba(0,0,0,0.2))';
        """
    )

show(LightDarkNotebookCard(nbs[0]))
```


<div onmouseover="
            this.style.transform = 'translateY(-2px)';
            this.style.boxShadow = '0 4px 8px light-dark(rgba(0,0,0,0.1), rgba(0,0,0,0.3))';
        " onmouseout="
            this.style.transform = 'translateY(0)';
            this.style.boxShadow = '0 2px 4px light-dark(rgba(0,0,0,0.05), rgba(0,0,0,0.2))';
        " style="
            border: 1px solid light-dark(#e0e0e0, #333333);
            padding: 20px;
            margin: 8px;
            border-radius: 8px;
            background-color: light-dark(#ffffff, #222222);
            color: light-dark(#1a1a1a, #ffffff);
            box-shadow: 0 2px 4px light-dark(rgba(0,0,0,0.05), rgba(0,0,0,0.2));
            transition: all 0.2s ease;
            cursor: pointer;
        ">
  <h3 style="margin: 0 0 12px 0; font-size: 1.3em;">2023-07-29-Blogging-With-nbdev.ipynb</h3>
  <p style="margin: 0; line-height: 1.5; opacity: 0.9;">Lorem ipsum dolor sit amet.</p>
</div>
<script>if (window.htmx) htmx.process(document.body)</script>


Here I map them to a handful of list items, to make them look more realistic:


```python
def LightDarkList(nbs):
    "FT component that returns a list of notebooks"
    return Div(*nbs.map(LightDarkNotebookCard), style="columns: 3;")
show(to_xml(LightDarkList(nbs[:9])))
```


<div style="columns: 3;">
  <div onmouseover="
            this.style.transform = 'translateY(-2px)';
            this.style.boxShadow = '0 4px 8px light-dark(rgba(0,0,0,0.1), rgba(0,0,0,0.3))';
        " onmouseout="
            this.style.transform = 'translateY(0)';
            this.style.boxShadow = '0 2px 4px light-dark(rgba(0,0,0,0.05), rgba(0,0,0,0.2))';
        " style="
            border: 1px solid light-dark(#e0e0e0, #333333);
            padding: 20px;
            margin: 8px;
            border-radius: 8px;
            background-color: light-dark(#ffffff, #222222);
            color: light-dark(#1a1a1a, #ffffff);
            box-shadow: 0 2px 4px light-dark(rgba(0,0,0,0.05), rgba(0,0,0,0.2));
            transition: all 0.2s ease;
            cursor: pointer;
        ">
    <h3 style="margin: 0 0 12px 0; font-size: 1.3em;">2023-07-29-Blogging-With-nbdev.ipynb</h3>
    <p style="margin: 0; line-height: 1.5; opacity: 0.9;">Lorem ipsum dolor sit amet.</p>
  </div>
  <div onmouseover="
            this.style.transform = 'translateY(-2px)';
            this.style.boxShadow = '0 4px 8px light-dark(rgba(0,0,0,0.1), rgba(0,0,0,0.3))';
        " onmouseout="
            this.style.transform = 'translateY(0)';
            this.style.boxShadow = '0 2px 4px light-dark(rgba(0,0,0,0.05), rgba(0,0,0,0.2))';
        " style="
            border: 1px solid light-dark(#e0e0e0, #333333);
            padding: 20px;
            margin: 8px;
            border-radius: 8px;
            background-color: light-dark(#ffffff, #222222);
            color: light-dark(#1a1a1a, #ffffff);
            box-shadow: 0 2px 4px light-dark(rgba(0,0,0,0.05), rgba(0,0,0,0.2));
            transition: all 0.2s ease;
            cursor: pointer;
        ">
    <h3 style="margin: 0 0 12px 0; font-size: 1.3em;">2024-12-31-Note-Box-FastTag.ipynb</h3>
    <p style="margin: 0; line-height: 1.5; opacity: 0.9;">Lorem ipsum dolor sit amet.</p>
  </div>
  <div onmouseover="
            this.style.transform = 'translateY(-2px)';
            this.style.boxShadow = '0 4px 8px light-dark(rgba(0,0,0,0.1), rgba(0,0,0,0.3))';
        " onmouseout="
            this.style.transform = 'translateY(0)';
            this.style.boxShadow = '0 2px 4px light-dark(rgba(0,0,0,0.05), rgba(0,0,0,0.2))';
        " style="
            border: 1px solid light-dark(#e0e0e0, #333333);
            padding: 20px;
            margin: 8px;
            border-radius: 8px;
            background-color: light-dark(#ffffff, #222222);
            color: light-dark(#1a1a1a, #ffffff);
            box-shadow: 0 2px 4px light-dark(rgba(0,0,0,0.05), rgba(0,0,0,0.2));
            transition: all 0.2s ease;
            cursor: pointer;
        ">
    <h3 style="margin: 0 0 12px 0; font-size: 1.3em;">2024-07-29-Delegates-Decorator.ipynb</h3>
    <p style="margin: 0; line-height: 1.5; opacity: 0.9;">Lorem ipsum dolor sit amet.</p>
  </div>
  <div onmouseover="
            this.style.transform = 'translateY(-2px)';
            this.style.boxShadow = '0 4px 8px light-dark(rgba(0,0,0,0.1), rgba(0,0,0,0.3))';
        " onmouseout="
            this.style.transform = 'translateY(0)';
            this.style.boxShadow = '0 2px 4px light-dark(rgba(0,0,0,0.05), rgba(0,0,0,0.2))';
        " style="
            border: 1px solid light-dark(#e0e0e0, #333333);
            padding: 20px;
            margin: 8px;
            border-radius: 8px;
            background-color: light-dark(#ffffff, #222222);
            color: light-dark(#1a1a1a, #ffffff);
            box-shadow: 0 2px 4px light-dark(rgba(0,0,0,0.05), rgba(0,0,0,0.2));
            transition: all 0.2s ease;
            cursor: pointer;
        ">
    <h3 style="margin: 0 0 12px 0; font-size: 1.3em;">2024-07-29-Auth-in-FastHTML.ipynb</h3>
    <p style="margin: 0; line-height: 1.5; opacity: 0.9;">Lorem ipsum dolor sit amet.</p>
  </div>
  <div onmouseover="
            this.style.transform = 'translateY(-2px)';
            this.style.boxShadow = '0 4px 8px light-dark(rgba(0,0,0,0.1), rgba(0,0,0,0.3))';
        " onmouseout="
            this.style.transform = 'translateY(0)';
            this.style.boxShadow = '0 2px 4px light-dark(rgba(0,0,0,0.05), rgba(0,0,0,0.2))';
        " style="
            border: 1px solid light-dark(#e0e0e0, #333333);
            padding: 20px;
            margin: 8px;
            border-radius: 8px;
            background-color: light-dark(#ffffff, #222222);
            color: light-dark(#1a1a1a, #ffffff);
            box-shadow: 0 2px 4px light-dark(rgba(0,0,0,0.05), rgba(0,0,0,0.2));
            transition: all 0.2s ease;
            cursor: pointer;
        ">
    <h3 style="margin: 0 0 12px 0; font-size: 1.3em;">2025-01-09-Reading-and-Writing-Jupyter-Notebooks-With-Python.ipynb</h3>
    <p style="margin: 0; line-height: 1.5; opacity: 0.9;">Lorem ipsum dolor sit amet.</p>
  </div>
  <div onmouseover="
            this.style.transform = 'translateY(-2px)';
            this.style.boxShadow = '0 4px 8px light-dark(rgba(0,0,0,0.1), rgba(0,0,0,0.3))';
        " onmouseout="
            this.style.transform = 'translateY(0)';
            this.style.boxShadow = '0 2px 4px light-dark(rgba(0,0,0,0.05), rgba(0,0,0,0.2))';
        " style="
            border: 1px solid light-dark(#e0e0e0, #333333);
            padding: 20px;
            margin: 8px;
            border-radius: 8px;
            background-color: light-dark(#ffffff, #222222);
            color: light-dark(#1a1a1a, #ffffff);
            box-shadow: 0 2px 4px light-dark(rgba(0,0,0,0.05), rgba(0,0,0,0.2));
            transition: all 0.2s ease;
            cursor: pointer;
        ">
    <h3 style="margin: 0 0 12px 0; font-size: 1.3em;">2025-01-06-Understanding-FastHTML-Headers.ipynb</h3>
    <p style="margin: 0; line-height: 1.5; opacity: 0.9;">Lorem ipsum dolor sit amet.</p>
  </div>
  <div onmouseover="
            this.style.transform = 'translateY(-2px)';
            this.style.boxShadow = '0 4px 8px light-dark(rgba(0,0,0,0.1), rgba(0,0,0,0.3))';
        " onmouseout="
            this.style.transform = 'translateY(0)';
            this.style.boxShadow = '0 2px 4px light-dark(rgba(0,0,0,0.05), rgba(0,0,0,0.2))';
        " style="
            border: 1px solid light-dark(#e0e0e0, #333333);
            padding: 20px;
            margin: 8px;
            border-radius: 8px;
            background-color: light-dark(#ffffff, #222222);
            color: light-dark(#1a1a1a, #ffffff);
            box-shadow: 0 2px 4px light-dark(rgba(0,0,0,0.05), rgba(0,0,0,0.2));
            transition: all 0.2s ease;
            cursor: pointer;
        ">
    <h3 style="margin: 0 0 12px 0; font-size: 1.3em;">2025-01-10-Understanding-FastHTML-Routes-Requests-and-Redirects.ipynb</h3>
    <p style="margin: 0; line-height: 1.5; opacity: 0.9;">Lorem ipsum dolor sit amet.</p>
  </div>
  <div onmouseover="
            this.style.transform = 'translateY(-2px)';
            this.style.boxShadow = '0 4px 8px light-dark(rgba(0,0,0,0.1), rgba(0,0,0,0.3))';
        " onmouseout="
            this.style.transform = 'translateY(0)';
            this.style.boxShadow = '0 2px 4px light-dark(rgba(0,0,0,0.05), rgba(0,0,0,0.2))';
        " style="
            border: 1px solid light-dark(#e0e0e0, #333333);
            padding: 20px;
            margin: 8px;
            border-radius: 8px;
            background-color: light-dark(#ffffff, #222222);
            color: light-dark(#1a1a1a, #ffffff);
            box-shadow: 0 2px 4px light-dark(rgba(0,0,0,0.05), rgba(0,0,0,0.2));
            transition: all 0.2s ease;
            cursor: pointer;
        ">
    <h3 style="margin: 0 0 12px 0; font-size: 1.3em;">2024-07-16_Xtend_Pico.ipynb</h3>
    <p style="margin: 0; line-height: 1.5; opacity: 0.9;">Lorem ipsum dolor sit amet.</p>
  </div>
  <div onmouseover="
            this.style.transform = 'translateY(-2px)';
            this.style.boxShadow = '0 4px 8px light-dark(rgba(0,0,0,0.1), rgba(0,0,0,0.3))';
        " onmouseout="
            this.style.transform = 'translateY(0)';
            this.style.boxShadow = '0 2px 4px light-dark(rgba(0,0,0,0.05), rgba(0,0,0,0.2))';
        " style="
            border: 1px solid light-dark(#e0e0e0, #333333);
            padding: 20px;
            margin: 8px;
            border-radius: 8px;
            background-color: light-dark(#ffffff, #222222);
            color: light-dark(#1a1a1a, #ffffff);
            box-shadow: 0 2px 4px light-dark(rgba(0,0,0,0.05), rgba(0,0,0,0.2));
            transition: all 0.2s ease;
            cursor: pointer;
        ">
    <h3 style="margin: 0 0 12px 0; font-size: 1.3em;">2024-12-28-Minimal-Typography-for-FastHTML-Apps.ipynb</h3>
    <p style="margin: 0; line-height: 1.5; opacity: 0.9;">Lorem ipsum dolor sit amet.</p>
  </div>
</div>
<script>if (window.htmx) htmx.process(document.body)</script>


## FastHTML App

You can see this component in action by creating a little FastHTML app with this `:root` style:


```python
app, rt = fast_app(hdrs=(picolink, Style(':root {color-scheme: light dark;}')))
```


```python
@rt
def index():
    return Main(H1("My Site"), LightDarkList(nbs[:9]))
```

I run this app from my notebook via the next line. If using a `main.py`, replace it with `serve()`.


```python
# server = JupyUvi(app)
```



<script>
document.body.addEventListener('htmx:configRequest', (event) => {
    if(event.detail.path.includes('://')) return;
    htmx.config.selfRequestsOnly=false;
    event.detail.path = `${location.protocol}//${location.hostname}:8000${event.detail.path}`;
});
</script>



```python
# server.stop()
```

## Takeaways

1. Set `color-scheme: light dark` in `:root` to respect the user's dark/light mode preference.
2. Use the `light-dark()` function to set properties based on mode
3. Refactor colors into CSS variables if needed
