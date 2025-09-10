# SemanticUI FastHTML Cards

Caution: I’ve learned better patterns since I wrote this. Leaving this here for posterity.


```
from fasthtml.common import *
```

I pasted the code for [Semantic UI's group of button cards](https://fomantic-ui.com/views/card.html#buttons) into [HTML to XT](https://h2x-production-16c0.up.railway.app/) and got:


```
Div(
  Div(
    Div(
      Div('Elliot Fu', cls='header'),
      Div('Elliot Fu is a film-maker from New York.', cls='description'),
      cls='content'
    ),
    Div(
      I(cls='add icon'),
      'Add Friend',
      cls='ui button'
    ),
    cls='card'
  ),
  Div(
    Div(
      Div('Veronika Ossi', cls='header'),
      Div('Veronika Ossi is a set designer living in New York who enjoys kittens, music, and partying.', cls='description'),
      cls='content'
    ),
    Div(
      I(cls='add icon'),
      'Add Friend',
      cls='ui button'
    ),
    cls='card'
  ),
  Div(
    Div(
      Div('Jenny Hess', cls='header'),
      Div('Jenny is a student studying Media Management at the New School', cls='description'),
      cls='content'
    ),
    Div(
      I(cls='add icon'),
      'Add Friend',
      cls='ui button'
    ),
    cls='card'
  ),
  cls='ui cards'
)
```

Extracting the data into a Python list of tuples:


```
cards_data = [
    ('Elliot Fu', 'Elliot Fu is a film-maker from New York.'),
    ('Veronika Ossi', 'Veronika Ossi is a set designer living in New York who enjoys kittens, music, and partying.'),
    ('Jenny Hess', 'Jenny is a student studying Media Management at the New School')
]
```

We could hardcode the Semantic UI tree structure in like this...


```
def Card(name, description):
    return Div(
        Div(
            Div(name, cls='header'),
            Div(description, cls='description'),
            cls='content'
        ),
        Div(
            I(cls='add icon'),
            'Add Friend',
            cls='ui button'
        ),
        cls='card'
    )
```


```
cards = [Card(name, description) for name, description in cards_data]
cards
```


```
result = Div(*cards, cls='ui cards')
result
```

But it might be nice to separate card text/values from how it is rendered as an XT, and offer different rendering options


```
@dataclass
class Card():
    title: str
    image: str
    description: str
    # button_links: list of text, link pairs maybe

    def __xt__(self, uiframework='semanticui'):
        if uiframework == 'semanticui':
            ...
        elif uiframework == 'frankenui':
            ...
        elif uiframework == 'bootstrap':
            ...
        else:
            raise ValueError(f"Unknown uiframework {uiframework}")
```

This would be hard to maintain, though. I feel like a system to allow devs to make their own CSS framework plugins for XT would be nice.

Daniel suggested using dataclasses like in his blog.

Claude 3.5 Sonnet suggested renderers for each framework could look like:


```
from typing import List, Tuple, Optional, Callable, Dict

# Global registry for renderers
renderer_registry: Dict[str, Callable] = {}

def register_renderer(framework: str):
    """Decorator to register a renderer for a specific framework."""
    def decorator(func: Callable):
        renderer_registry[framework] = func
        return func
    return decorator
```


```
from dataclasses import dataclass

@dataclass
class Card:
    title: str
    description: str
    image: Optional[str] = None
    button_links: List[Tuple[str, str]] = ()

    def __xt__(self, uiframework='semanticui'):
        if uiframework not in renderer_registry:
            raise ValueError(f"No renderer registered for framework: {uiframework}")
        return renderer_registry[uiframework](self)
```


```
@register_renderer('semanticui')
def render_semanticui(card: Card):
    content = [
        Div(card.title, cls='header'),
        Div(card.description, cls='description')
    ]
    if card.image:
        content.insert(0, Div(Img(src=card.image, cls='ui image'), cls='image'))
    
    buttons = [
        A(text, href=link, cls='ui button')
        for text, link in card.button_links
    ]

    return Div(
        Div(*content, cls='content'),
        *buttons,
        cls='ui card'
    )
```

Let's try rendering out a simple card with this


```
hannah_card = Card('Hannah', 'Hannah is a girl who likes to dance.', image='hannah.jpg', button_links=[('Add Friend', '#')])
hannah_card.__xt__()
```

Note: I've learned better patterns since I wrote this. Leaving this here for posterity.
