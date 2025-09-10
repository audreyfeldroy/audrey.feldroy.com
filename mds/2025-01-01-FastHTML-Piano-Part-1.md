# FastHTML Piano, Part 1

My adaptation of https://developer.mozilla.org/en-US/play to FastHTML, with improvements.


```python
from fastcore.all import *
from fasthtml.common import *
from fasthtml.jupyter import *
```

## Keys

Just the natural keys for now.


```python
def Key(note): return Div(
    Div(note, style='position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;'),
    style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;')
```


```python
show(Key('C'),Key('D'))
```


<div style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
  <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">C</div>
</div>
<div style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
  <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">D</div>
</div>
<script>if (window.htmx) htmx.process(document.body)</script>


The sharp/flat keys would be fun to add later, but we'll see how far I get.

## Keys With Octaves


```python
def Key(note, octave): return Div(
    Div(note, Sub(octave, style='font-size:10px;pointer-events:none;'), style='position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;'),
    style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;')
```


```python
show(Key('C','5'), Key('D','5'))
```


<div style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
  <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
C<sub style="font-size:10px;pointer-events:none;">5</sub>  </div>
</div>
<div style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
  <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
D<sub style="font-size:10px;pointer-events:none;">5</sub>  </div>
</div>
<script>if (window.htmx) htmx.process(document.body)</script>


## Adding Key Hover States

Top answer on https://stackoverflow.com/questions/1033156/how-can-i-write-ahover-in-inline-css says not to add hover states to inline CSS. 2nd answer says to change style in onMouseOver and onMouseOut. Maybe a fun opportunity for HTMX here.

MDN's CSS is:

```css
.key:hover{background-color:#eef;}

.key:active,
.active {background-color:#000;color:#fff;}
```


```python
def Key(note, octave): return Div(
    Div(note, Sub(octave, style='font-size:10px;pointer-events:none;'), style='position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;'),
    onmouseover="event.target.style.backgroundColor = '#eef';",
    onmouseout="event.target.style.backgroundColor = '#fff';",
    style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;')
```


```python
show(Key('E','5'), Key('F','5'))
```


<div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
  <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
E<sub style="font-size:10px;pointer-events:none;">5</sub>  </div>
</div>
<div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
  <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
F<sub style="font-size:10px;pointer-events:none;">5</sub>  </div>
</div>
<script>if (window.htmx) htmx.process(document.body)</script>


## Adding Octave Container


```python
show(partial(Key, octave=3)('C'))
```


<div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
  <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
C<sub style="font-size:10px;pointer-events:none;">3</sub>  </div>
</div>
<script>if (window.htmx) htmx.process(document.body)</script>



```python
notes = L(['C', 'D', 'E', 'F', 'G', 'A', 'B'])
```


```python
show(Div(*notes.map(partial(Key,octave=2))))
```


<div>
  <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
    <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
C<sub style="font-size:10px;pointer-events:none;">2</sub>    </div>
  </div>
  <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
    <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
D<sub style="font-size:10px;pointer-events:none;">2</sub>    </div>
  </div>
  <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
    <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
E<sub style="font-size:10px;pointer-events:none;">2</sub>    </div>
  </div>
  <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
    <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
F<sub style="font-size:10px;pointer-events:none;">2</sub>    </div>
  </div>
  <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
    <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
G<sub style="font-size:10px;pointer-events:none;">2</sub>    </div>
  </div>
  <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
    <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
A<sub style="font-size:10px;pointer-events:none;">2</sub>    </div>
  </div>
  <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
    <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
B<sub style="font-size:10px;pointer-events:none;">2</sub>    </div>
  </div>
</div>
<script>if (window.htmx) htmx.process(document.body)</script>



```python
def Octave(n):
    return Div(*notes.map(partial(Key,octave=n)),
        style='display:inline-block;padding:0 6px 0 0;')
```


```python
show(Div(Octave(1)))
```


<div>
  <div style="display:inline-block;padding:0 6px 0 0;">
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
C<sub style="font-size:10px;pointer-events:none;">1</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
D<sub style="font-size:10px;pointer-events:none;">1</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
E<sub style="font-size:10px;pointer-events:none;">1</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
F<sub style="font-size:10px;pointer-events:none;">1</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
G<sub style="font-size:10px;pointer-events:none;">1</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
A<sub style="font-size:10px;pointer-events:none;">1</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
B<sub style="font-size:10px;pointer-events:none;">1</sub>      </div>
    </div>
  </div>
</div>
<script>if (window.htmx) htmx.process(document.body)</script>


## Multiple Octaves


```python
show(Div(Octave(1),Octave(2),Octave(3)))
```


