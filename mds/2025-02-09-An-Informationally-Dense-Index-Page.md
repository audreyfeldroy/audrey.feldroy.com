# An Informationally-Dense Index Page

Now that I have a lot of notebooks, it would be nice to have a more compact index page. I want to see more of my posts from mobile all at once. I'm going to prototype it in Tailwind.


```python
from datetime import datetime
from execnb.nbio import read_nb
from fastcore.utils import *
from fasthtml.common import *
from fasthtml.jupyter import *
from monsterui import franken
from monsterui.all import Theme
```


```python
def get_nb_paths(): 
    root = Path() if IN_NOTEBOOK else Path("nbs/")
    return L(root.glob("*.ipynb")).sorted(reverse=True)
```


```python
nbpaths = get_nb_paths()
nbpaths
```




    (#66) [Path('2025-02-09-This-Site-Is-Now-Powered-by-This-Notebook-Part-7.ipynb'),Path('2025-02-09-An-Informationally-Dense-Index-Page.ipynb'),Path('2025-02-08-This-Notebook-Is-Also-a-Keylogger.ipynb'),Path('2025-02-07-This-Site-Is-Now-Powered-by-This-Notebook-Part-6.ipynb'),Path('2025-02-06-Creating-an-Accessible-Inline-Nav-FastTag.ipynb'),Path('2025-02-05-FastHTML-Time-Converter-Part-2.ipynb'),Path('2025-02-05-Create-a-CLI-Tool-With-Fastcore-Script.ipynb'),Path('2025-02-04-How-to-Turn-a-Jupyter-Notebook-Into-a-Python-Script.ipynb'),Path('2025-02-03-FastHTML-and-MonsterUI-Time-Converter.ipynb'),Path('2025-02-02-Text-Embeddings-and-Cosine-Similarity.ipynb'),Path('2025-02-01-Auto-Renaming-My-Untitled-ipynb-Files-With-Gemini.ipynb'),Path('2025-01-31-Performance-Optimization-Moving-HTML-Class-Injection-from-lxml-to-Mistletoe.ipynb'),Path('2025-01-30-This-Site-Is-Now-Powered-by-This-Notebook-Part-5.ipynb'),Path('2025-01-29-This-Site-Is-Now-Powered-by-This-Notebook-Part-4.ipynb'),Path('2025-01-28-Functional-Programming-with-datetime-and-Omni-Timezone-Discord-Timestamps.ipynb'),Path('2025-01-27-This-Site-Is-Now-Powered-by-This-Notebook-Part-3.ipynb'),Path('2025-01-26-Improving-Pygments-Code-Block-Display.ipynb'),Path('2025-01-25-This-Site-Is-Now-Powered-by-This-Notebook-Part-2.ipynb'),Path('2025-01-24-Creating-In-Notebook-Images-for-Social-Media-With-PIL-Pillow.ipynb'),Path('2025-01-23-Troubleshooting-MonsterUI-on-This-Site.ipynb')...]



## Use tighter notebook links instead of notebook cards


```python
def get_date_from_iso8601_prefix(fname):
    "Gets date from first 10 chars YYYY-MM-DD of `fname`, where `fname` is like `2025-01-12-Get-Date-From-This.whatever"
    try:
        return datetime.fromisoformat(str(fname)[0:10])
    except ValueError: return datetime.now()
```


```python
def get_title_and_desc(fpath):
    nb = read_nb(fpath)
    title = nb.cells[0].source.lstrip("# ")
    desc = nb.cells[1].source
    return title,desc
```


```python
app,rt = fast_app(pico=False)
```


```python
def NBLink(title, desc, href, date):
    return Div(
        A(f"{date:%b %-d} • {title}", href=href, cls="text-md font-semibold hover:text-blue-600 no-underline block"),
        P(desc, cls="text-s text-gray-500 mt-0.5 mb-2"),
        cls="py-1 break-inside-avoid")
```


```python
def mk_nblink_from_nbpath(nbpath):
    date = get_date_from_iso8601_prefix(nbpath.name) or datetime.now()
    return NBLink(*get_title_and_desc(nbpath), href=f'/nbs/{nbpath.name[:-6]}', date=date)
```


```python
@rt
def index():
    nbpaths = get_nb_paths()
    return (
        Theme.blue.headers(),
        Title("audrey.feldroy.com"),
        Div(
            H1('audrey.feldroy.com', cls="text-3xl font-bold mb-2"), 
            P(
                "The experimental Jupyter notebooks of Audrey M. Roy Greenfeld. This website and all its notebooks are open-source at ", 
                A("github.com/audreyfeldroy/audrey.feldroy.com", 
                        href="https://github.com/audreyfeldroy/arg-blog-fasthtml",
                        cls="text-blue-600 hover:text-blue-800"), 
                cls="mb-8 text-gray-600"
            ),
            Table(
                *nbpaths.map(mk_nblink_from_nbpath), 
                
            ),
            cls="px-4 py-8 w-full columns-1 md:columns-2 lg:columns-3 gap-6"
        )
    )
```

Improving this visually while providing extreme information density and compactness:


```python
@rt
def index():
    nbpaths = get_nb_paths()
    return (
        Script(src="https://unpkg.com/@tailwindcss/browser@4"),
        Title("audrey.feldroy.com"),
        Div(
            H1('audrey.feldroy.com', cls="text-2xl font-bold mb-2 dark:text-gray-100"), 
            P(
                "The experimental Jupyter notebooks of Audrey M. Roy Greenfeld. This website and all its notebooks are open-source at ", 
                A("github.com/audreyfeldroy/audrey.feldroy.com", 
                        href="https://github.com/audreyfeldroy/arg-blog-fasthtml",
                        cls="text-blue-600 hover:text-blue-800 dark:text-blue-400 dark:hover:text-blue-300"), 
                cls="mb-4 text-gray-600 dark:text-gray-300 text-sm"
            ),
            Div(
                *nbpaths.map(mk_nblink_from_nbpath),
                cls="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-x-6 gap-y-2"
            ),
            cls="mx-auto px-2 py-4 dark:bg-gray-900 min-h-screen"
        ),
    )

def NBLink(title, desc, href, date):
    return Div(
        A(
            Div(
                f"{date:%b %-d}", 
                cls="text-xs font-medium text-gray-500 dark:text-gray-400"
            ),
            Div(
                title,
                cls="text-base font-medium leading-snug hover:text-blue-600 dark:text-gray-100 dark:hover:text-blue-400"
            ),
            P(
                desc,
                cls="text-xs text-gray-600 dark:text-gray-400 mt-0.5 line-clamp-2"
            ),
            href=href,
            cls="block no-underline hover:bg-gray-50 dark:hover:bg-gray-800 p-2 rounded transition-colors"
        ),
        cls="break-inside-avoid"
    )
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
HTMX(index)
```




<iframe src="http://localhost:8000/" style="width: 100%; height: auto; border: none;" onload="{
        let frame = this;
        window.addEventListener('message', function(e) {
            if (e.source !== frame.contentWindow) return; // Only proceed if the message is from this iframe
            if (e.data.height) frame.style.height = (e.data.height+1) + 'px';
        }, false);
    }" allow="accelerometer; autoplay; camera; clipboard-read; clipboard-write; display-capture; encrypted-media; fullscreen; gamepad; geolocation; gyroscope; hid; identity-credentials-get; idle-detection; magnetometer; microphone; midi; payment; picture-in-picture; publickey-credentials-get; screen-wake-lock; serial; usb; web-share; xr-spatial-tracking"></iframe> 




```python
# server.stop()
```
