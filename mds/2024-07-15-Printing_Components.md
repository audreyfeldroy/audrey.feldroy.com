# Printing FastHTML Components


```
from fasthtml.common import *
```


```
btn = Button("Click me", "btn btn-primary")
btn
```


```
type(btn)
```


```
str(btn)
```

Reading https://github.com/fastai/fastcore/blob/master/fastcore/xml.py and https://github.com/fastai/fastcore/blob/master/nbs/11_xml.ipynb I see that an XT is a list with some properties:


```
btn.tag
```


```
btn.children
```


```
btn.attrs
```

Oh, I think I can use this to show the rendered component XML:


```
to_xml(btn)
```


```
highlight(btn)
```

What about stringifying the Python code for a component?


```
#|eval: false
import inspect
print(inspect.getsource(btn))
```


```

```
