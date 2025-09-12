# FastHTML Piano, Part 2


```python
from fastcore.all import *
from fasthtml.common import *
from fasthtml.jupyter import *
from IPython.display import display, Javascript
```

## Piano Keys

In Part 1 we defined piano keys like this:


```python
def Key(note, octave): return Div(
    Div(note, Sub(octave, style='font-size:10px;pointer-events:none;'), style='position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;'),
    onmouseover="event.target.style.backgroundColor = '#eef';",
    onmouseout="event.target.style.backgroundColor = '#fff';",
    style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;')
```


```python
show(Key('C','5'), Key('D','5'))
```


<div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
  <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
C<sub style="font-size:10px;pointer-events:none;">5</sub>  </div>
</div>
<div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:16px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
  <div style="position:absolute;bottom:0;text-align:center;width:100%;pointer-events:none;">
D<sub style="font-size:10px;pointer-events:none;">5</sub>  </div>
</div>
<script>if (window.htmx) htmx.process(document.body)</script>


We'll be adding frequencies to the keys.

## Frequencies of Notes

Even though our piano has just the white keys, we need all the notes to calculate the frequencies:


```python
notes_in_octave = L(['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'])
notes_in_octave
```




    (#12) ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']



There are 12 notes per octave. I define `npo` for later use:


```python
npo = len(notes_in_octave)
npo
```




    12



We use a4's frequency to calculate the other note frequencies:


```python
a4_freq = 440.0
```


```python
notes_in_octave.index('A')
```




    9



And a4's index:


```python
a4i = notes_in_octave.index('A') + (4 * npo)
a4i
```




    57



Instead of a hardcoded table in JS with all the note frequencies for all octaves, we define this Python function:


```python
def freq(note, octave):
    ni = notes_in_octave.index(note) + (octave * npo)
    semitones_from_a4 = ni - a4i
    freq = a4_freq * (2 ** (semitones_from_a4 / npo))
    return round(freq, ndigits=1)
freq('A', 4)
```




    440.0




```python
freq('C', 3)
```




    130.8



## Keys With Frequencies

I like the idea of showing the frequencies on the piano keys.


```python
def Key(note, octave): 
    f = freq(note,octave)
    return Div(
        Div(Div(f, style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;"), note, Sub(octave, style='font-size:10px;pointer-events:none;'), style='position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;'),
        onmouseover="event.target.style.backgroundColor = '#eef';",
        onmouseout="event.target.style.backgroundColor = '#fff';",
        style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;')
```


```python
show(Key('A', 4))
```


<div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
  <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
    <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">440.0</div>
A<sub style="font-size:10px;pointer-events:none;">4</sub>  </div>
</div>
<script>if (window.htmx) htmx.process(document.body)</script>


## Octaves


```python
def Octave(n):
    return Div(*notes_in_octave.map(partial(Key,octave=n)),
        style='display:inline-block;padding:0 6px 0 0;')
show(Octave(4))
```


<div style="display:inline-block;padding:0 6px 0 0;">
  <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
    <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
      <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">261.6</div>
C<sub style="font-size:10px;pointer-events:none;">4</sub>    </div>
  </div>
  <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
    <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
      <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">277.2</div>
C#<sub style="font-size:10px;pointer-events:none;">4</sub>    </div>
  </div>
  <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
    <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
      <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">293.7</div>
D<sub style="font-size:10px;pointer-events:none;">4</sub>    </div>
  </div>
  <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
    <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
      <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">311.1</div>
D#<sub style="font-size:10px;pointer-events:none;">4</sub>    </div>
  </div>
  <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
    <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
      <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">329.6</div>
E<sub style="font-size:10px;pointer-events:none;">4</sub>    </div>
  </div>
  <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
    <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
      <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">349.2</div>
F<sub style="font-size:10px;pointer-events:none;">4</sub>    </div>
  </div>
  <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
    <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
      <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">370.0</div>
F#<sub style="font-size:10px;pointer-events:none;">4</sub>    </div>
  </div>
  <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
    <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
      <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">392.0</div>
G<sub style="font-size:10px;pointer-events:none;">4</sub>    </div>
  </div>
  <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
    <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
      <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">415.3</div>
G#<sub style="font-size:10px;pointer-events:none;">4</sub>    </div>
  </div>
  <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
    <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
      <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">440.0</div>
A<sub style="font-size:10px;pointer-events:none;">4</sub>    </div>
  </div>
  <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
    <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
      <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">466.2</div>
A#<sub style="font-size:10px;pointer-events:none;">4</sub>    </div>
  </div>
  <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
    <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
      <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">493.9</div>
B<sub style="font-size:10px;pointer-events:none;">4</sub>    </div>
  </div>
</div>
<script>if (window.htmx) htmx.process(document.body)</script>


## Keyboard


```python
def Keyboard(): return Div(*L(range(8)).map(Octave), style="width:auto;padding:0;margin:0;")
show(Keyboard())
```


<div style="width:auto;padding:0;margin:0;">
  <div style="display:inline-block;padding:0 6px 0 0;">
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">16.4</div>
C<sub style="font-size:10px;pointer-events:none;">0</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">17.3</div>
C#<sub style="font-size:10px;pointer-events:none;">0</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">18.4</div>
D<sub style="font-size:10px;pointer-events:none;">0</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">19.4</div>
D#<sub style="font-size:10px;pointer-events:none;">0</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">20.6</div>
E<sub style="font-size:10px;pointer-events:none;">0</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">21.8</div>
F<sub style="font-size:10px;pointer-events:none;">0</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">23.1</div>
F#<sub style="font-size:10px;pointer-events:none;">0</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">24.5</div>
G<sub style="font-size:10px;pointer-events:none;">0</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">26.0</div>
G#<sub style="font-size:10px;pointer-events:none;">0</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">27.5</div>
A<sub style="font-size:10px;pointer-events:none;">0</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">29.1</div>
A#<sub style="font-size:10px;pointer-events:none;">0</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">30.9</div>
B<sub style="font-size:10px;pointer-events:none;">0</sub>      </div>
    </div>
  </div>
  <div style="display:inline-block;padding:0 6px 0 0;">
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">32.7</div>
C<sub style="font-size:10px;pointer-events:none;">1</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">34.6</div>
C#<sub style="font-size:10px;pointer-events:none;">1</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">36.7</div>
D<sub style="font-size:10px;pointer-events:none;">1</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">38.9</div>
D#<sub style="font-size:10px;pointer-events:none;">1</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">41.2</div>
E<sub style="font-size:10px;pointer-events:none;">1</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">43.7</div>
F<sub style="font-size:10px;pointer-events:none;">1</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">46.2</div>
F#<sub style="font-size:10px;pointer-events:none;">1</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">49.0</div>
G<sub style="font-size:10px;pointer-events:none;">1</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">51.9</div>
G#<sub style="font-size:10px;pointer-events:none;">1</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">55.0</div>
A<sub style="font-size:10px;pointer-events:none;">1</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">58.3</div>
A#<sub style="font-size:10px;pointer-events:none;">1</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">61.7</div>
B<sub style="font-size:10px;pointer-events:none;">1</sub>      </div>
    </div>
  </div>
  <div style="display:inline-block;padding:0 6px 0 0;">
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">65.4</div>
C<sub style="font-size:10px;pointer-events:none;">2</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">69.3</div>
C#<sub style="font-size:10px;pointer-events:none;">2</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">73.4</div>
D<sub style="font-size:10px;pointer-events:none;">2</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">77.8</div>
D#<sub style="font-size:10px;pointer-events:none;">2</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">82.4</div>
E<sub style="font-size:10px;pointer-events:none;">2</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">87.3</div>
F<sub style="font-size:10px;pointer-events:none;">2</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">92.5</div>
F#<sub style="font-size:10px;pointer-events:none;">2</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">98.0</div>
G<sub style="font-size:10px;pointer-events:none;">2</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">103.8</div>
G#<sub style="font-size:10px;pointer-events:none;">2</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">110.0</div>
A<sub style="font-size:10px;pointer-events:none;">2</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">116.5</div>
A#<sub style="font-size:10px;pointer-events:none;">2</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">123.5</div>
B<sub style="font-size:10px;pointer-events:none;">2</sub>      </div>
    </div>
  </div>
  <div style="display:inline-block;padding:0 6px 0 0;">
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">130.8</div>
C<sub style="font-size:10px;pointer-events:none;">3</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">138.6</div>
C#<sub style="font-size:10px;pointer-events:none;">3</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">146.8</div>
D<sub style="font-size:10px;pointer-events:none;">3</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">155.6</div>
D#<sub style="font-size:10px;pointer-events:none;">3</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">164.8</div>
E<sub style="font-size:10px;pointer-events:none;">3</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">174.6</div>
F<sub style="font-size:10px;pointer-events:none;">3</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">185.0</div>
F#<sub style="font-size:10px;pointer-events:none;">3</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">196.0</div>
G<sub style="font-size:10px;pointer-events:none;">3</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">207.7</div>
G#<sub style="font-size:10px;pointer-events:none;">3</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">220.0</div>
A<sub style="font-size:10px;pointer-events:none;">3</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">233.1</div>
A#<sub style="font-size:10px;pointer-events:none;">3</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">246.9</div>
B<sub style="font-size:10px;pointer-events:none;">3</sub>      </div>
    </div>
  </div>
  <div style="display:inline-block;padding:0 6px 0 0;">
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">261.6</div>
C<sub style="font-size:10px;pointer-events:none;">4</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">277.2</div>
C#<sub style="font-size:10px;pointer-events:none;">4</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">293.7</div>
D<sub style="font-size:10px;pointer-events:none;">4</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">311.1</div>
D#<sub style="font-size:10px;pointer-events:none;">4</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">329.6</div>
E<sub style="font-size:10px;pointer-events:none;">4</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">349.2</div>
F<sub style="font-size:10px;pointer-events:none;">4</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">370.0</div>
F#<sub style="font-size:10px;pointer-events:none;">4</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">392.0</div>
G<sub style="font-size:10px;pointer-events:none;">4</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">415.3</div>
G#<sub style="font-size:10px;pointer-events:none;">4</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">440.0</div>
A<sub style="font-size:10px;pointer-events:none;">4</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">466.2</div>
A#<sub style="font-size:10px;pointer-events:none;">4</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">493.9</div>
B<sub style="font-size:10px;pointer-events:none;">4</sub>      </div>
    </div>
  </div>
  <div style="display:inline-block;padding:0 6px 0 0;">
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">523.3</div>
C<sub style="font-size:10px;pointer-events:none;">5</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">554.4</div>
C#<sub style="font-size:10px;pointer-events:none;">5</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">587.3</div>
D<sub style="font-size:10px;pointer-events:none;">5</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">622.3</div>
D#<sub style="font-size:10px;pointer-events:none;">5</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">659.3</div>
E<sub style="font-size:10px;pointer-events:none;">5</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">698.5</div>
F<sub style="font-size:10px;pointer-events:none;">5</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">740.0</div>
F#<sub style="font-size:10px;pointer-events:none;">5</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">784.0</div>
G<sub style="font-size:10px;pointer-events:none;">5</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">830.6</div>
G#<sub style="font-size:10px;pointer-events:none;">5</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">880.0</div>
A<sub style="font-size:10px;pointer-events:none;">5</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">932.3</div>
A#<sub style="font-size:10px;pointer-events:none;">5</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">987.8</div>
B<sub style="font-size:10px;pointer-events:none;">5</sub>      </div>
    </div>
  </div>
  <div style="display:inline-block;padding:0 6px 0 0;">
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">1046.5</div>
C<sub style="font-size:10px;pointer-events:none;">6</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">1108.7</div>
C#<sub style="font-size:10px;pointer-events:none;">6</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">1174.7</div>
D<sub style="font-size:10px;pointer-events:none;">6</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">1244.5</div>
D#<sub style="font-size:10px;pointer-events:none;">6</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">1318.5</div>
E<sub style="font-size:10px;pointer-events:none;">6</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">1396.9</div>
F<sub style="font-size:10px;pointer-events:none;">6</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">1480.0</div>
F#<sub style="font-size:10px;pointer-events:none;">6</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">1568.0</div>
G<sub style="font-size:10px;pointer-events:none;">6</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">1661.2</div>
G#<sub style="font-size:10px;pointer-events:none;">6</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">1760.0</div>
A<sub style="font-size:10px;pointer-events:none;">6</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">1864.7</div>
A#<sub style="font-size:10px;pointer-events:none;">6</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">1975.5</div>
B<sub style="font-size:10px;pointer-events:none;">6</sub>      </div>
    </div>
  </div>
  <div style="display:inline-block;padding:0 6px 0 0;">
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">2093.0</div>
C<sub style="font-size:10px;pointer-events:none;">7</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">2217.5</div>
C#<sub style="font-size:10px;pointer-events:none;">7</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">2349.3</div>
D<sub style="font-size:10px;pointer-events:none;">7</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">2489.0</div>
D#<sub style="font-size:10px;pointer-events:none;">7</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">2637.0</div>
E<sub style="font-size:10px;pointer-events:none;">7</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">2793.8</div>
F<sub style="font-size:10px;pointer-events:none;">7</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">2960.0</div>
F#<sub style="font-size:10px;pointer-events:none;">7</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">3136.0</div>
G<sub style="font-size:10px;pointer-events:none;">7</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">3322.4</div>
G#<sub style="font-size:10px;pointer-events:none;">7</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">3520.0</div>
A<sub style="font-size:10px;pointer-events:none;">7</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">3729.3</div>
A#<sub style="font-size:10px;pointer-events:none;">7</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">3951.1</div>
B<sub style="font-size:10px;pointer-events:none;">7</sub>      </div>
    </div>
  </div>
</div>
<script>if (window.htmx) htmx.process(document.body)</script>


The MDN article had this:


```python
show(Div(Keyboard(), style="overflow-x:scroll;overflow-y:hidden;width:100%;height:110px;white-space:nowrap;margin:10px;"))
```


<div style="overflow-x:scroll;overflow-y:hidden;width:100%;height:110px;white-space:nowrap;margin:10px;">
  <div style="width:auto;padding:0;margin:0;">
    <div style="display:inline-block;padding:0 6px 0 0;">
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
          <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">16.4</div>
C<sub style="font-size:10px;pointer-events:none;">0</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
          <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">17.3</div>
C#<sub style="font-size:10px;pointer-events:none;">0</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
          <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">18.4</div>
D<sub style="font-size:10px;pointer-events:none;">0</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
          <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">19.4</div>
D#<sub style="font-size:10px;pointer-events:none;">0</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
          <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">20.6</div>
E<sub style="font-size:10px;pointer-events:none;">0</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
          <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">21.8</div>
F<sub style="font-size:10px;pointer-events:none;">0</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
          <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">23.1</div>
F#<sub style="font-size:10px;pointer-events:none;">0</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
          <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">24.5</div>
G<sub style="font-size:10px;pointer-events:none;">0</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
          <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">26.0</div>
G#<sub style="font-size:10px;pointer-events:none;">0</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
          <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">27.5</div>
A<sub style="font-size:10px;pointer-events:none;">0</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
          <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">29.1</div>
A#<sub style="font-size:10px;pointer-events:none;">0</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
          <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">30.9</div>
B<sub style="font-size:10px;pointer-events:none;">0</sub>        </div>
      </div>
    </div>
    <div style="display:inline-block;padding:0 6px 0 0;">
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
          <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">32.7</div>
C<sub style="font-size:10px;pointer-events:none;">1</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
          <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">34.6</div>
C#<sub style="font-size:10px;pointer-events:none;">1</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
          <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">36.7</div>
D<sub style="font-size:10px;pointer-events:none;">1</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
          <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">38.9</div>
D#<sub style="font-size:10px;pointer-events:none;">1</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
          <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">41.2</div>
E<sub style="font-size:10px;pointer-events:none;">1</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
          <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">43.7</div>
F<sub style="font-size:10px;pointer-events:none;">1</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
          <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">46.2</div>
F#<sub style="font-size:10px;pointer-events:none;">1</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
          <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">49.0</div>
G<sub style="font-size:10px;pointer-events:none;">1</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
          <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">51.9</div>
G#<sub style="font-size:10px;pointer-events:none;">1</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
          <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">55.0</div>
A<sub style="font-size:10px;pointer-events:none;">1</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
          <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">58.3</div>
A#<sub style="font-size:10px;pointer-events:none;">1</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
          <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">61.7</div>
B<sub style="font-size:10px;pointer-events:none;">1</sub>        </div>
      </div>
    </div>
    <div style="display:inline-block;padding:0 6px 0 0;">
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
          <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">65.4</div>
C<sub style="font-size:10px;pointer-events:none;">2</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
          <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">69.3</div>
C#<sub style="font-size:10px;pointer-events:none;">2</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
          <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">73.4</div>
D<sub style="font-size:10px;pointer-events:none;">2</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
          <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">77.8</div>
D#<sub style="font-size:10px;pointer-events:none;">2</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
          <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">82.4</div>
E<sub style="font-size:10px;pointer-events:none;">2</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
          <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">87.3</div>
F<sub style="font-size:10px;pointer-events:none;">2</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
          <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">92.5</div>
F#<sub style="font-size:10px;pointer-events:none;">2</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
          <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">98.0</div>
G<sub style="font-size:10px;pointer-events:none;">2</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
          <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">103.8</div>
G#<sub style="font-size:10px;pointer-events:none;">2</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
          <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">110.0</div>
A<sub style="font-size:10px;pointer-events:none;">2</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
          <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">116.5</div>
A#<sub style="font-size:10px;pointer-events:none;">2</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
          <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">123.5</div>
B<sub style="font-size:10px;pointer-events:none;">2</sub>        </div>
      </div>
    </div>
    <div style="display:inline-block;padding:0 6px 0 0;">
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
          <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">130.8</div>
C<sub style="font-size:10px;pointer-events:none;">3</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
          <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">138.6</div>
C#<sub style="font-size:10px;pointer-events:none;">3</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
          <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">146.8</div>
D<sub style="font-size:10px;pointer-events:none;">3</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
          <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">155.6</div>
D#<sub style="font-size:10px;pointer-events:none;">3</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
          <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">164.8</div>
E<sub style="font-size:10px;pointer-events:none;">3</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
          <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">174.6</div>
F<sub style="font-size:10px;pointer-events:none;">3</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
          <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">185.0</div>
F#<sub style="font-size:10px;pointer-events:none;">3</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
          <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">196.0</div>
G<sub style="font-size:10px;pointer-events:none;">3</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
          <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">207.7</div>
G#<sub style="font-size:10px;pointer-events:none;">3</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
          <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">220.0</div>
A<sub style="font-size:10px;pointer-events:none;">3</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
          <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">233.1</div>
A#<sub style="font-size:10px;pointer-events:none;">3</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
          <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">246.9</div>
B<sub style="font-size:10px;pointer-events:none;">3</sub>        </div>
      </div>
    </div>
    <div style="display:inline-block;padding:0 6px 0 0;">
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
          <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">261.6</div>
C<sub style="font-size:10px;pointer-events:none;">4</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
          <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">277.2</div>
C#<sub style="font-size:10px;pointer-events:none;">4</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
          <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">293.7</div>
D<sub style="font-size:10px;pointer-events:none;">4</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
          <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">311.1</div>
D#<sub style="font-size:10px;pointer-events:none;">4</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
          <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">329.6</div>
E<sub style="font-size:10px;pointer-events:none;">4</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
          <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">349.2</div>
F<sub style="font-size:10px;pointer-events:none;">4</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
          <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">370.0</div>
F#<sub style="font-size:10px;pointer-events:none;">4</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
          <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">392.0</div>
G<sub style="font-size:10px;pointer-events:none;">4</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
          <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">415.3</div>
G#<sub style="font-size:10px;pointer-events:none;">4</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
          <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">440.0</div>
A<sub style="font-size:10px;pointer-events:none;">4</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
          <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">466.2</div>
A#<sub style="font-size:10px;pointer-events:none;">4</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
          <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">493.9</div>
B<sub style="font-size:10px;pointer-events:none;">4</sub>        </div>
      </div>
    </div>
    <div style="display:inline-block;padding:0 6px 0 0;">
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
          <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">523.3</div>
C<sub style="font-size:10px;pointer-events:none;">5</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
          <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">554.4</div>
C#<sub style="font-size:10px;pointer-events:none;">5</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
          <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">587.3</div>
D<sub style="font-size:10px;pointer-events:none;">5</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
          <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">622.3</div>
D#<sub style="font-size:10px;pointer-events:none;">5</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
          <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">659.3</div>
E<sub style="font-size:10px;pointer-events:none;">5</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
          <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">698.5</div>
F<sub style="font-size:10px;pointer-events:none;">5</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
          <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">740.0</div>
F#<sub style="font-size:10px;pointer-events:none;">5</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
          <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">784.0</div>
G<sub style="font-size:10px;pointer-events:none;">5</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
          <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">830.6</div>
G#<sub style="font-size:10px;pointer-events:none;">5</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
          <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">880.0</div>
A<sub style="font-size:10px;pointer-events:none;">5</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
          <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">932.3</div>
A#<sub style="font-size:10px;pointer-events:none;">5</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
          <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">987.8</div>
B<sub style="font-size:10px;pointer-events:none;">5</sub>        </div>
      </div>
    </div>
    <div style="display:inline-block;padding:0 6px 0 0;">
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
          <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">1046.5</div>
C<sub style="font-size:10px;pointer-events:none;">6</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
          <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">1108.7</div>
C#<sub style="font-size:10px;pointer-events:none;">6</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
          <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">1174.7</div>
D<sub style="font-size:10px;pointer-events:none;">6</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
          <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">1244.5</div>
D#<sub style="font-size:10px;pointer-events:none;">6</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
          <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">1318.5</div>
E<sub style="font-size:10px;pointer-events:none;">6</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
          <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">1396.9</div>
F<sub style="font-size:10px;pointer-events:none;">6</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
          <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">1480.0</div>
F#<sub style="font-size:10px;pointer-events:none;">6</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
          <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">1568.0</div>
G<sub style="font-size:10px;pointer-events:none;">6</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
          <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">1661.2</div>
G#<sub style="font-size:10px;pointer-events:none;">6</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
          <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">1760.0</div>
A<sub style="font-size:10px;pointer-events:none;">6</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
          <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">1864.7</div>
A#<sub style="font-size:10px;pointer-events:none;">6</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
          <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">1975.5</div>
B<sub style="font-size:10px;pointer-events:none;">6</sub>        </div>
      </div>
    </div>
    <div style="display:inline-block;padding:0 6px 0 0;">
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
          <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">2093.0</div>
C<sub style="font-size:10px;pointer-events:none;">7</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
          <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">2217.5</div>
C#<sub style="font-size:10px;pointer-events:none;">7</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
          <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">2349.3</div>
D<sub style="font-size:10px;pointer-events:none;">7</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
          <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">2489.0</div>
D#<sub style="font-size:10px;pointer-events:none;">7</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
          <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">2637.0</div>
E<sub style="font-size:10px;pointer-events:none;">7</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
          <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">2793.8</div>
F<sub style="font-size:10px;pointer-events:none;">7</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
          <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">2960.0</div>
F#<sub style="font-size:10px;pointer-events:none;">7</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
          <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">3136.0</div>
G<sub style="font-size:10px;pointer-events:none;">7</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
          <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">3322.4</div>
G#<sub style="font-size:10px;pointer-events:none;">7</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
          <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">3520.0</div>
A<sub style="font-size:10px;pointer-events:none;">7</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
          <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">3729.3</div>
A#<sub style="font-size:10px;pointer-events:none;">7</sub>        </div>
      </div>
      <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
        <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
          <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">3951.1</div>
B<sub style="font-size:10px;pointer-events:none;">7</sub>        </div>
      </div>
    </div>
  </div>
</div>
<script>if (window.htmx) htmx.process(document.body)</script>


But I think wrapping the keys without a horizontal scrollbar is nicer.

## Settings Bar

For now, I convert the original to a FastTag here:


```python
def SettingsBar():
    return Div(
        Div(
            Span("Volume: ",style="vertical-align:middle;"),
            Input(type="range",min=0,max=1.0,step=0.01,value=0.5,list="volumes",name="volume",style="vertical-align:middle;"),
            Datalist(
                Option(value=0.0,label="Mute"),
                Option(value=1.0,label="100%"),
                id="volumes",),
            style="width:50%;position:absolute;left:0;display:table-cell;vertical-align:middle;"),
        Div(
            Span("Waveform: ", style="vertical-align:middle;"),
            Select(
                Option("Sine", value="sine"),
                Option("Square", value="square"),
                Option("Sawtooth", value="sawtooth"),
                Option("Triangle", value="triangle"),
                Option("Custom", value="custom"),
                name="waveform",
                style="vertical-align:middle;"),
            style="width:50%;position:absolute;right:0;display:table-cell;vertical-align:middle;"),
        style='padding-top:8px;font:14px "Open Sans","Lucida Grande","Arial",sans-serif;position:relative;vertical-align:middle;width:100%;height:80px;')
```


```python
show(SettingsBar())
```


<div style='padding-top:8px;font:14px "Open Sans","Lucida Grande","Arial",sans-serif;position:relative;vertical-align:middle;width:100%;height:80px;'>
  <div style="width:50%;position:absolute;left:0;display:table-cell;vertical-align:middle;">
<span style="vertical-align:middle;">Volume: </span>    <input type="range" max="1.0" step="0.01" value="0.5" list="volumes" name="volume" style="vertical-align:middle;">
<datalist id="volumes"><option label="Mute"></option><option value="1.0" label="100%"></option></datalist>  </div>
  <div style="width:50%;position:absolute;right:0;display:table-cell;vertical-align:middle;">
<span style="vertical-align:middle;">Waveform: </span><select name="waveform" style="vertical-align:middle;"><option value="sine">Sine</option><option value="square">Square</option><option value="sawtooth">Sawtooth</option><option value="triangle">Triangle</option><option value="custom">Custom</option></select>  </div>
</div>
<script>if (window.htmx) htmx.process(document.body)</script>


## Creating Oscillators in JS


```javascript
%%javascript
window.audioContext = new AudioContext();
window.gainNode = audioContext.createGain();
window.gainNode.gain.value = 0.5;

function playTone(freq) {
    const osc = window.audioContext.createOscillator();
    osc.type = 'sine';
    osc.frequency.value = freq;
    osc.connect(window.gainNode);
    window.gainNode.connect(window.audioContext.destination);
    osc.start();
}
playTone(400)
```


    <IPython.core.display.Javascript object>


## Creating Oscillators in Python

The MDN example creates 1 oscillator per note. I'm just playing around here and may change this later: instead of doing it in JS, I define a Python function to generate the Web Audio API JS code to do this:


```python
def mk_osc(freq): 
    return f"""if (!window.audioContext) {{
      window.audioContext = new AudioContext();
      window.gainNode = audioContext.createGain();
      window.gainNode.gain.value = 0.5;
    }}
    const osc=window.audioContext.createOscillator();
    osc.type='sine';
    osc.frequency.value={freq};
    osc.connect(window.gainNode);
    window.gainNode.connect(window.audioContext.destination);
    console.log('Starting freq {freq}');
    osc.start()"""
```


```python
mk_osc(440.0)
```




    "if (!window.audioContext) {\n      window.audioContext = new AudioContext();\n      window.gainNode = audioContext.createGain();\n      window.gainNode.gain.value = 0.5;\n    }\n    const osc=window.audioContext.createOscillator();\n    osc.type='sine';\n    osc.frequency.value=440.0;\n    osc.connect(window.gainNode);\n    window.gainNode.connect(window.audioContext.destination);\n    console.log('Starting freq 440.0');\n    osc.start()"



Running this cell plays the 440Hz tone:


```python
display(Javascript(mk_osc(440.0)))
```


    <IPython.core.display.Javascript object>



```python
def mk_stoposc(freq): return f"console.log('Stopping freq {freq}');osc.stop();";
```


```python
mk_stoposc(440.0)
```




    "console.log('Stopping freq 440.0');osc.stop();"




```python
display(Javascript(mk_stoposc(440.0)))
```


    <IPython.core.display.Javascript object>


This is tricker than I thought. mk_stoposc needs to get osc from window, I think. We probably want to create a list of oscillators for all note frequencies and waveforms, and attach it to window.

## Playing Frequencies


```python
def Key(note, octave): 
    f = freq(note,octave)
    return Div(
        Div(Div(f, style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;"), note, Sub(octave, style='font-size:10px;pointer-events:none;'), style='position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;'),
        onmouseover="event.target.style.backgroundColor = '#eef';",
        onmouseout="event.target.style.backgroundColor = '#fff';",
        onmousedown=mk_osc(f),
        onmouseup=mk_stoposc(f),
        style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;')
```


```python
show(Key('A', 4))
```


<div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" onmousedown="if (!window.audioContext) {
      window.audioContext = new AudioContext();
      window.gainNode = audioContext.createGain();
      window.gainNode.gain.value = 0.5;
    }
    const osc=window.audioContext.createOscillator();
    osc.type='sine';
    osc.frequency.value=440.0;
    osc.connect(window.gainNode);
    window.gainNode.connect(window.audioContext.destination);
    console.log('Starting freq 440.0');
    osc.start()" onmouseup="console.log('Stopping freq 440.0');osc.stop();" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:22px;height:80px;margin-right:3px;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
  <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
    <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">440.0</div>
A<sub style="font-size:10px;pointer-events:none;">4</sub>  </div>
</div>
<script>if (window.htmx) htmx.process(document.body)</script>


The tone plays, but `mk_stoposc` doesn't actually work here. To be continued...