<div>
  <div style="display:inline-block;padding:0 6px 0 0;">
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
C<sub style="font-size:10px;pointer-events:none;">1</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
D<sub style="font-size:10px;pointer-events:none;">1</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
E<sub style="font-size:10px;pointer-events:none;">1</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
F<sub style="font-size:10px;pointer-events:none;">1</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
G<sub style="font-size:10px;pointer-events:none;">1</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
A<sub style="font-size:10px;pointer-events:none;">1</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
B<sub style="font-size:10px;pointer-events:none;">1</sub>      </div>
    </div>
  </div>
  <div style="display:inline-block;padding:0 6px 0 0;">
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
C<sub style="font-size:10px;pointer-events:none;">2</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
D<sub style="font-size:10px;pointer-events:none;">2</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
E<sub style="font-size:10px;pointer-events:none;">2</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
F<sub style="font-size:10px;pointer-events:none;">2</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
G<sub style="font-size:10px;pointer-events:none;">2</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
A<sub style="font-size:10px;pointer-events:none;">2</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
B<sub style="font-size:10px;pointer-events:none;">2</sub>      </div>
    </div>
  </div>
  <div style="display:inline-block;padding:0 6px 0 0;">
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
C<sub style="font-size:10px;pointer-events:none;">3</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
D<sub style="font-size:10px;pointer-events:none;">3</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
E<sub style="font-size:10px;pointer-events:none;">3</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
F<sub style="font-size:10px;pointer-events:none;">3</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
G<sub style="font-size:10px;pointer-events:none;">3</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
A<sub style="font-size:10px;pointer-events:none;">3</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
B<sub style="font-size:10px;pointer-events:none;">3</sub>      </div>
    </div>
  </div>
</div>
<script>if (window.htmx) htmx.process(document.body)</script>



```python
show(Div(*L(range(8)).map(Octave)))
```


<div>
  <div style="display:inline-block;padding:0 6px 0 0;">
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
C<sub style="font-size:10px;pointer-events:none;">0</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
D<sub style="font-size:10px;pointer-events:none;">0</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
E<sub style="font-size:10px;pointer-events:none;">0</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
F<sub style="font-size:10px;pointer-events:none;">0</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
G<sub style="font-size:10px;pointer-events:none;">0</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
A<sub style="font-size:10px;pointer-events:none;">0</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
B<sub style="font-size:10px;pointer-events:none;">0</sub>      </div>
    </div>
  </div>
  <div style="display:inline-block;padding:0 6px 0 0;">
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
C<sub style="font-size:10px;pointer-events:none;">1</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
D<sub style="font-size:10px;pointer-events:none;">1</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
E<sub style="font-size:10px;pointer-events:none;">1</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
F<sub style="font-size:10px;pointer-events:none;">1</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
G<sub style="font-size:10px;pointer-events:none;">1</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
A<sub style="font-size:10px;pointer-events:none;">1</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
B<sub style="font-size:10px;pointer-events:none;">1</sub>      </div>
    </div>
  </div>
  <div style="display:inline-block;padding:0 6px 0 0;">
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
C<sub style="font-size:10px;pointer-events:none;">2</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
D<sub style="font-size:10px;pointer-events:none;">2</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
E<sub style="font-size:10px;pointer-events:none;">2</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
F<sub style="font-size:10px;pointer-events:none;">2</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
G<sub style="font-size:10px;pointer-events:none;">2</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
A<sub style="font-size:10px;pointer-events:none;">2</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
B<sub style="font-size:10px;pointer-events:none;">2</sub>      </div>
    </div>
  </div>
  <div style="display:inline-block;padding:0 6px 0 0;">
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
C<sub style="font-size:10px;pointer-events:none;">3</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
D<sub style="font-size:10px;pointer-events:none;">3</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
E<sub style="font-size:10px;pointer-events:none;">3</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
F<sub style="font-size:10px;pointer-events:none;">3</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
G<sub style="font-size:10px;pointer-events:none;">3</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
A<sub style="font-size:10px;pointer-events:none;">3</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
B<sub style="font-size:10px;pointer-events:none;">3</sub>      </div>
    </div>
  </div>
  <div style="display:inline-block;padding:0 6px 0 0;">
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
C<sub style="font-size:10px;pointer-events:none;">4</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
D<sub style="font-size:10px;pointer-events:none;">4</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
E<sub style="font-size:10px;pointer-events:none;">4</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
F<sub style="font-size:10px;pointer-events:none;">4</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
G<sub style="font-size:10px;pointer-events:none;">4</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
A<sub style="font-size:10px;pointer-events:none;">4</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
B<sub style="font-size:10px;pointer-events:none;">4</sub>      </div>
    </div>
  </div>
  <div style="display:inline-block;padding:0 6px 0 0;">
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
C<sub style="font-size:10px;pointer-events:none;">5</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
D<sub style="font-size:10px;pointer-events:none;">5</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
E<sub style="font-size:10px;pointer-events:none;">5</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
F<sub style="font-size:10px;pointer-events:none;">5</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
G<sub style="font-size:10px;pointer-events:none;">5</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
A<sub style="font-size:10px;pointer-events:none;">5</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
B<sub style="font-size:10px;pointer-events:none;">5</sub>      </div>
    </div>
  </div>
  <div style="display:inline-block;padding:0 6px 0 0;">
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
C<sub style="font-size:10px;pointer-events:none;">6</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
D<sub style="font-size:10px;pointer-events:none;">6</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
E<sub style="font-size:10px;pointer-events:none;">6</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
F<sub style="font-size:10px;pointer-events:none;">6</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
G<sub style="font-size:10px;pointer-events:none;">6</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
A<sub style="font-size:10px;pointer-events:none;">6</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
B<sub style="font-size:10px;pointer-events:none;">6</sub>      </div>
    </div>
  </div>
  <div style="display:inline-block;padding:0 6px 0 0;">
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
C<sub style="font-size:10px;pointer-events:none;">7</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
D<sub style="font-size:10px;pointer-events:none;">7</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
E<sub style="font-size:10px;pointer-events:none;">7</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
F<sub style="font-size:10px;pointer-events:none;">7</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
G<sub style="font-size:10px;pointer-events:none;">7</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
A<sub style="font-size:10px;pointer-events:none;">7</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
B<sub style="font-size:10px;pointer-events:none;">7</sub>      </div>
    </div>
  </div>
