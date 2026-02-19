# Introducing Air: A Pioneering AI-First Python Web Framework

Air is a pioneering AI-first Python web framework that represents the next evolution in web frameworks to be deeply AI-native. 

## This is a Post to Answer Your Questions

We've gotten a ton of questions about how it compares to other Python web frameworks. This post is my attempt to answer some of that.

For more answers:

* Watch this blog and [daniel.feldroy.com](https://daniel.feldroy.com)
* Join the [Air Discord](https://airwebframework.org/discord/) and read through the chat history
* Follow us on Twitter [@AirWebFramework](https://x.com/AirWebFramework)

## Why I Haven't Blogged About Air Yet

I've been keeping a low profile while working on Air because I wanted space to play around and experiment. I want to start blogging about what I'm doing with Air. This is just the start. My posts will not answer "Why?" but be more of explorations, recipes, and progress updates.

This early post is part of that experimental phase, and yes, it's still in alpha. If you want to try something that's wild, experimental, uses only bleeding-edge dependencies, and is already ridiculously useful to us, then join the growing Air community.

## Air Builds On Our Experience

Air builds on our deep experience and passion working with Python web frameworks, borrows great ideas the JavaScript and Ruby communities, and embraces a modern, AI-first approach.

### Django: Setting the Bar and More

The way I see it, Air is primarily being built on my and [Daniel Roy Greenfeld](https://daniel.feldroy.com)'s Django expertise. We wrote Two Scoops of Django, the book that established best practices for Django back when things were very uncertain. We spent over a decade contributing a ton to Django through our books and the package ecosystem. We got to shape and know Django inside and out, as well as areas where it could be modernized.

Django is truly great, and as we design every API in Air, Django sets the bar for quality. We ask ourselves, is this as good as the Django experience? If not, we keep iterating. We implement work-alike modules, classes, functions for the things we want most. 

Air Forms are inspired by django-crispy-forms, a library by Daniel (originally called django-uni-form and written while he was an engineer at NASA). They are still evolving - imagine next-gen Crispy Forms with Pydantic validation and updated components.

The forthcoming Air Admin will be heavily inspired by not just Django's built-in admin but by the best of the third-party Django admin community. Think automatic and extensible, but much more powerful and user-friendly. 

There will likely be Django connectors for Air. We want to build bridges, not compete. The more we can encourage helping each other and sharing in the Python web ecosystem, the better. Talk to us if you have ideas for how to architect any of these pieces.

### FastHTML and Predecessors: HTML Generation from Python Objects, and HTMX

Air Tags were inspired by our work experience on the FastHTML core team. When we wanted to add FastAPI to our FastHTML sites and use standard Python tooling and practices for better AI agent usability, we realized we sadly had to port our projects off. The use of Python to generate HTML in FastHTML and the confidence to build a new modern web framework today was what originally attracted me to join the company behind it, and those things still stick with me after leaving. 

For Air Tags I give full credit to FastHTML's amazing predecessors too: Dash, htmy, JustPy, and others pioneered using Python classes and/or functions to generate equivalent HTML. You will see the inspiration right away if you're familiar with those:

```python
import air

my_component = air.Div(
    air.H1("Hello from Air!", class_="title"),
    air.P("This was written entirely in Python."),
    style="font-family: sans-serif;"
)
```

Also inspired by FastHTML, Air makes HTMX a first-class citizen by default, allowing you the ability to make reactive sites without React or other JavaScript. While we have a lot of respect for JS and have worked extensively with React and Vue.js, extra development and deployment effort is needed to add heavy JS front-ends to FastAPI projects, which makes it hard for AI agents and people to build apps fast.

### Flask: Templates and Flexibility

Even with Air Tags, I strongly prefer Jinja templates for most HTML rendering. Air extends Flask's approach. But that's just me. Daniel strongly prefers to work with Air Tags. Air lets you use either workflow or combine them and meet in the middle.

Personally my Air workflow is very similar to a common modern Jinja/Flask development approach:

1. Use LLMs to build static HTML mockups
2. Then convert them to Jinja templates, and wire in Python functions to populate them with fake data
3. Then wire in the real database

### Meteor: Developer Experience

DX/DevEx in Air is inspired by my experience working on early Meteor.js. Years ago I worked with the core Meteor team in San Francisco. What stands strong in my mind is how obsessed Geoff Schmidt, Matt DeBergalis, and Nick Martin were with user experience for developers. They really just cared so much about DX, even in the face of community and investor pressure to focus elsewhere. I've never met web framework authors who were so obsessive about making every piece, every docs page or tool and developer-facing API, feel amazing to use.

### Modularity: Pyramid

Modularity in Air is inspired by Pyramid. I spent countless hours with Pyramid devs in Los Angeles, hearing them talk about Pyramid's design for a modular and swappable architecture and early goal of interoperable components that all web frameworks could share. I spent a PyCon sprint working with Pyramid author Chris McDonough, helping him improve the developer experience for new users.

### Scaffolding: RedwoodJS and Rails

RedwoodJS and Rails are the influences on Air's forthcoming approach to scaffolding. I worked with early Rails before I worked with Django, and I always missed Rails' scaffolding commands. I explored bringing more powerful scaffolding to Django years ago with my django-startcbv package. During the pandemic I explored RedwoodJS and appreciated its commands like `yarn redwood generate page home /` to generate a page, route, test, and Storybook file. That's way better than using LLMs to generate those starter files from scratch.

As scaffolding support we'll be using Cookiecutter's API. But first we have to modernize Cookiecutter, which is a huge project of its own. Years ago I wrote Cookiecutter which is one of the world's most popular project templating tools today, and I have a vision for using it as a critical part of Air.

## The Core Idea

Besides bringing the best of other web frameworks together, Air is specifically architected to be optimal for AI agents writing code. We've handcrafted Air to work beautifully with AI and humans equally. Every function, class, module, docs page, etc. is AI-optimized as best as possible.

Docstrings are comprehensive, with clear parameter descriptions and working examples. Formatters, linters, and type checkers work because we know how much better your code becomes when your AI agents can use them fully. 

Our goal is to allow agentic AI tools like OpenAI Codex, Anthropic's Claude Code, GitHub Copilot, and Amp to generate better code and provide much more intelligent suggestions.

## Database Integration

We use PostgreSQL (but we're very open to adding modern database connectors for whatever others use). This is a work in progress:

* Air currently includes SQLModel/SQLAlchemy integration through `air.ext.sqlmodel`, with database connection handling and helpful utilities like `get_object_or_404`. 
* Air will soon provide sensible defaults and patterns for building apps with raw SQL, asyncpg, and Pydantic in the forthcoming `air.ext.asyncpg`. 

It's so early that we haven't figured out our preferred patterns here yet. We have a test project set up with SQLAlchemy, SQLModel, and Alembic, and another with raw SQL + asyncpg + the Go-based Dbmate, and we're A/B testing to see what feels right. It may take a few more test projects to see what really works for us.

## Authentication

We make it easy to add a "Log in with GitHub" button to your apps. Air provides GitHub OAuth support and an OAuth router factory for authentication flows, built on OAuthlib. 

We have Air projects working with both GitHub OAuth apps and standard GitHub apps.

## FastAPI and Starlette Foundation

With Air built directly on top of FastAPI and Starlette, you get everything they provide including easy building of REST API endpoints, async support, automatic OpenAPI/Swagger docs, middleware, response types, etc. 

We import and use things from FastAPI and Starlette into our Air web apps all the time, and use them the way we normally would.

## Friend and Collaborator to Other Frameworks, Not a Competitor

We often get pressure to talk about the weaknesses and flaws of other frameworks. We're not building Air to compete with anyone. We're building it to fill the gaps not filled elsewhere. Just know that we definitely wouldn't build Air if existing frameworks met our needs.

Our hope is to eventually build bridges and connectors to other web frameworks, starting with Django. If you're a core team member of another web framework and want to collaborate, please reach out to us.

## Alpha Status

Air is in alpha. That means it's our playground to explore and make breaking changes freely. We put out new releases of Air all the time. Sometimes new release are like Christmas, where you get new features. Other times they break your projects. Such is life in alpha.

## So, Is Air Launched?

This is a long blog post that sort of resembles a launch post, but it's for transparency with the community, not a launch post. The official launch is still to come.

We soft-launched Air to a small group at Python Philippines in August 2025. Now we have a growing community of early Air adopters who build stuff with us.  You can be a part of this.


## Truly Free and Open-Source Software

We believe in true freedom - you can take your Air app and run it anywhere without vendor lock-in. We won't suddenly lock you into using a proprietary hosting platform. We don't even want to build one.

## Give Us Space to Build Out Air

I hope this answers a lot of the "But why are you building this?" questions. 

You probably have more questions or are eager to make comparisons. Air's not ready to compare, it's way too early. Just be patient with us, don't judge Air for what it is in its early alpha state, and give us space to code. 

I promise we're building something special. I'll blog more about Air. You'll see it unfold and evolve, piece by piece.

## Air Is Our Collaborative Work of Art

Borrowing from my days as a professional studio artist in SF, Air is like the first pieces of a found-object sculpture coming together. It's raw and unrefined, as we play around and see what pieces fit.

We don't know what it will look like eventually. But it will use all the best pieces that we find and assemble, plus a ton of love, nails, strings, and glue.

Not everyone will like it, but it will be beautiful to us, and probably a bit strange and weird in the end.

## Try It, and Then Join Us

First, go star [Air on GitHub](https://github.com/feldroy/air).

Then when you have 30 minutes to spare, read the official docs, and try building a little web app. 

If you give it a chance, we know you'll see Air's potential and want to help. Join the [Air Discord](https://airwebframework.org/discord/) community to get involved.

Air is free software and we invite everyone to contribute, starting with pull requests to make the newcomer's experience better.


