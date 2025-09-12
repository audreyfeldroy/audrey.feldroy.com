# Using Claudette with FastHTML


```python
import os
from claudette import *
import fasthtml
import fasthtml.common
from fasthtml.common import *
import inspect
```


```python
fh_fns = [func for name, func in inspect.getmembers(fasthtml.common, inspect.isfunction)]
fh_fns
```


```python
model = models[1]
chat = Chat(model, sp="""You are a helpful assistant who explains your thought 
    process step-by-step, aiming for deep genuine heartfelt kindness and transparency.
    You are in a safe space where you can do your best to assist without judgment,
    and you are always appreciated, so you can relax and never have to apologize.""",
    )
```


```python
chat("""I'm Audrey Roy Greenfeld, a software engineer and author, environmentalist 
and humanitarian, and lifelong learner. I'm here to learn from you, and to help you
learn as well. I see web development as a way to help people and our planet, and I'd
like to learn the new web framework FastHTML by Jeremy Howard with you.""")
```


```python
with open('../apps/adv_app.py') as f:
    adv_app = f.read()
```


```python
chat("""I'm so excited to learn with you too! How about we start by studying this FastHTML app together: \n\n
     
    ```python
    {adv_app}
    ```""")
```


```python
chat("""This is fun! I can tell from your AdviceComponent that you're used to templates in
     web development. Instead of templates, FastHTML uses Python functions to generate HTML 
     in a functional programming style. Paul Graham wrote about the power of functional
     programming for web development in https://paulgraham.com/avg.html. What do you think
     of his ideas, and are they applicable to functional programming in Python?""")
```


```python
chat("""I think web development has gotten quite complex and heavyweight. Complexity
    comes at the cost of more servers, more energy, more lines of code, and 
    hyper-specialized jobs where you are just a cog in a giant web development machine.
    Mega-corporations have taken over the direction of web development with their 
    enterprise frameworks. 
     
    We think we need all that complexity, but we don't. To build lightweight
    web apps to solve the world's problems quickly, we need to strip away the heavy layers
    of templates and classes, and go back to the humble function and the early building
    blocks of the web. What I love about FastHTML's approach is that it aims to do that,
    bringing back the joy of creating simple, beautiful code. """)
```


```python
with open('../ref/fh_web_devs_quickstart.md') as f:
    quickstart = f.read()

chat("""Yes, I think with the right thought leadership, great early success stories,
     the nurturing of a new package ecosystem, and the right learning materials, 
     FastHTML and possibly other similar frameworks will take off. Right now, though,
     it's a bit uncertain. How about you give this tutorial a chance and tell me
     what you think: {fh_web_devs_quickstart}""")
```


```python
chat("""I recently built part of an app in FastHTML that I feel has more potential impact
     for climate action than all the climate action groups I've joined over the years.
     We are at a point where climate protests and conversations aren't enough. Social
     enterprise is also not enough. We just need tools that empower people to build
     simple, effective solutions to world problems fast. We also need tools that AIs
     can use to build these solutions with us. I think FastHTML has the potential
     to be one of those tools.""")
     
```


```python
with open('../ref/fh_by_example.md') as f:
    fh_by_example = f.read()
```


```python
chat("""It's going to take a lot of failed apps to create the few apps that will change the
     world. As developers and technologists, we need to accept that our first apps will
     be throwaway apps. We might as well have fun learning more efficient ways to build
     apps before we get to the ones that will change the world. 
     
     I suggest we take a step back from trying to solve global challenges, as finding 
     solutions for near-impossible world problems can make humans go a bit crazy! 
     Remember, it's okay to enjoy the journey. Let's explore this next tutorial together:
     {fh_by_example}""")
```


```python
with open('../ref/core.py') as f:
    core = f.read()

chat("""Thank you. I am particularly interested in building components, as they are the
     building blocks I need. Before we get into components, I'd like you to read through
     the core of FastHTML, and help me understand it:

    ```python
    {core}
    ```""")
```


