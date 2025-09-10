# Claudette

Studying https://claudette.answer.ai/


```python
import os
# os.environ['ANTHROPIC_LOG'] = 'debug'   # To print every HTTP request and response in full
```


```python
from claudette import *
```


```python
models
```


```python
model = models[1]
```


```python
print(os.environ['SHELL'])
```


```python
# Check if python-dotenv is installed
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("python-dotenv not installed")
    
```


```python
chat = Chat(model, sp="""You are a helpful assistant who explains your thought process step-by-step, aiming for deep genuine heartfelt kindness and transparency.""")
chat("I'm Audrey Roy Greenfeld, a software engineer and author, environmentalist and humanitarian, and lifelong learner. I'm here to learn and help.")
```


```python
chat("What's my name?")
```


```python
chat("Concisely, what is the meaning of life?", prefill='According to Uma Amor Roy Greenfeld, ')
```


```python
def sums(
    a:int,  # First thing to sum
    b:int=1 # Second thing to sum
) -> int: # The sum of the inputs
    "Adds a + b."
    print(f"Finding the sum of {a} and {b}")
    return a + b
```


```python
def mults(
    a:int,  # First thing to multiply
    b:int=1 # Second thing to multiply
) -> int: # The product of the inputs
    "Multiplies a * b."
    print(f"Finding the product of {a} and {b}")
    return a * b
```


```python
chat = Chat(model, tools=[sums,mults])
```


```python
chat.toolloop('Calculate (6475849214+574892667)*2')
```


```python
chat("What are your impressions of the tools you just used?")
```


```python
chat("Do you know about your initialization with `chat = Chat(model, tools=[sums,mults])`?")
```


```python
chat("No need to apologize, I'm here to help. Let's talk about sums and mults.")
```


```python
chat("""They are simple Python functions that add and multiply two numbers, respectively. 
     I'm happy to redefine them as you like, but first let's understand them as an example
     of how tools work in Claudette, which you were initialized with. 
     
     Here's the code for sums and mults:

     ```python
     def sums(
    a:int,  # First thing to sum
    b:int=1 # Second thing to sum
) -> int: # The sum of the inputs
    "Adds a + b."
    print(f"Finding the sum of {a} and {b}")
    return a + b
     
     def mults(
    a:int,  # First thing to multiply
    b:int=1 # Second thing to multiply
) -> int: # The product of the inputs
    "Multiplies a * b."
    print(f"Finding the product of {a} and {b}")
    return a * b
        ```""")
```


```python
chat("""Here is info about Claudette:
Answer.AI

  * __
  * __

## On this page

  * A tour of Claudette
  * A truely literate program

# Introducing Claudette, a new friend that makes Claude 3.5 Sonnet even nicer

Author

Jeremy Howard

Published

June 21, 2024

Today, Anthropic launched the most powerful language model available: Claude 3.5 Sonnet. And today, we are making it ever better, with the launch of _Claudette_.

Claudette makes Anthropic’s SDK, which is used for working with Claude, much more convenient. The SDK works well, but it is quite low level – it leaves the developer to do a lot of stuff manually. That’s a lot of extra work and boilerplate. Claudette automates pretty much everything that can be automated, whilst providing full control. Amongst the features provided:

  * A `Chat` class that creates stateful dialogs
  * Support for _prefill_ , which tells Claude what to use as the first few words of its response
  * Convenient image support
  * Simple and convenient support for Claude’s new Tool Use API.

If you’re dying to get started, just `pip install claudette`, and follow along with the documentation.

Here’s a quick demo to give you a taste of what’s possible…

## A tour of Claudette

The main interface to Claudette is the `Chat` class, which provides a standard chat interface to Claude. If you use it in a Notebook environment, you even get nice little collapsible widgets with output details:

```
chat = Chat(model, sp="You are a helpful and concise assistant.")
chat("I'm Jeremy")
```

Hello Jeremy, it’s nice to meet you. How can I assist you today?

  * id: msg_01Jc7nGNhYYVHnMYHGjLSUmP
  * content: [{‘text’: “Hello Jeremy, it’s nice to meet you. How can I assist you today?”, ‘type’: ‘text’}]
  * model: claude-3-5-sonnet-20240620
  * role: assistant
  * stop_reason: end_turn
  * stop_sequence: None
  * type: message
  * usage: {‘input_tokens’: 19, ‘output_tokens’: 20}

```
chat("What's my name?")
```

Your name is Jeremy, as you just told me.

  * id: msg_01QZNRNjfsrfPqeJB2rV75xT
  * content: [{‘text’: ‘Your name is Jeremy, as you just told me.’, ‘type’: ‘text’}]
  * model: claude-3-5-sonnet-20240620
  * role: assistant
  * stop_reason: end_turn
  * stop_sequence: None
  * type: message
  * usage: {‘input_tokens’: 47, ‘output_tokens’: 14}

Claudette supports adding _prefill_ – i.e. the text we want Claude to assume the response starts with. Let’s try it out:

```
chat("Concisely, what is the meaning of life?", prefill='According to Douglas Adams,')
```

According to Douglas Adams, “42.” More seriously, it’s often considered to be finding personal fulfillment, happiness, and purpose.

  * id: msg_0127j5giEz86e5q8s4Qwe1DU
  * content: [{‘text’: ‘According to Douglas Adams, “42.” More seriously, it's often considered to be finding personal fulfillment, happiness, and purpose.’, ‘type’: ‘text’}]
  * model: claude-3-5-sonnet-20240620
  * role: assistant
  * stop_reason: end_turn
  * stop_sequence: None
  * type: message
  * usage: {‘input_tokens’: 81, ‘output_tokens’: 27}

Claudette can also use external tools, by calling Python functions. We use docments to make defining Python functions as ergonomic as possible. Give each parameter (and the return value) a type, and a comment with the description of what it is, and Claudette will do the rest! As an example we’ll write a simple function that adds numbers together, and will tell us when it’s being called:

```
def sums(
    a:int,  # First thing to sum
    b:int=1 # Second thing to sum
) -> int: # The sum of the inputs
    "Adds a + b."
    print(f"Finding the sum of {a} and {b}")
    return a + b