</div>
<script>if (window.htmx) htmx.process(document.body)</script>



```python
def Keyboard(): return Div(*L(range(8)).map(Octave), style="width:auto;padding:0;margin:0;")
show(Keyboard())
```


<div style="width:auto;padding:0;margin:0;">
  <div style="display:inline-block;padding:0 6px 0 0;">
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
C<sub style="font-size:10px;pointer-events:none;">0</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
D<sub style="font-size:10px;pointer-events:none;">0</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
E<sub style="font-size:10px;pointer-events:none;">0</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
F<sub style="font-size:10px;pointer-events:none;">0</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
G<sub style="font-size:10px;pointer-events:none;">0</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
A<sub style="font-size:10px;pointer-events:none;">0</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
B<sub style="font-size:10px;pointer-events:none;">0</sub>      </div>
    </div>
  </div>
  <div style="display:inline-block;padding:0 6px 0 0;">
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
C<sub style="font-size:10px;pointer-events:none;">1</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
D<sub style="font-size:10px;pointer-events:none;">1</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
E<sub style="font-size:10px;pointer-events:none;">1</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
F<sub style="font-size:10px;pointer-events:none;">1</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
G<sub style="font-size:10px;pointer-events:none;">1</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
A<sub style="font-size:10px;pointer-events:none;">1</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
B<sub style="font-size:10px;pointer-events:none;">1</sub>      </div>
    </div>
  </div>
  <div style="display:inline-block;padding:0 6px 0 0;">
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
C<sub style="font-size:10px;pointer-events:none;">2</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
D<sub style="font-size:10px;pointer-events:none;">2</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
E<sub style="font-size:10px;pointer-events:none;">2</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
F<sub style="font-size:10px;pointer-events:none;">2</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
G<sub style="font-size:10px;pointer-events:none;">2</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
A<sub style="font-size:10px;pointer-events:none;">2</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
B<sub style="font-size:10px;pointer-events:none;">2</sub>      </div>
    </div>
  </div>
  <div style="display:inline-block;padding:0 6px 0 0;">
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
C<sub style="font-size:10px;pointer-events:none;">3</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
D<sub style="font-size:10px;pointer-events:none;">3</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
E<sub style="font-size:10px;pointer-events:none;">3</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
F<sub style="font-size:10px;pointer-events:none;">3</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
G<sub style="font-size:10px;pointer-events:none;">3</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
A<sub style="font-size:10px;pointer-events:none;">3</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
B<sub style="font-size:10px;pointer-events:none;">3</sub>      </div>
    </div>
  </div>
  <div style="display:inline-block;padding:0 6px 0 0;">
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
C<sub style="font-size:10px;pointer-events:none;">4</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
D<sub style="font-size:10px;pointer-events:none;">4</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
E<sub style="font-size:10px;pointer-events:none;">4</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
F<sub style="font-size:10px;pointer-events:none;">4</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
G<sub style="font-size:10px;pointer-events:none;">4</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
A<sub style="font-size:10px;pointer-events:none;">4</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
B<sub style="font-size:10px;pointer-events:none;">4</sub>      </div>
    </div>
  </div>
  <div style="display:inline-block;padding:0 6px 0 0;">
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
C<sub style="font-size:10px;pointer-events:none;">5</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
D<sub style="font-size:10px;pointer-events:none;">5</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
E<sub style="font-size:10px;pointer-events:none;">5</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
F<sub style="font-size:10px;pointer-events:none;">5</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
G<sub style="font-size:10px;pointer-events:none;">5</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
A<sub style="font-size:10px;pointer-events:none;">5</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
B<sub style="font-size:10px;pointer-events:none;">5</sub>      </div>
    </div>
  </div>
  <div style="display:inline-block;padding:0 6px 0 0;">
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
C<sub style="font-size:10px;pointer-events:none;">6</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
D<sub style="font-size:10px;pointer-events:none;">6</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
E<sub style="font-size:10px;pointer-events:none;">6</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
F<sub style="font-size:10px;pointer-events:none;">6</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
G<sub style="font-size:10px;pointer-events:none;">6</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
A<sub style="font-size:10px;pointer-events:none;">6</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
B<sub style="font-size:10px;pointer-events:none;">6</sub>      </div>
    </div>
  </div>
  <div style="display:inline-block;padding:0 6px 0 0;">
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
C<sub style="font-size:10px;pointer-events:none;">7</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
D<sub style="font-size:10px;pointer-events:none;">7</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
E<sub style="font-size:10px;pointer-events:none;">7</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
F<sub style="font-size:10px;pointer-events:none;">7</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
G<sub style="font-size:10px;pointer-events:none;">7</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
A<sub style="font-size:10px;pointer-events:none;">7</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
B<sub style="font-size:10px;pointer-events:none;">7</sub>      </div>
    </div>
  </div>