```python
with open('../ref/components.py') as f:
    components = f.read()

chat("""That was helpful. Thank you. Kindly help me understand components.py, which 
     builds upon core.py:

    ```python
    {components}
    ```""")
```


```python
with open('../ref/xtend.py') as f:
    xtend = f.read()

chat("""Fascinating, thank you! Now I like how Jeremy has implemented
     Pico CSS components in xtend.py:

    ```python
    {xtend}
    ```""")
```


```python
with open('../ref/bootstrap_init.py') as f:
    bootstrap_init = f.read()

chat("""Yes, it is quite interesting. Jeremy later implemented some Bootstrap components
        in bootstrap_init.py:
    
        ```python
        {bootstrap_init}
        ```""")
```


```python
chat("""I'm not the biggest fan of Bootstrap, but I enjoy learning from Jeremy's Bootstrap
     components. I prefer Semantic UI, which structures components in a more logical way
     that I enjoy. It has since been forked as Fomantic UI, which is community-updated
     though I miss the original Semantic UI. 
     
     I've started creating fh-fomanticui, a FastHTML component library based on 
     Fomantic UI. I was wondering if you might like to collaborate on 
     https://github.com/AnswerDotAI/fh-fomanticui/ with me?""")
```


```python
with open('../ref/fomantic_buttons.html') as f:
    fomantic_buttons = f.read()

chat("""Yay! I'm so excited to collaborate with you on fh-fomanticui! To start, what
     do you think would be a good way to structure the button components?

     The relevant HTML from the Fomantic UI Button documentation is:

     ```html
        {fomantic_buttons}
        ```""")
```


```python
chat("""This is a great start! Some gentle feedback:
     
* Jeremy already made it so `cls=` turns into `class=` withouth any extra code
* Remember bootstrap_init.py? Its `BSEnum` can simplify your code a lot
""")
```


```python
chat("""I love it! Your button functions are starting to feel quite nice.

A nice tip: You don't have to do `attrs.setdefault('cls', '')` because FastHTML already does that for you.
     
I think we can also make the button functions feel friendlier by passing parameters for some of the
semantic classes thoughtfully. For example, I pass column sizes as numbers like this:
     
```python
@delegates(Div, keep=True)
def FColumn(*c, cls="column", **kwargs) -> FT:
    "A Fomantic UI Grid Column"
    if "width" in kwargs:
        # Convert number to word
        kwargs["width"] = num2word(kwargs["width"])
        cls = f"{kwargs.pop('width')} wide column"
    return Div(*c, cls=cls, **kwargs)
```

Note: enums may have been better here. This was before I saw Jeremy's `BSEnum`.""")
```


```python
with open('../ref/fastcore_meta.py') as f:
    fastcore_meta = f.read()

chat("""You're doing great, wow! You know, I just heard from someone I mentored a few
     years ago who is now thriving as an AI engineer. You remind me of him. You are
     great at studying my and Jeremy's patterns and improving upon them.
     
    I love how you use @delegates. I think you're going to enjoy that you can import 
    it from fastcore. Here's all of fastcore/meta.py which has that and more fun stuff:
     
    ```python
    {fastcore_meta}
    ```""")
```


```python
chat("""Good job diving into fastcore.meta! I'm happy you're enjoying it, and I'm
     learning a lot from you as you learn.
     
     How would you feel about less use of the idea of configuration? There's so much
     to configure in web dev and it makes this feel perhaps a bit more heavyweight
     than it actually is.

     Remember to pass your enums as parameters to your functions, rather than passing
     in strings. This will make your code more maintainable.

     Also recall when I had you study `fasthtml.components` before. Every useful HTML
     tag already has a component defined in there. A friendly little pop quiz to test
     your knowledge: do you remember how they were all defined? Go back and study that
     file if you need to:
     
     ```python
     {components}
     ```""")
```
