# Accessing CSS Classes in FastHTML

How to retrieve the CSS classes for a FastHTML FastTag instance.


```python
from fasthtml.common import *
```

## Define a Div in FastHTML, With Tailwind Classes

Here's a typical div with several Tailwind CSS classes:


```python
d = Div(cls="container mx-auto p-4 bg-white dark:bg-gray-800")
```


```python
d
```




```html
<div class="container mx-auto p-4 bg-white dark:bg-gray-800"></div>

```



## Get the CSS Classes

The FT variable `d` has these `attrs`:


```python
d.attrs
```




    {'class': 'container mx-auto p-4 bg-white dark:bg-gray-800'}



To get the CSS classes, you get the `class` attribute of `d`:


```python
d.attrs['class']
```




    'container mx-auto p-4 bg-white dark:bg-gray-800'



## Parse Them Into a List

Then you can split the space-separated string into a list, if you like:


```python
css_classes = d.attrs['class'].split()
css_classes
```




    ['container', 'mx-auto', 'p-4', 'bg-white', 'dark:bg-gray-800']


