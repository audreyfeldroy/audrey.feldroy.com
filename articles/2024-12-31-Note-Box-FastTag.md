# Note Box FastTag

I needed a quick note box for the index page of this site, without affecting the CSS of my notebooks that explore weird CSS stuff deeply.


```python
from fasthtml.common import *
```

So I whipped out this quick FastTag:


```python
def Note(c): return Div(H3("Note"), *c, style="padding:10px;border:1px lightblue solid; border-left:6px lightblue solid;")
```

Then I realized I should write about it, because creating a little FastTag like this doesn't come naturally for most people. In fact it took me probably too long to get into the flow of writing these little functions.

## Showing It in a Notebook

You can show it in a notebook like this:


```python
show(Note(
    P("Hey, I have something small to say in this box. And it's tangential to the main intent of the page, so I've put it into a note box. Now back to whatever we were talking about.")))
```

## `c` Can Be an Iterator

For multiple paragraphs or other elements, just pass in a tuple or other iterator:


```python
show(Note((
    P("Hey, I have something small to say in this box. It's really, really small, I promise. But as I write in this box that allows me to put anything into it, it's getting a tiny bit bigger. I suppose it's growing quickly like a child as the years go by."), 
    P("And it's tangential to the main intent of the page, so I've put it into a note box. Now back to whatever we were talking about."))))
```

## Typography and Jupyter Notebook Classic

The note box doesn't show up pixel-perfectly in Jupyter Notebook classic (where I'm working right now) because the CSS styles for notebook typography are changing it:

* I see that nbclassic uses Bootstrap 3's scaffolding.less and normalize.less to change font properties on the `body` and `html` elements. Some are overridden in `div#notebook` in notebook.less.
* In my FastHTML site the user agent stylesheet is also changing the styles, so perhaps it's more pixel-perfect in nbclassic than on the site. Hmm.
* Looks like [Bootstrap 5.3's reboot](https://getbootstrap.com/docs/5.3/content/reboot/#approach) no longer uses scaffolding.less and now builds upon Normalize.

This is quite a rabbit hole so I think I'm going to be okay with my note box looking a little off, and end this exploration for now.

## Reflection

If you need a quick note box or other component and are experimenting in weird ways with CSS so you can't bring in a UI framework easily, making quick little FastTags like this is a "good enough" solution. 
