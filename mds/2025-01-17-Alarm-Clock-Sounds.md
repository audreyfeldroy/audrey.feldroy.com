# Alarm Clock Sounds

FastHTML MonsterUI example app that uses Tone.js to make different alarm clock sounds.

The backstory: I've been adjusting my sleep schedule to match up better with my coworkers. This afternoon I found myself quite sleepy at the wrong time. I made this as a little utility for myself.

## Setup


```python
from fasthtml.common import *
from fasthtml.jupyter import *
from monsterui.all import *
```


```python
app,rt = fast_app(hdrs=(Theme.blue.headers(),Script(src="https://unpkg.com/tone")))
```


```python
server = JupyUvi(app)
```



<script>
document.body.addEventListener('htmx:configRequest', (event) => {
    if(event.detail.path.includes('://')) return;
    htmx.config.selfRequestsOnly=false;
    event.detail.path = `${location.protocol}//${location.hostname}:8000${event.detail.path}`;
});
</script>


## Sounds JS

Note: I may break this up, putting the code for each function into its corresponding FT. I feel like that would be a little cleaner.


```python
sounds_js = """const synth = new Tone.PolySynth().toDestination();
const pingPong = new Tone.PingPongDelay("4n", 0.2).toDestination();
synth.connect(pingPong);

let currentInterval;

// Classic alarm sound (repeating high-pitched beeps)
function playClassicAlarm() {
    stopCurrentSound();
    currentInterval = setInterval(() => {
        synth.triggerAttackRelease("C5", "16n");
        setTimeout(() => {
            synth.triggerAttackRelease("G4", "16n");
        }, 200);
    }, 400);
}

// Digital alarm sound (ascending beeps)
function playDigitalAlarm() {
    stopCurrentSound();
    const notes = ["C4", "E4", "G4", "C5"];
    let index = 0;
    currentInterval = setInterval(() => {
        synth.triggerAttackRelease(notes[index % notes.length], "8n");
        index++;
    }, 200);
}

// Gentle wake sound (soft pulsing chord)
function playGentleAlarm() {
    stopCurrentSound();
    const chord = ["C4", "E4", "G4"];
    currentInterval = setInterval(() => {
        synth.volume.value = -10;
        synth.triggerAttackRelease(chord, "2n");
    }, 2000);
}

// Stop all sounds
function stopCurrentSound() {
    if (currentInterval) {
        clearInterval(currentInterval);
        currentInterval = null;
    }
    synth.volume.value = 0;
}"""
```


```python
alarms = (
    ('Classic', 'Repeating high-pitched beeps', 'playClassicAlarm'),
    ('Digital Beep', 'Ascending beeps', 'playDigitalAlarm'),
    ('Gentle Wake', 'Soft pulsing chord', 'playGentleAlarm')
)
```

## SoundBar Page


```python
def SoundBar():
    mbrs1 = [Li('Classic', onmousedown="playClassicAlarm()"), Li('Digital Beep', onmousedown="playDigitalAlarm()"), Li('Gentle Wake', onmousedown="playGentleAlarm()"), Li('Stop', onmousedown="stopCurrentSound()")]
    return NavContainer(*mbrs1)
```


```python
SoundBar()
```




```html
<ul class="uk-nav uk-nav-primary">
  <li onmousedown="playClassicAlarm()">Classic</li>
  <li onmousedown="playDigitalAlarm()">Digital Beep</li>
  <li onmousedown="playGentleAlarm()">Gentle Wake</li>
  <li onmousedown="stopCurrentSound()">Stop</li>
</ul>

```




```python
@rt
def index():
    return Titled("Alarm Clock Sounds", SoundBar(), Script(sounds_js))
```

Click on the first 3 to play their sounds, and "Stop" to stop:


```python
# HTMX(index)
```

At this point I have clickable `Li` elements with `onmousedown` handlers. I could call this done if my goal is just to play different alarm clock sounds.

## Better Alarm Display

Let's take it up a level with UI improvements with MonsterUI.


```python
alarms[0]
```




    ('Classic', 'Repeating high-pitched beeps', 'playClassicAlarm')




```python
Card?
```


```python
c = Card((Img(alarms[0][1])), header=H2(alarms[0][0]), onmousedown=f"{alarms[0][2]}()")
c
```




```html
<div onmousedown="playClassicAlarm()" class="uk-card ">
  <div class="uk-card-header ">
    <h2 class="uk-h2 ">Classic</h2>
  </div>
  <div class="uk-card-body space-y-6">
<img>Repeating high-pitched beeps  </div>
</div>

```




```python
show(c)
```


<div onmousedown="playClassicAlarm()" class="uk-card ">
  <div class="uk-card-header ">
    <h2 class="uk-h2 ">Classic</h2>
  </div>
  <div class="uk-card-body space-y-6">
<img>Repeating high-pitched beeps  </div>
</div>
<script>if (window.htmx) htmx.process(document.body)</script>


Note: It would be nice if the card looked like a MonsterUI card here, so I could build them up cell by cell. Instead let's look at it by redefining the index handler.


```python
@rt
def index():
    return Titled("Alarm Clock Sounds", c, Script(sounds_js))
```

It works when I click on it on the index page. In the notebook it doesn't. Maybe I will break up the JS to fix that. Maybe.

But first let's show all the cards.


```python
def AlarmCard(alarm): return Card((Img(alarm[1])), header=H2(alarm[0]), onmousedown=f"{alarm[2]}()")
show(AlarmCard(alarms[2]))
```


<div onmousedown="playGentleAlarm()" class="uk-card ">
  <div class="uk-card-header ">
    <h2 class="uk-h2 ">Gentle Wake</h2>
  </div>
  <div class="uk-card-body space-y-6">
<img>Soft pulsing chord  </div>
</div>
<script>if (window.htmx) htmx.process(document.body)</script>



```python
@rt
def index():
    return Titled("Alarm Clock Sounds", 
        *[AlarmCard(a) for a in alarms], Script(sounds_js))
```


```python
# HTMX(index)
```


```python
@rt
def index():
    return Titled("Alarm Clock Sounds", 
        *[AlarmCard(a) for a in alarms], 
        Card("Stop the current alarm", header=H2("STOP"), onmousedown="stopCurrentSound()"),
        Script(sounds_js))
```


```python
# HTMX(index)
```


```python
@rt
def index():
    return Titled("Alarm Clock Sounds", 
        DivFullySpaced(
            *[AlarmCard(a) for a in alarms], 
            Card("Stop the current alarm", header=H2("STOP"), onmousedown="stopCurrentSound()"),
        ),
        Script(sounds_js))
```


```python
# HTMX(index)
```


```python
@rt
def index():
    return Titled("Alarm Clock Sounds", 
        DivFullySpaced(
            Div(
                *[AlarmCard(a) for a in alarms], 
            ),
            Card("Stop the current alarm", header=H2("STOP"), onmousedown="stopCurrentSound()"),
        ),
        Script(sounds_js))
```


```python
# HTMX(index)
```

## Stop the Server


```python
server.stop()
```


```python

```