</div>
<script>if (window.htmx) htmx.process(document.body)</script>



```python
show(Div(Keyboard(), style="overflow-x:scroll;overflow-y:hidden;width:660px;height:110px;white-space:nowrap;margin:10px;"))
```


<div style="overflow-x:scroll;overflow-y:hidden;width:660px;height:110px;white-space:nowrap;margin:10px;">
  <div style="width:auto;padding:0;margin:0;">
    <div style="display:inline-block;padding:0 6px 0 0;">
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
C<sub style="font-size:10px;pointer-events:none;">0</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
D<sub style="font-size:10px;pointer-events:none;">0</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
E<sub style="font-size:10px;pointer-events:none;">0</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
F<sub style="font-size:10px;pointer-events:none;">0</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
G<sub style="font-size:10px;pointer-events:none;">0</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
A<sub style="font-size:10px;pointer-events:none;">0</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
B<sub style="font-size:10px;pointer-events:none;">0</sub>        </div>
      </div>
    </div>
    <div style="display:inline-block;padding:0 6px 0 0;">
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
C<sub style="font-size:10px;pointer-events:none;">1</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
D<sub style="font-size:10px;pointer-events:none;">1</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
E<sub style="font-size:10px;pointer-events:none;">1</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
F<sub style="font-size:10px;pointer-events:none;">1</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
G<sub style="font-size:10px;pointer-events:none;">1</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
A<sub style="font-size:10px;pointer-events:none;">1</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
B<sub style="font-size:10px;pointer-events:none;">1</sub>        </div>
      </div>
    </div>
    <div style="display:inline-block;padding:0 6px 0 0;">
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
C<sub style="font-size:10px;pointer-events:none;">2</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
D<sub style="font-size:10px;pointer-events:none;">2</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
E<sub style="font-size:10px;pointer-events:none;">2</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
F<sub style="font-size:10px;pointer-events:none;">2</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
G<sub style="font-size:10px;pointer-events:none;">2</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
A<sub style="font-size:10px;pointer-events:none;">2</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
B<sub style="font-size:10px;pointer-events:none;">2</sub>        </div>
      </div>
    </div>
    <div style="display:inline-block;padding:0 6px 0 0;">
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
C<sub style="font-size:10px;pointer-events:none;">3</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
D<sub style="font-size:10px;pointer-events:none;">3</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
E<sub style="font-size:10px;pointer-events:none;">3</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
F<sub style="font-size:10px;pointer-events:none;">3</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
G<sub style="font-size:10px;pointer-events:none;">3</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
A<sub style="font-size:10px;pointer-events:none;">3</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
B<sub style="font-size:10px;pointer-events:none;">3</sub>        </div>
      </div>
    </div>
    <div style="display:inline-block;padding:0 6px 0 0;">
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
C<sub style="font-size:10px;pointer-events:none;">4</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
D<sub style="font-size:10px;pointer-events:none;">4</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
E<sub style="font-size:10px;pointer-events:none;">4</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
F<sub style="font-size:10px;pointer-events:none;">4</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
G<sub style="font-size:10px;pointer-events:none;">4</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
A<sub style="font-size:10px;pointer-events:none;">4</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
B<sub style="font-size:10px;pointer-events:none;">4</sub>        </div>
      </div>
    </div>
    <div style="display:inline-block;padding:0 6px 0 0;">
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
C<sub style="font-size:10px;pointer-events:none;">5</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
D<sub style="font-size:10px;pointer-events:none;">5</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
E<sub style="font-size:10px;pointer-events:none;">5</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
F<sub style="font-size:10px;pointer-events:none;">5</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
G<sub style="font-size:10px;pointer-events:none;">5</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
A<sub style="font-size:10px;pointer-events:none;">5</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
B<sub style="font-size:10px;pointer-events:none;">5</sub>        </div>
      </div>
    </div>
    <div style="display:inline-block;padding:0 6px 0 0;">
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
C<sub style="font-size:10px;pointer-events:none;">6</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
D<sub style="font-size:10px;pointer-events:none;">6</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
E<sub style="font-size:10px;pointer-events:none;">6</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
F<sub style="font-size:10px;pointer-events:none;">6</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
G<sub style="font-size:10px;pointer-events:none;">6</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
A<sub style="font-size:10px;pointer-events:none;">6</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
B<sub style="font-size:10px;pointer-events:none;">6</sub>        </div>
      </div>
    </div>
    <div style="display:inline-block;padding:0 6px 0 0;">
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
C<sub style="font-size:10px;pointer-events:none;">7</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
D<sub style="font-size:10px;pointer-events:none;">7</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
E<sub style="font-size:10px;pointer-events:none;">7</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
F<sub style="font-size:10px;pointer-events:none;">7</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
G<sub style="font-size:10px;pointer-events:none;">7</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
A<sub style="font-size:10px;pointer-events:none;">7</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
B<sub style="font-size:10px;pointer-events:none;">7</sub>        </div>
      </div>
    </div>
  </div>
