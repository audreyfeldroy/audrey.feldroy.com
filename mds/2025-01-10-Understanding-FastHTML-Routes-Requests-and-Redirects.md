# Understanding FastHTML Routes, Requests, and Redirects

In this tutorial we'll look at the simplest routes and route handlers you can create with FastHTML. We'll define the handlers as little functions, and then call them as we would any other Python function. After that, we'll make simple GET requests to a simple index route/handler, a parameterized one, and a parameterized one with a redirect.

## Setup


```python
from fasthtml.common import *
```


```python
app,rt = fast_app(pico=False)
```

We start with a FastHTML app as usual. `fast_app` is a convenience wrapper for `FastHTML` with some nice defaults.


```python
cli = Client(app)
cli
```




    <fasthtml.core.Client at 0x113dbcdd0>



We set up an HTTP client to make requests with. `Client` is defined in `fasthtml.core` and wraps httpx's `AsyncClient`.

## Defining a Homepage


```python
@rt
def index(): return Titled("My Homepage")
```

Here's a really simple index route handler, to give us something to request. `@rt` is my favorite way to define routes. It makes the index route in particular quick to type out fast because you don't even need a route string.


```python
r = cli.get('/')
r
```




    <Response [200 OK]>



We requested that page and got a successful 200 response with our client!


```python
r.text
```




    ' <!doctype html>\n <html>\n   <head>\n     <title>My Homepage</title>\n     <meta charset="utf-8">\n     <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n<script src="https://unpkg.com/htmx.org@2.0.4/dist/htmx.min.js"></script><script src="https://cdn.jsdelivr.net/gh/answerdotai/fasthtml-js@1.0.12/fasthtml.js"></script><script src="https://cdn.jsdelivr.net/gh/answerdotai/surreal@main/surreal.js"></script><script src="https://cdn.jsdelivr.net/gh/gnat/css-scope-inline@main/script.js"></script><script>\n    function sendmsg() {\n        window.parent.postMessage({height: document.documentElement.offsetHeight}, \'*\');\n    }\n    window.onload = function() {\n        sendmsg();\n        document.body.addEventListener(\'htmx:afterSettle\',    sendmsg);\n        document.body.addEventListener(\'htmx:wsAfterMessage\', sendmsg);\n    };</script>   </head>\n   <body>\n<main class="container">       <h1>My Homepage</h1>\n</main>   </body>\n </html>\n'



The response contains this text. If you look closely, you'll see it's a full HTML page containing `<h1>My Homepage</h1>` toward the end.


```python
r.headers
```




    Headers({'content-length': '971', 'content-type': 'text/html; charset=utf-8'})



These are the HTTP response headers.

## Defining a Route With a Parameter


```python
@rt('/pages/{pagename}')
def page(pagename:str):
    return Titled(pagename)
```

Here you see a route defined with `@rt` plus a parameterized route string. 

The string value of `pagename` from the route turns into the `pagename` argument to the `page` function. 

Then it's used in the function definition any way we want. For simple examples like this, I use `Titled` to create quick web pages with the string used twice: as a `<title>` and `<h1>` element.

## Calling the Route Handler as a Function


```python
heypage = page("HEYHEYHEYHEY")
heypage
```




    (title(('HEYHEYHEYHEY',),{}),
     main((h1(('HEYHEYHEYHEY',),{}),),{'class': 'container'}))



You can call a route handler function like `page("HEYHEYHEYHEY")` manually, like you would any other Python function. This can be good when you want to make sure your function behaves correctly.


```python
to_xml(heypage)
```




    '<title>HEYHEYHEYHEY</title>\n<main class="container">  <h1>HEYHEYHEYHEY</h1>\n</main>'



When you pass the returned value into `to_xml`, you can see that you only have a subset of an HTML page. When you call a route handler function manually, you're not making a full HTTP request.

## Making a Full HTTP Request


```python
rp = cli.get('/pages/HEYHEYHEYHEY')
rp
```




    <Response [200 OK]>



This is much more like typing `example.com/pages/HEYHEYHEYHEY` in your browser. You get not just what the function returns, but a whole HTTP request-response round trip.


