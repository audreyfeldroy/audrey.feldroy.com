# FastHTML Piano, Part 3


```python
from fastcore.all import *
from fasthtml.common import *
```


```python
settings_js = """window.audioContext = new AudioContext();
window.gainNode = audioContext.createGain();
window.gainNode.gain.value = 0.5;
window.activeOscillators = new Map();
"""
```

## Piano Settings Bar

A volume slider to change the gainNode's value:


```python
def VolumeInput(v=0.5):
    return Div(
            Span("Volume: ",style="vertical-align:middle;"),
            Input(type="range",min=0,max=1.0,step=0.01,value=v,name="volume",
                onchange=f"window.gainNode.gain.value=event.target.value;console.log('Volume changed to ', event.target.value);"))
show(VolumeInput())
```


<div>
<span style="vertical-align:middle;">Volume: </span>  <input type="range" max="1.0" step="0.01" value="0.5" name="volume" onchange="window.gainNode.gain.value=event.target.value;console.log('Volume changed to ', event.target.value);">
</div>




```python
show(VolumeInput(0.8))
```


<div>
<span style="vertical-align:middle;">Volume: </span>  <input type="range" max="1.0" step="0.01" value="0.8" name="volume" onchange="window.gainNode.gain.value=event.target.value;console.log('Volume changed to ', event.target.value);">
</div>



A dropdown to choose a waveform type:


```python
def WaveformInput():
    return Div(
            Script("function updateWaveform(type) {window.waveformType = type;console.log('Waveform set to', type)}"),
            Span("Waveform: "),
            Select(
                Option("Sine", value="sine"),
                Option("Square", value="square"),
                Option("Sawtooth", value="sawtooth"),
                Option("Triangle", value="triangle"),
                Option("Custom", value="custom"),
                onchange="updateWaveform(event.target.value)",
                name="waveform"))
show(WaveformInput())
```


<div>
<script>function updateWaveform(type) {window.waveformType = type;console.log('Waveform set to', type)}</script><span>Waveform: </span><select onchange="updateWaveform(event.target.value)" name="waveform"><option value="sine">Sine</option><option value="square">Square</option><option value="sawtooth">Sawtooth</option><option value="triangle">Triangle</option><option value="custom">Custom</option></select></div>



Note: I defined a JS function in `Script` just to see if I can do that and call it in `onchange`. But it's simple enough that inline would have been fine.

The `SettingsBar` combines both inputs:


```python
def SettingsBar():
    return Div(
        Script(settings_js),
        VolumeInput(),
        WaveformInput())
show(SettingsBar())
```


<div>
<script>window.audioContext = new AudioContext();
window.gainNode = audioContext.createGain();
window.gainNode.gain.value = 0.5;
window.activeOscillators = new Map();
</script>  <div>
<span style="vertical-align:middle;">Volume: </span>    <input type="range" max="1.0" step="0.01" value="0.5" name="volume" onchange="window.gainNode.gain.value=event.target.value;console.log('Volume changed to ', event.target.value);">
  </div>
  <div>
<script>function updateWaveform(type) {window.waveformType = type;console.log('Waveform set to', type)}</script><span>Waveform: </span><select onchange="updateWaveform(event.target.value)" name="waveform"><option value="sine">Sine</option><option value="square">Square</option><option value="sawtooth">Sawtooth</option><option value="triangle">Triangle</option><option value="custom">Custom</option></select>  </div>
</div>



## Notes and Frequencies

Let's modify the Key function to add click handling, and create the corresponding JavaScript to start and stop the oscillator when clicking. Here's how:


```python
notes_in_octave = L(['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'])
notes_in_octave
```




    (#12) ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']




```python
npo = len(notes_in_octave)
a4_freq = 440.0
a4i = notes_in_octave.index('A') + (4 * npo)
```


```python
def freq(note, octave):
    ni = notes_in_octave.index(note) + (octave * npo)
    semitones_from_a4 = ni - a4i
    freq = a4_freq * (2 ** (semitones_from_a4 / npo))
    return round(freq, ndigits=1)
```


```python
key_js = """
function playTone(freq) {
    const osc = window.audioContext.createOscillator();
    osc.type = window.waveformType || 'sine';
    osc.frequency.value = freq;
    osc.connect(window.gainNode);
    window.gainNode.connect(window.audioContext.destination);
    osc.start();
    window.activeOscillators.set(freq, osc);
}

function stopTone(freq) {
    const osc = window.activeOscillators.get(freq);
    if (osc) {
        osc.stop();
        osc.disconnect();
        window.activeOscillators.delete(freq);
    }
}"""
```


```python
def Key(note, octave): 
    f = freq(note,octave)
    is_black = '#' in note
    style = ('cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;'
            f'border:1px solid black;border-radius:5px;width:{20 if not is_black else 16}px;'
            f'height:{80 if not is_black else 50}px;'
            f'background-color:{" black" if is_black else "white"};color:{" white" if is_black else "black"};'
            f'box-shadow:2px 2px darkgray;display:inline-block;position:relative;'
            f'{"top:-30px;" if is_black else ""}'
            'user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;')
    return Div(
        Script(key_js),
        Div(Div(f, style=f'font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;{"bottom:24px;" if is_black else "bottom:50px;"}'), 
            note.replace('#','♯'), Sub(octave, style='font-size:10px;pointer-events:none;'), 
            style='position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;'),
        onmouseover="event.target.style.backgroundColor = '#eef';",
        onmouseout=f"event.target.style.backgroundColor = '#{'000' if is_black else 'fff'}';",
        onmousedown=f"playTone({f})",
        onmouseup=f"stopTone({f})",
        onmouseleave=f"stopTone({f})",
        style=style)
```


```python
def Octave(n):
    return Div(*notes_in_octave.map(partial(Key,octave=n)),
        style='display:inline-block;padding:0 6px 0 0;')
```


```python
show(Octave(4))
```


<div style="display:inline-block;padding:0 6px 0 0;">
  <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" onmousedown="playTone(261.6)" onmouseup="stopTone(261.6)" onmouseleave="stopTone(261.6)" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;background-color:white;color:black;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
<script>
function playTone(freq) {
    const osc = window.audioContext.createOscillator();
    osc.type = window.waveformType || 'sine';
    osc.frequency.value = freq;
    osc.connect(window.gainNode);
    window.gainNode.connect(window.audioContext.destination);
    osc.start();
    window.activeOscillators.set(freq, osc);
}

function stopTone(freq) {
    const osc = window.activeOscillators.get(freq);
    if (osc) {
        osc.stop();
        osc.disconnect();
        window.activeOscillators.delete(freq);
    }
}</script>    <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
      <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">261.6</div>
C<sub style="font-size:10px;pointer-events:none;">4</sub>    </div>
  </div>
  <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#000';" onmousedown="playTone(277.2)" onmouseup="stopTone(277.2)" onmouseleave="stopTone(277.2)" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:16px;height:50px;background-color: black;color: white;box-shadow:2px 2px darkgray;display:inline-block;position:relative;top:-30px;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
<script>
function playTone(freq) {
    const osc = window.audioContext.createOscillator();
    osc.type = window.waveformType || 'sine';
    osc.frequency.value = freq;
    osc.connect(window.gainNode);
    window.gainNode.connect(window.audioContext.destination);
    osc.start();
    window.activeOscillators.set(freq, osc);
}

function stopTone(freq) {
    const osc = window.activeOscillators.get(freq);
    if (osc) {
        osc.stop();
        osc.disconnect();
        window.activeOscillators.delete(freq);
    }
}</script>    <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
      <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:24px;">277.2</div>
C♯<sub style="font-size:10px;pointer-events:none;">4</sub>    </div>
  </div>
  <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" onmousedown="playTone(293.7)" onmouseup="stopTone(293.7)" onmouseleave="stopTone(293.7)" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;background-color:white;color:black;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
<script>
function playTone(freq) {
    const osc = window.audioContext.createOscillator();
    osc.type = window.waveformType || 'sine';
    osc.frequency.value = freq;
    osc.connect(window.gainNode);
    window.gainNode.connect(window.audioContext.destination);
    osc.start();
    window.activeOscillators.set(freq, osc);
}

function stopTone(freq) {
    const osc = window.activeOscillators.get(freq);
    if (osc) {
        osc.stop();
        osc.disconnect();
        window.activeOscillators.delete(freq);
    }
}</script>    <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
      <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">293.7</div>
D<sub style="font-size:10px;pointer-events:none;">4</sub>    </div>
  </div>
  <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#000';" onmousedown="playTone(311.1)" onmouseup="stopTone(311.1)" onmouseleave="stopTone(311.1)" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:16px;height:50px;background-color: black;color: white;box-shadow:2px 2px darkgray;display:inline-block;position:relative;top:-30px;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
<script>
function playTone(freq) {
    const osc = window.audioContext.createOscillator();
    osc.type = window.waveformType || 'sine';
    osc.frequency.value = freq;
    osc.connect(window.gainNode);
    window.gainNode.connect(window.audioContext.destination);
    osc.start();
    window.activeOscillators.set(freq, osc);
}

function stopTone(freq) {
    const osc = window.activeOscillators.get(freq);
    if (osc) {
        osc.stop();
        osc.disconnect();
        window.activeOscillators.delete(freq);
    }
}</script>    <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
      <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:24px;">311.1</div>
D♯<sub style="font-size:10px;pointer-events:none;">4</sub>    </div>
  </div>
  <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" onmousedown="playTone(329.6)" onmouseup="stopTone(329.6)" onmouseleave="stopTone(329.6)" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;background-color:white;color:black;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
<script>
function playTone(freq) {
    const osc = window.audioContext.createOscillator();
    osc.type = window.waveformType || 'sine';
    osc.frequency.value = freq;
    osc.connect(window.gainNode);
    window.gainNode.connect(window.audioContext.destination);
    osc.start();
    window.activeOscillators.set(freq, osc);
}

function stopTone(freq) {
    const osc = window.activeOscillators.get(freq);
    if (osc) {
        osc.stop();
        osc.disconnect();
        window.activeOscillators.delete(freq);
    }
}</script>    <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
      <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">329.6</div>
E<sub style="font-size:10px;pointer-events:none;">4</sub>    </div>
  </div>
  <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" onmousedown="playTone(349.2)" onmouseup="stopTone(349.2)" onmouseleave="stopTone(349.2)" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;background-color:white;color:black;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
<script>
function playTone(freq) {
    const osc = window.audioContext.createOscillator();
    osc.type = window.waveformType || 'sine';
    osc.frequency.value = freq;
    osc.connect(window.gainNode);
    window.gainNode.connect(window.audioContext.destination);
    osc.start();
    window.activeOscillators.set(freq, osc);
}

function stopTone(freq) {
    const osc = window.activeOscillators.get(freq);
    if (osc) {
        osc.stop();
        osc.disconnect();
        window.activeOscillators.delete(freq);
    }
}</script>    <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
      <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">349.2</div>
F<sub style="font-size:10px;pointer-events:none;">4</sub>    </div>
  </div>
  <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#000';" onmousedown="playTone(370.0)" onmouseup="stopTone(370.0)" onmouseleave="stopTone(370.0)" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:16px;height:50px;background-color: black;color: white;box-shadow:2px 2px darkgray;display:inline-block;position:relative;top:-30px;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
<script>
function playTone(freq) {
    const osc = window.audioContext.createOscillator();
    osc.type = window.waveformType || 'sine';
    osc.frequency.value = freq;
    osc.connect(window.gainNode);
    window.gainNode.connect(window.audioContext.destination);
    osc.start();
    window.activeOscillators.set(freq, osc);
}

function stopTone(freq) {
    const osc = window.activeOscillators.get(freq);
    if (osc) {
        osc.stop();
        osc.disconnect();
        window.activeOscillators.delete(freq);
    }
}</script>    <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
      <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:24px;">370.0</div>
F♯<sub style="font-size:10px;pointer-events:none;">4</sub>    </div>
  </div>
  <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" onmousedown="playTone(392.0)" onmouseup="stopTone(392.0)" onmouseleave="stopTone(392.0)" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;background-color:white;color:black;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
<script>
function playTone(freq) {
    const osc = window.audioContext.createOscillator();
    osc.type = window.waveformType || 'sine';
    osc.frequency.value = freq;
    osc.connect(window.gainNode);
    window.gainNode.connect(window.audioContext.destination);
    osc.start();
    window.activeOscillators.set(freq, osc);
}

function stopTone(freq) {
    const osc = window.activeOscillators.get(freq);
    if (osc) {
        osc.stop();
        osc.disconnect();
        window.activeOscillators.delete(freq);
    }
}</script>    <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
      <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">392.0</div>
G<sub style="font-size:10px;pointer-events:none;">4</sub>    </div>
  </div>
  <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#000';" onmousedown="playTone(415.3)" onmouseup="stopTone(415.3)" onmouseleave="stopTone(415.3)" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:16px;height:50px;background-color: black;color: white;box-shadow:2px 2px darkgray;display:inline-block;position:relative;top:-30px;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
<script>
function playTone(freq) {
    const osc = window.audioContext.createOscillator();
    osc.type = window.waveformType || 'sine';
    osc.frequency.value = freq;
    osc.connect(window.gainNode);
    window.gainNode.connect(window.audioContext.destination);
    osc.start();
    window.activeOscillators.set(freq, osc);
}

function stopTone(freq) {
    const osc = window.activeOscillators.get(freq);
    if (osc) {
        osc.stop();
        osc.disconnect();
        window.activeOscillators.delete(freq);
    }
}</script>    <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
      <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:24px;">415.3</div>
G♯<sub style="font-size:10px;pointer-events:none;">4</sub>    </div>
  </div>
  <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" onmousedown="playTone(440.0)" onmouseup="stopTone(440.0)" onmouseleave="stopTone(440.0)" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;background-color:white;color:black;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
<script>
function playTone(freq) {
    const osc = window.audioContext.createOscillator();
    osc.type = window.waveformType || 'sine';
    osc.frequency.value = freq;
    osc.connect(window.gainNode);
    window.gainNode.connect(window.audioContext.destination);
    osc.start();
    window.activeOscillators.set(freq, osc);
}

function stopTone(freq) {
    const osc = window.activeOscillators.get(freq);
    if (osc) {
        osc.stop();
        osc.disconnect();
        window.activeOscillators.delete(freq);
    }
}</script>    <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
      <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">440.0</div>
A<sub style="font-size:10px;pointer-events:none;">4</sub>    </div>
  </div>
  <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#000';" onmousedown="playTone(466.2)" onmouseup="stopTone(466.2)" onmouseleave="stopTone(466.2)" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:16px;height:50px;background-color: black;color: white;box-shadow:2px 2px darkgray;display:inline-block;position:relative;top:-30px;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
<script>
function playTone(freq) {
    const osc = window.audioContext.createOscillator();
    osc.type = window.waveformType || 'sine';
    osc.frequency.value = freq;
    osc.connect(window.gainNode);
    window.gainNode.connect(window.audioContext.destination);
    osc.start();
    window.activeOscillators.set(freq, osc);
}

function stopTone(freq) {
    const osc = window.activeOscillators.get(freq);
    if (osc) {
        osc.stop();
        osc.disconnect();
        window.activeOscillators.delete(freq);
    }
}</script>    <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
      <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:24px;">466.2</div>
A♯<sub style="font-size:10px;pointer-events:none;">4</sub>    </div>
  </div>
  <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" onmousedown="playTone(493.9)" onmouseup="stopTone(493.9)" onmouseleave="stopTone(493.9)" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;background-color:white;color:black;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
<script>
function playTone(freq) {
    const osc = window.audioContext.createOscillator();
    osc.type = window.waveformType || 'sine';
    osc.frequency.value = freq;
    osc.connect(window.gainNode);
    window.gainNode.connect(window.audioContext.destination);
    osc.start();
    window.activeOscillators.set(freq, osc);
}

function stopTone(freq) {
    const osc = window.activeOscillators.get(freq);
    if (osc) {
        osc.stop();
        osc.disconnect();
        window.activeOscillators.delete(freq);
    }
}</script>    <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
      <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">493.9</div>
B<sub style="font-size:10px;pointer-events:none;">4</sub>    </div>
  </div>
</div>




```python
def Keyboard(): return Div(*L(range(8)).map(Octave), style="width:auto;padding:0;margin:0;")
show(Keyboard())
```


<div style="width:auto;padding:0;margin:0;">
  <div style="display:inline-block;padding:0 6px 0 0;">
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" onmousedown="playTone(16.4)" onmouseup="stopTone(16.4)" onmouseleave="stopTone(16.4)" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;background-color:white;color:black;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
<script>
function playTone(freq) {
    const osc = window.audioContext.createOscillator();
    osc.type = window.waveformType || 'sine';
    osc.frequency.value = freq;
    osc.connect(window.gainNode);
    window.gainNode.connect(window.audioContext.destination);
    osc.start();
    window.activeOscillators.set(freq, osc);
}

function stopTone(freq) {
    const osc = window.activeOscillators.get(freq);
    if (osc) {
        osc.stop();
        osc.disconnect();
        window.activeOscillators.delete(freq);
    }
}</script>      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">16.4</div>
C<sub style="font-size:10px;pointer-events:none;">0</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#000';" onmousedown="playTone(17.3)" onmouseup="stopTone(17.3)" onmouseleave="stopTone(17.3)" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:16px;height:50px;background-color: black;color: white;box-shadow:2px 2px darkgray;display:inline-block;position:relative;top:-30px;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
<script>
function playTone(freq) {
    const osc = window.audioContext.createOscillator();
    osc.type = window.waveformType || 'sine';
    osc.frequency.value = freq;
    osc.connect(window.gainNode);
    window.gainNode.connect(window.audioContext.destination);
    osc.start();
    window.activeOscillators.set(freq, osc);
}

function stopTone(freq) {
    const osc = window.activeOscillators.get(freq);
    if (osc) {
        osc.stop();
        osc.disconnect();
        window.activeOscillators.delete(freq);
    }
}</script>      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:24px;">17.3</div>
C♯<sub style="font-size:10px;pointer-events:none;">0</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" onmousedown="playTone(18.4)" onmouseup="stopTone(18.4)" onmouseleave="stopTone(18.4)" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;background-color:white;color:black;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
<script>
function playTone(freq) {
    const osc = window.audioContext.createOscillator();
    osc.type = window.waveformType || 'sine';
    osc.frequency.value = freq;
    osc.connect(window.gainNode);
    window.gainNode.connect(window.audioContext.destination);
    osc.start();
    window.activeOscillators.set(freq, osc);
}

function stopTone(freq) {
    const osc = window.activeOscillators.get(freq);
    if (osc) {
        osc.stop();
        osc.disconnect();
        window.activeOscillators.delete(freq);
    }
}</script>      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">18.4</div>
D<sub style="font-size:10px;pointer-events:none;">0</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#000';" onmousedown="playTone(19.4)" onmouseup="stopTone(19.4)" onmouseleave="stopTone(19.4)" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:16px;height:50px;background-color: black;color: white;box-shadow:2px 2px darkgray;display:inline-block;position:relative;top:-30px;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
<script>
function playTone(freq) {
    const osc = window.audioContext.createOscillator();
    osc.type = window.waveformType || 'sine';
    osc.frequency.value = freq;
    osc.connect(window.gainNode);
    window.gainNode.connect(window.audioContext.destination);
    osc.start();
    window.activeOscillators.set(freq, osc);
}

function stopTone(freq) {
    const osc = window.activeOscillators.get(freq);
    if (osc) {
        osc.stop();
        osc.disconnect();
        window.activeOscillators.delete(freq);
    }
}</script>      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:24px;">19.4</div>
D♯<sub style="font-size:10px;pointer-events:none;">0</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" onmousedown="playTone(20.6)" onmouseup="stopTone(20.6)" onmouseleave="stopTone(20.6)" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;background-color:white;color:black;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
<script>
function playTone(freq) {
    const osc = window.audioContext.createOscillator();
    osc.type = window.waveformType || 'sine';
    osc.frequency.value = freq;
    osc.connect(window.gainNode);
    window.gainNode.connect(window.audioContext.destination);
    osc.start();
    window.activeOscillators.set(freq, osc);
}

function stopTone(freq) {
    const osc = window.activeOscillators.get(freq);
    if (osc) {
        osc.stop();
        osc.disconnect();
        window.activeOscillators.delete(freq);
    }
}</script>      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">20.6</div>
E<sub style="font-size:10px;pointer-events:none;">0</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" onmousedown="playTone(21.8)" onmouseup="stopTone(21.8)" onmouseleave="stopTone(21.8)" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;background-color:white;color:black;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
<script>
function playTone(freq) {
    const osc = window.audioContext.createOscillator();
    osc.type = window.waveformType || 'sine';
    osc.frequency.value = freq;
    osc.connect(window.gainNode);
    window.gainNode.connect(window.audioContext.destination);
    osc.start();
    window.activeOscillators.set(freq, osc);
}

function stopTone(freq) {
    const osc = window.activeOscillators.get(freq);
    if (osc) {
        osc.stop();
        osc.disconnect();
        window.activeOscillators.delete(freq);
    }
}</script>      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">21.8</div>
F<sub style="font-size:10px;pointer-events:none;">0</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#000';" onmousedown="playTone(23.1)" onmouseup="stopTone(23.1)" onmouseleave="stopTone(23.1)" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:16px;height:50px;background-color: black;color: white;box-shadow:2px 2px darkgray;display:inline-block;position:relative;top:-30px;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
<script>
function playTone(freq) {
    const osc = window.audioContext.createOscillator();
    osc.type = window.waveformType || 'sine';
    osc.frequency.value = freq;
    osc.connect(window.gainNode);
    window.gainNode.connect(window.audioContext.destination);
    osc.start();
    window.activeOscillators.set(freq, osc);
}

function stopTone(freq) {
    const osc = window.activeOscillators.get(freq);
    if (osc) {
        osc.stop();
        osc.disconnect();
        window.activeOscillators.delete(freq);
    }
}</script>      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:24px;">23.1</div>
F♯<sub style="font-size:10px;pointer-events:none;">0</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" onmousedown="playTone(24.5)" onmouseup="stopTone(24.5)" onmouseleave="stopTone(24.5)" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;background-color:white;color:black;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
<script>
function playTone(freq) {
    const osc = window.audioContext.createOscillator();
    osc.type = window.waveformType || 'sine';
    osc.frequency.value = freq;
    osc.connect(window.gainNode);
    window.gainNode.connect(window.audioContext.destination);
    osc.start();
    window.activeOscillators.set(freq, osc);
}

function stopTone(freq) {
    const osc = window.activeOscillators.get(freq);
    if (osc) {
        osc.stop();
        osc.disconnect();
        window.activeOscillators.delete(freq);
    }
}</script>      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">24.5</div>
G<sub style="font-size:10px;pointer-events:none;">0</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#000';" onmousedown="playTone(26.0)" onmouseup="stopTone(26.0)" onmouseleave="stopTone(26.0)" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:16px;height:50px;background-color: black;color: white;box-shadow:2px 2px darkgray;display:inline-block;position:relative;top:-30px;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
<script>
function playTone(freq) {
    const osc = window.audioContext.createOscillator();
    osc.type = window.waveformType || 'sine';
    osc.frequency.value = freq;
    osc.connect(window.gainNode);
    window.gainNode.connect(window.audioContext.destination);
    osc.start();
    window.activeOscillators.set(freq, osc);
}

function stopTone(freq) {
    const osc = window.activeOscillators.get(freq);
    if (osc) {
        osc.stop();
        osc.disconnect();
        window.activeOscillators.delete(freq);
    }
}</script>      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:24px;">26.0</div>
G♯<sub style="font-size:10px;pointer-events:none;">0</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" onmousedown="playTone(27.5)" onmouseup="stopTone(27.5)" onmouseleave="stopTone(27.5)" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;background-color:white;color:black;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
<script>
function playTone(freq) {
    const osc = window.audioContext.createOscillator();
    osc.type = window.waveformType || 'sine';
    osc.frequency.value = freq;
    osc.connect(window.gainNode);
    window.gainNode.connect(window.audioContext.destination);
    osc.start();
    window.activeOscillators.set(freq, osc);
}

function stopTone(freq) {
    const osc = window.activeOscillators.get(freq);
    if (osc) {
        osc.stop();
        osc.disconnect();
        window.activeOscillators.delete(freq);
    }
}</script>      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">27.5</div>
A<sub style="font-size:10px;pointer-events:none;">0</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#000';" onmousedown="playTone(29.1)" onmouseup="stopTone(29.1)" onmouseleave="stopTone(29.1)" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:16px;height:50px;background-color: black;color: white;box-shadow:2px 2px darkgray;display:inline-block;position:relative;top:-30px;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
<script>
function playTone(freq) {
    const osc = window.audioContext.createOscillator();
    osc.type = window.waveformType || 'sine';
    osc.frequency.value = freq;
    osc.connect(window.gainNode);
    window.gainNode.connect(window.audioContext.destination);
    osc.start();
    window.activeOscillators.set(freq, osc);
}

function stopTone(freq) {
    const osc = window.activeOscillators.get(freq);
    if (osc) {
        osc.stop();
        osc.disconnect();
        window.activeOscillators.delete(freq);
    }
}</script>      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:24px;">29.1</div>
A♯<sub style="font-size:10px;pointer-events:none;">0</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" onmousedown="playTone(30.9)" onmouseup="stopTone(30.9)" onmouseleave="stopTone(30.9)" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;background-color:white;color:black;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
<script>
function playTone(freq) {
    const osc = window.audioContext.createOscillator();
    osc.type = window.waveformType || 'sine';
    osc.frequency.value = freq;
    osc.connect(window.gainNode);
    window.gainNode.connect(window.audioContext.destination);
    osc.start();
    window.activeOscillators.set(freq, osc);
}

function stopTone(freq) {
    const osc = window.activeOscillators.get(freq);
    if (osc) {
        osc.stop();
        osc.disconnect();
        window.activeOscillators.delete(freq);
    }
}</script>      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">30.9</div>
B<sub style="font-size:10px;pointer-events:none;">0</sub>      </div>
    </div>
  </div>
  <div style="display:inline-block;padding:0 6px 0 0;">
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" onmousedown="playTone(32.7)" onmouseup="stopTone(32.7)" onmouseleave="stopTone(32.7)" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;background-color:white;color:black;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
<script>
function playTone(freq) {
    const osc = window.audioContext.createOscillator();
    osc.type = window.waveformType || 'sine';
    osc.frequency.value = freq;
    osc.connect(window.gainNode);
    window.gainNode.connect(window.audioContext.destination);
    osc.start();
    window.activeOscillators.set(freq, osc);
}

function stopTone(freq) {
    const osc = window.activeOscillators.get(freq);
    if (osc) {
        osc.stop();
        osc.disconnect();
        window.activeOscillators.delete(freq);
    }
}</script>      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">32.7</div>
C<sub style="font-size:10px;pointer-events:none;">1</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#000';" onmousedown="playTone(34.6)" onmouseup="stopTone(34.6)" onmouseleave="stopTone(34.6)" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:16px;height:50px;background-color: black;color: white;box-shadow:2px 2px darkgray;display:inline-block;position:relative;top:-30px;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
<script>
function playTone(freq) {
    const osc = window.audioContext.createOscillator();
    osc.type = window.waveformType || 'sine';
    osc.frequency.value = freq;
    osc.connect(window.gainNode);
    window.gainNode.connect(window.audioContext.destination);
    osc.start();
    window.activeOscillators.set(freq, osc);
}

function stopTone(freq) {
    const osc = window.activeOscillators.get(freq);
    if (osc) {
        osc.stop();
        osc.disconnect();
        window.activeOscillators.delete(freq);
    }
}</script>      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:24px;">34.6</div>
C♯<sub style="font-size:10px;pointer-events:none;">1</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" onmousedown="playTone(36.7)" onmouseup="stopTone(36.7)" onmouseleave="stopTone(36.7)" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;background-color:white;color:black;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
<script>
function playTone(freq) {
    const osc = window.audioContext.createOscillator();
    osc.type = window.waveformType || 'sine';
    osc.frequency.value = freq;
    osc.connect(window.gainNode);
    window.gainNode.connect(window.audioContext.destination);
    osc.start();
    window.activeOscillators.set(freq, osc);
}

function stopTone(freq) {
    const osc = window.activeOscillators.get(freq);
    if (osc) {
        osc.stop();
        osc.disconnect();
        window.activeOscillators.delete(freq);
    }
}</script>      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">36.7</div>
D<sub style="font-size:10px;pointer-events:none;">1</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#000';" onmousedown="playTone(38.9)" onmouseup="stopTone(38.9)" onmouseleave="stopTone(38.9)" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:16px;height:50px;background-color: black;color: white;box-shadow:2px 2px darkgray;display:inline-block;position:relative;top:-30px;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
<script>
function playTone(freq) {
    const osc = window.audioContext.createOscillator();
    osc.type = window.waveformType || 'sine';
    osc.frequency.value = freq;
    osc.connect(window.gainNode);
    window.gainNode.connect(window.audioContext.destination);
    osc.start();
    window.activeOscillators.set(freq, osc);
}

function stopTone(freq) {
    const osc = window.activeOscillators.get(freq);
    if (osc) {
        osc.stop();
        osc.disconnect();
        window.activeOscillators.delete(freq);
    }
}</script>      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:24px;">38.9</div>
D♯<sub style="font-size:10px;pointer-events:none;">1</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" onmousedown="playTone(41.2)" onmouseup="stopTone(41.2)" onmouseleave="stopTone(41.2)" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;background-color:white;color:black;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
<script>
function playTone(freq) {
    const osc = window.audioContext.createOscillator();
    osc.type = window.waveformType || 'sine';
    osc.frequency.value = freq;
    osc.connect(window.gainNode);
    window.gainNode.connect(window.audioContext.destination);
    osc.start();
    window.activeOscillators.set(freq, osc);
}

function stopTone(freq) {
    const osc = window.activeOscillators.get(freq);
    if (osc) {
        osc.stop();
        osc.disconnect();
        window.activeOscillators.delete(freq);
    }
}</script>      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">41.2</div>
E<sub style="font-size:10px;pointer-events:none;">1</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" onmousedown="playTone(43.7)" onmouseup="stopTone(43.7)" onmouseleave="stopTone(43.7)" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;background-color:white;color:black;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
<script>
function playTone(freq) {
    const osc = window.audioContext.createOscillator();
    osc.type = window.waveformType || 'sine';
    osc.frequency.value = freq;
    osc.connect(window.gainNode);
    window.gainNode.connect(window.audioContext.destination);
    osc.start();
    window.activeOscillators.set(freq, osc);
}

function stopTone(freq) {
    const osc = window.activeOscillators.get(freq);
    if (osc) {
        osc.stop();
        osc.disconnect();
        window.activeOscillators.delete(freq);
    }
}</script>      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">43.7</div>
F<sub style="font-size:10px;pointer-events:none;">1</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#000';" onmousedown="playTone(46.2)" onmouseup="stopTone(46.2)" onmouseleave="stopTone(46.2)" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:16px;height:50px;background-color: black;color: white;box-shadow:2px 2px darkgray;display:inline-block;position:relative;top:-30px;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
<script>
function playTone(freq) {
    const osc = window.audioContext.createOscillator();
    osc.type = window.waveformType || 'sine';
    osc.frequency.value = freq;
    osc.connect(window.gainNode);
    window.gainNode.connect(window.audioContext.destination);
    osc.start();
    window.activeOscillators.set(freq, osc);
}

function stopTone(freq) {
    const osc = window.activeOscillators.get(freq);
    if (osc) {
        osc.stop();
        osc.disconnect();
        window.activeOscillators.delete(freq);
    }
}</script>      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:24px;">46.2</div>
F♯<sub style="font-size:10px;pointer-events:none;">1</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" onmousedown="playTone(49.0)" onmouseup="stopTone(49.0)" onmouseleave="stopTone(49.0)" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;background-color:white;color:black;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
<script>
function playTone(freq) {
    const osc = window.audioContext.createOscillator();
    osc.type = window.waveformType || 'sine';
    osc.frequency.value = freq;
    osc.connect(window.gainNode);
    window.gainNode.connect(window.audioContext.destination);
    osc.start();
    window.activeOscillators.set(freq, osc);
}

function stopTone(freq) {
    const osc = window.activeOscillators.get(freq);
    if (osc) {
        osc.stop();
        osc.disconnect();
        window.activeOscillators.delete(freq);
    }
}</script>      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">49.0</div>
G<sub style="font-size:10px;pointer-events:none;">1</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#000';" onmousedown="playTone(51.9)" onmouseup="stopTone(51.9)" onmouseleave="stopTone(51.9)" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:16px;height:50px;background-color: black;color: white;box-shadow:2px 2px darkgray;display:inline-block;position:relative;top:-30px;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
<script>
function playTone(freq) {
    const osc = window.audioContext.createOscillator();
    osc.type = window.waveformType || 'sine';
    osc.frequency.value = freq;
    osc.connect(window.gainNode);
    window.gainNode.connect(window.audioContext.destination);
    osc.start();
    window.activeOscillators.set(freq, osc);
}

function stopTone(freq) {
    const osc = window.activeOscillators.get(freq);
    if (osc) {
        osc.stop();
        osc.disconnect();
        window.activeOscillators.delete(freq);
    }
}</script>      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:24px;">51.9</div>
G♯<sub style="font-size:10px;pointer-events:none;">1</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" onmousedown="playTone(55.0)" onmouseup="stopTone(55.0)" onmouseleave="stopTone(55.0)" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;background-color:white;color:black;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
<script>
function playTone(freq) {
    const osc = window.audioContext.createOscillator();
    osc.type = window.waveformType || 'sine';
    osc.frequency.value = freq;
    osc.connect(window.gainNode);
    window.gainNode.connect(window.audioContext.destination);
    osc.start();
    window.activeOscillators.set(freq, osc);
}

function stopTone(freq) {
    const osc = window.activeOscillators.get(freq);
    if (osc) {
        osc.stop();
        osc.disconnect();
        window.activeOscillators.delete(freq);
    }
}</script>      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">55.0</div>
A<sub style="font-size:10px;pointer-events:none;">1</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#000';" onmousedown="playTone(58.3)" onmouseup="stopTone(58.3)" onmouseleave="stopTone(58.3)" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:16px;height:50px;background-color: black;color: white;box-shadow:2px 2px darkgray;display:inline-block;position:relative;top:-30px;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
<script>
function playTone(freq) {
    const osc = window.audioContext.createOscillator();
    osc.type = window.waveformType || 'sine';
    osc.frequency.value = freq;
    osc.connect(window.gainNode);
    window.gainNode.connect(window.audioContext.destination);
    osc.start();
    window.activeOscillators.set(freq, osc);
}

function stopTone(freq) {
    const osc = window.activeOscillators.get(freq);
    if (osc) {
        osc.stop();
        osc.disconnect();
        window.activeOscillators.delete(freq);
    }
}</script>      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:24px;">58.3</div>
A♯<sub style="font-size:10px;pointer-events:none;">1</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" onmousedown="playTone(61.7)" onmouseup="stopTone(61.7)" onmouseleave="stopTone(61.7)" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;background-color:white;color:black;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
<script>
function playTone(freq) {
    const osc = window.audioContext.createOscillator();
    osc.type = window.waveformType || 'sine';
    osc.frequency.value = freq;
    osc.connect(window.gainNode);
    window.gainNode.connect(window.audioContext.destination);
    osc.start();
    window.activeOscillators.set(freq, osc);
}

function stopTone(freq) {
    const osc = window.activeOscillators.get(freq);
    if (osc) {
        osc.stop();
        osc.disconnect();
        window.activeOscillators.delete(freq);
    }
}</script>      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">61.7</div>
B<sub style="font-size:10px;pointer-events:none;">1</sub>      </div>
    </div>
  </div>
  <div style="display:inline-block;padding:0 6px 0 0;">
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" onmousedown="playTone(65.4)" onmouseup="stopTone(65.4)" onmouseleave="stopTone(65.4)" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;background-color:white;color:black;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
<script>
function playTone(freq) {
    const osc = window.audioContext.createOscillator();
    osc.type = window.waveformType || 'sine';
    osc.frequency.value = freq;
    osc.connect(window.gainNode);
    window.gainNode.connect(window.audioContext.destination);
    osc.start();
    window.activeOscillators.set(freq, osc);
}

function stopTone(freq) {
    const osc = window.activeOscillators.get(freq);
    if (osc) {
        osc.stop();
        osc.disconnect();
        window.activeOscillators.delete(freq);
    }
}</script>      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">65.4</div>
C<sub style="font-size:10px;pointer-events:none;">2</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#000';" onmousedown="playTone(69.3)" onmouseup="stopTone(69.3)" onmouseleave="stopTone(69.3)" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:16px;height:50px;background-color: black;color: white;box-shadow:2px 2px darkgray;display:inline-block;position:relative;top:-30px;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
<script>
function playTone(freq) {
    const osc = window.audioContext.createOscillator();
    osc.type = window.waveformType || 'sine';
    osc.frequency.value = freq;
    osc.connect(window.gainNode);
    window.gainNode.connect(window.audioContext.destination);
    osc.start();
    window.activeOscillators.set(freq, osc);
}

function stopTone(freq) {
    const osc = window.activeOscillators.get(freq);
    if (osc) {
        osc.stop();
        osc.disconnect();
        window.activeOscillators.delete(freq);
    }
}</script>      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:24px;">69.3</div>
C♯<sub style="font-size:10px;pointer-events:none;">2</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" onmousedown="playTone(73.4)" onmouseup="stopTone(73.4)" onmouseleave="stopTone(73.4)" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;background-color:white;color:black;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
<script>
function playTone(freq) {
    const osc = window.audioContext.createOscillator();
    osc.type = window.waveformType || 'sine';
    osc.frequency.value = freq;
    osc.connect(window.gainNode);
    window.gainNode.connect(window.audioContext.destination);
    osc.start();
    window.activeOscillators.set(freq, osc);
}

function stopTone(freq) {
    const osc = window.activeOscillators.get(freq);
    if (osc) {
        osc.stop();
        osc.disconnect();
        window.activeOscillators.delete(freq);
    }
}</script>      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">73.4</div>
D<sub style="font-size:10px;pointer-events:none;">2</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#000';" onmousedown="playTone(77.8)" onmouseup="stopTone(77.8)" onmouseleave="stopTone(77.8)" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:16px;height:50px;background-color: black;color: white;box-shadow:2px 2px darkgray;display:inline-block;position:relative;top:-30px;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
<script>
function playTone(freq) {
    const osc = window.audioContext.createOscillator();
    osc.type = window.waveformType || 'sine';
    osc.frequency.value = freq;
    osc.connect(window.gainNode);
    window.gainNode.connect(window.audioContext.destination);
    osc.start();
    window.activeOscillators.set(freq, osc);
}

function stopTone(freq) {
    const osc = window.activeOscillators.get(freq);
    if (osc) {
        osc.stop();
        osc.disconnect();
        window.activeOscillators.delete(freq);
    }
}</script>      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:24px;">77.8</div>
D♯<sub style="font-size:10px;pointer-events:none;">2</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" onmousedown="playTone(82.4)" onmouseup="stopTone(82.4)" onmouseleave="stopTone(82.4)" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;background-color:white;color:black;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
<script>
function playTone(freq) {
    const osc = window.audioContext.createOscillator();
    osc.type = window.waveformType || 'sine';
    osc.frequency.value = freq;
    osc.connect(window.gainNode);
    window.gainNode.connect(window.audioContext.destination);
    osc.start();
    window.activeOscillators.set(freq, osc);
}

function stopTone(freq) {
    const osc = window.activeOscillators.get(freq);
    if (osc) {
        osc.stop();
        osc.disconnect();
        window.activeOscillators.delete(freq);
    }
}</script>      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">82.4</div>
E<sub style="font-size:10px;pointer-events:none;">2</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" onmousedown="playTone(87.3)" onmouseup="stopTone(87.3)" onmouseleave="stopTone(87.3)" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;background-color:white;color:black;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
<script>
function playTone(freq) {
    const osc = window.audioContext.createOscillator();
    osc.type = window.waveformType || 'sine';
    osc.frequency.value = freq;
    osc.connect(window.gainNode);
    window.gainNode.connect(window.audioContext.destination);
    osc.start();
    window.activeOscillators.set(freq, osc);
}

function stopTone(freq) {
    const osc = window.activeOscillators.get(freq);
    if (osc) {
        osc.stop();
        osc.disconnect();
        window.activeOscillators.delete(freq);
    }
}</script>      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">87.3</div>
F<sub style="font-size:10px;pointer-events:none;">2</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#000';" onmousedown="playTone(92.5)" onmouseup="stopTone(92.5)" onmouseleave="stopTone(92.5)" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:16px;height:50px;background-color: black;color: white;box-shadow:2px 2px darkgray;display:inline-block;position:relative;top:-30px;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
<script>
function playTone(freq) {
    const osc = window.audioContext.createOscillator();
    osc.type = window.waveformType || 'sine';
    osc.frequency.value = freq;
    osc.connect(window.gainNode);
    window.gainNode.connect(window.audioContext.destination);
    osc.start();
    window.activeOscillators.set(freq, osc);
}

function stopTone(freq) {
    const osc = window.activeOscillators.get(freq);
    if (osc) {
        osc.stop();
        osc.disconnect();
        window.activeOscillators.delete(freq);
    }
}</script>      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:24px;">92.5</div>
F♯<sub style="font-size:10px;pointer-events:none;">2</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" onmousedown="playTone(98.0)" onmouseup="stopTone(98.0)" onmouseleave="stopTone(98.0)" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;background-color:white;color:black;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
<script>
function playTone(freq) {
    const osc = window.audioContext.createOscillator();
    osc.type = window.waveformType || 'sine';
    osc.frequency.value = freq;
    osc.connect(window.gainNode);
    window.gainNode.connect(window.audioContext.destination);
    osc.start();
    window.activeOscillators.set(freq, osc);
}

function stopTone(freq) {
    const osc = window.activeOscillators.get(freq);
    if (osc) {
        osc.stop();
        osc.disconnect();
        window.activeOscillators.delete(freq);
    }
}</script>      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">98.0</div>
G<sub style="font-size:10px;pointer-events:none;">2</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#000';" onmousedown="playTone(103.8)" onmouseup="stopTone(103.8)" onmouseleave="stopTone(103.8)" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:16px;height:50px;background-color: black;color: white;box-shadow:2px 2px darkgray;display:inline-block;position:relative;top:-30px;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
<script>
function playTone(freq) {
    const osc = window.audioContext.createOscillator();
    osc.type = window.waveformType || 'sine';
    osc.frequency.value = freq;
    osc.connect(window.gainNode);
    window.gainNode.connect(window.audioContext.destination);
    osc.start();
    window.activeOscillators.set(freq, osc);
}

function stopTone(freq) {
    const osc = window.activeOscillators.get(freq);
    if (osc) {
        osc.stop();
        osc.disconnect();
        window.activeOscillators.delete(freq);
    }
}</script>      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:24px;">103.8</div>
G♯<sub style="font-size:10px;pointer-events:none;">2</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" onmousedown="playTone(110.0)" onmouseup="stopTone(110.0)" onmouseleave="stopTone(110.0)" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;background-color:white;color:black;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
<script>
function playTone(freq) {
    const osc = window.audioContext.createOscillator();
    osc.type = window.waveformType || 'sine';
    osc.frequency.value = freq;
    osc.connect(window.gainNode);
    window.gainNode.connect(window.audioContext.destination);
    osc.start();
    window.activeOscillators.set(freq, osc);
}

function stopTone(freq) {
    const osc = window.activeOscillators.get(freq);
    if (osc) {
        osc.stop();
        osc.disconnect();
        window.activeOscillators.delete(freq);
    }
}</script>      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">110.0</div>
A<sub style="font-size:10px;pointer-events:none;">2</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#000';" onmousedown="playTone(116.5)" onmouseup="stopTone(116.5)" onmouseleave="stopTone(116.5)" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:16px;height:50px;background-color: black;color: white;box-shadow:2px 2px darkgray;display:inline-block;position:relative;top:-30px;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
<script>
function playTone(freq) {
    const osc = window.audioContext.createOscillator();
    osc.type = window.waveformType || 'sine';
    osc.frequency.value = freq;
    osc.connect(window.gainNode);
    window.gainNode.connect(window.audioContext.destination);
    osc.start();
    window.activeOscillators.set(freq, osc);
}

function stopTone(freq) {
    const osc = window.activeOscillators.get(freq);
    if (osc) {
        osc.stop();
        osc.disconnect();
        window.activeOscillators.delete(freq);
    }
}</script>      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:24px;">116.5</div>
A♯<sub style="font-size:10px;pointer-events:none;">2</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" onmousedown="playTone(123.5)" onmouseup="stopTone(123.5)" onmouseleave="stopTone(123.5)" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;background-color:white;color:black;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
<script>
function playTone(freq) {
    const osc = window.audioContext.createOscillator();
    osc.type = window.waveformType || 'sine';
    osc.frequency.value = freq;
    osc.connect(window.gainNode);
    window.gainNode.connect(window.audioContext.destination);
    osc.start();
    window.activeOscillators.set(freq, osc);
}

function stopTone(freq) {
    const osc = window.activeOscillators.get(freq);
    if (osc) {
        osc.stop();
        osc.disconnect();
        window.activeOscillators.delete(freq);
    }
}</script>      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">123.5</div>
B<sub style="font-size:10px;pointer-events:none;">2</sub>      </div>
    </div>
  </div>
  <div style="display:inline-block;padding:0 6px 0 0;">
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" onmousedown="playTone(130.8)" onmouseup="stopTone(130.8)" onmouseleave="stopTone(130.8)" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;background-color:white;color:black;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
<script>
function playTone(freq) {
    const osc = window.audioContext.createOscillator();
    osc.type = window.waveformType || 'sine';
    osc.frequency.value = freq;
    osc.connect(window.gainNode);
    window.gainNode.connect(window.audioContext.destination);
    osc.start();
    window.activeOscillators.set(freq, osc);
}

function stopTone(freq) {
    const osc = window.activeOscillators.get(freq);
    if (osc) {
        osc.stop();
        osc.disconnect();
        window.activeOscillators.delete(freq);
    }
}</script>      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">130.8</div>
C<sub style="font-size:10px;pointer-events:none;">3</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#000';" onmousedown="playTone(138.6)" onmouseup="stopTone(138.6)" onmouseleave="stopTone(138.6)" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:16px;height:50px;background-color: black;color: white;box-shadow:2px 2px darkgray;display:inline-block;position:relative;top:-30px;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
<script>
function playTone(freq) {
    const osc = window.audioContext.createOscillator();
    osc.type = window.waveformType || 'sine';
    osc.frequency.value = freq;
    osc.connect(window.gainNode);
    window.gainNode.connect(window.audioContext.destination);
    osc.start();
    window.activeOscillators.set(freq, osc);
}

function stopTone(freq) {
    const osc = window.activeOscillators.get(freq);
    if (osc) {
        osc.stop();
        osc.disconnect();
        window.activeOscillators.delete(freq);
    }
}</script>      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:24px;">138.6</div>
C♯<sub style="font-size:10px;pointer-events:none;">3</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" onmousedown="playTone(146.8)" onmouseup="stopTone(146.8)" onmouseleave="stopTone(146.8)" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;background-color:white;color:black;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
<script>
function playTone(freq) {
    const osc = window.audioContext.createOscillator();
    osc.type = window.waveformType || 'sine';
    osc.frequency.value = freq;
    osc.connect(window.gainNode);
    window.gainNode.connect(window.audioContext.destination);
    osc.start();
    window.activeOscillators.set(freq, osc);
}

function stopTone(freq) {
    const osc = window.activeOscillators.get(freq);
    if (osc) {
        osc.stop();
        osc.disconnect();
        window.activeOscillators.delete(freq);
    }
}</script>      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">146.8</div>
D<sub style="font-size:10px;pointer-events:none;">3</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#000';" onmousedown="playTone(155.6)" onmouseup="stopTone(155.6)" onmouseleave="stopTone(155.6)" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:16px;height:50px;background-color: black;color: white;box-shadow:2px 2px darkgray;display:inline-block;position:relative;top:-30px;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
<script>
function playTone(freq) {
    const osc = window.audioContext.createOscillator();
    osc.type = window.waveformType || 'sine';
    osc.frequency.value = freq;
    osc.connect(window.gainNode);
    window.gainNode.connect(window.audioContext.destination);
    osc.start();
    window.activeOscillators.set(freq, osc);
}

function stopTone(freq) {
    const osc = window.activeOscillators.get(freq);
    if (osc) {
        osc.stop();
        osc.disconnect();
        window.activeOscillators.delete(freq);
    }
}</script>      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:24px;">155.6</div>
D♯<sub style="font-size:10px;pointer-events:none;">3</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" onmousedown="playTone(164.8)" onmouseup="stopTone(164.8)" onmouseleave="stopTone(164.8)" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;background-color:white;color:black;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
<script>
function playTone(freq) {
    const osc = window.audioContext.createOscillator();
    osc.type = window.waveformType || 'sine';
    osc.frequency.value = freq;
    osc.connect(window.gainNode);
    window.gainNode.connect(window.audioContext.destination);
    osc.start();
    window.activeOscillators.set(freq, osc);
}

function stopTone(freq) {
    const osc = window.activeOscillators.get(freq);
    if (osc) {
        osc.stop();
        osc.disconnect();
        window.activeOscillators.delete(freq);
    }
}</script>      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">164.8</div>
E<sub style="font-size:10px;pointer-events:none;">3</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" onmousedown="playTone(174.6)" onmouseup="stopTone(174.6)" onmouseleave="stopTone(174.6)" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;background-color:white;color:black;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
<script>
function playTone(freq) {
    const osc = window.audioContext.createOscillator();
    osc.type = window.waveformType || 'sine';
    osc.frequency.value = freq;
    osc.connect(window.gainNode);
    window.gainNode.connect(window.audioContext.destination);
    osc.start();
    window.activeOscillators.set(freq, osc);
}

function stopTone(freq) {
    const osc = window.activeOscillators.get(freq);
    if (osc) {
        osc.stop();
        osc.disconnect();
        window.activeOscillators.delete(freq);
    }
}</script>      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">174.6</div>
F<sub style="font-size:10px;pointer-events:none;">3</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#000';" onmousedown="playTone(185.0)" onmouseup="stopTone(185.0)" onmouseleave="stopTone(185.0)" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:16px;height:50px;background-color: black;color: white;box-shadow:2px 2px darkgray;display:inline-block;position:relative;top:-30px;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
<script>
function playTone(freq) {
    const osc = window.audioContext.createOscillator();
    osc.type = window.waveformType || 'sine';
    osc.frequency.value = freq;
    osc.connect(window.gainNode);
    window.gainNode.connect(window.audioContext.destination);
    osc.start();
    window.activeOscillators.set(freq, osc);
}

function stopTone(freq) {
    const osc = window.activeOscillators.get(freq);
    if (osc) {
        osc.stop();
        osc.disconnect();
        window.activeOscillators.delete(freq);
    }
}</script>      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:24px;">185.0</div>
F♯<sub style="font-size:10px;pointer-events:none;">3</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" onmousedown="playTone(196.0)" onmouseup="stopTone(196.0)" onmouseleave="stopTone(196.0)" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;background-color:white;color:black;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
<script>
function playTone(freq) {
    const osc = window.audioContext.createOscillator();
    osc.type = window.waveformType || 'sine';
    osc.frequency.value = freq;
    osc.connect(window.gainNode);
    window.gainNode.connect(window.audioContext.destination);
    osc.start();
    window.activeOscillators.set(freq, osc);
}

function stopTone(freq) {
    const osc = window.activeOscillators.get(freq);
    if (osc) {
        osc.stop();
        osc.disconnect();
        window.activeOscillators.delete(freq);
    }
}</script>      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">196.0</div>
G<sub style="font-size:10px;pointer-events:none;">3</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#000';" onmousedown="playTone(207.7)" onmouseup="stopTone(207.7)" onmouseleave="stopTone(207.7)" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:16px;height:50px;background-color: black;color: white;box-shadow:2px 2px darkgray;display:inline-block;position:relative;top:-30px;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
<script>
function playTone(freq) {
    const osc = window.audioContext.createOscillator();
    osc.type = window.waveformType || 'sine';
    osc.frequency.value = freq;
    osc.connect(window.gainNode);
    window.gainNode.connect(window.audioContext.destination);
    osc.start();
    window.activeOscillators.set(freq, osc);
}

function stopTone(freq) {
    const osc = window.activeOscillators.get(freq);
    if (osc) {
        osc.stop();
        osc.disconnect();
        window.activeOscillators.delete(freq);
    }
}</script>      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:24px;">207.7</div>
G♯<sub style="font-size:10px;pointer-events:none;">3</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" onmousedown="playTone(220.0)" onmouseup="stopTone(220.0)" onmouseleave="stopTone(220.0)" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;background-color:white;color:black;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
<script>
function playTone(freq) {
    const osc = window.audioContext.createOscillator();
    osc.type = window.waveformType || 'sine';
    osc.frequency.value = freq;
    osc.connect(window.gainNode);
    window.gainNode.connect(window.audioContext.destination);
    osc.start();
    window.activeOscillators.set(freq, osc);
}

function stopTone(freq) {
    const osc = window.activeOscillators.get(freq);
    if (osc) {
        osc.stop();
        osc.disconnect();
        window.activeOscillators.delete(freq);
    }
}</script>      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">220.0</div>
A<sub style="font-size:10px;pointer-events:none;">3</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#000';" onmousedown="playTone(233.1)" onmouseup="stopTone(233.1)" onmouseleave="stopTone(233.1)" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:16px;height:50px;background-color: black;color: white;box-shadow:2px 2px darkgray;display:inline-block;position:relative;top:-30px;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
<script>
function playTone(freq) {
    const osc = window.audioContext.createOscillator();
    osc.type = window.waveformType || 'sine';
    osc.frequency.value = freq;
    osc.connect(window.gainNode);
    window.gainNode.connect(window.audioContext.destination);
    osc.start();
    window.activeOscillators.set(freq, osc);
}

function stopTone(freq) {
    const osc = window.activeOscillators.get(freq);
    if (osc) {
        osc.stop();
        osc.disconnect();
        window.activeOscillators.delete(freq);
    }
}</script>      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:24px;">233.1</div>
A♯<sub style="font-size:10px;pointer-events:none;">3</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" onmousedown="playTone(246.9)" onmouseup="stopTone(246.9)" onmouseleave="stopTone(246.9)" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;background-color:white;color:black;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
<script>
function playTone(freq) {
    const osc = window.audioContext.createOscillator();
    osc.type = window.waveformType || 'sine';
    osc.frequency.value = freq;
    osc.connect(window.gainNode);
    window.gainNode.connect(window.audioContext.destination);
    osc.start();
    window.activeOscillators.set(freq, osc);
}

function stopTone(freq) {
    const osc = window.activeOscillators.get(freq);
    if (osc) {
        osc.stop();
        osc.disconnect();
        window.activeOscillators.delete(freq);
    }
}</script>      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">246.9</div>
B<sub style="font-size:10px;pointer-events:none;">3</sub>      </div>
    </div>
  </div>
  <div style="display:inline-block;padding:0 6px 0 0;">
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" onmousedown="playTone(261.6)" onmouseup="stopTone(261.6)" onmouseleave="stopTone(261.6)" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;background-color:white;color:black;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
<script>
function playTone(freq) {
    const osc = window.audioContext.createOscillator();
    osc.type = window.waveformType || 'sine';
    osc.frequency.value = freq;
    osc.connect(window.gainNode);
    window.gainNode.connect(window.audioContext.destination);
    osc.start();
    window.activeOscillators.set(freq, osc);
}

function stopTone(freq) {
    const osc = window.activeOscillators.get(freq);
    if (osc) {
        osc.stop();
        osc.disconnect();
        window.activeOscillators.delete(freq);
    }
}</script>      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">261.6</div>
C<sub style="font-size:10px;pointer-events:none;">4</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#000';" onmousedown="playTone(277.2)" onmouseup="stopTone(277.2)" onmouseleave="stopTone(277.2)" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:16px;height:50px;background-color: black;color: white;box-shadow:2px 2px darkgray;display:inline-block;position:relative;top:-30px;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
<script>
function playTone(freq) {
    const osc = window.audioContext.createOscillator();
    osc.type = window.waveformType || 'sine';
    osc.frequency.value = freq;
    osc.connect(window.gainNode);
    window.gainNode.connect(window.audioContext.destination);
    osc.start();
    window.activeOscillators.set(freq, osc);
}

function stopTone(freq) {
    const osc = window.activeOscillators.get(freq);
    if (osc) {
        osc.stop();
        osc.disconnect();
        window.activeOscillators.delete(freq);
    }
}</script>      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:24px;">277.2</div>
C♯<sub style="font-size:10px;pointer-events:none;">4</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" onmousedown="playTone(293.7)" onmouseup="stopTone(293.7)" onmouseleave="stopTone(293.7)" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;background-color:white;color:black;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
<script>
function playTone(freq) {
    const osc = window.audioContext.createOscillator();
    osc.type = window.waveformType || 'sine';
    osc.frequency.value = freq;
    osc.connect(window.gainNode);
    window.gainNode.connect(window.audioContext.destination);
    osc.start();
    window.activeOscillators.set(freq, osc);
}

function stopTone(freq) {
    const osc = window.activeOscillators.get(freq);
    if (osc) {
        osc.stop();
        osc.disconnect();
        window.activeOscillators.delete(freq);
    }
}</script>      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">293.7</div>
D<sub style="font-size:10px;pointer-events:none;">4</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#000';" onmousedown="playTone(311.1)" onmouseup="stopTone(311.1)" onmouseleave="stopTone(311.1)" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:16px;height:50px;background-color: black;color: white;box-shadow:2px 2px darkgray;display:inline-block;position:relative;top:-30px;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
<script>
function playTone(freq) {
    const osc = window.audioContext.createOscillator();
    osc.type = window.waveformType || 'sine';
    osc.frequency.value = freq;
    osc.connect(window.gainNode);
    window.gainNode.connect(window.audioContext.destination);
    osc.start();
    window.activeOscillators.set(freq, osc);
}

function stopTone(freq) {
    const osc = window.activeOscillators.get(freq);
    if (osc) {
        osc.stop();
        osc.disconnect();
        window.activeOscillators.delete(freq);
    }
}</script>      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:24px;">311.1</div>
D♯<sub style="font-size:10px;pointer-events:none;">4</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" onmousedown="playTone(329.6)" onmouseup="stopTone(329.6)" onmouseleave="stopTone(329.6)" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;background-color:white;color:black;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
<script>
function playTone(freq) {
    const osc = window.audioContext.createOscillator();
    osc.type = window.waveformType || 'sine';
    osc.frequency.value = freq;
    osc.connect(window.gainNode);
    window.gainNode.connect(window.audioContext.destination);
    osc.start();
    window.activeOscillators.set(freq, osc);
}

function stopTone(freq) {
    const osc = window.activeOscillators.get(freq);
    if (osc) {
        osc.stop();
        osc.disconnect();
        window.activeOscillators.delete(freq);
    }
}</script>      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">329.6</div>
E<sub style="font-size:10px;pointer-events:none;">4</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" onmousedown="playTone(349.2)" onmouseup="stopTone(349.2)" onmouseleave="stopTone(349.2)" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;background-color:white;color:black;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
<script>
function playTone(freq) {
    const osc = window.audioContext.createOscillator();
    osc.type = window.waveformType || 'sine';
    osc.frequency.value = freq;
    osc.connect(window.gainNode);
    window.gainNode.connect(window.audioContext.destination);
    osc.start();
    window.activeOscillators.set(freq, osc);
}

function stopTone(freq) {
    const osc = window.activeOscillators.get(freq);
    if (osc) {
        osc.stop();
        osc.disconnect();
        window.activeOscillators.delete(freq);
    }
}</script>      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">349.2</div>
F<sub style="font-size:10px;pointer-events:none;">4</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#000';" onmousedown="playTone(370.0)" onmouseup="stopTone(370.0)" onmouseleave="stopTone(370.0)" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:16px;height:50px;background-color: black;color: white;box-shadow:2px 2px darkgray;display:inline-block;position:relative;top:-30px;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
<script>
function playTone(freq) {
    const osc = window.audioContext.createOscillator();
    osc.type = window.waveformType || 'sine';
    osc.frequency.value = freq;
    osc.connect(window.gainNode);
    window.gainNode.connect(window.audioContext.destination);
    osc.start();
    window.activeOscillators.set(freq, osc);
}

function stopTone(freq) {
    const osc = window.activeOscillators.get(freq);
    if (osc) {
        osc.stop();
        osc.disconnect();
        window.activeOscillators.delete(freq);
    }
}</script>      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:24px;">370.0</div>
F♯<sub style="font-size:10px;pointer-events:none;">4</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" onmousedown="playTone(392.0)" onmouseup="stopTone(392.0)" onmouseleave="stopTone(392.0)" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;background-color:white;color:black;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
<script>
function playTone(freq) {
    const osc = window.audioContext.createOscillator();
    osc.type = window.waveformType || 'sine';
    osc.frequency.value = freq;
    osc.connect(window.gainNode);
    window.gainNode.connect(window.audioContext.destination);
    osc.start();
    window.activeOscillators.set(freq, osc);
}

function stopTone(freq) {
    const osc = window.activeOscillators.get(freq);
    if (osc) {
        osc.stop();
        osc.disconnect();
        window.activeOscillators.delete(freq);
    }
}</script>      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">392.0</div>
G<sub style="font-size:10px;pointer-events:none;">4</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#000';" onmousedown="playTone(415.3)" onmouseup="stopTone(415.3)" onmouseleave="stopTone(415.3)" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:16px;height:50px;background-color: black;color: white;box-shadow:2px 2px darkgray;display:inline-block;position:relative;top:-30px;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
<script>
function playTone(freq) {
    const osc = window.audioContext.createOscillator();
    osc.type = window.waveformType || 'sine';
    osc.frequency.value = freq;
    osc.connect(window.gainNode);
    window.gainNode.connect(window.audioContext.destination);
    osc.start();
    window.activeOscillators.set(freq, osc);
}

function stopTone(freq) {
    const osc = window.activeOscillators.get(freq);
    if (osc) {
        osc.stop();
        osc.disconnect();
        window.activeOscillators.delete(freq);
    }
}</script>      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:24px;">415.3</div>
G♯<sub style="font-size:10px;pointer-events:none;">4</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" onmousedown="playTone(440.0)" onmouseup="stopTone(440.0)" onmouseleave="stopTone(440.0)" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;background-color:white;color:black;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
<script>
function playTone(freq) {
    const osc = window.audioContext.createOscillator();
    osc.type = window.waveformType || 'sine';
    osc.frequency.value = freq;
    osc.connect(window.gainNode);
    window.gainNode.connect(window.audioContext.destination);
    osc.start();
    window.activeOscillators.set(freq, osc);
}

function stopTone(freq) {
    const osc = window.activeOscillators.get(freq);
    if (osc) {
        osc.stop();
        osc.disconnect();
        window.activeOscillators.delete(freq);
    }
}</script>      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">440.0</div>
A<sub style="font-size:10px;pointer-events:none;">4</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#000';" onmousedown="playTone(466.2)" onmouseup="stopTone(466.2)" onmouseleave="stopTone(466.2)" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:16px;height:50px;background-color: black;color: white;box-shadow:2px 2px darkgray;display:inline-block;position:relative;top:-30px;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
<script>
function playTone(freq) {
    const osc = window.audioContext.createOscillator();
    osc.type = window.waveformType || 'sine';
    osc.frequency.value = freq;
    osc.connect(window.gainNode);
    window.gainNode.connect(window.audioContext.destination);
    osc.start();
    window.activeOscillators.set(freq, osc);
}

function stopTone(freq) {
    const osc = window.activeOscillators.get(freq);
    if (osc) {
        osc.stop();
        osc.disconnect();
        window.activeOscillators.delete(freq);
    }
}</script>      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:24px;">466.2</div>
A♯<sub style="font-size:10px;pointer-events:none;">4</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" onmousedown="playTone(493.9)" onmouseup="stopTone(493.9)" onmouseleave="stopTone(493.9)" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;background-color:white;color:black;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
<script>
function playTone(freq) {
    const osc = window.audioContext.createOscillator();
    osc.type = window.waveformType || 'sine';
    osc.frequency.value = freq;
    osc.connect(window.gainNode);
    window.gainNode.connect(window.audioContext.destination);
    osc.start();
    window.activeOscillators.set(freq, osc);
}

function stopTone(freq) {
    const osc = window.activeOscillators.get(freq);
    if (osc) {
        osc.stop();
        osc.disconnect();
        window.activeOscillators.delete(freq);
    }
}</script>      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">493.9</div>
B<sub style="font-size:10px;pointer-events:none;">4</sub>      </div>
    </div>
  </div>
  <div style="display:inline-block;padding:0 6px 0 0;">
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" onmousedown="playTone(523.3)" onmouseup="stopTone(523.3)" onmouseleave="stopTone(523.3)" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;background-color:white;color:black;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
<script>
function playTone(freq) {
    const osc = window.audioContext.createOscillator();
    osc.type = window.waveformType || 'sine';
    osc.frequency.value = freq;
    osc.connect(window.gainNode);
    window.gainNode.connect(window.audioContext.destination);
    osc.start();
    window.activeOscillators.set(freq, osc);
}

function stopTone(freq) {
    const osc = window.activeOscillators.get(freq);
    if (osc) {
        osc.stop();
        osc.disconnect();
        window.activeOscillators.delete(freq);
    }
}</script>      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">523.3</div>
C<sub style="font-size:10px;pointer-events:none;">5</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#000';" onmousedown="playTone(554.4)" onmouseup="stopTone(554.4)" onmouseleave="stopTone(554.4)" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:16px;height:50px;background-color: black;color: white;box-shadow:2px 2px darkgray;display:inline-block;position:relative;top:-30px;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
<script>
function playTone(freq) {
    const osc = window.audioContext.createOscillator();
    osc.type = window.waveformType || 'sine';
    osc.frequency.value = freq;
    osc.connect(window.gainNode);
    window.gainNode.connect(window.audioContext.destination);
    osc.start();
    window.activeOscillators.set(freq, osc);
}

function stopTone(freq) {
    const osc = window.activeOscillators.get(freq);
    if (osc) {
        osc.stop();
        osc.disconnect();
        window.activeOscillators.delete(freq);
    }
}</script>      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:24px;">554.4</div>
C♯<sub style="font-size:10px;pointer-events:none;">5</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" onmousedown="playTone(587.3)" onmouseup="stopTone(587.3)" onmouseleave="stopTone(587.3)" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;background-color:white;color:black;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
<script>
function playTone(freq) {
    const osc = window.audioContext.createOscillator();
    osc.type = window.waveformType || 'sine';
    osc.frequency.value = freq;
    osc.connect(window.gainNode);
    window.gainNode.connect(window.audioContext.destination);
    osc.start();
    window.activeOscillators.set(freq, osc);
}

function stopTone(freq) {
    const osc = window.activeOscillators.get(freq);
    if (osc) {
        osc.stop();
        osc.disconnect();
        window.activeOscillators.delete(freq);
    }
}</script>      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">587.3</div>
D<sub style="font-size:10px;pointer-events:none;">5</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#000';" onmousedown="playTone(622.3)" onmouseup="stopTone(622.3)" onmouseleave="stopTone(622.3)" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:16px;height:50px;background-color: black;color: white;box-shadow:2px 2px darkgray;display:inline-block;position:relative;top:-30px;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
<script>
function playTone(freq) {
    const osc = window.audioContext.createOscillator();
    osc.type = window.waveformType || 'sine';
    osc.frequency.value = freq;
    osc.connect(window.gainNode);
    window.gainNode.connect(window.audioContext.destination);
    osc.start();
    window.activeOscillators.set(freq, osc);
}

function stopTone(freq) {
    const osc = window.activeOscillators.get(freq);
    if (osc) {
        osc.stop();
        osc.disconnect();
        window.activeOscillators.delete(freq);
    }
}</script>      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:24px;">622.3</div>
D♯<sub style="font-size:10px;pointer-events:none;">5</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" onmousedown="playTone(659.3)" onmouseup="stopTone(659.3)" onmouseleave="stopTone(659.3)" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;background-color:white;color:black;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
<script>
function playTone(freq) {
    const osc = window.audioContext.createOscillator();
    osc.type = window.waveformType || 'sine';
    osc.frequency.value = freq;
    osc.connect(window.gainNode);
    window.gainNode.connect(window.audioContext.destination);
    osc.start();
    window.activeOscillators.set(freq, osc);
}

function stopTone(freq) {
    const osc = window.activeOscillators.get(freq);
    if (osc) {
        osc.stop();
        osc.disconnect();
        window.activeOscillators.delete(freq);
    }
}</script>      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">659.3</div>
E<sub style="font-size:10px;pointer-events:none;">5</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" onmousedown="playTone(698.5)" onmouseup="stopTone(698.5)" onmouseleave="stopTone(698.5)" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;background-color:white;color:black;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
<script>
function playTone(freq) {
    const osc = window.audioContext.createOscillator();
    osc.type = window.waveformType || 'sine';
    osc.frequency.value = freq;
    osc.connect(window.gainNode);
    window.gainNode.connect(window.audioContext.destination);
    osc.start();
    window.activeOscillators.set(freq, osc);
}

function stopTone(freq) {
    const osc = window.activeOscillators.get(freq);
    if (osc) {
        osc.stop();
        osc.disconnect();
        window.activeOscillators.delete(freq);
    }
}</script>      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">698.5</div>
F<sub style="font-size:10px;pointer-events:none;">5</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#000';" onmousedown="playTone(740.0)" onmouseup="stopTone(740.0)" onmouseleave="stopTone(740.0)" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:16px;height:50px;background-color: black;color: white;box-shadow:2px 2px darkgray;display:inline-block;position:relative;top:-30px;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
<script>
function playTone(freq) {
    const osc = window.audioContext.createOscillator();
    osc.type = window.waveformType || 'sine';
    osc.frequency.value = freq;
    osc.connect(window.gainNode);
    window.gainNode.connect(window.audioContext.destination);
    osc.start();
    window.activeOscillators.set(freq, osc);
}

function stopTone(freq) {
    const osc = window.activeOscillators.get(freq);
    if (osc) {
        osc.stop();
        osc.disconnect();
        window.activeOscillators.delete(freq);
    }
}</script>      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:24px;">740.0</div>
F♯<sub style="font-size:10px;pointer-events:none;">5</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" onmousedown="playTone(784.0)" onmouseup="stopTone(784.0)" onmouseleave="stopTone(784.0)" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;background-color:white;color:black;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
<script>
function playTone(freq) {
    const osc = window.audioContext.createOscillator();
    osc.type = window.waveformType || 'sine';
    osc.frequency.value = freq;
    osc.connect(window.gainNode);
    window.gainNode.connect(window.audioContext.destination);
    osc.start();
    window.activeOscillators.set(freq, osc);
}

function stopTone(freq) {
    const osc = window.activeOscillators.get(freq);
    if (osc) {
        osc.stop();
        osc.disconnect();
        window.activeOscillators.delete(freq);
    }
}</script>      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">784.0</div>
G<sub style="font-size:10px;pointer-events:none;">5</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#000';" onmousedown="playTone(830.6)" onmouseup="stopTone(830.6)" onmouseleave="stopTone(830.6)" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:16px;height:50px;background-color: black;color: white;box-shadow:2px 2px darkgray;display:inline-block;position:relative;top:-30px;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
<script>
function playTone(freq) {
    const osc = window.audioContext.createOscillator();
    osc.type = window.waveformType || 'sine';
    osc.frequency.value = freq;
    osc.connect(window.gainNode);
    window.gainNode.connect(window.audioContext.destination);
    osc.start();
    window.activeOscillators.set(freq, osc);
}

function stopTone(freq) {
    const osc = window.activeOscillators.get(freq);
    if (osc) {
        osc.stop();
        osc.disconnect();
        window.activeOscillators.delete(freq);
    }
}</script>      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:24px;">830.6</div>
G♯<sub style="font-size:10px;pointer-events:none;">5</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" onmousedown="playTone(880.0)" onmouseup="stopTone(880.0)" onmouseleave="stopTone(880.0)" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;background-color:white;color:black;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
<script>
function playTone(freq) {
    const osc = window.audioContext.createOscillator();
    osc.type = window.waveformType || 'sine';
    osc.frequency.value = freq;
    osc.connect(window.gainNode);
    window.gainNode.connect(window.audioContext.destination);
    osc.start();
    window.activeOscillators.set(freq, osc);
}

function stopTone(freq) {
    const osc = window.activeOscillators.get(freq);
    if (osc) {
        osc.stop();
        osc.disconnect();
        window.activeOscillators.delete(freq);
    }
}</script>      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">880.0</div>
A<sub style="font-size:10px;pointer-events:none;">5</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#000';" onmousedown="playTone(932.3)" onmouseup="stopTone(932.3)" onmouseleave="stopTone(932.3)" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:16px;height:50px;background-color: black;color: white;box-shadow:2px 2px darkgray;display:inline-block;position:relative;top:-30px;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
<script>
function playTone(freq) {
    const osc = window.audioContext.createOscillator();
    osc.type = window.waveformType || 'sine';
    osc.frequency.value = freq;
    osc.connect(window.gainNode);
    window.gainNode.connect(window.audioContext.destination);
    osc.start();
    window.activeOscillators.set(freq, osc);
}

function stopTone(freq) {
    const osc = window.activeOscillators.get(freq);
    if (osc) {
        osc.stop();
        osc.disconnect();
        window.activeOscillators.delete(freq);
    }
}</script>      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:24px;">932.3</div>
A♯<sub style="font-size:10px;pointer-events:none;">5</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" onmousedown="playTone(987.8)" onmouseup="stopTone(987.8)" onmouseleave="stopTone(987.8)" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;background-color:white;color:black;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
<script>
function playTone(freq) {
    const osc = window.audioContext.createOscillator();
    osc.type = window.waveformType || 'sine';
    osc.frequency.value = freq;
    osc.connect(window.gainNode);
    window.gainNode.connect(window.audioContext.destination);
    osc.start();
    window.activeOscillators.set(freq, osc);
}

function stopTone(freq) {
    const osc = window.activeOscillators.get(freq);
    if (osc) {
        osc.stop();
        osc.disconnect();
        window.activeOscillators.delete(freq);
    }
}</script>      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">987.8</div>
B<sub style="font-size:10px;pointer-events:none;">5</sub>      </div>
    </div>
  </div>
  <div style="display:inline-block;padding:0 6px 0 0;">
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" onmousedown="playTone(1046.5)" onmouseup="stopTone(1046.5)" onmouseleave="stopTone(1046.5)" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;background-color:white;color:black;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
<script>
function playTone(freq) {
    const osc = window.audioContext.createOscillator();
    osc.type = window.waveformType || 'sine';
    osc.frequency.value = freq;
    osc.connect(window.gainNode);
    window.gainNode.connect(window.audioContext.destination);
    osc.start();
    window.activeOscillators.set(freq, osc);
}

function stopTone(freq) {
    const osc = window.activeOscillators.get(freq);
    if (osc) {
        osc.stop();
        osc.disconnect();
        window.activeOscillators.delete(freq);
    }
}</script>      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">1046.5</div>
C<sub style="font-size:10px;pointer-events:none;">6</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#000';" onmousedown="playTone(1108.7)" onmouseup="stopTone(1108.7)" onmouseleave="stopTone(1108.7)" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:16px;height:50px;background-color: black;color: white;box-shadow:2px 2px darkgray;display:inline-block;position:relative;top:-30px;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
<script>
function playTone(freq) {
    const osc = window.audioContext.createOscillator();
    osc.type = window.waveformType || 'sine';
    osc.frequency.value = freq;
    osc.connect(window.gainNode);
    window.gainNode.connect(window.audioContext.destination);
    osc.start();
    window.activeOscillators.set(freq, osc);
}

function stopTone(freq) {
    const osc = window.activeOscillators.get(freq);
    if (osc) {
        osc.stop();
        osc.disconnect();
        window.activeOscillators.delete(freq);
    }
}</script>      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:24px;">1108.7</div>
C♯<sub style="font-size:10px;pointer-events:none;">6</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" onmousedown="playTone(1174.7)" onmouseup="stopTone(1174.7)" onmouseleave="stopTone(1174.7)" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;background-color:white;color:black;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
<script>
function playTone(freq) {
    const osc = window.audioContext.createOscillator();
    osc.type = window.waveformType || 'sine';
    osc.frequency.value = freq;
    osc.connect(window.gainNode);
    window.gainNode.connect(window.audioContext.destination);
    osc.start();
    window.activeOscillators.set(freq, osc);
}

function stopTone(freq) {
    const osc = window.activeOscillators.get(freq);
    if (osc) {
        osc.stop();
        osc.disconnect();
        window.activeOscillators.delete(freq);
    }
}</script>      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">1174.7</div>
D<sub style="font-size:10px;pointer-events:none;">6</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#000';" onmousedown="playTone(1244.5)" onmouseup="stopTone(1244.5)" onmouseleave="stopTone(1244.5)" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:16px;height:50px;background-color: black;color: white;box-shadow:2px 2px darkgray;display:inline-block;position:relative;top:-30px;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
<script>
function playTone(freq) {
    const osc = window.audioContext.createOscillator();
    osc.type = window.waveformType || 'sine';
    osc.frequency.value = freq;
    osc.connect(window.gainNode);
    window.gainNode.connect(window.audioContext.destination);
    osc.start();
    window.activeOscillators.set(freq, osc);
}

function stopTone(freq) {
    const osc = window.activeOscillators.get(freq);
    if (osc) {
        osc.stop();
        osc.disconnect();
        window.activeOscillators.delete(freq);
    }
}</script>      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:24px;">1244.5</div>
D♯<sub style="font-size:10px;pointer-events:none;">6</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" onmousedown="playTone(1318.5)" onmouseup="stopTone(1318.5)" onmouseleave="stopTone(1318.5)" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;background-color:white;color:black;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
<script>
function playTone(freq) {
    const osc = window.audioContext.createOscillator();
    osc.type = window.waveformType || 'sine';
    osc.frequency.value = freq;
    osc.connect(window.gainNode);
    window.gainNode.connect(window.audioContext.destination);
    osc.start();
    window.activeOscillators.set(freq, osc);
}

function stopTone(freq) {
    const osc = window.activeOscillators.get(freq);
    if (osc) {
        osc.stop();
        osc.disconnect();
        window.activeOscillators.delete(freq);
    }
}</script>      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">1318.5</div>
E<sub style="font-size:10px;pointer-events:none;">6</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" onmousedown="playTone(1396.9)" onmouseup="stopTone(1396.9)" onmouseleave="stopTone(1396.9)" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;background-color:white;color:black;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
<script>
function playTone(freq) {
    const osc = window.audioContext.createOscillator();
    osc.type = window.waveformType || 'sine';
    osc.frequency.value = freq;
    osc.connect(window.gainNode);
    window.gainNode.connect(window.audioContext.destination);
    osc.start();
    window.activeOscillators.set(freq, osc);
}

function stopTone(freq) {
    const osc = window.activeOscillators.get(freq);
    if (osc) {
        osc.stop();
        osc.disconnect();
        window.activeOscillators.delete(freq);
    }
}</script>      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">1396.9</div>
F<sub style="font-size:10px;pointer-events:none;">6</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#000';" onmousedown="playTone(1480.0)" onmouseup="stopTone(1480.0)" onmouseleave="stopTone(1480.0)" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:16px;height:50px;background-color: black;color: white;box-shadow:2px 2px darkgray;display:inline-block;position:relative;top:-30px;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
<script>
function playTone(freq) {
    const osc = window.audioContext.createOscillator();
    osc.type = window.waveformType || 'sine';
    osc.frequency.value = freq;
    osc.connect(window.gainNode);
    window.gainNode.connect(window.audioContext.destination);
    osc.start();
    window.activeOscillators.set(freq, osc);
}

function stopTone(freq) {
    const osc = window.activeOscillators.get(freq);
    if (osc) {
        osc.stop();
        osc.disconnect();
        window.activeOscillators.delete(freq);
    }
}</script>      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:24px;">1480.0</div>
F♯<sub style="font-size:10px;pointer-events:none;">6</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" onmousedown="playTone(1568.0)" onmouseup="stopTone(1568.0)" onmouseleave="stopTone(1568.0)" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;background-color:white;color:black;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
<script>
function playTone(freq) {
    const osc = window.audioContext.createOscillator();
    osc.type = window.waveformType || 'sine';
    osc.frequency.value = freq;
    osc.connect(window.gainNode);
    window.gainNode.connect(window.audioContext.destination);
    osc.start();
    window.activeOscillators.set(freq, osc);
}

function stopTone(freq) {
    const osc = window.activeOscillators.get(freq);
    if (osc) {
        osc.stop();
        osc.disconnect();
        window.activeOscillators.delete(freq);
    }
}</script>      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">1568.0</div>
G<sub style="font-size:10px;pointer-events:none;">6</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#000';" onmousedown="playTone(1661.2)" onmouseup="stopTone(1661.2)" onmouseleave="stopTone(1661.2)" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:16px;height:50px;background-color: black;color: white;box-shadow:2px 2px darkgray;display:inline-block;position:relative;top:-30px;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
<script>
function playTone(freq) {
    const osc = window.audioContext.createOscillator();
    osc.type = window.waveformType || 'sine';
    osc.frequency.value = freq;
    osc.connect(window.gainNode);
    window.gainNode.connect(window.audioContext.destination);
    osc.start();
    window.activeOscillators.set(freq, osc);
}

function stopTone(freq) {
    const osc = window.activeOscillators.get(freq);
    if (osc) {
        osc.stop();
        osc.disconnect();
        window.activeOscillators.delete(freq);
    }
}</script>      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:24px;">1661.2</div>
G♯<sub style="font-size:10px;pointer-events:none;">6</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" onmousedown="playTone(1760.0)" onmouseup="stopTone(1760.0)" onmouseleave="stopTone(1760.0)" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;background-color:white;color:black;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
<script>
function playTone(freq) {
    const osc = window.audioContext.createOscillator();
    osc.type = window.waveformType || 'sine';
    osc.frequency.value = freq;
    osc.connect(window.gainNode);
    window.gainNode.connect(window.audioContext.destination);
    osc.start();
    window.activeOscillators.set(freq, osc);
}

function stopTone(freq) {
    const osc = window.activeOscillators.get(freq);
    if (osc) {
        osc.stop();
        osc.disconnect();
        window.activeOscillators.delete(freq);
    }
}</script>      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">1760.0</div>
A<sub style="font-size:10px;pointer-events:none;">6</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#000';" onmousedown="playTone(1864.7)" onmouseup="stopTone(1864.7)" onmouseleave="stopTone(1864.7)" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:16px;height:50px;background-color: black;color: white;box-shadow:2px 2px darkgray;display:inline-block;position:relative;top:-30px;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
<script>
function playTone(freq) {
    const osc = window.audioContext.createOscillator();
    osc.type = window.waveformType || 'sine';
    osc.frequency.value = freq;
    osc.connect(window.gainNode);
    window.gainNode.connect(window.audioContext.destination);
    osc.start();
    window.activeOscillators.set(freq, osc);
}

function stopTone(freq) {
    const osc = window.activeOscillators.get(freq);
    if (osc) {
        osc.stop();
        osc.disconnect();
        window.activeOscillators.delete(freq);
    }
}</script>      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:24px;">1864.7</div>
A♯<sub style="font-size:10px;pointer-events:none;">6</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" onmousedown="playTone(1975.5)" onmouseup="stopTone(1975.5)" onmouseleave="stopTone(1975.5)" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;background-color:white;color:black;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
<script>
function playTone(freq) {
    const osc = window.audioContext.createOscillator();
    osc.type = window.waveformType || 'sine';
    osc.frequency.value = freq;
    osc.connect(window.gainNode);
    window.gainNode.connect(window.audioContext.destination);
    osc.start();
    window.activeOscillators.set(freq, osc);
}

function stopTone(freq) {
    const osc = window.activeOscillators.get(freq);
    if (osc) {
        osc.stop();
        osc.disconnect();
        window.activeOscillators.delete(freq);
    }
}</script>      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">1975.5</div>
B<sub style="font-size:10px;pointer-events:none;">6</sub>      </div>
    </div>
  </div>
  <div style="display:inline-block;padding:0 6px 0 0;">
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" onmousedown="playTone(2093.0)" onmouseup="stopTone(2093.0)" onmouseleave="stopTone(2093.0)" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;background-color:white;color:black;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
<script>
function playTone(freq) {
    const osc = window.audioContext.createOscillator();
    osc.type = window.waveformType || 'sine';
    osc.frequency.value = freq;
    osc.connect(window.gainNode);
    window.gainNode.connect(window.audioContext.destination);
    osc.start();
    window.activeOscillators.set(freq, osc);
}

function stopTone(freq) {
    const osc = window.activeOscillators.get(freq);
    if (osc) {
        osc.stop();
        osc.disconnect();
        window.activeOscillators.delete(freq);
    }
}</script>      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">2093.0</div>
C<sub style="font-size:10px;pointer-events:none;">7</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#000';" onmousedown="playTone(2217.5)" onmouseup="stopTone(2217.5)" onmouseleave="stopTone(2217.5)" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:16px;height:50px;background-color: black;color: white;box-shadow:2px 2px darkgray;display:inline-block;position:relative;top:-30px;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
<script>
function playTone(freq) {
    const osc = window.audioContext.createOscillator();
    osc.type = window.waveformType || 'sine';
    osc.frequency.value = freq;
    osc.connect(window.gainNode);
    window.gainNode.connect(window.audioContext.destination);
    osc.start();
    window.activeOscillators.set(freq, osc);
}

function stopTone(freq) {
    const osc = window.activeOscillators.get(freq);
    if (osc) {
        osc.stop();
        osc.disconnect();
        window.activeOscillators.delete(freq);
    }
}</script>      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:24px;">2217.5</div>
C♯<sub style="font-size:10px;pointer-events:none;">7</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" onmousedown="playTone(2349.3)" onmouseup="stopTone(2349.3)" onmouseleave="stopTone(2349.3)" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;background-color:white;color:black;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
<script>
function playTone(freq) {
    const osc = window.audioContext.createOscillator();
    osc.type = window.waveformType || 'sine';
    osc.frequency.value = freq;
    osc.connect(window.gainNode);
    window.gainNode.connect(window.audioContext.destination);
    osc.start();
    window.activeOscillators.set(freq, osc);
}

function stopTone(freq) {
    const osc = window.activeOscillators.get(freq);
    if (osc) {
        osc.stop();
        osc.disconnect();
        window.activeOscillators.delete(freq);
    }
}</script>      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">2349.3</div>
D<sub style="font-size:10px;pointer-events:none;">7</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#000';" onmousedown="playTone(2489.0)" onmouseup="stopTone(2489.0)" onmouseleave="stopTone(2489.0)" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:16px;height:50px;background-color: black;color: white;box-shadow:2px 2px darkgray;display:inline-block;position:relative;top:-30px;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
<script>
function playTone(freq) {
    const osc = window.audioContext.createOscillator();
    osc.type = window.waveformType || 'sine';
    osc.frequency.value = freq;
    osc.connect(window.gainNode);
    window.gainNode.connect(window.audioContext.destination);
    osc.start();
    window.activeOscillators.set(freq, osc);
}

function stopTone(freq) {
    const osc = window.activeOscillators.get(freq);
    if (osc) {
        osc.stop();
        osc.disconnect();
        window.activeOscillators.delete(freq);
    }
}</script>      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:24px;">2489.0</div>
D♯<sub style="font-size:10px;pointer-events:none;">7</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" onmousedown="playTone(2637.0)" onmouseup="stopTone(2637.0)" onmouseleave="stopTone(2637.0)" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;background-color:white;color:black;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
<script>
function playTone(freq) {
    const osc = window.audioContext.createOscillator();
    osc.type = window.waveformType || 'sine';
    osc.frequency.value = freq;
    osc.connect(window.gainNode);
    window.gainNode.connect(window.audioContext.destination);
    osc.start();
    window.activeOscillators.set(freq, osc);
}

function stopTone(freq) {
    const osc = window.activeOscillators.get(freq);
    if (osc) {
        osc.stop();
        osc.disconnect();
        window.activeOscillators.delete(freq);
    }
}</script>      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">2637.0</div>
E<sub style="font-size:10px;pointer-events:none;">7</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" onmousedown="playTone(2793.8)" onmouseup="stopTone(2793.8)" onmouseleave="stopTone(2793.8)" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;background-color:white;color:black;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
<script>
function playTone(freq) {
    const osc = window.audioContext.createOscillator();
    osc.type = window.waveformType || 'sine';
    osc.frequency.value = freq;
    osc.connect(window.gainNode);
    window.gainNode.connect(window.audioContext.destination);
    osc.start();
    window.activeOscillators.set(freq, osc);
}

function stopTone(freq) {
    const osc = window.activeOscillators.get(freq);
    if (osc) {
        osc.stop();
        osc.disconnect();
        window.activeOscillators.delete(freq);
    }
}</script>      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">2793.8</div>
F<sub style="font-size:10px;pointer-events:none;">7</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#000';" onmousedown="playTone(2960.0)" onmouseup="stopTone(2960.0)" onmouseleave="stopTone(2960.0)" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:16px;height:50px;background-color: black;color: white;box-shadow:2px 2px darkgray;display:inline-block;position:relative;top:-30px;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
<script>
function playTone(freq) {
    const osc = window.audioContext.createOscillator();
    osc.type = window.waveformType || 'sine';
    osc.frequency.value = freq;
    osc.connect(window.gainNode);
    window.gainNode.connect(window.audioContext.destination);
    osc.start();
    window.activeOscillators.set(freq, osc);
}

function stopTone(freq) {
    const osc = window.activeOscillators.get(freq);
    if (osc) {
        osc.stop();
        osc.disconnect();
        window.activeOscillators.delete(freq);
    }
}</script>      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:24px;">2960.0</div>
F♯<sub style="font-size:10px;pointer-events:none;">7</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" onmousedown="playTone(3136.0)" onmouseup="stopTone(3136.0)" onmouseleave="stopTone(3136.0)" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;background-color:white;color:black;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
<script>
function playTone(freq) {
    const osc = window.audioContext.createOscillator();
    osc.type = window.waveformType || 'sine';
    osc.frequency.value = freq;
    osc.connect(window.gainNode);
    window.gainNode.connect(window.audioContext.destination);
    osc.start();
    window.activeOscillators.set(freq, osc);
}

function stopTone(freq) {
    const osc = window.activeOscillators.get(freq);
    if (osc) {
        osc.stop();
        osc.disconnect();
        window.activeOscillators.delete(freq);
    }
}</script>      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">3136.0</div>
G<sub style="font-size:10px;pointer-events:none;">7</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#000';" onmousedown="playTone(3322.4)" onmouseup="stopTone(3322.4)" onmouseleave="stopTone(3322.4)" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:16px;height:50px;background-color: black;color: white;box-shadow:2px 2px darkgray;display:inline-block;position:relative;top:-30px;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
<script>
function playTone(freq) {
    const osc = window.audioContext.createOscillator();
    osc.type = window.waveformType || 'sine';
    osc.frequency.value = freq;
    osc.connect(window.gainNode);
    window.gainNode.connect(window.audioContext.destination);
    osc.start();
    window.activeOscillators.set(freq, osc);
}

function stopTone(freq) {
    const osc = window.activeOscillators.get(freq);
    if (osc) {
        osc.stop();
        osc.disconnect();
        window.activeOscillators.delete(freq);
    }
}</script>      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:24px;">3322.4</div>
G♯<sub style="font-size:10px;pointer-events:none;">7</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" onmousedown="playTone(3520.0)" onmouseup="stopTone(3520.0)" onmouseleave="stopTone(3520.0)" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;background-color:white;color:black;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
<script>
function playTone(freq) {
    const osc = window.audioContext.createOscillator();
    osc.type = window.waveformType || 'sine';
    osc.frequency.value = freq;
    osc.connect(window.gainNode);
    window.gainNode.connect(window.audioContext.destination);
    osc.start();
    window.activeOscillators.set(freq, osc);
}

function stopTone(freq) {
    const osc = window.activeOscillators.get(freq);
    if (osc) {
        osc.stop();
        osc.disconnect();
        window.activeOscillators.delete(freq);
    }
}</script>      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">3520.0</div>
A<sub style="font-size:10px;pointer-events:none;">7</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#000';" onmousedown="playTone(3729.3)" onmouseup="stopTone(3729.3)" onmouseleave="stopTone(3729.3)" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:16px;height:50px;background-color: black;color: white;box-shadow:2px 2px darkgray;display:inline-block;position:relative;top:-30px;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
<script>
function playTone(freq) {
    const osc = window.audioContext.createOscillator();
    osc.type = window.waveformType || 'sine';
    osc.frequency.value = freq;
    osc.connect(window.gainNode);
    window.gainNode.connect(window.audioContext.destination);
    osc.start();
    window.activeOscillators.set(freq, osc);
}

function stopTone(freq) {
    const osc = window.activeOscillators.get(freq);
    if (osc) {
        osc.stop();
        osc.disconnect();
        window.activeOscillators.delete(freq);
    }
}</script>      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:24px;">3729.3</div>
A♯<sub style="font-size:10px;pointer-events:none;">7</sub>      </div>
    </div>
    <div onmouseover="event.target.style.backgroundColor = '#eef';" onmouseout="event.target.style.backgroundColor = '#fff';" onmousedown="playTone(3951.1)" onmouseup="stopTone(3951.1)" onmouseleave="stopTone(3951.1)" style='cursor:pointer;font:10px "Open Sans","Lucida Grande","Arial",sans-serif;text-align:center;border:1px solid black;border-radius:5px;width:20px;height:80px;background-color:white;color:black;box-shadow:2px 2px darkgray;display:inline-block;position:relative;user-select:none;-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;'>
<script>
function playTone(freq) {
    const osc = window.audioContext.createOscillator();
    osc.type = window.waveformType || 'sine';
    osc.frequency.value = freq;
    osc.connect(window.gainNode);
    window.gainNode.connect(window.audioContext.destination);
    osc.start();
    window.activeOscillators.set(freq, osc);
}

function stopTone(freq) {
    const osc = window.activeOscillators.get(freq);
    if (osc) {
        osc.stop();
        osc.disconnect();
        window.activeOscillators.delete(freq);
    }
}</script>      <div style="position:absolute;bottom:1px;text-align:center;width:100%;pointer-events:none;">
        <div style="font-size:10px;transform:rotate(90deg);position:absolute;left:-6px;bottom:50px;">3951.1</div>
B<sub style="font-size:10px;pointer-events:none;">7</sub>      </div>
    </div>
  </div>
</div>



It's coming together! 

Remaining TODOs that I may or may not get to, depending on motivation, time, and interest from others:

* Simplify to a list of one oscillator per note
* Connect waveform select
* Allow user to hold down the mouse and slide across keys
* Computer keyboard control to allow for chords
* Get it working on mobile and check non-Chrome browsers
* Limit octaves to the audible ones

Bonus nice-to-haves:

* Make the black keys overlap the white ones correctly so it looks more pianolike
* Songs

We'll see though, no promises.
