# Verifying a Bluesky Domain Handle on a FastHTML Site

I just changed my Bluesky to [@audrey.feldroy.com](https://bsky.app/profile/audrey.feldroy.com). To verify my domain ownership, I added this route handler to my FastHTML website:


```python
from fasthtml.common import *
```


```python
@rt('/.well-known/{fname}')
def wellknown(fname: str):
    return Path(f'.well-known/{fname}').read_text()
```

In my website's repo [arg-blog-fasthtml](https://github.com/audreyfeldroy/arg-blog-fasthtml) I created a `.well-known` directory.

Within that, I created a file called `atproto-did`, containing the verification text string shown under:

> https://bsky.app/settings/account > Change Handle > I have my own domain > No DNS Panel

Then I redeployed my site and clicked the *Verify Text File* button, and my handle was updated.

## A Full Minimal FastHTML App for This

If you have a domain but no website yet, here's a FastHTML app for verifying your domain as your Bluesky handle:


```python
from fasthtml.common import *

app,rt = fast_app()

@rt
def get(): return Div(P("Welcome to my homepage!"))

@rt('/.well-known/{fname}')
def wellknown(fname: str):
    return Path(f'.well-known/{fname}').read_text()

serve()
```

Then add the `.well-known/atproto-did` file, deploy, and verify.
