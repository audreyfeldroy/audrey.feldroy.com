# Auth in FastHTML

My early attempts to figure out auth in FastHTML. Things have likely changed a lot since.

Basic auth:

* https://github.com/AnswerDotAI/fasthtml/blob/main/fasthtml/authmw.py
* https://github.com/AnswerDotAI/fasthtml/blob/main/nbs/api/00_core.ipynb has some auth tests

Oauth:

* https://github.com/AnswerDotAI/fasthtml/blob/main/nbs/incomplete/oauth.ipynb


```python
from fasthtml.authmw import user_pwd_auth
from fasthtml.common import *
from fastcore.test import *
from fastcore.utils import *
from fastcore.xml import *
from fasthtml.xtend import *
from starlette.testclient import TestClient
```


```python
def get_cli(app): return app,TestClient(app),app.route
```

From https://github.com/AnswerDotAI/fasthtml/blob/main/nbs/api/00_core.ipynb


```python
auth = user_pwd_auth(testuser='spycraft')
app,cli,rt = get_cli(FastHTML(middleware=[auth]))

@rt("/locked")
def get(auth): return 'Hello, ' + auth

test_eq(cli.get('/locked').text, 'not authenticated')
test_eq(cli.get('/locked', auth=("testuser","spycraft")).text, 'Hello, testuser')
```

Passing a dict into `lookup`:


```python
auth = user_pwd_auth(lookup={'testuser':'spycraft', 'testuser2':'spycraft2'})
app,cli,rt = get_cli(FastHTML(middleware=[auth]))

@rt("/locked")
def get(auth): return 'Hello, ' + auth

test_eq(cli.get('/locked').text, 'not authenticated')
test_eq(cli.get('/locked', auth=("testuser","spycraft")).text, 'Hello, testuser')
test_eq(cli.get('/locked', auth=("testuser2","spycraft2")).text, 'Hello, testuser2')
```

Passing a callable into `lookup`:


```python
def user_lookup(u, p):
    users = {
        'testuser': 'spycraft',
        'testuser2': 'spycraft2',
        'testuser3': 'spycraft3',
    }
    expected_p = users.get(u)
    if expected_p is None: return None

    # WARNING: Toy implementation, not secure
    # Pretend we are comparing Argon2 or PBKDF2 hashes
    return p == expected_p

auth = user_pwd_auth(lookup=user_lookup)
app, cli, rt = get_cli(FastHTML(middleware=[auth]))

@rt("/locked")
def get(auth): return 'Hello, ' + auth

test_eq(cli.get('/locked').text, 'not authenticated')
test_eq(cli.get('/locked', auth=("testuser","spycraft")).text, 'Hello, testuser')
test_eq(cli.get('/locked', auth=("testuser2","spycraft2")).text, 'Hello, testuser2')
test_eq(cli.get('/locked', auth=("testuser3","spycraft3")).text, 'Hello, testuser3')
```
