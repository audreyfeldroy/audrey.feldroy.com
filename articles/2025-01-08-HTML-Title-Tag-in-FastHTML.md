# HTML Title Tag in FastHTML

I get so lazy about title tags. The point of today's notebook is to make me less lazy, so I actually fix the title of this site. Oh, and to explore `Title` and `Titled` in FastHTML.


```python
from fasthtml.common import *
from fasthtml.jupyter import *
from nb2fasthtml.core import render_nb
```

To create a `<title>` tag, you use the Title FT:


```python
Title("Hey")
```




```html
<title>Hey</title>

```



`Titled` is a shortcut to give you `<title>` and `<h1>` containing the same thing, with the `<h1>` wrapped in a main container:


```python
to_xml(Titled("Hey this is Titled"))
```




    '<title>Hey this is Titled</title>\n<main class="container">  <h1>Hey this is Titled</h1>\n</main>'



It doesn't make much sense until you add a list of FTs to `Titled`:


```python
print(to_xml(Titled("Hey this is Titled", P("Here's some page content in a paragraph."), 
             Div(P("And here's a paragraph in a div.")),
             Ol(Li("You can add stuff here"), Li("And more stuff"), Li("And the page can go on and on.")))))
```

    <title>Hey this is Titled</title>
    <main class="container">  <h1>Hey this is Titled</h1>
      <p>Here&#x27;s some page content in a paragraph.</p>
      <div>
        <p>And here&#x27;s a paragraph in a div.</p>
      </div>
      <ol>
        <li>You can add stuff here</li>
        <li>And more stuff</li>
        <li>And the page can go on and on.</li>
      </ol>
    </main>


## FastHTML App With Titled Pages

Here's a FastHTML app I'm running from this notebook. 


```python
app,rt = fast_app(pico=False)
```


```python
@rt
def index():
    return Titled("My Homepage",
        Div(P("This page has a title and h1.")),
        P("Here's some page content in a paragraph."), 
        Div(P("And here's a paragraph in a div.")),
        Ol(Li("You can add stuff here"), Li("And more stuff"), Li("The page can go on and on.")))
```


```python
server = JupyUvi(app)
```



<script>
document.body.addEventListener('htmx:configRequest', (event) => {
    if(event.detail.path.includes('://')) return;
    htmx.config.selfRequestsOnly=false;
    event.detail.path = `${location.protocol}//${location.hostname}:8000${event.detail.path}`;
});
</script>



```python
@rt('/pages/{title}')
def page(title:str):
    return Titled(title,
        Div(P("The title and h1 match the title page URL slug")))
```


```python
server.stop()
```

## Titles From `nb2fasthtml`


```python
name = "2025-01-07-Verifying-Bluesky-Domain-in-FastHTML"
css = ':root {font-family: system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", sans-serif;} p {line-height: 1.5;}'
nb = Path(f'{name}.ipynb')
```

`render_nb` from the `nb2fasthtml` package already turns the notebook's title into an h1, but it appears it doesn't add a title tag.

To get around that, I have my notebook route handler return:


```python
r = (Title(name[11:].replace('-', ' ').replace('_', ' ')),
Style(css),
render_nb(nb, wrapper=Div))
r
```




    (title(('Verifying Bluesky Domain in FastHTML',),{}),
     style((':root {font-family: system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", sans-serif;} p {line-height: 1.5;}',),{}),
     div((div((h1(('Verifying a Bluesky Domain Handle on a FastHTML Site',),{}),),{'class': 'frontmatter'}), div((div(('I just changed my Bluesky to [@audrey.feldroy.com](https://bsky.app/profile/audrey.feldroy.com). To verify my domain ownership, I added this route handler to my FastHTML website:',),{'class': 'marked'}),),{}), article((div(("\n```python\n@rt('/.well-known/{fname}')\ndef wellknown(fname: str):\n    return Path(f'.well-known/{fname}').read_text()\n```\n",),{'class': 'marked'}), ''),{}), div((div(("In my website's repo [arg-blog-fasthtml](https://github.com/audreyfeldroy/arg-blog-fasthtml) I created a `.well-known` directory.",),{'class': 'marked'}),),{}), div((div(('Within that, I created a file called `atproto-did`, containing the verification text string shown under:\n\n> https://bsky.app/settings/account > Change Handle > I have my own domain > No DNS Panel',),{'class': 'marked'}),),{}), div((div(('Then I redeployed my site and clicked the *Verify Text File* button, and my handle was updated.',),{'class': 'marked'}),),{}), div((div(('## A Full Minimal FastHTML App for This',),{'class': 'marked'}),),{}), div((div(("If you have a domain but no website yet, here's a FastHTML app for verifying your domain as your Bluesky handle:",),{'class': 'marked'}),),{}), article((div(('\n```python\nfrom fasthtml.common import *\n\napp,rt = fast_app()\n\n@rt\ndef get(): return Div(P("Welcome to my homepage!"))\n\n@rt(\'/.well-known/{fname}\')\ndef wellknown(fname: str):\n    return Path(f\'.well-known/{fname}\').read_text()\n\nserve()\n```\n',),{'class': 'marked'}), ''),{}), article((div(('\n```python\nThen add the `.well-known/atproto-did` file, deploy, and verify.\n```\n',),{'class': 'marked'}), ''),{})),{'class': 'container'}))



Which we can see generally more readably with:


```python
print(to_xml(r))
```

    <title>Verifying Bluesky Domain in FastHTML</title>
    <style>:root {font-family: system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", sans-serif;} p {line-height: 1.5;}</style>
    <div class="container">
      <div class="frontmatter">
        <h1>Verifying a Bluesky Domain Handle on a FastHTML Site</h1>
      </div>
      <div>
        <div class="marked">I just changed my Bluesky to [@audrey.feldroy.com](https://bsky.app/profile/audrey.feldroy.com). To verify my domain ownership, I added this route handler to my FastHTML website:</div>
      </div>
      <article>
        <div class="marked">
    ```python
    @rt(&#x27;/.well-known/{fname}&#x27;)
    def wellknown(fname: str):
        return Path(f&#x27;.well-known/{fname}&#x27;).read_text()
    ```
    </div>
      </article>
      <div>
        <div class="marked">In my website&#x27;s repo [arg-blog-fasthtml](https://github.com/audreyfeldroy/arg-blog-fasthtml) I created a `.well-known` directory.</div>
      </div>
      <div>
        <div class="marked">Within that, I created a file called `atproto-did`, containing the verification text string shown under:
    
    &gt; https://bsky.app/settings/account &gt; Change Handle &gt; I have my own domain &gt; No DNS Panel</div>
      </div>
      <div>
        <div class="marked">Then I redeployed my site and clicked the *Verify Text File* button, and my handle was updated.</div>
      </div>
      <div>
        <div class="marked">## A Full Minimal FastHTML App for This</div>
      </div>
      <div>
        <div class="marked">If you have a domain but no website yet, here&#x27;s a FastHTML app for verifying your domain as your Bluesky handle:</div>
      </div>
      <article>
        <div class="marked">
    ```python
    from fasthtml.common import *
    
    app,rt = fast_app()
    
    @rt
    def get(): return Div(P(&quot;Welcome to my homepage!&quot;))
    
    @rt(&#x27;/.well-known/{fname}&#x27;)
    def wellknown(fname: str):
        return Path(f&#x27;.well-known/{fname}&#x27;).read_text()
    
    serve()
    ```
    </div>
      </article>
      <article>
        <div class="marked">
    ```python
    Then add the `.well-known/atproto-did` file, deploy, and verify.
    ```
    </div>
      </article>
    </div>
    