```python
rp.text
```




    ' <!doctype html>\n <html>\n   <head>\n     <title>HEYHEYHEYHEY</title>\n     <meta charset="utf-8">\n     <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n<script src="https://unpkg.com/htmx.org@2.0.4/dist/htmx.min.js"></script><script src="https://cdn.jsdelivr.net/gh/answerdotai/fasthtml-js@1.0.12/fasthtml.js"></script><script src="https://cdn.jsdelivr.net/gh/answerdotai/surreal@main/surreal.js"></script><script src="https://cdn.jsdelivr.net/gh/gnat/css-scope-inline@main/script.js"></script><script>\n    function sendmsg() {\n        window.parent.postMessage({height: document.documentElement.offsetHeight}, \'*\');\n    }\n    window.onload = function() {\n        sendmsg();\n        document.body.addEventListener(\'htmx:afterSettle\',    sendmsg);\n        document.body.addEventListener(\'htmx:wsAfterMessage\', sendmsg);\n    };</script>   </head>\n   <body>\n<main class="container">       <h1>HEYHEYHEYHEY</h1>\n</main>   </body>\n </html>\n'



You can inspect the response text like you would the HTTP response of any site. Now you see why I capitalized `pagename` and made it so long and obvious. That makes it easy to spot in the 2 places it shows up in the response string: in the title and in the h1 within the main element.


```python
rp.headers
```




    Headers({'content-length': '973', 'content-type': 'text/html; charset=utf-8'})



The response has HTTP response headers.

## Implementing a Redirect

Now imagine the above route had an old location that we needed to redirect from.


```python
@rt('/pageswasherebefore/{pagename}')
def old_page(pagename:str): return Redirect(f"/pages/{pagename}")
```

Here we define a second route with the old URL path string. It returns a redirect pointing to the new location. The redirect uses the `Redirect` class from fasthtml.core.

## Making a Request and Inspecting the Redirect's Response


```python
rop = cli.get('/pageswasherebefore/HIHIHIHIHIHIHIHI')
rop
```




    <Response [303 See Other]>



We can make a GET request with our HTTP client the way we did before, and assign the returned response object to a variable.


```python
rop.headers
```




    Headers({'content-length': '0', 'location': '/pages/HIHIHIHIHIHIHIHI'})



Looking at the HTTP response headers, we now see a location. That's the new location you're getting redirected to, not the old one.


```python
rop.text
```




    ''



And there's no response text content, which matches the length of 0 that we saw in the headers.

## Making a Request that Follows the Redirect


```python
rop2 = cli.get('/pageswasherebefore/HIHIHIHIHIHIHIHI', follow_redirects=True)
rop2
```




    <Response [200 OK]>




```python
rop2.headers
```




    Headers({'content-length': '981', 'content-type': 'text/html; charset=utf-8'})



Now we see a 200 response, content, and no location!


```python
rop2.text
```




    ' <!doctype html>\n <html>\n   <head>\n     <title>HIHIHIHIHIHIHIHI</title>\n     <meta charset="utf-8">\n     <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n<script src="https://unpkg.com/htmx.org@2.0.4/dist/htmx.min.js"></script><script src="https://cdn.jsdelivr.net/gh/answerdotai/fasthtml-js@1.0.12/fasthtml.js"></script><script src="https://cdn.jsdelivr.net/gh/answerdotai/surreal@main/surreal.js"></script><script src="https://cdn.jsdelivr.net/gh/gnat/css-scope-inline@main/script.js"></script><script>\n    function sendmsg() {\n        window.parent.postMessage({height: document.documentElement.offsetHeight}, \'*\');\n    }\n    window.onload = function() {\n        sendmsg();\n        document.body.addEventListener(\'htmx:afterSettle\',    sendmsg);\n        document.body.addEventListener(\'htmx:wsAfterMessage\', sendmsg);\n    };</script>   </head>\n   <body>\n<main class="container">       <h1>HIHIHIHIHIHIHIHI</h1>\n</main>   </body>\n </html>\n'



This looks like the HTTP response for the new route, which is what we want to see.

## Wrapping Up

We've seen how FastHTML makes it easy to create routes and handle HTTP requests. We covered:
- Creating a simple homepage with `@rt`
- Adding a parameterized route with `@rt('/pages/{pagename}')`
- Testing route handlers by calling them directly as Python functions
- Making HTTP requests with FastHTML's `Client`
- Setting up redirects and seeing how they work both with and without following them

What I love here is how much FastHTML development feels so much like regular Python development. You can call handlers like normal functions to make sure they work as expected, and they still work great as full web endpoints.
