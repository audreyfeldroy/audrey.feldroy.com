# FastHTML by Example

Studying https://docs.fastht.ml/tutorials/by_example.html more


```
from fasthtml.common import *
```


```
app = FastHTML()
```


```
@app.get("/")
def home():
    return Div(H1('Hello, World'), P('Some text'), P('Some more text'))
```


```
from starlette.testclient import TestClient
client = TestClient(app)
r = client.get("/")
r.text
```

## Forms


```
Form(Input(type="text", name="data"),
                     Button("Submit"),
                     action="/", method="post")
```