</div>
<script>if (window.htmx) htmx.process(document.body)</script>



```python
show(Div(Keyboard(), style="overflow-x:scroll;overflow-y:hidden;width:100%;height:110px;white-space:nowrap;margin:10px;"))
```


<div style="overflow-x:scroll;overflow-y:hidden;width:100%;height:110px;white-space:nowrap;margin:10px;">
  <div style="width:auto;padding:0;margin:0;">
    <div style="display:inline-block;padding:0 6px 0 0;">
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
C<sub style="font-size:10px;pointer-events:none;">0</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
D<sub style="font-size:10px;pointer-events:none;">0</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
E<sub style="font-size:10px;pointer-events:none;">0</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
F<sub style="font-size:10px;pointer-events:none;">0</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
G<sub style="font-size:10px;pointer-events:none;">0</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
A<sub style="font-size:10px;pointer-events:none;">0</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
B<sub style="font-size:10px;pointer-events:none;">0</sub>        </div>
      </div>
    </div>
    <div style="display:inline-block;padding:0 6px 0 0;">
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
C<sub style="font-size:10px;pointer-events:none;">1</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
D<sub style="font-size:10px;pointer-events:none;">1</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
E<sub style="font-size:10px;pointer-events:none;">1</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
F<sub style="font-size:10px;pointer-events:none;">1</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
G<sub style="font-size:10px;pointer-events:none;">1</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
A<sub style="font-size:10px;pointer-events:none;">1</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
B<sub style="font-size:10px;pointer-events:none;">1</sub>        </div>
      </div>
    </div>
    <div style="display:inline-block;padding:0 6px 0 0;">
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
C<sub style="font-size:10px;pointer-events:none;">2</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
D<sub style="font-size:10px;pointer-events:none;">2</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
E<sub style="font-size:10px;pointer-events:none;">2</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
F<sub style="font-size:10px;pointer-events:none;">2</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
G<sub style="font-size:10px;pointer-events:none;">2</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
A<sub style="font-size:10px;pointer-events:none;">2</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
B<sub style="font-size:10px;pointer-events:none;">2</sub>        </div>
      </div>
    </div>
    <div style="display:inline-block;padding:0 6px 0 0;">
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
C<sub style="font-size:10px;pointer-events:none;">3</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
D<sub style="font-size:10px;pointer-events:none;">3</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
E<sub style="font-size:10px;pointer-events:none;">3</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
F<sub style="font-size:10px;pointer-events:none;">3</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
G<sub style="font-size:10px;pointer-events:none;">3</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
A<sub style="font-size:10px;pointer-events:none;">3</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
B<sub style="font-size:10px;pointer-events:none;">3</sub>        </div>
      </div>
    </div>
    <div style="display:inline-block;padding:0 6px 0 0;">
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
C<sub style="font-size:10px;pointer-events:none;">4</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
D<sub style="font-size:10px;pointer-events:none;">4</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
E<sub style="font-size:10px;pointer-events:none;">4</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
F<sub style="font-size:10px;pointer-events:none;">4</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
G<sub style="font-size:10px;pointer-events:none;">4</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
A<sub style="font-size:10px;pointer-events:none;">4</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
B<sub style="font-size:10px;pointer-events:none;">4</sub>        </div>
      </div>
    </div>
    <div style="display:inline-block;padding:0 6px 0 0;">
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
C<sub style="font-size:10px;pointer-events:none;">5</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
D<sub style="font-size:10px;pointer-events:none;">5</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
E<sub style="font-size:10px;pointer-events:none;">5</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
F<sub style="font-size:10px;pointer-events:none;">5</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
G<sub style="font-size:10px;pointer-events:none;">5</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
A<sub style="font-size:10px;pointer-events:none;">5</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
B<sub style="font-size:10px;pointer-events:none;">5</sub>        </div>
      </div>
    </div>
    <div style="display:inline-block;padding:0 6px 0 0;">
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
C<sub style="font-size:10px;pointer-events:none;">6</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
D<sub style="font-size:10px;pointer-events:none;">6</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
E<sub style="font-size:10px;pointer-events:none;">6</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
F<sub style="font-size:10px;pointer-events:none;">6</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
G<sub style="font-size:10px;pointer-events:none;">6</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
A<sub style="font-size:10px;pointer-events:none;">6</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
B<sub style="font-size:10px;pointer-events:none;">6</sub>        </div>
      </div>
    </div>
    <div style="display:inline-block;padding:0 6px 0 0;">
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
C<sub style="font-size:10px;pointer-events:none;">7</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
D<sub style="font-size:10px;pointer-events:none;">7</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
E<sub style="font-size:10px;pointer-events:none;">7</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
F<sub style="font-size:10px;pointer-events:none;">7</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
G<sub style="font-size:10px;pointer-events:none;">7</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
A<sub style="font-size:10px;pointer-events:none;">7</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
B<sub style="font-size:10px;pointer-events:none;">7</sub>        </div>
      </div>
    </div>
  </div>
