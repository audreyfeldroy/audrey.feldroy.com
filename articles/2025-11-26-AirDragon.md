# Introducing AirDragon: A Component Library Born on an Airplane

On a recent flight from Japan to the Philippines, [Pydanny](https://daniel.feldroy.com/) and I started coding a new project. The result is **AirDragon**, a layout and component library for the [Air](https://github.com/air-py/air-py) web framework.

We landed on the name AirDragon because it sounded dynamic and airy, fitting for a library meant to help you build UIs that feel light and responsive. Plus, we were on an airplane. Dragons fly, after all.

The goal is to provide an initial component library for Air, letting you think in terms of components, much like the early days of Bootstrap. It's designed to help you build interfaces quickly with sensible, stylish defaults.

### Getting Started: The Basics

Using AirDragon is straightforward. You import it alongside Air, and you can start using its components immediately. We recommend importing it as the 2-letter `ad` for convenience. `ad` is also short for AudreyDanny, so you'll think of us as you code.

```
import air
import air_dragon as ad

def app(air):
    air.layout(
        ad.H1("Hello World")
    )

```

Here, instead of the standard `air.H1`, we use `ad.H1`. This small change gives us a pre-styled heading element.

Screenshot at [00:20]:

![The rendered Hello World heading in the browser.](https://devrelifier-public.s3.amazonaws.com/public/screenshots/sha256/86/8672514d09c4a9689cc186c796433bb153f37dfa9e53e44980c832d80db901f5.jpg)

If you open the page in a web browser and then inspect the element, you'll see that AirDragon has applied several [Tailwind CSS](https://tailwindcss.com/) utility classes to provide default styling. Here, 

Here at [01:25] you can see the `text-3xl sm:text-4xl font-semibold leading-tight` classes were added to make the `h1` text large and responsive. (The header styles aren't from Basecoat, they're from Danny's awesome UI design sensibilities, using AI to combine Tailwind classes for the header look he wanted right before we got on the plane).

![Browser inspector showing the default Tailwind classes on the H1 element.](https://devrelifier-public.s3.amazonaws.com/public/screenshots/sha256/d6/d6ef3c4327a6f248f88e40e7feb93974072ab2197af1b3e47df7804b2caa1562.jpg)

### Customization and Overrides

While the defaults are designed to be useful, you're not locked into them. You can easily append your own classes. If we want to add a `Dragons` class, we just pass it in.

```
ad.H1("Hello World", class_="Dragons")

```

(Note: he doesn't know why he capitalized it. He says he did so in the heat of the moment. You can lowercase your class names if that feels better. I think I would. Unless the same thing happened to me while recording a video.)

AirDragon intelligently appends your class (case-sensitively, yeah) to the existing list, giving you the power to extend the base styles.

Screenshot at [02:10]:

![Code demonstrating how to add a custom class to an AirDragon component.](https://devrelifier-public.s3.amazonaws.com/public/screenshots/sha256/ca/ca47fc455850aebbcb4a885e201de041850d9293b04bdf52c8bd794776aa9882.jpg)

Of course, if you want complete control and none of AirDragon's default styling, you can always fall back to the standard Air components:

```
# This will have no default AirDragon styles
air.h1("Hello World", class_="dragons")

```

### Building with Components: A Practical Example

The real power of AirDragon comes from its collection of higher-level components like cards, buttons, and headers. Let's build a simple card to see it in action.

A card in AirDragon is structured with a `Header`, `Section`, and an optional `Footer`.

```
# ... inside air.layout()
AD.Card(
    AD.Header(
        AD.H2("Card Title")
    ),
    AD.Section(
        # Card content goes here...
    )
)

```

Screenshot at [03:25]:

![Code for creating a basic card component with a header.](https://devrelifier-public.s3.amazonaws.com/public/screenshots/sha256/2f/2f82d9307450b683f09604770a9f2501ebb51fdbd45b4df681bb6e3dd72d8a2a.jpg)

### Adding Buttons and Variants

Now, let's add some actions to our card. AirDragon includes a `ButtonGroup` component for laying out buttons, and `Button`s come with different variants. This is similar to patterns in other UI frameworks where you have primary, secondary, or destructive actions.

Here, we'll add a standard button and a "destructive" variant, which is styled in red to indicate a potentially dangerous action.

```
# ... inside the AD.Section()
AD.ButtonGroup(
    AD.Button("Save Changes"),
    AD.Button("Delete", class_="destructive")
)

```

Screenshot at [05:05]:

![Code showing the addition of a ButtonGroup with default and destructive buttons.](https://devrelifier-public.s3.amazonaws.com/public/screenshots/sha256/4a/4a319aa00a416d52c77fa72a68dbc605a67ce640cd1a419c2923b1859105e4f4.jpg)

Putting it all together, we get a clean, well-structured card component with just a few lines of Python.

Screenshot at [06:20]:

![The fully rendered card component with a title, section, and buttons.](https://devrelifier-public.s3.amazonaws.com/public/screenshots/sha256/fb/fb07ae74bdcc301a945d44a06ca5f50018aff2cc693ce07d73b0185ab4f33d32.jpg)

### Under the Hood and the Broader Ecosystem

AirDragon is built on top of **Basecoat**, which is a port of the popular **Shadcn/ui** from the React ecosystem to plain HTML and CSS. This provides a solid and modern design foundation for our components. But it's not just Basecoat for Air, it's more like Basecoat + whatever we think looks good.

The Air component ecosystem is still young and growing. There are several great projects exploring different patterns. If you're looking for alternatives, you might also check out Isaac Flath's work on [EidosUI](https://github.com/kentro-tech/eidosui). It's an exciting time with lots of innovation happening.

### What's Next

AirDragon is still in its very early stages. As we saw during the live demo, some things are still being built and refined. For example, creating a grid of cards requires a bit more layout work.

Screenshot at [07:40]:

![Two card components rendered vertically, showing an area for future layout improvements.](https://devrelifier-public.s3.amazonaws.com/public/screenshots/sha256/c2/c23d48f839c53770b1282db381da0c52eef8370ada06bae163452ef406a2e813.jpg)

Our focus is on hashing out the core UI and establishing simple, straightforward defaults that empower developers to build things quickly. We believe AirDragon can be a valuable tool for anyone looking to create beautiful, component-driven user interfaces with Air. We're excited to see where it goes.