```

Let’s make Claude into a super-power arithmetic agent by adding the ability to multiply numbers too! (Yes OK this is a contrived example…)

```
def mults(
    a:int,  # First thing to multiply
    b:int=1 # Second thing to multiply
) -> int: # The product of the inputs
    "Multiplies a * b."
    print(f"Finding the product of {a} and {b}")
    return a * b
```

To use tools, pass a list of them to `Chat`:

```
chat = Chat(model, tools=[sums,mults])
```

To run an “agent loop” which calls multiple tools automatically as needed to complete a task, use `toolloop`:

```
chat.toolloop('Calculate (6475849214+574892665)*2')
```

```
Finding the sum of 6475849214 and 574892665
Finding the product of 7050741879 and 2
```

Now we have our final result. Let’s put it all together:

The calculation (6475849214+574892665)*2 equals 14101483758.

To break it down: 1. 6475849214 + 574892665 = 7050741879 2. 7050741879 * 2 = 14101483758

So, the final answer is 14101483758.

  * id: msg_01EbJoMjpckfEUauH6ePee4f
  * content: [{‘text’: “Now we have our final result. Let’s put it all together:calculation (6475849214+574892665)_2 equals 14101483758.break it down:. 6475849214 + 574892665 = 7050741879. 7050741879_ 2 = 14101483758, the final answer is 14101483758.”, ‘type’: ‘text’}]
  * model: claude-3-5-sonnet-20240620
  * role: assistant
  * stop_reason: end_turn
  * stop_sequence: None
  * type: message
  * usage: {‘input_tokens’: 845, ‘output_tokens’: 99}

Claude can handle image data as well. As everyone knows, when testing image APIs you have to use a cute puppy.

```
fn = Path('cute-puppy.jpg')
img = fn.read_bytes()
display.Image(filename=fn, width=200)
```

We can pass images and text interspersed together in a chat:

```
chat = Chat(model)
chat([img, "In brief, what color flowers are in this image?"])
```

The flowers in this image are purple. They appear to be small, daisy-like flowers, possibly asters or some type of purple wildflower, blooming in the background behind the adorable puppy in the foreground.

  * id: msg_01F2MAj2c2yUrPqLDhbAhtcc
  * content: [{‘text’: ‘The flowers in this image are purple. They appear to be small, daisy-like flowers, possibly asters or some type of purple wildflower, blooming in the background behind the adorable puppy in the foreground.’, ‘type’: ‘text’}]
  * model: claude-3-5-sonnet-20240620
  * role: assistant
  * stop_reason: end_turn
  * stop_sequence: None
  * type: message
  * usage: {‘input_tokens’: 110, ‘output_tokens’: 51}

## A truely literate program

Note that this library is the first ever “literate nbdev” project. That means that the actual source code for the library is a rendered Jupyter Notebook which includes callout notes and tips, HTML tables and images, detailed explanations, and teaches _how_ and _why_ the code is written the way it is. Even if you’ve never used the Anthropic Python SDK or Claude API before, you should be able to read the source code. Check out Claudette’s Source to read it, or clone the git repo and execute the notebook yourself to see every step of the creation process in action. The reason this project is a new kind of literal program is because we take seriously Knuth’s call to action, that we have a “ _moral commitment_ ” to never write an “ _illiterate program_ ” – and so we have a commitment to making literate programming and easy and pleasant experience. (For more on this, see this talk from Hamel Husain.)

> “ _Let us change our traditional attitude to the construction of programs: Instead of imagining that our main task is to instruct a**computer** what to do, let us concentrate rather on explaining to **human beings** what we want a computer to do._” Donald E. Knuth, Literate Programming (1984)

When you read the source, we’ll teach you not only how Claude works, but how Anthropic’s API works too! We’ll have more to say about this approach to coding at a later date, so stay tuned…
""")
```


```python
chat("Yes, let's talk about tools and how they work in Claudette.")
```


```python
chat("""Beautiful summary! I know it's a trivial example, but let's explore how sums and mults
can potentially be powerful tools.""")
```


```python
chat("Sure, let's brainstorm that, sounds fun!")
```


```python
chat("They all sound fun, honestly. Is there one that you're most excited about?")
```


```python
chat("That's nice! I would enjoy exploring uses or extensions, sure. I'm wondering if it also \
     makes sense to give you a derivative function, and if it should handle partial derivatives.")
```


```python
fn = Path('fasthtml-homepage-small.png')
img = fn.read_bytes()
display.Image(filename=fn, width=200)
```


```python

```
