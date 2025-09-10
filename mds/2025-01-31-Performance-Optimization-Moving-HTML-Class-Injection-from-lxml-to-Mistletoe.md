# Performance Optimization: Moving HTML Class Injection from lxml to Mistletoe

This is a proof-of-concept of moving MonsterUI's HTML class injection from lxml post-processing to a custom Mistletoe renderer. Looks like we can get 3x faster Markdown rendering using this simple MonsterHTMLRenderer vs. parsing the rendered HTML to inject the classes.


```python
from fasthtml.common import *
from lxml import html, etree
from monsterui.all import *
import mistletoe
from mistletoe import markdown
from mistletoe.html_renderer import block_token, HtmlRenderer
import timeit
```

## My Current Markdown to HTML FastTag

This is what I currently use on this site to render Markdown cells from my Jupyter notebooks:


```python
def StyledMd(m):
    return Safe(markdown(m))
```


```python
x = "## A Test Level 2 Heading"
```


```python
StyledMd(x)
```




    '<h2>A Test Level 2 Heading</h2>\n'



## How MonsterUI Uses Mistletoe

`monsterui.franken` has this function. This seems promising! My goal is to add the `uk-h2` class to the above:


```python
def render_md(md_content:str, # Markdown content
               class_map=None, # Class map
               class_map_mods=None # Additional class map
              )->FT: # Rendered markdown
    "Renders markdown using mistletoe and lxml"
    if md_content=='': return md_content
    # Check for required dependencies        
    html_content = mistletoe.markdown(md_content) #, mcp.PygmentsRenderer)
    return NotStr(apply_classes(html_content, class_map, class_map_mods))
```


```python
render_md(x)
```




    '<h2 class="uk-h2 text-3xl font-bold mt-10 mb-5">A Test Level 2 Heading</h2>\n'



That looks like too many classes? Aha, I see `monsterui.franken` defines:


```python
franken_class_map = {
    'h1': 'uk-h1 text-4xl font-bold mt-12 mb-6',
    'h2': 'uk-h2 text-3xl font-bold mt-10 mb-5', 
    'h3': 'uk-h3 text-2xl font-semibold mt-8 mb-4',
    'h4': 'uk-h4 text-xl font-semibold mt-6 mb-3',
    
    # Body text and links
    'p': 'text-lg leading-relaxed mb-6',
    'a': 'uk-link text-primary hover:text-primary-focus underline',
    
    # Lists with proper spacing
    'ul': 'uk-list uk-list-disc space-y-2 mb-6 ml-6',
    'ol': 'uk-list uk-list-decimal space-y-2 mb-6 ml-6',
    'li': 'leading-relaxed',
    
    # Code and quotes
    'pre': 'bg-base-200 rounded-lg p-4 mb-6',
    'code': 'uk-codespan px-1',
    'pre code': 'uk-codespan px-1 block overflow-x-auto',
    'blockquote': 'uk-blockquote pl-4 border-l-4 border-primary italic mb-6',
    
    # Tables
    'table': 'uk-table uk-table-divider uk-table-hover uk-table-small w-full mb-6',
    'th': 'text-left p-2',
    'td': 'p-2',
    
    # Other elements
    'hr': 'uk-divider-icon my-8',
    'img': 'max-w-full h-auto rounded-lg mb-6'
}
```

Let's try updating just the headings to remove the non-UIkit Tailwind classes:


```python
franken_class_map = {
    'h1': 'uk-h1',
    'h2': 'uk-h2', 
    'h3': 'uk-h3',
    'h4': 'uk-h4',
    
    # Body text and links
    'p': 'text-lg leading-relaxed mb-6',
    'a': 'uk-link text-primary hover:text-primary-focus underline',
    
    # Lists with proper spacing
    'ul': 'uk-list uk-list-disc space-y-2 mb-6 ml-6',
    'ol': 'uk-list uk-list-decimal space-y-2 mb-6 ml-6',
    'li': 'leading-relaxed',
    
    # Code and quotes
    'pre': 'bg-base-200 rounded-lg p-4 mb-6',
    'code': 'uk-codespan px-1',
    'pre code': 'uk-codespan px-1 block overflow-x-auto',
    'blockquote': 'uk-blockquote pl-4 border-l-4 border-primary italic mb-6',
    
    # Tables
    'table': 'uk-table uk-table-divider uk-table-hover uk-table-small w-full mb-6',
    'th': 'text-left p-2',
    'td': 'p-2',
    
    # Other elements
    'hr': 'uk-divider-icon my-8',
    'img': 'max-w-full h-auto rounded-lg mb-6'
}
```

Now explicitly passing in the updated one:


```python
render_md(x, class_map=franken_class_map)
```




    '<h2 class="uk-h2">A Test Level 2 Heading</h2>\n'



That worked!

## Understanding render_md

`render_md` calls `apply_classes`:


```python
def apply_classes(html_str:str, # Html string
                  class_map=None, # Class map
                  class_map_mods=None # Class map that will modify the class map map (useful for small changes to a base class map)
                 )->str: # Html string with classes applied
    "Apply classes to html string"
    if not html_str: return html_str
    try:
        class_map = ifnone(class_map, franken_class_map)
        if class_map_mods: class_map = {**class_map, **class_map_mods}
        html_str = html.fromstring(html_str)
        for selector, classes in class_map.items():
            # Handle descendant selectors (e.g., 'pre code')
            xpath = '//' + '/descendant::'.join(selector.split())
            for element in html_str.xpath(xpath):
                existing_class = element.get('class', '')
                new_class = f"{existing_class} {classes}".strip()
                element.set('class', new_class)
        return etree.tostring(html_str, encoding='unicode', method='html')
    except etree.ParserError:
        return html_str
```

Here, lxml matches and appends the classes after mistletoe generates the HTML. This could probably be improved by implementing a custom Mistletoe HTML renderer instead of parsing its rendered HTML. [html_renderer.py](https://github.com/miyuchina/mistletoe/blob/master/mistletoe/html_renderer.py) looks nicely customizable.


```python
class MonsterHtmlRenderer(HtmlRenderer):
    def render_heading(self, token: block_token.Heading) -> str:
        template = '<h{level} class="uk-h{level}">{inner}</h{level}>'
        inner = self.render_inner(token)
        return template.format(level=token.level, inner=inner)
```

Now we try it:


```python
markdown("## Heading 2", MonsterHtmlRenderer)
```




    '<h2 class="uk-h2">Heading 2</h2>\n'



That worked!

## Updating StyledMd


```python
def StyledMd(m):
    return Safe(markdown(m, MonsterHtmlRenderer))
```


```python
StyledMd("## Heading 2")
```




    '<h2 class="uk-h2">Heading 2</h2>\n'



## Benchmarks

Over 100,000 iterations I dramatically improved Markdown rendering performance:


```python
test_md = "## Heading\n\nParagraph\n\n* List item 1\n* List item 2"

def benchmark_old():
    return render_md(test_md, class_map=franken_class_map)

def benchmark_new():
    return markdown(test_md, MonsterHtmlRenderer)
```


```python
n = 100000
```


```python
t_old = timeit.timeit('benchmark_old()', globals=globals(), number=n)
print(f"Old method: {t_old/n*1000:.2f}ms per iteration")
```

    Old method: 0.15ms per iteration



```python
t_new = timeit.timeit('benchmark_new()', globals=globals(), number=n)
print(f"New method: {t_new/n*1000:.2f}ms per iteration")
```

    New method: 0.05ms per iteration


## Next Steps

This is ready to back-integrate into this site. I hope to contribute the relevant parts of this back to MonsterUI as well, to improve Markdown rendering performance in sites that use it.
