# SVG Animations in FastHTML

Exploring how to make basic SVG animations work with FastHTML.


```python
from fastcore.meta import delegates
from fastcore.utils import snake2camel
from fasthtml.common import *
from fasthtml.svg import *
```

## FastHTML SVG Docs Examples

The [FastHTML SVG API Docs](https://docs.fastht.ml/api/svg.html) introduce you to `fasthtml.svg` with this nice circle specified as an SVG string:


```python
svg = '<svg width="50" height="50"><circle cx="20" cy="20" r="15" fill="red"></circle></svg>'
show(NotStr(svg))
```


<svg width="50" height="50"><circle cx="20" cy="20" r="15" fill="red"></circle></svg>


Often you'll just want to paste these strings into your FastHTML apps, and that's fine. However, when you want to construct SVG elements programmatically via Python, you can!


```python
def demo(el, h=50, w=50): return show(Svg(h=h,w=w)(el))
```


```python
demo(Rect(30, 30, fill='blue', rx=8, ry=8))
```


<svg xmlns="http://www.w3.org/2000/svg" viewbox="0 0 50 50" height="50" width="50"><rect width="30" height="30" fill="blue" rx="8" ry="8"></rect></svg>


## MDN Example

[MDN's SVG <animate> example](https://developer.mozilla.org/en-US/docs/Web/SVG/Element/animate) is:


```python
svg = """<svg viewBox="0 0 10 10" xmlns="http://www.w3.org/2000/svg">
  <rect width="10" height="10">
    <animate
      attributeName="rx"
      values="0;5;0"
      dur="10s"
      repeatCount="indefinite" />
  </rect>
</svg>
"""
```


```python
show(NotStr(svg))
```


<svg viewBox="0 0 10 10" xmlns="http://www.w3.org/2000/svg">
  <rect width="10" height="10">
    <animate
      attributeName="rx"
      values="0;5;0"
      dur="10s"
      repeatCount="indefinite" />
  </rect>
</svg>



Why is that rectangle so big here? Let's try


```python
svg2 = """<svg width="100" height="100">
  <rect width="10" height="10">
    <animate
      attributeName="rx"
      values="0;5;0"
      dur="10s"
      repeatCount="indefinite" />
  </rect>
</svg>
"""
show(NotStr(svg2))
```


<svg width="100" height="100">
  <rect width="10" height="10">
    <animate
      attributeName="rx"
      values="0;5;0"
      dur="10s"
      repeatCount="indefinite" />
  </rect>
</svg>



## MDN Example in FastHTML

Currently `Rect()` doesn't accept an `animate` child. Seeing if I can make that work:


```python
def Animate(attributeName, values, dur, repeatCount):
    return Safe(f"<animate {attributeName=} {values=} {dur=} {repeatCount=} />")
```


```python
Animate(attributeName="rx", values="0;5;0", dur="10s", repeatCount="indefinite")
```




    "<animate attributeName='rx' values='0;5;0' dur='10s' repeatCount='indefinite' />"




```python
@delegates(ft_svg)
def AnimatedRect(animate, width, height, x=0, y=0, fill=None, stroke=None, stroke_width=None, rx=None, ry=None, **kwargs):
    "An animated standard SVG `rect` element"
    return ft_svg('rect', animate, width=width, height=height, x=x, y=y, fill=fill,
                 stroke=stroke, stroke_width=stroke_width, rx=rx, ry=ry, **kwargs)
```


```python
show(Svg(AnimatedRect(
    Animate(attributeName="rx", values="0;5;0", dur="10s", repeatCount="indefinite"), 
    width=10, height=10), h=10, w=10))
```


<svg xmlns="http://www.w3.org/2000/svg" viewbox="0 0 10 10" height="10" width="10"><rect width="10" height="10"><animate attributeName='rx' values='0;5;0' dur='10s' repeatCount='indefinite' /></rect></svg>



```python
show(Svg(AnimatedRect(
    Animate(attributeName="rx", values="0;50;0", dur="10s", repeatCount="indefinite"), 
    width=100, height=100), h=100, w=100))
```


<svg xmlns="http://www.w3.org/2000/svg" viewbox="0 0 100 100" height="100" width="100"><rect width="100" height="100"><animate attributeName='rx' values='0;50;0' dur='10s' repeatCount='indefinite' /></rect></svg>



```python
demo(AnimatedRect(
        Animate(attributeName="rx", values="0;50;0", dur="1s", repeatCount="indefinite"), 
    width=100, height=100), h=100, w=100)
```


<svg xmlns="http://www.w3.org/2000/svg" viewbox="0 0 100 100" height="100" width="100"><rect width="100" height="100"><animate attributeName='rx' values='0;50;0' dur='1s' repeatCount='indefinite' /></rect></svg>


## More Complex SVG Animation


```python
svg4 = """<svg width="100" height="100" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
  <!-- Gradient definitions -->
  <defs>
    <linearGradient id="gradient1" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#60a5fa">
        <animate attributeName="stop-color" 
          values="#60a5fa;#8b5cf6;#ec4899;#60a5fa"
          dur="8s" repeatCount="indefinite" />
      </stop>
      <stop offset="100%" stop-color="#8b5cf6">
        <animate attributeName="stop-color" 
          values="#8b5cf6;#ec4899;#60a5fa;#8b5cf6"
          dur="8s" repeatCount="indefinite" />
      </stop>
    </linearGradient>
  </defs>

  <!-- Background star burst -->
  <g>
    <circle cx="50" cy="50" r="45" fill="url(#gradient1)">
      <animate attributeName="opacity"
        values="0.3;0.5;0.3"
        dur="3s" repeatCount="indefinite" />
    </circle>
  </g>

  <!-- Spinning triangles -->
  <g transform="translate(50 50)">
    <path d="M0,-30 L26,15 L-26,15 Z" fill="#fcd34d" opacity="0.8">
      <animateTransform attributeName="transform"
        type="rotate"
        from="0"
        to="360"
        dur="8s"
        repeatCount="indefinite" />
      <animate attributeName="d"
        values="M0,-30 L26,15 L-26,15 Z;M0,-20 L35,25 L-35,25 Z;M0,-30 L26,15 L-26,15 Z"
        dur="4s"
        repeatCount="indefinite" />
    </path>
  </g>

  <!-- Bouncing squares -->
  <rect x="40" y="40" width="20" height="20" fill="#34d399" opacity="0.8">
    <animate attributeName="x" 
      values="40;30;50;40"
      dur="3s"
      repeatCount="indefinite" />
    <animate attributeName="y"
      values="40;50;30;40"
      dur="3s"
      repeatCount="indefinite" />
    <animate attributeName="rx"
      values="0;10;0"
      dur="3s"
      repeatCount="indefinite" />
  </rect>

  <!-- Orbiting particles -->
  <g>
    <circle cx="50" cy="20" r="4" fill="#f472b6">
      <animateMotion
        path="M 0,0 a 30,30 0 1,1 0,0"
        dur="3s"
        repeatCount="indefinite" />
      <animate attributeName="r"
        values="4;6;4"
        dur="1.5s"
        repeatCount="indefinite" />
    </circle>
    <circle cx="80" cy="50" r="4" fill="#60a5fa">
      <animateMotion
        path="M 0,0 a 30,30 0 1,0 0,0"
        dur="4s"
        repeatCount="indefinite" />
      <animate attributeName="r"
        values="4;6;4"
        dur="2s"
        repeatCount="indefinite" />
    </circle>
  </g>

  <!-- Dancing dots -->
  <g>
    <circle cx="50" cy="50" r="3" fill="#fcd34d">
      <animateMotion
        path="M 0,0 q 15,15 0,30 q -15,15 0,0"
        dur="2.5s"
        repeatCount="indefinite" />
    </circle>
    <circle cx="50" cy="50" r="3" fill="#f472b6">
      <animateMotion
        path="M 0,0 q -15,-15 -30,0 q -15,15 0,0"
        dur="2.5s"
        repeatCount="indefinite" />
    </circle>
  </g>

  <!-- Pulsing rings -->
  <circle cx="50" cy="50" r="20" fill="none" stroke="#93c5fd" stroke-width="1">
    <animate attributeName="r"
      values="20;30;20"
      dur="4s"
      repeatCount="indefinite" />
    <animate attributeName="stroke-opacity"
      values="1;0;1"
      dur="4s"
      repeatCount="indefinite" />
  </circle>
  <circle cx="50" cy="50" r="25" fill="none" stroke="#93c5fd" stroke-width="1">
    <animate attributeName="r"
      values="25;35;25"
      dur="4s"
      repeatCount="indefinite" />
    <animate attributeName="stroke-opacity"
      values="0;1;0"
      dur="4s"
      repeatCount="indefinite" />
  </circle>
</svg>"""
show(NotStr(svg4))
```


<svg width="100" height="100" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
  <!-- Gradient definitions -->
  <defs>
    <linearGradient id="gradient1" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#60a5fa">
        <animate attributeName="stop-color" 
          values="#60a5fa;#8b5cf6;#ec4899;#60a5fa"
          dur="8s" repeatCount="indefinite" />
      </stop>
      <stop offset="100%" stop-color="#8b5cf6">
        <animate attributeName="stop-color" 
          values="#8b5cf6;#ec4899;#60a5fa;#8b5cf6"
          dur="8s" repeatCount="indefinite" />
      </stop>
    </linearGradient>
  </defs>

  <!-- Background star burst -->
  <g>
    <circle cx="50" cy="50" r="45" fill="url(#gradient1)">
      <animate attributeName="opacity"
        values="0.3;0.5;0.3"
        dur="3s" repeatCount="indefinite" />
    </circle>
  </g>

  <!-- Spinning triangles -->
  <g transform="translate(50 50)">
    <path d="M0,-30 L26,15 L-26,15 Z" fill="#fcd34d" opacity="0.8">
      <animateTransform attributeName="transform"
        type="rotate"
        from="0"
        to="360"
        dur="8s"
        repeatCount="indefinite" />
      <animate attributeName="d"
        values="M0,-30 L26,15 L-26,15 Z;M0,-20 L35,25 L-35,25 Z;M0,-30 L26,15 L-26,15 Z"
        dur="4s"
        repeatCount="indefinite" />
    </path>
  </g>

  <!-- Bouncing squares -->
  <rect x="40" y="40" width="20" height="20" fill="#34d399" opacity="0.8">
    <animate attributeName="x" 
      values="40;30;50;40"
      dur="3s"
      repeatCount="indefinite" />
    <animate attributeName="y"
      values="40;50;30;40"
      dur="3s"
      repeatCount="indefinite" />
    <animate attributeName="rx"
      values="0;10;0"
      dur="3s"
      repeatCount="indefinite" />
  </rect>

  <!-- Orbiting particles -->
  <g>
    <circle cx="50" cy="20" r="4" fill="#f472b6">
      <animateMotion
        path="M 0,0 a 30,30 0 1,1 0,0"
        dur="3s"
        repeatCount="indefinite" />
      <animate attributeName="r"
        values="4;6;4"
        dur="1.5s"
        repeatCount="indefinite" />
    </circle>
    <circle cx="80" cy="50" r="4" fill="#60a5fa">
      <animateMotion
        path="M 0,0 a 30,30 0 1,0 0,0"
        dur="4s"
        repeatCount="indefinite" />
      <animate attributeName="r"
        values="4;6;4"
        dur="2s"
        repeatCount="indefinite" />
    </circle>
  </g>

  <!-- Dancing dots -->
  <g>
    <circle cx="50" cy="50" r="3" fill="#fcd34d">
      <animateMotion
        path="M 0,0 q 15,15 0,30 q -15,15 0,0"
        dur="2.5s"
        repeatCount="indefinite" />
    </circle>
    <circle cx="50" cy="50" r="3" fill="#f472b6">
      <animateMotion
        path="M 0,0 q -15,-15 -30,0 q -15,15 0,0"
        dur="2.5s"
        repeatCount="indefinite" />
    </circle>
  </g>

  <!-- Pulsing rings -->
  <circle cx="50" cy="50" r="20" fill="none" stroke="#93c5fd" stroke-width="1">
    <animate attributeName="r"
      values="20;30;20"
      dur="4s"
      repeatCount="indefinite" />
    <animate attributeName="stroke-opacity"
      values="1;0;1"
      dur="4s"
      repeatCount="indefinite" />
  </circle>
  <circle cx="50" cy="50" r="25" fill="none" stroke="#93c5fd" stroke-width="1">
    <animate attributeName="r"
      values="25;35;25"
      dur="4s"
      repeatCount="indefinite" />
    <animate attributeName="stroke-opacity"
      values="0;1;0"
      dur="4s"
      repeatCount="indefinite" />
  </circle>
</svg>


I kind of like this one for representing "a sound is currently playing" for experimental audio apps.