</div>
<script>if (window.htmx) htmx.process(document.body)</script>


## Original Code

Below is the original code from [MDN Web Audio API Simple Synth](https://developer.mozilla.org/en-US/docs/Web/API/Web_Audio_API/Simple_synth). It's here for me to refer to as I build this out.


```python
<div class="container">
  <div class="keyboard"></div>
</div>

<div class="settingsBar">
  <div class="left">
    <span>Volume: </span>
    <input
      type="range"
      min="0.0"
      max="1.0"
      step="0.01"
      value="0.5"
      list="volumes"
      name="volume" />
    <datalist id="volumes">
      <option value="0.0" label="Mute"></option>
      <option value="1.0" label="100%"></option>
    </datalist>
  </div>
</div>

  <div class="right">
    <span>Current waveform: </span>
    <select name="waveform">
      <option value="sine">Sine</option>
      <option value="square" selected>Square</option>
      <option value="sawtooth">Sawtooth</option>
      <option value="triangle">Triangle</option>
      <option value="custom">Custom</option>
    </select>
  </div>
</div>

```


```python
.container {
  overflow-x: scroll;
  overflow-y: hidden;
  width: 660px;
  height: 110px;
  white-space: nowrap;
  margin: 10px;
}

.keyboard {
  width: auto;
  padding: 0;
  margin: 0;
}

.key {
  cursor: pointer;
  font:
    16px "Open Sans",
    "Lucida Grande",
    "Arial",
    sans-serif;
  border: 1px solid black;
  border-radius: 5px;
  width: 20px;
  height: 80px;
  text-align: center;
  box-shadow: 2px 2px darkgray;
  display: inline-block;
  position: relative;
  margin-right: 3px;
  user-select: none;
  -moz-user-select: none;
  -webkit-user-select: none;
  -ms-user-select: none;
}

.key div {
  position: absolute;
  bottom: 0;
  text-align: center;
  width: 100%;
  pointer-events: none;
}

.key div sub {
  font-size: 10px;
  pointer-events: none;
}

.key:hover {
  background-color: #eef;
}

.key:active,
.active {
  background-color: #000;
  color: #fff;
}

.octave {
  display: inline-block;
  padding: 0 6px 0 0;
}

.settingsBar {
  padding-top: 8px;
  font:
    14px "Open Sans",
    "Lucida Grande",
    "Arial",
    sans-serif;
  position: relative;
  vertical-align: middle;
  width: 100%;
  height: 30px;
}

.left {
  width: 50%;
  position: absolute;
  left: 0;
  display: table-cell;
  vertical-align: middle;
}

.left span,
.left input {
  vertical-align: middle;
}

.right {
  width: 50%;
  position: absolute;
  right: 0;
  display: table-cell;
  vertical-align: middle;
}

.right span {
  vertical-align: middle;
}

.right input {
  vertical-align: baseline;
}

```


```python
const audioContext = new AudioContext();
const oscList = [];
let mainGainNode = null;

const keyboard = document.querySelector(".keyboard");
const wavePicker = document.querySelector("select[name='waveform']");
const volumeControl = document.querySelector("input[name='volume']");

let noteFreq = null;
let customWaveform = null;
let sineTerms = null;
let cosineTerms = null;

function createNoteTable() {
  const noteFreq = [];
  for (let i=0; i< 9; i++) {
    noteFreq[i] = [];
  }

  noteFreq[0]["A"] = 27.500000000000000;
  noteFreq[0]["A#"] = 29.135235094880619;
  noteFreq[0]["B"] = 30.867706328507756;

  noteFreq[1]["C"] = 32.703195662574829;
  noteFreq[1]["C#"] = 34.647828872109012;
  noteFreq[1]["D"] = 36.708095989675945;
  noteFreq[1]["D#"] = 38.890872965260113;
  noteFreq[1]["E"] = 41.203444614108741;
  noteFreq[1]["F"] = 43.653528929125485;
  noteFreq[1]["F#"] = 46.249302838954299;
  noteFreq[1]["G"] = 48.999429497718661;
  noteFreq[1]["G#"] = 51.913087197493142;
  noteFreq[1]["A"] = 55.000000000000000;
  noteFreq[1]["A#"] = 58.270470189761239;
  noteFreq[1]["B"] = 61.735412657015513;
  // …

noteFreq[2]["C"] = 65.406391325149658;
noteFreq[2]["C#"] = 69.295657744218024;
noteFreq[2]["D"] = 73.41619197935189;
noteFreq[2]["D#"] = 77.781745930520227;
noteFreq[2]["E"] = 82.406889228217482;
noteFreq[2]["F"] = 87.307057858250971;
noteFreq[2]["F#"] = 92.498605677908599;
noteFreq[2]["G"] = 97.998858995437323;
noteFreq[2]["G#"] = 103.826174394986284;
noteFreq[2]["A"] = 110.0;
noteFreq[2]["A#"] = 116.540940379522479;
noteFreq[2]["B"] = 123.470825314031027;

noteFreq[3]["C"] = 130.812782650299317;
noteFreq[3]["C#"] = 138.591315488436048;
noteFreq[3]["D"] = 146.83238395870378;
noteFreq[3]["D#"] = 155.563491861040455;
noteFreq[3]["E"] = 164.813778456434964;
noteFreq[3]["F"] = 174.614115716501942;
noteFreq[3]["F#"] = 184.997211355817199;
noteFreq[3]["G"] = 195.997717990874647;
noteFreq[3]["G#"] = 207.652348789972569;
noteFreq[3]["A"] = 220.0;
noteFreq[3]["A#"] = 233.081880759044958;
noteFreq[3]["B"] = 246.941650628062055;

noteFreq[4]["C"] = 261.625565300598634;
noteFreq[4]["C#"] = 277.182630976872096;
noteFreq[4]["D"] = 293.66476791740756;
noteFreq[4]["D#"] = 311.12698372208091;
noteFreq[4]["E"] = 329.627556912869929;
noteFreq[4]["F"] = 349.228231433003884;
noteFreq[4]["F#"] = 369.994422711634398;
noteFreq[4]["G"] = 391.995435981749294;
noteFreq[4]["G#"] = 415.304697579945138;
noteFreq[4]["A"] = 440.0;
noteFreq[4]["A#"] = 466.163761518089916;
noteFreq[4]["B"] = 493.883301256124111;

noteFreq[5]["C"] = 523.251130601197269;
noteFreq[5]["C#"] = 554.365261953744192;
noteFreq[5]["D"] = 587.32953583481512;
noteFreq[5]["D#"] = 622.253967444161821;
noteFreq[5]["E"] = 659.255113825739859;
noteFreq[5]["F"] = 698.456462866007768;
noteFreq[5]["F#"] = 739.988845423268797;
noteFreq[5]["G"] = 783.990871963498588;
noteFreq[5]["G#"] = 830.609395159890277;
noteFreq[5]["A"] = 880.0;
noteFreq[5]["A#"] = 932.327523036179832;
noteFreq[5]["B"] = 987.766602512248223;

noteFreq[6]["C"] = 1046.502261202394538;
noteFreq[6]["C#"] = 1108.730523907488384;
noteFreq[6]["D"] = 1174.659071669630241;
noteFreq[6]["D#"] = 1244.507934888323642;
noteFreq[6]["E"] = 1318.510227651479718;
noteFreq[6]["F"] = 1396.912925732015537;
noteFreq[6]["F#"] = 1479.977690846537595;
noteFreq[6]["G"] = 1567.981743926997176;
noteFreq[6]["G#"] = 1661.218790319780554;
noteFreq[6]["A"] = 1760.0;
noteFreq[6]["A#"] = 1864.655046072359665;
noteFreq[6]["B"] = 1975.533205024496447;

  noteFreq[7]["C"] = 2093.004522404789077;
  noteFreq[7]["C#"] = 2217.461047814976769;
  noteFreq[7]["D"] = 2349.318143339260482;
  noteFreq[7]["D#"] = 2489.015869776647285;
  noteFreq[7]["E"] = 2637.020455302959437;
  noteFreq[7]["F"] = 2793.825851464031075;
  noteFreq[7]["F#"] = 2959.955381693075191;
  noteFreq[7]["G"] = 3135.963487853994352;
  noteFreq[7]["G#"] = 3322.437580639561108;
  noteFreq[7]["A"] = 3520.000000000000000;
  noteFreq[7]["A#"] = 3729.310092144719331;
  noteFreq[7]["B"] = 3951.066410048992894;

  noteFreq[8]["C"] = 4186.009044809578154;
  return noteFreq;
}

if (!Object.entries) {
  Object.entries = function entries(O) {
    return reduce(
      keys(O),
      (e, k) =>
        concat(
          e,
          typeof k === "string" && isEnumerable(O, k) ? [[k, O[k]]] : [],
        ),
      [],
    );
  };
}

function setup() {
  noteFreq = createNoteTable();

  volumeControl.addEventListener("change", changeVolume, false);

  mainGainNode = audioContext.createGain();
  mainGainNode.connect(audioContext.destination);
  mainGainNode.gain.value = volumeControl.value;

  // Create the keys; skip any that are sharp or flat; for
  // our purposes we don't need them. Each octave is inserted
  // into a <div> of class "octave".

  noteFreq.forEach((keys, idx) => {
    const keyList = Object.entries(keys);
    const octaveElem = document.createElement("div");
    octaveElem.className = "octave";

    keyList.forEach((key) => {
      if (key[0].length === 1) {
        octaveElem.appendChild(createKey(key[0], idx, key[1]));
      }
    });

    keyboard.appendChild(octaveElem);
  });

  document
    .querySelector("div[data-note='B'][data-octave='5']")
    .scrollIntoView(false);

  sineTerms = new Float32Array([0, 0, 1, 0, 1]);
  cosineTerms = new Float32Array(sineTerms.length);
  customWaveform = audioContext.createPeriodicWave(cosineTerms, sineTerms);

  for (let i = 0; i < 9; i++) {
    oscList[i] = {};
  }
}

setup();

function createKey(note, octave, freq) {
  const keyElement = document.createElement("div");
  const labelElement = document.createElement("div");

  keyElement.className = "key";
  keyElement.dataset["octave"] = octave;
  keyElement.dataset["note"] = note;
  keyElement.dataset["frequency"] = freq;
  labelElement.appendChild(document.createTextNode(note));
  labelElement.appendChild(document.createElement("sub")).textContent = octave;
  keyElement.appendChild(labelElement);

  keyElement.addEventListener("mousedown", notePressed, false);
  keyElement.addEventListener("mouseup", noteReleased, false);
  keyElement.addEventListener("mouseover", notePressed, false);
  keyElement.addEventListener("mouseleave", noteReleased, false);

  return keyElement;
}

function playTone(freq) {
  const osc = audioContext.createOscillator();
  osc.connect(mainGainNode);

  const type = wavePicker.options[wavePicker.selectedIndex].value;

  if (type === "custom") {
    osc.setPeriodicWave(customWaveform);
  } else {
    osc.type = type;
  }

  osc.frequency.value = freq;
  osc.start();

  return osc;
}

function notePressed(event) {
  if (event.buttons & 1) {
    const dataset = event.target.dataset;

    if (!dataset["pressed"] && dataset["octave"]) {
      const octave = Number(dataset["octave"]);
      oscList[octave][dataset["note"]] = playTone(dataset["frequency"]);
      dataset["pressed"] = "yes";
    }
  }
}

function noteReleased(event) {
  const dataset = event.target.dataset;

  if (dataset && dataset["pressed"]) {
    const octave = Number(dataset["octave"]);

    if (oscList[octave] && oscList[octave][dataset["note"]]) {
      oscList[octave][dataset["note"]].stop();
      delete oscList[octave][dataset["note"]];
      delete dataset["pressed"];
    }
  }
}

function changeVolume(event) {
  mainGainNode.gain.value = volumeControl.value;
}

const synthKeys = document.querySelectorAll(".key");
const keyCodes = [
  "Space",
  "ShiftLeft", "KeyZ", "KeyX", "KeyC", "KeyV", "KeyB", "KeyN", "KeyM", "Comma", "Period", "Slash", "ShiftRight",
  "KeyA", "KeyS", "KeyD", "KeyF", "KeyG", "KeyH", "KeyJ", "KeyK", "KeyL", "Semicolon", "Quote", "Enter",
  "Tab", "KeyQ", "KeyW", "KeyE", "KeyR", "KeyT", "KeyY", "KeyU", "KeyI", "KeyO", "KeyP", "BracketLeft", "BracketRight",
  "Digit1", "Digit2", "Digit3", "Digit4", "Digit5", "Digit6", "Digit7", "Digit8", "Digit9", "Digit0", "Minus", "Equal", "Backspace",
  "Escape",
];
function keyNote(event) {
  const elKey = synthKeys[keyCodes.indexOf(event.code)];
  if (elKey) {
    if (event.type === "keydown") {
      elKey.tabIndex = -1;
      elKey.focus();
      elKey.classList.add("active");
      notePressed({ buttons: 1, target: elKey });
    } else {
      elKey.classList.remove("active");
      noteReleased({ buttons: 1, target: elKey });
    }
    event.preventDefault();
  }
}
addEventListener("keydown", keyNote);
addEventListener("keyup", keyNote);
```
